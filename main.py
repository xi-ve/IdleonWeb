import subprocess
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

NODE_PATH = 'node'
CORE_DIR = Path(__file__).parent / 'core'
INJECTOR_PATH = CORE_DIR / 'injector.js'
CONF_PATH = CORE_DIR / 'conf.json'
PLUGINS_DIR = Path(__file__).parent / 'plugins'

console = Console()
injector = None
update_loop_task = None
update_loop_stop = threading.Event()

def ensure_node_dependencies(startup_msgs=None):
    node_modules_path = CORE_DIR / 'node_modules'
    if not node_modules_path.exists():
        msg = "[bold yellow]Node.js dependencies not found. Installing...[/bold yellow]"
        if startup_msgs:
            startup_msgs.append(msg)
        try:
            result = subprocess.run(['npm', 'install'], cwd=CORE_DIR, check=True)
            msg = "[bold green]Node.js dependencies installed.[/bold green]"
        except subprocess.CalledProcessError:
            msg = "[bold red]Failed to install Node.js dependencies.[/bold red]"
            if startup_msgs:
                startup_msgs.append(msg)
            sys.exit(1)
        if startup_msgs:
            startup_msgs.append(msg)
    else:
        msg = "[bold green]Node.js dependencies already installed.[/bold green]"
        if startup_msgs:
            startup_msgs.append(msg)

def ensure_config(startup_msgs=None):
    msg = f"[bold cyan]Config file ready at [white]{CONF_PATH}[/white][/bold cyan]"
    if startup_msgs:
        startup_msgs.append(msg)

def load_config():
    return config_manager.get_full_config()

def save_config(config):
    config_manager.set_full_config(config)
    console.print("[green]Config updated.[/green]")

def run_injector(silent=True):
    if silent:
        process = subprocess.Popen(
            [NODE_PATH, str(INJECTOR_PATH)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True
        )
    else:
        process = subprocess.Popen(
            [NODE_PATH, str(INJECTOR_PATH)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        if process.stdout:
            for line in process.stdout:
                print(line, end='')
    process.wait()

def collect_plugin_js(plugin_manager):
    js_code = plugin_manager.collect_all_plugin_js()
    if config_manager.get_path('debug', False):
        console.print("[DEBUG] Generated plugin JS code length:", len(js_code))
    js_path = CORE_DIR / "plugins_combined.js"
    with open(js_path, "w") as f:
        f.write(js_code)
    plugins = list(plugin_manager.plugins.values())
    table = Table(title="Plugin System Details", show_lines=True)
    table.add_column("Plugin Name", style="bold green")
    table.add_column("Function Count", style="cyan")
    table.add_column("JS KB Size", style="magenta")
    for plugin in plugins:
        name = getattr(plugin, 'name', plugin.__class__.__name__)
        func_count = len(plugin.get_commands())
        js_size = len(js_code) / len(plugins) if plugins else 0
        table.add_row(name, str(func_count), f"{js_size/1024:.2f}")
    console.print(table)

def update_inject_files():
    inject_files = config_manager.get_path("injectFiles", [])
    if "plugins_combined.js" not in inject_files:
        inject_files.append("plugins_combined.js")
        config_manager.set_path("injectFiles", inject_files)

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
    global injector, update_loop_task, update_loop_stop
    collect_plugin_js(plugin_manager)
    update_inject_files()
    console.print("[cyan]Running injector.js with config from conf.json...[/cyan]")
    run_injector(silent=True)
    injector = PyInjector()
    try:
        injector.connect()
        console.print("[green]Injector connected successfully.[/green]")
        asyncio.run(plugin_manager.initialize_all(injector, load_config().get('plugin_configs', {})))
        if update_loop_task is None or not update_loop_task.is_alive():
            update_loop_stop.clear()
            update_loop_task = threading.Thread(
                target=run_update_loop, 
                args=(plugin_manager,), 
                daemon=True
            )
            update_loop_task.start()
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

def cmd_help(args=None, plugin_manager=None, all_commands=None):
    table = Table(title="Available Commands")
    table.add_column("Command", style="bold green")
    table.add_column("Help", style="white")
    for cmd, meta in all_commands.items():
        table.add_row(cmd, meta.get("help", "No help available"))
    console.print(table)
    console.print("[cyan]Type a command and press [bold]Tab[/bold] for autocomplete.[/cyan]")

def cmd_exit(args=None, plugin_manager=None):
    global update_loop_stop, update_loop_task
    console.print("[bold green]Shutting down...[/bold green]")
    update_loop_stop.set()
    if update_loop_task and update_loop_task.is_alive():
        update_loop_task.join(timeout=2)
    if plugin_manager:
        asyncio.run(plugin_manager.cleanup_all())
    console.print("[bold green]Goodbye![/bold green]")
    sys.exit(0)

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
    ensure_config(startup_msgs)
    log_level = logging.INFO if config_manager.get_path("debug", True) else logging.WARNING
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
            global_debug=config_manager.get_path('debug', True)
        ))
    except Exception as e:
        startup_msgs.append(f"[red]Error loading plugins: {e}[/red]")
    startup_text = Text()
    for msg in startup_msgs:
        startup_text.append(Text.from_markup(msg))
        startup_text.append('\n')
    console.print(Panel(startup_text, title="Startup Summary", style="bold blue"))
    builtin_commands = {
        'inject': {'func': cmd_inject, 'help': 'Run the injector with current config.'},
        'config': {'func': cmd_config, 'help': 'Show current injector config.'},
        'plugins': {'func': cmd_plugins, 'help': 'List loaded plugins.'},
        'reload_config': {'func': cmd_reload_config, 'help': 'Reload plugin configurations from conf.json.'},
        'help': {'func': cmd_help, 'help': 'Show this help menu.'},
        'exit': {'func': cmd_exit, 'help': 'Exit the CLI.'}
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
    if not config_manager.get_path("interactive", True):
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