from ast import Dict
from typing import Any, Dict
from plugin_system import plugin_command, js_export, PluginBase, console
from config_manager import config_manager

class InstantMobRespawnPlugin(PluginBase):
    VERSION = "1.0.1"
    DESCRIPTION = "Change the rates of the game."

    def __init__(self, config=None):
        super().__init__(config or {})
        self.injector = None
        self.name = 'instant_mob_respawn'
        self.debug = config_manager.get_path('plugin_configs.instant_mob_respawn.debug', True)

    async def cleanup(self) -> None:
        pass

    async def update(self) -> None:
        self.debug = config_manager.get_path('plugin_configs.instant_mob_respawn.debug', True)

    async def on_game_ready(self) -> None:
        if self.injector:
            try:
                self.set_config(config_manager.get_plugin_config(self.name))
                self.run_js_export('setup_proxy_mob_respawn_rate_js', self.injector)
            except Exception as e:
                console.print(f"[instant_mob_respawn] Error setting up mob spawn rate proxy: {e}")

    async def on_config_changed(self, config: Dict[str, Any]) -> None:
        self.debug = config_manager.get_path('plugin_configs.instant_mob_respawn.debug', True)
        if self.debug:
            console.print(f"[instant_mob_respawn] Config changed: {config}")
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)

    @plugin_command(
        help="Set instant mob respawn.",
        params=[
            {"name": "toggle", "type": bool, "default": False, "help": "Set the mob respawn rate (default: False)"},
        ],
    )
    async def set(self, toggle=False, injector=None, **kwargs):
        config_manager.set_path('plugin_configs.instant_mob_respawn.toggle', toggle)
        self.debug = config_manager.get_path('plugin_configs.instant_mob_respawn.debug', True)
        self.set_config(config_manager.get_plugin_config(self.name))

    @js_export()
    def setup_proxy_mob_respawn_rate_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            const engine = ctx["com.stencyl.Engine"].engine;
            engine.setGameAttribute("MonsterRespawnTime",
                new Proxy(engine.getGameAttribute("MonsterRespawnTime"), {
                    set: function(target, prop, value) {
                        return (target[prop] = window.pluginConfigs['instant_mob_respawn']?.toggle ? 0 : value);
                    },
                })
            );
            console.log("[instant_mob_respawn] proxy was set");
            return "Mob respawn rate proxy setup successfully";
        } catch (e) {
            console.error("Error setting up mob respawn rate proxy:", e);
            return `Error: ${e.message}`;
        }
        '''

plugin_class = InstantMobRespawnPlugin