import subprocess
import os
import sys
import logging
import asyncio
import threading
import shutil
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

logging.getLogger('websocket').setLevel(logging.CRITICAL)
logging.getLogger('pychrome').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)

import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*JSONDecodeError.*")
warnings.filterwarnings("ignore", message=".*Expecting value.*")

import sys
import io
from contextlib import redirect_stderr

def suppress_websocket_errors():
    original_stderr = sys.stderr
    
    class WebsocketErrorFilter:
        def __init__(self, original):
            self.original = original
            
        def write(self, message):
            if "JSONDecodeError" in message and "Expecting value" in message:
                return
            if "Exception in thread" in message and "_recv_loop" in message:
                return
            self.original.write(message)
            
        def flush(self):
            self.original.flush()
            
        def __getattr__(self, name):
            return getattr(self.original, name)
    
    sys.stderr = WebsocketErrorFilter(original_stderr)

suppress_websocket_errors()

import threading
original_excepthook = threading.excepthook

def custom_excepthook(args):
    if hasattr(args, 'exc_value') and args.exc_value:
        exc_type = type(args.exc_value).__name__
        exc_msg = str(args.exc_value)
        
        if exc_type == 'JSONDecodeError' and 'Expecting value' in exc_msg:
            return
        if '_recv_loop' in str(args.thread):
            return
    
    original_excepthook(args)

threading.excepthook = custom_excepthook

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

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    CORE_DIR = Path(sys._MEIPASS) / 'core'
else:
    CORE_DIR = Path(__file__).parent / 'core'

INJECTOR_PATH = CORE_DIR / 'injector.js'

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    PLUGINS_DIR = Path(sys._MEIPASS) / 'plugins'
else:
    PLUGINS_DIR = Path(__file__).parent / 'plugins'

console = Console()
injector = None
injector_process = None
update_loop_task = None
update_loop_stop = threading.Event()
web_server_task = None

def ensure_node_dependencies(startup_msgs=None):
    node_modules_path = CORE_DIR / 'node_modules'
    
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        if not node_modules_path.exists():
            msg = "[bold red]Node.js dependencies missing from standalone build.[/bold red]"
            if startup_msgs:
                startup_msgs.append(msg)
            console.print(msg)
            return
        else:
            # Check for OpenSSL compatibility issues
            try:
                # Test if bundled Node.js works with current OpenSSL
                test_result = subprocess.run(['node', '--version'], 
                                           capture_output=True, text=True, timeout=5)
                if test_result.returncode == 0:
                    msg = "[bold green]Node.js dependencies found in standalone build.[/bold green]"
                else:
                    msg = "[bold yellow]Bundled Node.js has compatibility issues. Will use system Node.js.[/bold yellow]"
            except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
                msg = "[bold yellow]Bundled Node.js has compatibility issues. Will use system Node.js.[/bold yellow]"
            
            if startup_msgs:
                startup_msgs.append(msg)
            console.print(msg)
            return
    
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
        config_path = str(config_manager.conf_path)
        debug = config_manager.get_path('debug', False)
        
        if debug:
            console.print(f"[cyan]DEBUG: Launching injector with config: {config_path}[/cyan]")
            console.print(f"[cyan]DEBUG: Config file exists: {Path(config_path).exists()}[/cyan]")
            console.print(f"[cyan]DEBUG: Node path: {NODE_PATH}[/cyan]")
            console.print(f"[cyan]DEBUG: Injector path: {INJECTOR_PATH}[/cyan]")
            console.print(f"[cyan]DEBUG: Full command: {[NODE_PATH, str(INJECTOR_PATH), '--config', config_path]}[/cyan]")
        
        process = subprocess.Popen(
            [NODE_PATH, str(INJECTOR_PATH), '--config', config_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace',
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        )
        return process
    except FileNotFoundError:
        console.print(f"[bold red]Error: Node.js not found at '{NODE_PATH}'. Please install Node.js or check your PATH.[/bold red]")
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            console.print("[yellow]Note: Standalone builds require Node.js to be installed on the system.[/yellow]")
        raise
    except Exception as e:
        # Check if it's an OpenSSL compatibility issue
        if "OPENSSL" in str(e).upper() or "libcrypto" in str(e).lower():
            console.print(f"[bold yellow]OpenSSL compatibility issue detected: {e}[/bold yellow]")
            console.print("[yellow]Attempting to use system Node.js instead of bundled version...[/yellow]")
            
            # Try to use system Node.js by installing dependencies locally
            try:
                # Install dependencies in a temporary location
                import tempfile
                temp_core_dir = Path(tempfile.gettempdir()) / "idleonweb_core"
                temp_core_dir.mkdir(exist_ok=True)
                
                # Copy core files to temp location
                shutil.copytree(CORE_DIR, temp_core_dir, dirs_exist_ok=True)
                
                # Install dependencies using system Node.js
                result = subprocess.run(['npm', 'install'], cwd=temp_core_dir, 
                                      check=True, capture_output=True, text=True)
                
                # Use the temp injector path
                temp_injector_path = temp_core_dir / "injector.js"
                
                process = subprocess.Popen(
                    ['node', str(temp_injector_path)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                )
                console.print("[bold green]Successfully using system Node.js with compatible dependencies.[/bold green]")
                return process
                
            except Exception as fallback_error:
                console.print(f"[bold red]Fallback to system Node.js failed: {fallback_error}[/bold red]")
                console.print("[bold red]Please install Node.js dependencies manually or update your OpenSSL version.[/bold red]")
                raise
        else:
            console.print(f"[bold red]Error running injector: {e}[/bold red]")
            raise

def collect_plugin_js(plugin_manager, include_core=True):
    js_code, plugin_sizes = plugin_manager.collect_all_plugin_js_with_sizes()
    if config_manager.get_path('debug', False):
        console.print("[DEBUG] Generated plugin JS code length:", len(js_code))
    
    js_path = CORE_DIR / "plugins_combined.js"
    
    if include_core:
        core_path = CORE_DIR / "core.js"
        if core_path.exists():
            with open(core_path, "r", encoding='utf-8') as f:
                core_code = f.read()
            js_code = core_code + '\n' + js_code
    
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
    global injector, injector_process, update_loop_task, update_loop_stop, web_server_task
    
    _tab_reload_disconnected = False
    
    update_loop_stop.clear()
    
    console.print("[cyan]Performing full reload before injection...[/cyan]")
    
    config_manager.reload()
    console.print("[green]Main configuration reloaded from conf.json.[/green]")
    
    import plugin_system
    plugin_system.GLOBAL_DEBUG = config_manager.get_path('debug', False)
    console.print(f"[green]Debug mode: {'enabled' if plugin_system.GLOBAL_DEBUG else 'disabled'}[/green]")

    asyncio.run(plugin_manager.reload_plugins())
    console.print("[green]Python plugins reloaded.[/green]")

    collect_plugin_js(plugin_manager, include_core=True)
    console.print("[green]Plugin JS regenerated.[/green]")

    cdp_port = config_manager.get_cdp_port()
    idleon_url = config_manager.get_idleon_url()
    
    console.print(f"[cyan]Running injector.js with config from conf.json...[/cyan]")
    console.print(f"[cyan]CDP Port: {cdp_port}, Idleon URL: {idleon_url}[/cyan]")
    injector_process = run_injector()
    
    import time
    time.sleep(3)
    
    if injector_process.poll() is not None:
        stdout, stderr = injector_process.communicate()
        console.print(f"[red]Injector process exited with code {injector_process.returncode}[/red]")
        if stdout:
            console.print(f"[yellow]Injector stdout: {stdout}[/yellow]")
        if stderr:
            console.print(f"[red]Injector stderr: {stderr}[/red]")
        raise RuntimeError("Injector process failed to start")
    
    injector = PyInjector()
    try:
        injector.connect()

        time.sleep(0.5)

        console.print("[green]Injector connected successfully.[/green]")
        
        try:
            console.print("[cyan]Injecting fresh JS into browser...[/cyan]")
            injector.reload_js()
            console.print("[green]Plugin JS injected into browser.[/green]")
        except Exception as e:
            console.print(f"[yellow]Could not inject JS into browser: {e}[/yellow]")
            console.print(f"[yellow]JS will be injected when the game loads[/yellow]")
        
        asyncio.run(plugin_manager.initialize_all(injector, config_manager.get_path('plugin_configs', {})))
        console.print("[green]Plugins initialized in injector session.[/green]")

        if update_loop_task is None or not update_loop_task.is_alive():
            update_loop_stop.clear()
            update_loop_task = threading.Thread(
                target=run_update_loop, 
                args=(plugin_manager,), 
                daemon=True
            )
            update_loop_task.start()
        
        if web_server_task is None or not web_server_task.is_alive():
            web_server = PluginWebAPI(plugin_manager)
            web_server_task = threading.Thread(
                target=lambda: asyncio.run(web_server.start_server()),
                daemon=True
            )
            web_server_task.start()
            webui_port = config_manager.get_webui_port()
            webui_url = f"http://localhost:{webui_port}"
            console.print(f"[green]Plugin UI web server started at {webui_url}[/green]")
            try:
                if config_manager.get_webui_auto_open():
                    url_to_open = config_manager.get_webui_url_from_port()
                    console.print(f"[cyan]Opening Web UI at {url_to_open} in the target browser...[/cyan]")
                    import time
                    time.sleep(1)
                    try:
                        injector.open_url_in_new_tab(url_to_open)
                        console.print("[green]Web UI opened in target browser.[/green]")
                    except Exception as e:
                        console.print(f"[yellow]Could not open Web UI automatically: {e}[/yellow]")
                        console.print(f"[yellow]You can open it manually at {url_to_open}[/yellow]")
            except Exception as e:
                console.print(f"[yellow]Auto-open web UI encountered an error: {e}[/yellow]")
            
    except Exception as e:
        console.print(f"[red]Failed to connect injector: {e}[/red]")
        injector = None
        injector_process = None

def cmd_stop_injection(args=None, plugin_manager=None):
    global injector, injector_process, update_loop_task, update_loop_stop
    
    console.print("[cyan]Stopping injection and closing browser...[/cyan]")
    
    if update_loop_stop:
        update_loop_stop.set()
        console.print("[green]Update loop stopped.[/green]")
    
    if injector:
        try:
            injector.close_browser()
            console.print("[green]Browser closed via CDP.[/green]")
        except Exception as e:
            console.print(f"[yellow]Error closing browser via CDP: {e}[/yellow]")
            try:
                if hasattr(injector, 'tab') and injector.tab:
                    injector.tab.stop()
                    console.print("[green]CDP connection closed (fallback).[/green]")
            except Exception as e2:
                console.print(f"[yellow]Error closing CDP connection: {e2}[/yellow]")
        
        injector = None
        console.print("[green]Injector disconnected.[/green]")
    
    if injector_process:
        try:
            injector_process.terminate()
            console.print("[green]Injector process terminated.[/green]")
            
            try:
                injector_process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                injector_process.kill()
                console.print("[yellow]Injector process force killed.[/yellow]")
                
        except Exception as e:
            console.print(f"[yellow]Error stopping injector process: {e}[/yellow]")
        
        injector_process = None
    
    try:
        cdp_port = config_manager.get_cdp_port()
        if sys.platform == 'win32':
            subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe', '/T'], 
                         capture_output=True, check=False)
            subprocess.run(['taskkill', '/F', '/IM', 'chromium.exe', '/T'], 
                         capture_output=True, check=False)
        else:
            subprocess.run(['pkill', '-f', f'chrome.*--remote-debugging-port={cdp_port}'], 
                         capture_output=True, check=False)
        console.print("[green]Browser processes cleaned up (fallback).[/green]")
    except Exception as e:
        console.print(f"[yellow]Error cleaning up browser processes: {e}[/yellow]")
    
    console.print("[bold green]Injection stopped and browser closed.[/bold green]")

def cmd_config(args=None, plugin_manager=None):
    config = config_manager.get_full_config()
    table = Table(title="Current Injector Config")
    table.add_column("Key", style="bold cyan")
    table.add_column("Value", style="white")
    for k, v in config.items():
        table.add_row(str(k), str(v))
    console.print(table)

def cmd_injector_config(args=None, plugin_manager=None):
    table = Table(title="Injector Configuration")
    table.add_column("Setting", style="bold cyan")
    table.add_column("Value", style="white")
    table.add_column("Description", style="yellow")
    
    table.add_row("CDP Port", str(config_manager.get_cdp_port()), "Chrome DevTools Protocol port")
    table.add_row("N.js Pattern", config_manager.get_njs_pattern(), "Pattern for intercepting game JS")
    table.add_row("Idleon URL", config_manager.get_idleon_url(), "Game URL to launch")
    table.add_row("Timeout (ms)", str(config_manager.get_timeout()), "CDP connection timeout in milliseconds")
    table.add_row("Web UI Auto Open", str(config_manager.get_webui_auto_open()), "Open the Web UI after injection")
    table.add_row("Web UI URL", config_manager.get_webui_url(), "Web UI URL to open after injection")
    
    console.print(table)

def cmd_darkmode(args=None, plugin_manager=None):
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
        current = config_manager.get_darkmode()
        new_state = not current
        config_manager.set_darkmode(new_state)
        status = "enabled" if new_state else "disabled"
        console.print(f"[green]Dark mode {status}[/green]")

def cmd_auto_inject(args=None, plugin_manager=None):
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
        current = config_manager.get_auto_inject()
        new_state = not current
        config_manager.set_auto_inject(new_state)
        status = "enabled" if new_state else "disabled"
        console.print(f"[green]Auto-inject {status}[/green]")

def cmd_gui_mode(args=None, plugin_manager=None):
    if args:
        if args[0].lower() in ['on', 'true', '1', 'yes']:
            config_manager.set_gui_enabled(True)
            console.print("[green]GUI mode enabled[/green]")
        elif args[0].lower() in ['off', 'false', '0', 'no']:
            config_manager.set_gui_enabled(False)
            console.print("[green]GUI mode disabled[/green]")
        else:
            console.print("[red]Invalid argument. Use 'on' or 'off'[/red]")
    else:
        current = config_manager.get_gui_enabled()
        new_state = not current
        config_manager.set_gui_enabled(new_state)
        status = "enabled" if new_state else "disabled"
        console.print(f"[green]GUI mode {status}[/green]")
        console.print("[yellow]Restart the application to apply GUI mode changes[/yellow]")

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
        config_manager.reload()
        console.print("[green]Main configuration reloaded from conf.json.[/green]")
        
        import plugin_system
        plugin_system.GLOBAL_DEBUG = config_manager.get_path('debug', False)
        console.print(f"[green]Debug mode: {'enabled' if plugin_system.GLOBAL_DEBUG else 'disabled'}[/green]")

        asyncio.run(plugin_manager.reload_plugins())
        console.print("[green]Python plugins reloaded.[/green]")

        js_code, plugin_sizes = plugin_manager.collect_all_plugin_js_with_sizes()
        if config_manager.get_path('debug', False):
            console.print("[DEBUG] Generated plugin JS code length:", len(js_code))
        
        js_path = CORE_DIR / "plugins_combined.js"
        with open(js_path, "w", encoding='utf-8') as f:
            f.write(js_code)
        console.print("[green]Plugin JS regenerated (without core.js for reload).[/green]")
        
        if injector:
            try:
                console.print("[cyan]Attempting to reload JS into injector...[/cyan]")
                injector.reload_js()
                console.print("[green]Plugin JS reloaded into injector.[/green]")
            except Exception as e:
                console.print(f"[yellow]Could not reload JS into injector: {e}[/yellow]")
                console.print(f"[yellow]This might be normal if the injector is not fully connected[/yellow]")
        else:
            console.print("[yellow]No injector connected - JS will be loaded on next 'inject' command[/yellow]")

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
    webui_port = config_manager.get_webui_port()
    webui_url = f"http://localhost:{webui_port}"
    
    if web_server_task and web_server_task.is_alive():
        console.print(f"[yellow]Web server is already running at {webui_url}[/yellow]")
        return
    
    try:
        web_server = PluginWebAPI(plugin_manager)
        web_server_task = threading.Thread(
            target=lambda: asyncio.run(web_server.start_server()),
            daemon=True
        )
        web_server_task.start()
        console.print(f"[green]Plugin UI web server started at {webui_url}[/green]")
        console.print("[cyan]Open your browser to configure plugins with a modern web interface![/cyan]")
    except Exception as e:
        console.print(f"[red]Failed to start web server: {e}[/red]")

def cmd_stop_web_ui(args=None, plugin_manager=None):
    global web_server_task
    
    if not web_server_task or not web_server_task.is_alive():
        console.print("[yellow]Web UI server is not running[/yellow]")
        return
    
    try:
        console.print("[cyan]Stopping Web UI server...[/cyan]")
        
        web_server_task = None
        console.print("[green]Web UI server stop requested (will stop when process exits)[/green]")
        console.print("[yellow]Note: Web UI server runs as daemon thread and will stop when the main process exits[/yellow]")
        
    except Exception as e:
        console.print(f"[red]Error stopping Web UI server: {e}[/red]")

def cmd_webui_auto_open(args=None, plugin_manager=None):
    if args:
        if args[0].lower() in ['on', 'true', '1', 'yes']:
            config_manager.set_webui_auto_open(True)
            console.print("[green]Web UI auto-open enabled[/green]")
        elif args[0].lower() in ['off', 'false', '0', 'no']:
            config_manager.set_webui_auto_open(False)
            console.print("[green]Web UI auto-open disabled[/green]")
        else:
            console.print("[red]Invalid argument. Use 'on' or 'off'[/red]")
    else:
        current = config_manager.get_webui_auto_open()
        new_state = not current
        config_manager.set_webui_auto_open(new_state)
        status = "enabled" if new_state else "disabled"
        console.print(f"[green]Web UI auto-open {status}[/green]")

def cmd_webui_url(args=None, plugin_manager=None):
    if args and args[0]:
        config_manager.set_webui_url(args[0])
        console.print(f"[green]Web UI URL set to {args[0]}[/green]")
    else:
        console.print(f"[cyan]Current Web UI URL: {config_manager.get_webui_url()}[/cyan]")

def cmd_webui_port(args=None, plugin_manager=None):
    if args and args[0]:
        try:
            port = int(args[0])
            if port < 1 or port > 65535:
                console.print("[red]Port must be between 1 and 65535[/red]")
                return
            config_manager.set_webui_port(port)
            console.print(f"[green]Web UI port set to {port}[/green]")
        except ValueError:
            console.print("[red]Port must be a valid number[/red]")
    else:
        port = config_manager.get_webui_port()
        console.print(f"[cyan]Current Web UI port: {port}[/cyan]")

def cmd_browser_path(args=None, plugin_manager=None):
    if args and args[0]:
        config_manager.set_browser_path(args[0])
        console.print(f"[green]Browser path set to {args[0]}[/green]")
    else:
        path = config_manager.get_browser_path()
        if path:
            console.print(f"[cyan]Current browser path: {path}[/cyan]")
        else:
            console.print("[cyan]No browser path configured (using auto-detection)[/cyan]")

def cmd_browser_name(args=None, plugin_manager=None):
    if args and args[0]:
        browser_name = args[0].lower()
        valid_browsers = ['auto', 'chrome', 'chromium', 'edge', 'brave', 'operagx', 'opera']
        if browser_name not in valid_browsers:
            console.print(f"[red]Invalid browser name. Valid options: {', '.join(valid_browsers)}[/red]")
            return
        config_manager.set_browser_name(browser_name)
        console.print(f"[green]Browser name set to {browser_name}[/green]")
    else:
        name = config_manager.get_browser_name()
        console.print(f"[cyan]Current browser name: {name}[/cyan]")

def cmd_browser_detect(args=None, plugin_manager=None):
    import os
    import platform
    
    possible_paths = []
    system = platform.system().lower()
    
    if system == 'windows':
        username = os.environ.get('USERNAME', '')
        possible_paths = [
            f'C:/Program Files/Google/Chrome/Application/chrome.exe',
            f'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
            f'C:/Users/{username}/AppData/Local/Google/Chrome/Application/chrome.exe',
            f'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
            f'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
            f'C:/Users/{username}/AppData/Local/Microsoft/Edge/Application/msedge.exe',
            f'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe',
            f'C:/Program Files (x86)/BraveSoftware/Brave-Browser/Application/brave.exe',
            f'C:/Users/{username}/AppData/Local/BraveSoftware/Brave-Browser/Application/brave.exe',
            f'C:/Users/{username}/AppData/Local/Programs/Opera GX/opera.exe',
            f'C:/Program Files/Opera GX/opera.exe',
            f'C:/Program Files (x86)/Opera GX/opera.exe',
        ]
    elif system == 'linux':
        possible_paths = [
            '/usr/bin/google-chrome',
            '/usr/bin/google-chrome-stable',
            '/usr/bin/chromium',
            '/usr/bin/chromium-browser',
            '/usr/bin/microsoft-edge',
            '/usr/bin/brave',
            '/usr/bin/opera-gx',
            '/usr/bin/opera',
            '/snap/bin/opera',
        ]
    elif system == 'darwin':
        possible_paths = [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '/Applications/Chromium.app/Contents/MacOS/Chromium',
            '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
            '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
            '/Applications/Opera GX.app/Contents/MacOS/Opera GX',
        ]
    
    found_browsers = []
    for path in possible_paths:
        if os.path.exists(path):
            browser_name = os.path.basename(path).lower()
            if 'chrome' in browser_name:
                browser_type = 'chrome'
            elif 'chromium' in browser_name:
                browser_type = 'chromium'
            elif 'edge' in browser_name:
                browser_type = 'edge'
            elif 'brave' in browser_name:
                browser_type = 'brave'
            elif 'opera' in browser_name:
                browser_type = 'operagx'
            else:
                browser_type = 'unknown'
            
            found_browsers.append((path, browser_type))
    
    if found_browsers:
        console.print("[green]Found browsers:[/green]")
        for i, (path, browser_type) in enumerate(found_browsers, 1):
            console.print(f"  {i}. {browser_type.title()}: {path}")
        
        best_path, best_type = found_browsers[0]
        config_manager.set_browser_path(best_path)
        config_manager.set_browser_name(best_type)
        console.print(f"[green]Auto-selected: {best_type.title()} at {best_path}[/green]")
    else:
        console.print("[red]No browsers detected. Please install Chrome, Chromium, Edge, Brave, or OperaGX.[/red]")

def cmd_exit(args=None, plugin_manager=None):
    global update_loop_stop, update_loop_task, web_server_task
    console.print("[bold green]Shutting down...[/bold green]")
    update_loop_stop.set()
    if update_loop_task and update_loop_task.is_alive():
        update_loop_task.join(timeout=2)
    if web_server_task and web_server_task.is_alive():
        console.print("[cyan]Stopping web server...[/cyan]")
    if plugin_manager:
        asyncio.run(plugin_manager.cleanup_all())
    console.print("[bold green]Goodbye![/bold green]")
    sys.exit(0)

def check_unused_plugins(plugin_manager, startup_msgs):
    try:
        configured_plugins = set(config_manager.get_path('plugins', []))
        
        plugin_files = []
        
        for plugin_file in PLUGINS_DIR.glob("*.py"):
            if plugin_file.name != "__init__.py" and plugin_file.name != "example_plugin.py":
                plugin_name = plugin_file.stem
                plugin_files.append(plugin_name)
        
        for subdir in PLUGINS_DIR.iterdir():
            if subdir.is_dir() and not subdir.name.startswith('.'):
                for plugin_file in subdir.glob("*.py"):
                    if plugin_file.name != "__init__.py" and plugin_file.name != "example_plugin.py":
                        plugin_name = f"{subdir.name}.{plugin_file.stem}"
                        plugin_files.append(plugin_name)
        
        unused_plugins = [name for name in plugin_files if name not in configured_plugins]
        
        if unused_plugins:
            startup_msgs.append(f"[yellow]Found {len(unused_plugins)} unused plugins: {', '.join(unused_plugins)}[/yellow]")
            
            is_standalone = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
            gui_enabled = config_manager.get_gui_enabled()
            
            if is_standalone or gui_enabled:
                current_plugins = config_manager.get_path('plugins', [])
                for plugin_name in unused_plugins:
                    if plugin_name not in current_plugins:
                        current_plugins.append(plugin_name)
                        config_manager.add_plugin(plugin_name, {})
                config_manager.set_plugins_list(current_plugins)
                mode_text = "standalone mode" if is_standalone else "GUI mode"
                startup_msgs.append(f"[green]Auto-enabled all unused plugins in {mode_text}: {', '.join(unused_plugins)}[/green]")
                console.print(f"[green]Auto-enabled all unused plugins in {mode_text}: {', '.join(unused_plugins)}[/green]")
                
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
                console.print(f"[cyan]Found {len(unused_plugins)} unused plugins:[/cyan]")
                for plugin_name in unused_plugins:
                    console.print(f"  [yellow]• {plugin_name}[/yellow]")
                
                console.print(f"\n[cyan]Would you like to enable any of these plugins?[/cyan]")
                console.print(f"[cyan]Type 'all' to enable all, 'none' to skip, or enter plugin names separated by spaces:[/cyan]")
                
                try:
                    user_input = input("> ").strip().lower()
                
                    if user_input == 'all':
                        current_plugins = config_manager.get_path('plugins', [])
                        for plugin_name in unused_plugins:
                            if plugin_name not in current_plugins:
                                current_plugins.append(plugin_name)
                                config_manager.add_plugin(plugin_name, {})
                        config_manager.set_plugins_list(current_plugins)
                        startup_msgs.append(f"[green]Enabled all unused plugins: {', '.join(unused_plugins)}[/green]")
                        console.print(f"[green]Enabled all unused plugins![/green]")
                        
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
    import argparse
    
    parser = argparse.ArgumentParser(description='IdleonWeb Plugin System')
    parser.add_argument('--cli', action='store_true', help='Force CLI mode')
    parser.add_argument('--gui', action='store_true', help='Force GUI mode')
    parser.add_argument('--no-gui', action='store_true', help='Disable GUI mode')
    args = parser.parse_args()
    
    gui_enabled = config_manager.get_gui_enabled()
    
    if args.cli or args.no_gui:
        gui_enabled = False
    elif args.gui:
        gui_enabled = True
    
    if gui_enabled:
        try:
            from gui_main import main as gui_main
            gui_main()
        except ImportError as e:
            console.print(f"[red]GUI mode failed to start: {e}[/red]")
            console.print("[yellow]Falling back to CLI mode...[/yellow]")
            start_cli_mode()
        except Exception as e:
            console.print(f"[red]GUI error: {e}[/red]")
            console.print("[yellow]Falling back to CLI mode...[/yellow]")
            start_cli_mode()
    else:
        start_cli_mode()

def start_cli_mode():
    startup_msgs = []
    ensure_node_dependencies(startup_msgs)
    
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
    
    check_unused_plugins(plugin_manager, startup_msgs)
    
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
        'stop': {'func': cmd_stop_injection, 'help': 'Stop injection and close browser.'},
        'config': {'func': cmd_config, 'help': 'Show current injector config.'},
        'injector_config': {'func': cmd_injector_config, 'help': 'Show injector-specific configuration.'},
        'darkmode': {'func': cmd_darkmode, 'help': 'Toggle or set dark mode for web UI (on/off).'},
        'auto_inject': {'func': cmd_auto_inject, 'help': 'Toggle or set auto-inject on startup (on/off).'},
        'gui_mode': {'func': cmd_gui_mode, 'help': 'Toggle or set GUI mode (on/off).'},
        'plugins': {'func': cmd_plugins, 'help': 'List loaded plugins.'},
        'reload_config': {'func': cmd_reload_config, 'help': 'Reload plugin configurations from conf.json.'},
        'web_ui': {'func': cmd_web_ui, 'help': 'Start the plugin web UI server.'},
        'stop_web_ui': {'func': cmd_stop_web_ui, 'help': 'Stop the plugin web UI server.'},
        'webui_auto_open': {'func': cmd_webui_auto_open, 'help': 'Toggle or set auto-open of Web UI after injection (on/off).'},
        'webui_url': {'func': cmd_webui_url, 'help': 'Set or view the Web UI URL to open after injection.'},
        'webui_port': {'func': cmd_webui_port, 'help': 'Set or view the Web UI port (1-65535).'},
        'browser_path': {'func': cmd_browser_path, 'help': 'Set or view the browser executable path.'},
        'browser_name': {'func': cmd_browser_name, 'help': 'Set or view the browser name (auto, chrome, chromium, edge, brave, operagx).'},
        'browser_detect': {'func': cmd_browser_detect, 'help': 'Auto-detect and configure browser.'},
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