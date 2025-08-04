import time
from plugin_system import PluginBase, js_export, ui_toggle, ui_search_with_results, plugin_command, ui_autocomplete_input, console, ui_button
from config_manager import config_manager

class AnvilCheatsPlugin(PluginBase):
    VERSION = "1.0.2"
    DESCRIPTION = "Cheats for World 1 - Anvil and Smithing related"
    PLUGIN_ORDER = 1 
    CATEGORY = "World 1"

    def __init__(self, config=None):
        super().__init__(config or {})        
        self.debug = config.get('debug', False) if config else False
        self.name = 'anvil_cheats'
        self.last_update = time.time()

    async def cleanup(self): pass
    async def update(self): 
        self.debug = config_manager.get_path('plugin_configs.anvil_cheats.debug', False)
        if self.last_update < time.time() - 10:
            self.last_update = time.time()
            if hasattr(self, 'injector') and self.injector and config_manager.get_path('plugin_configs.anvil_cheats.free_recipe_costs', False):
                try:
                    result = self.run_js_export('free_recipe_costs_js', self.injector)
                    if self.debug:
                        console.print(f"[anvil_cheats] Result: {result}")
                except Exception as e:
                    if self.debug:
                        console.print(f"[anvil_cheats] Error enabling free recipe costs: {e}")

    async def on_config_changed(self, config): 
        self.debug = config.get('debug', False)
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)
    async def on_game_ready(self): pass

    @ui_toggle(
        label="Debug Mode",
        description="Enable debug logging for anvil cheats plugin",
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
        label="Free Recipe Costs",
        description="Make all smithing recipe costs free (0/0 requirements)",
        config_key="free_recipe_costs",
        default_value=False,
        order=2
    )
    async def free_recipe_costs_ui(self, value: bool = None):
        if value is not None:
            self.config["free_recipe_costs"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector and value:
                try:
                    if self.debug:
                        console.print(f"[anvil_cheats] Enabling free recipe costs")
                    result = await self.free_recipe_costs(self.injector)
                    if self.debug:
                        console.print(f"[anvil_cheats] Result: {result}")
                    return f"SUCCESS: {result}"
                except Exception as e:
                    if self.debug:
                        console.print(f"[anvil_cheats] Error enabling free recipe costs: {e}")
                    return f"ERROR: Error enabling free recipe costs: {str(e)}"
        return f"Free Recipe Costs {'enabled' if self.config.get('free_recipe_costs', False) else 'disabled'}"

    @ui_toggle(
        label="Free Anvil Upgrades",
        description="Make all anvil upgrade costs free",
        config_key="free_anvil_upgrades",
        default_value=False,
        order=3
    )
    async def free_anvil_upgrades_ui(self, value: bool = None):
        if value is not None:
            self.config["free_anvil_upgrades"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector and value:
                try:
                    if self.debug:
                        console.print(f"[anvil_cheats] Enabling free anvil upgrades")
                    result = await self.free_anvil_upgrades(self.injector)
                    if self.debug:
                        console.print(f"[anvil_cheats] Result: {result}")
                    return f"SUCCESS: {result}"
                except Exception as e:
                    if self.debug:
                        console.print(f"[anvil_cheats] Error enabling free anvil upgrades: {e}")
                    return f"ERROR: Error enabling free anvil upgrades: {str(e)}"
        return f"Free Anvil Upgrades {'enabled' if self.config.get('free_anvil_upgrades', False) else 'disabled'}"

    @ui_toggle(
        label="Instant Anvil Production",
        description="Make anvil production instant (no waiting time)",
        config_key="instant_anvil_production",
        default_value=False,
        order=4
    )
    async def instant_anvil_production_ui(self, value: bool = None):
        if value is not None:
            self.config["instant_anvil_production"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector and value:
                try:
                    if self.debug:
                        console.print(f"[anvil_cheats] Enabling instant anvil production")
                    result = await self.instant_anvil_production(self.injector)
                    if self.debug:
                        console.print(f"[anvil_cheats] Result: {result}")
                    return f"SUCCESS: {result}"
                except Exception as e:
                    if self.debug:
                        console.print(f"[anvil_cheats] Error enabling instant anvil production: {e}")
                    return f"ERROR: Error enabling instant anvil production: {str(e)}"
        return f"Instant Anvil Production {'enabled' if self.config.get('instant_anvil_production', False) else 'disabled'}"

    @ui_search_with_results(
        label="Anvil Status",
        description="Show current anvil status including recipes, upgrades, and production",
        button_text="Show Status",
        placeholder="Enter filter term (leave empty to show all)",
        category="Status & Info",
        order=7
    )
    async def anvil_status_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[anvil_cheats] Getting anvil status, filter: {value}")
                result = self.run_js_export('get_anvil_status_js', self.injector, filter_query=value or "")
                return result
            except Exception as e:
                if self.debug:
                    console.print(f"[anvil_cheats] Error getting anvil status: {e}")
                return f"ERROR: Error getting anvil status: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_autocomplete_input(
        label="Unlock Recipe by Name",
        description="Unlock a specific recipe by name, or use 'tab1', 'tab2', 'tab3', or 'all' to unlock entire tabs",
        button_text="Unlock Recipe",
        placeholder="Enter recipe name (e.g., 'IronBar', 'SteelArmor') or 'tab1'/'all'",
        category="Recipe Unlocks",
        order=5
    )
    async def unlock_recipe_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[anvil_cheats] Unlocking recipe: {value}")
                
                if not value or not value.strip():
                    return "Please provide a recipe name, tab (e.g., 'tab1'), or 'all'"
                
                result = await self.unlock_recipe(value.strip())
                if self.debug:
                    console.print(f"[anvil_cheats] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[anvil_cheats] Error unlocking recipe: {e}")
                return f"ERROR: Error unlocking recipe: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    def get_unlock_recipe_ui_autocomplete(self, query: str = None) -> list:
        if not hasattr(self, 'injector') or not self.injector:
            return []
        
        try:
            if self.debug:
                console.print(f"[anvil_cheats] Getting unlock recipe autocomplete for query: {query}")
            
            result = self.run_js_export('get_locked_recipes_js', self.injector)
            if not result or result.startswith("Error:"):
                return ["tab1", "tab2", "tab3", "all"]

            import re
            recipes = re.findall(r'Recipe:\s*([^|]+)', result)
            
            recipe_names = []
            for recipe in recipes:
                clean_name = recipe.strip()
                if clean_name and clean_name != "undefined":
                    recipe_names.append(clean_name)
            
            options = ["all", "tab1", "tab2", "tab3"] + sorted(set(recipe_names))
            
            if query:
                query_lower = query.lower()
                filtered_options = [opt for opt in options if query_lower in opt.lower()]
            else:
                filtered_options = options[:15]
            
            if self.debug:
                console.print(f"[anvil_cheats] Unlock autocomplete found {len(filtered_options)} options")
            
            return filtered_options[:10]
        except Exception as e:
            if self.debug:
                console.print(f"[anvil_cheats] Error in unlock autocomplete: {e}")
            return ["all", "tab1", "tab2", "tab3"]

    @plugin_command(
        help="Get current anvil status.",
        params=[],
    )
    async def get_anvil_status(self, injector=None, **kwargs):
        result = self.run_js_export('get_anvil_status_js', injector)
        return result

    @plugin_command(
        help="Enable free recipe costs.",
        params=[],
    )
    async def free_recipe_costs(self, injector=None, **kwargs):
        result = self.run_js_export('free_recipe_costs_js', injector)
        return result

    @plugin_command(
        help="Enable free anvil upgrades.",
        params=[],
    )
    async def free_anvil_upgrades(self, injector=None, **kwargs):
        result = self.run_js_export('free_anvil_upgrades_js', injector)
        return result

    @plugin_command(
        help="Enable instant anvil production.",
        params=[],
    )
    async def instant_anvil_production(self, injector=None, **kwargs):
        result = self.run_js_export('instant_anvil_production_js', injector)
        return result

    @plugin_command(
        help="Unlock a specific recipe by name, or use 'tab1', 'tab2', 'tab3', or 'all' to unlock entire tabs.",
        params=[
            {"name": "recipe_name", "type": str, "help": "Name of the recipe to unlock (e.g., 'IronBar', 'SteelArmor') or 'tab1'/'all'"},
        ],
    )
    async def unlock_recipe(self, recipe_name: str):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('unlock_recipe_js', self.injector, recipe_name=recipe_name)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_autocomplete_input(
        label="Set Smithing Level",
        description="Set smithing level to a specific value (this affects available points)",
        button_text="Set Level",
        placeholder="Enter level (e.g., '200')",
        category="Points",
        order=1
    )
    async def set_smithing_level_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if not value or not value.strip():
                    return "Please provide a level amount"
                
                try:
                    level = int(value.strip())
                    if level < 0:
                        return "Level must be positive"
                except ValueError:
                    return "Please enter a valid number"
                
                result = self.run_js_export('set_smithing_level_js', self.injector, level=level)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "Injector not available"

    @ui_autocomplete_input(
        label="Set Bonus EXP Points",
        description="Set bonus EXP points to a specific value",
        button_text="Set Points",
        placeholder="Enter points amount (e.g., '1000')",
        category="Points",
        order=2
    )
    async def set_bonus_exp_points_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if not value or not value.strip():
                    return "Please provide a points amount"
                
                try:
                    points = int(value.strip())
                    if points < 0:
                        return "Points amount must be positive"
                except ValueError:
                    return "Please enter a valid number"
                
                result = self.run_js_export('set_bonus_exp_points_js', self.injector, points=points)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "Injector not available"

    @ui_autocomplete_input(
        label="Set Production Speed Points",
        description="Set production speed points to a specific value",
        button_text="Set Points",
        placeholder="Enter points amount (e.g., '1000')",
        category="Points",
        order=3
    )
    async def set_production_speed_points_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if not value or not value.strip():
                    return "Please provide a points amount"
                
                try:
                    points = int(value.strip())
                    if points < 0:
                        return "Points amount must be positive"
                except ValueError:
                    return "Please enter a valid number"
                
                result = self.run_js_export('set_production_speed_points_js', self.injector, points=points)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "Injector not available"

    @ui_autocomplete_input(
        label="Set Capacity Points",
        description="Set capacity points to a specific value",
        button_text="Set Points",
        placeholder="Enter points amount (e.g., '1000')",
        category="Points",
        order=4
    )
    async def set_capacity_points_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if not value or not value.strip():
                    return "Please provide a points amount"
                
                try:
                    points = int(value.strip())
                    if points < 0:
                        return "Points amount must be positive"
                except ValueError:
                    return "Please enter a valid number"
                
                result = self.run_js_export('set_capacity_points_js', self.injector, points=points)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "Injector not available"

    @ui_button(
        label="Reset All Anvil Stats",
        description="Reset all anvil stats and fix negative points",
        category="Points",
        order=0
    )
    async def reset_anvil_stats_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = self.run_js_export('reset_anvil_stats_js', self.injector)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "Injector not available"

    @js_export(params=["filter_query"])
    def get_anvil_status_js(self, filter_query=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const anvilStats = bEngine.getGameAttribute("AnvilPAstats"); // [ Pts , CostUpg1 , CostUpg2 , LvClicksT1 , LvClicksT2 , LvClicksT3 ]
            const itemToCraftName = bEngine.getGameAttribute("CustomLists").h.ItemToCraftNAME;
            const itemToCraftExp = bEngine.getGameAttribute("CustomLists").h.ItemToCraftEXP;
            const anvilCraftStatus = bEngine.getGameAttribute("AnvilCraftStatus");
            const smithLvl = bEngine.getGameAttribute("Lv0")[2] || 0;
            
            if (!Array.isArray(anvilStats) || anvilStats.length < 6) {
                return "Error: AnvilPAstats array not initialised";
            }
            
            let html = "";
            html += `<div style='font-weight:bold;font-size:16px;margin-bottom:10px;'>🔨 ANVIL – PRODUCTION & STATS</div>`;
            
            html += `<div style='margin:10px 0;padding:10px;border:1px solid #666;border-radius:4px;'>`;
            html += `<div style='font-weight:bold;margin-bottom:6px;'>Core Stats</div>`;
            html += `<div>Anvil&nbsp;Points: ${anvilStats[0]}</div>`;
            html += `<div>Bonus&nbsp;EXP&nbsp;Points: ${anvilStats[3]}</div>`;
            html += `<div>Production&nbsp;Speed&nbsp;Points: ${anvilStats[4]}</div>`;
            html += `<div>Capacity&nbsp;Points: ${anvilStats[5]}</div>`;
            html += `<div style='margin-top:6px;color:#888;'>Current Smithing Level: ${smithLvl}</div>`;
            html += `</div>`;
            
            return html;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def free_recipe_costs_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const CList = bEngine.getGameAttribute("CustomLists").h;
            const itemToCraftExp = CList["ItemToCraftEXP"];
            
            if (!itemToCraftExp) {
                return "Error: Recipe data not found";
            }
            
            const size = [];
            for (const [index, element] of Object.entries(itemToCraftExp)) {
                size.push(element.length);
            }
            
            const newReqs = [];
            for (let i = 0; i < size.length; i++) {
                newReqs.push(new Array(size[i]).fill([["Copper", "0"]]));
            }
            
            const tCustomList = ctx["scripts.CustomLists"];
            const originalItemToCraftCostTYPE = tCustomList["ItemToCraftCostTYPE"];
            
            const handler = {
                apply: function (originalFn, context, argumentsList) {
                    return newReqs;
                },
            };
            
            const proxy = new Proxy(originalItemToCraftCostTYPE, handler);
            tCustomList["ItemToCraftCostTYPE"] = proxy;
            
            return `🔨 All smithing recipe costs set to free! (0/0 requirements)`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def free_anvil_upgrades_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const events = function(num) { return ctx["scripts.ActorEvents_" + num]; };
            
            const forgeUpdateCosts = events(12)._customBlock_ForgeUpdateCosts;
            if (!forgeUpdateCosts) {
                return "Error: Forge update function not found";
            }
            
            events(12)._customBlock_ForgeUpdateCosts = function (...argumentsList) {
                return 0;
            };
            
            return `⚒️ All anvil upgrade costs set to free!`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def instant_anvil_production_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const events = function(num) { return ctx["scripts.ActorEvents_" + num]; };
            
            const anvilProduceStats = events(189)._customBlock_AnvilProduceStats;
            if (!anvilProduceStats) {
                return "Error: Anvil produce stats function not found";
            }
            
            events(189)._customBlock_AnvilProduceStats = function (...argumentsList) {
                const t = argumentsList[0];
                if (t === "Costs1" || t === "Costs2") return 0;
                if (t === "ProductionSpeed") return 999999;
                return Reflect.apply(anvilProduceStats, this, argumentsList);
            };
            
            return `⚡ Anvil production set to instant!`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export(params=["recipe_name"])
    def unlock_recipe_js(self, recipe_name=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const playerLevels = bEngine.getGameAttribute("Lv0") || [];
            const currentSmithingLevel = playerLevels[2] || 0;
            const itemToCraftName = bEngine.getGameAttribute("CustomLists").h.ItemToCraftNAME;
            const itemToCraftExp = bEngine.getGameAttribute("CustomLists").h.ItemToCraftEXP;
            const anvilCraftStatus = bEngine.getGameAttribute("AnvilCraftStatus");
            
            if (!itemToCraftName || !itemToCraftExp || !anvilCraftStatus) {
                return "Error: Recipe data not found";
            }
            
            const recipeName = recipe_name;
            console.log("[anvil_cheats] Unlocking recipe: " + recipeName);
            if (!recipeName) {
                return "Error: No recipe name provided";
            }
            
            let message = "Recipe not found or not applicable.";
            let newLevel = currentSmithingLevel;
            let unlockedCount = 0;
            let storageUnlockedCount = 0;
            
            if (recipeName.toLowerCase() === "all") {
                let maxRequiredLevel = 0;
                for (let tab = 0; tab < itemToCraftExp.length; tab++) {
                    const recipes = itemToCraftExp[tab] || [];
                    for (let i = 0; i < recipes.length; i++) {
                        const expArr = recipes[i] || ["0","0"];
                        const reqLvl = Number(expArr[0] || 0);
                        maxRequiredLevel = Math.max(maxRequiredLevel, reqLvl);
                        
                        if (anvilCraftStatus[tab] && anvilCraftStatus[tab][i] !== undefined) {
                            if (anvilCraftStatus[tab][i] === -1) {
                                anvilCraftStatus[tab][i] = 0; // Set to unlocked but not crafted
                                unlockedCount++;
                                storageUnlockedCount++;
                            }
                        }
                    }
                }
                newLevel = Math.max(maxRequiredLevel + 10, currentSmithingLevel);
                playerLevels[2] = newLevel;
                message = `🔓 Set Smithing level to ${newLevel} and unlocked ${unlockedCount} recipes! (${storageUnlockedCount} storage unlocks)`;
            } else if (recipeName.toLowerCase().startsWith("tab")) {
                const tabNumber = parseInt(recipeName.substring(3)) - 1;
                if (tabNumber >= 0 && tabNumber < itemToCraftExp.length) {
                    let maxTabLevel = 0;
                    const recipes = itemToCraftExp[tabNumber] || [];
                    for (let i = 0; i < recipes.length; i++) {
                        const expArr = recipes[i] || ["0","0"];
                        const reqLvl = Number(expArr[0] || 0);
                        maxTabLevel = Math.max(maxTabLevel, reqLvl);
                        
                        if (anvilCraftStatus[tabNumber] && anvilCraftStatus[tabNumber][i] !== undefined) {
                            if (anvilCraftStatus[tabNumber][i] === -1) {
                                anvilCraftStatus[tabNumber][i] = 0; // Set to unlocked but not crafted
                                unlockedCount++;
                                storageUnlockedCount++;
                            }
                        }
                    }
                    newLevel = Math.max(maxTabLevel + 5, currentSmithingLevel);
                    playerLevels[2] = newLevel;
                    message = `🔓 Set Smithing level to ${newLevel} and unlocked ${unlockedCount} recipes in Tab ${tabNumber + 1}! (${storageUnlockedCount} storage unlocks)`;
                } else {
                    message = `Invalid tab number. Available tabs: tab1 to tab${itemToCraftExp.length}`;
                }
            } else {
                let foundRecipe = false;
                let requiredLevel = 0;
                let foundTab = -1;
                let foundIndex = -1;
                let foundName = "";
                
                const searchName = recipeName.toLowerCase();
                for (let tab = 0; tab < itemToCraftName.length; tab++) {
                    const recipes = itemToCraftName[tab] || [];
                    for (let i = 0; i < recipes.length; i++) {
                        const recId = recipes[i];
                        if (recId && recId.toLowerCase().includes(searchName)) {
                            const expArr = itemToCraftExp[tab][i] || ["0","0"];
                            requiredLevel = Number(expArr[0] || 0);
                            foundRecipe = true;
                            foundTab = tab;
                            foundIndex = i;
                            foundName = recId;
                            break;
                        }
                    }
                    if (foundRecipe) break;
                }
                
                if (foundRecipe) {
                    newLevel = Math.max(requiredLevel + 1, currentSmithingLevel);
                    playerLevels[2] = newLevel;
                    
                    // Also unlock the recipe in AnvilCraftStatus
                    if (anvilCraftStatus[foundTab] && anvilCraftStatus[foundTab][foundIndex] !== undefined) {
                        if (anvilCraftStatus[foundTab][foundIndex] === -1) {
                            anvilCraftStatus[foundTab][foundIndex] = 0; // Set to unlocked but not crafted
                            unlockedCount++;
                            storageUnlockedCount++;
                        }
                    }
                    
                    message = `🔓 Set Smithing level to ${newLevel} and unlocked recipe "${foundName}"! (Tab ${foundTab + 1}, Required: ${requiredLevel})`;
                } else {
                    message = `Recipe "${recipeName}" not found. Try using partial names like "copper", "iron", etc.`;
                }
            }
            
            return message;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def reset_anvil_stats_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const anvilStats = bEngine.getGameAttribute("AnvilPAstats");
            
            if (!Array.isArray(anvilStats) || anvilStats.length < 6) {
                return "Error: AnvilPAstats array not initialized";
            }
            
            anvilStats[0] = 0;  // Anvil Points
            anvilStats[1] = 0;  // Cost Reducer Tier 1
            anvilStats[2] = 0;  // Cost Reducer Tier 2
            anvilStats[3] = 0;  // Bonus EXP Points
            anvilStats[4] = 0;  // Production Speed Points
            anvilStats[5] = 0;  // Capacity Points
            
            return `Reset all anvil stats to 0`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export(params=["level"])
    def set_smithing_level_js(self, level=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const playerLevels = bEngine.getGameAttribute("Lv0") || [];
            const oldLevel = playerLevels[2] || 0;
            
            // Set new smithing level
            playerLevels[2] = level;
            
            const anvilStats = bEngine.getGameAttribute("AnvilPAstats");
            if (Array.isArray(anvilStats) && anvilStats.length >= 6) {
                anvilStats[1] = 0;
                anvilStats[2] = 0;
            }
            
            return `Set Smithing level from ${oldLevel} to ${level}`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export(params=["points"])
    def set_bonus_exp_points_js(self, points=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const anvilStats = bEngine.getGameAttribute("AnvilPAstats");
            const playerLevels = bEngine.getGameAttribute("Lv0") || [];
            const currentSmithingLevel = playerLevels[2] || 0;
            
            if (!Array.isArray(anvilStats) || anvilStats.length < 6) {
                return "Error: AnvilPAstats array not initialized";
            }
            
            const oldPoints = anvilStats[3];
            anvilStats[3] = points;
            
            const totalPoints = anvilStats[3] + anvilStats[4] + anvilStats[5];
            const neededLevel = Math.max(currentSmithingLevel, totalPoints);
            playerLevels[2] = neededLevel;
            
            anvilStats[1] = 0;
            anvilStats[2] = 0;

            return `Set Bonus EXP Points from ${oldPoints} to ${points} (Smithing level set to ${neededLevel})`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export(params=["points"])
    def set_production_speed_points_js(self, points=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const anvilStats = bEngine.getGameAttribute("AnvilPAstats");
            const playerLevels = bEngine.getGameAttribute("Lv0") || [];
            const currentSmithingLevel = playerLevels[2] || 0;
            
            if (!Array.isArray(anvilStats) || anvilStats.length < 6) {
                return "Error: AnvilPAstats array not initialized";
            }
            
            const oldPoints = anvilStats[4];
            anvilStats[4] = points;
            
            const totalPoints = anvilStats[3] + anvilStats[4] + anvilStats[5];
            const neededLevel = Math.max(currentSmithingLevel, totalPoints);
            playerLevels[2] = neededLevel;
            
            anvilStats[1] = 0;  // Cost Reducer Tier 1
            anvilStats[2] = 0;  // Cost Reducer Tier 2
            
            return `Set Production Speed Points from ${oldPoints} to ${points} (Smithing level set to ${neededLevel})`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export(params=["points"])
    def set_capacity_points_js(self, points=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const anvilStats = bEngine.getGameAttribute("AnvilPAstats");
            const playerLevels = bEngine.getGameAttribute("Lv0") || [];
            const currentSmithingLevel = playerLevels[2] || 0;
            
            if (!Array.isArray(anvilStats) || anvilStats.length < 6) {
                return "Error: AnvilPAstats array not initialized";
            }
            
            const oldPoints = anvilStats[5];
            anvilStats[5] = points;
            
            const totalPoints = anvilStats[3] + anvilStats[4] + anvilStats[5];
            const neededLevel = Math.max(currentSmithingLevel, totalPoints);
            playerLevels[2] = neededLevel;
            
            anvilStats[1] = 0;  // Cost Reducer Tier 1
            anvilStats[2] = 0;  // Cost Reducer Tier 2
            
            return `Set Capacity Points from ${oldPoints} to ${points} (Smithing level set to ${neededLevel})`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def get_locked_recipes_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const itemToCraftName = bEngine.getGameAttribute("CustomLists").h.ItemToCraftNAME;
            const itemToCraftExp = bEngine.getGameAttribute("CustomLists").h.ItemToCraftEXP;
            const smithLvl = bEngine.getGameAttribute("Lv0")[2] || 0;
            
            if (!itemToCraftName || !itemToCraftExp) {
                return "Error: Recipe data not found";
            }
            
            let lockedRecipes = [];
            for (let tab = 0; tab < itemToCraftName.length; tab++) {
                const recipes = itemToCraftName[tab] || [];
                for (let i = 0; i < recipes.length; i++) {
                    const recId = recipes[i];
                    const expArr = itemToCraftExp?.[tab]?.[i] || ["0","0"];
                    const reqLvl = Number(expArr[0] || 0);
                    
                    if (recId && smithLvl < reqLvl) {
                        lockedRecipes.push(`Recipe: ${recId} | Req Level: ${reqLvl}`);
                    }
                }
            }
            
            if (lockedRecipes.length === 0) {
                return "No recipes are currently locked.";
            }
            
            return lockedRecipes.join(" | ");
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

plugin_class = AnvilCheatsPlugin 