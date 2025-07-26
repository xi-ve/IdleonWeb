"""
Global Configuration Manager

This module provides a centralized configuration management system
that serves as the single source of truth for all application and plugin configurations.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional
from rich.console import Console

console = Console()
logger = logging.getLogger(__name__)

class ConfigManager:
    """
    Global configuration manager - single source of truth for all config.
    """
    _instance = None
    _initialized = False

    def __new__(cls, conf_path: Optional[Path] = None):
        """
        Singleton instance creation for ConfigManager.
        Args:
            conf_path (Path, optional): Path to the config file.
        Returns:
            ConfigManager: The singleton instance.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, conf_path: Optional[Path] = None):
        """
        Initialize the ConfigManager, loading config from file or defaults.
        Args:
            conf_path (Path, optional): Path to the config file.
        """
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
        """
        Load configuration from file.
        Returns:
            dict: The loaded configuration.
        """
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
        """
        Get default configuration values.
        Returns:
            dict: Default configuration.
        """
        return {
            "openDevTools": False,
            "interactive": True,
            "plugins": [],
            "plugin_configs": {},
            "debug": False,
            "injectFiles": ["plugins_combined.js"]
        }

    def _save_config(self) -> None:
        """
        Save configuration to file.
        """
        try:
            self.conf_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.conf_path, 'w') as f:
                json.dump(self._config, f, indent=2)
            logger.debug(f"Saved config to {self.conf_path}")
        except Exception as e:
            logger.error(f"Error saving config: {e}")
            console.print(f"[red]Error saving config: {e}[/red]")

    def get_plugin_config(self, plugin_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific plugin.
        Args:
            plugin_name (str): Name of the plugin.
        Returns:
            dict: Plugin configuration.
        """
        return self._config.get('plugin_configs', {}).get(plugin_name, {})

    def set_plugin_config(self, plugin_name: str, config: Dict[str, Any]) -> None:
        """
        Set configuration for a specific plugin and save.
        Args:
            plugin_name (str): Name of the plugin.
            config (dict): Plugin configuration.
        """
        if 'plugin_configs' not in self._config:
            self._config['plugin_configs'] = {}
        self._config['plugin_configs'][plugin_name] = config
        self._save_config()
        logger.info(f"Updated config for plugin: {plugin_name}")

    def get_global(self, key: str, default: Any = None) -> Any:
        """
        Get a global configuration value.
        Args:
            key (str): Config key.
            default (Any, optional): Default value if key not found.
        Returns:
            Any: The value for the key or default.
        """
        return self._config.get(key, default)

    def set_global(self, key: str, value: Any) -> None:
        """
        Set a global configuration value and save.
        Args:
            key (str): Config key.
            value (Any): Value to set.
        """
        self._config[key] = value
        self._save_config()
        logger.info(f"Updated global config: {key} = {value}")

    def get_all_plugin_configs(self) -> Dict[str, Any]:
        """
        Get all plugin configurations.
        Returns:
            dict: All plugin configurations.
        """
        return self._config.get('plugin_configs', {})

    def get_plugins_list(self) -> list:
        """
        Get the list of enabled plugins.
        Returns:
            list: List of plugin names.
        """
        return self._config.get('plugins', [])

    def set_plugins_list(self, plugins: list) -> None:
        """
        Set the list of enabled plugins and save.
        Args:
            plugins (list): List of plugin names.
        """
        self._config['plugins'] = plugins
        self._save_config()
        logger.info(f"Updated plugins list: {plugins}")

    def add_plugin(self, plugin_name: str, config: Dict[str, Any] = None) -> None:
        """
        Add a plugin to the configuration.
        Args:
            plugin_name (str): Name of the plugin.
            config (dict, optional): Plugin configuration.
        """
        plugins = self.get_plugins_list()
        if plugin_name not in plugins:
            plugins.append(plugin_name)
            self.set_plugins_list(plugins)
        if config:
            self.set_plugin_config(plugin_name, config)

    def remove_plugin(self, plugin_name: str) -> None:
        """
        Remove a plugin from the configuration and delete its config.
        Args:
            plugin_name (str): Name of the plugin.
        """
        plugins = self.get_plugins_list()
        if plugin_name in plugins:
            plugins.remove(plugin_name)
            self.set_plugins_list(plugins)
        if 'plugin_configs' in self._config and plugin_name in self._config['plugin_configs']:
            del self._config['plugin_configs'][plugin_name]
            self._save_config()

    def reload(self) -> None:
        """
        Reload configuration from file.
        """
        self._config = self._load_config()
        logger.info("Configuration reloaded from file")

    def get_full_config(self) -> Dict[str, Any]:
        """
        Get the complete configuration dictionary.
        Returns:
            dict: The full configuration.
        """
        return self._config.copy()

    def set_full_config(self, config: Dict[str, Any]) -> None:
        """
        Set the complete configuration dictionary and save.
        Args:
            config (dict): The full configuration.
        """
        self._config = config
        self._save_config()
        logger.info("Full configuration updated")

    def get_path(self, path: str, default: Any = None) -> Any:
        """
        Get a value from the config using a dotted path (e.g., 'plugin_configs.mob_spawn_rate.toggle').
        Args:
            path (str): Dotted path to the config value.
            default (Any, optional): Default value if path not found.
        Returns:
            Any: The value at the path or default.
        """
        keys = path.split('.')
        value = self._config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    def set_path(self, path: str, value: Any) -> None:
        """
        Set a value in the config using a dotted path (e.g., 'plugin_configs.mob_spawn_rate.toggle').
        Automatically saves the config after updating.
        Args:
            path (str): Dotted path to the config value.
            value (Any): Value to set.
        """
        keys = path.split('.')
        d = self._config
        for key in keys[:-1]:
            if key not in d or not isinstance(d[key], dict):
                d[key] = {}
            d = d[key]
        d[keys[-1]] = value
        self._save_config()
        logger.info(f"Set config path '{path}' to {value}")

# Global instance
config_manager = ConfigManager() 