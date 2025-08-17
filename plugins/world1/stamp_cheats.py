from plugin_system import PluginBase, js_export, ui_toggle, ui_button, ui_search_with_results, plugin_command, ui_autocomplete_input, console, ui_banner
from config_manager import config_manager
import time

class StampCheatsPlugin(PluginBase):
    VERSION = "1.0.0"
    DESCRIPTION = "⚠️ Unlock and manage stamp upgrades & bribes. Includes stamp viewing, leveling, unlocking, and bribe purchasing tools. Use with caution as stamps and bribes affect multiple game systems! ⚠️"
    PLUGIN_ORDER = 2
    CATEGORY = "World 1"

    def __init__(self, config=None):
        super().__init__(config or {})        
        self.debug = config.get('debug', False) if config else False
        self.name = 'stamp_cheats'
        self._stamps_cache = None
        self._cache_timestamp = 0
        self._cache_duration = 300
        self._bribes_cache = None
        self._bribes_cache_timestamp = 0

    async def cleanup(self): pass
    async def update(self): pass
    async def on_config_changed(self, config): 
        self.debug = config.get('debug', False)
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)
    async def on_game_ready(self): pass

    @ui_toggle(
        label="Debug Mode",
        description="Enable debug logging for stamp and bribe cheats plugin",
        config_key="debug",
        default_value=False,
        category="Settings",
        order=-500
    )
    async def enable_debug(self, value: bool = None):
        if value is not None:
            self.config["debug"] = value
            self.save_to_global_config()
            self.debug = value
        return f"Debug mode {'enabled' if self.config.get('debug', False) else 'disabled'}"

    @ui_search_with_results(
        label="Stamps Status",
        description="Show all stamps with their current levels, max levels, and unlock status",
        button_text="Show Stamps",
        placeholder="Enter filter term (leave empty to show all)",
        category="Stamp Management",
        order=1
    )
    async def stamps_status_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[stamp_cheats] Getting stamps status, filter: {value}")
                result = self.run_js_export('get_stamps_status_js', self.injector, filter_query=value or "")
                return result
            except Exception as e:
                if self.debug:
                    console.print(f"[stamp_cheats] Error getting stamps status: {e}")
                return f"ERROR: Error getting stamps status: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_search_with_results(
        label="Bribes Status",
        description="Show all bribes with their names, costs, bonuses, and purchase status",
        button_text="Show Bribes",
        placeholder="Enter filter term (leave empty to show all)",
        category="Bribe Management",
        order=1
    )
    async def bribes_status_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[stamp_cheats] Getting bribes status, filter: {value}")
                result = self.run_js_export('get_bribes_status_js', self.injector, filter_query=value or "")
                return result
            except Exception as e:
                if self.debug:
                    console.print(f"[stamp_cheats] Error getting bribes status: {e}")
                return f"ERROR: Error getting bribes status: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["filter_query"])
    def get_stamps_status_js(self, filter_query=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const stampLevel = bEngine.getGameAttribute("StampLevel");
            const stampLevelMAX = bEngine.getGameAttribute("StampLevelMAX");
            const stampDescriptions = bEngine.getGameAttribute("CustomLists").h.StampDescriptions;
            const itemDefinitionsGET = bEngine.getGameAttribute("ItemDefinitionsGET");
            
            if (!stampLevel || !stampLevelMAX || !stampDescriptions || !itemDefinitionsGET) {
                return "Error: Stamp data not found";
            }
            
            function getStampName(category, index) {
                let itemKey = "";
                if (category === 0) itemKey = `StampA${index + 1}`;
                else if (category === 1) itemKey = `StampB${index + 1}`;
                else itemKey = `StampC${index + 1}`;
                
                if (itemDefinitionsGET.h[itemKey]) {
                    let displayName = itemDefinitionsGET.h[itemKey].h?.displayName || "";
                    return displayName.replace(/_/g, ' ').replace(/\\s+/g, ' ').trim();
                }
                
                const rawDesc = stampDescriptions[category][index] || "";
                return rawDesc.replace(/^\\+\\{([^}]+)\\}.*/, '$1').replace(/[_%]/g, ' ').replace(/\\s+/g, ' ').trim() || `Unknown Stamp ${index + 1}`;
            }
            
            function getStampEffect(category, index) {
                const rawDesc = stampDescriptions[category][index] || "";
                let effect = rawDesc;
                
                if (effect.startsWith('+{')) {
                    effect = effect.substring(2); // Remove '+{'
                    const closingBrace = effect.indexOf('}');
                    if (closingBrace !== -1) {
                        effect = effect.substring(0, closingBrace); // Get text before first '}'
                    }
                }
                
                effect = effect.replace(/_/g, ' ').replace(/\\s+/g, ' ').trim();
                
                return effect || "Unknown Effect";
            }
            
            let output = "";
            output += "<div style='font-weight: bold; font-size: 16px; margin-bottom: 10px;'>🏷️ STAMPS STATUS</div>";
            
            let total_stamps = 0;
            let unlocked_stamps = 0;
            let max_leveled_stamps = 0;
            
            const locked = [];
            const unlocked = [];
            const max_leveled = [];
            
            for (let category = 0; category < 3; category++) {
                if (!stampLevel[category] || !stampLevelMAX[category] || !stampDescriptions[category]) continue;
                
                const categoryName = category === 0 ? "Combat" : category === 1 ? "Skills" : "Misc";
                
                for (let i = 0; i < stampDescriptions[category].length; i++) {
                    if (!stampDescriptions[category][i]) continue;
                    
                    total_stamps++;
                    const stampName = getStampName(category, i);
                    const stampEffect = getStampEffect(category, i);
                    const currentLevel = stampLevel[category][i] || 0;
                    const maxLevel = stampLevelMAX[category][i] || 0;
                    const isUnlocked = maxLevel > 0;
                    const isMaxLeveled = isUnlocked && currentLevel >= maxLevel;
                    
                    if (isUnlocked) unlocked_stamps++;
                    if (isMaxLeveled) max_leveled_stamps++;
                    
                    const item = {
                        name: `[${categoryName}] ${stampName}`,
                        effect: stampEffect,
                        level: currentLevel,
                        maxLevel: maxLevel,
                        category: category,
                        index: i,
                        isUnlocked: isUnlocked
                    };
                    
                    if (isMaxLeveled) {
                        max_leveled.push(item);
                    } else if (isUnlocked) {
                        unlocked.push(item);
                    } else {
                        locked.push(item);
                    }
                }
            }
            
            const filterQuery = filter_query ? filter_query.toLowerCase() : "";
            
            if (locked.length > 0) {
                const filteredLocked = locked.filter(item => !filterQuery || 
                    item.name.toLowerCase().includes(filterQuery) || 
                    item.effect.toLowerCase().includes(filterQuery));
                if (filteredLocked.length > 0) {
                    output += "<div style='color: #ff6b6b; font-weight: bold; margin: 10px 0 5px 0;'>🔒 LOCKED/NOT FOUND (" + filteredLocked.length + ")</div>";
                    for (const item of filteredLocked) {
                        output += "<div style='margin: 2px 0; padding: 3px 8px; background: rgba(255, 107, 107, 0.1); border-left: 3px solid #ff6b6b;'>" + item.name + " | Effect: " + item.effect + " | Max: " + item.maxLevel + "</div>";
                    }
                }
            }
            
            if (unlocked.length > 0) {
                const filteredUnlocked = unlocked.filter(item => !filterQuery || 
                    item.name.toLowerCase().includes(filterQuery) || 
                    item.effect.toLowerCase().includes(filterQuery));
                if (filteredUnlocked.length > 0) {
                    output += "<div style='color: #ffd93d; font-weight: bold; margin: 10px 0 5px 0;'>🟡 UNLOCKED (" + filteredUnlocked.length + ")</div>";
                    for (const item of filteredUnlocked) {
                        const progress = Math.round((item.level / item.maxLevel) * 100);
                        output += "<div style='margin: 2px 0; padding: 3px 8px; background: rgba(255, 217, 61, 0.1); border-left: 3px solid #ffd93d;'>" + item.name + " | Effect: " + item.effect + " | Level: " + item.level + "/" + item.maxLevel + " (" + progress + "%)</div>";
                    }
                }
            }
            
            if (max_leveled.length > 0) {
                const filteredMaxLeveled = max_leveled.filter(item => !filterQuery || 
                    item.name.toLowerCase().includes(filterQuery) || 
                    item.effect.toLowerCase().includes(filterQuery));
                if (filteredMaxLeveled.length > 0) {
                    output += "<div style='color: #6bcf7f; font-weight: bold; margin: 10px 0 5px 0;'>🟢 MAX LEVEL (" + filteredMaxLeveled.length + ")</div>";
                    for (const item of filteredMaxLeveled) {
                        output += "<div style='margin: 2px 0; padding: 3px 8px; background: rgba(107, 207, 127, 0.1); border-left: 3px solid #6bcf7f;'>" + item.name + " | Effect: " + item.effect + " | Level: " + item.level + "/" + item.maxLevel + "</div>";
                    }
                }
            }
            
            if (!filterQuery) {
                output += "<div style='margin-top: 15px; padding: 10px; background: rgba(0, 0, 0, 0.1); border-radius: 5px;'>";
                output += "<div style='font-weight: bold; margin-bottom: 5px;'>📊 SUMMARY</div>";
                output += "<div>Total Stamps: " + total_stamps + "</div>";
                output += "<div>Unlocked: " + unlocked_stamps + "/" + total_stamps + " (" + Math.round(unlocked_stamps/total_stamps*100) + "%)</div>";
                output += "<div>Max Leveled: " + max_leveled_stamps + "/" + total_stamps + " (" + Math.round(max_leveled_stamps/total_stamps*100) + "%)</div>";
                output += "</div>";
            }
            
            return output;
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @ui_autocomplete_input(
        label="Set Stamp Level",
        description="Set a specific stamp to a specific level. Syntax: 'stamp_name level' (e.g., 'Sword Stamp 100' or 'Mining Efficiency 50')",
        button_text="Set Level",
        placeholder="Enter: stamp_name level (e.g., 'Sword Stamp 100')",
        category="Stamp Management",
        order=2
    )
    async def set_stamp_level_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[stamp_cheats] Setting stamp level, input: {value}")
                
                if not value or not value.strip():
                    return "Please provide stamp name and level (e.g., 'Sword Stamp 100')"
                
                parts = value.strip().split()
                if len(parts) < 2:
                    return "Syntax: 'stamp_name level' (e.g., 'Sword Stamp 100')"
                
                level_str = parts[-1]
                stamp_name = ' '.join(parts[:-1])
                
                if self.debug:
                    console.print(f"[stamp_cheats] Parsed - stamp_name: '{stamp_name}', level: {level_str}")
                
                try:
                    level_int = int(level_str)
                    if level_int < 0:
                        return "Level must be 0 or higher"
                except ValueError:
                    return "Level must be a valid number"
                
                result = await self.set_stamp_level(stamp_name, level_int)
                if self.debug:
                    console.print(f"[stamp_cheats] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[stamp_cheats] Error setting stamp level: {e}")
                return f"ERROR: Error setting stamp level: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_autocomplete_input(
        label="Unlock Individual Stamp",
        description="Unlock a specific stamp by name and set it to level 1. This will make the stamp discoverable with a default max level.",
        button_text="Unlock Stamp",
        placeholder="Enter stamp name (e.g., 'Sword Stamp' or 'Mining Efficiency')",
        category="Stamp Management",
        order=3
    )
    async def unlock_individual_stamp_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[stamp_cheats] Unlocking individual stamp: {value}")
                
                if not value or not value.strip():
                    return "Please provide stamp name (e.g., 'Sword Stamp')"
                
                stamp_name = value.strip()
                
                result = await self.unlock_individual_stamp(stamp_name)
                if self.debug:
                    console.print(f"[stamp_cheats] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[stamp_cheats] Error unlocking individual stamp: {e}")
                return f"ERROR: Error unlocking individual stamp: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    async def get_unlock_individual_stamp_ui_autocomplete(self, query: str = ""):
        return await self.get_set_stamp_level_ui_autocomplete(query)

    async def get_cached_stamps_list(self):
        if (not hasattr(self, '_stamps_cache') or 
            not hasattr(self, '_cache_timestamp') or 
            not hasattr(self, '_cache_duration') or
            time.time() - self._cache_timestamp > self._cache_duration):
            
            if self.debug:
                console.print("[stamp_cheats] Cache expired or missing, fetching stamps list...")
            try:
                if not hasattr(self, 'injector') or not self.injector:
                    if self.debug:
                        console.print("[stamp_cheats] No injector available")
                    return []
                
                raw_result = self.run_js_export('get_stamp_names_js', self.injector)
                if self.debug:
                    console.print(f"[stamp_cheats] Raw JS result: {raw_result}")
                
                if not raw_result or raw_result.startswith("Error:"):
                    if self.debug:
                        console.print(f"[stamp_cheats] No valid result from JS: {raw_result}")
                    return []
                
                stamps = []
                lines = raw_result.strip().split('\n')
                if self.debug:
                    console.print(f"[stamp_cheats] Processing {len(lines)} lines")
                
                for line in lines:
                    line = line.strip()
                    if line and '|' in line:
                        parts = line.split('|')
                        if len(parts) >= 1:
                            stamp_name = parts[0].strip()
                            stamps.append(stamp_name)
                
                self._stamps_cache = stamps
                self._cache_timestamp = time.time()
                self._cache_duration = 300
                if self.debug:
                    console.print(f"[stamp_cheats] Cached {len(stamps)} stamps")
                return stamps
            except Exception as e:
                if self.debug:
                    console.print(f"[stamp_cheats] Error fetching stamps list: {e}")
                return []
        else:
            if self.debug:
                console.print(f"[stamp_cheats] Using cached stamps list ({len(self._stamps_cache)} items)")
            return self._stamps_cache

    async def get_set_stamp_level_ui_autocomplete(self, query: str = ""):
        if self.debug:
            console.print(f"[stamp_cheats] get_set_stamp_level_ui_autocomplete called with query: '{query}'")
        try:
            if not hasattr(self, 'injector') or not self.injector:
                if self.debug:
                    console.print("[stamp_cheats] No injector available for autocomplete")
                return []
            
            stamps = await self.get_cached_stamps_list()
            if self.debug:
                console.print(f"[stamp_cheats] Got {len(stamps)} stamps from cache")
            
            if not stamps:
                if self.debug:
                    console.print("[stamp_cheats] No stamps found")
                return []
            
            query_lower = query.lower()
            suggestions = []
            
            for stamp in stamps:
                if query_lower in stamp.lower():
                    suggestions.append(stamp)
                    if self.debug:
                        console.print(f"[stamp_cheats] Added suggestion: {stamp}")
            
            if self.debug:
                console.print(f"[stamp_cheats] Returning {len(suggestions)} suggestions: {suggestions}")
            return suggestions[:10]
        except Exception as e:
            if self.debug:
                console.print(f"[stamp_cheats] Error in get_set_stamp_level_ui_autocomplete: {e}")
            return []

    @ui_button(
        label="🔓 Unlock All Missing Stamps",
        description="Discover/unlock all stamps that haven't been found yet (sets max level to default)",
        category="Quick Actions",
        order=1
    )
    async def unlock_missing_stamps_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print("[stamp_cheats] Unlocking missing stamps")
                result = await self.unlock_missing_stamps()
                if self.debug:
                    console.print(f"[stamp_cheats] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[stamp_cheats] Error unlocking missing stamps: {e}")
                return f"ERROR: Error unlocking missing stamps: {str(e)}"
        return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_button(
        label="📈 Max Level All Stamps",
        description="Set all unlocked stamps to their maximum level",
        category="Quick Actions",
        order=2
    )
    async def max_level_all_stamps_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print("[stamp_cheats] Maxing all stamps")
                result = await self.max_level_all_stamps()
                if self.debug:
                    console.print(f"[stamp_cheats] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[stamp_cheats] Error maxing all stamps: {e}")
                return f"ERROR: Error maxing all stamps: {str(e)}"
        return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_autocomplete_input(
        label="📊 Set All Stamps to % of Max",
        description="Set all unlocked stamps to a percentage of their maximum level (e.g., '50' for 50%, '75' for 75%)",
        button_text="Set Percentage",
        placeholder="Enter percentage (0-100, e.g., '50' for 50%)",
        category="Quick Actions",
        order=3
    )
    async def set_all_stamps_percentage_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[stamp_cheats] Setting all stamps to percentage: {value}")
                
                if not value or not value.strip():
                    return "Please provide a percentage (0-100, e.g., '50' for 50%)"
                
                percentage_str = value.strip()
                
                try:
                    percentage = float(percentage_str)
                    if percentage < 0 or percentage > 100:
                        return "Percentage must be between 0 and 100"
                except ValueError:
                    return "Percentage must be a valid number (0-100)"
                
                result = await self.set_all_stamps_percentage(percentage)
                if self.debug:
                    console.print(f"[stamp_cheats] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[stamp_cheats] Error setting stamps percentage: {e}")
                return f"ERROR: Error setting stamps percentage: {str(e)}"
        return "ERROR: No injector available - run 'inject' first to connect to the game"

    def get_autocomplete_suggestions_set_all_stamps_percentage_ui(self):
        """Provide autocomplete suggestions for common percentages"""
        return ["25", "50", "75", "80", "90", "95", "100"]

    @ui_button(
        label="🔄 Reset All Stamps",
        description="Reset all stamps to level 0 (keeps them unlocked)",
        category="Quick Actions",
        order=4
    )
    async def reset_all_stamps_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print("[stamp_cheats] Resetting all stamps")
                result = await self.reset_all_stamps()
                if self.debug:
                    console.print(f"[stamp_cheats] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[stamp_cheats] Error resetting all stamps: {e}")
                return f"ERROR: Error resetting all stamps: {str(e)}"
        return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_button(
        label="🚫 Remove All Stamps",
        description="⚠️ DANGER: Completely remove all stamps (sets max level to 0) - This will make them undiscovered!",
        category="Dangerous Actions",
        order=1
    )
    async def remove_all_stamps_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print("[stamp_cheats] Removing all stamps")
                result = await self.remove_all_stamps()
                if self.debug:
                    console.print(f"[stamp_cheats] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[stamp_cheats] Error removing all stamps: {e}")
                return f"ERROR: Error removing all stamps: {str(e)}"
        return "ERROR: No injector available - run 'inject' first to connect to the game"

    @plugin_command(
        help="Get stamps status showing all stamps and their levels.",
        params=[],
    )
    async def get_stamps_status(self, injector=None, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('get_stamps_status_js', self.injector)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @plugin_command(
        help="Set a specific stamp to a specific level.",
        params=[
            {"name": "stamp_name", "type": str, "help": "Name of the stamp"},
            {"name": "level", "type": int, "help": "Level to set (0 or higher)"},
        ],
    )
    async def set_stamp_level(self, stamp_name: str, level: int, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('set_stamp_level_js', self.injector, stamp_name=stamp_name, level=level)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @plugin_command(
        help="Unlock all missing stamps (sets max level to default values).",
        params=[],
    )
    async def unlock_missing_stamps(self, injector=None, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('unlock_missing_stamps_js', self.injector)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @plugin_command(
        help="Unlock a specific stamp by name and set it to level 1.",
        params=[
            {"name": "stamp_name", "type": str, "help": "Name of the stamp to unlock"},
        ],
    )
    async def unlock_individual_stamp(self, stamp_name: str, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('unlock_individual_stamp_js', self.injector, stamp_name=stamp_name)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @plugin_command(
        help="Set all stamps to maximum level.",
        params=[],
    )
    async def max_level_all_stamps(self, injector=None, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('max_level_all_stamps_js', self.injector)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @plugin_command(
        help="Set all unlocked stamps to a percentage of their maximum level.",
        params=[
            {"name": "percentage", "type": float, "help": "Percentage of max level to set (0-100)"},
        ],
    )
    async def set_all_stamps_percentage(self, percentage: float, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            if percentage < 0 or percentage > 100:
                return "ERROR: Percentage must be between 0 and 100"
            result = self.run_js_export('set_all_stamps_percentage_js', self.injector, percentage=percentage)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @plugin_command(
        help="Reset all stamps to level 0.",
        params=[],
    )
    async def reset_all_stamps(self, injector=None, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('reset_all_stamps_js', self.injector)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @plugin_command(
        help="Remove all stamps (sets max level to 0).",
        params=[],
    )
    async def remove_all_stamps(self, injector=None, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('remove_all_stamps_js', self.injector)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @plugin_command(
        help="Get list of stamp names for autocomplete.",
        params=[],
    )
    async def get_stamp_names(self, injector=None, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('get_stamp_names_js', self.injector)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["stamp_name", "level"])
    def set_stamp_level_js(self, stamp_name=None, level=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const stampLevel = bEngine.getGameAttribute("StampLevel");
            const stampLevelMAX = bEngine.getGameAttribute("StampLevelMAX");
            const stampDescriptions = bEngine.getGameAttribute("CustomLists").h.StampDescriptions;
            const itemDefinitionsGET = bEngine.getGameAttribute("ItemDefinitionsGET");
            
            if (!stampLevel || !stampLevelMAX || !stampDescriptions || !itemDefinitionsGET) {
                return "Error: Stamp data not found";
            }
            
            if (!stamp_name || level === undefined || level === null) {
                return "Error: Stamp name and level are required";
            }
            
            if (level < 0) {
                return "Error: Level must be 0 or higher";
            }
            
            function getStampName(category, index) {
                let itemKey = "";
                if (category === 0) itemKey = `StampA${index + 1}`;
                else if (category === 1) itemKey = `StampB${index + 1}`;
                else itemKey = `StampC${index + 1}`;
                
                if (itemDefinitionsGET.h[itemKey]) {
                    let displayName = itemDefinitionsGET.h[itemKey].h?.displayName || "";
                    return displayName.replace(/_/g, ' ').replace(/\\s+/g, ' ').trim();
                }
                
                const rawDesc = stampDescriptions[category][index] || "";
                return rawDesc.replace(/^\\+\\{([^}]+)\\}.*/, '$1').replace(/[_%]/g, ' ').replace(/\\s+/g, ' ').trim() || `Unknown Stamp ${index + 1}`;
            }
            
            let found_category = -1;
            let found_index = -1;
            let found_name = "";
            const search_name = stamp_name.toLowerCase().replace(/[^a-z0-9]/g, '');
            
            for (let category = 0; category < 3; category++) {
                if (!stampDescriptions[category]) continue;
                
                for (let i = 0; i < stampDescriptions[category].length; i++) {
                    if (!stampDescriptions[category][i]) continue;
                    
                    const cleanStampName = getStampName(category, i);
                    const clean_name = cleanStampName.toLowerCase().replace(/[^a-z0-9]/g, '');
                    
                    if (clean_name.includes(search_name) || search_name.includes(clean_name)) {
                        found_category = category;
                        found_index = i;
                        found_name = cleanStampName;
                        break;
                    }
                }
                if (found_category !== -1) break;
            }
            
            if (found_category === -1 || found_index === -1) {
                return "Error: Stamp '" + stamp_name + "' not found";
            }
            
            let maxLevel = stampLevelMAX[found_category][found_index] || 0;
            if (maxLevel === 0) {
                let defaultMaxLevel = 100;
                if (found_category === 0) defaultMaxLevel = 150; // Combat stamps
                else if (found_category === 1) defaultMaxLevel = 200; // Skill stamps
                else defaultMaxLevel = 100; // Misc stamps
                
                stampLevelMAX[found_category][found_index] = defaultMaxLevel;
                maxLevel = defaultMaxLevel; // Update maxLevel for subsequent checks
                
                const finalLevel = Math.min(level, defaultMaxLevel);
                stampLevel[found_category][found_index] = finalLevel;
                
                const categoryName = found_category === 0 ? "Combat" : found_category === 1 ? "Skills" : "Misc";
                
                if (finalLevel !== level) {
                    return "🔓✅ Auto-unlocked '" + found_name + "' [" + categoryName + "] (max level " + defaultMaxLevel + ") and set to level " + finalLevel + " (requested " + level + " was capped to max)";
                } else {
                    return "🔓✅ Auto-unlocked '" + found_name + "' [" + categoryName + "] (max level " + defaultMaxLevel + ") and set to level " + finalLevel;
                }
            }
            
            const oldLevel = stampLevel[found_category][found_index] || 0;
            
            if (level > maxLevel) {
                return "Error: Level " + level + " exceeds maximum level " + maxLevel + " for '" + found_name + "'";
            }
            
            stampLevel[found_category][found_index] = level;
            
            const categoryName = found_category === 0 ? "Combat" : found_category === 1 ? "Skills" : "Misc";
            
            if (level === 0) {
                return "✅ Reset '" + found_name + "' [" + categoryName + "] to level 0 (was level " + oldLevel + ")";
            } else if (level === maxLevel) {
                return "🚀 Set '" + found_name + "' [" + categoryName + "] to maximum level " + maxLevel + " (was level " + oldLevel + ")";
            } else {
                return "📈 Set '" + found_name + "' [" + categoryName + "] to level " + level + " (was level " + oldLevel + ", max is " + maxLevel + ")";
            }
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @js_export()
    def get_stamp_names_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const stampLevel = bEngine.getGameAttribute("StampLevel");
            const stampLevelMAX = bEngine.getGameAttribute("StampLevelMAX");
            const stampDescriptions = bEngine.getGameAttribute("CustomLists").h.StampDescriptions;
            const itemDefinitionsGET = bEngine.getGameAttribute("ItemDefinitionsGET");
            
            if (!stampLevel || !stampLevelMAX || !stampDescriptions || !itemDefinitionsGET) {
                return "Error: Stamp data not found";
            }
            
            function getStampName(category, index) {
                let itemKey = "";
                if (category === 0) itemKey = `StampA${index + 1}`;
                else if (category === 1) itemKey = `StampB${index + 1}`;
                else itemKey = `StampC${index + 1}`;
                
                if (itemDefinitionsGET.h[itemKey]) {
                    let displayName = itemDefinitionsGET.h[itemKey].h?.displayName || "";
                    return displayName.replace(/_/g, ' ').replace(/\\s+/g, ' ').trim();
                }
                
                const rawDesc = stampDescriptions[category][index] || "";
                return rawDesc.replace(/^\\+\\{([^}]+)\\}.*/, '$1').replace(/[_%]/g, ' ').replace(/\\s+/g, ' ').trim() || `Unknown Stamp ${index + 1}`;
            }
            
            let output = "Stamp | Category | Level | Max Level | Status\\n";
            output += "------|----------|-------|-----------|--------\\n";
            
            for (let category = 0; category < 3; category++) {
                if (!stampDescriptions[category]) continue;
                
                const categoryName = category === 0 ? "Combat" : category === 1 ? "Skills" : "Misc";
                
                for (let i = 0; i < stampDescriptions[category].length; i++) {
                    if (!stampDescriptions[category][i]) continue;
                    
                    const stampName = getStampName(category, i);
                    const currentLevel = stampLevel[category][i] || 0;
                    const maxLevel = stampLevelMAX[category][i] || 0;
                    const isUnlocked = maxLevel > 0;
                    const isMaxLeveled = isUnlocked && currentLevel >= maxLevel;
                    
                    let status = "🔒 LOCKED";
                    if (!isUnlocked) {
                        status = "🔒 NOT FOUND";
                    } else if (isMaxLeveled) {
                        status = "🟢 MAX LEVEL";
                    } else if (currentLevel > 0) {
                        status = "🟡 UNLOCKED";
                    } else {
                        status = "🔵 UNLOCKED (Level 0)";
                    }
                    
                    output += stampName + " | " + categoryName + " | " + currentLevel + " | " + maxLevel + " | " + status + "\\n";
                }
            }
            
            return output;
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @js_export(params=["stamp_name"])
    def unlock_individual_stamp_js(self, stamp_name=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const stampLevel = bEngine.getGameAttribute("StampLevel");
            const stampLevelMAX = bEngine.getGameAttribute("StampLevelMAX");
            const stampDescriptions = bEngine.getGameAttribute("CustomLists").h.StampDescriptions;
            const itemDefinitionsGET = bEngine.getGameAttribute("ItemDefinitionsGET");
            
            if (!stampLevel || !stampLevelMAX || !stampDescriptions || !itemDefinitionsGET) {
                return "Error: Stamp data not found";
            }
            
            if (!stamp_name) {
                return "Error: Stamp name is required";
            }
            
            function getStampName(category, index) {
                let itemKey = "";
                if (category === 0) itemKey = `StampA${index + 1}`;
                else if (category === 1) itemKey = `StampB${index + 1}`;
                else itemKey = `StampC${index + 1}`;
                
                if (itemDefinitionsGET.h[itemKey]) {
                    let displayName = itemDefinitionsGET.h[itemKey].h?.displayName || "";
                    return displayName.replace(/_/g, ' ').replace(/\\s+/g, ' ').trim();
                }
                
                const rawDesc = stampDescriptions[category][index] || "";
                return rawDesc.replace(/^\\+\\{([^}]+)\\}.*/, '$1').replace(/[_%]/g, ' ').replace(/\\s+/g, ' ').trim() || `Unknown Stamp ${index + 1}`;
            }
            
            let found_category = -1;
            let found_index = -1;
            let found_name = "";
            const search_name = stamp_name.toLowerCase().replace(/[^a-z0-9]/g, '');
            
            for (let category = 0; category < 3; category++) {
                if (!stampDescriptions[category]) continue;
                
                for (let i = 0; i < stampDescriptions[category].length; i++) {
                    if (!stampDescriptions[category][i]) continue;
                    
                    const cleanStampName = getStampName(category, i);
                    const clean_name = cleanStampName.toLowerCase().replace(/[^a-z0-9]/g, '');
                    
                    if (clean_name.includes(search_name) || search_name.includes(clean_name)) {
                        found_category = category;
                        found_index = i;
                        found_name = cleanStampName;
                        break;
                    }
                }
                if (found_category !== -1) break;
            }
            
            if (found_category === -1 || found_index === -1) {
                return "Error: Stamp '" + stamp_name + "' not found";
            }
            
            const currentMaxLevel = stampLevelMAX[found_category][found_index] || 0;
            if (currentMaxLevel > 0) {
                const categoryName = found_category === 0 ? "Combat" : found_category === 1 ? "Skills" : "Misc";
                const currentLevel = stampLevel[found_category][found_index] || 0;
                return "✅ Stamp '" + found_name + "' [" + categoryName + "] is already unlocked! (Level: " + currentLevel + "/" + currentMaxLevel + ")";
            }
            
            let defaultMaxLevel = 100;
            if (found_category === 0) defaultMaxLevel = 150; // Combat stamps
            else if (found_category === 1) defaultMaxLevel = 200; // Skill stamps
            else defaultMaxLevel = 100; // Misc stamps
            
            stampLevelMAX[found_category][found_index] = defaultMaxLevel;
            stampLevel[found_category][found_index] = 1;
            
            const categoryName = found_category === 0 ? "Combat" : found_category === 1 ? "Skills" : "Misc";
            
            return "🔓 Unlocked '" + found_name + "' [" + categoryName + "] with max level " + defaultMaxLevel + " and set to level 1!";
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @js_export()
    def unlock_missing_stamps_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const stampLevel = bEngine.getGameAttribute("StampLevel");
            const stampLevelMAX = bEngine.getGameAttribute("StampLevelMAX");
            const stampDescriptions = bEngine.getGameAttribute("CustomLists").h.StampDescriptions;
            
            if (!stampLevel || !stampLevelMAX || !stampDescriptions) {
                return "Error: Stamp data not found";
            }
            
            let unlocked_count = 0;
            let already_unlocked = 0;
            
            for (let category = 0; category < 3; category++) {
                if (!stampDescriptions[category]) continue;
                
                for (let i = 0; i < stampDescriptions[category].length; i++) {
                    if (!stampDescriptions[category][i]) continue;
                    
                    const currentMaxLevel = stampLevelMAX[category][i] || 0;
                    
                    if (currentMaxLevel === 0) {
                        let defaultMaxLevel = 100;
                        if (category === 0) defaultMaxLevel = 150; // Combat stamps
                        else if (category === 1) defaultMaxLevel = 200; // Skill stamps
                        else defaultMaxLevel = 100; // Misc stamps
                        
                        stampLevelMAX[category][i] = defaultMaxLevel;
                        if (!stampLevel[category][i]) stampLevel[category][i] = 0;
                        unlocked_count++;
                    } else {
                        already_unlocked++;
                    }
                }
            }
            
            if (unlocked_count === 0) {
                return "✅ All stamps are already unlocked! (" + already_unlocked + " stamps)";
            } else {
                return "🔓 Unlocked " + unlocked_count + " missing stamps! (" + already_unlocked + " were already unlocked)";
            }
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @js_export()
    def max_level_all_stamps_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const stampLevel = bEngine.getGameAttribute("StampLevel");
            const stampLevelMAX = bEngine.getGameAttribute("StampLevelMAX");
            const stampDescriptions = bEngine.getGameAttribute("CustomLists").h.StampDescriptions;
            
            if (!stampLevel || !stampLevelMAX || !stampDescriptions) {
                return "Error: Stamp data not found";
            }
            
            let max_leveled_count = 0;
            let already_max_leveled = 0;
            let not_unlocked_count = 0;
            
            for (let category = 0; category < 3; category++) {
                if (!stampDescriptions[category]) continue;
                
                for (let i = 0; i < stampDescriptions[category].length; i++) {
                    if (!stampDescriptions[category][i]) continue;
                    
                    const currentLevel = stampLevel[category][i] || 0;
                    const maxLevel = stampLevelMAX[category][i] || 0;
                    
                    if (maxLevel === 0) {
                        not_unlocked_count++;
                        continue;
                    }
                    
                    if (currentLevel < maxLevel) {
                        stampLevel[category][i] = maxLevel;
                        max_leveled_count++;
                    } else {
                        already_max_leveled++;
                    }
                }
            }
            
            let result = "";
            if (max_leveled_count === 0) {
                result = "✅ All unlocked stamps are already at maximum level! (" + already_max_leveled + " stamps)";
            } else {
                result = "🚀 Set " + max_leveled_count + " stamps to maximum level! (" + already_max_leveled + " were already max level)";
            }
            
            if (not_unlocked_count > 0) {
                result += " [" + not_unlocked_count + " stamps not unlocked - use 'Unlock Missing Stamps' first]";
            }
            
            return result;
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @js_export(params=["percentage"])
    def set_all_stamps_percentage_js(self, percentage=None):
        return f'''
        try {{
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const stampLevel = bEngine.getGameAttribute("StampLevel");
            const stampLevelMAX = bEngine.getGameAttribute("StampLevelMAX");
            const stampDescriptions = bEngine.getGameAttribute("CustomLists").h.StampDescriptions;
            
            if (!stampLevel || !stampLevelMAX || !stampDescriptions) {{
                return "Error: Stamp data not found";
            }}
            
            const targetPercentage = percentage;
            if (targetPercentage < 0 || targetPercentage > 100) {{
                return "Error: Percentage must be between 0 and 100";
            }}
            
            let updated_count = 0;
            let already_at_target = 0;
            let not_unlocked_count = 0;
            
            for (let category = 0; category < 3; category++) {{
                if (!stampDescriptions[category]) continue;
                
                for (let i = 0; i < stampDescriptions[category].length; i++) {{
                    if (!stampDescriptions[category][i]) continue;
                    
                    const currentLevel = stampLevel[category][i] || 0;
                    const maxLevel = stampLevelMAX[category][i] || 0;
                    
                    if (maxLevel === 0) {{
                        not_unlocked_count++;
                        continue;
                    }}
                    
                    const targetLevel = Math.floor((targetPercentage / 100) * maxLevel);
                    
                    if (currentLevel !== targetLevel) {{
                        stampLevel[category][i] = targetLevel;
                        updated_count++;
                    }} else {{
                        already_at_target++;
                    }}
                }}
            }}
            
            let result = "";
            if (updated_count === 0) {{
                result = "✅ All unlocked stamps are already at " + targetPercentage + "% of their maximum level! (" + already_at_target + " stamps)";
            }} else {{
                result = "📊 Set " + updated_count + " stamps to " + targetPercentage + "% of their maximum level! (" + already_at_target + " were already at target)";
            }}
            
            if (not_unlocked_count > 0) {{
                result += " [" + not_unlocked_count + " stamps not unlocked - use 'Unlock Missing Stamps' first]";
            }}
            
            return result;
        }} catch (e) {{
            return "Error: " + e.message;
        }}
        '''

    @js_export()
    def reset_all_stamps_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const stampLevel = bEngine.getGameAttribute("StampLevel");
            const stampLevelMAX = bEngine.getGameAttribute("StampLevelMAX");
            const stampDescriptions = bEngine.getGameAttribute("CustomLists").h.StampDescriptions;
            
            if (!stampLevel || !stampLevelMAX || !stampDescriptions) {
                return "Error: Stamp data not found";
            }
            
            let reset_count = 0;
            let already_reset = 0;
            let not_unlocked_count = 0;
            
            for (let category = 0; category < 3; category++) {
                if (!stampDescriptions[category]) continue;
                
                for (let i = 0; i < stampDescriptions[category].length; i++) {
                    if (!stampDescriptions[category][i]) continue;
                    
                    const currentLevel = stampLevel[category][i] || 0;
                    const maxLevel = stampLevelMAX[category][i] || 0;
                    
                    if (maxLevel === 0) {
                        not_unlocked_count++;
                        continue;
                    }
                    
                    if (currentLevel > 0) {
                        stampLevel[category][i] = 0;
                        reset_count++;
                    } else {
                        already_reset++;
                    }
                }
            }
            
            let result = "";
            if (reset_count === 0) {
                result = "✅ All unlocked stamps are already reset! (" + already_reset + " stamps)";
            } else {
                result = "🔄 Reset " + reset_count + " stamps to level 0! (" + already_reset + " were already reset)";
            }
            
            if (not_unlocked_count > 0) {
                result += " [" + not_unlocked_count + " stamps not unlocked]";
            }
            
            return result;
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @js_export()
    def remove_all_stamps_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const stampLevel = bEngine.getGameAttribute("StampLevel");
            const stampLevelMAX = bEngine.getGameAttribute("StampLevelMAX");
            const stampDescriptions = bEngine.getGameAttribute("CustomLists").h.StampDescriptions;
            
            if (!stampLevel || !stampLevelMAX || !stampDescriptions) {
                return "Error: Stamp data not found";
            }
            
            let removed_count = 0;
            let already_removed = 0;
            
            for (let category = 0; category < 3; category++) {
                if (!stampDescriptions[category]) continue;
                
                for (let i = 0; i < stampDescriptions[category].length; i++) {
                    if (!stampDescriptions[category][i]) continue;
                    
                    const currentLevel = stampLevel[category][i] || 0;
                    const maxLevel = stampLevelMAX[category][i] || 0;
                    
                    if (maxLevel > 0 || currentLevel > 0) {
                        stampLevel[category][i] = 0;
                        stampLevelMAX[category][i] = 0;
                        removed_count++;
                    } else {
                        already_removed++;
                    }
                }
            }
            
            if (removed_count === 0) {
                return "✅ All stamps are already removed! (" + already_removed + " stamps)";
            } else {
                return "🚫 Removed " + removed_count + " stamps completely! (" + already_removed + " were already removed) - They will need to be found again.";
            }
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @js_export(params=["filter_query"])
    def get_bribes_status_js(self, filter_query=None):
        return f'''
        try {{
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) {{
                return "Error: Game engine not found";
            }}
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const brStatus = bEngine.getGameAttribute("BribeStatus");
            const brDescriptions = bEngine.getGameAttribute("CustomLists").h.BribeDescriptions;
            
            if (!brStatus || !brDescriptions) {{
                return "Error: Bribe data not found";
            }}
            
            const filterQuery = "{filter_query}";
            const filter = (filterQuery === "None" || filterQuery === "null" || filterQuery === "undefined") ? "" : filterQuery;
            const filterLower = filter.toLowerCase();
            
            let output = "";
            output += "<div style='font-weight: bold; font-size: 16px; margin-bottom: 10px;'>💰 BRIBES STATUS</div>";
            
            let total_bribes = 0;
            let purchased_bribes = 0;
            let locked_bribes = 0;
            
            const purchased = [];
            const not_purchased = [];
            const locked = [];
            
            for (let i = 0; i < brDescriptions.length; i++) {{
                if (!brDescriptions[i]) continue;
                total_bribes++;
                
                const name = brDescriptions[i][0] || "Unknown Bribe";
                const cost = brDescriptions[i][2] || 0;
                const bonusType = brDescriptions[i][4] || "";
                const bonusValue = brDescriptions[i][5] || "";
                const status = brStatus[i] || 0;
                
                const bonus = bonusType && bonusValue ? 
                    bonusType + ": " + bonusValue : "No bonus info";
                
                const item = {{
                    name: name,
                    cost: cost,
                    bonus: bonus,
                    status: status,
                    index: i
                }};
                
                if (status === 1) {{
                    purchased_bribes++;
                    purchased.push(item);
                }} else if (status === -1) {{
                    locked_bribes++;
                    locked.push(item);
                }} else {{
                    not_purchased.push(item);
                }}
            }}
            
            if (purchased.length > 0) {{
                const filteredPurchased = purchased.filter(item => !filter || 
                    item.name.toLowerCase().includes(filterLower) || 
                    item.bonus.toLowerCase().includes(filterLower));
                if (filteredPurchased.length > 0) {{
                    output += "<div style='color: #6bcf7f; font-weight: bold; margin: 10px 0 5px 0;'>✅ PURCHASED (" + filteredPurchased.length + ")</div>";
                    for (const item of filteredPurchased) {{
                        output += "<div style='margin: 2px 0; padding: 3px 8px; background: rgba(107, 207, 127, 0.1); border-left: 3px solid #6bcf7f;'>" + item.name + " | Cost: " + item.cost + " | Bonus: " + item.bonus + "</div>";
                    }}
                }}
            }}
            
            if (not_purchased.length > 0) {{
                const filteredNotPurchased = not_purchased.filter(item => !filter || 
                    item.name.toLowerCase().includes(filterLower) || 
                    item.bonus.toLowerCase().includes(filterLower));
                if (filteredNotPurchased.length > 0) {{
                    output += "<div style='color: #ffd93d; font-weight: bold; margin: 10px 0 5px 0;'>❌ NOT PURCHASED (" + filteredNotPurchased.length + ")</div>";
                    for (const item of filteredNotPurchased) {{
                        output += "<div style='margin: 2px 0; padding: 3px 8px; background: rgba(255, 217, 61, 0.1); border-left: 3px solid #ffd93d;'>" + item.name + " | Cost: " + item.cost + " | Bonus: " + item.bonus + "</div>";
                    }}
                }}
            }}
            
            if (locked.length > 0) {{
                const filteredLocked = locked.filter(item => !filter || 
                    item.name.toLowerCase().includes(filterLower) || 
                    item.bonus.toLowerCase().includes(filterLower));
                if (filteredLocked.length > 0) {{
                    output += "<div style='color: #ff6b6b; font-weight: bold; margin: 10px 0 5px 0;'>🔒 LOCKED (" + filteredLocked.length + ")</div>";
                    for (const item of filteredLocked) {{
                        output += "<div style='margin: 2px 0; padding: 3px 8px; background: rgba(255, 107, 107, 0.1); border-left: 3px solid #ff6b6b;'>" + item.name + " | Cost: " + item.cost + " | Bonus: " + item.bonus + "</div>";
                    }}
                }}
            }}
            
            if (!filter) {{
                output += "<div style='margin-top: 15px; padding: 10px; background: rgba(0, 0, 0, 0.1); border-radius: 5px;'>";
                output += "<div style='font-weight: bold; margin-bottom: 5px;'>📊 SUMMARY</div>";
                output += "<div>Total Bribes: " + total_bribes + "</div>";
                output += "<div>Purchased: " + purchased_bribes + "/" + total_bribes + " (" + Math.round(purchased_bribes/total_bribes*100) + "%)</div>";
                if (locked_bribes > 0) {{
                    output += "<div>Locked: " + locked_bribes + "/" + total_bribes + " (" + Math.round(locked_bribes/total_bribes*100) + "%)</div>";
                }}
                output += "</div>";
            }}
            
            return output;
        }} catch (e) {{
            return "Error: " + e.message;
        }}
        '''

    @js_export(params=["bribe_name"])
    def buy_bribe_by_name_js(self, bribe_name=None):
        return f'''
        try {{
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) {{
                return "Error: Game engine not found";
            }}
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const brStatus = bEngine.getGameAttribute("BribeStatus");
            const brDescriptions = bEngine.getGameAttribute("CustomLists").h.BribeDescriptions;
            
            if (!brStatus || !brDescriptions) {{
                return "Error: Bribe data not found";
            }}
            
            const searchName = "{bribe_name}".toLowerCase();
            let found = false;
            let bribeIndex = -1;
            
            for (let i = 0; i < brDescriptions.length; i++) {{
                if (brDescriptions[i] && brDescriptions[i][0]) {{
                    const name = brDescriptions[i][0].toLowerCase();
                    if (name.includes(searchName)) {{
                        found = true;
                        bribeIndex = i;
                        break;
                    }}
                }}
            }}
            
            if (!found) {{
                return "❌ Bribe not found: " + "{bribe_name}";
            }}
            
            const currentStatus = brStatus[bribeIndex];
            if (currentStatus === 1) {{
                return "✅ Bribe '" + brDescriptions[bribeIndex][0] + "' is already purchased!";
            }}
            
            brStatus[bribeIndex] = 1;
            
            return "✅ Successfully purchased bribe: " + brDescriptions[bribeIndex][0];
        }} catch (e) {{
            return "Error: " + e.message;
        }}
        '''

    @js_export(params=["bribe_name"])
    def remove_bribe_by_name_js(self, bribe_name=None):
        return f'''
        try {{
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) {{
                return "Error: Game engine not found";
            }}
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const brStatus = bEngine.getGameAttribute("BribeStatus");
            const brDescriptions = bEngine.getGameAttribute("CustomLists").h.BribeDescriptions;
            
            if (!brStatus || !brDescriptions) {{
                return "Error: Bribe data not found";
            }}
            
            const searchName = "{bribe_name}".toLowerCase();
            let found = false;
            let bribeIndex = -1;
            
            for (let i = 0; i < brDescriptions.length; i++) {{
                if (brDescriptions[i] && brDescriptions[i][0]) {{
                    const name = brDescriptions[i][0].toLowerCase();
                    if (name.includes(searchName)) {{
                        found = true;
                        bribeIndex = i;
                        break;
                    }}
                }}
            }}
            
            if (!found) {{
                return "❌ Bribe not found: " + "{bribe_name}";
            }}
            
            const currentStatus = brStatus[bribeIndex];
            if (currentStatus === 0 || currentStatus === -1) {{
                return "ℹ️ Bribe '" + brDescriptions[bribeIndex][0] + "' is already not purchased!";
            }}
            
            brStatus[bribeIndex] = 0;
            
            return "🚫 Successfully removed bribe: " + brDescriptions[bribeIndex][0];
        }} catch (e) {{
            return "Error: " + e.message;
        }}
        '''

    @js_export()
    def buy_all_bribes_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) {
                return "Error: Game engine not found";
            }
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const brStatus = bEngine.getGameAttribute("BribeStatus");
            const brDescriptions = bEngine.getGameAttribute("CustomLists").h.BribeDescriptions;
            
            if (!brStatus || !brDescriptions) {
                return "Error: Bribe data not found";
            }
            
            let purchased_count = 0;
            let already_purchased = 0;
            
            for (let i = 0; i < brDescriptions.length; i++) {
                if (brDescriptions[i] && brDescriptions[i][0]) {
                    if (brStatus[i] === 1) {
                        already_purchased++;
                    } else {
                        brStatus[i] = 1;
                        purchased_count++;
                    }
                }
            }
            
            if (purchased_count === 0) {
                return "✅ All bribes are already purchased! (" + already_purchased + " bribes)";
            } else {
                return "💰 Purchased " + purchased_count + " bribes! (" + already_purchased + " were already purchased)";
            }
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @js_export()
    def remove_all_bribes_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) {
                return "Error: Game engine not found";
            }
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const brStatus = bEngine.getGameAttribute("BribeStatus");
            const brDescriptions = bEngine.getGameAttribute("CustomLists").h.BribeDescriptions;
            
            if (!brStatus || !brDescriptions) {
                return "Error: Bribe data not found";
            }
            
            let removed_count = 0;
            let already_removed = 0;
            
            for (let i = 0; i < brDescriptions.length; i++) {
                if (brDescriptions[i] && brDescriptions[i][0]) {
                    if (brStatus[i] === 0 || brStatus[i] === -1) {
                        already_removed++;
                    } else {
                        brStatus[i] = 0;
                        removed_count++;
                    }
                }
            }
            
            if (removed_count === 0) {
                return "✅ All bribes are already not purchased! (" + already_removed + " bribes)";
            } else {
                return "🚫 Removed " + removed_count + " bribes! (" + already_removed + " were already not purchased)";
            }
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @js_export()
    def get_bribe_names_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) {
                return "Error: Game engine not found";
            }
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const brDescriptions = bEngine.getGameAttribute("CustomLists").h.BribeDescriptions;
            
            if (!brDescriptions) {
                return "Error: Bribe data not found";
            }
            
            let names = [];
            for (let i = 0; i < brDescriptions.length; i++) {
                if (brDescriptions[i] && brDescriptions[i][0]) {
                    names.push(brDescriptions[i][0]);
                }
            }
            
            return names;
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @ui_autocomplete_input(
        label="Buy Bribe by Name",
        description="Purchase a specific bribe by name (with autocomplete)",
        button_text="Buy Bribe",
        placeholder="Enter bribe name",
        category="Bribe Management",
        order=2
    )
    async def buy_bribe_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if not value or not value.strip():
                    return "❌ Please enter a bribe name to purchase"
                
                if self.debug:
                    console.print(f"[stamp_cheats] Buying bribe: {value}")
                result = self.run_js_export('buy_bribe_by_name_js', self.injector, bribe_name=value.strip())
                return result
            except Exception as e:
                if self.debug:
                    console.print(f"[stamp_cheats] Error buying bribe: {e}")
                return f"ERROR: Error buying bribe: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    def get_autocomplete_suggestions_buy_bribe_ui(self):
        """Provide autocomplete suggestions for bribe names"""
        if hasattr(self, 'injector') and self.injector:
            try:
                result = self.run_js_export('get_bribe_names_js', self.injector)
                if isinstance(result, list):
                    return result
                else:
                    return []
            except Exception:
                return []
        return []

    @ui_autocomplete_input(
        label="Remove Bribe by Name", 
        description="Remove a specific bribe by name (with autocomplete)",
        button_text="Remove Bribe",
        placeholder="Enter bribe name",
        category="Bribe Management",
        order=3
    )
    async def remove_bribe_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if not value or not value.strip():
                    return "❌ Please enter a bribe name to remove"
                
                if self.debug:
                    console.print(f"[stamp_cheats] Removing bribe: {value}")
                result = self.run_js_export('remove_bribe_by_name_js', self.injector, bribe_name=value.strip())
                return result
            except Exception as e:
                if self.debug:
                    console.print(f"[stamp_cheats] Error removing bribe: {e}")
                return f"ERROR: Error removing bribe: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    def get_autocomplete_suggestions_remove_bribe_ui(self):
        """Provide autocomplete suggestions for bribe names"""
        if hasattr(self, 'injector') and self.injector:
            try:
                result = self.run_js_export('get_bribe_names_js', self.injector)
                if isinstance(result, list):
                    return result
                else:
                    return []
            except Exception:
                return []
        return []

    @ui_button(
        label="Buy All Bribes",
        description="Purchase all available bribes",
        category="Bribe Management",
        order=4
    )
    async def buy_all_bribes_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print("[stamp_cheats] Buying all bribes")
                result = self.run_js_export('buy_all_bribes_js', self.injector)
                return result
            except Exception as e:
                if self.debug:
                    console.print(f"[stamp_cheats] Error buying all bribes: {e}")
                return f"ERROR: Error buying all bribes: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_button(
        label="Remove All Bribes",
        description="Remove all purchased bribes",
        category="Bribe Management", 
        order=5
    )
    async def remove_all_bribes_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print("[stamp_cheats] Removing all bribes")
                result = self.run_js_export('remove_all_bribes_js', self.injector)
                return result
            except Exception as e:
                if self.debug:
                    console.print(f"[stamp_cheats] Error removing all bribes: {e}")
                return f"ERROR: Error removing all bribes: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

plugin_class = StampCheatsPlugin
