from plugin_system import PluginBase, js_export, ui_toggle, ui_search_with_results, plugin_command, ui_autocomplete_input, console
from config_manager import config_manager

class AnvilCheatsPlugin(PluginBase):
    VERSION = "1.0.0"
    DESCRIPTION = "Comprehensive cheats for the crafting anvil (Smithing) system including free recipes, storage crafting, and anvil upgrades."

    def __init__(self, config=None):
        super().__init__(config or {})
        self.name = 'anvil_cheats'
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
        category="Recipe Cheats",
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
        category="Anvil Upgrades",
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
        category="Anvil Upgrades",
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
        label="Max Anvil Level",
        description="Set a specific anvil to maximum level",
        button_text="Max Level",
        placeholder="Enter anvil name (e.g., 'Anvil1', 'Anvil2')",
        category="Anvil Upgrades",
        order=8
    )
    async def max_anvil_level_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[anvil_cheats] Maxing anvil level, input: {value}")
                
                if not value or not value.strip():
                    return "Please provide an anvil name (e.g., 'Anvil1', 'Anvil2')"
                
                result = await self.max_anvil_level(value.strip())
                if self.debug:
                    console.print(f"[anvil_cheats] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[anvil_cheats] Error maxing anvil level: {e}")
                return f"ERROR: Error maxing anvil level: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    def get_max_anvil_level_ui_autocomplete(self, query: str = None) -> list:
        if not hasattr(self, 'injector') or not self.injector:
            return []
        
        try:
            if self.debug:
                console.print(f"[anvil_cheats] Getting autocomplete for query: {query}")
            
            anvil_names = [
                "Anvil1", "Anvil2", "Anvil3", "Anvil4", "Anvil5",
                "Anvil6", "Anvil7", "Anvil8", "Anvil9", "Anvil10"
            ]
            
            if query:
                query_lower = query.lower()
                filtered_names = [name for name in anvil_names if query_lower in name.lower()]
            else:
                filtered_names = anvil_names[:5]
            
            if self.debug:
                console.print(f"[anvil_cheats] Autocomplete found {len(filtered_names)} anvils")
            
            return filtered_names[:10]
        except Exception as e:
            if self.debug:
                console.print(f"[anvil_cheats] Error in autocomplete: {e}")
            return []

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
        help="Max a specific anvil level.",
        params=[
            {"name": "anvil_name", "type": str, "help": "Name of the anvil to max (e.g., 'Anvil1')"},
        ],
    )
    async def max_anvil_level(self, anvil_name: str, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('max_anvil_level_js', self.injector, anvil_name=anvil_name)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["filter_query"])
    def get_anvil_status_js(self, filter_query=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const anvilStats = bEngine.getGameAttribute("AnvilPAstats");
            const itemToCraftName = bEngine.getGameAttribute("CustomLists").h.ItemToCraftNAME;
            const itemToCraftCost = bEngine.getGameAttribute("CustomLists").h.ItemToCraftCostTYPE;
            const itemToCraftExp = bEngine.getGameAttribute("CustomLists").h.ItemToCraftEXP;
            
            if (!anvilStats || !itemToCraftName) {
                return "Error: Anvil data not found";
            }
            
            let output = "";
            output += "<div style='font-weight: bold; font-size: 16px; margin-bottom: 10px;'>🔨 ANVIL STATUS</div>";
            
            const filterQuery = filter_query ? filter_query.toLowerCase() : "";
            
            output += "<div style='margin: 10px 0; padding: 10px; background: rgba(0, 0, 0, 0.1); border-radius: 5px;'>";
            output += "<div style='font-weight: bold; margin-bottom: 5px;'>⚒️ ANVIL LEVELS</div>";
            
            for (let i = 0; i < anvilStats.length; i++) {
                const anvilLevel = anvilStats[i] || 0;
                const anvilName = `Anvil${i + 1}`;
                
                if (!filterQuery || anvilName.toLowerCase().includes(filterQuery)) {
                    const status = anvilLevel >= 100 ? "🟢 MAX" : anvilLevel > 0 ? "🟡 LEVELED" : "🔒 LOCKED";
                    const bgColor = anvilLevel >= 100 ? "rgba(107, 207, 127, 0.1)" : anvilLevel > 0 ? "rgba(255, 217, 61, 0.1)" : "rgba(255, 107, 107, 0.1)";
                    const borderColor = anvilLevel >= 100 ? "#6bcf7f" : anvilLevel > 0 ? "#ffd93d" : "#ff6b6b";
                    
                    output += "<div style='margin: 2px 0; padding: 3px 8px; background: " + bgColor + "; border-left: 3px solid " + borderColor + ";'>";
                    output += anvilName + " | Level: " + anvilLevel + " | " + status + "</div>";
                }
            }
            output += "</div>";
            
            if (itemToCraftName && itemToCraftName.length > 0) {
                output += "<div style='margin: 10px 0; padding: 10px; background: rgba(0, 0, 0, 0.1); border-radius: 5px;'>";
                output += "<div style='font-weight: bold; margin-bottom: 5px;'>📋 RECIPE TABS</div>";
                
                let totalRecipes = 0;
                let unlockedRecipes = 0;
                
                for (let tabIndex = 0; tabIndex < itemToCraftName.length; tabIndex++) {
                    const tabRecipes = itemToCraftName[tabIndex];
                    if (tabRecipes && tabRecipes.length > 0) {
                        const tabName = `Smithing Tab ${tabIndex + 1}`;
                        
                        if (!filterQuery || tabName.toLowerCase().includes(filterQuery)) {
                            output += "<div style='margin: 5px 0; padding: 5px; background: rgba(255, 255, 255, 0.05); border-radius: 3px;'>";
                            output += "<div style='font-weight: bold;'>" + tabName + " (" + tabRecipes.length + " recipes)</div>";
                            
                            for (let recipeIndex = 0; recipeIndex < Math.min(tabRecipes.length, 5); recipeIndex++) {
                                const recipeId = tabRecipes[recipeIndex];
                                const recipeExp = itemToCraftExp && itemToCraftExp[tabIndex] ? itemToCraftExp[tabIndex][recipeIndex] || 0 : 0;
                                const isUnlocked = recipeExp > 0;
                                
                                if (isUnlocked) unlockedRecipes++;
                                totalRecipes++;
                                
                                const status = isUnlocked ? "🟢 UNLOCKED" : "🔒 LOCKED";
                                output += "<div style='margin: 1px 0; padding: 2px 5px; font-size: 12px;'>";
                                output += "Recipe " + (recipeIndex + 1) + " | EXP: " + recipeExp + " | " + status + "</div>";
                            }
                            
                            if (tabRecipes.length > 5) {
                                output += "<div style='margin: 1px 0; padding: 2px 5px; font-size: 12px; color: #888;'>";
                                output += "... and " + (tabRecipes.length - 5) + " more recipes</div>";
                            }
                            
                            output += "</div>";
                        }
                    }
                }
                
                output += "<div style='margin-top: 10px; padding: 8px; background: rgba(0, 0, 0, 0.1); border-radius: 3px;'>";
                output += "<div style='font-weight: bold;'>📊 SUMMARY</div>";
                output += "<div>Total Recipes: " + totalRecipes + "</div>";
                output += "<div>Unlocked: " + unlockedRecipes + "/" + totalRecipes + " (" + Math.round(unlockedRecipes/totalRecipes*100) + "%)</div>";
                output += "</div>";
                
                output += "</div>";
            }
            
            return output;
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

    @js_export()
    def max_anvil_level_js(self, anvil_name=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const anvilStats = bEngine.getGameAttribute("AnvilPAstats");
            
            if (!anvilStats) {
                return "Error: Anvil stats not found";
            }
            
            if (!anvil_name || !anvil_name.trim()) {
                return "Error: No anvil name provided";
            }
            
            const anvilMatch = anvil_name.match(/Anvil(\\d+)/i);
            if (!anvilMatch) {
                return "Error: Invalid anvil name format. Use 'Anvil1', 'Anvil2', etc.";
            }
            
            const anvilIndex = parseInt(anvilMatch[1]) - 1;
            if (anvilIndex < 0 || anvilIndex >= anvilStats.length) {
                return `Error: Anvil index ${anvilIndex + 1} out of range (1-${anvilStats.length})`;
            }
            
            const oldLevel = anvilStats[anvilIndex] || 0;
            anvilStats[anvilIndex] = 100;
            
            return `🔨 ${anvil_name} leveled to maximum! (was ${oldLevel}, now 100)`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

plugin_class = AnvilCheatsPlugin 