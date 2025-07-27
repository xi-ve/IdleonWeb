import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional
from rich.console import Console

console = Console()
logger = logging.getLogger(__name__)

class ConfigManager:
    _instance = None
    _initialized = False

    def __new__(cls, conf_path: Optional[Path] = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, conf_path: Optional[Path] = None):
        if self._initialized:
            return
        self.conf_path = conf_path or Path(__file__).parent / 'core' / 'conf.json'
        self._config = self._load_config()
        self._initialized = True
        if 'plugin_configs' not in self._config:
            self._config['plugin_configs'] = {}
        if 'plugins' not in self._config:
            self._config['plugins'] = []
        if 'debug' not in self._config:
            self._config['debug'] = False

    def _load_config(self) -> Dict[str, Any]:
        try:
            if self.conf_path.exists():
                with open(self.conf_path, 'r') as f:
                    config = json.load(f)
                logger.info(f"Loaded config from {self.conf_path}")
                return config
            else:
                logger.warning(f"Config file not found at {self.conf_path}, using defaults")
                return self._get_default_config()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        return {
            "openDevTools": False,
            "interactive": True,
            "plugins": [],
            "plugin_configs": {},
            "debug": False,
            "webui": {
                "darkmode": False
            },
            "injector": {
                "cdp_port": 32123,
                "njs_pattern": "*N.js",
                "idleon_url": "https://www.legendsofidleon.com/ytGl5oc/"
            }
        }

    def _save_config(self) -> None:
        try:
            self.conf_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.conf_path, 'w') as f:
                json.dump(self._config, f, indent=2)
            logger.debug(f"Saved config to {self.conf_path}")
        except Exception as e:
            logger.error(f"Error saving config: {e}")
            console.print(f"[red]Error saving config: {e}[/red]")

    def get_plugin_config(self, plugin_name: str) -> Dict[str, Any]:
        return self._config.get('plugin_configs', {}).get(plugin_name, {})

    def set_plugin_config(self, plugin_name: str, config: Dict[str, Any]) -> None:
        if 'plugin_configs' not in self._config:
            self._config['plugin_configs'] = {}
        self._config['plugin_configs'][plugin_name] = config
        self._save_config()
        logger.info(f"Updated config for plugin: {plugin_name}")

    def get_global(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    def set_global(self, key: str, value: Any) -> None:
        self._config[key] = value
        self._save_config()
        logger.info(f"Updated global config: {key} = {value}")

    def get_all_plugin_configs(self) -> Dict[str, Any]:
        return self._config.get('plugin_configs', {})

    def get_plugins_list(self) -> list:
        return self._config.get('plugins', [])

    def set_plugins_list(self, plugins: list) -> None:
        self._config['plugins'] = plugins
        self._save_config()
        logger.info(f"Updated plugins list: {plugins}")

    def add_plugin(self, plugin_name: str, config: Dict[str, Any] = None) -> None:
        plugins = self.get_plugins_list()
        if plugin_name not in plugins:
            plugins.append(plugin_name)
            self.set_plugins_list(plugins)
        if config:
            self.set_plugin_config(plugin_name, config)

    def remove_plugin(self, plugin_name: str) -> None:
        plugins = self.get_plugins_list()
        if plugin_name in plugins:
            plugins.remove(plugin_name)
            self.set_plugins_list(plugins)
        if 'plugin_configs' in self._config and plugin_name in self._config['plugin_configs']:
            del self._config['plugin_configs'][plugin_name]
            self._save_config()

    def reload(self) -> None:
        self._config = self._load_config()
        logger.info("Configuration reloaded from file")

    def get_full_config(self) -> Dict[str, Any]:
        return self._config.copy()

    def set_full_config(self, config: Dict[str, Any]) -> None:
        self._config = config
        self._save_config()
        logger.info("Full configuration updated")

    def get_path(self, path: str, default: Any = None) -> Any:
        keys = path.split('.')
        value = self._config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    def set_path(self, path: str, value: Any) -> None:
        keys = path.split('.')
        d = self._config
        for key in keys[:-1]:
            if key not in d or not isinstance(d[key], dict):
                d[key] = {}
            d = d[key]
        d[keys[-1]] = value
        self._save_config()
        logger.info(f"Set config path '{path}' to {value}")

    # Convenience methods for injector configuration
    def get_injector_config(self) -> Dict[str, Any]:
        """Get the injector configuration section."""
        return self._config.get('injector', {})

    def get_cdp_port(self) -> int:
        """Get the Chrome DevTools Protocol port."""
        return self.get_path('injector.cdp_port', 32123)

    def get_njs_pattern(self) -> str:
        """Get the N.js pattern for interception."""
        return self.get_path('injector.njs_pattern', '*N.js')

    def get_idleon_url(self) -> str:
        """Get the Idleon game URL."""
        return self.get_path('injector.idleon_url', 'https://www.legendsofidleon.com/ytGl5oc/')

    def set_injector_config(self, cdp_port: int = None, njs_pattern: str = None, idleon_url: str = None) -> None:
        """Set injector configuration values."""
        injector_config = self.get_injector_config()
        
        if cdp_port is not None:
            injector_config['cdp_port'] = cdp_port
        if njs_pattern is not None:
            injector_config['njs_pattern'] = njs_pattern
        if idleon_url is not None:
            injector_config['idleon_url'] = idleon_url
        
        self._config['injector'] = injector_config
        self._save_config()
        logger.info("Updated injector configuration")

    # Convenience methods for webui configuration
    def get_webui_config(self) -> Dict[str, Any]:
        """Get the webui configuration section."""
        return self._config.get('webui', {})

    def get_darkmode(self) -> bool:
        """Get the dark mode setting."""
        return self.get_path('webui.darkmode', False)

    def set_darkmode(self, enabled: bool) -> None:
        """Set the dark mode setting."""
        self.set_path('webui.darkmode', enabled)
        logger.info(f"Updated dark mode setting: {enabled}")

    def set_webui_config(self, darkmode: bool = None) -> None:
        """Set webui configuration values."""
        webui_config = self.get_webui_config()
        
        if darkmode is not None:
            webui_config['darkmode'] = darkmode
        
        self._config['webui'] = webui_config
        self._save_config()
        logger.info("Updated webui configuration")

config_manager = ConfigManager() 