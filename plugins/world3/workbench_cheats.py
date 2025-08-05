from plugin_system import PluginBase, js_export, ui_toggle, ui_search_with_results, plugin_command, ui_autocomplete_input, console
from config_manager import config_manager
from typing import Optional
import time

class WorkbenchCheatsPlugin(PluginBase):
    VERSION = "1.0.0"
    DESCRIPTION = "World 3 Workbench and Construction cheats with comprehensive status overview and toggles for all building features."
    PLUGIN_ORDER = 1
    CATEGORY = "World 3"

    def __init__(self, config=None):
        super().__init__(config or {})
        self.debug = config.get('debug', False) if config else False
        self._workbench_cache = None
        self._tower_cache = None
        self._cache_timestamp = 0
        self._cache_duration = 300
        self.name = 'workbench_cheats'

    async def cleanup(self): pass
    async def update(self): pass
    
    def update_js_config(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                return self.run_js_export('update_workbench_config_js', self.injector, config=self.config)
            except Exception as e:
                if self.debug:
                    console.print(f"[workbench_cheats] Error updating JS config: {e}")
                return False
        return False
    async def on_config_changed(self, config): 
        self.debug = config.get('debug', False)
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)
            try:
                if any(config.get(cheat, False) for cheat in ["free_buildings", "instant_build", "build_speed", "flag_requirements", "total_flags", "better_cogs", "multikill_bonus", "sample_size_bonus", "printer_slots", "const_mastery", "death_note_rank", "shrine_cheats", "damage_bonus", "exp_drop_bonus"]):
                    if not hasattr(self, '_workbench_setup'):
                        self.run_js_export('setup_workbench_cheats_js', self.injector)
                        self._workbench_setup = True
                    self.update_js_config()
            except Exception as e:
                if self.debug:
                    console.print(f"[workbench_cheats] Config change error: {e}")
    
    async def on_game_ready(self):
        if self.injector:
            try:
                config = config_manager.get_plugin_config(self.name)
                self.set_config(config)
                if any(config.get(cheat, False) for cheat in ["free_buildings", "instant_build", "build_speed", "flag_requirements", "total_flags", "better_cogs", "multikill_bonus", "sample_size_bonus", "printer_slots", "const_mastery", "death_note_rank", "shrine_cheats", "damage_bonus", "exp_drop_bonus"]):
                    self.run_js_export('setup_workbench_cheats_js', self.injector)
                    self._workbench_setup = True
                    self.update_js_config()
            except Exception as e:
                console.print(f"[workbench_cheats] Error setting up workbench cheats: {e}")

    @ui_toggle(
        label="Debug Mode",
        description="Enable debug logging for workbench cheats plugin",
        config_key="debug",
        default_value=False
    )
    async def enable_debug(self, value: Optional[bool] = None):
        if value is not None:
            self.config["debug"] = value
            self.save_to_global_config()
            self.debug = value
        return f"Debug mode {'enabled' if self.config.get('debug', False) else 'disabled'}"

    @ui_toggle(
        label="Free Tower Buildings",
        description="Nullify all tower upgrade costs (salt and materials)",
        config_key="free_buildings",
        default_value=False
    )
    async def toggle_free_buildings(self, value: Optional[bool] = None):
        if value is not None:
            self.config["free_buildings"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                try:
                    if not hasattr(self, '_workbench_setup'):
                        self.run_js_export('setup_workbench_cheats_js', self.injector)
                        self._workbench_setup = True
                    self.update_js_config()
                    return f"SUCCESS: Free tower buildings {'enabled' if value else 'disabled'}"
                except Exception as e:
                    return f"ERROR: {str(e)}"
        return f"Free tower buildings {'enabled' if self.config.get('free_buildings', False) else 'disabled'}"

    @ui_toggle(
        label="Instant Build",
        description="Instantly build/upgrade towers (no waiting time)",
        config_key="instant_build",
        default_value=False
    )
    async def toggle_instant_build(self, value: Optional[bool] = None):
        if value is not None:
            self.config["instant_build"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                try:
                    if not hasattr(self, '_workbench_setup'):
                        self.run_js_export('setup_workbench_cheats_js', self.injector)
                        self._workbench_setup = True
                    self.update_js_config()
                    return f"SUCCESS: Instant build {'enabled' if value else 'disabled'}"
                except Exception as e:
                    return f"ERROR: {str(e)}"
        return f"Instant build {'enabled' if self.config.get('instant_build', False) else 'disabled'}"

    @ui_toggle(
        label="Super Build Speed",
        description="Massively increase building speed (1,000,000x)",
        config_key="build_speed",
        default_value=False
    )
    async def toggle_build_speed(self, value: Optional[bool] = None):
        if value is not None:
            self.config["build_speed"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                try:
                    if not hasattr(self, '_workbench_setup'):
                        self.run_js_export('setup_workbench_cheats_js', self.injector)
                        self._workbench_setup = True
                    self.update_js_config()
                    return f"SUCCESS: Super build speed {'enabled' if value else 'disabled'}"
                except Exception as e:
                    return f"ERROR: {str(e)}"
        return f"Super build speed {'enabled' if self.config.get('build_speed', False) else 'disabled'}"

    @ui_toggle(
        label="Flag Requirements Nullified",
        description="Remove time requirements for flag unlocks",
        config_key="flag_requirements",
        default_value=False
    )
    async def toggle_flag_requirements(self, value: Optional[bool] = None):
        if value is not None:
            self.config["flag_requirements"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                try:
                    if not hasattr(self, '_workbench_setup'):
                        self.run_js_export('setup_workbench_cheats_js', self.injector)
                        self._workbench_setup = True
                    self.update_js_config()
                    return f"SUCCESS: Flag requirements {'nullified' if value else 'restored'}"
                except Exception as e:
                    return f"ERROR: {str(e)}"
        return f"Flag requirements nullification {'enabled' if self.config.get('flag_requirements', False) else 'disabled'}"

    @ui_toggle(
        label="Max Total Flags (10)",
        description="Set total placeable flags to 10",
        config_key="total_flags",
        default_value=False
    )
    async def toggle_total_flags(self, value: Optional[bool] = None):
        if value is not None:
            self.config["total_flags"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                try:
                    if not hasattr(self, '_workbench_setup'):
                        self.run_js_export('setup_workbench_cheats_js', self.injector)
                        self._workbench_setup = True
                    self.update_js_config()
                    return f"SUCCESS: Total flags {'set to 10' if value else 'restored to normal'}"
                except Exception as e:
                    return f"ERROR: {str(e)}"
        return f"Max total flags {'enabled' if self.config.get('total_flags', False) else 'disabled'}"

    @ui_toggle(
        label="Better Cogs",
        description="Improve cog drop rates and quality",
        config_key="better_cogs",
        default_value=False
    )
    async def toggle_better_cogs(self, value: Optional[bool] = None):
        if value is not None:
            self.config["better_cogs"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                try:
                    if not hasattr(self, '_workbench_setup'):
                        self.run_js_export('setup_workbench_cheats_js', self.injector)
                        self._workbench_setup = True
                    self.update_js_config()
                    return f"SUCCESS: Better cogs {'enabled' if value else 'disabled'}"
                except Exception as e:
                    return f"ERROR: {str(e)}"
        return f"Better cogs {'enabled' if self.config.get('better_cogs', False) else 'disabled'}"

    @ui_toggle(
        label="Super MultiKill",
        description="Massive multi-kill bonuses for damage and sampling",
        config_key="multikill_bonus",
        default_value=False
    )
    async def toggle_multikill_bonus(self, value: Optional[bool] = None):
        if value is not None:
            self.config["multikill_bonus"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                try:
                    if not hasattr(self, '_workbench_setup'):
                        self.run_js_export('setup_workbench_cheats_js', self.injector)
                        self._workbench_setup = True
                    self.update_js_config()
                    return f"SUCCESS: Super MultiKill {'enabled' if value else 'disabled'}"
                except Exception as e:
                    return f"ERROR: {str(e)}"
        return f"Super MultiKill {'enabled' if self.config.get('multikill_bonus', False) else 'disabled'}"

    @ui_toggle(
        label="Max Sample Size",
        description="Maximum sample size bonus for all sampling activities",
        config_key="sample_size_bonus",
        default_value=False
    )
    async def toggle_sample_size_bonus(self, value: Optional[bool] = None):
        if value is not None:
            self.config["sample_size_bonus"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                try:
                    if not hasattr(self, '_workbench_setup'):
                        self.run_js_export('setup_workbench_cheats_js', self.injector)
                        self._workbench_setup = True
                    self.update_js_config()
                    return f"SUCCESS: Max sample size {'enabled' if value else 'disabled'}"
                except Exception as e:
                    return f"ERROR: {str(e)}"
        return f"Max sample size {'enabled' if self.config.get('sample_size_bonus', False) else 'disabled'}"

    @ui_toggle(
        label="Infinite Printer Slots",
        description="Unlimited printer sample slots",
        config_key="printer_slots",
        default_value=False
    )
    async def toggle_printer_slots(self, value: Optional[bool] = None):
        if value is not None:
            self.config["printer_slots"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                try:
                    if not hasattr(self, '_workbench_setup'):
                        self.run_js_export('setup_workbench_cheats_js', self.injector)
                        self._workbench_setup = True
                    self.update_js_config()
                    return f"SUCCESS: Infinite printer slots {'enabled' if value else 'disabled'}"
                except Exception as e:
                    return f"ERROR: {str(e)}"
        return f"Infinite printer slots {'enabled' if self.config.get('printer_slots', False) else 'disabled'}"

    @ui_toggle(
        label="Max Construction Mastery",
        description="Maximum construction mastery bonuses",
        config_key="const_mastery",
        default_value=False
    )
    async def toggle_const_mastery(self, value: Optional[bool] = None):
        if value is not None:
            self.config["const_mastery"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                try:
                    if not hasattr(self, '_workbench_setup'):
                        self.run_js_export('setup_workbench_cheats_js', self.injector)
                        self._workbench_setup = True
                    self.update_js_config()
                    return f"SUCCESS: Max construction mastery {'enabled' if value else 'disabled'}"
                except Exception as e:
                    return f"ERROR: {str(e)}"
        return f"Max construction mastery {'enabled' if self.config.get('const_mastery', False) else 'disabled'}"

    @ui_toggle(
        label="Max Death Note Rank",
        description="Maximum death note ranking",
        config_key="death_note_rank",
        default_value=False
    )
    async def toggle_death_note_rank(self, value: Optional[bool] = None):
        if value is not None:
            self.config["death_note_rank"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                try:
                    if not hasattr(self, '_workbench_setup'):
                        self.run_js_export('setup_workbench_cheats_js', self.injector)
                        self._workbench_setup = True
                    self.update_js_config()
                    return f"SUCCESS: Max death note rank {'enabled' if value else 'disabled'}"
                except Exception as e:
                    return f"ERROR: {str(e)}"
        return f"Max death note rank {'enabled' if self.config.get('death_note_rank', False) else 'disabled'}"

    @ui_toggle(
        label="Instant Shrine Completion",
        description="Instant shrine experience and no hour requirements",
        config_key="shrine_cheats",
        default_value=False
    )
    async def toggle_shrine_cheats(self, value: Optional[bool] = None):
        if value is not None:
            self.config["shrine_cheats"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                try:
                    if not hasattr(self, '_workbench_setup'):
                        self.run_js_export('setup_workbench_cheats_js', self.injector)
                        self._workbench_setup = True
                    self.update_js_config()
                    return f"SUCCESS: Shrine cheats {'enabled' if value else 'disabled'}"
                except Exception as e:
                    return f"ERROR: {str(e)}"
        return f"Shrine cheats {'enabled' if self.config.get('shrine_cheats', False) else 'disabled'}"

    @ui_toggle(
        label="Super Damage Bonus",
        description="Massive additional damage bonuses",
        config_key="damage_bonus",
        default_value=False
    )
    async def toggle_damage_bonus(self, value: Optional[bool] = None):
        if value is not None:
            self.config["damage_bonus"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                try:
                    if not hasattr(self, '_workbench_setup'):
                        self.run_js_export('setup_workbench_cheats_js', self.injector)
                        self._workbench_setup = True
                    self.update_js_config()
                    return f"SUCCESS: Super damage bonus {'enabled' if value else 'disabled'}"
                except Exception as e:
                    return f"ERROR: {str(e)}"
        return f"Super damage bonus {'enabled' if self.config.get('damage_bonus', False) else 'disabled'}"

    @ui_toggle(
        label="Super EXP & Drop Rate",
        description="Massive experience and drop rate bonuses",
        config_key="exp_drop_bonus",
        default_value=False
    )
    async def toggle_exp_drop_bonus(self, value: Optional[bool] = None):
        if value is not None:
            self.config["exp_drop_bonus"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                try:
                    if not hasattr(self, '_workbench_setup'):
                        self.run_js_export('setup_workbench_cheats_js', self.injector)
                        self._workbench_setup = True
                    self.update_js_config()
                    return f"SUCCESS: Super EXP & drop rate {'enabled' if value else 'disabled'}"
                except Exception as e:
                    return f"ERROR: {str(e)}"
        return f"Super EXP & drop rate {'enabled' if self.config.get('exp_drop_bonus', False) else 'disabled'}"

    @ui_autocomplete_input(
        label="Cheat Values Configuration",
        description="Configure values for various cheats (format: <code>variableName number</code>, one per line)<br><br><strong>Available Cheats:</strong><br><br><strong>multikillBonus</strong> - Multi-kill bonus multiplier for damage and sampling<br><i>Higher values = more damage and better sampling</i><br><br><strong>sampleSizeBonus</strong> - Sample size bonus percentage for all sampling activities<br><i>Affects mining, chopping, fishing, etc.</i><br><br><strong>printerSlots</strong> - Number of printer sample slots available<br><i>More slots = more items printed simultaneously</i><br><br><strong>constMastery</strong> - Construction mastery bonus for building speed and efficiency<br><i>Improves construction-related activities</i><br><br><strong>deathNoteRank</strong> - Death note ranking level for monster kill tracking and bonuses<br><i>Higher ranks provide better monster tracking rewards</i><br><br><strong>shrineExpBonus</strong> - Shrine experience bonus multiplier<br><i>Higher values = faster shrine leveling</i><br><br><strong>shrineHrReq</strong> - Shrine hour requirements<br><i>0 = instant completion, higher values = longer wait times</i><br><br><strong>damageBonus</strong> - Additional damage bonus added to all attacks<br><i>Direct damage increase for combat</i><br><br><strong>expDropBonus</strong> - Experience and drop rate bonus multiplier<br><i>Higher values = faster leveling and better loot drops</i>",
        placeholder="Enter cheat values (e.g., multikillBonus 1000, sampleSizeBonus 50)",
        button_text="Update Values",
        category="Cheat Configuration",
        order=1
    )
    async def configure_cheat_values(self, value: Optional[str] = None):
        if value is not None:
            cleaned_value = value
            if " - " in value:
                cleaned_value = value.split(" - ")[0]
            self.config["cheat_values"] = cleaned_value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                try:
                    self.update_js_config()
                    return f"SUCCESS: Cheat values updated"
                except Exception as e:
                    return f"ERROR: {str(e)}"
        return f"Current cheat values: {self.config.get('cheat_values', 'Not configured')}"

    async def get_configure_cheat_values_autocomplete(self, query: str = ""):
        """Provide autocomplete suggestions for cheat values"""
        suggestions = [
            "multikillBonus 1000",
            "sampleSizeBonus 50", 
            "printerSlots 20",
            "constMastery 100",
            "deathNoteRank 50",
            "shrineExpBonus 10000",
            "shrineHrReq 0",
            "damageBonus 5000",
            "expDropBonus 5000"
        ]
        
        if query:
            query_lower = query.lower()
            filtered_suggestions = []
            for suggestion in suggestions:
                if query_lower in suggestion.lower():
                    filtered_suggestions.append(suggestion)
            return filtered_suggestions
        else:
            return suggestions

    @js_export()
    def setup_workbench_cheats_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx || !ctx["com.stencyl.Engine"]?.engine) {
                return "Error: Game context not available";
            }

            const events = function(num) { return ctx["scripts.ActorEvents_" + num]; };
            const actorEvents345 = events(345);
            
            if (!actorEvents345) {
                return "Error: ActorEvents_345 not found";
            }

            if (!window.__workbench_original__) {
                window.__workbench_original__ = actorEvents345._customBlock_WorkbenchStuff;
            }

            const getConfig = () => {
                return window.pluginConfigs?.workbench_cheats || {};
            };

            const parseCheatValues = (config) => {
                const cheatValues = {};
                if (config.cheat_values) {
                    const lines = config.cheat_values.split('\\n');
                    for (const line of lines) {
                        const cleanLine = line.split(' - ')[0].trim();
                        const parts = cleanLine.split(' ');
                        if (parts.length >= 2) {
                            const key = parts[0];
                            const value = parts[1];
                            cheatValues[key] = parseInt(value) || 0;
                        }
                    }
                }
                return cheatValues;
            };

            actorEvents345._customBlock_WorkbenchStuff = function(...argumentsList) {
                const t = argumentsList[0];
                const config = getConfig();
                const cheatValues = parseCheatValues(config);
                
                if (config.flag_requirements && t == "FlagReq") return 0;
                if (config.free_buildings && (t == "TowerSaltCost" || t == "TowerMatCost")) return 0;
                if (config.instant_build && t == "TowerBuildReq") return 0;
                if (config.total_flags && t == "TotalFlags") return 10;
                if (config.build_speed && t == "PlayerBuildSpd") return 1000000;
                if (config.better_cogs && t == "CogSlots") return 999;
                if (config.better_cogs && t == "CogBuildClaims") return Math.max(999, window.__workbench_original__.apply(this, argumentsList));
                if (config.multikill_bonus && t == "MultiKillTOTAL") return cheatValues.multikillBonus || 1000;
                if (config.sample_size_bonus && t == "SampleSizeBONUS") return cheatValues.sampleSizeBonus || 50;
                if (config.printer_slots && t == "PrinterSampleSlots") return cheatValues.printerSlots || 20;
                if (config.const_mastery && t == "ConstMasteryBonus") return cheatValues.constMastery || 100;
                if (config.death_note_rank && t == "DeathNoteRank") return cheatValues.deathNoteRank || 50;
                if (config.shrine_cheats && t == "ShrineExpBonus") return cheatValues.shrineExpBonus || 10000;
                if (config.shrine_cheats && t == "ShrineHrREQ") return cheatValues.shrineHrReq || 0;
                if (config.damage_bonus && t == "AdditionExtraDMG") return cheatValues.damageBonus || 5000;
                if (config.exp_drop_bonus && t == "AdditionExtraEXPnDR") return cheatValues.expDropBonus || 5000;
                
                return window.__workbench_original__.apply(this, argumentsList);
            };

            return "🔨 Workbench cheat system initialized!";
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export(params=['config'])
    def update_workbench_config_js(self, config=None):
        return '''
        try {
            if (!window.pluginConfigs) {
                window.pluginConfigs = {};
            }
            
            window.pluginConfigs.workbench_cheats = config || {};
            
            return "Config updated successfully";
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

plugin_class = WorkbenchCheatsPlugin
