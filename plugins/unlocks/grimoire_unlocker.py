from plugin_system import PluginBase, js_export, ui_toggle, ui_search_with_results, plugin_command, ui_autocomplete_input, console
from config_manager import config_manager

class GrimoireUnlockerPlugin(PluginBase):
    VERSION = "1.0.0"
    DESCRIPTION = "Unlock and manage grimoire upgrades for Death Bringer class."
    PLUGIN_ORDER = 2
    CATEGORY = "Unlocks"

    def __init__(self, config=None):
        super().__init__(config or {})        
        self.debug = config.get('debug', False) if config else False
        self.name = 'grimoire_unlocker'
        self._grimoire_cache = None
        self._cache_timestamp = 0
        self._cache_duration = 300

    async def cleanup(self): pass
    async def update(self): pass
    async def on_config_changed(self, config): 
        self.debug = config.get('debug', False)
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)
    async def on_game_ready(self): pass

    @ui_toggle(
        label="Debug Mode",
        description="Enable debug logging for grimoire unlocker plugin",
        config_key="debug",
        default_value=False
    )
    async def enable_debug(self, value: bool = None):
        if value is not None:
            self.config["debug"] = value
            self.save_to_global_config()
            self.debug = value
        return f"Debug mode {'enabled' if self.config.get('debug', False) else 'disabled'}"

    @ui_search_with_results(
        label="Grimoire Upgrades Status",
        description="Show all grimoire upgrades with their unlock status and levels",
        button_text="Show Grimoire Status",
        placeholder="Enter filter term (leave empty to show all)",
    )
    async def grimoire_status_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[grimoire_unlocker] Getting grimoire status, filter: {value}")
                result = self.run_js_export('get_grimoire_status_js', self.injector, filter_query=value or "")
                return result
            except Exception as e:
                if self.debug:
                    console.print(f"[grimoire_unlocker] Error getting grimoire status: {e}")
                return f"ERROR: Error getting grimoire status: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["filter_query"])
    def get_grimoire_status_js(self, filter_query=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const grimoire = bEngine.getGameAttribute("Grimoire");
            const grimoireUpg = bEngine.getGameAttribute("CustomLists").h.GrimoireUpg;
            
            if (!grimoire || !grimoireUpg) {
                return "Error: Grimoire data not found";
            }
            
            let output = "";
            output += "<div style='font-weight: bold; font-size: 16px; margin-bottom: 10px;'>📚 GRIMOIRE UPGRADES STATUS</div>";
            
            let total_upgrades = 0;
            let unlocked_upgrades = 0;
            let max_leveled_upgrades = 0;
            
            const locked = [];
            const unlocked = [];
            const max_leveled = [];
            
            for (let i = 0; i < grimoireUpg.length; i++) {
                const upgrade = grimoireUpg[i];
                if (!upgrade || !upgrade[0]) continue;
                
                total_upgrades++;
                const upgradeName = upgrade[0].replace(/_/g, ' ');
                const currentLevel = grimoire[i] || 0;
                const maxLevel = upgrade[4] || 0;
                const isUnlocked = currentLevel > 0;
                const isMaxLeveled = currentLevel >= maxLevel;
                
                if (isUnlocked) unlocked_upgrades++;
                if (isMaxLeveled) max_leveled_upgrades++;
                
                const item = {
                    name: upgradeName,
                    level: currentLevel,
                    maxLevel: maxLevel,
                    index: i
                };
                
                if (isMaxLeveled) {
                    max_leveled.push(item);
                } else if (isUnlocked) {
                    unlocked.push(item);
                } else {
                    locked.push(item);
                }
            }
            
            const filterQuery = filter_query ? filter_query.toLowerCase() : "";
            
            if (locked.length > 0) {
                const filteredLocked = locked.filter(item => !filterQuery || item.name.toLowerCase().includes(filterQuery));
                if (filteredLocked.length > 0) {
                    output += "<div style='color: #ff6b6b; font-weight: bold; margin: 10px 0 5px 0;'>🔒 LOCKED (" + filteredLocked.length + ")</div>";
                    for (const item of filteredLocked) {
                        output += "<div style='margin: 2px 0; padding: 3px 8px; background: rgba(255, 107, 107, 0.1); border-left: 3px solid #ff6b6b;'>" + item.name + " | Level: 0/" + item.maxLevel + "</div>";
                    }
                }
            }
            
            if (unlocked.length > 0) {
                const filteredUnlocked = unlocked.filter(item => !filterQuery || item.name.toLowerCase().includes(filterQuery));
                if (filteredUnlocked.length > 0) {
                    output += "<div style='color: #ffd93d; font-weight: bold; margin: 10px 0 5px 0;'>🟡 UNLOCKED (" + filteredUnlocked.length + ")</div>";
                    for (const item of filteredUnlocked) {
                        const progress = Math.round((item.level / item.maxLevel) * 100);
                        output += "<div style='margin: 2px 0; padding: 3px 8px; background: rgba(255, 217, 61, 0.1); border-left: 3px solid #ffd93d;'>" + item.name + " | Level: " + item.level + "/" + item.maxLevel + " (" + progress + "%)</div>";
                    }
                }
            }
            
            if (max_leveled.length > 0) {
                const filteredMaxLeveled = max_leveled.filter(item => !filterQuery || item.name.toLowerCase().includes(filterQuery));
                if (filteredMaxLeveled.length > 0) {
                    output += "<div style='color: #6bcf7f; font-weight: bold; margin: 10px 0 5px 0;'>🟢 MAX LEVEL (" + filteredMaxLeveled.length + ")</div>";
                    for (const item of filteredMaxLeveled) {
                        output += "<div style='margin: 2px 0; padding: 3px 8px; background: rgba(107, 207, 127, 0.1); border-left: 3px solid #6bcf7f;'>" + item.name + " | Level: " + item.level + "/" + item.maxLevel + "</div>";
                    }
                }
            }
            
            if (!filterQuery) {
                output += "<div style='margin-top: 15px; padding: 10px; background: rgba(0, 0, 0, 0.1); border-radius: 5px;'>";
                output += "<div style='font-weight: bold; margin-bottom: 5px;'>📊 SUMMARY</div>";
                output += "<div>Total Upgrades: " + total_upgrades + "</div>";
                output += "<div>Unlocked: " + unlocked_upgrades + "/" + total_upgrades + " (" + Math.round(unlocked_upgrades/total_upgrades*100) + "%)</div>";
                output += "<div>Max Leveled: " + max_leveled_upgrades + "/" + total_upgrades + " (" + Math.round(max_leveled_upgrades/total_upgrades*100) + "%)</div>";
                output += "</div>";
            }
            
            return output;
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @ui_autocomplete_input(
        label="Set Grimoire Upgrade Level",
        description="Set a specific grimoire upgrade to a specific level. Syntax: 'upgrade_name level' (e.g., 'Wraith Damage 100' or 'Wraith Accuracy 200')",
        button_text="Set Level",
        placeholder="Enter: upgrade_name level (e.g., 'Wraith Damage 100')",
    )
    async def set_grimoire_upgrade_level_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[grimoire_unlocker] Setting grimoire upgrade level, input: {value}")
                
                if not value or not value.strip():
                    return "Please provide upgrade name and level (e.g., 'Wraith Damage 100')"
                
                parts = value.strip().split()
                if len(parts) < 2:
                    return "Syntax: 'upgrade_name level' (e.g., 'Wraith Damage 100')"
                
                level_str = parts[-1]
                upgrade_name = ' '.join(parts[:-1])
                
                if self.debug:
                    console.print(f"[grimoire_unlocker] Parsed - upgrade_name: '{upgrade_name}', level: {level_str}")
                
                try:
                    level_int = int(level_str)
                    if level_int < 0:
                        return "Level must be 0 or higher"
                except ValueError:
                    return "Level must be a valid number"
                
                result = await self.set_grimoire_upgrade_level(upgrade_name, level_int)
                if self.debug:
                    console.print(f"[grimoire_unlocker] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[grimoire_unlocker] Error setting grimoire upgrade level: {e}")
                return f"ERROR: Error setting grimoire upgrade level: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    async def get_cached_grimoire_list(self):
        import time
        if (not hasattr(self, '_grimoire_cache') or 
            not hasattr(self, '_cache_timestamp') or 
            not hasattr(self, '_cache_duration') or
            time.time() - self._cache_timestamp > self._cache_duration):
            
            if self.debug:
                console.print("[grimoire_unlocker] Cache expired or missing, fetching grimoire list...")
            try:
                if not hasattr(self, 'injector') or not self.injector:
                    if self.debug:
                        console.print("[grimoire_unlocker] No injector available")
                    return []
                
                raw_result = self.run_js_export('get_grimoire_upgrade_names_js', self.injector)
                if self.debug:
                    console.print(f"[grimoire_unlocker] Raw JS result: {raw_result}")
                
                if not raw_result or raw_result.startswith("Error:"):
                    if self.debug:
                        console.print(f"[grimoire_unlocker] No valid result from JS: {raw_result}")
                    return []
                
                grimoire_upgrades = []
                lines = raw_result.strip().split('\n')
                if self.debug:
                    console.print(f"[grimoire_unlocker] Processing {len(lines)} lines")
                
                for line in lines:
                    line = line.strip()
                    if line and '|' in line:
                        parts = line.split('|')
                        if len(parts) >= 2:
                            name = parts[0].strip()
                            if name and name != "Upgrade":
                                grimoire_upgrades.append(name)
                                if self.debug:
                                    console.print(f"[grimoire_unlocker] Added grimoire upgrade: {name}")
                
                self._grimoire_cache = grimoire_upgrades
                self._cache_timestamp = time.time()
                self._cache_duration = 300
                if self.debug:
                    console.print(f"[grimoire_unlocker] Cached {len(grimoire_upgrades)} grimoire upgrades")
                return grimoire_upgrades
            except Exception as e:
                if self.debug:
                    console.print(f"[grimoire_unlocker] Error fetching grimoire list: {e}")
                return []
        else:
            if self.debug:
                console.print(f"[grimoire_unlocker] Using cached grimoire list ({len(self._grimoire_cache)} items)")
            return self._grimoire_cache

    async def get_set_grimoire_upgrade_level_ui_autocomplete(self, query: str = ""):
        if self.debug:
            console.print(f"[grimoire_unlocker] get_set_grimoire_upgrade_level_ui_autocomplete called with query: '{query}'")
        try:
            if not hasattr(self, 'injector') or not self.injector:
                if self.debug:
                    console.print("[grimoire_unlocker] No injector available for autocomplete")
                return []
            
            grimoire_upgrades = await self.get_cached_grimoire_list()
            if self.debug:
                console.print(f"[grimoire_unlocker] Got {len(grimoire_upgrades)} grimoire upgrades from cache")
            
            if not grimoire_upgrades:
                if self.debug:
                    console.print("[grimoire_unlocker] No grimoire upgrades found")
                return []
            
            query_lower = query.lower()
            suggestions = []
            
            for upgrade in grimoire_upgrades:
                if query_lower in upgrade.lower():
                    suggestions.append(upgrade)
                    if self.debug:
                        console.print(f"[grimoire_unlocker] Added suggestion: {upgrade}")
            
            if self.debug:
                console.print(f"[grimoire_unlocker] Returning {len(suggestions)} suggestions: {suggestions}")
            return suggestions[:10]
        except Exception as e:
            if self.debug:
                console.print(f"[grimoire_unlocker] Error in get_set_grimoire_upgrade_level_ui_autocomplete: {e}")
            return []

    @ui_toggle(
        label="Unlock All Grimoire Upgrades",
        description="Unlock all grimoire upgrades (sets level to 1, does not max level)",
        config_key="unlock_all_upgrades",
        default_value=False
    )
    async def unlock_all_grimoire_upgrades_ui(self, value: bool = None):
        if value is not None:
            self.config["unlock_all_upgrades"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector and value:
                try:
                    result = await self.unlock_all_grimoire_upgrades(self.injector)
                    return f"SUCCESS: {result}"
                except Exception as e:
                    return f"ERROR: Error unlocking grimoire upgrades: {str(e)}"
        return f"Unlock all grimoire upgrades {'enabled' if self.config.get('unlock_all_upgrades', False) else 'disabled'}"

    @ui_toggle(
        label="Max Level All Grimoire Upgrades",
        description="Set all grimoire upgrades to maximum level",
        config_key="max_level_all_upgrades",
        default_value=False
    )
    async def max_level_all_grimoire_upgrades_ui(self, value: bool = None):
        if value is not None:
            self.config["max_level_all_upgrades"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector and value:
                try:
                    result = await self.max_level_all_grimoire_upgrades(self.injector)
                    return f"SUCCESS: {result}"
                except Exception as e:
                    return f"ERROR: Error max leveling grimoire upgrades: {str(e)}"
        return f"Max level all grimoire upgrades {'enabled' if self.config.get('max_level_all_upgrades', False) else 'disabled'}"

    @ui_toggle(
        label="Reset All Grimoire Upgrades",
        description="Reset all grimoire upgrades to level 0",
        config_key="reset_all_upgrades",
        default_value=False
    )
    async def reset_all_grimoire_upgrades_ui(self, value: bool = None):
        if value is not None:
            self.config["reset_all_upgrades"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector and value:
                try:
                    result = await self.reset_all_grimoire_upgrades(self.injector)
                    return f"SUCCESS: {result}"
                except Exception as e:
                    return f"ERROR: Error resetting grimoire upgrades: {str(e)}"
        return f"Reset all grimoire upgrades {'enabled' if self.config.get('reset_all_upgrades', False) else 'disabled'}"

    @plugin_command(
        help="Get grimoire status showing all upgrades and their levels.",
        params=[],
    )
    async def get_grimoire_status(self, injector=None, **kwargs):
        result = self.run_js_export('get_grimoire_status_js', injector)
        return result

    @plugin_command(
        help="Set a specific grimoire upgrade to a specific level.",
        params=[
            {"name": "upgrade_name", "type": str, "help": "Name of the grimoire upgrade"},
            {"name": "level", "type": int, "help": "Level to set (0 or higher)"},
        ],
    )
    async def set_grimoire_upgrade_level(self, upgrade_name: str, level: int, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('set_grimoire_upgrade_level_js', self.injector, upgrade_name=upgrade_name, level=level)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["upgrade_name", "level"])
    def set_grimoire_upgrade_level_js(self, upgrade_name=None, level=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const grimoire = bEngine.getGameAttribute("Grimoire");
            const grimoireUpg = bEngine.getGameAttribute("CustomLists").h.GrimoireUpg;
            
            if (!grimoire || !grimoireUpg) {
                return "Error: Grimoire data not found";
            }
            
            if (!upgrade_name || level === undefined || level === null) {
                return "Error: Upgrade name and level are required";
            }
            
            if (level < 0) {
                return "Error: Level must be 0 or higher";
            }
            
            let found_index = -1;
            let found_name = "";
            const search_name = upgrade_name.toLowerCase().replace(/[^a-z0-9]/g, '');
            
            for (let i = 0; i < grimoireUpg.length; i++) {
                const upgrade = grimoireUpg[i];
                if (!upgrade || !upgrade[0]) continue;
                
                const upgradeName = upgrade[0].replace(/_/g, ' ');
                const clean_name = upgradeName.toLowerCase().replace(/[^a-z0-9]/g, '');
                
                if (clean_name.includes(search_name) || search_name.includes(clean_name)) {
                    found_index = i;
                    found_name = upgradeName;
                    break;
                }
            }
            
            if (found_index === -1) {
                return "Error: Grimoire upgrade '" + upgrade_name + "' not found";
            }
            
            const maxLevel = grimoireUpg[found_index][4] || 0;
            const oldLevel = grimoire[found_index] || 0;
            
            if (level > maxLevel) {
                return "Error: Level " + level + " exceeds maximum level " + maxLevel + " for '" + found_name + "'";
            }
            
            grimoire[found_index] = level;
            
            if (level === 0) {
                return "✅ Reset '" + found_name + "' to level 0 (was level " + oldLevel + ")";
            } else if (level === maxLevel) {
                return "🚀 Set '" + found_name + "' to maximum level " + maxLevel + " (was level " + oldLevel + ")";
            } else {
                return "📈 Set '" + found_name + "' to level " + level + " (was level " + oldLevel + ", max is " + maxLevel + ")";
            }
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @plugin_command(
        help="Get list of grimoire upgrade names for autocomplete.",
        params=[],
    )
    async def get_grimoire_upgrade_names(self, injector=None, **kwargs):
        result = self.run_js_export('get_grimoire_upgrade_names_js', injector)
        return result

    @js_export()
    def get_grimoire_upgrade_names_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const grimoire = bEngine.getGameAttribute("Grimoire");
            const grimoireUpg = bEngine.getGameAttribute("CustomLists").h.GrimoireUpg;
            
            if (!grimoire || !grimoireUpg) {
                return "Error: Grimoire data not found";
            }
            
            let output = "Upgrade | Level | Max Level | Status\\n";
            output += "---------|-------|-----------|--------\\n";
            
            for (let i = 0; i < grimoireUpg.length; i++) {
                const upgrade = grimoireUpg[i];
                if (!upgrade || !upgrade[0]) continue;
                
                const upgradeName = upgrade[0].replace(/_/g, ' ');
                const currentLevel = grimoire[i] || 0;
                const maxLevel = upgrade[4] || 0;
                const isUnlocked = currentLevel > 0;
                const isMaxLeveled = currentLevel >= maxLevel;
                
                let status = "🔒 LOCKED";
                if (isMaxLeveled) {
                    status = "🟢 MAX LEVEL";
                } else if (isUnlocked) {
                    status = "🟡 UNLOCKED";
                }
                
                output += upgradeName + " | " + currentLevel + " | " + maxLevel + " | " + status + "\\n";
            }
            
            return output;
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @plugin_command(
        help="Unlock all grimoire upgrades (sets level to 1, does not max level).",
        params=[],
    )
    async def unlock_all_grimoire_upgrades(self, injector=None, **kwargs):
        result = self.run_js_export('unlock_all_grimoire_upgrades_js', injector)
        return result

    @js_export()
    def unlock_all_grimoire_upgrades_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const grimoire = bEngine.getGameAttribute("Grimoire");
            const grimoireUpg = bEngine.getGameAttribute("CustomLists").h.GrimoireUpg;
            
            if (!grimoire || !grimoireUpg) {
                return "Error: Grimoire data not found";
            }
            
            let unlocked_count = 0;
            let already_unlocked = 0;
            
            for (let i = 0; i < grimoireUpg.length; i++) {
                const upgrade = grimoireUpg[i];
                if (!upgrade || !upgrade[0]) continue;
                
                const upgradeName = upgrade[0].replace(/_/g, ' ');
                const currentLevel = grimoire[i] || 0;
                
                if (currentLevel === 0) {
                    grimoire[i] = 1;
                    unlocked_count++;
                } else {
                    already_unlocked++;
                }
            }
            
            if (unlocked_count === 0) {
                return "✅ All grimoire upgrades are already unlocked! (" + already_unlocked + " upgrades)";
            } else {
                return "🔓 Unlocked " + unlocked_count + " grimoire upgrades! (" + already_unlocked + " were already unlocked)";
            }
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @plugin_command(
        help="Set all grimoire upgrades to maximum level.",
        params=[],
    )
    async def max_level_all_grimoire_upgrades(self, injector=None, **kwargs):
        result = self.run_js_export('max_level_all_grimoire_upgrades_js', injector)
        return result

    @js_export()
    def max_level_all_grimoire_upgrades_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const grimoire = bEngine.getGameAttribute("Grimoire");
            const grimoireUpg = bEngine.getGameAttribute("CustomLists").h.GrimoireUpg;
            
            if (!grimoire || !grimoireUpg) {
                return "Error: Grimoire data not found";
            }
            
            let max_leveled_count = 0;
            let already_max_leveled = 0;
            
            for (let i = 0; i < grimoireUpg.length; i++) {
                const upgrade = grimoireUpg[i];
                if (!upgrade || !upgrade[0]) continue;
                
                const upgradeName = upgrade[0].replace(/_/g, ' ');
                const currentLevel = grimoire[i] || 0;
                const maxLevel = upgrade[4] || 0;
                
                if (currentLevel < maxLevel) {
                    grimoire[i] = maxLevel;
                    max_leveled_count++;
                } else {
                    already_max_leveled++;
                }
            }
            
            if (max_leveled_count === 0) {
                return "✅ All grimoire upgrades are already at maximum level! (" + already_max_leveled + " upgrades)";
            } else {
                return "🚀 Set " + max_leveled_count + " grimoire upgrades to maximum level! (" + already_max_leveled + " were already max level)";
            }
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @plugin_command(
        help="Reset all grimoire upgrades to level 0.",
        params=[],
    )
    async def reset_all_grimoire_upgrades(self, injector=None, **kwargs):
        result = self.run_js_export('reset_all_grimoire_upgrades_js', injector)
        return result

    @js_export()
    def reset_all_grimoire_upgrades_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const grimoire = bEngine.getGameAttribute("Grimoire");
            const grimoireUpg = bEngine.getGameAttribute("CustomLists").h.GrimoireUpg;
            
            if (!grimoire || !grimoireUpg) {
                return "Error: Grimoire data not found";
            }
            
            let reset_count = 0;
            let already_reset = 0;
            
            for (let i = 0; i < grimoireUpg.length; i++) {
                const upgrade = grimoireUpg[i];
                if (!upgrade || !upgrade[0]) continue;
                
                const upgradeName = upgrade[0].replace(/_/g, ' ');
                const currentLevel = grimoire[i] || 0;
                
                if (currentLevel > 0) {
                    grimoire[i] = 0;
                    reset_count++;
                } else {
                    already_reset++;
                }
            }
            
            if (reset_count === 0) {
                return "✅ All grimoire upgrades are already reset! (" + already_reset + " upgrades)";
            } else {
                return "🔄 Reset " + reset_count + " grimoire upgrades to level 0! (" + already_reset + " were already reset)";
            }
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @ui_autocomplete_input(
        label="Set All Grimoire Upgrades to % of Max",
        description="Set all grimoire upgrades to a percentage of their maximum level (capped at 999999). Enter a number 0-100 for percentage.",
        button_text="Set Percentage",
        placeholder="Enter percentage (0-100, e.g., '50' for 50%)",
    )
    async def set_all_grimoire_upgrades_percentage_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[grimoire_unlocker] Setting grimoire upgrades to percentage, input: {value}")
                
                if not value or not value.strip():
                    return "Please provide a percentage value (0-100)"
                
                try:
                    percentage = float(value.strip())
                    if percentage < 0 or percentage > 100:
                        return "Percentage must be between 0 and 100"
                except ValueError:
                    return "Percentage must be a valid number"
                
                result = await self.set_all_grimoire_upgrades_percentage(percentage)
                if self.debug:
                    console.print(f"[grimoire_unlocker] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[grimoire_unlocker] Error setting grimoire upgrades percentage: {e}")
                return f"ERROR: Error setting grimoire upgrades percentage: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @plugin_command(
        help="Set all grimoire upgrades to a percentage of their maximum level (capped at 999999).",
        params=[
            {"name": "percentage", "type": float, "help": "Percentage of max level (0-100)"},
        ],
    )
    async def set_all_grimoire_upgrades_percentage(self, percentage: float, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('set_all_grimoire_upgrades_percentage_js', self.injector, percentage=percentage)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["percentage"])
    def set_all_grimoire_upgrades_percentage_js(self, percentage=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const grimoire = bEngine.getGameAttribute("Grimoire");
            const grimoireUpg = bEngine.getGameAttribute("CustomLists").h.GrimoireUpg;
            
            if (!grimoire || !grimoireUpg) {
                return "Error: Grimoire data not found";
            }
            
            if (percentage === undefined || percentage === null) {
                return "Error: Percentage is required";
            }
            
            if (percentage < 0 || percentage > 100) {
                return "Error: Percentage must be between 0 and 100";
            }
            
            const percentage_decimal = percentage / 100;
            const max_cap = 999999;
            
            let updated_count = 0;
            let unchanged_count = 0;
            let capped_upgrades = 0;
            let total_upgrades = 0;
            
            for (let i = 0; i < grimoireUpg.length; i++) {
                const upgrade = grimoireUpg[i];
                if (!upgrade || !upgrade[0]) continue;
                
                total_upgrades++;
                const upgradeName = upgrade[0].replace(/_/g, ' ');
                const currentLevel = grimoire[i] || 0;
                const maxLevel = upgrade[4] || 0;
                
                // Only process upgrades that are capped at 999999
                if (maxLevel === max_cap) {
                    capped_upgrades++;
                    const targetLevel = Math.floor(maxLevel * percentage_decimal);
                    
                    if (currentLevel !== targetLevel) {
                        grimoire[i] = targetLevel;
                        updated_count++;
                    } else {
                        unchanged_count++;
                    }
                }
            }
            
            if (capped_upgrades === 0) {
                return "❌ No grimoire upgrades found that are capped at " + max_cap + "!";
            } else if (updated_count === 0) {
                return "✅ All " + capped_upgrades + " grimoire upgrades capped at " + max_cap + " are already at " + percentage + "% of their maximum level!";
            } else {
                return "📊 Set " + updated_count + " grimoire upgrades (capped at " + max_cap + ") to " + percentage + "% of their maximum level! (" + unchanged_count + " were already at target level, " + capped_upgrades + " total capped upgrades)";
            }
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

plugin_class = GrimoireUnlockerPlugin 