from rich.panel import Panel
from plugin_system import plugin_command, js_export, PluginBase

class ChangeRatesPlugin(PluginBase):

    VERSION = "1.0.0"
    DESCRIPTION = "Change the rates of the game."

    def __init__(self, config=None):
        super().__init__(config or {})
        self.injector = None
        self.debug = self.config.get('debug', True)
        self.name = self.__class__.__name__
        self.base_respawn_rate = None

    async def initialize(self, injector) -> bool:
        self.injector = injector
        return True

    async def cleanup(self) -> None:
        pass

    async def update(self) -> None:
        self.debug = self.config.get('debug', True)
        self.respawn_rate_config = self.config.get('RespawnRate', {
            "rate": 0,
            "toggle": False
        })
        if self.base_respawn_rate is None:
            self.base_respawn_rate = self.get_base_respawn_rate()
        if self.respawn_rate_config["toggle"]:
            self.run_js_export('change_mob_respawn_rate_js', self.injector, multiplier=self.respawn_rate_config["rate"])

    async def get_base_respawn_rate(self) -> int:
        return self.injector.run_js_export('get_base_respawn_rate_js')

    @js_export()
    def get_base_respawn_rate_js(self) -> int:
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const engine = ctx["com.stencyl.Engine"].engine;
            return engine.getGameAttribute("MonsterRespawnTime");
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @plugin_command(
        help="Get the base mob respawn rate.",
        params=[],
    )
    async def get_base_respawn_rate(self, injector=None, **kwargs):
        """Get the base mob respawn rate."""
        return self.get_base_respawn_rate()

    @plugin_command(
        help="Change the mob respawn rate.",
        params=[
            {"name": "rate", "type": int, "default": 0, "help": "Rate to change the mob respawn rate to (default: 0)"},
            {"name": "toggle", "type": bool, "default": False, "help": "Toggle the mob respawn rate (default: False)"},
        ],
    )
    async def change_mob_respawn_rate(self, rate=0, toggle=False, injector=None, **kwargs):
        """Change the mob respawn rate."""
        print(f"> Changing mob respawn rate to {rate} (toggle: {toggle})")
        self.respawn_rate_config["rate"] = rate
        self.respawn_rate_config["toggle"] = toggle
        return self.run_js_export('change_mob_respawn_rate_js', injector, multiplier=rate)

    @js_export(params=["multiplier"])
    def change_mob_respawn_rate_js(self, multiplier=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const engine = ctx["com.stencyl.Engine"].engine;
                engine.setGameAttribute("MonsterRespawnTime", 
                new Proxy(engine.getGameAttribute("MonsterRespawnTime"), {
                    get: function(target, prop, receiver) {
                        return 0;
                    },
                    set: function(target, prop, value, receiver) {
                        target[prop] = 0;
                        return true;
                    }
                }));

            return `Changed mob respawn rate to ${multiplier}`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

plugin_class = ChangeRatesPlugin