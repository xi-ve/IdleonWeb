import subprocess
import os
import sys
import logging
import asyncio
import threading
from pathlib import Path

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completion
from prompt_toolkit.formatted_text import ANSI
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.style import Style
from rich import box

from plugin_system import PluginManager
from core.py_injector import PyInjector
from config_manager import config_manager
from webui.web_api_integration import PluginWebAPI

NODE_PATH = 'node'
CORE_DIR = Path(__file__).parent / 'core'
INJECTOR_PATH = CORE_DIR / 'injector.js'
PLUGINS_DIR = Path(__file__).parent / 'plugins'

console = Console()
injector = None
update_loop_task = None
update_loop_stop = threading.Event()
web_server_task = None

def ensure_node_dependencies(startup_msgs=None):
    node_modules_path = CORE_DIR / 'node_modules'
    
    # In standalone mode, node_modules should be bundled
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        if not node_modules_path.exists():
            msg = "[bold red]Node.js dependencies missing from standalone build.[/bold red]"
            if startup_msgs:
                startup_msgs.append(msg)
            console.print(msg)
            # Don't exit in standalone mode, just warn
            return
        else:
            msg = "[bold green]Node.js dependencies found in standalone build.[/bold green]"
            if startup_msgs:
                startup_msgs.append(msg)
            return
    
    # Development mode - install if needed
    if not node_modules_path.exists():
        msg = "[bold yellow]Node.js dependencies not found. Installing...[/bold yellow]"
        if startup_msgs:
            startup_msgs.append(msg)
        try:
            result = subprocess.run(['npm', 'install'], cwd=CORE_DIR, check=True, 
                                  encoding='utf-8', errors='replace',
                                  creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
            msg = "[bold green]Node.js dependencies installed.[/bold green]"
        except subprocess.CalledProcessError:
            msg = "[bold red]Failed to install Node.js dependencies.[/bold red]"
            if startup_msgs:
                startup_msgs.append(msg)
            sys.exit(1)
        except FileNotFoundError:
            msg = "[bold red]npm not found. Please install Node.js and npm.[/bold red]"
            if startup_msgs:
                startup_msgs.append(msg)
            sys.exit(1)
        if startup_msgs:
            startup_msgs.append(msg)
    else:
        msg = "[bold green]Node.js dependencies already installed.[/bold green]"
        if startup_msgs:
            startup_msgs.append(msg)

def run_injector():
    try:
        process = subprocess.Popen(
            [NODE_PATH, str(INJECTOR_PATH)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
            encoding='utf-8',
            errors='replace',
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        )
        process.wait()
    except FileNotFoundError:
        console.print(f"[bold red]Error: Node.js not found at '{NODE_PATH}'. Please install Node.js or check your PATH.[/bold red]")
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            console.print("[yellow]Note: Standalone builds require Node.js to be installed on the system.[/yellow]")
        raise
    except Exception as e:
        console.print(f"[bold red]Error running injector: {e}[/bold red]")
        raise

def collect_plugin_js(plugin_manager, include_core=True):
    js_code, plugin_sizes = plugin_manager.collect_all_plugin_js_with_sizes()
    if config_manager.get_path('debug', False):
        console.print("[DEBUG] Generated plugin JS code length:", len(js_code))
    
    js_path = CORE_DIR / "plugins_combined.js"
    
    if include_core:
        # Include core.js for initial injection
        core_path = CORE_DIR / "core.js"
        if core_path.exists():
            with open(core_path, "r", encoding='utf-8') as f:
                core_code = f.read()
            js_code = core_code + '\n' + js_code
            console.print("[DEBUG] Included core.js in combined JS")
    
    with open(js_path, "w", encoding='utf-8') as f:
        f.write(js_code)

async def start_update_loop(plugin_manager):
    try:
        while not update_loop_stop.is_set():
            await plugin_manager.update_all()
            await asyncio.sleep(1.0)
    except Exception as e:
        console.print(f"[red]Update loop error: {e}[/red]")
    finally:
        await plugin_manager.cleanup_all()

def run_update_loop(plugin_manager):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(start_update_loop(plugin_manager))
    finally:
        loop.close()

def cmd_inject(args=None, plugin_manager=None):
    global injector, update_loop_task, update_loop_stop, web_server_task
    
    console.print("[cyan]Performing full reload before injection...[/cyan]")
    
    # 0. Reload main configuration from conf.json
    config_manager.reload()
    console.print("[green]Main configuration reloaded from conf.json.[/green]")
    
    # Update global debug setting
    import plugin_system
    plugin_system.GLOBAL_DEBUG = config_manager.get_path('debug', False)
    console.print(f"[green]Debug mode: {'enabled' if plugin_system.GLOBAL_DEBUG else 'disabled'}[/green]")

    # 1. Reload plugin Python modules and re-instantiate them
    asyncio.run(plugin_manager.reload_plugins())
    console.print("[green]Python plugins reloaded.[/green]")

    # 2. Regenerate and reload the combined plugin JS
    collect_plugin_js(plugin_manager, include_core=True)
    console.print("[green]Plugin JS regenerated.[/green]")

    # Get injector configuration
    cdp_port = config_manager.get_cdp_port()
    idleon_url = config_manager.get_idleon_url()
    
    console.print(f"[cyan]Running injector.js with config from conf.json...[/cyan]")
    console.print(f"[cyan]CDP Port: {cdp_port}, Idleon URL: {idleon_url}[/cyan]")
    run_injector()
    injector = PyInjector()
    try:
        injector.connect()
        console.print("[green]Injector connected successfully.[/green]")
        
        # Inject the fresh JS into the browser
        try:
            console.print("[cyan]Injecting fresh JS into browser...[/cyan]")
            injector.reload_js()
            console.print("[green]Plugin JS injected into browser.[/green]")
        except Exception as e:
            console.print(f"[yellow]Could not inject JS into browser: {e}[/yellow]")
            console.print(f"[yellow]JS will be injected when the game loads[/yellow]")
        
        asyncio.run(plugin_manager.initialize_all(injector, config_manager.get_path('plugin_configs', {})))
        console.print("[green]Plugins initialized in injector session.[/green]")
        
        # Start update loop
        if update_loop_task is None or not update_loop_task.is_alive():
            update_loop_stop.clear()
            update_loop_task = threading.Thread(
                target=run_update_loop, 
                args=(plugin_manager,), 
                daemon=True
            )
            update_loop_task.start()
        
        # Start web server for plugin UI
        if web_server_task is None or not web_server_task.is_alive():
            web_server = PluginWebAPI(plugin_manager)
            web_server_task = threading.Thread(
                target=lambda: asyncio.run(web_server.start_server()),
                daemon=True
            )
            web_server_task.start()
            console.print("[green]Plugin UI web server started at http://localhost:8080[/green]")
            
    except Exception as e:
        console.print(f"[red]Failed to connect injector: {e}[/red]")
        injector = None

def cmd_config(args=None, plugin_manager=None):
    config = config_manager.get_full_config()
    table = Table(title="Current Injector Config")
    table.add_column("Key", style="bold cyan")
    table.add_column("Value", style="white")
    for k, v in config.items():
        table.add_row(str(k), str(v))
    console.print(table)

def cmd_injector_config(args=None, plugin_manager=None):
    """Show injector-specific configuration."""
    table = Table(title="Injector Configuration")
    table.add_column("Setting", style="bold cyan")
    table.add_column("Value", style="white")
    table.add_column("Description", style="yellow")
    
    table.add_row("CDP Port", str(config_manager.get_cdp_port()), "Chrome DevTools Protocol port")
    table.add_row("N.js Pattern", config_manager.get_njs_pattern(), "Pattern for intercepting game JS")
    table.add_row("Idleon URL", config_manager.get_idleon_url(), "Game URL to launch")
    table.add_row("Timeout (ms)", str(config_manager.get_timeout()), "CDP connection timeout in milliseconds")
    
    console.print(table)

def cmd_darkmode(args=None, plugin_manager=None):
    """Toggle or set dark mode for the web UI."""
    if args:
        if args[0].lower() in ['on', 'true', '1', 'yes']:
            config_manager.set_darkmode(True)
            console.print("[green]Dark mode enabled[/green]")
        elif args[0].lower() in ['off', 'false', '0', 'no']:
            config_manager.set_darkmode(False)
            console.print("[green]Dark mode disabled[/green]")
        else:
            console.print("[red]Invalid argument. Use 'on' or 'off'[/red]")
    else:
        # Toggle current state
        current = config_manager.get_darkmode()
        new_state = not current
        config_manager.set_darkmode(new_state)
        status = "enabled" if new_state else "disabled"
        console.print(f"[green]Dark mode {status}[/green]")

def cmd_auto_inject(args=None, plugin_manager=None):
    """Toggle or set auto-inject on startup."""
    if args:
        if args[0].lower() in ['on', 'true', '1', 'yes']:
            config_manager.set_auto_inject(True)
            console.print("[green]Auto-inject enabled[/green]")
        elif args[0].lower() in ['off', 'false', '0', 'no']:
            config_manager.set_auto_inject(False)
            console.print("[green]Auto-inject disabled[/green]")
        else:
            console.print("[red]Invalid argument. Use 'on' or 'off'[/red]")
    else:
        # Toggle current state
        current = config_manager.get_auto_inject()
        new_state = not current
        config_manager.set_auto_inject(new_state)
        status = "enabled" if new_state else "disabled"
        console.print(f"[green]Auto-inject {status}[/green]")

def cmd_plugins(args=None, plugin_manager=None):
    table = Table(title="Loaded Plugins")
    table.add_column("Plugin Name", style="bold green")
    table.add_column("Status", style="cyan")
    table.add_column("Version", style="yellow")
    for name, plugin in plugin_manager.plugins.items():
        version = getattr(plugin, 'version', '1.0.0')
        table.add_row(name, "Loaded", version)
    console.print(table)

def cmd_reload_config(args=None, plugin_manager=None):
    console.print("[cyan]Reloading plugin configurations from conf.json...[/cyan]")
    plugin_manager.reload_configs_from_file()
    console.print("[green]Configuration reload complete.[/green]")

def cmd_reload(args=None, plugin_manager=None):
    global injector
    console.print("[cyan]Hot reloading all plugins, JS, and main configuration...[/cyan]")
    try:
        # 0. Reload main configuration from conf.json
        config_manager.reload()
        console.print("[green]Main configuration reloaded from conf.json.[/green]")
        
        # Update global debug setting
        import plugin_system
        plugin_system.GLOBAL_DEBUG = config_manager.get_path('debug', False)
        console.print(f"[green]Debug mode: {'enabled' if plugin_system.GLOBAL_DEBUG else 'disabled'}[/green]")

        # 1. Reload plugin Python modules and re-instantiate them
        asyncio.run(plugin_manager.reload_plugins())
        console.print("[green]Python plugins reloaded.[/green]")

        # 2. Regenerate and reload the combined plugin JS (without core.js for reloads)
        js_code, plugin_sizes = plugin_manager.collect_all_plugin_js_with_sizes()
        if config_manager.get_path('debug', False):
            console.print("[DEBUG] Generated plugin JS code length:", len(js_code))
        
        # For reloads, we don't include core.js to avoid conflicts with existing functions
        js_path = CORE_DIR / "plugins_combined.js"
        with open(js_path, "w", encoding='utf-8') as f:
            f.write(js_code)
        console.print("[green]Plugin JS regenerated (without core.js for reload).[/green]")
        
        if injector:
            try:
                # Re-inject the new JS into the running injector session
                console.print("[cyan]Attempting to reload JS into injector...[/cyan]")
                injector.reload_js()
                console.print("[green]Plugin JS reloaded into injector.[/green]")
            except Exception as e:
                console.print(f"[yellow]Could not reload JS into injector: {e}[/yellow]")
                console.print(f"[yellow]This might be normal if the injector is not fully connected[/yellow]")
        else:
            console.print("[yellow]No injector connected - JS will be loaded on next 'inject' command[/yellow]")

        # 3. Re-initialize plugins in the active injector session
        if injector:
            asyncio.run(plugin_manager.initialize_all(injector, config_manager.get_path('plugin_configs', {})))
            console.print("[green]Plugins re-initialized in injector session.[/green]")
        else:
            console.print("[yellow]Injector not connected; plugins not re-initialized.[/yellow]")

        console.print("[bold green]Hot reload complete![/bold green]")
    except Exception as e:
        console.print(f"[red]Hot reload failed: {e}[/red]")

def cmd_help(args=None, plugin_manager=None, all_commands=None):
    table = Table(title="Available Commands")
    table.add_column("Command", style="bold green")
    table.add_column("Help", style="white")
    for cmd, meta in all_commands.items():
        table.add_row(cmd, meta.get("help", "No help available"))
    console.print(table)
    console.print("[cyan]Type a command and press [bold]Tab[/bold] for autocomplete.[/cyan]")

def cmd_web_ui(args=None, plugin_manager=None):
    global web_server_task
    if web_server_task and web_server_task.is_alive():
        console.print("[yellow]Web server is already running at http://localhost:8080[/yellow]")
        return
    
    try:
        web_server = PluginWebAPI(plugin_manager)
        web_server_task = threading.Thread(
            target=lambda: asyncio.run(web_server.start_server()),
            daemon=True
        )
        web_server_task.start()
        console.print("[green]Plugin UI web server started at http://localhost:8080[/green]")
        console.print("[cyan]Open your browser to configure plugins with a modern web interface![/cyan]")
    except Exception as e:
        console.print(f"[red]Failed to start web server: {e}[/red]")

def cmd_exit(args=None, plugin_manager=None):
    global update_loop_stop, update_loop_task, web_server_task
    console.print("[bold green]Shutting down...[/bold green]")
    update_loop_stop.set()
    if update_loop_task and update_loop_task.is_alive():
        update_loop_task.join(timeout=2)
    if web_server_task and web_server_task.is_alive():
        console.print("[cyan]Stopping web server...[/cyan]")
        # The web server will stop when the main process exits
    if plugin_manager:
        asyncio.run(plugin_manager.cleanup_all())
    console.print("[bold green]Goodbye![/bold green]")
    sys.exit(0)

def check_unused_plugins(plugin_manager, startup_msgs):
    """Check for plugins in the plugins folder that are not in the config and recommend enabling them."""
    try:
        # Get list of plugins in the config
        configured_plugins = set(config_manager.get_path('plugins', []))
        
        # Get list of all plugin files in the plugins directory (including subdirectories)
        plugin_files = []
        
        # First, check for plugins in the root plugins directory
        for plugin_file in PLUGINS_DIR.glob("*.py"):
            if plugin_file.name != "__init__.py" and plugin_file.name != "example_plugin.py":
                plugin_name = plugin_file.stem
                plugin_files.append(plugin_name)
        
        # Then, check for plugins in subdirectories
        for subdir in PLUGINS_DIR.iterdir():
            if subdir.is_dir() and not subdir.name.startswith('.'):
                for plugin_file in subdir.glob("*.py"):
                    if plugin_file.name != "__init__.py" and plugin_file.name != "example_plugin.py":
                        # Use the subdirectory name as prefix for the plugin name
                        plugin_name = f"{subdir.name}.{plugin_file.stem}"
                        plugin_files.append(plugin_name)
        
        # Find unused plugins
        unused_plugins = [name for name in plugin_files if name not in configured_plugins]
        
        if unused_plugins:
            startup_msgs.append(f"[yellow]Found {len(unused_plugins)} unused plugins: {', '.join(unused_plugins)}[/yellow]")
            
            # Ask user if they want to enable any unused plugins
            console.print(f"[cyan]Found {len(unused_plugins)} unused plugins:[/cyan]")
            for plugin_name in unused_plugins:
                console.print(f"  [yellow]• {plugin_name}[/yellow]")
            
            console.print(f"\n[cyan]Would you like to enable any of these plugins?[/cyan]")
            console.print(f"[cyan]Type 'all' to enable all, 'none' to skip, or enter plugin names separated by spaces:[/cyan]")
            
            try:
                user_input = input("> ").strip().lower()
                
                if user_input == 'all':
                    # Enable all unused plugins
                    current_plugins = config_manager.get_path('plugins', [])
                    for plugin_name in unused_plugins:
                        if plugin_name not in current_plugins:
                            current_plugins.append(plugin_name)
                            config_manager.add_plugin(plugin_name, {})
                    config_manager.set_plugins_list(current_plugins)
                    startup_msgs.append(f"[green]Enabled all unused plugins: {', '.join(unused_plugins)}[/green]")
                    console.print(f"[green]Enabled all unused plugins![/green]")
                    
                    # Reload plugin manager with new plugins
                    console.print(f"[cyan]Reloading plugin manager with new plugins...[/cyan]")
                    plugin_manager.plugin_names = current_plugins
                    try:
                        asyncio.run(plugin_manager.load_plugins(
                            None, 
                            plugin_configs=config_manager.get_all_plugin_configs(), 
                            global_debug=config_manager.get_path('debug', False)
                        ))
                        startup_msgs.append(f"[green]Successfully loaded {len(plugin_manager.plugins)} plugins (including newly enabled ones)[/green]")
                        console.print(f"[green]Successfully loaded {len(plugin_manager.plugins)} plugins![/green]")
                    except Exception as e:
                        startup_msgs.append(f"[red]Error loading new plugins: {e}[/red]")
                        console.print(f"[red]Error loading new plugins: {e}[/red]")
                    
                elif user_input == 'none':
                    startup_msgs.append(f"[yellow]Skipped enabling unused plugins[/yellow]")
                    console.print(f"[yellow]Skipped enabling unused plugins[/yellow]")
                    
                elif user_input:
                    # Enable specific plugins
                    selected_plugins = user_input.split()
                    current_plugins = config_manager.get_path('plugins', [])
                    enabled_plugins = []
                    
                    for plugin_name in selected_plugins:
                        if plugin_name in unused_plugins and plugin_name not in current_plugins:
                            current_plugins.append(plugin_name)
                            config_manager.add_plugin(plugin_name, {})
                            enabled_plugins.append(plugin_name)
                    
                    if enabled_plugins:
                        config_manager.set_plugins_list(current_plugins)
                        startup_msgs.append(f"[green]Enabled plugins: {', '.join(enabled_plugins)}[/green]")
                        console.print(f"[green]Enabled plugins: {', '.join(enabled_plugins)}[/green]")
                        
                        # Reload plugin manager with new plugins
                        console.print(f"[cyan]Reloading plugin manager with new plugins...[/cyan]")
                        plugin_manager.plugin_names = current_plugins
                        try:
                            asyncio.run(plugin_manager.load_plugins(
                                None, 
                                plugin_configs=config_manager.get_all_plugin_configs(), 
                                global_debug=config_manager.get_path('debug', False)
                            ))
                            startup_msgs.append(f"[green]Successfully loaded {len(plugin_manager.plugins)} plugins (including newly enabled ones)[/green]")
                            console.print(f"[green]Successfully loaded {len(plugin_manager.plugins)} plugins![/green]")
                        except Exception as e:
                            startup_msgs.append(f"[red]Error loading new plugins: {e}[/red]")
                            console.print(f"[red]Error loading new plugins: {e}[/red]")
                    else:
                        startup_msgs.append(f"[yellow]No valid plugins selected[/yellow]")
                        console.print(f"[yellow]No valid plugins selected[/yellow]")
                        
            except (KeyboardInterrupt, EOFError):
                startup_msgs.append(f"[yellow]Plugin selection cancelled[/yellow]")
                console.print(f"[yellow]Plugin selection cancelled[/yellow]")
                
    except Exception as e:
        startup_msgs.append(f"[red]Error checking unused plugins: {e}[/red]")
        console.print(f"[red]Error checking unused plugins: {e}[/red]")

class HierarchicalCompleter:
    def __init__(self, get_commands_func):
        self.get_commands = get_commands_func
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.strip()
        last_token = text.split()[-1] if text else ''
        all_commands = self.get_commands()
        completions = []
        for cmd in all_commands.keys():
            if cmd.startswith(last_token):
                completions.append(cmd)
        for comp in sorted(completions):
            yield Completion(comp, start_position=-len(last_token))
    
    async def get_completions_async(self, document, complete_event):
        text = document.text_before_cursor.strip()
        last_token = text.split()[-1] if text else ''
        all_commands = self.get_commands()
        completions = []
        for cmd in all_commands.keys():
            if cmd.startswith(last_token):
                completions.append(cmd)
        for comp in sorted(completions):
            yield Completion(comp, start_position=-len(last_token))

def main():
    startup_msgs = []
    ensure_node_dependencies(startup_msgs)
    
    # Add basic startup information
    startup_msgs.append(f"[cyan]Configuration loaded from [white]{config_manager.conf_path}[/white][/cyan]")
    startup_msgs.append(f"[cyan]Plugins directory: [white]{PLUGINS_DIR}[/white][/cyan]")
    
    log_level = logging.INFO if config_manager.get_path("debug", False) else logging.WARNING
    logging.basicConfig(level=log_level)
    import plugin_system
    plugin_system.GLOBAL_DEBUG = config_manager.get_path('debug', False)
    plugin_names = config_manager.get_path('plugins', [])
    plugin_configs = config_manager.get_path('plugin_configs', {})
    plugin_manager = PluginManager(plugin_names, plugin_dir=str(PLUGINS_DIR))
    try:
        asyncio.run(plugin_manager.load_plugins(
            None, 
            plugin_configs=plugin_configs, 
            global_debug=config_manager.get_path('debug', False)
        ))
        startup_msgs.append(f"[green]Successfully loaded {len(plugin_manager.plugins)} plugins[/green]")
    except Exception as e:
        startup_msgs.append(f"[red]Error loading plugins: {e}[/red]")
    
    # Check for unused plugins and recommend enabling them
    check_unused_plugins(plugin_manager, startup_msgs)
    
    # Check if auto inject is enabled
    if config_manager.get_auto_inject():
        startup_msgs.append("[cyan]Auto-inject is enabled. Starting injection automatically...[/cyan]")
        console.print("[cyan]Auto-inject is enabled. Starting injection automatically...[/cyan]")
        try:
            cmd_inject(plugin_manager=plugin_manager)
            startup_msgs.append("[green]Auto-injection completed successfully[/green]")
        except Exception as e:
            startup_msgs.append(f"[red]Auto-injection failed: {e}[/red]")
            console.print(f"[red]Auto-injection failed: {e}[/red]")
    
    startup_text = Text()
    for msg in startup_msgs:
        startup_text.append(Text.from_markup(msg))
        startup_text.append('\n')
    console.print(Panel(startup_text, title="Startup Summary", style="bold blue"))
    builtin_commands = {
        'inject': {'func': cmd_inject, 'help': 'Run the injector with current config.'},
        'config': {'func': cmd_config, 'help': 'Show current injector config.'},
        'injector_config': {'func': cmd_injector_config, 'help': 'Show injector-specific configuration.'},
        'darkmode': {'func': cmd_darkmode, 'help': 'Toggle or set dark mode for web UI (on/off).'},
        'auto_inject': {'func': cmd_auto_inject, 'help': 'Toggle or set auto-inject on startup (on/off).'},
        'plugins': {'func': cmd_plugins, 'help': 'List loaded plugins.'},
        'reload_config': {'func': cmd_reload_config, 'help': 'Reload plugin configurations from conf.json.'},
        'web_ui': {'func': cmd_web_ui, 'help': 'Start the plugin web UI server.'},
        'help': {'func': cmd_help, 'help': 'Show this help menu.'},
        'exit': {'func': cmd_exit, 'help': 'Exit the CLI.'},
        'reload': {'func': cmd_reload, 'help': 'Hot reload all plugins, JS, and web UI into the active injector session.'}
    }
    def get_all_commands():
        cmds = dict(builtin_commands)
        plugin_cmds = plugin_manager.get_all_commands()
        cmds.update(plugin_cmds)
        return cmds
    completer = HierarchicalCompleter(get_all_commands)
    session = PromptSession()
    banner = Panel(
        Text("Idleon Injector CLI", style="bold magenta"),
        subtitle="type 'help' for commands",
        style=Style(color="cyan"),
        box=box.DOUBLE
    )
    console.print(banner)
    if not config_manager.get_path("interactive", True) and os.environ.get('IDLEONWEB_FORCE_INTERACTIVE') != '1':
        console.print("[yellow]Interactive mode is disabled in config. Exiting.[/yellow]")
        return
    while True:
        try:
            user_input = session.prompt(
                ANSI('\x1b[1;32m»\x1b[0m '),
                completer=completer,
                complete_while_typing=True
            )
            if not user_input.strip():
                continue
            parts = user_input.strip().split()
            cmd = parts[0]
            args = parts[1:]
            all_commands = get_all_commands()
            if cmd in all_commands:
                meta = all_commands[cmd]
                func = meta['func']
                try:
                    if cmd in builtin_commands:
                        if cmd == 'help':
                            func(args, plugin_manager, all_commands)
                        else:
                            func(args, plugin_manager)
                    else:
                        from plugin_system import execute_plugin_command, parse_plugin_args
                        params_meta = meta.get('params', [])
                        if params_meta and args:
                            try:
                                parsed_args = parse_plugin_args(params_meta, args)
                                execute_plugin_command(
                                    func, parsed_args,
                                    injector=injector,
                                    plugin_manager=plugin_manager,
                                    console=console
                                )
                            except ValueError as e:
                                console.print(f"[red]{e}[/red]")
                        else:
                            execute_plugin_command(
                                func, {},
                                injector=injector,
                                plugin_manager=plugin_manager,
                                console=console
                            )
                    console.rule(style="dim")
                except Exception as e:
                    console.print(f"[red]Error executing command: {e}[/red]")
            else:
                console.print(f"[red]Unknown command: {cmd}[/red]")
        except (KeyboardInterrupt, EOFError):
            cmd_exit([], plugin_manager)
        except Exception as e:
            console.print(Panel(f"Error: {e}", style="bold red"))

if __name__ == '__main__':
    main()