from plugin_system import PluginBase, js_export, ui_banner, ui_toggle, ui_button, ui_search_with_results, ui_autocomplete_input, plugin_command, console
from config_manager import config_manager

class SneakingCheatsPlugin(PluginBase):
    VERSION = "1.0.1"
    DESCRIPTION = "Comprehensive cheats for the sneaking game including money, unlocks, upgrades, and more. ⚠️ HIGH RISK: These features may brick your account as the sneaking game data structure is complex and not fully explored. Use at your own risk!"
    PLUGIN_ORDER = 2
    CATEGORY = "World 6"

    def __init__(self, config=None):
        super().__init__(config or {})        
        self.debug = config.get('debug', False) if config else False
        self.name = 'sneaking_cheats'
        self._talents_cache = None
        self._cache_timestamp = 0
        self._cache_duration = 300

    async def cleanup(self): pass
    async def update(self): pass
    async def on_config_changed(self, config): 
        self.debug = config.get('debug', False)
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)
    async def on_game_ready(self): pass

    async def get_cached_talents_list(self):
        import time
        if (not hasattr(self, '_talents_cache') or 
            not hasattr(self, '_cache_timestamp') or 
            not hasattr(self, '_cache_duration') or
            time.time() - self._cache_timestamp > self._cache_duration):
            
            if self.debug:
                console.print("[sneaking_cheats] Cache expired or missing, fetching talents list...")
            try:
                if not hasattr(self, 'injector') or not self.injector:
                    if self.debug:
                        console.print("[sneaking_cheats] No injector available")
                    return []
                
                raw_result = self.run_js_export('get_talent_names_js', self.injector)
                if self.debug:
                    console.print(f"[sneaking_cheats] Raw JS result: {raw_result}")
                
                if not raw_result or raw_result.startswith("Error:"):
                    if self.debug:
                        console.print(f"[sneaking_cheats] No valid result from JS: {raw_result}")
                    return []
                
                talent_items = []
                lines = raw_result.strip().split('\n')
                if self.debug:
                    console.print(f"[sneaking_cheats] Processing {len(lines)} lines")
                
                # Fallback: Use indices as names
                totalTalents = 20
                talent_items = [f"Talent {i+1}" for i in range(totalTalents)]
                self._talents_cache = talent_items
                self._cache_timestamp = time.time()
                self._cache_duration = 300
                if self.debug:
                    console.print(f"[sneaking_cheats] Cached {len(talent_items)} talents (indices)")
                return talent_items
            except Exception as e:
                if self.debug:
                    console.print(f"[sneaking_cheats] Error fetching talents list: {e}")
                return []
        else:
            if self.debug:
                console.print(f"[sneaking_cheats] Using cached talents list ({len(self._talents_cache)} items)")
            return self._talents_cache

    async def get_set_talent_level_ui_autocomplete(self, query: str = ""):
        if self.debug:
            console.print(f"[sneaking_cheats] get_set_talent_level_ui_autocomplete called with query: '{query}'")
        try:
            if not hasattr(self, 'injector') or not self.injector:
                if self.debug:
                    console.print("[sneaking_cheats] No injector available for autocomplete")
                return []
            
            talent_items = await self.get_cached_talents_list()
            if self.debug:
                console.print(f"[sneaking_cheats] Got {len(talent_items)} talent items from cache")
            
            if not talent_items:
                if self.debug:
                    console.print("[sneaking_cheats] No talent items found")
                return []
            
            query_lower = query.lower()
            suggestions = []
            
            # Accept index or 'Talent N' as input
            for i, item in enumerate(talent_items):
                if query_lower in item.lower() or query_lower == str(i+1):
                    suggestions.append(item)
                    if self.debug:
                        console.print(f"[sneaking_cheats] Added suggestion: {item}")
            
            if self.debug:
                console.print(f"[sneaking_cheats] Returning {len(suggestions)} suggestions: {suggestions}")
            return suggestions[:10]
        except Exception as e:
            if self.debug:
                console.print(f"[sneaking_cheats] Error in get_set_talent_level_ui_autocomplete: {e}")
            return []

    @ui_search_with_results(
        label="Sneaking Talents Status",
        description="Show all sneaking talents with their current levels and max levels",
        button_text="Show Talents",
        placeholder="Enter filter term (leave empty to show all)",
        category="Talents",
        order=6.5
    )
    async def sneaking_talents_status_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[sneaking_cheats] Getting sneaking talents status, filter: {value}")
                result = self.run_js_export('get_sneaking_talents_status_js', self.injector, filter_query=value or "")
                return result
            except Exception as e:
                if self.debug:
                    console.print(f"[sneaking_cheats] Error getting sneaking talents status: {e}")
                return f"ERROR: Error getting sneaking talents status: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_autocomplete_input(
        label="Set Talent Level",
        description="Set a specific sneaking talent to a specific level. Syntax: 'talent_name level' (e.g., 'strength 100')",
        button_text="Set Level",
        placeholder="Enter: talent_name level (e.g., 'strength 100')",
        category="Talents",
        order=6.6
    )
    async def set_talent_level_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[sneaking_cheats] Setting talent level, input: {value}")
                if not value or not value.strip():
                    return "Please provide talent index and level (e.g., '1 100' or 'Talent 1 100')"
                parts = value.strip().split()
                if len(parts) < 2:
                    return "Syntax: 'talent_index level' (e.g., '1 100' or 'Talent 1 100')"
                level_str = parts[-1]
                talent_name = ' '.join(parts[:-1])
                if self.debug:
                    console.print(f"[sneaking_cheats] Parsed - talent_name: '{talent_name}', level: {level_str}")
                try:
                    level_int = int(level_str)
                    if level_int < 0:
                        return "Level must be 0 or higher"
                except ValueError:
                    return "Level must be a valid number"
                result = await self.set_talent_level(talent_name, level_int)
                if self.debug:
                    console.print(f"[sneaking_cheats] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[sneaking_cheats] Error setting talent level: {e}")
                return f"ERROR: Error setting talent level: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_autocomplete_input(
        label="Add Jade Coins",
        description="Add a specific amount of Jade Coins to your current balance",
        button_text="Add Coins",
        placeholder="Enter amount (e.g., '1000000')",
        category="Money Cheats",
        order=7
    )
    async def add_jade_coins_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[sneaking_cheats] Adding Jade Coins, input: {value}")
                
                if not value or not value.strip():
                    return "Please provide an amount (e.g., '1000000')"
                
                try:
                    amount = int(value.strip())
                    if amount < 0:
                        return "Amount must be positive"
                except ValueError:
                    return "Amount must be a valid number"
                
                result = await self.add_jade_coins(amount)
                if self.debug:
                    console.print(f"[sneaking_cheats] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[sneaking_cheats] Error adding Jade Coins: {e}")
                return f"ERROR: Error adding Jade Coins: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_button(
        label="🚨 Fix Bricked Character ⚠️",
        description="⚠️ EMERGENCY FIX: Restore character data to working state ⚠️",
        category="Emergency Fixes",
        order=10
    )
    async def fix_bricked_character_ui(self):
        result = await self.fix_bricked_character()
        return f"Fix character executed! {result}"

    @ui_toggle(
        label="⚠️ Initialize Sneaking Game 🚨",
        description="⚠️ FIRST-TIME SETUP: Set up initial sneaking game state (use if you have no floor UI or player is NULL) - This sets up basic game data without nuking everything ⚠️",
        config_key="initialize_sneaking",
        default_value=False,
        category="Emergency Fixes",
        order=11
    )
    async def initialize_sneaking_ui(self, value: bool = None):
        if value is not None:
            self.config["initialize_sneaking"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector and value:
                try:
                    if self.debug:
                        console.print(f"[sneaking_cheats] Initializing sneaking game")
                    result = await self.initialize_sneaking(self.injector)
                    if self.debug:
                        console.print(f"[sneaking_cheats] Result: {result}")
                    return f"SUCCESS: {result}"
                except Exception as e:
                    if self.debug:
                        console.print(f"[sneaking_cheats] Error initializing sneaking game: {e}")
                    return f"ERROR: Error initializing sneaking game: {str(e)}"
        return f"Initialize Sneaking Game {'enabled' if self.config.get('initialize_sneaking', False) else 'disabled'}"




    @plugin_command(
        help="Get current sneaking game status.",
        params=[],
    )
    async def get_sneaking_status(self, injector=None, **kwargs):
        result = self.run_js_export('get_sneaking_status_js', injector)
        return result

    @plugin_command(
        help="Set Jade Coins to maximum amount.",
        params=[],
    )
    async def max_jade_coins(self, injector=None, **kwargs):
        result = self.run_js_export('max_jade_coins_js', injector)
        return result

    @plugin_command(
        help="Unlock all sneaking floors.",
        params=[],
    )
    async def unlock_all_floors(self, injector=None, **kwargs):
        result = self.run_js_export('unlock_all_floors_js', injector)
        return result

    @plugin_command(
        help="Max level all sneaking upgrades.",
        params=[],
    )
    async def max_all_upgrades(self, injector=None, **kwargs):
        result = self.run_js_export('max_all_upgrades_js', injector)
        return result

    @plugin_command(
        help="Unlock all ninja equipment.",
        params=[],
    )
    async def unlock_all_equipment(self, injector=None, **kwargs):
        result = self.run_js_export('unlock_all_equipment_js', injector)
        return result

    @plugin_command(
        help="Add a specific amount of Jade Coins.",
        params=[
            {"name": "amount", "type": int, "help": "Amount of Jade Coins to add"},
        ],
    )
    async def add_jade_coins(self, amount: int, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('add_jade_coins_js', self.injector, amount=amount)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @plugin_command(
        help="Get sneaking talents status showing all talents and their levels.",
        params=[],
    )
    async def get_sneaking_talents_status(self, injector=None, **kwargs):
        result = self.run_js_export('get_sneaking_talents_status_js', injector)
        return result

    @plugin_command(
        help="Set a specific sneaking talent to a specific level.",
        params=[
            {"name": "talent_name", "type": str, "help": "Name of the sneaking talent"},
            {"name": "level", "type": int, "help": "Level to set (0 or higher)"},
        ],
    )
    async def set_talent_level(self, talent_name: str, level: int, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('set_talent_level_js', self.injector, talent_name=talent_name, level=level)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @plugin_command(
        help="Set all sneaking talents to maximum level.",
        params=[],
    )
    async def max_all_talents(self, injector=None, **kwargs):
        result = self.run_js_export('max_all_talents_js', injector)
        return result

    @plugin_command(
        help="Reset all sneaking talents to level 0.",
        params=[],
    )
    async def reset_all_talents(self, injector=None, **kwargs):
        result = self.run_js_export('reset_all_talents_js', injector)
        return result

    @plugin_command(
        help="Set infinite stealth (no detection).",
        params=[],
    )
    async def infinite_stealth(self, injector=None, **kwargs):
        result = self.run_js_export('infinite_stealth_js', injector)
        return result

    @plugin_command(
        help="Set max sneaking experience for all ninja twins.",
        params=[],
    )
    async def max_sneaking_exp(self, injector=None, **kwargs):
        result = self.run_js_export('max_sneaking_exp_js', injector)
        return result

    @plugin_command(
        help="Fix bricked character data to restore game functionality.",
        params=[],
    )
    async def fix_bricked_character(self, injector=None, **kwargs):
        result = self.run_js_export('fix_bricked_character_js', injector)
        return result

    @plugin_command(
        help="Initialize sneaking game with proper first-time setup.",
        params=[],
    )
    async def initialize_sneaking(self, injector=None, **kwargs):
        result = self.run_js_export('initialize_sneaking_js', injector)
        return result

    @plugin_command(
        help="Add all 12 ninja twins with max levels.",
        params=[],
    )
    async def add_max_ninjas(self, injector=None, **kwargs):
        result = self.run_js_export('add_max_ninjas_js', injector)
        return result

    @plugin_command(
        help="Add one ninja twin with specified level.",
        params=[],
    )
    async def add_single_ninja(self, injector=None, **kwargs):
        result = self.run_js_export('add_single_ninja_js', injector)
        return result

    @plugin_command(
        help="Delete all ninja twins.",
        params=[],
    )
    async def delete_all_ninjas(self, injector=None, **kwargs):
        result = self.run_js_export('delete_all_ninjas_js', injector)
        return result

    @plugin_command(
        help="Spawn ninja actors on the game board.",
        params=[],
    )
    async def spawn_ninja_actors(self, injector=None, **kwargs):
        result = self.run_js_export('spawn_ninja_actors_js', injector)
        return result

    @js_export(params=["filter_query"])
    def get_sneaking_status_js(self, filter_query=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const ninja = bEngine.getGameAttribute("Ninja");
            const ninjaInfo = bEngine.getGameAttribute("CustomLists").h.NinjaInfo;
            if (!ninja || !ninjaInfo) {
                return "Error: Sneaking data not found";
            }
            let output = "";
            output += "<div style='font-weight: bold; font-size: 16px; margin-bottom: 10px;'>SNEAKING GAME STATUS</div>";
            const jadeCoins = ninja[102] ? ninja[102][1] || 0 : 0;
            const currentFloor = ninja[102] ? ninja[102][0] || 0 : 0;
            const floorsUnlocked = ninjaInfo[3] ? ninjaInfo[3].length : 0;
            const ninjaTwins = ninja.length > 0 ? ninja.length : 0;
            output += "<div style='margin: 10px 0; padding: 10px; background: rgba(0, 0, 0, 0.1); border-radius: 5px;'>";
            output += "<div style='font-weight: bold; margin-bottom: 5px;'>MONEY & PROGRESS</div>";
            output += "<div>Jade Coins: " + jadeCoins.toLocaleString() + "</div>";
            output += "<div>Current Floor: " + currentFloor + "</div>";
            output += "<div>Total Floors: " + floorsUnlocked + "</div>";
            output += "<div>Ninja Twins: " + ninjaTwins + "</div>";
            output += "</div>";
            if (ninjaInfo[3] && ninjaInfo[3].length > 0) {
                output += "<div style='margin: 10px 0; padding: 10px; background: rgba(0, 0, 0, 0.1); border-radius: 5px;'>";
                output += "<div style='font-weight: bold; margin-bottom: 5px;'>FLOORS</div>";
                const filterQuery = filter_query ? filter_query.toLowerCase() : "";
                for (let i = 0; i < ninjaInfo[3].length; i++) {
                    const floorName = ninjaInfo[3][i] || "Unknown Floor " + (i + 1);
                    const isUnlocked = i <= currentFloor;
                    const status = isUnlocked ? "UNLOCKED" : "LOCKED";
                    if (!filterQuery || floorName.toLowerCase().includes(filterQuery)) {
                        output += "<div style='margin: 2px 0; padding: 3px 8px; background: " + (isUnlocked ? "rgba(107, 207, 127, 0.1)" : "rgba(255, 107, 107, 0.1)") + "; border-left: 3px solid " + (isUnlocked ? "#6bcf7f" : "#ff6b6b") + ";'>";
                        output += floorName + " | " + status + "</div>";
                    }
                }
                output += "</div>";
            }
            if (ninja.length > 0) {
                output += "<div style='margin: 10px 0; padding: 10px; background: rgba(0, 0, 0, 0.1); border-radius: 5px;'>";
                output += "<div style='font-weight: bold; margin-bottom: 5px;'>NINJA TWINS</div>";
                for (let i = 0; i < Math.min(ninja.length, 12); i++) {
                    const ninjaData = ninja[i];
                    if (ninjaData && ninjaData.length > 0) {
                        const level = ninjaData[0] || 0;
                        const exp = ninjaData[1] || 0;
                        const stealth = ninjaData[2] || 0;
                        output += "<div style='margin: 2px 0; padding: 3px 8px; background: rgba(255, 217, 61, 0.1); border-left: 3px solid #ffd93d;'>";
                        output += "Ninja " + (i + 1) + " | Level: " + level + " | EXP: " + exp.toLocaleString() + " | Stealth: " + stealth + "</div>";
                    }
                }
                output += "</div>";
            }
            return output;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export(params=["filter_query"])
    def get_sneaking_talents_status_js(self, filter_query=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const ninja = bEngine.getGameAttribute("Ninja");
            const ninjaInfo = bEngine.getGameAttribute("CustomLists").h.NinjaInfo;
            if (!ninja || !ninjaInfo) {
                return "Error: Sneaking data not found";
            }
let output = "";
            output += "<div style='font-weight: bold; font-size: 16px; margin-bottom: 10px;'>SNEAKING TALENTS STATUS</div>";
            const talentLevels = ninja[103] || [];
            const talentMaxLevels = ninjaInfo[28] || [];
            const totalTalents = talentLevels.length || 20;
            const talentNames = Array.from({length: totalTalents}, (_, i) => `Talent ${i + 1}`);
            while (talentMaxLevels.length < talentLevels.length) talentMaxLevels.push(100);
            let total_talents = talentLevels.length;
            let unlocked_talents = 0;
            let max_leveled_talents = 0;
            const allTalents = [];
            for (let i = 0; i < talentLevels.length; i++) {
                const name = `Talent ${i + 1}`;
                const level = talentLevels[i] || 0;
                const maxLevel = talentMaxLevels[i] || 100;
                const isUnlocked = level > 0;
                if (isUnlocked) unlocked_talents++;
                if (level === maxLevel) max_leveled_talents++;
                allTalents.push({ name, level, maxLevel, isUnlocked, index: i });
            }
            const filterQuery = filter_query ? filter_query.toLowerCase() : "";
            output += "<div style='margin: 10px 0; padding: 10px; background: rgba(0,0,0,0.07); border-radius: 5px;'>";
            output += `<div style='font-weight:bold;margin-bottom:5px;'>All Sneaking Talents (${allTalents.length})</div>`;
            for (const item of allTalents) {
                if (filterQuery && !item.name.toLowerCase().includes(filterQuery)) continue;
                let color = item.level === item.maxLevel ? '#6bcf7f' : item.isUnlocked ? '#ffd93d' : '#ff6b6b';
                let bg = item.level === item.maxLevel ? 'rgba(107,207,127,0.1)' : item.isUnlocked ? 'rgba(255,217,61,0.1)' : 'rgba(255,107,107,0.1)';
                let status = item.level === item.maxLevel ? 'MAX' : item.isUnlocked ? 'UNLOCKED' : 'LOCKED';
                output += `<div style='margin:2px 0;padding:3px 8px;background:${bg};border-left:3px solid ${color};'>${item.name} | Level: ${item.level} | ${status}</div>`;
            }
            output += "</div>";
            output += "<div style='margin-top: 15px; padding: 10px; background: rgba(0, 0, 0, 0.1); border-radius: 5px;'>";
            output += "<div style='font-weight: bold; margin-bottom: 5px;'>SUMMARY</div>";
            output += "<div>Total Talents: " + total_talents + "</div>";
            output += "<div>Unlocked: " + unlocked_talents + "/" + total_talents + " (" + Math.round(unlocked_talents/total_talents*100) + "%)</div>";
            output += "</div>";
            return output;
        } catch (e) {
            return `[ERROR] ${e.message}`;
        }
        '''
    @ui_autocomplete_input(
        label="Set All Talents to Level",
        description="Set all sneaking talents to a specific level (e.g., '50')",
        button_text="Set All Levels",
        placeholder="Enter level (e.g., '50')",
        category="Talents",
        order=6.7
    )
    async def set_all_talents_level_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[sneaking_cheats] Setting all talents to level: {value}")
                if not value or not value.strip():
                    return "Please provide a level (e.g., '50')"
                try:
                    level_int = int(value.strip())
                    if level_int < 0:
                        return "Level must be 0 or higher"
                except ValueError:
                    return "Level must be a valid number"
                result = await self.set_all_talents_level(level_int)
                if self.debug:
                    console.print(f"[sneaking_cheats] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[sneaking_cheats] Error setting all talents level: {e}")
                return f"ERROR: Error setting all talents level: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @plugin_command(
        help="Set all sneaking talents to a specific level.",
        params=[
            {"name": "level", "type": int, "help": "Level to set (0 or higher)"},
        ],
    )
    async def set_all_talents_level(self, level: int, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('set_all_talents_level_js', self.injector, level=level)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["level"])
    def set_all_talents_level_js(self, level=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const ninja = bEngine.getGameAttribute("Ninja");
            if (ninja?.[103]) {
                for (let i = 0; i < ninja[103].length; i++) {
                    ninja[103][i] = (typeof level === 'number' && !isNaN(level)) ? level : 999999;
                }
                console.log(`🎯 Set all ${ninja[103].length} ninja talents to level ${level}`);
                return true;
            }
            return false;
        } catch (e) {
            console.error("Error setting all ninja talents:", e);
            return false;
        }
        '''

    @js_export(params=["talent_name", "level"])
    def set_talent_level_js(self, talent_name=None, level=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const ninja = bEngine.getGameAttribute("Ninja");
            const ninjaInfo = bEngine.getGameAttribute("CustomLists").h.NinjaInfo;
            
            if (!ninja || !ninjaInfo) {
                return "Error: Sneaking data not found";
            }
            
            if (!talent_name || level === undefined || level === null) {
                return "Error: Talent name and level are required";
            }
            
            if (level < 0) {
                return "Error: Level must be 0 or higher";
            }
            
            const talentLevels = ninja[103] || [];
            const talentMaxLevels = ninjaInfo[28] || [];
            const totalTalents = talentLevels.length || 20;
            let found_index = -1;
            let found_name = "";
            // Accept either index or 'Talent N' as name
            if (/^talent\\s*\\d+$/i.test(talent_name.trim())) {
                found_index = parseInt(talent_name.trim().match(/\\d+/)[0], 10) - 1;
                found_name = `Talent ${found_index + 1}`;
            } else if (/^\\d+$/.test(talent_name.trim())) {
                found_index = parseInt(talent_name.trim(), 10) - 1;
                found_name = `Talent ${found_index + 1}`;
            }
            if (found_index < 0 || found_index >= totalTalents) {
                return `Error: Talent '${talent_name}' not found (valid: 1-${totalTalents})`;
            }
            const maxLevel = talentMaxLevels[found_index] || 100;
            const oldLevel = talentLevels[found_index] || 0;
            if (level > maxLevel) {
                return `Error: Level ${level} exceeds maximum level ${maxLevel} for '${found_name}'`;
            }
            while (talentLevels.length <= found_index) {
                talentLevels.push(0);
            }
            talentLevels[found_index] = level;
            ninja[103] = talentLevels;
            if (level === 0) {
                return `✅ Reset '${found_name}' to level 0 (was level ${oldLevel})`;
            } else if (level === maxLevel) {
                return `🚀 Set '${found_name}' to maximum level ${maxLevel} (was level ${oldLevel})`;
            } else {
                return `📈 Set '${found_name}' to level ${level} (was level ${oldLevel}, max is ${maxLevel})`;
            }
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def max_all_talents_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const ninja = bEngine.getGameAttribute("Ninja");
            const ninjaInfo = bEngine.getGameAttribute("CustomLists").h.NinjaInfo;
            
            if (!ninja || !ninjaInfo) {
                return "Error: Sneaking data not found";
            }
            
            const talentLevels = ninja[103] || [];
            const talentNames = ninjaInfo[27] || [];
            const talentMaxLevels = ninjaInfo[28] || [];
            
            if (talentNames.length === 0) {
                return "Error: No talent data found";
            }
            
            let maxedCount = 0;
            let alreadyMaxedCount = 0;
            
            while (talentLevels.length < talentNames.length) {
                talentLevels.push(0);
            }
            
            for (let i = 0; i < talentNames.length; i++) {
                const maxLevel = talentMaxLevels[i] || 100;
                const currentLevel = talentLevels[i] || 0;
                
                if (currentLevel < maxLevel) {
                    talentLevels[i] = maxLevel;
                    maxedCount++;
                } else {
                    alreadyMaxedCount++;
                }
            }
            
            ninja[103] = talentLevels;
            
            if (maxedCount === 0) {
                return `✅ All talents are already at maximum level! (${alreadyMaxedCount} talents)`;
            } else {
                return `🚀 Set ${maxedCount} talents to maximum level! (${alreadyMaxedCount} were already maxed)`;
            }
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def reset_all_talents_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const ninja = bEngine.getGameAttribute("Ninja");
            const ninjaInfo = bEngine.getGameAttribute("CustomLists").h.NinjaInfo;
            
            if (!ninja || !ninjaInfo) {
                return "Error: Sneaking data not found";
            }
            
            // Get talent data
            const talentLevels = ninja[103] || [];
            const talentNames = ninjaInfo[27] || [];
            
            if (talentNames.length === 0) {
                return "Error: No talent data found";
            }
            
            let resetCount = 0;
            let alreadyResetCount = 0;
            
            // Ensure talent levels array is large enough
            while (talentLevels.length < talentNames.length) {
                talentLevels.push(0);
            }
            
            for (let i = 0; i < talentNames.length; i++) {
                const currentLevel = talentLevels[i] || 0;
                
                if (currentLevel > 0) {
                    talentLevels[i] = 0;
                    resetCount++;
                } else {
                    alreadyResetCount++;
                }
            }
            
            ninja[103] = talentLevels;
            
            if (resetCount === 0) {
                return `✅ All talents are already reset! (${alreadyResetCount} talents)`;
            } else {
                return `🔄 Reset ${resetCount} talents to level 0! (${alreadyResetCount} were already reset)`;
            }
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def max_jade_coins_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const ninja = bEngine.getGameAttribute("Ninja");
            
            if (!ninja) {
                return "Error: Ninja data not found";
            }
            
            if (!ninja[102]) {
                ninja[102] = [0, 0];
            }
            
            const oldAmount = ninja[102][1] || 0;
            const newAmount = 999999999;
            
            ninja[102][1] = newAmount;
            
            return `Set Jade Coins to maximum: ${newAmount.toLocaleString()} (was ${oldAmount.toLocaleString()})`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def unlock_all_floors_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const ninja = bEngine.getGameAttribute("Ninja");
            const ninjaInfo = bEngine.getGameAttribute("CustomLists").h.NinjaInfo;
            
            if (!ninja || !ninjaInfo || !ninjaInfo[3]) {
                return "Error: Floor data not found";
            }
            
            const totalFloors = ninjaInfo[3].length;
            
            if (!ninja[102]) {
                ninja[102] = [0, 0];
            }
            
            ninja[102][0] = totalFloors - 1;
            
            return `Unlocked all ${totalFloors} sneaking floors! (Set current floor to ${totalFloors - 1})`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def max_all_upgrades_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const ninja = bEngine.getGameAttribute("Ninja");
            const ninjaInfo = bEngine.getGameAttribute("CustomLists").h.NinjaInfo;
            
            if (!ninja || !ninjaInfo) {
                return "Error: Ninja data not found";
            }
            
            let upgradedCount = 0;
            
            for (let i = 0; i < ninja.length; i++) {
                const ninjaData = ninja[i];
                if (ninjaData && Array.isArray(ninjaData)) {
                    for (let j = 0; j < ninjaData.length; j++) {
                        if (typeof ninjaData[j] === 'number' && ninjaData[j] >= 0 && ninjaData[j] < 999) {
                            ninjaData[j] = 999;
                            upgradedCount++;
                        }
                    }
                }
            }
            
            return `Maxed ${upgradedCount} sneaking upgrades!`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def unlock_all_equipment_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const ninja = bEngine.getGameAttribute("Ninja");
            
            if (!ninja) {
                return "Error: Ninja data not found";
            }
            
            let unlockedCount = 0;
            const currentChar = 0;
            
            for (let slotIndex = 0; slotIndex < 24; slotIndex++) {
                const inventoryIndex = 12 + (4 * slotIndex) + (24 * currentChar);
                const inventorySlot = ninja[inventoryIndex];
                
                if (inventorySlot && Array.isArray(inventorySlot)) {
                    if (inventorySlot[0] === "Blank" || !inventorySlot[0]) {
                        const itemKey = "NjItem" + Math.floor(slotIndex / 4);
                        inventorySlot[0] = itemKey;
                        inventorySlot[1] = 1;
                        unlockedCount++;
                    }
                }
            }
            
            return `Unlocked ${unlockedCount} ninja equipment items!`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export(params=["amount"])
    def add_jade_coins_js(self, amount=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const ninja = bEngine.getGameAttribute("Ninja");
            
            if (!ninja) {
                return "Error: Ninja data not found";
            }
            
            if (!amount || amount < 0) {
                return "Error: Invalid amount provided";
            }
            
            if (!ninja[102]) {
                ninja[102] = [0, 0];
            }
            
            const oldAmount = ninja[102][1] || 0;
            const newAmount = oldAmount + amount;
            
            ninja[102][1] = newAmount;
            
            return `Added ${amount.toLocaleString()} Jade Coins! New total: ${newAmount.toLocaleString()}`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def fix_bricked_character_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const ninja = bEngine.getGameAttribute("Ninja");
            const ninjaInfo = bEngine.getGameAttribute("CustomLists").h.NinjaInfo;
            
            if (!ninja) {
                return "Error: Ninja data not found";
            }
            
            let fixedCount = 0;
            
            ninja.length = 0;
            
            for (let i = 0; i < 12; i++) {
                const twinData = [];
                twinData.push(1);
                twinData.push(0);
                twinData.push(50);
                twinData.push(0);
                ninja.push(twinData);
                fixedCount++;
            }
            
            for (let charIndex = 0; charIndex < 10; charIndex++) {
                for (let slotIndex = 0; slotIndex < 24; slotIndex++) {
                    const inventorySlot = [];
                    inventorySlot.push("Blank");
                    inventorySlot.push(0);
                    ninja.push(inventorySlot);
                    fixedCount++;
                }
            }
            
            const doorHealth = [];
            const totalFloors = ninjaInfo && ninjaInfo[3] ? ninjaInfo[3].length : 20;
            for (let i = 0; i < totalFloors; i++) {
                doorHealth.push(0);
            }
            doorHealth[0] = 1000;
            ninja.push(doorHealth);
            fixedCount++;
            
            const mainChar = [];
            mainChar.push(0);
            mainChar.push(1000);
            mainChar.push(0);
            mainChar.push(0);
            mainChar.push(0);
            mainChar.push(0);
            mainChar.push(0);
            mainChar.push(0);
            mainChar.push(0);
            mainChar.push("");
            mainChar.push(0);
            ninja.push(mainChar);
            fixedCount++;
            
            const upgrades = [];
            const totalUpgrades = 20;
            for (let i = 0; i < totalUpgrades; i++) {
                upgrades.push(0);
            }
            ninja.push(upgrades);
            fixedCount++;
            
            const itemCollection = [];
            const totalItems = ninjaInfo && ninjaInfo[29] ? Math.floor(ninjaInfo[29].length / 3) : 20;
            for (let i = 0; i < totalItems; i++) {
                itemCollection.push(0);
            }
            ninja.push(itemCollection);
            fixedCount++;
            
            const monsterKills = [];
            const totalMonsters = ninjaInfo && ninjaInfo[30] ? ninjaInfo[30].length : 20;
            for (let i = 0; i < totalMonsters; i++) {
                monsterKills.push(0);
            }
            ninja.push(monsterKills);
            fixedCount++;
            
            for (let i = 106; i < 120; i++) {
                const otherData = [];
                for (let j = 0; j < 10; j++) {
                    otherData.push(0);
                }
                ninja.push(otherData);
                fixedCount++;
            }
            
            return `🔧 COMPLETE REBUILD: Fixed ${fixedCount} character data arrays! Character should now be functional.`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def initialize_sneaking_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const ninja = bEngine.getGameAttribute("Ninja");
            const ninjaInfo = bEngine.getGameAttribute("CustomLists").h.NinjaInfo;
            const n = ctx["scripts.CustomMaps"];
            
            if (!ninja) {
                return "Error: Ninja data not found";
            }
            
            let initializedCount = 0;
            
            if (ninja[102]) {
                ninja[102][0] = 0;
                ninja[102][1] = 1000;
                ninja[102][2] = 0;
                ninja[102][3] = 0;
                ninja[102][4] = 0;
                ninja[102][5] = 0;
                ninja[102][6] = 0;
                ninja[102][7] = 0;
                ninja[102][8] = 0;
                ninja[102][9] = "";
                ninja[102][10] = 0;
                initializedCount++;
            }
            
            for (let i = 0; i < 12; i++) {
                if (ninja[i] && Array.isArray(ninja[i])) {
                    ninja[i][0] = 1;
                    ninja[i][1] = 0;
                    ninja[i][2] = 50;
                    ninja[i][3] = 0;
                    initializedCount++;
                }
            }
            
            if (ninja[0] && Array.isArray(ninja[0])) {
                ninja[0][0] = 1;
                ninja[0][1] = 0;
                ninja[0][2] = 50;
                ninja[0][3] = 0;
                initializedCount++;
            }
            
            if (ninja[0] && Array.isArray(ninja[0]) && ninja[0][0] === 0) {
                ninja[0][0] = 1;
                initializedCount++;
            }
            
            if (ninja[100]) {
                const totalFloors = ninjaInfo && ninjaInfo[3] ? ninjaInfo[3].length : 20;
                for (let i = 0; i < totalFloors; i++) {
                    const baseDoorHP = 1000 + (i * 500);
                    ninja[100][i] = baseDoorHP;
                }
                initializedCount++;
            }
            
            if (ninja[103]) {
                const totalUpgrades = 20;
                for (let i = 0; i < totalUpgrades; i++) {
                    ninja[103][i] = 0;
                }
                initializedCount++;
            }
            
            if (ninja[105]) {
                const totalMonsters = ninjaInfo && ninjaInfo[30] ? ninjaInfo[30].length : 20;
                for (let i = 0; i < totalMonsters; i++) {
                    ninja[105][i] = 0;
                }
                initializedCount++;
            }
            
            if (ninja[104]) {
                const totalItems = ninjaInfo && ninjaInfo[29] ? Math.floor(ninjaInfo[29].length / 3) : 20;
                for (let i = 0; i < totalItems; i++) {
                    ninja[104][i] = 0;
                }
                initializedCount++;
            }
            
            for (let charIndex = 0; charIndex < 10; charIndex++) {
                for (let slotIndex = 0; slotIndex < 24; slotIndex++) {
                    const inventoryIndex = 12 + (4 * slotIndex) + (24 * charIndex);
                    const inventorySlot = ninja[inventoryIndex];
                    
                    if (inventorySlot && Array.isArray(inventorySlot)) {
                        inventorySlot[0] = "Blank";
                        inventorySlot[1] = 0;
                        initializedCount++;
                    }
                }
            }
            
            if (ninjaInfo && ninjaInfo[3] && ninjaInfo[3].length > 0) {
                initializedCount++;
            }
            
            const pixelHelperActors = bEngine.getGameAttribute("PixelHelperActor");
            let sneakingActor = null;
            
            for (let i = 0; i < pixelHelperActors.length; i++) {
                if (pixelHelperActors[i] && pixelHelperActors[i].behaviors) {
                    const behaviors = pixelHelperActors[i].behaviors;
                    for (let j = 0; j < behaviors.length; j++) {
                        if (behaviors[j] && behaviors[j]._GenINFO && behaviors[j]._GenINFO[77]) {
                            sneakingActor = pixelHelperActors[i];
                            break;
                        }
                    }
                    if (sneakingActor) break;
                }
            }
            
            if (sneakingActor) {
                const sneakingBehavior = sneakingActor.behaviors.find(b => b._GenINFO && b._GenINFO[77]);
                if (sneakingBehavior) {
                    if (!sneakingBehavior._GenINFO[77]) {
                        sneakingBehavior._GenINFO[77] = [];
                    }
                    
                    for (let i = 0; i < 12; i++) {
                        if (ninja[i] && Array.isArray(ninja[i]) && ninja[i][0] > 0) {
                            sneakingBehavior._GenINFO[77][i] = 400 + (i * 30);
                            
                            bEngine.gameAttributes.h.DummyNumber5 = i;
                            bEngine.gameAttributes.h.DummyText3 = "Ninja";
                            
                            c.createRecycledActor(
                                c.getActorType(358), 
                                sneakingBehavior._GenINFO[77][i], 
                                397 + (-150 * Math.round(ninja[i][0] - 3 * Math.floor(ninja[i][0] / 3))), 
                                0
                            );
                            
                            initializedCount++;
                        }
                    }
                }
            }
            
            return `INITIALIZED: Set up ${initializedCount} sneaking game arrays and spawned ninja actors! Game should now be functional with UI and visible ninjas.`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def add_max_ninjas_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const ninja = bEngine.getGameAttribute("Ninja");
            const n = ctx["scripts.CustomMaps"];
            
            if (!ninja) {
                return "Error: Ninja data not found";
            }
            
            let addedCount = 0;
            
            for (let i = 0; i < 12; i++) {
                if (ninja[i] && Array.isArray(ninja[i])) {
                    ninja[i][0] = 999;
                    ninja[i][1] = 999999999;
                    ninja[i][2] = 999;
                    ninja[i][3] = 999;
                    addedCount++;
                }
            }
            
            return `Added ${addedCount} ninja twins with max levels!`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def add_single_ninja_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const ninja = bEngine.getGameAttribute("Ninja");
            const n = ctx["scripts.CustomMaps"];
            
            if (!ninja) {
                return "Error: Ninja data not found";
            }
            
            let ninjaIndex = -1;
            for (let i = 0; i < 12; i++) {
                if (!ninja[i] || !Array.isArray(ninja[i]) || ninja[i][0] === 0 || ninja[i][0] === undefined) {
                    ninjaIndex = i;
                    break;
                }
            }
            
            if (ninjaIndex === -1) {
                return "Error: All ninja slots are full (max 12 ninjas)";
            }
            
            ninja[ninjaIndex][0] = 50;
            ninja[ninjaIndex][1] = 100000;
            ninja[ninjaIndex][2] = 100;
            ninja[ninjaIndex][3] = 50;
            
            return `Added ninja twin #${ninjaIndex + 1} with level 50!`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def delete_all_ninjas_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const ninja = bEngine.getGameAttribute("Ninja");
            const n = ctx["scripts.CustomMaps"];
            
            if (!ninja) {
                return "Error: Ninja data not found";
            }
            
            let deletedCount = 0;
            
            for (let i = 0; i < 12; i++) {
                if (ninja[i] && Array.isArray(ninja[i])) {
                    ninja[i][0] = 0;
                    ninja[i][1] = 0;
                    ninja[i][2] = 0;
                    ninja[i][3] = 0;
                    deletedCount++;
                }
            }
            
            return `Deleted ${deletedCount} ninja twins!`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def spawn_ninja_actors_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const ninja = bEngine.getGameAttribute("Ninja");
            const ninjaInfo = bEngine.getGameAttribute("CustomLists").h.NinjaInfo;
            const c = ctx["com.stencyl.behavior.Script"];
            const n = ctx["scripts.CustomMaps"];
            
            if (!ninja) {
                return "Error: Ninja data not found";
            }
            
            const pixelHelperActors = bEngine.getGameAttribute("PixelHelperActor");
            let sneakingActor = null;
            
            for (let i = 0; i < pixelHelperActors.length; i++) {
                if (pixelHelperActors[i] && pixelHelperActors[i].behaviors) {
                    const behaviors = pixelHelperActors[i].behaviors;
                    for (let j = 0; j < behaviors.length; j++) {
                        if (behaviors[j] && behaviors[j]._GenINFO && behaviors[j]._GenINFO[77]) {
                            sneakingActor = pixelHelperActors[i];
                            break;
                        }
                    }
                    if (sneakingActor) break;
                }
            }
            
            if (!sneakingActor) {
                return "Error: Could not find sneaking game actor";
            }
            
            const sneakingBehavior = sneakingActor.behaviors.find(b => b._GenINFO && b._GenINFO[77]);
            if (!sneakingBehavior) {
                return "Error: Could not find sneaking behavior";
            }
            
            if (!sneakingBehavior._GenINFO[77]) {
                sneakingBehavior._GenINFO[77] = [];
            }
            
            let spawnedCount = 0;
            
            for (let i = 0; i < 12; i++) {
                if (ninja[i] && Array.isArray(ninja[i]) && ninja[i][0] > 0) {
                    if (n._customBlock_Ninja("ActionDisp", i, 0) === 1) {
                        sneakingBehavior._GenINFO[77][i] = ninjaInfo[6] && ninjaInfo[6][i] ? 
                            ninjaInfo[6][i] : 400 + (i * 30);
                    } else if (n._customBlock_Ninja("ActionDisp", i, 0) === 3) {
                        sneakingBehavior._GenINFO[77][i] = c.randomInt(800, 870);
                    } else {
                        sneakingBehavior._GenINFO[77][i] = c.randomInt(100, 800);
                    }
                    
                    bEngine.gameAttributes.h.DummyNumber5 = i;
                    bEngine.gameAttributes.h.DummyText3 = "Ninja";
                    
                    c.createRecycledActor(
                        c.getActorType(358), 
                        sneakingBehavior._GenINFO[77][i], 
                        397 + (-150 * Math.round(ninja[i][0] - 3 * Math.floor(ninja[i][0] / 3))), 
                        0
                    );
                    
                    spawnedCount++;
                }
            }
            
            return `Spawned ${spawnedCount} ninja actors using game logic!`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''



plugin_class = SneakingCheatsPlugin