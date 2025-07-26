"""
Plugin System for Enhanced Python Idleon Cheat Injector

This module provides a flexible plugin architecture that allows extending
functionality without modifying core code.
"""

import importlib
import importlib.util
import inspect
import logging
import asyncio
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, Callable
import traceback
import json
import os

from rich.console import Console
from config_manager import config_manager

# Global debug flag, set by main.py
GLOBAL_DEBUG = False

logger = logging.getLogger(__name__)
console = Console()

# Command registry for plugin commands
command_registry = {}

def plugin_command(help: str = None, js_export: bool = False, params: List[Dict[str, Any]] = None):
    """
    Decorator for plugin commands.
    
    Args:
        help: Help text for the command
        js_export: Whether to export this command to JavaScript
        params: List of parameter definitions, each dict can have:
            - name (str): parameter name
            - type (type): type for conversion (optional, default: str)
            - default: default value (optional)
            - help (str): help text (optional)
    """
    def decorator(func: Callable) -> Callable:
        func._plugin_command = True
        func._command_help = help or ""
        func._js_export = js_export
        func._js_params = [p["name"] if isinstance(p, dict) else p for p in (params or [])]
        func._command_params = params or []
        command_registry[func.__name__] = func
        return func
    return decorator

def js_export(params: List[str] = None):
    """
    Decorator for JavaScript export functions.
    
    Args:
        params: List of parameter names for JavaScript function
    """
    def decorator(func: Callable) -> Callable:
        func._js_export = True
        func._js_params = params or []
        return func
    return decorator

class PluginBase(ABC):
    """Base class for all plugins."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = True
        self.name = self.__class__.__name__
        self.version = getattr(self, 'VERSION', '1.0.0')
        self.description = getattr(self, 'DESCRIPTION', 'No description provided')
        self.dependencies = getattr(self, 'DEPENDENCIES', [])
        self.injector = None
        self.plugin_manager = None

    async def initialize(self, injector) -> bool:
        """Initialize the plugin and set up its config in the browser context."""
        if GLOBAL_DEBUG:
            console.print(f"[DEBUG] Initializing plugin {self.name}")
        
        self.injector = injector
        
        if injector:
            self.init_config_in_browser()
        
        return True

    @abstractmethod
    async def on_game_ready(self) -> None:
        """Called when the game is ready."""
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Clean up plugin resources."""
        pass

    @abstractmethod
    async def update(self) -> None:
        """Update plugin state (called periodically)."""
        pass

    @abstractmethod
    async def on_config_changed(self, config: Dict[str, Any]) -> None:
        """Called when plugin config changes."""
        pass

    def get_commands(self) -> Dict[str, Dict[str, Any]]:
        """Get all commands provided by this plugin."""
        commands = {}
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and getattr(attr, "_plugin_command", False):
                commands[attr_name] = {
                    "func": attr,
                    "help": getattr(attr, "_command_help", ""),
                    "params": getattr(attr, "_command_params", [])
                }
        return commands

    def get_web_routes(self) -> List[tuple]:
        """Get web routes for this plugin."""
        return []

    def get_js_exports(self) -> List[Callable]:
        """Get JavaScript export functions."""
        exports = []
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if (callable(attr) and 
                getattr(attr, "_plugin_command", False) and 
                getattr(attr, "_js_export", False)):
                exports.append(attr)
        return exports

    def run_js_export(self, js_func_name: str, injector, **params) -> Any:
        """Run a JavaScript exported function."""
        js_func = getattr(self, js_func_name)
        js_name = js_func_name[:-3] if js_func_name.endswith('_js') else js_func_name
        
        # Prepare argument list
        js_params = getattr(js_func, '_js_params', [])
        args = [params.get(p, '') for p in js_params]
        
        # Serialize arguments for JS call
        js_args = ', '.join(json.dumps(a) for a in args)
        
        # Execute in correct context
        expr = (f'(typeof getIdleonContext === "function" ? '
                f'window.{js_name}.call(getIdleonContext(), {js_args}) : '
                f'window.{js_name}({js_args}))')
        
        result = injector.evaluate(expr)
        return result.get('result', {}).get('value')

    def set_config(self, config: Dict[str, Any]) -> None:
        """Set plugin configuration in browser context."""
        if self.injector:
            js_config = json.dumps(config)
            expr = f"window.pluginConfigs['{self.name}'] = {js_config};"
            
            if GLOBAL_DEBUG:
                console.print(f"[DEBUG] Setting config for {self.name}: {expr}")
            
            try:
                result = self.injector.evaluate(expr)
                if GLOBAL_DEBUG:
                    console.print(f"[DEBUG] Set config result: {result}")
            except Exception as e:
                if GLOBAL_DEBUG:
                    console.print(f"[DEBUG] Error setting config: {e}")

    def init_config_in_browser(self) -> None:
        """Initialize this plugin's config in the browser context."""
        if not self.injector:
            return
        
        if GLOBAL_DEBUG:
            console.print(f"[DEBUG] Initializing config for plugin {self.name}")
        
        try:
            # Ensure window.pluginConfigs exists
            init_expr = "window.pluginConfigs = window.pluginConfigs || {};"
            self.injector.evaluate(init_expr)
            
            # Set this plugin's config
            self.set_config(self.config)
        except Exception as e:
            if GLOBAL_DEBUG:
                console.print(f"[DEBUG] Error initializing config: {e}")

    def save_to_global_config(self, config: Dict[str, Any] = None) -> None:
        """Save plugin configuration using ConfigManager."""
        plugin_config = config or self.config
        
        # Use ConfigManager to save the config
        config_manager.set_plugin_config(self.name, plugin_config)
        
        # Notify only this plugin about the config change
        if self.plugin_manager:
            try:
                loop = None
                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    pass
                if loop and loop.is_running():
                    asyncio.create_task(self.plugin_manager.notify_config_changed(plugin_config, self.name))
                else:
                    asyncio.run(self.plugin_manager.notify_config_changed(plugin_config, self.name))
            except Exception:
                pass  # Ignore if already running

class PluginManager:
    """Manages loading, initialization, and lifecycle of plugins."""
    
    def __init__(self, plugin_names: List[str], plugin_dir: str = 'plugins'):
        self.plugins: Dict[str, PluginBase] = {}
        self.plugin_dir = Path(plugin_dir)
        self.plugin_names = plugin_names

    async def load_plugins(self, injector, plugin_configs: Dict[str, Any] = None, 
                          global_debug: bool = True) -> None:
        """Load all configured plugins."""
        # Use ConfigManager to get plugin configs if not provided
        if plugin_configs is None:
            plugin_configs = config_manager.get_all_plugin_configs()
        
        for plugin_name in self.plugin_names:
            try:
                console.print(f"Loading plugin: {plugin_name}...")
                await self._load_plugin(
                    plugin_name, 
                    plugin_configs.get(plugin_name, {}), 
                    injector, 
                    global_debug=global_debug
                )
                console.print(f"Loaded plugin: {plugin_name}")
            except Exception as e:
                console.print(f"[red]Failed to load plugin '{plugin_name}': {e}[/red]")
                logger.error(f"Failed to load plugin '{plugin_name}': {e}")
                if GLOBAL_DEBUG:
                    logger.debug(traceback.format_exc())

    async def _load_plugin(self, plugin_name: str, plugin_config: Dict, 
                          injector, global_debug: bool = True) -> None:
        """Load a single plugin from the plugin directory."""
        plugin_class = await self._load_external_plugin(plugin_name)
        
        if not plugin_class:
            raise ImportError(f"Plugin '{plugin_name}' not found in {self.plugin_dir}")
        
        plugin_instance = plugin_class(plugin_config)
        plugin_instance.plugin_manager = self
        plugin_instance.global_debug = global_debug
        
        # Check dependencies
        for dependency in getattr(plugin_instance, 'dependencies', []):
            if dependency not in self.plugins:
                console.print(f"[yellow]Plugin '{plugin_name}' requires '{dependency}' "
                            f"which is not loaded[/yellow]")
                logger.warning(f"Plugin '{plugin_name}' requires '{dependency}' "
                             f"which is not loaded")
        
        success = await plugin_instance.initialize(injector)
        if success:
            self.plugins[plugin_name] = plugin_instance
            logger.info(f"Loaded plugin: {plugin_name}")
        else:
            raise RuntimeError(f"Failed to initialize plugin: {plugin_name}")

    async def _load_external_plugin(self, plugin_name: str) -> Optional[Type[PluginBase]]:
        """Load plugin class from external file."""
        plugin_file = self.plugin_dir / f"{plugin_name}.py"
        
        if not plugin_file.exists():
            return None
        
        spec = importlib.util.spec_from_file_location(plugin_name, plugin_file)
        if not spec or not spec.loader:
            return None
            
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Find plugin class
        for name, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) and 
                issubclass(obj, PluginBase) and 
                obj != PluginBase):
                return obj
        
        return None

    async def initialize_all(self, injector, plugin_configs: Dict[str, Any] = None) -> None:
        """Initialize all plugins with injector."""
        plugin_configs = plugin_configs or {}
        
        if GLOBAL_DEBUG:
            console.print(f"[DEBUG] Initializing all plugins with injector")
        
        for plugin_name in self.plugin_names:
            try:
                if plugin_name in self.plugins:
                    # Re-initialize existing plugin with new injector
                    plugin = self.plugins[plugin_name]
                    plugin.injector = injector
                    await plugin.initialize(injector)
                    if GLOBAL_DEBUG:
                        console.print(f"Re-initialized plugin: {plugin_name}")
                else:
                    # Load new plugin
                    await self._load_plugin(
                        plugin_name, 
                        plugin_configs.get(plugin_name, {}), 
                        injector
                    )
            except Exception as e:
                console.print(f"[red]Failed to initialize plugin '{plugin_name}': {e}[/red]")
                logger.error(f"Failed to initialize plugin '{plugin_name}': {e}")
        
        # Execute on_game_ready for all plugins
        if injector:
            for plugin in self.plugins.values():
                try:
                    await plugin.on_game_ready()
                    if GLOBAL_DEBUG:
                        console.print(f"Executed on_game_ready for plugin: {plugin.name}")
                except Exception as e:
                    logger.error(f"Error executing on_game_ready for plugin '{plugin.name}': {e}")

    async def cleanup_all(self) -> None:
        """Clean up all plugins."""
        for plugin_name, plugin in list(self.plugins.items()):
            try:
                await plugin.cleanup()
                logger.info(f"Cleaned up plugin: {plugin_name}")
            except Exception as e:
                logger.error(f"Error cleaning up plugin '{plugin_name}': {e}")

    async def update_all(self) -> None:
        """Update all plugins."""
        for plugin in self.plugins.values():
            try:
                await plugin.update()
            except Exception as e:
                logger.error(f"Error updating plugin: {e}")

    def get_plugin(self, name: str) -> Optional[PluginBase]:
        """Get a plugin by name."""
        return self.plugins.get(name)

    async def unload_plugin(self, plugin_name: str) -> None:
        """Unload a specific plugin."""
        plugin = self.plugins.get(plugin_name)
        if plugin:
            try:
                await plugin.cleanup()
                del self.plugins[plugin_name]
                logger.info(f"Unloaded plugin: {plugin_name}")
            except Exception as e:
                logger.error(f"Error unloading plugin '{plugin_name}': {e}")
        else:
            logger.warning(f"Plugin '{plugin_name}' not loaded.")

    def get_all_commands(self) -> Dict[str, Dict[str, Any]]:
        """Get all commands from all plugins."""
        commands = {}
        for name, plugin in self.plugins.items():
            plugin_cmds = plugin.get_commands()
            for cmd, meta in plugin_cmds.items():
                namespaced_cmd = f"plugins.{name}.{cmd}"
                commands[namespaced_cmd] = {
                    "func": meta["func"],
                    "help": meta.get("help", ""),
                    "params": meta.get("params", []),
                    "plugin": name
                }
        return commands

    def get_command_help(self, command_name: str) -> str:
        """Get help text for a command."""
        cmds = self.get_all_commands()
        if command_name in cmds:
            return cmds[command_name]["help"]
        return "No help available."

    def get_web_routes(self) -> List[tuple]:
        """Get all web routes from all plugins."""
        routes = []
        for plugin in self.plugins.values():
            routes.extend(plugin.get_web_routes())
        return routes

    async def notify_cheat_executed(self, command: str, result: Any) -> None:
        """Notify all plugins that a cheat was executed."""
        for plugin in self.plugins.values():
            try:
                await plugin.on_cheat_executed(command, result)
            except Exception as e:
                logger.error(f"Error notifying plugin of cheat execution: {e}")

    async def notify_page_load(self) -> None:
        """Notify all plugins that a page loaded."""
        for plugin in self.plugins.values():
            try:
                await plugin.on_page_load()
            except Exception as e:
                logger.error(f"Error notifying plugin of page load: {e}")

    async def notify_config_changed(self, config: Dict[str, Any], plugin_name: str = None) -> None:
        """Notify plugins that config changed. If plugin_name is given, only notify that plugin."""
        if plugin_name and plugin_name in self.plugins:
            try:
                await self.plugins[plugin_name].on_config_changed(config)
            except Exception as e:
                logger.error(f"Error notifying plugin of config change: {e}")
        else:
            for name, plugin in self.plugins.items():
                try:
                    await plugin.on_config_changed(plugin.config)
                except Exception as e:
                    logger.error(f"Error notifying plugin of config change: {e}")

    def collect_all_plugin_js(self) -> str:
        """Collect JavaScript code from all plugins."""
        js_code = ""
        
        # Check if debug mode is enabled
        debug = any(
            hasattr(plugin, 'config') and plugin.config.get('debug', False)
            for plugin in self.plugins.values()
        )
        
        # Create debug directory if needed
        if debug:
            tmp_js_dir = Path(__file__).parent / 'core' / 'tmp_js'
            tmp_js_dir.mkdir(exist_ok=True)
        
        for plugin in self.plugins.values():
            plugin_js = ""
            
            for attr_name in dir(plugin):
                if attr_name.endswith('_js'):
                    func = getattr(plugin, attr_name)
                    if callable(func) and getattr(func, '_js_export', False):
                        js_params = getattr(func, '_js_params', None)
                        
                        # Get function signature and parameters
                        sig = inspect.signature(func)
                        if js_params and len(js_params) > 0:
                            param_list = ", ".join(js_params)
                            # Get default values for parameters
                            bound_args = []
                            for p in js_params:
                                if p in sig.parameters and sig.parameters[p].default != inspect.Parameter.empty:
                                    bound_args.append(sig.parameters[p].default)
                                else:
                                    bound_args.append('')
                            js_body = func(*bound_args)
                        else:
                            params = list(sig.parameters.keys())[1:]  # skip 'self'
                            param_list = ", ".join(params) if params else ""
                            bound_args = []
                            for p in params:
                                param = sig.parameters[p]
                                if param.default != inspect.Parameter.empty:
                                    bound_args.append(param.default)
                                else:
                                    bound_args.append('')
                            js_body = func(*bound_args)
                        
                        js_name = attr_name[:-3]  # Remove '_js' suffix
                        
                        # Wrap JS body with game ready check
                        wrapped_js_body = f"""
                        try {{
                            // Wait for game to be ready before executing plugin function
                            await window.__idleon_wait_for_game_ready();
                            
                            {js_body}
                        }} catch (e) {{
                            console.error('[{js_name}] Error:', e);
                            return `Error: ${{e.message}}`;
                        }}
                        """
                        
                        js_func_code = f"window.{js_name} = async function({param_list}) {{\n{wrapped_js_body}\n}}\n"
                        js_code += js_func_code
                        plugin_js += js_func_code
            
            # Save plugin-specific JS if debug enabled
            if debug and plugin_js:
                plugin_file = tmp_js_dir / f"{plugin.__class__.__name__}_js_dump.js"
                with open(plugin_file, 'w') as f:
                    f.write(plugin_js)
        
        return js_code

    def reload_configs_from_file(self) -> None:
        """Reload all plugin configs using ConfigManager."""
        # Reload config from file
        config_manager.reload()
        
        # Get updated plugin configs
        plugin_configs = config_manager.get_all_plugin_configs()
        
        for plugin_name, plugin in self.plugins.items():
            if plugin_name in plugin_configs:
                old_config = plugin.config.copy()
                plugin.config.update(plugin_configs[plugin_name])
                
                # Update config in browser if injector is available
                if hasattr(plugin, 'injector') and plugin.injector:
                    plugin.set_config(plugin.config)
                
                # Notify plugin about config change
                try:
                    asyncio.create_task(plugin.on_config_changed(plugin.config))
                except RuntimeError:
                    # If no event loop, run synchronously
                    try:
                        asyncio.run(plugin.on_config_changed(plugin.config))
                    except:
                        pass  # Ignore if already running
                
                console.print(f"[green]Reloaded config for plugin: {plugin_name}[/green]")
            else:
                console.print(f"[yellow]No config found for plugin: {plugin_name}[/yellow]")

# --- Utility Functions ---
def parse_plugin_args(params_meta: List[Dict[str, Any]], args: List[str]) -> Dict[str, Any]:
    """
    Parse CLI arguments based on parameter metadata.
    
    Args:
        params_meta: List of parameter definitions
        args: List of string arguments from CLI
        
    Returns:
        Dictionary of parsed arguments
        
    Raises:
        ValueError: If parsing fails
    """
    result = {}
    
    # Special case: single string parameter, join all args
    if len(params_meta) == 1 and params_meta[0].get("type", str) == str:
        name = params_meta[0]["name"]
        if args:
            value = " ".join(args).strip('"\'')
            result[name] = value
        elif "default" in params_meta[0]:
            result[name] = params_meta[0]["default"]
        else:
            raise ValueError(f"Missing required argument: {name}")
        return result
    
    # Parse multiple parameters
    i = 0
    for meta in params_meta:
        name = meta["name"]
        typ = meta.get("type", str)
        
        if i < len(args):
            try:
                if typ == bool:
                    # Handle boolean conversion properly
                    arg_value = args[i].lower().strip()
                    if arg_value in ('true', '1', 'yes', 'on'):
                        value = True
                    elif arg_value in ('false', '0', 'no', 'off'):
                        value = False
                    else:
                        raise ValueError(f"Invalid boolean value: {args[i]}")
                else:
                    value = typ(args[i])
                    if typ == str:
                        value = value.strip('"\'')
            except Exception:
                raise ValueError(f"Invalid value for {name}: {args[i]}")
            result[name] = value
            i += 1
        elif "default" in meta:
            result[name] = meta["default"]
        else:
            raise ValueError(f"Missing required argument: {name}")
    
    if i < len(args):
        raise ValueError(f"Too many arguments: {' '.join(args[i:])}")
    
    return result

def execute_plugin_command(func: Callable, call_kwargs: Dict[str, Any], 
                          injector=None, plugin_manager=None, console=None) -> Any:
    """
    Execute a plugin command function with proper error handling.
    
    Args:
        func: The plugin command function
        call_kwargs: Dictionary of arguments to pass
        injector: Injector instance (optional)
        plugin_manager: Plugin manager (optional)
        console: Rich console instance (optional)
        
    Returns:
        Result of the command, or None if error
    """
    sig = inspect.signature(func)
    
    # Add injector and plugin_manager if needed
    if 'injector' in sig.parameters:
        if injector is None:
            if console:
                console.print("[red]No injector connected. Run 'inject' first.[/red]")
            return None
        call_kwargs['injector'] = injector
    
    if 'plugin_manager' in sig.parameters:
        call_kwargs['plugin_manager'] = plugin_manager
    
    try:
        if inspect.iscoroutinefunction(func):
            result = asyncio.run(func(**call_kwargs))
        else:
            result = func(**call_kwargs)
        
        # Display result if available
        if result is not None and console:
            console.print(f"[JS return] {result}")
        
        # Notify plugins if this might have changed config
        if plugin_manager and hasattr(func, '__self__') and hasattr(func.__self__, 'config'):
            command_name = func.__name__.lower()
            config_changing_keywords = ['toggle', 'set', 'config', 'save', 'update']
            if any(keyword in command_name for keyword in config_changing_keywords):
                try:
                    loop = None
                    try:
                        loop = asyncio.get_running_loop()
                    except RuntimeError:
                        pass
                    plugin_name = getattr(func.__self__, 'name', None)
                    if loop and loop.is_running():
                        asyncio.create_task(plugin_manager.notify_config_changed(func.__self__.config, plugin_name))
                    else:
                        asyncio.run(plugin_manager.notify_config_changed(func.__self__.config, plugin_name))
                except Exception:
                    pass  # Ignore if already running
        
        return result
    except Exception as e:
        if console:
            console.print(f"[red]Error executing command: {e}[/red]")
        else:
            print(f"Error executing command: {e}")
        return None