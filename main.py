import subprocess
import sys
import os
import json
import logging
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from rich.console import Console
from rich.table import Table
from plugin_system import PluginManager
import inspect
from core.py_injector import PyInjector
from prompt_toolkit.completion import Completion
from rich.panel import Panel
from rich.text import Text
from rich.style import Style
from rich import box
from prompt_toolkit.formatted_text import ANSI
import threading
import asyncio
import signal

NODE_PATH = 'node'
INJECTOR_PATH = os.path.join(os.path.dirname(__file__), 'core', 'injector.js')
CORE_DIR = os.path.join(os.path.dirname(__file__), 'core')
CONF_PATH = os.path.join(CORE_DIR, 'conf.json')

console = Console()
injector = None

# --- Utility Functions ---
def ensure_node_dependencies(startup_msgs=None):
    node_modules_path = os.path.join(CORE_DIR, 'node_modules')
    if not os.path.exists(node_modules_path):
        msg = "[bold yellow]Node.js dependencies not found. Installing...[/bold yellow]"
        if startup_msgs is not None:
            startup_msgs.append(msg)
        result = subprocess.run(['npm', 'install'], cwd=CORE_DIR)
        if result.returncode != 0:
            msg = "[bold red]Failed to install Node.js dependencies.[/bold red]"
            if startup_msgs is not None:
                startup_msgs.append(msg)
            sys.exit(1)
        msg = "[bold green]Node.js dependencies installed.[/bold green]"
        if startup_msgs is not None:
            startup_msgs.append(msg)
    else:
        msg = "[bold green]Node.js dependencies already installed.[/bold green]"
        if startup_msgs is not None:
            startup_msgs.append(msg)

def ensure_config(startup_msgs=None):
    if not os.path.exists(CONF_PATH):
        config = {
            "injectFiles": ["test.js"],
            "openDevTools": False,
            "interactive": True,
            "plugins": ["schalom_popup"],
            "plugin_configs": {"schalom_popup": {"debug": True}},
            "debug": True
        }
        with open(CONF_PATH, 'w') as f:
            json.dump(config, f, indent=2)
        msg = f"[bold cyan]Config file created at [white]{CONF_PATH}[/white][/bold cyan]"
        if startup_msgs is not None:
            startup_msgs.append(msg)
    else:
        with open(CONF_PATH, 'r') as f:
            config = json.load(f)
        changed = False
        if 'plugins' not in config:
            config['plugins'] = ["schalom_popup"]
            changed = True
        if 'plugin_configs' not in config:
            config['plugin_configs'] = {"schalom_popup": {"debug": True}}
            changed = True
        if changed:
            with open(CONF_PATH, 'w') as f:
                json.dump(config, f, indent=2)
            msg = f"[bold yellow]Updated config at [white]{CONF_PATH}[/white] with missing keys.[/bold yellow]"
            if startup_msgs is not None:
                startup_msgs.append(msg)
        else:
            msg = f"[bold cyan]Config file already exists at [white]{CONF_PATH}[/white][/bold cyan]"
            if startup_msgs is not None:
                startup_msgs.append(msg)

def load_config():
    with open(CONF_PATH, 'r') as f:
        config = json.load(f)
    changed = False
    if 'plugins' not in config:
        config['plugins'] = ["schalom_popup"]
        changed = True
    if 'plugin_configs' not in config:
        config['plugin_configs'] = {"schalom_popup": {"debug": True}}
        changed = True
    if changed:
        with open(CONF_PATH, 'w') as f2:
            json.dump(config, f2, indent=2)
        console.print(f"[yellow]Updated config at {CONF_PATH} with missing keys.[/yellow]")
    return config

def save_config(config):
    with open(CONF_PATH, 'w') as f:
        json.dump(config, f, indent=2)
    console.print("[green]Config updated.[/green]")

def run_injector(silent=True):
    if silent:
        process = subprocess.Popen(
            [NODE_PATH, INJECTOR_PATH],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1
        )
        process.wait()
    else:
        process = subprocess.Popen(
            [NODE_PATH, INJECTOR_PATH],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        for line in process.stdout:
            print(line, end='')
        process.wait()

def collect_plugin_js(plugin_manager):
    js_code = plugin_manager.collect_all_plugin_js()
    config = load_config()
    if config.get('debug', False):
        print("[DEBUG] Generated plugin JS code:\n" + js_code)
    js_path = os.path.join(CORE_DIR, "plugins_combined.js")
    with open(js_path, "w") as f:
        f.write(js_code)
    # Table with plugin info (simple version)
    from rich.table import Table
    from rich.text import Text
    plugins = list(plugin_manager.plugins.values())
    table = Table(title="Plugin System Details", show_lines=True)
    table.add_column("Plugin Name", style="bold green")
    table.add_column("Function Count", style="cyan")
    table.add_column("JS KB Size", style="magenta")
    for plugin in plugins:
        name = getattr(plugin, 'name', plugin.__class__.__name__)
        func_count = len(plugin.get_commands())
        # Estimate JS size for this plugin (by function name in js_code)
        js_size = 0
        for cmd in plugin.get_commands().keys():
            js_func_name = f"window.{cmd} = function"
            if js_func_name in js_code:
                js_size += len(js_func_name)
        # Fallback: show 0 if not found
        table.add_row(name, str(func_count), f"{js_size/1024:.2f}")
    console.print(table)

def update_inject_files():
    config = load_config()
    inject_files = config.get("injectFiles", [])
    if "plugins_combined.js" not in inject_files:
        inject_files.append("plugins_combined.js")
        config["injectFiles"] = inject_files
        save_config(config)

# --- CLI Command Handlers ---
update_loop_task = None
update_loop_stop = threading.Event()

async def start_update_loop(plugin_manager):
    try:
        while not update_loop_stop.is_set():
            await plugin_manager.update_all()
            await asyncio.sleep(1.0)
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
    args = args or []
    global injector, update_loop_task, update_loop_stop
    collect_plugin_js(plugin_manager)
    update_inject_files()
    console.print("[cyan]Running injector.js with config from conf.json...[/cyan]")
    run_injector(silent=True)
    injector = PyInjector()
    try:
        injector.connect()
        console.print("[green]injector.js finished running and injector connected.[/green]")
        # After successful injection, initialize plugins (suppress plugin loading prints)
        import builtins
        orig_print = builtins.print
        builtins.print = lambda *a, **k: None
        asyncio.run(plugin_manager.initialize_all(injector, load_config().get('plugin_configs', {})))
        builtins.print = orig_print
        # Start the update loop in a background thread
        if update_loop_task is None or not update_loop_task.is_alive():
            update_loop_stop.clear()
            update_loop_task = threading.Thread(target=run_update_loop, args=(plugin_manager,), daemon=True)
            update_loop_task.start()
    except Exception as e:
        console.print(f"[red]Failed to connect injector: {e}[/red]")
        injector = None

def cmd_config(args=None, plugin_manager=None):
    args = args or []
    config = load_config()
    table = Table(title="Current Injector Config")
    table.add_column("Key")
    table.add_column("Value")
    for k, v in config.items():
        table.add_row(str(k), str(v))
    console.print(table)
    # Optionally allow editing config here

def cmd_plugins(args=None, plugin_manager=None):
    args = args or []
    table = Table(title="Loaded Plugins")
    table.add_column("Plugin Name")
    table.add_column("Status")
    for name in plugin_manager.plugins:
        table.add_row(name, "Loaded")
    console.print(table)
    # Optionally allow load/unload/update here

def cmd_help(args=None, plugin_manager=None, all_commands=None):
    args = args or []
    table = Table(title="Available Commands")
    table.add_column("Command")
    table.add_column("Help")
    for cmd, meta in all_commands.items():
        table.add_row(cmd, meta.get("help", ""))
    console.print(table)
    console.print("[cyan]Type a command and press [bold]Tab[/bold] for autocomplete.[/cyan]")

def cmd_exit(args=None, plugin_manager=None):
    args = args or []
    global update_loop_stop, update_loop_task
    console.print("[bold green]Goodbye![/bold green]")
    update_loop_stop.set()
    if update_loop_task is not None:
        update_loop_task.join(timeout=2)
    sys.exit(0)

def rich_help(args=None, plugin_manager=None, all_commands=None):
    args = args or []
    if args and args[0] in all_commands:
        cmd = args[0]
        meta = all_commands[cmd]
        usage = Text(f"Usage: {cmd} ", style="bold yellow")
        for p in meta.get('params', []):
            pname = p['name']
            typ = p.get('type', str).__name__
            if 'default' in p:
                usage.append(f"[{pname}:{typ}={p['default']}] ", style="cyan")
            else:
                usage.append(f"<{pname}:{typ}> ", style="magenta")
        helptext = meta.get('help', '')
        panel = Panel(usage, title=f"Help: {cmd}", subtitle=helptext, style="bold blue")
        console.print(panel)
    else:
        table = Text("Available Commands:\n", style="bold magenta")
        for cmd, meta in all_commands.items():
            table.append(f"  {cmd}", style="bold green")
            table.append(f": {meta.get('help', '')}\n", style="white")
        panel = Panel(table, title="Help", style="bold blue")
        console.print(panel)

# --- Main CLI Loop ---
def main():
    startup_msgs = []
    ensure_node_dependencies(startup_msgs)
    ensure_config(startup_msgs)
    config = load_config()
    # Set logging level based on debug config
    if not config.get("debug", True):
        logging.basicConfig(level=logging.WARNING)
    else:
        logging.basicConfig(level=logging.INFO)
    plugin_names = config.get("plugins", [])
    plugin_configs = config.get("plugin_configs", {})
    plugin_manager = PluginManager(plugin_names, plugin_dir=os.path.join(os.path.dirname(__file__), 'plugins'))
    # Patch plugin_manager to collect plugin loading messages
    orig_print = print
    def rich_plugin_print(*args, **kwargs):
        msg = ' '.join(str(a) for a in args)
        if msg.startswith('Loading plugin:'):
            plugin = msg.split(':', 1)[-1].strip(' .')
            startup_msgs.append(f"[bold yellow]Loading plugin: [white]{plugin}[/white]...[/bold yellow]")
        elif msg.startswith('Loaded plugin:'):
            plugin = msg.split(':', 1)[-1].strip(' .')
            startup_msgs.append(f"[bold green]Loaded plugin: [white]{plugin}[/white][/bold green]")
        else:
            orig_print(*args, **kwargs)
    import builtins
    builtins.print = rich_plugin_print
    asyncio.run(plugin_manager.load_plugins(None, plugin_configs=plugin_configs))  # Pass None for injector for now
    builtins.print = orig_print
    # Print all startup messages in a single panel
    from rich.panel import Panel
    from rich.text import Text
    startup_text = Text()
    for msg in startup_msgs:
        startup_text.append(Text.from_markup(msg))
        startup_text.append('\n')
    console.print(Panel(startup_text, title="Startup Summary", style="bold blue"))
    builtins = {
        'inject': {'func': cmd_inject, 'help': 'Run the injector with current config.'},
        'config': {'func': cmd_config, 'help': 'Show current injector config.'},
        'plugins': {'func': cmd_plugins, 'help': 'List loaded plugins.'},
        'help': {'func': rich_help, 'help': 'Show this help menu.'},
        'exit': {'func': cmd_exit, 'help': 'Exit the CLI.'}
    }
    def get_all_commands():
        cmds = dict(builtins)
        plugin_cmds = plugin_manager.get_all_commands()
        for cmd, meta in plugin_cmds.items():
            if cmd not in cmds:
                cmds[cmd] = meta
        return cmds
    all_commands = get_all_commands()
    # Build a list of completions: command names and, for plugin commands, their parameter names
    completions = list(all_commands.keys())
    for cmd, meta in all_commands.items():
        params = meta.get('params', [])
        for p in params:
            completions.append(p['name'])

    def get_completions(prefix):
        all_cmds = list(get_all_commands().keys())
        # REVERT: Do not suppress completions when prefix matches a full command
        builtins_list = [cmd for cmd in all_cmds if '.' not in cmd]
        if not prefix or (prefix in builtins_list) or any(b.startswith(prefix) for b in builtins_list):
            # Top-level: show builtins and 'plugins', deduplicated
            completions = set(builtins_list + ['plugins'])
            # Filter by prefix if any
            if prefix:
                completions = {c for c in completions if c.startswith(prefix)}
            # If the prefix is exactly 'plugins', do not suggest 'plugins' again
            if prefix == 'plugins':
                completions.discard('plugins')
            return sorted(completions)
        parts = prefix.split('.')
        depth = len(parts)
        completions = set()
        for cmd in all_cmds:
            cmd_parts = cmd.split('.')
            if cmd.startswith(prefix):
                if len(cmd_parts) > depth:
                    next_part = '.'.join(cmd_parts[:depth+1])
                    completions.add(next_part)
        return sorted(completions)

    session = PromptSession()
    class HierarchicalCompleter:
        def get_completions(self, document, complete_event):
            text = document.text_before_cursor.strip()
            last_token = text.split()[-1] if text else ''
            for comp in get_completions(last_token):
                yield Completion(comp, start_position=-len(last_token))

        async def get_completions_async(self, document, complete_event):
            for completion in self.get_completions(document, complete_event):
                yield completion

    completer = HierarchicalCompleter()
    # Visually distinct welcome banner
    banner = Panel(
        Text("Idleon Injector CLI", style="bold magenta"),
        subtitle="type 'help' for commands",
        style=Style(color="cyan"),
        box=box.DOUBLE
    )
    console.print(banner)
    if not config.get("interactive", True):
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
            all_commands = get_all_commands()  # Refresh in case plugins change
            if cmd in all_commands:
                func = all_commands[cmd]['func']
                params_meta = all_commands[cmd].get('params', [])
                is_builtin = cmd in builtins
                # If help requested or no args and required params, show usage
                if (args and args[0] in ('-h', '--help')) or (params_meta and not args):
                    usage = Text(f"Usage: {cmd} ", style="bold yellow")
                    for p in params_meta:
                        pname = p['name']
                        typ = p.get('type', str).__name__
                        if 'default' in p:
                            usage.append(f"[{pname}:{typ}={p['default']}] ", style="cyan")
                        else:
                            usage.append(f"<{pname}:{typ}> ", style="magenta")
                    console.print(usage)
                    for p in params_meta:
                        helptext = p.get('help', '')
                        console.print(f"[bold green]  {p['name']}[/bold green]: [white]{helptext}[/white]")
                    console.rule(style="dim")
                    continue
                try:
                    if is_builtin:
                        # Call built-in commands directly
                        if cmd == 'help':
                            func(args, plugin_manager, all_commands)
                        else:
                            func(args, plugin_manager)
                        console.rule(style="dim")
                        continue
                    if params_meta:
                        from plugin_system import parse_plugin_args
                        try:
                            parsed_args = parse_plugin_args(params_meta, args)
                        except ValueError as e:
                            console.print(f"[red]{e}[/red]")
                            usage = f"Usage: {cmd} "
                            for p in params_meta:
                                pname = p['name']
                                typ = p.get('type', str).__name__
                                if 'default' in p:
                                    usage += f"[{pname}:{typ}={p['default']}] "
                                else:
                                    usage += f"<{pname}:{typ}> "
                            console.print(usage)
                            continue
                        call_kwargs = dict(parsed_args)
                        # Remove injector and plugin_manager if present
                        call_kwargs.pop('injector', None)
                        call_kwargs.pop('plugin_manager', None)
                        from plugin_system import execute_plugin_command
                        execute_plugin_command(
                            func,
                            call_kwargs,
                            injector=injector,
                            plugin_manager=plugin_manager,
                            console=console
                        )
                        console.rule(style="dim")
                        continue  # Always continue after execute_plugin_command for param commands
                    else:
                        from plugin_system import execute_plugin_command
                        execute_plugin_command(
                            func,
                            {},
                            injector=injector,
                            plugin_manager=plugin_manager,
                            console=console
                        )
                except TypeError:
                    # Only fallback for commands with NO parameter metadata
                    if not params_meta:
                        from plugin_system import execute_plugin_command
                        execute_plugin_command(
                            func,
                            {},
                            injector=injector,
                            plugin_manager=plugin_manager,
                            console=console
                        )
                    else:
                        console.print(f"[red]Internal error: argument mismatch for {cmd}. Check your plugin signature.[/red]")
                        continue
            else:
                console.print(f"[red]Unknown command: {cmd}[/red]")
        except (KeyboardInterrupt, EOFError):
            cmd_exit([], plugin_manager)
        except Exception as e:
            console.print(Panel(f"Error executing command: {e}", style="bold red"))
            continue

if __name__ == '__main__':
    main() 