from plugin_system import PluginBase, js_export, ui_toggle, ui_autocomplete_input, plugin_command, console

class InstantAfkTimePlugin(PluginBase):
    VERSION = "1.0.1"
    DESCRIPTION = "Set instant AFK time and trigger character selection screen."
    PLUGIN_ORDER = 2
    CATEGORY = "Character"

    def __init__(self, config=None):
        super().__init__(config or {})
        self.name = 'instant_afk_time'
        self.debug = config.get('debug', False) if config else False

    async def cleanup(self): pass
    async def update(self): pass
    async def on_config_changed(self, config): 
        self.debug = config.get('debug', False)
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)
    async def on_game_ready(self): pass

    @ui_toggle(
        label="Debug Mode",
        description="Enable debug logging for instant AFK time plugin",
        config_key="debug",
        default_value=False
    )
    async def enable_debug(self, value: bool = None):
        if value is not None:
            self.debug = value
            if hasattr(self, 'injector') and self.injector:
                self.set_config({"debug": value})
        return f"Debug mode {'enabled' if self.debug else 'disabled'}"

    @ui_autocomplete_input(
        label="Set Instant AFK Time",
        description="Set AFK time and trigger character selection screen.",
        button_text="Set AFK Time",
        placeholder="e.g. 8"
    )
    async def set_instant_afk_time_ui(self, value: str = None):
        if not value:
            return "Please enter hours (e.g. 8)"
        
        try:
            hours = int(value)
            if hours <= 0:
                return "Hours must be greater than 0"
            
            if hasattr(self, 'injector') and self.injector:
                try:
                    result = await self.set_instant_afk_time(hours)
                    return f"SUCCESS: {result}"
                except Exception as e:
                    return f"ERROR: {str(e)}"
            else:
                return "ERROR: No injector available - run 'inject' first"
                
        except ValueError:
            return "Please enter a valid number of hours"

    def get_set_instant_afk_time_ui_autocomplete(self, query: str = ""):
        suggestions = []
        if query:
            suggestions = [f"{query} hours"]
        else:
            suggestions = ["8 hours", "12 hours", "24 hours", "48 hours", "72 hours"]
        return suggestions

    @plugin_command(
        help="Set instant AFK time and trigger character selection screen.",
        params=[
            {"name": "hours", "type": int, "help": "Hours of AFK time (e.g. 8)"},
        ],
    )
    async def set_instant_afk_time(self, hours: int, injector=None, **kwargs):
        if hours <= 0:
            return "Hours must be greater than 0"
        
        if self.debug:
            console.print(f"[Instant AFK] Setting {hours} hours of AFK time")
        
        result = self.run_js_export('set_instant_afk_time_js', injector, hours=hours)
        return result

    @js_export(params=["hours"])
    def set_instant_afk_time_js(self, hours=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) {
                return "ERROR: Game engine not found";
            }
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const hours = arguments[0] || 8;
            const seconds = hours * 3600;
            
            console.log("[Instant AFK] Setting AFK time to", hours, "hours (", seconds, "seconds)");
            
            const timeAway = bEngine.getGameAttribute("TimeAway");
            if (timeAway && timeAway.h) {
                const currentTime = Date.now();
                const afkStartTime = currentTime - (seconds * 1000);
                
                timeAway.h.GlobalTime = afkStartTime;
                timeAway.h.Player = afkStartTime;
                
                bEngine.setGameAttribute("TimeAway", timeAway);
                console.log("[Instant AFK] TimeAway.GlobalTime set to:", afkStartTime);
                console.log("[Instant AFK] TimeAway.Player set to:", afkStartTime);
            }
            
            return `SUCCESS: AFK time set to ${hours} hours!`;
            
        } catch (e) {
            return `ERROR: ${e.message}`;
        }
        '''

plugin_class = InstantAfkTimePlugin 