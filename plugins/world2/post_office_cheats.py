from typing import Dict, Any
from plugin_system import plugin_command, js_export, PluginBase, console, ui_toggle, ui_button, ui_slider, ui_select, ui_search_with_results, ui_autocomplete_input
from config_manager import config_manager

class PostOfficeCheatsPlugin(PluginBase):
    VERSION = "1.0.2"
    DESCRIPTION = "Post Office cheats - complete orders and manage upgrades with detailed status"
    PLUGIN_ORDER = 5
    CATEGORY = "World 2"

    def __init__(self, config=None):
        super().__init__(config or {})
        self.injector = None
        self.name = 'post_office_cheats'
        self.debug = config_manager.get_path('plugin_configs.post_office_cheats.debug', False)
        self._upgrade_cache = None
        self._cache_timestamp = 0
        self._cache_duration = 300

    async def cleanup(self) -> None:
        pass

    async def update(self) -> None:
        if self.config.get('free_order_completion', False) and hasattr(self, 'injector') and self.injector:
            try:
                self.run_js_export('apply_free_order_completion_js', self.injector)
            except Exception as e:
                if self.debug:
                    console.print(f"[post_office_cheats] Error in update loop: {e}")

    async def on_config_changed(self, config: Dict[str, Any]) -> None:
        self.debug = config_manager.get_path('plugin_configs.post_office_cheats.debug', False)
        if self.debug:
            console.print(f"[post_office_cheats] Config changed: {config}")
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)

    async def on_game_ready(self) -> None:
        pass

    @ui_toggle(
        label="Debug Mode",
        description="Enable debug logging for post office plugin",
        config_key="debug",
        default_value=False
    )
    async def enable_debug(self, value: bool = None):
        if value is not None:
            self.config["debug"] = value
            self.save_to_global_config()
        return f"Debug mode {'enabled' if self.config.get('debug', False) else 'disabled'}"

    @ui_search_with_results(
        label="Post Office Status",
        description="Show all post office upgrades with their levels and current orders",
        button_text="Show Status",
        placeholder="Enter filter term (leave empty to show all)",
    )
    async def post_office_status_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[post_office_cheats] Getting post office status, filter: {value}")
                result = self.run_js_export('get_post_office_status_js', self.injector, filter_query=value or "")
                return result
            except Exception as e:
                if self.debug:
                    console.print(f"[post_office_cheats] Error getting status: {e}")
                return f"ERROR: Error getting post office status: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first"

    @ui_autocomplete_input(
        label="Set Upgrade Level",
        description="Set a specific upgrade to a specific level. Syntax: 'upgrade_name level' (e.g., 'damage 100' or 'Bigger Damage 200')",
        button_text="Set Level",
        placeholder="Enter: upgrade_name level (e.g., 'damage 100')",
        category="Upgrade Management"
    )
    async def set_upgrade_level_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[post_office_cheats] Setting upgrade level, input: {value}")
                
                if not value or not value.strip():
                    return "Please provide upgrade name and level (e.g., 'damage 100')"
                
                parts = value.strip().split()
                if len(parts) < 2:
                    return "Syntax: 'upgrade_name level' (e.g., 'damage 100')"
                
                level_str = parts[-1]
                upgrade_name = ' '.join(parts[:-1])
                
                if self.debug:
                    console.print(f"[post_office_cheats] Parsed - upgrade_name: '{upgrade_name}', level: {level_str}")
                
                try:
                    level_int = int(level_str)
                    if level_int < 0:
                        return "Level must be 0 or higher"
                except ValueError:
                    return "Level must be a valid number"
                
                result = await self.set_upgrade_level(upgrade_name, level_int)
                if self.debug:
                    console.print(f"[post_office_cheats] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[post_office_cheats] Error setting upgrade level: {e}")
                return f"ERROR: Error setting upgrade level: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first"

    @ui_autocomplete_input(
        label="Reset Specific Upgrade",
        description="Reset a specific upgrade to level 0. Enter upgrade name only.",
        button_text="Reset Upgrade",
        placeholder="Enter upgrade name (e.g., 'damage')",
        category="Upgrade Management"
    )
    async def reset_specific_upgrade_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[post_office_cheats] Resetting upgrade, input: {value}")
                
                if not value or not value.strip():
                    return "Please provide upgrade name (e.g., 'damage')"
                
                upgrade_name = value.strip()
                
                result = await self.set_upgrade_level(upgrade_name, 0)
                if self.debug:
                    console.print(f"[post_office_cheats] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[post_office_cheats] Error resetting upgrade: {e}")
                return f"ERROR: Error resetting upgrade: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first"

    @ui_button(
        label="Reset All Upgrades",
        description="Reset all post office upgrades to level 0",
        category="Upgrade Management"
    )
    async def reset_all_upgrades_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.reset_all_upgrades(self.injector)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "ERROR: No injector available - run 'inject' first"

    @ui_button(
        label="Max All Upgrades",
        description="Max out all post office upgrades",
        category="Upgrade Management"
    )
    async def max_all_upgrades_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.max_all_upgrades(self.injector)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "ERROR: No injector available - run 'inject' first"

    @ui_button(
        label="Complete All Orders",
        description="Complete all available post office orders",
        category="Order Management"
    )
    async def complete_all_orders_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.complete_all_orders(self.injector)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "ERROR: No injector available - run 'inject' first"

    @ui_button(
        label="Refresh Orders",
        description="Refresh all post office orders",
        category="Order Management"
    )
    async def refresh_orders_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.refresh_orders(self.injector)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "ERROR: No injector available - run 'inject' first"

    @ui_toggle(
        label="Free Order Completion",
        description="Set all order requirements to zero, allowing manual completion without materials",
        config_key="free_order_completion",
        default_value=False,
        category="Order Management"
    )
    async def free_order_completion_ui(self, value: bool = None):
        if value is not None:
            self.config["free_order_completion"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                try:
                    result = self.run_js_export('set_free_order_completion_js', self.injector, enabled=value)
                    return f"SUCCESS: {result}"
                except Exception as e:
                    return f"ERROR: {str(e)}"
        return f"Free order completion: {'enabled' if self.config.get('free_order_completion', False) else 'disabled'}"



    @ui_select(
        label="Complete Order Type",
        description="Choose which type of orders to complete",
        config_key="order_type",
        default_value="all",
        options=[
            {"value": "all", "label": "All Orders"},
            {"value": "easy", "label": "Easy Orders Only"},
            {"value": "medium", "label": "Medium Orders Only"},
            {"value": "hard", "label": "Hard Orders Only"}
        ],
        category="Order Management"
    )
    async def set_order_type_ui(self, value: str = None):
        if value is not None:
            self.config["order_type"] = value
            self.save_to_global_config()
        return f"Order type: {self.config.get('order_type', 'all')}"

    @plugin_command(
        help="Get post office status showing all upgrades and their levels",
        params=[]
    )
    async def get_post_office_status(self, injector=None, **kwargs):
        if self.debug:
            console.print("[post_office_cheats] Getting post office status...")
        return self.run_js_export('get_post_office_status_js', injector)

    @js_export(params=["filter_query"])
    def get_post_office_status_js(self, filter_query=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const engine = ctx["com.stencyl.Engine"].engine;
            const postOfficeInfo = engine.getGameAttribute("PostOfficeInfo");
            const customLists = engine.getGameAttribute("CustomLists");
            
            if (!postOfficeInfo || !postOfficeInfo[3]) {
                return "Error: Post office data not found";
            }
            
            const upgrades = postOfficeInfo[3];
            const upgradeInfo = customLists?.h?.PostOffUpgradeInfo;
            
            if (!upgradeInfo) {
                return "Error: Upgrade info not found";
            }
            
            let output = "";
            output += "<div style='font-weight: bold; font-size: 16px; margin-bottom: 10px;'>📮 POST OFFICE UPGRADES STATUS</div>";
            
            let total_upgrades = 0;
            let unlocked_upgrades = 0;
            let max_leveled_upgrades = 0;
            
            const locked = [];
            const unlocked = [];
            const max_leveled = [];
            
            for (let i = 0; i < upgrades.length; i++) {
                const upgrade = upgrades[i];
                if (!upgrade) continue;
                
                total_upgrades++;
                const upgradeName = upgradeInfo[i]?.[0] || `Upgrade ${i}`;
                const currentLevel = Math.floor(upgrade[0] || 0);
                const maxLevel = Math.floor(upgradeInfo[i]?.[15] || 100);
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
            return `Error: ${e.message}`;
        }
        '''

    @plugin_command(
        help="Set a specific upgrade to a specific level",
        params=[
            {"name": "upgrade_name", "type": str, "help": "Name of the upgrade"},
            {"name": "level", "type": int, "help": "Level to set (0 or higher)"},
        ]
    )
    async def set_upgrade_level(self, upgrade_name: str, level: int, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('set_upgrade_level_js', self.injector, upgradeName=upgrade_name, level=level)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first"

    @js_export(params=["upgradeName", "level"])
    def set_upgrade_level_js(self, upgradeName, level):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const engine = ctx["com.stencyl.Engine"].engine;
            const postOfficeInfo = engine.getGameAttribute("PostOfficeInfo");
            const customLists = engine.getGameAttribute("CustomLists");
            
            if (!postOfficeInfo || !customLists) {
                return "Error: Post office data not found";
            }
            
            const upgradeName = arguments[0];
            const targetLevel = Math.floor(parseInt(arguments[1]) || 0);
            
            let upgradeIndex = -1;
            const upgradeInfo = customLists.h.PostOffUpgradeInfo;
            
            for (let i = 0; i < upgradeInfo.length; i++) {
                if (upgradeInfo[i] && upgradeInfo[i][0] === upgradeName) {
                    upgradeIndex = i;
                    break;
                }
            }
            
            if (upgradeIndex === -1) {
                return `Error: Upgrade '${upgradeName}' not found`;
            }
            
            let currentTotalLevels = 0;
            if (postOfficeInfo[3]) {
                for (let i = 0; i < postOfficeInfo[3].length; i++) {
                    const upgrade = postOfficeInfo[3][i];
                    if (upgrade && upgrade[0]) {
                        currentTotalLevels += Math.floor(upgrade[0]);
                    }
                }
            }
            
            const currentLevel = postOfficeInfo[3] && postOfficeInfo[3][upgradeIndex] ? Math.floor(postOfficeInfo[3][upgradeIndex][0] || 0) : 0;
            const levelDifference = targetLevel - currentLevel;
            
            const newTotalLevels = currentTotalLevels + levelDifference;
            
            const currentTotalEarned = postOfficeInfo[1] && postOfficeInfo[1][0] ? Math.floor(postOfficeInfo[1][0][2] || 0) : 0;
            const boxesToAdd = Math.max(0, newTotalLevels - currentTotalEarned);
            const newTotalEarned = currentTotalEarned + boxesToAdd;
            
            if (postOfficeInfo[1] && postOfficeInfo[1][0]) {
                postOfficeInfo[1][0][2] = newTotalEarned;
                postOfficeInfo[1][0][0] = newTotalEarned;
            }
            
            const currenciesOwned = engine.getGameAttribute("CurrenciesOwned");
            if (currenciesOwned) {
                currenciesOwned.h.DeliveryBoxComplete = newTotalEarned;
            }
            
            if (postOfficeInfo[3] && postOfficeInfo[3][upgradeIndex]) {
                postOfficeInfo[3][upgradeIndex][0] = targetLevel;
            }
            
            const finalTotalEarned = postOfficeInfo[1] && postOfficeInfo[1][0] ? Math.floor(postOfficeInfo[1][0][2] || 0) : 0;
            const availableBoxes = finalTotalEarned - newTotalLevels;
            return `Successfully set ${upgradeName} to level ${targetLevel}. Available boxes: ${availableBoxes}`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @plugin_command(
        help="Get list of upgrade names for autocomplete",
        params=[]
    )
    async def get_upgrade_names(self, injector=None, **kwargs):
        result = self.run_js_export('get_upgrade_names_js', injector)
        return result

    @js_export()
    def get_upgrade_names_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const engine = ctx["com.stencyl.Engine"].engine;
            const postOfficeInfo = engine.getGameAttribute("PostOfficeInfo");
            const customLists = engine.getGameAttribute("CustomLists");
            
            if (!postOfficeInfo || !postOfficeInfo[3]) {
                return "Error: Post office data not found";
            }
            
            const upgrades = postOfficeInfo[3];
            const upgradeInfo = customLists?.h?.PostOffUpgradeInfo;
            
            if (!upgradeInfo) {
                return "Error: Upgrade info not found";
            }
            
            let output = "Upgrade | Level | Max Level | Status\\n";
            output += "--------|-------|-----------|--------\\n";
            
            let found_upgrades = 0;
            for (let i = 0; i < upgradeInfo.length; i++) {
                const upgrade = upgradeInfo[i];
                if (!upgrade || !upgrade[0]) continue;
                
                const upgradeName = upgrade[0];
                const currentLevel = Math.floor(upgrades[i]?.[0] || 0);
                const maxLevel = Math.floor(upgrade[15] || 100);
                const isUnlocked = currentLevel > 0;
                const isMaxLeveled = currentLevel >= maxLevel;
                
                let status = "🔒 LOCKED";
                if (isMaxLeveled) {
                    status = "🟢 MAX LEVEL";
                } else if (isUnlocked) {
                    status = "🟡 UNLOCKED";
                }
                
                output += upgradeName + " | " + currentLevel + " | " + maxLevel + " | " + status + "\\n";
                found_upgrades++;
            }
            
            return output;
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @plugin_command(
        help="Get current orders with details",
        params=[]
    )
    async def get_current_orders(self, injector=None, **kwargs):
        if self.debug:
            console.print("[post_office_cheats] Getting current orders...")
        return self.run_js_export('get_current_orders_js', injector)

    @js_export(params=["filter_query"])
    def get_current_orders_js(self, filter_query=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const engine = ctx["com.stencyl.Engine"].engine;
            const postOfficeInfo = engine.getGameAttribute("PostOfficeInfo");
            
            if (!postOfficeInfo || !postOfficeInfo[0]) {
                return "Error: Post office orders not found";
            }
            
            const orders = postOfficeInfo[0];
            const stats = postOfficeInfo[1];
            const rewards = postOfficeInfo[2];
            
            let output = "";
            output += "<div style='font-weight: bold; font-size: 16px; margin-bottom: 10px;'>📦 CURRENT ORDERS</div>";
            
            let available_orders = 0;
            let completed_orders = 0;
            
            const available = [];
            const completed = [];
            
            for (let i = 0; i < orders.length; i++) {
                const order = orders[i];
                if (!order) continue;
                
                const itemName = order[0] || "Unknown";
                const itemAmount = order[1] || 0;
                const isCompleted = order[2] === 1;
                const reward = rewards[i];
                const stat = stats[i];
                
                const orderInfo = {
                    index: i,
                    itemName: itemName,
                    itemAmount: itemAmount,
                    isCompleted: isCompleted,
                    reward: reward,
                    stat: stat
                };
                
                if (isCompleted) {
                    completed.push(orderInfo);
                    completed_orders++;
                } else {
                    available.push(orderInfo);
                    available_orders++;
                }
            }
            
            const filterQuery = filter_query ? filter_query.toLowerCase() : "";
            
            if (available.length > 0) {
                const filteredAvailable = available.filter(item => !filterQuery || item.itemName.toLowerCase().includes(filterQuery));
                if (filteredAvailable.length > 0) {
                    output += "<div style='color: #4ecdc4; font-weight: bold; margin: 10px 0 5px 0;'>📦 AVAILABLE (" + filteredAvailable.length + ")</div>";
                    for (const item of filteredAvailable) {
                        const rewardText = item.reward ? ` | Reward: ${item.reward[3] || 0} coins` : "";
                        output += "<div style='margin: 2px 0; padding: 3px 8px; background: rgba(78, 205, 196, 0.1); border-left: 3px solid #4ecdc4;'>" + 
                                 "Slot " + (item.index + 1) + ": " + item.itemName + " x" + item.itemAmount + rewardText + "</div>";
                    }
                }
            }
            
            if (completed.length > 0) {
                const filteredCompleted = completed.filter(item => !filterQuery || item.itemName.toLowerCase().includes(filterQuery));
                if (filteredCompleted.length > 0) {
                    output += "<div style='color: #6bcf7f; font-weight: bold; margin: 10px 0 5px 0;'>✅ COMPLETED (" + filteredCompleted.length + ")</div>";
                    for (const item of filteredCompleted) {
                        const rewardText = item.reward ? ` | Reward: ${item.reward[3] || 0} coins` : "";
                        output += "<div style='margin: 2px 0; padding: 3px 8px; background: rgba(107, 207, 127, 0.1); border-left: 3px solid #6bcf7f;'>" + 
                                 "Slot " + (item.index + 1) + ": " + item.itemName + " x" + item.itemAmount + rewardText + "</div>";
                    }
                }
            }
            
            if (!filterQuery) {
                output += "<div style='margin-top: 15px; padding: 10px; background: rgba(0, 0, 0, 0.1); border-radius: 5px;'>";
                output += "<div style='font-weight: bold; margin-bottom: 5px;'>📊 SUMMARY</div>";
                output += "<div>Total Orders: " + orders.length + "</div>";
                output += "<div>Available: " + available_orders + "</div>";
                output += "<div>Completed: " + completed_orders + "</div>";
                output += "</div>";
            }
            
            return output;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @plugin_command(
        help="Complete all available post office orders",
        params=[]
    )
    async def complete_all_orders(self, injector=None, **kwargs):
        if self.debug:
            console.print("[post_office_cheats] Completing all orders...")
        return self.run_js_export('complete_all_orders_js', injector)

    @js_export()
    def complete_all_orders_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            const engine = ctx["com.stencyl.Engine"].engine;
            const postOfficeInfo = engine.getGameAttribute("PostOfficeInfo");
            
            if (!postOfficeInfo || !postOfficeInfo[0]) {
                return "Post office not available";
            }
            
            let completedCount = 0;
            const orders = postOfficeInfo[0];
            
            for (let i = 0; i < orders.length; i++) {
                const order = orders[i];
                if (order && order[2] === 0) {
                    try {
                        order[2] = 1;
                        completedCount++;
                        
                        if (postOfficeInfo[1] && postOfficeInfo[1][i]) {
                            postOfficeInfo[1][i][0] = (postOfficeInfo[1][i][0] || 0) + 1;
                        }
                    } catch (e) {
                        console.error(`Error completing order ${i}:`, e);
                    }
                }
            }
            
            return `Completed ${completedCount} orders`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @plugin_command(
        help="Refresh all post office orders",
        params=[]
    )
    async def refresh_orders(self, injector=None, **kwargs):
        if self.debug:
            console.print("[post_office_cheats] Refreshing orders...")
        return self.run_js_export('refresh_orders_js', injector)

    @plugin_command(
        help="Set free order completion mode",
        params=[
            {"name": "enabled", "type": bool, "help": "Enable or disable free order completion"},
        ]
    )
    async def set_free_order_completion(self, enabled: bool, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('set_free_order_completion_js', self.injector, enabled=enabled)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first"

    @js_export()
    def refresh_orders_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            const engine = ctx["com.stencyl.Engine"].engine;
            const postOfficeInfo = engine.getGameAttribute("PostOfficeInfo");
            
            if (!postOfficeInfo || !postOfficeInfo[0]) {
                return "Post office not available";
            }
            
            let refreshedCount = 0;
            const orders = postOfficeInfo[0];
            
            for (let i = 0; i < orders.length; i++) {
                try {
                    if (orders[i]) {
                        orders[i][2] = 0;
                        refreshedCount++;
                    }
                } catch (e) {
                    console.error(`Error refreshing order ${i}:`, e);
                }
            }
            
            return `Refreshed ${refreshedCount} orders`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export(params=["enabled"])
    def set_free_order_completion_js(self, enabled):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            const engine = ctx["com.stencyl.Engine"].engine;
            const enabled = arguments[0];
            
            if (!window.__idleon_cheats__) {
                window.__idleon_cheats__ = {};
            }
            
            if (enabled) {
                if (!window.__idleon_cheats__.postOfficeOriginal) {
                    window.__idleon_cheats__.postOfficeOriginal = {};
                }
                
                const postOfficeInfo = engine.getGameAttribute("PostOfficeInfo");
                if (postOfficeInfo && postOfficeInfo[0]) {
                    if (!window.__idleon_cheats__.postOfficeOriginal.orders) {
                        window.__idleon_cheats__.postOfficeOriginal.orders = [];
                    }
                    
                    for (let i = 0; i < postOfficeInfo[0].length; i++) {
                        const order = postOfficeInfo[0][i];
                        if (order && order[2] === 0) {
                            if (!window.__idleon_cheats__.postOfficeOriginal.orders[i]) {
                                window.__idleon_cheats__.postOfficeOriginal.orders[i] = {
                                    itemName: order[0],
                                    requiredAmount: order[1]
                                };
                            }
                            order[1] = 0;
                        }
                    }
                }
                
                return "Free order completion enabled - all order requirements set to zero";
            } else {
                const postOfficeInfo = engine.getGameAttribute("PostOfficeInfo");
                if (postOfficeInfo && postOfficeInfo[0] && window.__idleon_cheats__.postOfficeOriginal.orders) {
                    for (let i = 0; i < window.__idleon_cheats__.postOfficeOriginal.orders.length; i++) {
                        const original = window.__idleon_cheats__.postOfficeOriginal.orders[i];
                        if (original && postOfficeInfo[0][i]) {
                            postOfficeInfo[0][i][1] = original.requiredAmount;
                        }
                    }
                }
                
                return "Free order completion disabled - requirements restored";
            }
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def apply_free_order_completion_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            const engine = ctx["com.stencyl.Engine"].engine;
            
            if (!window.__idleon_cheats__ || !window.__idleon_cheats__.postOfficeOriginal) {
                return;
            }
            
            const postOfficeInfo = engine.getGameAttribute("PostOfficeInfo");
            if (postOfficeInfo && postOfficeInfo[0]) {
                for (let i = 0; i < postOfficeInfo[0].length; i++) {
                    const order = postOfficeInfo[0][i];
                    if (order && order[2] === 0) {
                        if (!window.__idleon_cheats__.postOfficeOriginal.orders[i]) {
                            window.__idleon_cheats__.postOfficeOriginal.orders[i] = {
                                itemName: order[0],
                                requiredAmount: order[1]
                            };
                        }
                        order[1] = 0;
                    }
                }
            }
        } catch (e) {
            console.error("Error in apply_free_order_completion_js:", e);
        }
        '''

    @plugin_command(
        help="Max out all post office upgrades",
        params=[]
    )
    async def max_all_upgrades(self, injector=None, **kwargs):
        if self.debug:
            console.print("[post_office_cheats] Maxing all upgrades...")
        return self.run_js_export('max_all_upgrades_js', injector)

    @js_export()
    def max_all_upgrades_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const engine = ctx["com.stencyl.Engine"].engine;
            const postOfficeInfo = engine.getGameAttribute("PostOfficeInfo");
            const customLists = engine.getGameAttribute("CustomLists");
            
            if (!postOfficeInfo || !customLists) {
                return "Error: Post office data not found";
            }
            
            const upgradeInfo = customLists.h.PostOffUpgradeInfo;
            if (!upgradeInfo) {
                return "Error: Upgrade info not found";
            }
            
            let totalUpgradeLevels = 0;
            let upgradeDetails = [];
            for (let i = 0; i < upgradeInfo.length; i++) {
                const upgrade = upgradeInfo[i];
                if (upgrade && upgrade[15]) {
                    const maxLevel = Math.floor(upgrade[15]);
                    const upgradeName = upgrade[0] || `Upgrade ${i}`;
                    totalUpgradeLevels += maxLevel;
                    upgradeDetails.push(`${upgradeName}: ${maxLevel}`);
                }
            }
            
            let currentTotalLevels = 0;
            if (postOfficeInfo[3]) {
                for (let i = 0; i < postOfficeInfo[3].length; i++) {
                    const upgrade = postOfficeInfo[3][i];
                    if (upgrade && upgrade[0]) {
                        currentTotalLevels += Math.floor(upgrade[0]);
                    }
                }
            }
            
            const currentTotalEarned = postOfficeInfo[1] && postOfficeInfo[1][0] ? Math.floor(postOfficeInfo[1][0][2] || 0) : 0;
            const boxesToAdd = Math.max(0, totalUpgradeLevels - currentTotalEarned);
            const newTotalEarned = currentTotalEarned + boxesToAdd;
            
            if (postOfficeInfo[1] && postOfficeInfo[1][0]) {
                postOfficeInfo[1][0][2] = newTotalEarned;
                postOfficeInfo[1][0][0] = newTotalEarned;
            }
            
            const currenciesOwned = engine.getGameAttribute("CurrenciesOwned");
            if (currenciesOwned) {
                currenciesOwned.h.DeliveryBoxComplete = newTotalEarned;
            }
            
            engine.setGameAttribute("PostOfficeInfo", postOfficeInfo);
            if (currenciesOwned) {
                engine.setGameAttribute("CurrenciesOwned", currenciesOwned);
            }
            
            if (postOfficeInfo[3]) {
                for (let i = 0; i < upgradeInfo.length; i++) {
                    const upgrade = upgradeInfo[i];
                    if (upgrade && upgrade[15] && postOfficeInfo[3][i]) {
                        const maxLevel = Math.floor(upgrade[15]);
                        postOfficeInfo[3][i][0] = maxLevel;
                    }
                }
            }
            
            const finalTotalEarned = postOfficeInfo[1] && postOfficeInfo[1][0] ? Math.floor(postOfficeInfo[1][0][2] || 0) : 0;
            const availableBoxes = finalTotalEarned - totalUpgradeLevels;
            
            return `Successfully maxed all upgrades. Available boxes: ${availableBoxes}`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''



    @plugin_command(
        help="Get post office status and information",
        params=[]
    )
    async def get_status(self, injector=None, **kwargs):
        if self.debug:
            console.print("[post_office_cheats] Getting status...")
        return self.run_js_export('get_status_js', injector)

    @js_export()
    def get_status_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            const engine = ctx["com.stencyl.Engine"].engine;
            const postOfficeInfo = engine.getGameAttribute("PostOfficeInfo");
            
            if (!postOfficeInfo) {
                return "Post office not available";
            }
            
            const orders = postOfficeInfo[0] || [];
            const stats = postOfficeInfo[1] || [];
            const rewards = postOfficeInfo[2] || [];
            const upgrades = postOfficeInfo[3] || [];
            
            let availableOrders = 0;
            let completedOrders = 0;
            
            for (let i = 0; i < orders.length; i++) {
                if (orders[i] && orders[i][2] === 0) {
                    availableOrders++;
                } else if (orders[i] && orders[i][2] === 1) {
                    completedOrders++;
                }
            }
            
            let totalUpgradePoints = 0;
            for (let i = 0; i < upgrades.length; i++) {
                if (upgrades[i]) {
                    totalUpgradePoints += upgrades[i][0] || 0;
                }
            }
            
            let totalCompletedOrders = 0;
            for (let i = 0; i < stats.length; i++) {
                if (stats[i]) {
                    totalCompletedOrders += stats[i][0] || 0;
                }
            }
            
            return `Orders: ${availableOrders} available, ${completedOrders} completed. Upgrade points: ${totalUpgradePoints}`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @plugin_command(
        help="Reset all post office upgrades to level 0",
        params=[]
    )
    async def reset_all_upgrades(self, injector=None, **kwargs):
        if self.debug:
            console.print("[post_office_cheats] Resetting all upgrades...")
        return self.run_js_export('reset_all_upgrades_js', injector)

    @js_export()
    def reset_all_upgrades_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const engine = ctx["com.stencyl.Engine"].engine;
            const postOfficeInfo = engine.getGameAttribute("PostOfficeInfo");
            
            if (!postOfficeInfo) {
                return "Error: Post office data not found";
            }
            
            if (postOfficeInfo[3]) {
                for (let i = 0; i < postOfficeInfo[3].length; i++) {
                    if (postOfficeInfo[3][i]) {
                        postOfficeInfo[3][i][0] = 0;
                    }
                }
            }
            
            if (postOfficeInfo[1] && postOfficeInfo[1][0]) {
                postOfficeInfo[1][0][2] = 0;
                postOfficeInfo[1][0][0] = 0;
                postOfficeInfo[1][0][1] = Math.max(0, postOfficeInfo[1][0][1] || 0);
            }
            
            const currenciesOwned = engine.getGameAttribute("CurrenciesOwned");
            if (currenciesOwned) {
                currenciesOwned.h.DeliveryBoxComplete = 0;
                currenciesOwned.h.DeliveryBoxStreak = 0;
            }
            
            return "Successfully reset all upgrades to level 0.";
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @plugin_command(
        help="Reset a specific upgrade to level 0",
        params=[
            {"name": "upgrade_name", "type": str, "help": "Name of the upgrade to reset"},
        ]
    )
    async def reset_specific_upgrade(self, upgrade_name: str, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('set_upgrade_level_js', self.injector, upgradeName=upgrade_name, level=0)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first"

    async def get_cached_upgrade_list(self):
        import time
        if (not hasattr(self, '_upgrade_cache') or 
            not hasattr(self, '_cache_timestamp') or 
            not hasattr(self, '_cache_duration') or
            time.time() - self._cache_timestamp > self._cache_duration):
            
            if self.debug:
                console.print("[post_office_cheats] Cache expired or missing, fetching upgrade list...")
            try:
                if not hasattr(self, 'injector') or not self.injector:
                    if self.debug:
                        console.print("[post_office_cheats] No injector available")
                    return []
                
                raw_result = self.run_js_export('get_upgrade_names_js', self.injector)
                if self.debug:
                    console.print(f"[post_office_cheats] Raw JS result: {raw_result}")
                
                if not raw_result or raw_result.startswith("Error:"):
                    if self.debug:
                        console.print(f"[post_office_cheats] No valid result from JS: {raw_result}")
                    return []
                
                upgrade_items = []
                lines = raw_result.strip().split('\n')
                if self.debug:
                    console.print(f"[post_office_cheats] Processing {len(lines)} lines")
                
                for line in lines:
                    line = line.strip()
                    if line and '|' in line:
                        parts = line.split('|')
                        if len(parts) >= 2:
                            name = parts[0].strip()
                            if name and name != "Upgrade":
                                upgrade_items.append(name)
                                if self.debug:
                                    console.print(f"[post_office_cheats] Added upgrade item: {name}")
                
                self._upgrade_cache = upgrade_items
                self._cache_timestamp = time.time()
                self._cache_duration = 300
                if self.debug:
                    console.print(f"[post_office_cheats] Cached {len(upgrade_items)} upgrade items")
                return upgrade_items
            except Exception as e:
                if self.debug:
                    console.print(f"[post_office_cheats] Error fetching upgrade list: {e}")
                return []
        else:
            if self.debug:
                console.print(f"[post_office_cheats] Using cached upgrade list ({len(self._upgrade_cache)} items)")
            return self._upgrade_cache

    async def get_set_upgrade_level_ui_autocomplete(self, query: str = ""):
        if self.debug:
            console.print(f"[post_office_cheats] get_set_upgrade_level_ui_autocomplete called with query: '{query}'")
        try:
            if not hasattr(self, 'injector') or not self.injector:
                if self.debug:
                    console.print("[post_office_cheats] No injector available for autocomplete")
                return []
            
            upgrade_items = await self.get_cached_upgrade_list()
            if self.debug:
                console.print(f"[post_office_cheats] Got {len(upgrade_items)} upgrade items from cache")
            
            if not upgrade_items:
                if self.debug:
                    console.print("[post_office_cheats] No upgrade items found")
                return []
            
            query_lower = query.lower()
            suggestions = []
            
            for item in upgrade_items:
                if query_lower in item.lower():
                    suggestions.append(item)
                    if self.debug:
                        console.print(f"[post_office_cheats] Added suggestion: {item}")
            
            if self.debug:
                console.print(f"[post_office_cheats] Returning {len(suggestions)} suggestions: {suggestions}")
            return suggestions[:10]
        except Exception as e:
            if self.debug:
                console.print(f"[post_office_cheats] Error in get_set_upgrade_level_ui_autocomplete: {e}")
            return []

    async def get_reset_specific_upgrade_ui_autocomplete(self, query: str = ""):
        if self.debug:
            console.print(f"[post_office_cheats] get_reset_specific_upgrade_ui_autocomplete called with query: '{query}'")
        try:
            if not hasattr(self, 'injector') or not self.injector:
                if self.debug:
                    console.print("[post_office_cheats] No injector available for autocomplete")
                return []
            
            upgrade_items = await self.get_cached_upgrade_list()
            if self.debug:
                console.print(f"[post_office_cheats] Got {len(upgrade_items)} upgrade items from cache")
            
            if not upgrade_items:
                if self.debug:
                    console.print("[post_office_cheats] No upgrade items found")
                return []
            
            query_lower = query.lower()
            suggestions = []
            
            for item in upgrade_items:
                if query_lower in item.lower():
                    suggestions.append(item)
                    if self.debug:
                        console.print(f"[post_office_cheats] Added suggestion: {item}")
            
            if self.debug:
                console.print(f"[post_office_cheats] Returning {len(suggestions)} suggestions: {suggestions}")
            return suggestions[:10]
        except Exception as e:
            if self.debug:
                console.print(f"[post_office_cheats] Error in get_reset_specific_upgrade_ui_autocomplete: {e}")
            return []

    @plugin_command(
        help="Debug function to show all post office values",
        params=[]
    )
    async def debug_post_office_values(self, injector=None, **kwargs):
        if self.debug:
            console.print("[post_office_cheats] Getting debug values...")
        return self.run_js_export('debug_post_office_values_js', injector)

    @js_export()
    def debug_post_office_values_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const engine = ctx["com.stencyl.Engine"].engine;
            const postOfficeInfo = engine.getGameAttribute("PostOfficeInfo");
            
            if (!postOfficeInfo) {
                return "Error: Post office data not found";
            }
            
            let output = "";
            output += "<div style='font-weight: bold; font-size: 16px; margin-bottom: 10px;'>🔍 POST OFFICE DEBUG VALUES</div>";
            
            output += "<div style='color: #4ecdc4; font-weight: bold; margin: 10px 0 5px 0;'>📦 POSTOFFICEINFO[0] - CURRENT ORDERS</div>";
            if (postOfficeInfo[0]) {
                for (let i = 0; i < postOfficeInfo[0].length; i++) {
                    const order = postOfficeInfo[0][i];
                    if (order) {
                        output += `<div style='margin: 2px 0; padding: 3px 8px; background: rgba(78, 205, 196, 0.1);'>`;
                        output += `Order ${i}: Item=${order[0] || 'null'}, Amount=${order[1] || 'null'}, Completed=${order[2] || 'null'}`;
                        output += "</div>";
                    }
                }
            } else {
                output += "<div style='color: #ff6b6b;'>No orders data</div>";
            }
            
            output += "<div style='color: #ffd93d; font-weight: bold; margin: 10px 0 5px 0;'>📊 POSTOFFICEINFO[1] - ORDER STATISTICS</div>";
            if (postOfficeInfo[1]) {
                for (let i = 0; i < postOfficeInfo[1].length; i++) {
                    const stat = postOfficeInfo[1][i];
                    if (stat) {
                        output += `<div style='margin: 2px 0; padding: 3px 8px; background: rgba(255, 217, 61, 0.1);'>`;
                        output += `Stat ${i}: Completed=${stat[0] || 'null'}, Streak=${stat[1] || 'null'}, TotalEarned=${stat[2] || 'null'}`;
                        output += "</div>";
                    }
                }
            } else {
                output += "<div style='color: #ff6b6b;'>No stats data</div>";
            }
            
            output += "<div style='color: #6bcf7f; font-weight: bold; margin: 10px 0 5px 0;'>🎁 POSTOFFICEINFO[2] - ORDER REWARDS</div>";
            if (postOfficeInfo[2]) {
                for (let i = 0; i < postOfficeInfo[2].length; i++) {
                    const reward = postOfficeInfo[2][i];
                    if (reward) {
                        output += `<div style='margin: 2px 0; padding: 3px 8px; background: rgba(107, 207, 127, 0.1);'>`;
                        output += `Reward ${i}: Coins=${reward[3] || 'null'}, Items=${reward[4] || 'null'}, ${reward[5] || 'null'}`;
                        output += "</div>";
                    }
                }
            } else {
                output += "<div style='color: #ff6b6b;'>No rewards data</div>";
            }
            
            output += "<div style='color: #a855f7; font-weight: bold; margin: 10px 0 5px 0;'>🔧 POSTOFFICEINFO[3] - UPGRADE LEVELS</div>";
            if (postOfficeInfo[3]) {
                let totalUpgradeLevels = 0;
                for (let i = 0; i < postOfficeInfo[3].length; i++) {
                    const upgrade = postOfficeInfo[3][i];
                    if (upgrade) {
                        const level = Math.floor(upgrade[0] || 0);
                        totalUpgradeLevels += level;
                        output += `<div style='margin: 2px 0; padding: 3px 8px; background: rgba(168, 85, 247, 0.1);'>`;
                        output += `Upgrade ${i}: Level=${level}`;
                        output += "</div>";
                    }
                }
                output += `<div style='margin: 5px 0; padding: 5px 8px; background: rgba(168, 85, 247, 0.2); font-weight: bold;'>`;
                output += `TOTAL UPGRADE LEVELS: ${totalUpgradeLevels}`;
                output += "</div>";
            } else {
                output += "<div style='color: #ff6b6b;'>No upgrades data</div>";
            }
            
            let totalEarned = 0;
            let totalLevels = 0;
            
            if (postOfficeInfo[1] && postOfficeInfo[1][0]) {
                totalEarned = Math.floor(postOfficeInfo[1][0][2] || 0);
            }
            
            if (postOfficeInfo[3]) {
                for (let i = 0; i < postOfficeInfo[3].length; i++) {
                    const upgrade = postOfficeInfo[3][i];
                    if (upgrade && upgrade[0]) {
                        totalLevels += Math.floor(upgrade[0]);
                    }
                }
            }
            
            const availableBoxes = totalEarned - totalLevels;
            
            output += "<div style='margin-top: 15px; padding: 10px; background: rgba(0, 0, 0, 0.1); border-radius: 5px;'>";
            output += "<div style='font-weight: bold; margin-bottom: 5px;'>🧮 CALCULATION</div>";
            output += `<div>Total Boxes Earned: ${totalEarned}</div>`;
            output += `<div>Total Upgrade Levels: ${totalLevels}</div>`;
            output += `<div>Available Boxes: ${totalEarned} - ${totalLevels} = ${availableBoxes}</div>`;
            output += "</div>";
            
            output += "<div style='margin-top: 15px; padding: 10px; background: rgba(255, 107, 107, 0.1); border-radius: 5px;'>";
            output += "<div style='font-weight: bold; margin-bottom: 5px;'>🎮 GAME'S ACTUAL CALCULATION</div>";
            
            try {
                const gameEngine = engine;
                if (gameEngine && typeof gameEngine._customBlock_PostOfficeINFO === 'function') {
                    const gameAvailablePoints = gameEngine._customBlock_PostOfficeINFO("AvailablePoints", 0, "a");
                    output += `<div>Game's AvailablePoints: ${gameAvailablePoints}</div>`;
                } else {
                    output += "<div>Game's AvailablePoints function not found</div>";
                }
            } catch (e) {
                output += `<div>Error calling game's function: ${e.message}</div>`;
            }
            
            try {
                const currenciesOwned = engine.getGameAttribute("CurrenciesOwned");
                if (currenciesOwned) {
                    output += `<div>DeliveryBoxComplete: ${currenciesOwned.h.DeliveryBoxComplete || 'null'}</div>`;
                    output += `<div>DeliveryBoxStreak: ${currenciesOwned.h.DeliveryBoxStreak || 'null'}</div>`;
                }
            } catch (e) {
                output += `<div>Error checking currencies: ${e.message}</div>`;
            }
            
            output += "</div>";
            
            return output;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @ui_button(
        label="Reset Box Counts",
        description="Reset total earned boxes and completed orders to a reasonable level (1000)",
        category="Configuration"
    )
    async def reset_box_counts_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.reset_box_counts(self.injector)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "ERROR: No injector available - run 'inject' first"

    @plugin_command(
        help="Reset box counts to a reasonable level",
        params=[]
    )
    async def reset_box_counts(self, injector=None, **kwargs):
        if self.debug:
            console.print("[post_office_cheats] Resetting box counts...")
        return self.run_js_export('reset_box_counts_js', injector)

    @js_export()
    def reset_box_counts_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const engine = ctx["com.stencyl.Engine"].engine;
            const postOfficeInfo = engine.getGameAttribute("PostOfficeInfo");
            
            if (!postOfficeInfo) {
                return "Error: Post office data not found";
            }
            
            const reasonableBoxCount = 1000;
            
            if (postOfficeInfo[1] && postOfficeInfo[1][0]) {
                postOfficeInfo[1][0][2] = reasonableBoxCount;
                postOfficeInfo[1][0][0] = reasonableBoxCount;
                postOfficeInfo[1][0][1] = Math.max(0, postOfficeInfo[1][0][1] || 0);
            }
            
            const currenciesOwned = engine.getGameAttribute("CurrenciesOwned");
            if (currenciesOwned) {
                currenciesOwned.h.DeliveryBoxComplete = reasonableBoxCount;
                currenciesOwned.h.DeliveryBoxStreak = reasonableBoxCount;
            }
            
            return `Successfully reset box counts to ${reasonableBoxCount}.`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

plugin_class = PostOfficeCheatsPlugin 