import importlib
import importlib.util
import inspect
import logging
import asyncio
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, Callable, Union
import traceback
import json
from enum import Enum
import ast

from rich.console import Console
from config_manager import config_manager

GLOBAL_DEBUG = False

logger = logging.getLogger(__name__)
console = Console()

command_registry = {}

def check_js_syntax(js_code: str, plugin_name: str, function_name: str) -> tuple[bool, str]:
    """
    Check JavaScript syntax by attempting to compile/validate the code.
    Returns (is_valid, error_message).
    """
    try:
        # Try to use Node.js to validate the JavaScript syntax
        import subprocess
        import tempfile
        import os
        
        # Create a temporary file with the JavaScript code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as temp_file:
            temp_file.write(js_code)
            temp_file_path = temp_file.name
        
        try:
            # Try to validate the JavaScript using Node.js
            result = subprocess.run(
                ['node', '--check', temp_file_path],
                capture_output=True,
                text=True,
                timeout=5  # 5 second timeout
            )
            
            # Clean up the temporary file
            os.unlink(temp_file_path)
            
            if result.returncode == 0:
                return True, ""
            else:
                # Extract the error message, removing the temp file path
                error_msg = result.stderr.replace(temp_file_path, f"{plugin_name}.{function_name}")
                return False, f"JavaScript syntax error: {error_msg.strip()}"
                
        except subprocess.TimeoutExpired:
            # Clean up the temporary file
            os.unlink(temp_file_path)
            return False, f"JavaScript validation timed out for {plugin_name}.{function_name}"
        except FileNotFoundError:
            # Node.js not available, skip validation
            return True, ""
        except Exception as e:
            # Clean up the temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass
            return False, f"JavaScript validation error: {str(e)}"
            
    except Exception as e:
        return False, f"Syntax check error in {plugin_name}.{function_name}: {str(e)}"

class UIElementType(Enum):
    TOGGLE = "toggle"
    SLIDER = "slider"
    BUTTON = "button"
    SELECT = "select"
    TEXT_INPUT = "text_input"
    NUMBER_INPUT = "number_input"
    COLOR_PICKER = "color_picker"
    FILE_UPLOAD = "file_upload"
    INPUT_WITH_BUTTON = "input_with_button"
    SEARCH_WITH_RESULTS = "search_with_results"
    AUTOCOMPLETE_INPUT = "autocomplete_input"

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

def ui_element(
    element_type: Union[UIElementType, str],
    label: str = None,
    description: str = None,
    config_key: str = None,
    default_value: Any = None,
    min_value: Union[int, float] = None,
    max_value: Union[int, float] = None,
    step: Union[int, float] = None,
    options: List[Dict[str, Any]] = None,
    placeholder: str = None,
    required: bool = False,
    category: str = "General",
    order: int = 0,
    **kwargs
):
    """
    Decorator to create UI elements for plugin configuration.
    
    Args:
        element_type: Type of UI element (toggle, slider, button, etc.)
        label: Display label for the element
        description: Help text for the element
        config_key: Key in plugin config to bind to (defaults to function name)
        default_value: Default value for the element
        min_value: Minimum value for numeric inputs
        max_value: Maximum value for numeric inputs
        step: Step value for sliders
        options: List of options for select elements
        placeholder: Placeholder text for inputs
        required: Whether the field is required
        category: UI category to group elements
        order: Display order within category
        **kwargs: Additional element-specific properties
    """
    def decorator(func: Callable) -> Callable:
        # Convert string to enum if needed
        final_element_type = element_type
        if isinstance(element_type, str):
            try:
                final_element_type = UIElementType(element_type.lower())
            except ValueError:
                raise ValueError(f"Invalid UI element type: {element_type}")
        
        func._ui_element = True
        func._ui_element_type = final_element_type
        func._ui_label = label or func.__name__.replace('_', ' ').title()
        func._ui_description = description or ""
        func._ui_config_key = config_key or func.__name__
        func._ui_default_value = default_value
        func._ui_min_value = min_value
        func._ui_max_value = max_value
        func._ui_step = step
        func._ui_options = options or []
        func._ui_placeholder = placeholder or ""
        func._ui_required = required
        func._ui_category = category
        func._ui_order = order
        func._ui_properties = kwargs
        
        return func
    return decorator

# Convenience decorators for common UI elements
def ui_toggle(label: str = None, description: str = None, config_key: str = None, 
              default_value: bool = False, category: str = "General", order: int = 0):
    """Decorator for toggle/switch UI elements."""
    return ui_element(
        UIElementType.TOGGLE,
        label=label,
        description=description,
        config_key=config_key,
        default_value=default_value,
        category=category,
        order=order
    )

def ui_slider(label: str = None, description: str = None, config_key: str = None,
              default_value: Union[int, float] = 0, min_value: Union[int, float] = 0,
              max_value: Union[int, float] = 100, step: Union[int, float] = 1,
              category: str = "General", order: int = 0):
    """Decorator for slider UI elements."""
    return ui_element(
        UIElementType.SLIDER,
        label=label,
        description=description,
        config_key=config_key,
        default_value=default_value,
        min_value=min_value,
        max_value=max_value,
        step=step,
        category=category,
        order=order
    )

def ui_button(label: str = None, description: str = None, category: str = "Actions", 
              order: int = 0, **kwargs):
    """Decorator for button UI elements."""
    return ui_element(
        UIElementType.BUTTON,
        label=label,
        description=description,
        category=category,
        order=order,
        **kwargs
    )

def ui_select(label: str = None, description: str = None, config_key: str = None,
              options: List[Dict[str, Any]] = None, default_value: Any = None,
              category: str = "General", order: int = 0):
    """Decorator for select/dropdown UI elements."""
    return ui_element(
        UIElementType.SELECT,
        label=label,
        description=description,
        config_key=config_key,
        default_value=default_value,
        options=options or [],
        category=category,
        order=order
    )

def ui_text_input(label: str = None, description: str = None, config_key: str = None,
                  default_value: str = "", placeholder: str = None, required: bool = False,
                  category: str = "General", order: int = 0):
    """Decorator for text input UI elements."""
    return ui_element(
        UIElementType.TEXT_INPUT,
        label=label,
        description=description,
        config_key=config_key,
        default_value=default_value,
        placeholder=placeholder or "",
        required=required,
        category=category,
        order=order
    )

def ui_number_input(label: str = None, description: str = None, config_key: str = None,
                   default_value: Union[int, float] = 0, min_value: Union[int, float] = None,
                   max_value: Union[int, float] = None, step: Union[int, float] = 1,
                   category: str = "General", order: int = 0):
    """Decorator for number input UI elements."""
    return ui_element(
        UIElementType.NUMBER_INPUT,
        label=label,
        description=description,
        config_key=config_key,
        default_value=default_value,
        min_value=min_value,
        max_value=max_value,
        step=step,
        category=category,
        order=order
    )

def ui_input_with_button(label: str = None, description: str = None, button_text: str = "Execute",
                        placeholder: str = None, category: str = "Actions", order: int = 0):
    """Decorator for input field with button UI elements."""
    return ui_element(
        UIElementType.INPUT_WITH_BUTTON,
        label=label,
        description=description,
        placeholder=placeholder or "",
        category=category,
        order=order,
        button_text=button_text
    )

def ui_search_with_results(label: str = None, description: str = None, button_text: str = "Search",
                          placeholder: str = None, category: str = "Search", order: int = 0):
    """Decorator for search input with results list UI elements."""
    return ui_element(
        UIElementType.SEARCH_WITH_RESULTS,
        label=label,
        description=description,
        placeholder=placeholder or "",
        category=category,
        order=order,
        button_text=button_text
    )

def ui_autocomplete_input(label: str = None, description: str = None, button_text: str = "Execute",
                         placeholder: str = None, category: str = "Actions", order: int = 0):
    """Decorator for autocomplete input with button UI elements."""
    return ui_element(
        UIElementType.AUTOCOMPLETE_INPUT,
        label=label,
        description=description,
        placeholder=placeholder or "",
        category=category,
        order=order,
        button_text=button_text
    )

class PluginBase(ABC):
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = True
        self.name = self.__class__.__name__
        self.version = getattr(self, 'VERSION', '1.0.0')
        self.description = getattr(self, 'DESCRIPTION', 'No description provided')
        self.dependencies = getattr(self, 'DEPENDENCIES', [])
        self.plugin_order = getattr(self, 'PLUGIN_ORDER', 0)
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

    def get_ui_elements(self) -> Dict[str, List[Dict[str, Any]]]:
        """Collect all UI elements from the plugin, organized by category."""
        elements_by_category = {}
        
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and getattr(attr, "_ui_element", False):
                config_key = getattr(attr, "_ui_config_key", attr_name)
                default_value = getattr(attr, "_ui_default_value", None)
                
                # Get current value from config manager, fallback to default
                # This matches how plugins actually get their config values
                current_value = config_manager.get_path(f'plugin_configs.{self.name}.{config_key}', default_value)
                
                element_data = {
                    "name": attr_name,
                    "type": getattr(attr, "_ui_element_type", UIElementType.BUTTON).value,
                    "label": getattr(attr, "_ui_label", attr_name),
                    "description": getattr(attr, "_ui_description", ""),
                    "config_key": config_key,
                    "default_value": default_value,
                    "current_value": current_value,
                    "min_value": getattr(attr, "_ui_min_value", None),
                    "max_value": getattr(attr, "_ui_max_value", None),
                    "step": getattr(attr, "_ui_step", None),
                    "options": getattr(attr, "_ui_options", []),
                    "placeholder": getattr(attr, "_ui_placeholder", ""),
                    "required": getattr(attr, "_ui_required", False),
                    "order": getattr(attr, "_ui_order", 0),
                    "properties": getattr(attr, "_ui_properties", {}),
                    "func": attr
                }
                
                category = getattr(attr, "_ui_category", "General")
                if category not in elements_by_category:
                    elements_by_category[category] = []
                elements_by_category[category].append(element_data)
        
        # Sort elements by order within each category
        for category in elements_by_category:
            elements_by_category[category].sort(key=lambda x: x["order"])
        
        return elements_by_category

    def get_ui_schema(self) -> Dict[str, Any]:
        """Generate a complete UI schema for the plugin."""
        ui_elements = self.get_ui_elements()
        
        # Use the plugin's CATEGORY field, or 'General' if not defined
        plugin_category = getattr(self, 'CATEGORY', 'General')
        
        schema = {
            "plugin_info": {
                "name": self.name,
                "description": self.description,
                "version": self.version,
                "category": plugin_category,
                "order": self.plugin_order
            },
            "categories": {}
        }
        
        for category, elements in ui_elements.items():
            schema["categories"][category] = elements
        
        return schema

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
        
        # Use plugin namespace to avoid conflicts
        plugin_name = getattr(self, 'name', self.__class__.__name__)
        check_expr = f"typeof window.{plugin_name}.{js_name} === 'function'"
        try:
            check_result = injector.evaluate(check_expr)
            if not check_result.get('result', {}).get('value', False):
                if GLOBAL_DEBUG:
                    console.print(f"[DEBUG] Function {plugin_name}.{js_name} not found in window")
                return f"Error: Function {plugin_name}.{js_name} not found"
        except Exception as e:
            if GLOBAL_DEBUG:
                console.print(f"[DEBUG] Error checking function {plugin_name}.{js_name}: {e}")
            return f"Error checking function: {e}"
        
        expr = f"window.{plugin_name}.{js_name}({js_args})"
        
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
                console.print(f"[DEBUG] Error executing {plugin_name}.{js_name}: {e}")
            return f"Error executing {plugin_name}.{js_name}: {e}"

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
            
            # Get current config from config manager to ensure we have the latest values
            current_config = config_manager.get_plugin_config(self.name)
            self.set_config(current_config)
        except Exception as e:
            if GLOBAL_DEBUG:
                console.print(f"[DEBUG] Error initializing config: {e}")

    def save_to_global_config(self, config: Dict[str, Any] = None) -> None:
        plugin_config = config or self.config
        
        # Save to config manager using merge method (this automatically saves to file)
        config_manager.update_plugin_config(self.name, plugin_config)
        
        # Update local config to match what was saved
        self.config = config_manager.get_plugin_config(self.name)
        
        # Reload config to ensure consistency
        config_manager.reload()
        
        # Update browser config with the latest values
        if self.injector:
            self.set_config(self.config)

class PluginManager:
    
    def __init__(self, plugin_names: List[str], plugin_dir: str = 'plugins'):
        self.plugins: Dict[str, PluginBase] = {}
        self.plugin_dir = Path(plugin_dir)
        self.plugin_names = plugin_names
        self.failed_plugins = set()  # Track plugins that failed to load

    async def load_plugins(self, injector, plugin_configs: Dict[str, Any] = None, 
                          global_debug: bool = True) -> None:
        # Ensure we have the latest config from file
        config_manager.reload()
        
        if plugin_configs is None:
            plugin_configs = config_manager.get_all_plugin_configs()
        
        for plugin_name in self.plugin_names:
            try:
                if GLOBAL_DEBUG:
                    console.print(f"Loading plugin: {plugin_name}...")
                await self._load_plugin(
                    plugin_name, 
                    plugin_configs.get(plugin_name, {}), 
                    injector, 
                    global_debug=global_debug
                )
                if GLOBAL_DEBUG:
                    console.print(f"Loaded plugin: {plugin_name}")
            except Exception as e:
                console.print(f"[red]Failed to load plugin '{plugin_name}': {e}[/red]")
                logger.error(f"Failed to load plugin '{plugin_name}': {e}")
                self.failed_plugins.add(plugin_name)  # Track failed plugin
                if GLOBAL_DEBUG:
                    logger.debug(traceback.format_exc())

    async def _load_plugin(self, plugin_name: str, plugin_config: Dict, 
                          injector, global_debug: bool = True) -> None:
        plugin_class = await self._load_external_plugin(plugin_name)
        
        if not plugin_class:
            raise ImportError(f"Plugin '{plugin_name}' not found in {self.plugin_dir}")
        
        # Get the latest config from config manager to ensure consistency
        latest_config = config_manager.get_plugin_config(plugin_name)
        # Merge with provided config (provided config takes precedence for initialization)
        merged_config = {**latest_config, **plugin_config}
        
        plugin_instance = plugin_class(merged_config)
        plugin_instance.plugin_manager = self
        plugin_instance.global_debug = global_debug
        
        # Ensure the plugin's local config is synced with the global config
        # This ensures plugins use config_manager.get_path() correctly
        plugin_instance.config = config_manager.get_plugin_config(plugin_name)
        
        for dependency in getattr(plugin_instance, 'dependencies', []):
            if dependency not in self.plugins:
                console.print(f"[yellow]Plugin '{plugin_name}' requires '{dependency}' "
                            f"which is not loaded[/yellow]")
                logger.warning(f"Plugin '{plugin_name}' requires '{dependency}' "
                             f"which is not loaded")

        success = await plugin_instance.initialize(injector)
        if success:
            if GLOBAL_DEBUG:
                console.print(f"Initialized plugin: {plugin_name}")
            self.plugins[plugin_name] = plugin_instance
            logger.info(f"Loaded plugin: {plugin_name}")
        else:
            raise RuntimeError(f"Failed to initialize plugin: {plugin_name}")

    async def _load_external_plugin(self, plugin_name: str) -> Optional[Type[PluginBase]]:
        # Check if this is a folderized plugin (contains a dot)
        if '.' in plugin_name:
            # Split the plugin name into subdirectory and filename
            subdir_name, file_name = plugin_name.split('.', 1)
            plugin_file = self.plugin_dir / subdir_name / f"{file_name}.py"
        else:
            # Regular plugin in root directory
            plugin_file = self.plugin_dir / f"{plugin_name}.py"
        
        if not plugin_file.exists():
            return None
        
        # Create a unique module name to avoid conflicts
        module_name = f"plugins.{plugin_name.replace('.', '_')}"
        spec = importlib.util.spec_from_file_location(module_name, plugin_file)
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
                self.failed_plugins.add(plugin_name)  # Track failed plugin
        
        if injector:
            for plugin in self.plugins.values():
                try:
                    await plugin.on_game_ready()
                    if GLOBAL_DEBUG:
                        console.print(f"Executed on_game_ready for plugin: {plugin.name}")
                except Exception as e:
                    logger.error(f"Error executing on_game_ready for plugin '{plugin.name}': {e}")
        
        if GLOBAL_DEBUG:
            console.print(f"[DEBUG] Plugin initialization complete. {len(self.plugins)} plugins initialized, {len(self.failed_plugins)} failed.")

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

    def get_all_ui_elements(self) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """Collect all UI elements from all plugins, organized by plugin and category."""
        all_ui_elements = {}
        
        for plugin_name, plugin in self.plugins.items():
            # Skip plugins that failed to load
            if plugin_name in self.failed_plugins:
                continue
                
            plugin_ui_elements = plugin.get_ui_elements()
            if plugin_ui_elements:  # Only include plugins with UI elements
                # Use the plugin's UI schema to get proper category information
                plugin_schema = plugin.get_ui_schema()
                all_ui_elements[plugin_name] = plugin_schema
        
        return all_ui_elements

    def get_ui_schema_for_plugin(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """Get UI schema for a specific plugin."""
        plugin = self.plugins.get(plugin_name)
        if plugin:
            return plugin.get_ui_schema()
        return None

    def get_all_ui_schemas(self) -> Dict[str, Dict[str, Any]]:
        """Get UI schemas for all plugins."""
        schemas = {}
        for plugin_name, plugin in self.plugins.items():
            # Skip plugins that failed to load
            if plugin_name in self.failed_plugins:
                continue
            schemas[plugin_name] = plugin.get_ui_schema()
        return schemas

    async def execute_ui_action(self, plugin_name: str, element_name: str, value: Any = None) -> Any:
        """Execute a UI element action for a specific plugin."""
        plugin = self.plugins.get(plugin_name)
        if not plugin:
            return {"error": f"Plugin '{plugin_name}' not found"}
        
        # Find the UI element function
        ui_elements = plugin.get_ui_elements()
        target_func = None
        
        for category_elements in ui_elements.values():
            for element in category_elements:
                if element["name"] == element_name:
                    target_func = element["func"]
                    break
            if target_func:
                break
        
        if not target_func:
            return {"error": f"UI element '{element_name}' not found in plugin '{plugin_name}'"}
        
        try:
            # Check if the function expects a value parameter
            sig = inspect.signature(target_func)
            params = list(sig.parameters.keys())
            
            # Skip 'self' parameter
            if params and params[0] == 'self':
                params = params[1:]
            
            # Execute the function with or without value parameter
            if inspect.iscoroutinefunction(target_func):
                if params and len(params) > 0:
                    result = await target_func(value)
                else:
                    result = await target_func()
            else:
                if params and len(params) > 0:
                    result = target_func(value)
                else:
                    result = target_func()
            
            # Update config if the function has a config_key and value is provided
            config_key = getattr(target_func, "_ui_config_key", None)
            if config_key and value is not None:
                # Update plugin config
                plugin.config[config_key] = value
                
                # Save only the specific config key to global config (this will handle the config change notification)
                config_manager.update_plugin_config(plugin_name, {config_key: value})
                
                # Update the plugin's local config to match what was saved
                plugin.config = config_manager.get_plugin_config(plugin_name)
                
                # Notify the plugin of the config change with the updated config
                if plugin.plugin_manager:
                    try:
                        loop = None
                        try:
                            loop = asyncio.get_running_loop()
                        except RuntimeError:
                            pass
                        if loop and loop.is_running():
                            asyncio.create_task(plugin.plugin_manager.notify_config_changed(plugin.config, plugin_name))
                        else:
                            asyncio.run(plugin.plugin_manager.notify_config_changed(plugin.config, plugin_name))
                    except Exception:
                        pass
            
            return {"success": True, "result": result}
        except Exception as e:
            return {"error": f"Error executing UI action: {str(e)}"}

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
                if GLOBAL_DEBUG:
                    logger.error(f"Error notifying plugin of config change: {e}")
        elif plugin_name is None:
            # Only broadcast to all plugins when no specific plugin is specified
            for name, plugin in self.plugins.items():
                try:
                    await plugin.on_config_changed(plugin.config)
                except Exception as e:
                    if GLOBAL_DEBUG:
                        logger.error(f"Error notifying plugin of config change: {e}")

    def collect_all_plugin_js(self) -> str:
        js_code, _ = self.collect_all_plugin_js_with_sizes()
        return js_code

    def collect_all_plugin_js_with_sizes(self) -> tuple[str, dict[str, int]]:
        js_code = ""
        plugin_sizes = {}
        syntax_errors = []
        plugin_results = []
        
        debug = any(
            hasattr(plugin, 'config') and plugin.config.get('debug', False)
            for plugin in self.plugins.values()
        )
        
        if debug:
            tmp_js_dir = Path(__file__).parent / 'core' / 'tmp_js'
            tmp_js_dir.mkdir(exist_ok=True)
        
        # Add compatibility layer for old-style function calls
        compatibility_layer = """
        // Compatibility layer for old-style function calls
        // This automatically translates window.func_name calls to window.plugin_name.func_name
        if (!window.__compatibility_layer_initialized__) {
            window.__compatibility_layer_initialized__ = true;
            const originalWindow = window;
            window = new Proxy(window, {
                get: function(target, prop) {
                    // If it's a function call pattern, check if it exists in any plugin namespace
                    if (typeof prop === 'string' && !target.hasOwnProperty(prop)) {
                        for (const pluginName in target) {
                            if (target[pluginName] && typeof target[pluginName] === 'object' && target[pluginName][prop]) {
                                return target[pluginName][prop];
                            }
                        }
                    }
                    return target[prop];
                }
            });
        }
        """
        js_code += compatibility_layer
        
        for plugin in self.plugins.values():
            plugin_js = ""
            plugin_name = getattr(plugin, 'name', plugin.__class__.__name__)
            plugin_has_errors = False
            plugin_error_details = []
            
            # Initialize plugin namespace to ensure it exists
            namespace_init = f"window.{plugin_name} = window.{plugin_name} || {{}};\n"
            js_code += namespace_init
            plugin_js += namespace_init
            
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
                        
                        # Check syntax before wrapping
                        is_valid, error_msg = check_js_syntax(js_body, plugin_name, js_name)
                        if not is_valid:
                            syntax_errors.append(f"[{plugin_name}.{js_name}] {error_msg}")
                            plugin_has_errors = True
                            plugin_error_details.append(f"  • {js_name}: {error_msg}")
                            continue
                        
                        wrapped_js_body = f"""
                        try {{
                            await window.__idleon_wait_for_game_ready();
                            
                            {js_body}
                        }} catch (e) {{
                            console.error('[{js_name}] Error:', e);
                            return `Error: ${{e.message}}`;
                        }}
                        """
                        
                        js_func_code = f"window.{plugin_name}.{js_name} = async function({param_list}) {{\n{wrapped_js_body}\n}}\n"
                        
                        js_code += js_func_code
                        plugin_js += js_func_code
            
            # Store individual plugin size
            plugin_sizes[plugin_name] = len(plugin_js)
            
            if debug and plugin_js:
                plugin_file = tmp_js_dir / f"{plugin.__class__.__name__}_js_dump.js"
                with open(plugin_file, 'w', encoding='utf-8') as f:
                    f.write(plugin_js)
            
            # Store plugin result for summary
            plugin_results.append({
                'name': plugin_name,
                'success': not plugin_has_errors,
                'error_details': plugin_error_details,
                'js_size': len(plugin_js)
            })
            
            # Add to failed plugins if JS syntax errors were found
            if plugin_has_errors:
                self.failed_plugins.add(plugin_name)
                console.print(f"[DEBUG] Added {plugin_name} to failed_plugins due to JS syntax errors")
        
        # Display comprehensive summary
        from rich.table import Table
        from rich.panel import Panel
        
        # Create summary table
        summary_table = Table(title="Plugin JavaScript Generation Summary", show_lines=True)
        summary_table.add_column("Plugin Name", style="bold green")
        summary_table.add_column("Status", style="cyan")
        summary_table.add_column("JS Size (KB)", style="magenta")
        summary_table.add_column("Functions", style="yellow")
        
        total_size = 0
        total_functions = 0
        successful_plugins = 0
        failed_plugins = 0
        
        for result in plugin_results:
            status_icon = "✅" if result['success'] else "❌"
            status_text = "Success" if result['success'] else "Failed"
            js_size_kb = f"{result['js_size']/1024:.2f}"
            
            # Count functions for this plugin
            plugin = self.plugins.get(result['name'])
            func_count = len(plugin.get_commands()) if plugin else 0
            
            summary_table.add_row(
                result['name'],
                f"{status_icon} {status_text}",
                js_size_kb,
                str(func_count)
            )
            
            total_size += result['js_size']
            total_functions += func_count
            if result['success']:
                successful_plugins += 1
            else:
                failed_plugins += 1
        
        # Add total row
        summary_table.add_row("", "", "", "")
        summary_table.add_row(
            "TOTAL", 
            f"✅ {successful_plugins} success, ❌ {failed_plugins} failed", 
            f"{total_size/1024:.2f}", 
            str(total_functions),
            style="bold"
        )
        
        console.print(summary_table)
        
        # Show detailed error information if any
        if syntax_errors:
            error_details = []
            for result in plugin_results:
                if not result['success']:
                    error_details.append(f"[bold red]{result['name']}:[/bold red]")
                    error_details.extend(result['error_details'])
                    error_details.append("")  # Empty line between plugins
            
            error_panel = Panel(
                "\n".join(error_details),
                title="[bold red]JavaScript Syntax Errors[/bold red]",
                border_style="red"
            )
            console.print(error_panel)
            console.print("[yellow]Plugins with errors were skipped. Fix the syntax issues and reload.[/yellow]")
        
        return js_code, plugin_sizes

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

    async def reload_plugins(self) -> None:
        """Unload all plugins and reload them from their Python files."""
        if GLOBAL_DEBUG:
            console.print("[DEBUG] Starting plugin reload...")
        
        # Clean up existing plugins
        await self.cleanup_all()
        
        # Clear the plugins dictionary and failed plugins set
        self.plugins.clear()
        self.failed_plugins.clear()
        
        # Clear any cached modules to force fresh reload
        import sys
        modules_to_remove = []
        for module_name in sys.modules.keys():
            if module_name.startswith('plugins.'):
                modules_to_remove.append(module_name)
        
        for module_name in modules_to_remove:
            if module_name in sys.modules:
                del sys.modules[module_name]
                if GLOBAL_DEBUG:
                    console.print(f"[DEBUG] Removed cached module: {module_name}")
        
        # Reload configuration
        config_manager.reload()
        plugin_configs = config_manager.get_all_plugin_configs()
        
        # Reload all plugins
        for plugin_name in self.plugin_names:
            try:
                if GLOBAL_DEBUG:
                    console.print(f"[DEBUG] Reloading plugin: {plugin_name}...")
                await self._load_plugin(
                    plugin_name, 
                    plugin_configs.get(plugin_name, {}), 
                    None,  # No injector during reload
                    global_debug=GLOBAL_DEBUG
                )
                if GLOBAL_DEBUG:
                    console.print(f"[DEBUG] Reloaded plugin: {plugin_name}")
            except Exception as e:
                console.print(f"[red]Failed to reload plugin '{plugin_name}': {e}[/red]")
                logger.error(f"Failed to reload plugin '{plugin_name}': {e}")
                self.failed_plugins.add(plugin_name)  # Track failed plugin
                if GLOBAL_DEBUG:
                    logger.debug(traceback.format_exc())
        
        if GLOBAL_DEBUG:
            console.print(f"[DEBUG] Plugin reload complete. Loaded {len(self.plugins)} plugins, {len(self.failed_plugins)} failed.")

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