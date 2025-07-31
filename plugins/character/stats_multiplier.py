from plugin_system import PluginBase, ui_toggle, ui_slider, plugin_command, js_export, console
from config_manager import config_manager

class StatsMultiplierPlugin(PluginBase):
    VERSION = "1.0.1"
    DESCRIPTION = "Multiplies various game stats by configurable amounts."
    PLUGIN_ORDER = 7
    CATEGORY = "Character"

    def __init__(self, config=None):
        super().__init__(config or {})
        self.injector = None
        self.name = 'stats_multiplier'
        self.enabled = self.config.get('enabled', False)
        self.debug = config_manager.get_path('plugin_configs.stats_multiplier.debug', False)

    async def cleanup(self):
        pass

    async def update(self):
        self.debug = config_manager.get_path('plugin_configs.stats_multiplier.debug', False)
        if hasattr(self, 'injector') and self.injector and self.enabled:
            try:
                self.run_js_export('stats_multiplier_js', self.injector, enabled=self.config.get('enabled', False))
            except Exception as e:
                if self.debug:
                    console.print(f"[stats_multiplier] Update error: {e}")

    async def on_config_changed(self, config):
        self.enabled = config.get('enabled', False)
        self.debug = config_manager.get_path('plugin_configs.stats_multiplier.debug', False)
        if self.debug:
            console.print(f"[stats_multiplier] Config changed: {config}")
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)
            try:
                self.run_js_export('stats_multiplier_js', self.injector, enabled=self.config.get('enabled', False))
            except Exception as e:
                if self.debug:
                    console.print(f"[stats_multiplier] Config change error: {e}")

    async def on_game_ready(self):
        if self.injector:
            try:
                self.set_config(config_manager.get_plugin_config(self.name))
                self.run_js_export('stats_multiplier_js', self.injector, enabled=self.config.get('enabled', False))
            except Exception as e:
                console.print(f"[stats_multiplier] Error setting up stats multiplier: {e}")

    @ui_toggle(
        label="Enable Stats Multiplier",
        description="Enable all stats multiplier features",
        config_key="enabled",
        default_value=False
    )
    async def enable_stats_multiplier_ui(self, value=None):
        if value is not None:
            self.config['enabled'] = value
            self.save_to_global_config()
            self.enabled = value
            if hasattr(self, 'injector') and self.injector:
                self.run_js_export('stats_multiplier_js', self.injector, enabled=value)
        return f"Stats Multiplier is {'enabled' if self.config.get('enabled', False) else 'disabled'}"

    @ui_toggle(
        label="Debug Mode",
        description="Enable debug logging for stats multiplier plugin",
        config_key="debug",
        default_value=False
    )
    async def enable_debug(self, value=None):
        if value is not None:
            self.config['debug'] = value
            self.save_to_global_config()
        return f"Debug mode {'enabled' if self.config.get('debug', False) else 'disabled'}"

    @ui_slider(
        label="Damage Multiplier",
        description="Multiplies damage by this amount (use reasonably!)",
        config_key="damage_multiplier",
        default_value=1.0,
        min_value=1.0,
        max_value=50.0,
        step=0.1,
    )
    async def damage_multiplier_ui(self, value=None):
        if value is not None:
            self.config['damage_multiplier'] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                self.run_js_export('stats_multiplier_js', self.injector, enabled=self.config.get('enabled', False))
        return f"Damage multiplier set to {self.config.get('damage_multiplier', 1.0)}x"

    @ui_slider(
        label="Efficiency Multiplier",
        description="Multiplies skill efficiency by this amount (use reasonably!)",
        config_key="efficiency_multiplier",
        default_value=1.0,
        min_value=1.0,
        max_value=50.0,
        step=0.1,
    )
    async def efficiency_multiplier_ui(self, value=None):
        if value is not None:
            self.config['efficiency_multiplier'] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                self.run_js_export('stats_multiplier_js', self.injector, enabled=self.config.get('enabled', False))
        return f"Efficiency multiplier set to {self.config.get('efficiency_multiplier', 1.0)}x"

    @ui_slider(
        label="AFK Rate Multiplier",
        description="Multiplies AFK gains by this amount (use reasonably!)",
        config_key="afk_multiplier",
        default_value=1.0,
        min_value=1.0,
        max_value=50.0,
        step=0.1,
    )
    async def afk_multiplier_ui(self, value=None):
        if value is not None:
            self.config['afk_multiplier'] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                self.run_js_export('stats_multiplier_js', self.injector, enabled=self.config.get('enabled', False))
        return f"AFK rate multiplier set to {self.config.get('afk_multiplier', 1.0)}x"

    @ui_slider(
        label="Drop Rate Multiplier",
        description="Multiplies drop rate by this amount (use reasonably!)",
        config_key="drop_multiplier",
        default_value=1.0,
        min_value=1.0,
        max_value=50.0,
        step=0.1,
    )
    async def drop_multiplier_ui(self, value=None):
        if value is not None:
            self.config['drop_multiplier'] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                self.run_js_export('stats_multiplier_js', self.injector, enabled=self.config.get('enabled', False))
        return f"Drop rate multiplier set to {self.config.get('drop_multiplier', 1.0)}x"

    @ui_slider(
        label="Monster Count Multiplier",
        description="Multiplies the number of monsters on the map by this amount",
        config_key="monster_multiplier",
        default_value=1.0,
        min_value=1.0,
        max_value=50.0,
        step=0.1,
    )
    async def monster_multiplier_ui(self, value=None):
        if value is not None:
            self.config['monster_multiplier'] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                self.run_js_export('stats_multiplier_js', self.injector, enabled=self.config.get('enabled', False))
        return f"Monster count multiplier set to {self.config.get('monster_multiplier', 1.0)}x"

    @ui_slider(
        label="Printer Multiplier",
        description="Multiplies sample print by this amount, overrides lab/god bonus",
        config_key="printer_multiplier",
        default_value=1.0,
        min_value=1.0,
        max_value=50.0,
        step=0.1,
    )
    async def printer_multiplier_ui(self, value=None):
        if value is not None:
            self.config['printer_multiplier'] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                self.run_js_export('stats_multiplier_js', self.injector, enabled=self.config.get('enabled', False))
        return f"Printer multiplier set to {self.config.get('printer_multiplier', 1.0)}x"

    @plugin_command(help="Set stats multiplier values")
    async def set_multipliers(self, injector=None, **kwargs):
        if not injector:
            return "ERROR: No injector available - run 'inject' first"
        
        return self.run_js_export('stats_multiplier_js', injector, enabled=self.config.get('enabled', False))

    @js_export(params=["enabled"])
    def stats_multiplier_js(self, enabled=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx) {
                return "Error: Game context not available";
            }
            
            const engine = ctx["com.stencyl.Engine"].engine;
            const behavior = ctx["com.stencyl.behavior.Script"];
            const events = function(num) { return ctx["scripts.ActorEvents_" + num]; };
            
            if (!engine || !behavior) {
                return "Error: Game engine not ready";
            }
            
            if (!window.__stats_multiplier_originals__) {
                window.__stats_multiplier_originals__ = {
                    DamageDealt: events(12)._customBlock_DamageDealed,
                    SkillStats: events(12)._customBlock_SkillStats,
                    SkillStats2: events(12)._customBlock_skillstats2,
                    AFKgainrates: events(124)._customBlock_AFKgainrates,
                    TotalStats: events(12)._customBlock_TotalStats,
                    getValueForScene: behavior.getValueForScene,
                    Workbench: events(345)._customBlock_Workbench
                };
            }
            
            if (window.pluginConfigs && window.pluginConfigs['stats_multiplier'] && window.pluginConfigs['stats_multiplier'].enabled) {
                const pluginConfig = window.pluginConfigs['stats_multiplier'];
                const originals = window.__stats_multiplier_originals__;
                
                if (originals.DamageDealt && pluginConfig.damage_multiplier > 1.0) {
                    events(12)._customBlock_DamageDealed = function(...argumentsList) {
                        return argumentsList[0] == "Max" 
                            ? originals.DamageDealt(...argumentsList) * pluginConfig.damage_multiplier
                            : originals.DamageDealt(...argumentsList);
                    };
                }
                
                if (originals.SkillStats && pluginConfig.efficiency_multiplier > 1.0) {
                    events(12)._customBlock_SkillStats = function(...argumentsList) {
                        const t = argumentsList[0];
                        if (t.includes("Efficiency")) {
                            return originals.SkillStats(...argumentsList) * pluginConfig.efficiency_multiplier;
                        }
                        return originals.SkillStats(...argumentsList);
                    };
                }
                
                if (originals.SkillStats2 && pluginConfig.efficiency_multiplier > 1.0) {
                    events(12)._customBlock_skillstats2 = function(...argumentsList) {
                        const t = argumentsList[0];
                        if (t.includes("Efficiency")) {
                            return originals.SkillStats2(...argumentsList) * pluginConfig.efficiency_multiplier;
                        }
                        return originals.SkillStats2(...argumentsList);
                    };
                }
                
                if (originals.AFKgainrates && pluginConfig.afk_multiplier > 1.0) {
                    events(124)._customBlock_AFKgainrates = function(...argumentsList) {
                        return originals.AFKgainrates(...argumentsList) * pluginConfig.afk_multiplier;
                    };
                }
                
                if (originals.TotalStats && pluginConfig.drop_multiplier > 1.0) {
                    events(12)._customBlock_TotalStats = function(...argumentsList) {
                        return originals.TotalStats(...argumentsList) * 
                            (argumentsList[0] == "Drop_Rarity" ? pluginConfig.drop_multiplier : 1);
                    };
                }
                
                if (originals.getValueForScene && pluginConfig.monster_multiplier > 1.0) {
                    behavior.getValueForScene = function(...argumentsList) {
                        if (argumentsList[1] === "_NumberOfEnemies") {
                            return originals.getValueForScene(...argumentsList) * pluginConfig.monster_multiplier;
                        }
                        return originals.getValueForScene(...argumentsList);
                    };
                }
                
                if (originals.Workbench && pluginConfig.printer_multiplier > 1.0) {
                    events(345)._customBlock_Workbench = function(...argumentsList) {
                        const t = argumentsList[0];
                        if (t == "ExtraPrinting") {
                            argumentsList[0] = "AdditionExtraPrinting";
                            return pluginConfig.printer_multiplier * originals.Workbench(...argumentsList);
                        }
                        return originals.Workbench(...argumentsList);
                    };
                }
                
                return `Stats multipliers applied: Damage(${pluginConfig.damage_multiplier}x), Efficiency(${pluginConfig.efficiency_multiplier}x), AFK(${pluginConfig.afk_multiplier}x), Drop(${pluginConfig.drop_multiplier}x), Monster(${pluginConfig.monster_multiplier}x), Printer(${pluginConfig.printer_multiplier}x)`;
            } else {
                const originals = window.__stats_multiplier_originals__;
                if (originals) {
                    if (originals.DamageDealt) events(12)._customBlock_DamageDealed = originals.DamageDealt;
                    if (originals.SkillStats) events(12)._customBlock_SkillStats = originals.SkillStats;
                    if (originals.SkillStats2) events(12)._customBlock_skillstats2 = originals.SkillStats2;
                    if (originals.AFKgainrates) events(124)._customBlock_AFKgainrates = originals.AFKgainrates;
                    if (originals.TotalStats) events(12)._customBlock_TotalStats = originals.TotalStats;
                    if (originals.getValueForScene) behavior.getValueForScene = originals.getValueForScene;
                    if (originals.Workbench) events(345)._customBlock_Workbench = originals.Workbench;
                }
                return "Stats multipliers disabled and original functions restored.";
            }
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

plugin_class = StatsMultiplierPlugin 