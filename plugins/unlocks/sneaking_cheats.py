from plugin_system import PluginBase, js_export, ui_banner, ui_toggle, ui_search_with_results, plugin_command, ui_autocomplete_input, console
from config_manager import config_manager

class SneakingCheatsPlugin(PluginBase):
    VERSION = "1.0.0"
    DESCRIPTION = "Comprehensive cheats for the sneaking game including money, unlocks, upgrades, and more. ⚠️ HIGH RISK: These features may brick your account as the sneaking game data structure is complex and not fully explored. Use at your own risk!"
    PLUGIN_ORDER = 6
    CATEGORY = "Unlocks"

    def __init__(self, config=None):
        super().__init__(config or {})        
        self.debug = config.get('debug', False) if config else False
        self.name = 'sneaking_cheats'

    async def cleanup(self): pass
    async def update(self): pass
    async def on_config_changed(self, config): 
        self.debug = config.get('debug', False)
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)
    async def on_game_ready(self): pass

    @ui_banner(
        label="⚠️ HIGH RISK WARNING",
        description="This plugin is work-in-progress and has a high risk of bricking your quests permanently! Use at your own risk!",
        banner_type="warning",
        category="Money Cheats",
        order=-100
    )
    async def warning_banner(self):
        return "Warning banner displayed"

    @ui_toggle(
        label="Debug Mode",
        description="Enable debug logging for sneaking cheats plugin",
        config_key="debug",
        default_value=False,
        category="Debug Settings",
        order=1
    )
    async def enable_debug(self, value: bool = None):
        if value is not None:
            self.config["debug"] = value
            self.save_to_global_config()
            self.debug = value
        return f"Debug mode {'enabled' if self.config.get('debug', False) else 'disabled'}"

    @ui_toggle(
        label="Max Jade Coins",
        description="Set Jade Coins to maximum amount (999,999,999)",
        config_key="max_jade_coins",
        default_value=False,
        category="Money Cheats",
        order=2
    )
    async def max_jade_coins_ui(self, value: bool = None):
        if value is not None:
            self.config["max_jade_coins"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector and value:
                try:
                    if self.debug:
                        console.print(f"[sneaking_cheats] Setting max Jade Coins")
                    result = await self.max_jade_coins(self.injector)
                    if self.debug:
                        console.print(f"[sneaking_cheats] Result: {result}")
                    return f"SUCCESS: {result}"
                except Exception as e:
                    if self.debug:
                        console.print(f"[sneaking_cheats] Error setting max Jade Coins: {e}")
                    return f"ERROR: Error setting max Jade Coins: {str(e)}"
        return f"Max Jade Coins {'enabled' if self.config.get('max_jade_coins', False) else 'disabled'}"

    @ui_toggle(
        label="Unlock All Sneaking Floors",
        description="Unlock all sneaking floors and areas",
        config_key="unlock_all_floors",
        default_value=False,
        category="Unlock Cheats",
        order=3
    )
    async def unlock_all_floors_ui(self, value: bool = None):
        if value is not None:
            self.config["unlock_all_floors"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector and value:
                try:
                    if self.debug:
                        console.print(f"[sneaking_cheats] Unlocking all floors")
                    result = await self.unlock_all_floors(self.injector)
                    if self.debug:
                        console.print(f"[sneaking_cheats] Result: {result}")
                    return f"SUCCESS: {result}"
                except Exception as e:
                    if self.debug:
                        console.print(f"[sneaking_cheats] Error unlocking all floors: {e}")
                    return f"ERROR: Error unlocking all floors: {str(e)}"
        return f"Unlock All Floors {'enabled' if self.config.get('unlock_all_floors', False) else 'disabled'}"

    @ui_toggle(
        label="Max All Sneaking Upgrades",
        description="Max level all sneaking upgrades and equipment",
        config_key="max_all_upgrades",
        default_value=False,
        category="Upgrade Cheats",
        order=4
    )
    async def max_all_upgrades_ui(self, value: bool = None):
        if value is not None:
            self.config["max_all_upgrades"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector and value:
                try:
                    if self.debug:
                        console.print(f"[sneaking_cheats] Maxing all upgrades")
                    result = await self.max_all_upgrades(self.injector)
                    if self.debug:
                        console.print(f"[sneaking_cheats] Result: {result}")
                    return f"SUCCESS: {result}"
                except Exception as e:
                    if self.debug:
                        console.print(f"[sneaking_cheats] Error maxing all upgrades: {e}")
                    return f"ERROR: Error maxing all upgrades: {str(e)}"
        return f"Max All Upgrades {'enabled' if self.config.get('max_all_upgrades', False) else 'disabled'}"

    @ui_toggle(
        label="Unlock All Ninja Equipment",
        description="Unlock all ninja equipment and items",
        config_key="unlock_all_equipment",
        default_value=False,
        category="Equipment Cheats",
        order=5
    )
    async def unlock_all_equipment_ui(self, value: bool = None):
        if value is not None:
            self.config["unlock_all_equipment"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector and value:
                try:
                    if self.debug:
                        console.print(f"[sneaking_cheats] Unlocking all equipment")
                    result = await self.unlock_all_equipment(self.injector)
                    if self.debug:
                        console.print(f"[sneaking_cheats] Result: {result}")
                    return f"SUCCESS: {result}"
                except Exception as e:
                    if self.debug:
                        console.print(f"[sneaking_cheats] Error unlocking all equipment: {e}")
                    return f"ERROR: Error unlocking all equipment: {str(e)}"
        return f"Unlock All Equipment {'enabled' if self.config.get('unlock_all_equipment', False) else 'disabled'}"

    @ui_search_with_results(
        label="Sneaking Status",
        description="Show current sneaking game status including Jade Coins, floors unlocked, upgrades, etc.",
        button_text="Show Status",
        placeholder="Enter filter term (leave empty to show all)",
        category="Status & Info",
        order=6
    )
    async def sneaking_status_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[sneaking_cheats] Getting sneaking status, filter: {value}")
                result = self.run_js_export('get_sneaking_status_js', self.injector, filter_query=value or "")
                return result
            except Exception as e:
                if self.debug:
                    console.print(f"[sneaking_cheats] Error getting sneaking status: {e}")
                return f"ERROR: Error getting sneaking status: {str(e)}"
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

    @ui_toggle(
        label="Infinite Stealth",
        description="Set stealth to maximum (no detection chance)",
        config_key="infinite_stealth",
        default_value=False,
        category="Gameplay Cheats",
        order=8
    )
    async def infinite_stealth_ui(self, value: bool = None):
        if value is not None:
            self.config["infinite_stealth"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector and value:
                try:
                    if self.debug:
                        console.print(f"[sneaking_cheats] Setting infinite stealth")
                    result = await self.infinite_stealth(self.injector)
                    if self.debug:
                        console.print(f"[sneaking_cheats] Result: {result}")
                    return f"SUCCESS: {result}"
                except Exception as e:
                    if self.debug:
                        console.print(f"[sneaking_cheats] Error setting infinite stealth: {e}")
                    return f"ERROR: Error setting infinite stealth: {str(e)}"
        return f"Infinite Stealth {'enabled' if self.config.get('infinite_stealth', False) else 'disabled'}"

    @ui_toggle(
        label="Max Sneaking Experience",
        description="Set all ninja twins to maximum sneaking experience",
        config_key="max_sneaking_exp",
        default_value=False,
        category="Experience Cheats",
        order=9
    )
    async def max_sneaking_exp_ui(self, value: bool = None):
        if value is not None:
            self.config["max_sneaking_exp"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector and value:
                try:
                    if self.debug:
                        console.print(f"[sneaking_cheats] Setting max sneaking experience")
                    result = await self.max_sneaking_exp(self.injector)
                    if self.debug:
                        console.print(f"[sneaking_cheats] Result: {result}")
                    return f"SUCCESS: {result}"
                except Exception as e:
                    if self.debug:
                        console.print(f"[sneaking_cheats] Error setting max sneaking experience: {e}")
                    return f"ERROR: Error setting max sneaking experience: {str(e)}"
        return f"Max Sneaking Experience {'enabled' if self.config.get('max_sneaking_exp', False) else 'disabled'}"

    @ui_toggle(
        label="🔧 Fix Bricked Character",
        description="⚠️ EMERGENCY FIX: Restore character data to working state (use if cheats broke the game) - This is a nuclear option that completely rebuilds your character data",
        config_key="fix_bricked_character",
        default_value=False,
        category="⚠️ Emergency Fixes",
        order=10
    )
    async def fix_bricked_character_ui(self, value: bool = None):
        if value is not None:
            self.config["fix_bricked_character"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector and value:
                try:
                    if self.debug:
                        console.print(f"[sneaking_cheats] Fixing bricked character")
                    result = await self.fix_bricked_character(self.injector)
                    if self.debug:
                        console.print(f"[sneaking_cheats] Result: {result}")
                    return f"SUCCESS: {result}"
                except Exception as e:
                    if self.debug:
                        console.print(f"[sneaking_cheats] Error fixing bricked character: {e}")
                    return f"ERROR: Error fixing bricked character: {str(e)}"
        return f"Fix Bricked Character {'enabled' if self.config.get('fix_bricked_character', False) else 'disabled'}"

    @ui_toggle(
        label="🎯 Initialize Sneaking Game",
        description="⚠️ FIRST-TIME SETUP: Set up initial sneaking game state (use if you have no floor UI or player is NULL) - This sets up basic game data without nuking everything",
        config_key="initialize_sneaking",
        default_value=False,
        category="⚠️ Emergency Fixes",
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

    @ui_toggle(
        label="🥷 Add Max Ninjas",
        description="Add all 12 ninja twins with max levels",
        config_key="add_max_ninjas",
        default_value=False,
        category="Ninja Management",
        order=12
    )
    async def add_max_ninjas_ui(self, value: bool = None):
        if value is not None:
            self.config["add_max_ninjas"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector and value:
                try:
                    if self.debug:
                        console.print(f"[sneaking_cheats] Adding max ninjas")
                    result = await self.add_max_ninjas(self.injector)
                    if self.debug:
                        console.print(f"[sneaking_cheats] Result: {result}")
                    return f"SUCCESS: {result}"
                except Exception as e:
                    if self.debug:
                        console.print(f"[sneaking_cheats] Error adding max ninjas: {e}")
                    return f"ERROR: Error adding max ninjas: {str(e)}"
        return f"Add Max Ninjas {'enabled' if self.config.get('add_max_ninjas', False) else 'disabled'}"

    @ui_toggle(
        label="➕ Add Single Ninja",
        description="Add one ninja twin with specified level",
        config_key="add_single_ninja",
        default_value=False,
        category="Ninja Management",
        order=13
    )
    async def add_single_ninja_ui(self, value: bool = None):
        if value is not None:
            self.config["add_single_ninja"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector and value:
                try:
                    if self.debug:
                        console.print(f"[sneaking_cheats] Adding single ninja")
                    result = await self.add_single_ninja(self.injector)
                    if self.debug:
                        console.print(f"[sneaking_cheats] Result: {result}")
                    return f"SUCCESS: {result}"
                except Exception as e:
                    if self.debug:
                        console.print(f"[sneaking_cheats] Error adding single ninja: {e}")
                    return f"ERROR: Error adding single ninja: {str(e)}"
        return f"Add Single Ninja {'enabled' if self.config.get('add_single_ninja', False) else 'disabled'}"

    @ui_toggle(
        label="🗑️ Delete All Ninjas",
        description="Remove all ninja twins",
        config_key="delete_all_ninjas",
        default_value=False,
        category="Ninja Management",
        order=14
    )
    async def delete_all_ninjas_ui(self, value: bool = None):
        if value is not None:
            self.config["delete_all_ninjas"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector and value:
                try:
                    if self.debug:
                        console.print(f"[sneaking_cheats] Deleting all ninjas")
                    result = await self.delete_all_ninjas(self.injector)
                    if self.debug:
                        console.print(f"[sneaking_cheats] Result: {result}")
                    return f"SUCCESS: {result}"
                except Exception as e:
                    if self.debug:
                        console.print(f"[sneaking_cheats] Error deleting all ninjas: {e}")
                    return f"ERROR: Error deleting all ninjas: {str(e)}"
        return f"Delete All Ninjas {'enabled' if self.config.get('delete_all_ninjas', False) else 'disabled'}"

    @ui_toggle(
        label="🎭 Spawn Ninja Actors",
        description="Spawn ninja actors on the game board (visual)",
        config_key="spawn_ninja_actors",
        default_value=False,
        category="Ninja Management",
        order=15
    )
    async def spawn_ninja_actors_ui(self, value: bool = None):
        if value is not None:
            self.config["spawn_ninja_actors"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector and value:
                try:
                    if self.debug:
                        console.print(f"[sneaking_cheats] Spawning ninja actors")
                    result = await self.spawn_ninja_actors(self.injector)
                    if self.debug:
                        console.print(f"[sneaking_cheats] Result: {result}")
                    return f"SUCCESS: {result}"
                except Exception as e:
                    if self.debug:
                        console.print(f"[sneaking_cheats] Error spawning ninja actors: {e}")
                    return f"ERROR: Error spawning ninja actors: {str(e)}"
        return f"Spawn Ninja Actors {'enabled' if self.config.get('spawn_ninja_actors', False) else 'disabled'}"



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
            output += "<div style='font-weight: bold; font-size: 16px; margin-bottom: 10px;'>🥷 SNEAKING GAME STATUS</div>";
            
            const jadeCoins = ninja[102] ? ninja[102][1] || 0 : 0;
            const currentFloor = ninja[102] ? ninja[102][0] || 0 : 0;
            const floorsUnlocked = ninjaInfo[3] ? ninjaInfo[3].length : 0;
            const ninjaTwins = ninja.length > 0 ? ninja.length : 0;
            
            output += "<div style='margin: 10px 0; padding: 10px; background: rgba(0, 0, 0, 0.1); border-radius: 5px;'>";
            output += "<div style='font-weight: bold; margin-bottom: 5px;'>💰 MONEY & PROGRESS</div>";
            output += "<div>Jade Coins: " + jadeCoins.toLocaleString() + "</div>";
            output += "<div>Current Floor: " + currentFloor + "</div>";
            output += "<div>Total Floors: " + floorsUnlocked + "</div>";
            output += "<div>Ninja Twins: " + ninjaTwins + "</div>";
            output += "</div>";
            
            if (ninjaInfo[3] && ninjaInfo[3].length > 0) {
                output += "<div style='margin: 10px 0; padding: 10px; background: rgba(0, 0, 0, 0.1); border-radius: 5px;'>";
                output += "<div style='font-weight: bold; margin-bottom: 5px;'>🏢 FLOORS</div>";
                
                const filterQuery = filter_query ? filter_query.toLowerCase() : "";
                
                for (let i = 0; i < ninjaInfo[3].length; i++) {
                    const floorName = ninjaInfo[3][i] || "Unknown Floor " + (i + 1);
                    const isUnlocked = i <= currentFloor;
                    const status = isUnlocked ? "🟢 UNLOCKED" : "🔒 LOCKED";
                    
                    if (!filterQuery || floorName.toLowerCase().includes(filterQuery)) {
                        output += "<div style='margin: 2px 0; padding: 3px 8px; background: " + (isUnlocked ? "rgba(107, 207, 127, 0.1)" : "rgba(255, 107, 107, 0.1)") + "; border-left: 3px solid " + (isUnlocked ? "#6bcf7f" : "#ff6b6b") + ";'>";
                        output += floorName + " | " + status + "</div>";
                    }
                }
                output += "</div>";
            }
            
            if (ninja.length > 0) {
                output += "<div style='margin: 10px 0; padding: 10px; background: rgba(0, 0, 0, 0.1); border-radius: 5px;'>";
                output += "<div style='font-weight: bold; margin-bottom: 5px;'>🥷 NINJA TWINS</div>";
                
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
            
            return `💰 Set Jade Coins to maximum: ${newAmount.toLocaleString()} (was ${oldAmount.toLocaleString()})`;
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
            
            return `🏢 Unlocked all ${totalFloors} sneaking floors! (Set current floor to ${totalFloors - 1})`;
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
            
            return `⚡ Maxed ${upgradedCount} sneaking upgrades!`;
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
            
            return `🥷 Unlocked ${unlockedCount} ninja equipment items!`;
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
            
            return `💰 Added ${amount.toLocaleString()} Jade Coins! New total: ${newAmount.toLocaleString()}`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def infinite_stealth_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const ninja = bEngine.getGameAttribute("Ninja");
            
            if (!ninja) {
                return "Error: Ninja data not found";
            }
            
            let stealthSetCount = 0;
            
            for (let i = 0; i < ninja.length; i++) {
                const ninjaData = ninja[i];
                if (ninjaData && Array.isArray(ninjaData) && ninjaData.length > 2) {
                    ninjaData[2] = 999;
                    stealthSetCount++;
                }
            }
            
            return `🥷 Set infinite stealth for ${stealthSetCount} ninja twins! (No detection chance)`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def max_sneaking_exp_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const ninja = bEngine.getGameAttribute("Ninja");
            
            if (!ninja) {
                return "Error: Ninja data not found";
            }
            
            let expSetCount = 0;
            
            for (let i = 0; i < ninja.length; i++) {
                const ninjaData = ninja[i];
                if (ninjaData && Array.isArray(ninjaData) && ninjaData.length > 1) {
                    ninjaData[0] = 999;
                    ninjaData[1] = 999999999;
                    expSetCount++;
                }
            }
            
            return `📈 Set max sneaking experience for ${expSetCount} ninja twins!`;
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
            
            return `🎯 INITIALIZED: Set up ${initializedCount} sneaking game arrays and spawned ninja actors! Game should now be functional with UI and visible ninjas.`;
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
            
            return `🥷 Added ${addedCount} ninja twins with max levels!`;
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
            
            return `➕ Added ninja twin #${ninjaIndex + 1} with level 50!`;
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
            
            return `🗑️ Deleted ${deletedCount} ninja twins!`;
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
            
            return `🎭 Spawned ${spawnedCount} ninja actors using game logic!`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''



plugin_class = SneakingCheatsPlugin 