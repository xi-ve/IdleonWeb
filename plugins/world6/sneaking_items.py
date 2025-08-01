from plugin_system import PluginBase, js_export, ui_banner, ui_toggle, ui_search_with_results, plugin_command, ui_autocomplete_input, console, ui_button
from config_manager import config_manager

class SneakingItemsPlugin(PluginBase):
    VERSION = "1.0.1"
    DESCRIPTION = "Comprehensive item cheats for the sneaking game including hats, weapons, gloves, and charms."
    PLUGIN_ORDER = 8
    CATEGORY = "World 6"

    def __init__(self, config=None):
        super().__init__(config or {})        
        self.debug = config.get('debug', False) if config else False
        self._item_cache = None
        self._cache_timestamp = 0
        self._cache_duration = 300
        self.name = 'sneaking_items'

    async def cleanup(self): pass
    async def update(self): pass
    async def on_config_changed(self, config): 
        self.debug = config.get('debug', False)
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)
    async def on_game_ready(self): pass

    @ui_banner(
        label="⚠️ HIGH RISK WARNING",
        description="This plugin is work-in-progress and has a high risk of bricking you permanently! Use at your own risk!",
        banner_type="warning",
        category="Actions",
        order=-100
    )
    async def warning_banner(self):
        return "Warning banner displayed"

    @ui_toggle(
        label="Debug Mode",
        description="Enable debug logging for sneaking items plugin",
        config_key="debug",
        default_value=False
    )
    async def enable_debug(self, value: bool = None):
        if value is not None:
            self.config["debug"] = value
            self.save_to_global_config()
            self.debug = value
        return f"Debug mode {'enabled' if self.config.get('debug', False) else 'disabled'}"

    @ui_button(
        label="Unlock All Sneaking Items",
        description="Unlock all sneaking items (hats, weapons, gloves, charms)",
        category="Actions",
        order=1
    )
    async def unlock_all_items_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.unlock_all_items(self.injector)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: Error unlocking all items: {str(e)}"
        return "Injector not available"

    @ui_button(
        label="Max All Item Levels",
        description="Set all sneaking items to maximum level",
        category="Actions",
        order=2
    )
    async def max_item_levels_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.max_item_levels(self.injector)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: Error maxing item levels: {str(e)}"
        return "Injector not available"

    @ui_button(
        label="Clear All Items",
        description="Remove all sneaking items from inventory",
        category="Actions",
        order=3
    )
    async def clear_all_items_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.clear_all_items(self.injector)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: Error clearing items: {str(e)}"
        return "Injector not available"

    @ui_search_with_results(
        label="Sneaking Items Status",
        description="Show current sneaking items status including hats, weapons, gloves, and charms",
        button_text="Show Items",
        placeholder="Enter filter term (leave empty to show all)"
    )
    async def sneaking_items_status_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[sneaking_items] Getting items status, filter: {value}")
                result = self.run_js_export('get_sneaking_items_status_js', self.injector, filter_query=value or "")
                return result
            except Exception as e:
                if self.debug:
                    console.print(f"[sneaking_items] Error getting items status: {e}")
                return f"ERROR: Error getting items status: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_autocomplete_input(
        label="Give Sneaking Item",
        description="Give a specific sneaking item to your inventory",
        button_text="Give Item",
        placeholder="Enter item name (e.g., 'Straw Hat', 'Wood Nunchaku')"
    )
    async def give_sneaking_item_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[sneaking_items] Giving item, input: {value}")
                
                if not value or not value.strip():
                    return "Please provide an item name (e.g., 'Straw Hat', 'Wood Nunchaku')"
                
                result = await self.give_sneaking_item(value.strip())
                if self.debug:
                    console.print(f"[sneaking_items] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[sneaking_items] Error giving item: {e}")
                return f"ERROR: Error giving item: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    def get_give_sneaking_item_ui_autocomplete(self, query: str = None) -> list:
        if not hasattr(self, 'injector') or not self.injector:
            return []
        
        try:
            if self.debug:
                console.print(f"[sneaking_items] Getting autocomplete for query: {query}")
            
            item_list = self.get_cached_item_list()
            if not item_list:
                return []
            
            if query:
                query_lower = query.lower()
                filtered_items = [item for item in item_list if query_lower in item.lower()]
            else:
                filtered_items = item_list[:20]
            
            if self.debug:
                console.print(f"[sneaking_items] Autocomplete found {len(filtered_items)} items")
            
            return filtered_items[:10]
        except Exception as e:
            if self.debug:
                console.print(f"[sneaking_items] Error in autocomplete: {e}")
            return []

    def get_cached_item_list(self) -> list:
        import time
        current_time = time.time()
        
        if (self._item_cache and 
            current_time - self._cache_timestamp < self._cache_duration):
            return self._item_cache
        
        try:
            result = self.run_js_export('get_sneaking_item_list_js', self.injector)
            if result and isinstance(result, str):
                import re
                items = re.findall(r'^([^|]+)\s*\|', result, re.MULTILINE)
                if items:
                    self._item_cache = [item.strip() for item in items if item.strip()]
                    self._cache_timestamp = current_time
                    if self.debug:
                        console.print(f"[sneaking_items] Cached {len(self._item_cache)} items")
                    return self._item_cache
        except Exception as e:
            if self.debug:
                console.print(f"[sneaking_items] Error fetching item list: {e}")
        
        fallback_items = [
            "Straw Hat", "Wood Nunchaku", "Cloth Gloves", "Lucky Charm",
            "Iron Helmet", "Steel Katana", "Leather Gloves", "Magic Ring",
            "Golden Crown", "Diamond Sword", "Mythril Gauntlets", "Crystal Necklace"
        ]
        self._item_cache = fallback_items
        self._cache_timestamp = current_time
        return fallback_items

    @plugin_command(
        help="Get current sneaking items status.",
        params=[],
    )
    async def get_sneaking_items_status(self, injector=None, **kwargs):
        result = self.run_js_export('get_sneaking_items_status_js', injector)
        return result

    @plugin_command(
        help="Unlock all sneaking items.",
        params=[],
    )
    async def unlock_all_items(self, injector=None, **kwargs):
        result = self.run_js_export('unlock_all_items_js', injector)
        return result

    @plugin_command(
        help="Max level all sneaking items.",
        params=[],
    )
    async def max_item_levels(self, injector=None, **kwargs):
        result = self.run_js_export('max_item_levels_js', injector)
        return result

    @plugin_command(
        help="Give a specific sneaking item.",
        params=[
            {"name": "item_name", "type": str, "help": "Name of the item to give"},
        ],
    )
    async def give_sneaking_item(self, item_name: str, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('give_sneaking_item_js', self.injector, item_name=item_name)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @plugin_command(
        help="Clear all sneaking items.",
        params=[],
    )
    async def clear_all_items(self, injector=None, **kwargs):
        result = self.run_js_export('clear_all_items_js', injector)
        return result

    @js_export(params=["filter_query"])
    def get_sneaking_items_status_js(self, filter_query=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const ninja = bEngine.getGameAttribute("Ninja");
            const ninjaInfo = bEngine.getGameAttribute("CustomLists").h.NinjaInfo;
            const njEQ = bEngine.getGameAttribute("CustomMaps").h.NjEQ;
            
            if (!ninja || !ninjaInfo || !njEQ) {
                return "Error: Sneaking items data not found";
            }
            
            let output = "";
            output += "<div style='font-weight: bold; font-size: 16px; margin-bottom: 10px;'>🥷 SNEAKING ITEMS STATUS</div>";
            
            const filterQuery = filter_query ? filter_query.toLowerCase() : "";
            
            let totalItems = 0;
            let unlockedItems = 0;
            let maxLeveledItems = 0;
            
            const categories = [
                { name: "Hats", prefix: "NjItem", startIndex: 0, endIndex: 15 },
                { name: "Weapons", prefix: "NjWep", startIndex: 0, endIndex: 9 },
                { name: "Gloves", prefix: "NjGl", startIndex: 0, endIndex: 3 },
                { name: "Charms", prefix: "NjTr", startIndex: 0, endIndex: 25 }
            ];
            
            for (const category of categories) {
                const categoryItems = [];
                
                for (let i = category.startIndex; i < category.endIndex; i++) {
                    const itemKey = category.prefix + i;
                    const itemData = njEQ.h[itemKey];
                    
                    if (itemData && Array.isArray(itemData) && itemData.length > 2) {
                        const itemName = itemData[2] || itemKey;
                        let isUnlocked = false;
                        let isMaxLeveled = false;
                        let itemLevel = 0;
                        
                        for (let charIndex = 0; charIndex < 10; charIndex++) {
                            for (let slotIndex = 0; slotIndex < 24; slotIndex++) {
                                const inventoryIndex = 12 + (4 * slotIndex) + (24 * charIndex);
                                const inventorySlot = ninja[inventoryIndex];
                                
                                if (inventorySlot && Array.isArray(inventorySlot) && inventorySlot[0] === itemKey) {
                                    isUnlocked = true;
                                    itemLevel = inventorySlot[1] || 0;
                                    if (itemLevel >= 999) isMaxLeveled = true;
                                    break;
                                }
                            }
                            if (isUnlocked) break;
                        }
                        
                        if (isUnlocked) unlockedItems++;
                        if (isMaxLeveled) maxLeveledItems++;
                        totalItems++;
                        
                        const displayName = itemName.replace(/_/g, ' ');
                        
                        if (!filterQuery || displayName.toLowerCase().includes(filterQuery)) {
                            categoryItems.push({
                                name: displayName,
                                key: itemKey,
                                level: itemLevel,
                                isUnlocked: isUnlocked,
                                isMaxLeveled: isMaxLeveled
                            });
                        }
                    }
                }
                
                if (categoryItems.length > 0) {
                    output += "<div style='margin: 10px 0; padding: 10px; background: rgba(0, 0, 0, 0.1); border-radius: 5px;'>";
                    output += "<div style='font-weight: bold; margin-bottom: 5px;'>" + category.name.toUpperCase() + "</div>";
                    
                    for (const item of categoryItems) {
                        const status = item.isUnlocked ? (item.isMaxLeveled ? "🟢 MAX" : "🟡 UNLOCKED") : "🔒 LOCKED";
                        const bgColor = item.isUnlocked ? (item.isMaxLeveled ? "rgba(107, 207, 127, 0.1)" : "rgba(255, 217, 61, 0.1)") : "rgba(255, 107, 107, 0.1)";
                        const borderColor = item.isUnlocked ? (item.isMaxLeveled ? "#6bcf7f" : "#ffd93d") : "#ff6b6b";
                        
                        output += "<div style='margin: 2px 0; padding: 3px 8px; background: " + bgColor + "; border-left: 3px solid " + borderColor + ";'>";
                        output += item.name + " | Level: " + item.level + " | " + status + "</div>";
                    }
                    output += "</div>";
                }
            }
            
            if (!filterQuery) {
                output += "<div style='margin-top: 15px; padding: 10px; background: rgba(0, 0, 0, 0.1); border-radius: 5px;'>";
                output += "<div style='font-weight: bold; margin-bottom: 5px;'>📊 SUMMARY</div>";
                output += "<div>Total Items: " + totalItems + "</div>";
                output += "<div>Unlocked: " + unlockedItems + "/" + totalItems + " (" + Math.round(unlockedItems/totalItems*100) + "%)</div>";
                output += "<div>Max Leveled: " + maxLeveledItems + "/" + totalItems + " (" + Math.round(maxLeveledItems/totalItems*100) + "%)</div>";
                output += "</div>";
            }
            
            return output;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def unlock_all_items_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const ninja = bEngine.getGameAttribute("Ninja");
            const njEQ = bEngine.getGameAttribute("CustomMaps").h.NjEQ;
            
            if (!ninja || !njEQ) {
                return "Error: Sneaking items data not found";
            }
            
            let unlockedCount = 0;
            const currentChar = 0;
            
            const itemRanges = [
                { prefix: "NjItem", count: 15 },
                { prefix: "NjWep", count: 9 },
                { prefix: "NjGl", count: 3 },
                { prefix: "NjTr", count: 25 }
            ];
            
            for (const range of itemRanges) {
                for (let i = 0; i < range.count; i++) {
                    const itemKey = range.prefix + i;
                    if (njEQ.h[itemKey]) {
                        let foundSlot = -1;
                        
                        for (let slotIndex = 0; slotIndex < 24; slotIndex++) {
                            const inventoryIndex = 12 + (4 * slotIndex) + (24 * currentChar);
                            const inventorySlot = ninja[inventoryIndex];
                            
                            if (inventorySlot && Array.isArray(inventorySlot) && (inventorySlot[0] === "Blank" || !inventorySlot[0])) {
                                foundSlot = inventoryIndex;
                                break;
                            }
                        }
                        
                        if (foundSlot !== -1) {
                            ninja[foundSlot][0] = itemKey;
                            ninja[foundSlot][1] = 1;
                            unlockedCount++;
                        }
                    }
                }
            }
            
            return `🥷 Unlocked ${unlockedCount} sneaking items!`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def max_item_levels_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const ninja = bEngine.getGameAttribute("Ninja");
            
            if (!ninja) {
                return "Error: Ninja data not found";
            }
            
            let maxedCount = 0;
            const currentChar = 0;
            
            for (let slotIndex = 0; slotIndex < 24; slotIndex++) {
                const inventoryIndex = 12 + (4 * slotIndex) + (24 * currentChar);
                const inventorySlot = ninja[inventoryIndex];
                
                if (inventorySlot && Array.isArray(inventorySlot) && inventorySlot.length > 1) {
                    if (inventorySlot[0] && inventorySlot[0] !== "Blank") {
                        if (inventorySlot[1] < 999) {
                            inventorySlot[1] = 999;
                            maxedCount++;
                        }
                    }
                }
            }
            
            return `⚡ Maxed ${maxedCount} sneaking item levels!`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export(params=["item_name"])
    def give_sneaking_item_js(self, item_name=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const ninja = bEngine.getGameAttribute("Ninja");
            const njEQ = bEngine.getGameAttribute("CustomMaps").h.NjEQ;
            
            if (!ninja || !njEQ) {
                return "Error: Sneaking items data not found";
            }
            
            if (!item_name || !item_name.trim()) {
                return "Error: No item name provided";
            }
            
            const searchName = item_name.toLowerCase().replace(/\\s+/g, '_');
            let foundItem = null;
            
            for (const [itemKey, itemData] of Object.entries(njEQ.h)) {
                if (itemData && Array.isArray(itemData) && itemData.length > 2) {
                    const itemDisplayName = itemData[2] || "";
                    if (itemDisplayName.toLowerCase().replace(/\\s+/g, '_').includes(searchName) ||
                        itemKey.toLowerCase().includes(searchName)) {
                        foundItem = itemKey;
                        break;
                    }
                }
            }
            
            if (!foundItem) {
                return `Error: Item '${item_name}' not found. Try searching for partial names like 'Hat', 'Nunchaku', 'Gloves', etc.`;
            }
            
            const currentChar = 0;
            let foundSlot = -1;
            
            for (let slotIndex = 0; slotIndex < 24; slotIndex++) {
                const inventoryIndex = 12 + (4 * slotIndex) + (24 * currentChar);
                const inventorySlot = ninja[inventoryIndex];
                
                if (inventorySlot && Array.isArray(inventorySlot) && (inventorySlot[0] === "Blank" || !inventorySlot[0])) {
                    foundSlot = inventoryIndex;
                    break;
                }
            }
            
            if (foundSlot === -1) {
                return "Error: No empty inventory slots available";
            }
            
            ninja[foundSlot][0] = foundItem;
            ninja[foundSlot][1] = 1;
            
            const itemDisplayName = njEQ.h[foundItem][2] || foundItem;
            return `🎁 Gave ${itemDisplayName} to inventory slot ${foundSlot}!`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def clear_all_items_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const ninja = bEngine.getGameAttribute("Ninja");
            
            if (!ninja) {
                return "Error: Ninja data not found";
            }
            
            let clearedCount = 0;
            const currentChar = 0;
            
            for (let slotIndex = 0; slotIndex < 24; slotIndex++) {
                const inventoryIndex = 12 + (4 * slotIndex) + (24 * currentChar);
                const inventorySlot = ninja[inventoryIndex];
                
                if (inventorySlot && Array.isArray(inventorySlot)) {
                    if (inventorySlot[0] && inventorySlot[0] !== "Blank") {
                        inventorySlot[0] = "Blank";
                        inventorySlot[1] = 0;
                        clearedCount++;
                    }
                }
            }
            
            return `🗑️ Cleared ${clearedCount} sneaking items from inventory!`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def get_sneaking_item_list_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const njEQ = bEngine.getGameAttribute("CustomMaps").h.NjEQ;
            
            if (!njEQ) {
                return "Error: Sneaking item definitions not found";
            }
            
            let itemList = [];
            
            const categories = [
                { name: "Hats", prefix: "NjItem", startIndex: 0, endIndex: 15 },
                { name: "Weapons", prefix: "NjWep", startIndex: 0, endIndex: 9 },
                { name: "Gloves", prefix: "NjGl", startIndex: 0, endIndex: 3 },
                { name: "Charms", prefix: "NjTr", startIndex: 0, endIndex: 25 }
            ];
            
            for (const category of categories) {
                for (let i = category.startIndex; i < category.endIndex; i++) {
                    const itemKey = category.prefix + i;
                    const itemData = njEQ.h[itemKey];
                    
                    if (itemData && Array.isArray(itemData) && itemData.length > 2) {
                        const itemName = itemData[2] || itemKey;
                        if (itemName && itemName !== 'Blank') {
                            const displayName = itemName.replace(/_/g, ' ');
                            itemList.push(displayName);
                        }
                    }
                }
            }
            
            itemList = [...new Set(itemList)].sort();
            
            const formattedList = itemList.map(item => `${item} | Available`).join('\\n');
            
            return formattedList || "No items found";
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

plugin_class = SneakingItemsPlugin 