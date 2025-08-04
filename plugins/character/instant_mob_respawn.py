from ast import Dict
import time
from typing import Any, Dict
from plugin_system import plugin_command, js_export, PluginBase, console, ui_toggle, ui_button
from config_manager import config_manager

class InstantMobRespawnPlugin(PluginBase):
    VERSION = "1.0.4"
    DESCRIPTION = "Change the rates of the game."
    PLUGIN_ORDER = 4
    CATEGORY = "Character"

    def __init__(self, config=None):
        super().__init__(config or {})
        self.injector = None
        self.name = 'instant_mob_respawn'
        self.debug = config_manager.get_path('plugin_configs.instant_mob_respawn.debug', False)
        self.last_update = 0

    async def cleanup(self) -> None:
        pass

    async def update(self) -> None:
        self.debug = config_manager.get_path('plugin_configs.instant_mob_respawn.debug', False)
        if self.last_update < time.time() - 10:
            self.last_update = time.time()
            if hasattr(self, 'injector') and self.injector and config_manager.get_path('plugin_configs.instant_mob_respawn.enabled', False):
                try:
                    proxy_status = self.run_js_export('check_proxy_status_js', self.injector)
                    if not proxy_status:
                        self.run_js_export('setup_proxy_mob_respawn_rate_js', self.injector, enabled=self.config.get('toggle', False))
                except Exception as e:
                    if self.debug:
                        console.print(f"[instant_mob_respawn] Error checking proxy status: {e}")

    async def on_game_ready(self) -> None:
        if self.injector:
            try:
                self.set_config(config_manager.get_plugin_config(self.name))
                self.run_js_export('setup_proxy_mob_respawn_rate_js', self.injector)
            except Exception as e:
                console.print(f"[instant_mob_respawn] Error setting up mob spawn rate proxy: {e}")

    async def on_config_changed(self, config: Dict[str, Any]) -> None:
        self.debug = config_manager.get_path('plugin_configs.instant_mob_respawn.debug', False)
        if  self.debug:
            console.print(f"[instant_mob_respawn] Config changed: {config}")
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)

    @ui_toggle(
        label="Enable Instant Mob Respawn",
        description="Toggle instant mob respawn functionality",
        config_key="toggle",
        default_value=False
    )
    async def enable_instant_respawn(self, value: bool = None):
        if value is not None:
            self.config["toggle"] = value
            self.save_to_global_config()
        return f"Instant mob respawn {'enabled' if self.config.get('toggle', False) else 'disabled'}"

    @ui_toggle(
        label="Debug Mode",
        description="Enable debug logging for mob respawn plugin",
        config_key="debug",
        default_value=False
    )
    async def enable_debug(self, value: bool = None):
        if value is not None:
            self.config["debug"] = value
            self.save_to_global_config()
        return f"Debug mode {'enabled' if self.config.get('debug', False) else 'disabled'}"

    @plugin_command(
        help="Set instant mob respawn.",
        params=[
            {"name": "toggle", "type": bool, "default": False, "help": "Set the mob respawn rate (default: False)"}
        ],
    )
    async def set(self, toggle=False, injector=None, **kwargs):
        config_manager.set_path('plugin_configs.instant_mob_respawn.toggle', toggle)
        self.debug = config_manager.get_path('plugin_configs.instant_mob_respawn.debug', False)
        self.set_config(config_manager.get_plugin_config(self.name))

    @js_export()
    def setup_proxy_mob_respawn_rate_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            const engine = ctx["com.stencyl.Engine"].engine;
            
            if (window.__mob_respawn_proxy_setup__) {
                console.log("[instant_mob_respawn] Proxy already set up");
            }
            
            if (!window.__mob_respawn_original__) {
                window.__mob_respawn_original__ = engine.getGameAttribute("MonsterRespawnTime");
                console.log("[instant_mob_respawn] Stored original MonsterRespawnTime");
            }
            
            const originalRespawnTime = window.__mob_respawn_original__;
            const proxy = new Proxy(originalRespawnTime, {
                set: function(target, prop, value) {
                    const pluginConfig = window.pluginConfigs && window.pluginConfigs['instant_mob_respawn'];
                    const shouldUseZero = pluginConfig && pluginConfig.toggle;
                    
                    if (shouldUseZero) {
                        return (target[prop] = 0);
                    } else {
                        return (target[prop] = value);
                    }
                },
                get: function(target, prop) {
                    const pluginConfig = window.pluginConfigs && window.pluginConfigs['instant_mob_respawn'];
                    const shouldUseZero = pluginConfig && pluginConfig.toggle;
                    
                    if (shouldUseZero && prop !== 'constructor' && prop !== 'toString' && prop !== 'valueOf') {
                        return 0;
                    }
                    return target[prop];
                }
            });
            
            engine.setGameAttribute("MonsterRespawnTime", proxy);
            window.__mob_respawn_proxy_setup__ = true;
            
            console.log("[instant_mob_respawn] Proxy was set successfully");
            return "Mob respawn rate proxy setup successfully";
        } catch (e) {
            console.error("Error setting up mob respawn rate proxy:", e);
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def check_proxy_status_js(self):
        return '''
        try {
            const isProxySetup = window.__mob_respawn_proxy_setup__ === true;            
            return isProxySetup;
        } catch (e) {
            console.error("Error checking proxy status:", e);
            return false;
        }
        '''

plugin_class = InstantMobRespawnPlugin