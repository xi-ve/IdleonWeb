from ast import Dict
from typing import Any, Dict
from plugin_system import plugin_command, js_export, PluginBase, console
from config_manager import config_manager

class ChangeRatesPlugin(PluginBase):
    VERSION = "1.0.1"
    DESCRIPTION = "Change the rates of the game."

    def __init__(self, config=None):
        super().__init__(config or {})
        self.injector = None
        self.name = 'mob_spawn_rate'
        # Always get the latest debug value from config_manager
        self.debug = config_manager.get_path('plugin_configs.mob_spawn_rate.debug', True)

    async def cleanup(self) -> None:
        pass

    async def update(self) -> None:
        # Always get the latest debug value from config_manager
        self.debug = config_manager.get_path('plugin_configs.mob_spawn_rate.debug', True)

    async def on_game_ready(self) -> None:
        """Called when the game is ready."""
        if self.injector:
            # Call the setup function directly using the injector
            try:
                self.run_js_export('setup_proxy_mob_respawn_rate_js', self.injector)
            except Exception as e:
                console.print(f"[mob_spawn_rate] Error setting up mob spawn rate proxy: {e}")

    async def on_config_changed(self, config: Dict[str, Any]) -> None:
        # Always get the latest debug value from config_manager
        self.debug = config_manager.get_path('plugin_configs.mob_spawn_rate.debug', True)
        if self.debug:
            console.print(f"[mob_spawn_rate] Config changed: {config}")
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)

    @plugin_command(
        help="Toggle instant mob respawn.",
        params=[
            {"name": "toggle", "type": bool, "default": False, "help": "Toggle the mob respawn rate (default: False)"},
        ],
    )
    async def toggle(self, toggle=False, injector=None, **kwargs):
        """Toggle instant mob respawn."""
        # Update config via config_manager
        config_manager.set_path('plugin_configs.mob_spawn_rate.toggle', toggle)
        # Optionally update debug value in memory
        self.debug = config_manager.get_path('plugin_configs.mob_spawn_rate.debug', True)
        # Set the updated config in the browser
        self.set_config(config_manager.get_plugin_config(self.name))

    @js_export()
    def setup_proxy_mob_respawn_rate_js(self):
        return '''
        const ctx = window.__idleon_cheats__;
        const engine = ctx["com.stencyl.Engine"].engine;

        console.log("Setup proxy mob respawn rate");

        console.log(window.pluginConfigs['mob_spawn_rate']?.toggle);
        
        engine.setGameAttribute("MonsterRespawnTime", 
            new Proxy(engine.getGameAttribute("MonsterRespawnTime"), {
                set: function(target, prop, value) {
                    return (target[prop] = window.pluginConfigs['mob_spawn_rate']?.toggle ? 0 : value);
                },
            })
        );
        '''

plugin_class = ChangeRatesPlugin