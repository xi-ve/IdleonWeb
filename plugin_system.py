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

from rich.console import Console
from config_manager import config_manager

GLOBAL_DEBUG = False

logger = logging.getLogger(__name__)
console = Console()

command_registry = {}

def plugin_command(help: str = None, js_export: bool = False, params: List[Dict[str, Any]] = None):
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
    def decorator(func: Callable) -> Callable:
        func._js_export = True
        func._js_params = params or []
        return func
    return decorator

class PluginBase(ABC):
    
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
        if GLOBAL_DEBUG:
            console.print(f"[DEBUG] Initializing plugin {self.name}")
        
        self.injector = injector
        
        if injector:
            self.init_config_in_browser()
        
        return True

    @abstractmethod
    async def on_game_ready(self) -> None:
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        pass

    @abstractmethod
    async def update(self) -> None:
        pass

    @abstractmethod
    async def on_config_changed(self, config: Dict[str, Any]) -> None:
        pass

    def get_commands(self) -> Dict[str, Dict[str, Any]]:
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
        return []

    def get_js_exports(self) -> List[Callable]:
        exports = []
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if (callable(attr) and 
                getattr(attr, "_plugin_command", False) and 
                getattr(attr, "_js_export", False)):
                exports.append(attr)
        return exports

    def run_js_export(self, js_func_name: str, injector, **params) -> Any:
        if not injector:
            if GLOBAL_DEBUG:
                console.print(f"[DEBUG] No injector available for {js_func_name}")
            return None
            
        js_func = getattr(self, js_func_name)
        js_name = js_func_name[:-3] if js_func_name.endswith('_js') else js_func_name
        
        js_params = getattr(js_func, '_js_params', [])
        args = [params.get(p, '') for p in js_params]
        
        js_args = ', '.join(json.dumps(a) for a in args)
        
        check_expr = f"typeof window.{js_name} === 'function'"
        try:
            check_result = injector.evaluate(check_expr)
            if not check_result.get('result', {}).get('value', False):
                if GLOBAL_DEBUG:
                    console.print(f"[DEBUG] Function {js_name} not found in window")
                return f"Error: Function {js_name} not found"
        except Exception as e:
            if GLOBAL_DEBUG:
                console.print(f"[DEBUG] Error checking function {js_name}: {e}")
            return f"Error checking function: {e}"
        
        expr = f"window.{js_name}({js_args})"
        
        if GLOBAL_DEBUG:
            console.print(f"[DEBUG] Executing: {expr}")
        
        try:
            result = injector.evaluate(expr, awaitPromise=True)
            value = result.get('result', {}).get('value')
            if GLOBAL_DEBUG:
                console.print(f"[DEBUG] Result: {value}")
            return value
        except Exception as e:
            if GLOBAL_DEBUG:
                console.print(f"[DEBUG] Error executing {js_name}: {e}")
            return f"Error executing {js_name}: {e}"

    def set_config(self, config: Dict[str, Any]) -> None:
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
        if not self.injector:
            return
        
        if GLOBAL_DEBUG:
            console.print(f"[DEBUG] Initializing config for plugin {self.name}")
        
        try:
            init_expr = "window.pluginConfigs = window.pluginConfigs || {};"
            self.injector.evaluate(init_expr)
            
            self.set_config(self.config)
        except Exception as e:
            if GLOBAL_DEBUG:
                console.print(f"[DEBUG] Error initializing config: {e}")

    def save_to_global_config(self, config: Dict[str, Any] = None) -> None:
        plugin_config = config or self.config
        
        config_manager.set_plugin_config(self.name, plugin_config)
        
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
                pass

class PluginManager:
    
    def __init__(self, plugin_names: List[str], plugin_dir: str = 'plugins'):
        self.plugins: Dict[str, PluginBase] = {}
        self.plugin_dir = Path(plugin_dir)
        self.plugin_names = plugin_names

    async def load_plugins(self, injector, plugin_configs: Dict[str, Any] = None, 
                          global_debug: bool = True) -> None:
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
        plugin_class = await self._load_external_plugin(plugin_name)
        
        if not plugin_class:
            raise ImportError(f"Plugin '{plugin_name}' not found in {self.plugin_dir}")
        
        plugin_instance = plugin_class(plugin_config)
        plugin_instance.plugin_manager = self
        plugin_instance.global_debug = global_debug
        
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
        plugin_file = self.plugin_dir / f"{plugin_name}.py"
        
        if not plugin_file.exists():
            return None
        
        spec = importlib.util.spec_from_file_location(plugin_name, plugin_file)
        if not spec or not spec.loader:
            return None
            
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        for name, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) and 
                issubclass(obj, PluginBase) and 
                obj != PluginBase):
                return obj
        
        return None

    async def initialize_all(self, injector, plugin_configs: Dict[str, Any] = None) -> None:
        plugin_configs = plugin_configs or {}
        
        if GLOBAL_DEBUG:
            console.print(f"[DEBUG] Initializing all plugins with injector")
        
        for plugin_name in self.plugin_names:
            try:
                if plugin_name in self.plugins:
                    plugin = self.plugins[plugin_name]
                    plugin.injector = injector
                    await plugin.initialize(injector)
                    if GLOBAL_DEBUG:
                        console.print(f"Re-initialized plugin: {plugin_name}")
                else:
                    await self._load_plugin(
                        plugin_name, 
                        plugin_configs.get(plugin_name, {}), 
                        injector
                    )
            except Exception as e:
                console.print(f"[red]Failed to initialize plugin '{plugin_name}': {e}[/red]")
                logger.error(f"Failed to initialize plugin '{plugin_name}': {e}")
        
        if injector:
            for plugin in self.plugins.values():
                try:
                    await plugin.on_game_ready()
                    if GLOBAL_DEBUG:
                        console.print(f"Executed on_game_ready for plugin: {plugin.name}")
                except Exception as e:
                    logger.error(f"Error executing on_game_ready for plugin '{plugin.name}': {e}")

    async def cleanup_all(self) -> None:
        for plugin_name, plugin in list(self.plugins.items()):
            try:
                await plugin.cleanup()
                logger.info(f"Cleaned up plugin: {plugin_name}")
            except Exception as e:
                logger.error(f"Error cleaning up plugin '{plugin_name}': {e}")

    async def update_all(self) -> None:
        for plugin in self.plugins.values():
            try:
                await plugin.update()
            except Exception as e:
                logger.error(f"Error updating plugin: {e}")

    def get_plugin(self, name: str) -> Optional[PluginBase]:
        return self.plugins.get(name)

    async def unload_plugin(self, plugin_name: str) -> None:
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

    async def notify_config_changed(self, config: Dict[str, Any], plugin_name: str = None) -> None:
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
        js_code = ""
        
        debug = any(
            hasattr(plugin, 'config') and plugin.config.get('debug', False)
            for plugin in self.plugins.values()
        )
        
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
                        
                        sig = inspect.signature(func)
                        if js_params and len(js_params) > 0:
                            param_list = ", ".join(js_params)
                            bound_args = []
                            for p in js_params:
                                if p in sig.parameters and sig.parameters[p].default != inspect.Parameter.empty:
                                    bound_args.append(sig.parameters[p].default)
                                else:
                                    bound_args.append('')
                            js_body = func(*bound_args)
                        else:
                            params = list(sig.parameters.keys())[1:]
                            param_list = ", ".join(params) if params else ""
                            bound_args = []
                            for p in params:
                                param = sig.parameters[p]
                                if param.default != inspect.Parameter.empty:
                                    bound_args.append(param.default)
                                else:
                                    bound_args.append('')
                            js_body = func(*bound_args)
                        
                        js_name = attr_name[:-3]
                        
                        wrapped_js_body = f"""
                        try {{
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
            
            if debug and plugin_js:
                plugin_file = tmp_js_dir / f"{plugin.__class__.__name__}_js_dump.js"
                with open(plugin_file, 'w') as f:
                    f.write(plugin_js)
        
        return js_code

    def reload_configs_from_file(self) -> None:
        config_manager.reload()
        
        plugin_configs = config_manager.get_all_plugin_configs()
        
        for plugin_name, plugin in self.plugins.items():
            if plugin_name in plugin_configs:
                old_config = plugin.config.copy()
                plugin.config.update(plugin_configs[plugin_name])
                
                if hasattr(plugin, 'injector') and plugin.injector:
                    plugin.set_config(plugin.config)
                
                try:
                    asyncio.create_task(plugin.on_config_changed(plugin.config))
                except RuntimeError:
                    try:
                        asyncio.run(plugin.on_config_changed(plugin.config))
                    except:
                        pass
                
                console.print(f"[green]Reloaded config for plugin: {plugin_name}[/green]")
            else:
                console.print(f"[yellow]No config found for plugin: {plugin_name}[/yellow]")

def parse_plugin_args(params_meta: List[Dict[str, Any]], args: List[str]) -> Dict[str, Any]:
    result = {}
    
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
    
    i = 0
    for meta in params_meta:
        name = meta["name"]
        typ = meta.get("type", str)
        
        if i < len(args):
            try:
                if typ == bool:
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
    sig = inspect.signature(func)
    
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
        
        if result is not None and console:
            console.print(f"[JS return] {result}")
        
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
                    pass
        
        return result
    except Exception as e:
        if console:
            console.print(f"[red]Error executing command: {e}[/red]")
        else:
            print(f"Error executing command: {e}")
        return None