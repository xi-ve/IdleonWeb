"""
Plugin System for Enhanced Python Idleon Cheat Injector

This module provides a flexible plugin architecture that allows extending
functionality without modifying core code. Only the PluginBase and PluginManager are defined here.
"""

import importlib
import inspect
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Type
import traceback
from rich.console import Console
console = Console()

logger = logging.getLogger(__name__)

command_registry = {}

def plugin_command(help=None, js_export=False, params=None):
    """
    params: list of dicts, each dict can have:
      - name (str): parameter name
      - type (type): type for conversion (optional)
      - default: default value (optional)
      - help (str): help text (optional)
    """
    def decorator(func):
        func._plugin_command = True
        func._command_help = help or ""
        func._js_export = js_export
        func._js_params = [p["name"] if isinstance(p, dict) else p for p in (params or [])]
        func._command_params = params or []
        command_registry[func.__name__] = func
        return func
    return decorator

def js_export(params=None):
    def decorator(func):
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

    @abstractmethod
    async def initialize(self, injector) -> bool:
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        pass

    async def update(self) -> None:
        pass

    async def on_cheat_executed(self, command: str, result: Any) -> None:
        pass

    async def on_page_load(self) -> None:
        pass

    async def on_config_changed(self, config: Dict[str, Any]) -> None:
        pass

    def get_commands(self):
        commands = {}
        for attr in dir(self):
            func = getattr(self, attr)
            if callable(func) and getattr(func, "_plugin_command", False):
                commands[func.__name__] = {
                    "func": func,
                    "help": getattr(func, "_command_help", ""),
                    "params": getattr(func, "_command_params", [])
                }
        return commands

    def get_web_routes(self) -> List[tuple]:
        return []

    def get_js_exports(self):
        exports = []
        for attr in dir(self):
            func = getattr(self, attr)
            if callable(func) and getattr(func, "_plugin_command", False) and getattr(func, "_js_export", False):
                exports.append(func)
        return exports

    def run_js_export(self, js_func_name: str, injector, **params):
        """
        Run a JS-exported function in the browser context via the injector.
        - js_func_name: the Python method name (ending with _js) to export (e.g. 'schalom_popup_js')
        - injector: the injector instance
        - params: parameters to pass to the JS function
        Returns the JS evaluation result value.
        """
        import json
        js_func = getattr(self, js_func_name)
        # Get the JS-exported function name (strip _js)
        js_name = js_func_name[:-3] if js_func_name.endswith('_js') else js_func_name
        # Prepare argument list in order
        js_params = getattr(js_func, '_js_params', [])
        args = [params.get(p, '') for p in js_params]
        # Serialize arguments for JS call
        js_args = ', '.join(json.dumps(a) for a in args)
        # Always call with correct context
        expr = f'(typeof getIdleonContext === "function" ? window.{js_name}.call(getIdleonContext(), {js_args}) : window.{js_name}({js_args}))'
        result = injector.evaluate(expr)
        return result.get('result', {}).get('value')

class PluginManager:
    """Manages loading, initialization, and lifecycle of plugins dynamically."""
    def __init__(self, plugin_names: List[str], plugin_dir: str = 'plugins'):
        self.plugins: Dict[str, PluginBase] = {}
        self.plugin_dir = Path(plugin_dir)
        self.plugin_names = plugin_names

    async def load_plugins(self, injector, plugin_configs: Dict[str, Any] = None) -> None:
        plugin_configs = plugin_configs or {}
        for plugin_name in self.plugin_names:
            try:
                print(f"Loading plugin: {plugin_name}...")
                await self._load_plugin(plugin_name, plugin_configs.get(plugin_name, {}), injector)
            except Exception as e:
                console.print(f"[red]Failed to load plugin '{plugin_name}': {e}[/red]")
                logger.error(f"Failed to load plugin '{plugin_name}': {e}")
                logger.debug(traceback.format_exc())

    async def _load_plugin(self, plugin_name: str, plugin_config: Dict, injector) -> None:
        """Load a single plugin from the plugin directory."""
        plugin_class = await self._load_external_plugin(plugin_name)
        if not plugin_class:
            console.print(f"[red]Plugin '{plugin_name}' not found in {self.plugin_dir}[/red]")
            raise ImportError(f"Plugin '{plugin_name}' not found in {self.plugin_dir}")
        plugin_instance = plugin_class(plugin_config)
        for dependency in getattr(plugin_instance, 'dependencies', []):
            if dependency not in self.plugins:
                console.print(f"[yellow]Plugin '{plugin_name}' requires '{dependency}' which is not loaded[/yellow]")
                logger.warning(f"Plugin '{plugin_name}' requires '{dependency}' which is not loaded")
        success = await plugin_instance.initialize(injector)
        if success:
            self.plugins[plugin_name] = plugin_instance
            print(f"Loaded plugin: {plugin_name}")
            logger.info(f"Loaded plugin: {plugin_name}")
        else:
            console.print(f"[red]Failed to initialize plugin: {plugin_name}[/red]")
            logger.error(f"Failed to initialize plugin: {plugin_name}")

    async def _load_external_plugin(self, plugin_name: str) -> Optional[Type[PluginBase]]:
        """Load plugin from external file."""
        plugin_file = self.plugin_dir / f"{plugin_name}.py"
        if not plugin_file.exists():
            return None
        spec = importlib.util.spec_from_file_location(plugin_name, plugin_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for name, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) and issubclass(obj, PluginBase) and obj != PluginBase):
                return obj
        return None

    async def unload_all_plugins(self) -> None:
        for plugin_name, plugin in list(self.plugins.items()):
            try:
                await plugin.cleanup()
                logger.info(f"Unloaded plugin: {plugin_name}")
            except Exception as e:
                logger.error(f"Error unloading plugin '{plugin_name}': {e}")
        self.plugins.clear()

    def get_plugin(self, name: str) -> Optional[PluginBase]:
        return self.plugins.get(name)

    async def update_plugin(self, plugin_name: str) -> None:
        plugin = self.plugins.get(plugin_name)
        if plugin:
            try:
                await plugin.update()
                logger.info(f"Updated plugin: {plugin_name}")
            except Exception as e:
                logger.error(f"Error updating plugin '{plugin_name}': {e}")
        else:
            logger.warning(f"Plugin '{plugin_name}' not loaded.")

    async def unload_plugin(self, plugin_name: str) -> None:
        plugin = self.plugins.get(plugin_name)
        if plugin:
            try:
                await plugin.cleanup()
                logger.info(f"Unloaded plugin: {plugin_name}")
            except Exception as e:
                logger.error(f"Error unloading plugin '{plugin_name}': {e}")
            del self.plugins[plugin_name]
        else:
            logger.warning(f"Plugin '{plugin_name}' not loaded.")

    def get_all_commands(self) -> dict:
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
        cmds = self.get_all_commands()
        if command_name in cmds:
            return cmds[command_name]["help"]
        return "No help available."

    def get_web_routes(self) -> List[tuple]:
        routes = []
        for plugin in self.plugins.values():
            routes.extend(plugin.get_web_routes())
        return routes

    async def notify_cheat_executed(self, command: str, result: Any) -> None:
        for plugin in self.plugins.values():
            try:
                await plugin.on_cheat_executed(command, result)
            except Exception as e:
                logger.error(f"Error notifying plugin of cheat execution: {e}")

    async def notify_page_load(self) -> None:
        for plugin in self.plugins.values():
            try:
                await plugin.on_page_load()
            except Exception as e:
                logger.error(f"Error notifying plugin of page load: {e}")

    async def notify_config_changed(self, config: Dict[str, Any]) -> None:
        for plugin in self.plugins.values():
            try:
                await plugin.on_config_changed(config)
            except Exception as e:
                logger.error(f"Error notifying plugin of config change: {e}")

    def collect_all_plugin_js(self):
        js_code = ""
        import inspect
        import os
        # Try to get debug mode from config (from any loaded plugin)
        debug = False
        for plugin in self.plugins.values():
            if hasattr(plugin, 'config') and plugin.config.get('debug', False):
                debug = True
                break
        tmp_js_dir = os.path.join(os.path.dirname(__file__), 'core', 'tmp_js')
        if debug and not os.path.exists(tmp_js_dir):
            os.makedirs(tmp_js_dir, exist_ok=True)
        for plugin in self.plugins.values():
            for attr in dir(plugin):
                if attr.endswith('_js'):
                    func = getattr(plugin, attr)
                    if callable(func) and getattr(func, '_js_export', False):
                        js_params = getattr(func, '_js_params', None)
                        if js_params is not None and len(js_params) > 0:
                            param_list = ", ".join(js_params)
                            sig = inspect.signature(func)
                            bound_args = []
                            for p in js_params:
                                if p in sig.parameters and sig.parameters[p].default is not inspect.Parameter.empty:
                                    bound_args.append(sig.parameters[p].default)
                                else:
                                    bound_args.append('')
                            js_body = func(*bound_args)
                        else:
                            sig = inspect.signature(func)
                            params = list(sig.parameters.keys())[1:]  # skip self
                            param_list = ", ".join(params) if params else ""
                            bound_args = []
                            for p in params:
                                param = sig.parameters[p]
                                if param.default is not inspect.Parameter.empty:
                                    bound_args.append(param.default)
                                else:
                                    bound_args.append('')
                            js_body = func(*bound_args)
                        js_name = attr[:-3]
                        js_func_code = f"window.{js_name} = function({param_list}) {{\n{js_body}\n}}\n"
                        js_code += js_func_code
                        # Dump per-plugin JS if debug is enabled
                        if debug:
                            plugin_file = os.path.join(tmp_js_dir, f"{plugin.__class__.__name__}_js_dump.js")
                            with open(plugin_file, 'a') as f:
                                f.write(js_func_code)
        return js_code

    async def initialize_all(self, injector, plugin_configs=None):
        plugin_configs = plugin_configs or {}
        for plugin_name in self.plugin_names:
            try:
                print(f"Loading plugin: {plugin_name}...")
                await self._load_plugin(plugin_name, plugin_configs.get(plugin_name, {}), injector)
            except Exception as e:
                console.print(f"[red]Failed to load plugin '{plugin_name}': {e}[/red]")
                logger.error(f"Failed to load plugin '{plugin_name}': {e}")
                logger.debug(traceback.format_exc())

    async def cleanup_all(self):
        for plugin in self.plugins.values():
            cleanup_fn = getattr(plugin, "cleanup", None)
            if cleanup_fn and callable(cleanup_fn):
                if inspect.iscoroutinefunction(cleanup_fn):
                    await cleanup_fn()
                else:
                    cleanup_fn()

    async def update_all(self):
        for plugin in self.plugins.values():
            update_fn = getattr(plugin, "update", None)
            if update_fn and callable(update_fn):
                if inspect.iscoroutinefunction(update_fn):
                    await update_fn()
                else:
                    update_fn()

# --- Add CLI argument parsing utility ---
def parse_plugin_args(params_meta, args):
    """
    params_meta: list of dicts as in plugin_command
    args: list of str from CLI
    Returns: dict of param_name: value
    Raises ValueError on parse error.
    """
    result = {}
    # Special case: single string parameter, join all args
    if len(params_meta) == 1 and params_meta[0].get("type", str) == str:
        name = params_meta[0]["name"]
        if args:
            value = " ".join(args)
            value = value.strip('"\'')
            result[name] = value
        elif "default" in params_meta[0]:
            result[name] = params_meta[0]["default"]
        else:
            raise ValueError(f"Missing required argument: {name}")
        return result
    i = 0
    for meta in params_meta:
        name = meta["name"]
        typ = meta.get("type", str)
        if i < len(args):
            try:
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

# --- Plugin command execution utility ---
def execute_plugin_command(func, call_kwargs, injector=None, plugin_manager=None, console=None):
    """
    Executes a plugin command function with proper injector checking and error handling.
    - func: the plugin command function
    - call_kwargs: dict of arguments to pass (from parse_plugin_args)
    - injector: injector instance (optional)
    - plugin_manager: plugin manager (optional)
    - console: rich.console.Console instance (optional, for printing)
    Returns the result of the command, or prints error and returns None.
    """
    import inspect
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
            import asyncio
            result = asyncio.run(func(**call_kwargs))
        else:
            result = func(**call_kwargs)
        if result is not None and console:
            console.print(f"[JS return] {result}")
        return result
    except Exception as e:
        if console:
            console.print(f"[red]Error executing command: {e}[/red]")
        else:
            print(f"Error executing command: {e}")
        return None