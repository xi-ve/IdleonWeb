import json
import logging
import os
import sys
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
        self.conf_path = conf_path or self._get_config_path()
        self._config = self._load_config()
        self._initialized = True
        if 'plugin_configs' not in self._config:
            self._config['plugin_configs'] = {}
        if 'plugins' not in self._config:
            self._config['plugins'] = []
        if 'debug' not in self._config:
            self._config['debug'] = False
        if 'webui' not in self._config:
            self._config['webui'] = {}
        if 'darkmode' not in self._config['webui']:
            self._config['webui']['darkmode'] = False
        if 'autoOpenOnInject' not in self._config['webui']:
            self._config['webui']['autoOpenOnInject'] = True
        if 'url' not in self._config['webui']:
            self._config['webui']['url'] = 'http://localhost:8080'
        if 'port' not in self._config['webui']:
            self._config['webui']['port'] = 8080
        if 'browser' not in self._config:
            self._config['browser'] = {}
        if 'path' not in self._config['browser']:
            self._config['browser']['path'] = ''
        if 'name' not in self._config['browser']:
            self._config['browser']['name'] = 'auto'
        
        # Auto-detect browser if not configured
        if not self._config['browser']['path']:
            self.auto_detect_browser()
        
        # Migrate autoInject to injector section if it exists at root level
        if 'autoInject' in self._config and 'injector' in self._config:
            if 'autoInject' not in self._config['injector']:
                self._config['injector']['autoInject'] = self._config['autoInject']
            del self._config['autoInject']
            self._save_config()  # Save the migrated config
        elif 'autoInject' in self._config:
            # Create injector section and move autoInject there
            if 'injector' not in self._config:
                self._config['injector'] = {}
            self._config['injector']['autoInject'] = self._config['autoInject']
            del self._config['autoInject']
            self._save_config()  # Save the migrated config
        
        # Ensure injector section exists with autoInject
        if 'injector' not in self._config:
            self._config['injector'] = {}
        if 'autoInject' not in self._config['injector']:
            self._config['injector']['autoInject'] = True

    def _get_config_path(self) -> Path:
        """Determine the correct config path based on execution mode."""
        # Check if running as a standalone PyInstaller executable
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # Running as PyInstaller executable
            executable_dir = Path(sys.executable).parent
            config_path = executable_dir / 'conf.json'
            logger.info(f"Standalone mode detected, using config at: {config_path}")
            return config_path
        elif os.environ.get("IDLEONWEB_STANDALONE") == "1":
            # Running in standalone mode (even if not frozen)
            executable_dir = Path(sys.executable).parent
            config_path = executable_dir / 'conf.json'
            logger.info(f"Standalone environment detected, using config at: {config_path}")
            return config_path
        else:
            # Running in development mode
            config_path = Path(__file__).parent / 'core' / 'conf.json'
            logger.info(f"Development mode detected, using config at: {config_path}")
            return config_path

    def _load_config(self) -> Dict[str, Any]:
        try:
            if self.conf_path.exists():
                with open(self.conf_path, 'r', encoding='utf-8') as f:
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
            "debug": False,
            "webui": {
                "darkmode": False,
                "autoOpenOnInject": True,
                "url": "http://localhost:8080"
            },
            "injector": {
                "cdp_port": 32123,
                "njs_pattern": "*N.js",
                "idleon_url": "https://www.legendsofidleon.com/ytGl5oc/",
                "timeout": 120000,
                "autoInject": True
            }
        }

    def _save_config(self) -> None:
        try:
            self.conf_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.conf_path, 'w', encoding='utf-8') as f:
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

    def update_plugin_config(self, plugin_name: str, config_updates: Dict[str, Any]) -> None:
        if 'plugin_configs' not in self._config:
            self._config['plugin_configs'] = {}

        existing_config = self._config['plugin_configs'].get(plugin_name, {})        
        updated_config = {**existing_config, **config_updates}        
        self._config['plugin_configs'][plugin_name] = updated_config
        self._save_config()
        
        logger.info(f"Updated config for plugin: {plugin_name} (merged {len(config_updates)} keys)")

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

    def get_injector_config(self) -> Dict[str, Any]:
        return self._config.get('injector', {})

    def get_cdp_port(self) -> int:
        return self.get_path('injector.cdp_port', 32123)

    def get_njs_pattern(self) -> str:
        return self.get_path('injector.njs_pattern', '*N.js')

    def get_idleon_url(self) -> str:
        return self.get_path('injector.idleon_url', 'https://www.legendsofidleon.com/ytGl5oc/')

    def get_timeout(self) -> int:
        return self.get_path('injector.timeout', 120000)

    def set_injector_config(self, cdp_port: int = None, njs_pattern: str = None, idleon_url: str = None, timeout: int = None) -> None:
        injector_config = self.get_injector_config()
        
        if cdp_port is not None:
            injector_config['cdp_port'] = cdp_port
        if njs_pattern is not None:
            injector_config['njs_pattern'] = njs_pattern
        if idleon_url is not None:
            injector_config['idleon_url'] = idleon_url
        if timeout is not None:
            injector_config['timeout'] = timeout
        
        self._config['injector'] = injector_config
        self._save_config()
        logger.info("Updated injector configuration")

    def get_webui_config(self) -> Dict[str, Any]:
        return self._config.get('webui', {})

    def get_darkmode(self) -> bool:
        return self.get_path('webui.darkmode', False)

    def set_darkmode(self, enabled: bool) -> None:
        self.set_path('webui.darkmode', enabled)
        logger.info(f"Updated dark mode setting: {enabled}")

    def get_webui_auto_open(self) -> bool:
        return self.get_path('webui.autoOpenOnInject', True)

    def set_webui_auto_open(self, enabled: bool) -> None:
        self.set_path('webui.autoOpenOnInject', enabled)
        logger.info(f"Updated web UI auto open setting: {enabled}")

    def get_webui_url(self) -> str:
        return self.get_path('webui.url', 'http://localhost:8080')

    def set_webui_url(self, url: str) -> None:
        self.set_path('webui.url', url)
        logger.info(f"Updated web UI URL: {url}")

    def get_webui_port(self) -> int:
        return self.get_path('webui.port', 8080)

    def set_webui_port(self, port: int) -> None:
        self.set_path('webui.port', port)
        # Automatically update the URL to match the new port
        url = f"http://localhost:{port}"
        self.set_path('webui.url', url)
        logger.info(f"Updated web UI port: {port} and URL: {url}")

    def get_webui_url_from_port(self) -> str:
        """Get the webui URL constructed from the current port setting"""
        port = self.get_webui_port()
        return f"http://localhost:{port}"

    def set_webui_config(self, darkmode: bool = None, autoOpenOnInject: bool = None, url: str = None, port: int = None) -> None:
        webui_config = self.get_webui_config()
        
        if darkmode is not None:
            webui_config['darkmode'] = darkmode
        if autoOpenOnInject is not None:
            webui_config['autoOpenOnInject'] = autoOpenOnInject
        if url is not None:
            webui_config['url'] = url
        if port is not None:
            webui_config['port'] = port
        
        self._config['webui'] = webui_config
        self._save_config()
        logger.info("Updated webui configuration")

    def get_browser_config(self) -> Dict[str, Any]:
        return self._config.get('browser', {})

    def get_browser_path(self) -> str:
        return self.get_path('browser.path', '')

    def set_browser_path(self, path: str) -> None:
        self.set_path('browser.path', path)
        logger.info(f"Updated browser path: {path}")

    def get_browser_name(self) -> str:
        return self.get_path('browser.name', 'auto')

    def set_browser_name(self, name: str) -> None:
        self.set_path('browser.name', name)
        logger.info(f"Updated browser name: {name}")

    def set_browser_config(self, path: str = None, name: str = None) -> None:
        browser_config = self.get_browser_config()
        
        if path is not None:
            browser_config['path'] = path
        if name is not None:
            browser_config['name'] = name
        
        self._config['browser'] = browser_config
        self._save_config()
        logger.info("Updated browser configuration")

    def auto_detect_browser(self) -> bool:
        """Auto-detect browser and write to config if found"""
        import os
        import platform
        
        # Only auto-detect if no browser is configured
        if self.get_browser_path():
            return True
        
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
        elif system == 'darwin':  # macOS
            possible_paths = [
                '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                '/Applications/Chromium.app/Contents/MacOS/Chromium',
                '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
                '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
                '/Applications/Opera GX.app/Contents/MacOS/Opera GX',
            ]
        
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
                    browser_type = 'auto'
                
                # Auto-write the detected browser to config
                self.set_browser_path(path)
                self.set_browser_name(browser_type)
                logger.info(f"Auto-detected browser: {browser_type} at {path}")
                return True
        
        return False

    def get_auto_inject(self) -> bool:
        return self.get_path('injector.autoInject', True)

    def set_auto_inject(self, enabled: bool) -> None:
        self.set_path('injector.autoInject', enabled)
        logger.info(f"Updated auto inject setting: {enabled}")

config_manager = ConfigManager() 