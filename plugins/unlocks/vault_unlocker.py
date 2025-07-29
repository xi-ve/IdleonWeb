from plugin_system import PluginBase, js_export, ui_toggle, ui_search_with_results, plugin_command, ui_autocomplete_input, console
from config_manager import config_manager

class VaultUnlockerPlugin(PluginBase):
    VERSION = "1.0.1"
    DESCRIPTION = "Unlock and manage vault upgrades with category-based controls."
    PLUGIN_ORDER = 1
    CATEGORY = "Unlocks"

    def __init__(self, config=None):
        super().__init__(config or {})
        self.debug = config.get('debug', False) if config else False
        self._vault_cache = None
        self._cache_timestamp = 0
        self._cache_duration = 300
        self.name = 'vault_unlocker'

    async def cleanup(self): pass
    async def update(self): pass
    async def on_config_changed(self, config): 
        self.debug = config.get('debug', False)
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)
    async def on_game_ready(self): pass

    @ui_toggle(
        label="Debug Mode",
        description="Enable debug logging for vault unlocker plugin",
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
        label="Vault Categories Status",
        description="Show all vault categories with their unlock status and levels",
        button_text="Show Vault Status",
        placeholder="Enter filter term (leave empty to show all)",
    )
    async def vault_status_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[vault_unlocker] Getting vault status, filter: {value}")
                result = self.run_js_export('get_vault_status_js', self.injector, filter_query=value or "")
                return result
            except Exception as e:
                if self.debug:
                    console.print(f"[vault_unlocker] Error getting vault status: {e}")
                return f"ERROR: Error getting vault status: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["filter_query"])
    def get_vault_status_js(self, filter_query=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const upgVault = bEngine.getGameAttribute("UpgVault");
            const upgradeVault = bEngine.getGameAttribute("CustomLists").h.UpgradeVault;
            
            if (!upgVault || !upgradeVault) {
                return "Error: Vault data not found";
            }
            
            let output = "";
            output += "<div style='font-weight: bold; font-size: 16px; margin-bottom: 10px;'>🏦 VAULT CATEGORIES STATUS</div>";
            
            let total_categories = 0;
            let unlocked_categories = 0;
            let max_leveled_categories = 0;
            
            const locked = [];
            const unlocked = [];
            const max_leveled = [];
            
            for (let i = 0; i < upgradeVault.length; i++) {
                const category = upgradeVault[i];
                if (!category || !category[0]) continue;
                
                total_categories++;
                const categoryName = category[0].replace(/_/g, ' ');
                const currentLevel = upgVault[i] || 0;
                const maxLevel = category[4] || 0;
                const isUnlocked = currentLevel > 0;
                const isMaxLeveled = currentLevel >= maxLevel;
                
                if (isUnlocked) unlocked_categories++;
                if (isMaxLeveled) max_leveled_categories++;
                
                const item = {
                    name: categoryName,
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
                output += "<div>Total Categories: " + total_categories + "</div>";
                output += "<div>Unlocked: " + unlocked_categories + "/" + total_categories + " (" + Math.round(unlocked_categories/total_categories*100) + "%)</div>";
                output += "<div>Max Leveled: " + max_leveled_categories + "/" + total_categories + " (" + Math.round(max_leveled_categories/total_categories*100) + "%)</div>";
                output += "</div>";
            }
            
            return output;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @ui_autocomplete_input(
        label="Set Vault Item Level",
        description="Set a specific vault item to a specific level. Syntax: 'item_name level' (e.g., 'damage 100' or 'Bigger Damage 200')",
        button_text="Set Level",
        placeholder="Enter: item_name level (e.g., 'damage 100')",
    )
    async def set_vault_item_level_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[vault_unlocker] Setting vault item level, input: {value}")
                
                if not value or not value.strip():
                    return "Please provide item name and level (e.g., 'damage 100')"
                
                parts = value.strip().split()
                if len(parts) < 2:
                    return "Syntax: 'item_name level' (e.g., 'damage 100')"
                
                level_str = parts[-1]
                item_name = ' '.join(parts[:-1])
                
                if self.debug:
                    console.print(f"[vault_unlocker] Parsed - item_name: '{item_name}', level: {level_str}")
                
                try:
                    level_int = int(level_str)
                    if level_int < 0:
                        return "Level must be 0 or higher"
                except ValueError:
                    return "Level must be a valid number"
                
                result = await self.set_vault_item_level(item_name, level_int)
                if self.debug:
                    console.print(f"[vault_unlocker] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[vault_unlocker] Error setting vault item level: {e}")
                return f"ERROR: Error setting vault item level: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    async def get_cached_vault_list(self):
        import time
        if (not hasattr(self, '_vault_cache') or 
            not hasattr(self, '_cache_timestamp') or 
            not hasattr(self, '_cache_duration') or
            time.time() - self._cache_timestamp > self._cache_duration):
            
            if self.debug:
                console.print("[vault_unlocker] Cache expired or missing, fetching vault list...")
            try:
                if not hasattr(self, 'injector') or not self.injector:
                    if self.debug:
                        console.print("[vault_unlocker] No injector available")
                    return []
                
                raw_result = self.run_js_export('get_vault_item_names_js', self.injector)
                if self.debug:
                    console.print(f"[vault_unlocker] Raw JS result: {raw_result}")
                
                if not raw_result or raw_result.startswith("Error:"):
                    if self.debug:
                        console.print(f"[vault_unlocker] No valid result from JS: {raw_result}")
                    return []
                
                vault_items = []
                lines = raw_result.strip().split('\n')
                if self.debug:
                    console.print(f"[vault_unlocker] Processing {len(lines)} lines")
                
                for line in lines:
                    line = line.strip()
                    if line and '|' in line:
                        parts = line.split('|')
                        if len(parts) >= 2:
                            name = parts[0].strip()
                            if name and name != "Category":
                                vault_items.append(name)
                                if self.debug:
                                    console.print(f"[vault_unlocker] Added vault item: {name}")
                
                self._vault_cache = vault_items
                self._cache_timestamp = time.time()
                self._cache_duration = 300
                if self.debug:
                    console.print(f"[vault_unlocker] Cached {len(vault_items)} vault items")
                return vault_items
            except Exception as e:
                if self.debug:
                    console.print(f"[vault_unlocker] Error fetching vault list: {e}")
                return []
        else:
            if self.debug:
                console.print(f"[vault_unlocker] Using cached vault list ({len(self._vault_cache)} items)")
            return self._vault_cache

    async def get_set_vault_item_level_ui_autocomplete(self, query: str = ""):
        if self.debug:
            console.print(f"[vault_unlocker] get_set_vault_item_level_ui_autocomplete called with query: '{query}'")
        try:
            if not hasattr(self, 'injector') or not self.injector:
                if self.debug:
                    console.print("[vault_unlocker] No injector available for autocomplete")
                return []
            
            vault_items = await self.get_cached_vault_list()
            if self.debug:
                console.print(f"[vault_unlocker] Got {len(vault_items)} vault items from cache")
            
            if not vault_items:
                if self.debug:
                    console.print("[vault_unlocker] No vault items found")
                return []
            
            query_lower = query.lower()
            suggestions = []
            
            for item in vault_items:
                if query_lower in item.lower():
                    suggestions.append(item)
                    if self.debug:
                        console.print(f"[vault_unlocker] Added suggestion: {item}")
            
            if self.debug:
                console.print(f"[vault_unlocker] Returning {len(suggestions)} suggestions: {suggestions}")
            return suggestions[:10]
        except Exception as e:
            if self.debug:
                console.print(f"[vault_unlocker] Error in get_set_vault_item_level_ui_autocomplete: {e}")
            return []

    @ui_toggle(
        label="Unlock All Vault Categories",
        description="Unlock all vault categories (does not level them up)",
        config_key="unlock_all_categories",
        default_value=False,
    )
    async def unlock_all_categories_ui(self, value: bool = None):
        if value is not None:
            self.config["unlock_all_categories"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector and value:
                try:
                    result = await self.unlock_all_vault_categories(self.injector)
                    return f"SUCCESS: {result}"
                except Exception as e:
                    return f"ERROR: Error unlocking vault categories: {str(e)}"
        return f"Unlock all vault categories {'enabled' if self.config.get('unlock_all_categories', False) else 'disabled'}"

    @ui_toggle(
        label="Max Level All Vault Categories",
        description="Set all vault categories to maximum level",
        config_key="max_level_all_categories",
        default_value=False,
    )
    async def max_level_all_categories_ui(self, value: bool = None):
        if value is not None:
            self.config["max_level_all_categories"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector and value:
                try:
                    result = await self.max_level_all_vault_categories(self.injector)
                    return f"SUCCESS: {result}"
                except Exception as e:
                    return f"ERROR: Error max leveling vault categories: {str(e)}"
        return f"Max level all vault categories {'enabled' if self.config.get('max_level_all_categories', False) else 'disabled'}"

    @ui_toggle(
        label="Reset All Vault Categories",
        description="Reset all vault categories to level 0",
        config_key="reset_all_categories",
        default_value=False,
    )
    async def reset_all_categories_ui(self, value: bool = None):
        if value is not None:
            self.config["reset_all_categories"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector and value:
                try:
                    result = await self.reset_all_vault_categories(self.injector)
                    return f"SUCCESS: {result}"
                except Exception as e:
                    return f"ERROR: Error resetting vault categories: {str(e)}"
        return f"Reset all vault categories {'enabled' if self.config.get('reset_all_categories', False) else 'disabled'}"

    @plugin_command(
        help="Get vault status showing all categories and their levels.",
        params=[],
    )
    async def get_vault_status(self, injector=None, **kwargs):
        result = self.run_js_export('get_vault_status_js', injector)
        return result

    @plugin_command(
        help="Set a specific vault item to a specific level.",
        params=[
            {"name": "item_name", "type": str, "help": "Name of the vault item"},
            {"name": "level", "type": int, "help": "Level to set (0 or higher)"},
        ],
    )
    async def set_vault_item_level(self, item_name: str, level: int, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('set_vault_item_level_js', self.injector, item_name=item_name, level=level)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["item_name", "level"])
    def set_vault_item_level_js(self, item_name=None, level=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const upgVault = bEngine.getGameAttribute("UpgVault");
            const upgradeVault = bEngine.getGameAttribute("CustomLists").h.UpgradeVault;
            
            if (!upgVault || !upgradeVault) {
                return "Error: Vault data not found";
            }
            
            if (!item_name || level === undefined || level === null) {
                return "Error: Item name and level are required";
            }
            
            if (level < 0) {
                return "Error: Level must be 0 or higher";
            }
            
            let found_index = -1;
            let found_name = "";
            const search_name = item_name.toLowerCase().replace(/[^a-z0-9]/g, '');
            
            for (let i = 0; i < upgradeVault.length; i++) {
                const category = upgradeVault[i];
                if (!category || !category[0]) continue;
                
                const categoryName = category[0].replace(/_/g, ' ');
                const clean_name = categoryName.toLowerCase().replace(/[^a-z0-9]/g, '');
                
                if (clean_name.includes(search_name) || search_name.includes(clean_name)) {
                    found_index = i;
                    found_name = categoryName;
                    break;
                }
            }
            
            if (found_index === -1) {
                return `Error: Vault item '${item_name}' not found`;
            }
            
            const maxLevel = upgradeVault[found_index][4] || 0;
            const oldLevel = upgVault[found_index] || 0;
            
            if (level > maxLevel) {
                return `Error: Level ${level} exceeds maximum level ${maxLevel} for '${found_name}'`;
            }
            
            upgVault[found_index] = level;
            
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

    @plugin_command(
        help="Get list of vault item names for autocomplete.",
        params=[],
    )
    async def get_vault_item_names(self, injector=None, **kwargs):
        result = self.run_js_export('get_vault_item_names_js', injector)
        return result

    @js_export()
    def get_vault_item_names_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const upgVault = bEngine.getGameAttribute("UpgVault");
            const upgradeVault = bEngine.getGameAttribute("CustomLists").h.UpgradeVault;
            
            if (!upgVault || !upgradeVault) {
                return "Error: Vault data not found";
            }
            
            let output = "Category | Level | Max Level | Status\\n";
            output += "---------|-------|-----------|--------\\n";
            
            let found_categories = 0;
            for (let i = 0; i < upgradeVault.length; i++) {
                const category = upgradeVault[i];
                if (!category || !category[0]) continue;
                
                const categoryName = category[0].replace(/_/g, ' ');
                const currentLevel = upgVault[i] || 0;
                const maxLevel = category[4] || 0;
                const isUnlocked = currentLevel > 0;
                const isMaxLeveled = currentLevel >= maxLevel;
                
                let status = "🔒 LOCKED";
                if (isMaxLeveled) {
                    status = "🟢 MAX LEVEL";
                } else if (isUnlocked) {
                    status = "🟡 UNLOCKED";
                }
                
                output += categoryName + " | " + currentLevel + " | " + maxLevel + " | " + status + "\\n";
                found_categories++;
            }
            
            return output;
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @plugin_command(
        help="Unlock all vault categories (sets level to 1, does not max level).",
        params=[],
    )
    async def unlock_all_vault_categories(self, injector=None, **kwargs):
        result = self.run_js_export('unlock_all_vault_categories_js', injector)
        return result

    @js_export()
    def unlock_all_vault_categories_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const upgVault = bEngine.getGameAttribute("UpgVault");
            const upgradeVault = bEngine.getGameAttribute("CustomLists").h.UpgradeVault;
            
            if (!upgVault || !upgradeVault) {
                return "Error: Vault data not found";
            }
            
            let unlocked_count = 0;
            let already_unlocked = 0;
            
            for (let i = 0; i < upgradeVault.length; i++) {
                const category = upgradeVault[i];
                if (!category || !category[0]) continue;
                
                const categoryName = category[0].replace(/_/g, ' ');
                const currentLevel = upgVault[i] || 0;
                
                if (currentLevel === 0) {
                    upgVault[i] = 1;
                    unlocked_count++;
                } else {
                    already_unlocked++;
                }
            }
            
            if (unlocked_count === 0) {
                return `✅ All vault categories are already unlocked! (${already_unlocked} categories)`;
            } else {
                return `🔓 Unlocked ${unlocked_count} vault categories! (${already_unlocked} were already unlocked)`;
            }
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @plugin_command(
        help="Set all vault categories to maximum level.",
        params=[],
    )
    async def max_level_all_vault_categories(self, injector=None, **kwargs):
        result = self.run_js_export('max_level_all_vault_categories_js', injector)
        return result

    @js_export()
    def max_level_all_vault_categories_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const upgVault = bEngine.getGameAttribute("UpgVault");
            const upgradeVault = bEngine.getGameAttribute("CustomLists").h.UpgradeVault;
            
            if (!upgVault || !upgradeVault) {
                return "Error: Vault data not found";
            }
            
            let max_leveled_count = 0;
            let already_max_leveled = 0;
            
            for (let i = 0; i < upgradeVault.length; i++) {
                const category = upgradeVault[i];
                if (!category || !category[0]) continue;
                
                const categoryName = category[0].replace(/_/g, ' ');
                const currentLevel = upgVault[i] || 0;
                const maxLevel = category[4] || 0;
                
                if (currentLevel < maxLevel) {
                    upgVault[i] = maxLevel;
                    max_leveled_count++;
                } else {
                    already_max_leveled++;
                }
            }
            
            if (max_leveled_count === 0) {
                return `✅ All vault categories are already at maximum level! (${already_max_leveled} categories)`;
            } else {
                return `🚀 Set ${max_leveled_count} vault categories to maximum level! (${already_max_leveled} were already max level)`;
            }
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @plugin_command(
        help="Reset all vault categories to level 0.",
        params=[],
    )
    async def reset_all_vault_categories(self, injector=None, **kwargs):
        result = self.run_js_export('reset_all_vault_categories_js', injector)
        return result

    @js_export()
    def reset_all_vault_categories_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const upgVault = bEngine.getGameAttribute("UpgVault");
            const upgradeVault = bEngine.getGameAttribute("CustomLists").h.UpgradeVault;
            
            if (!upgVault || !upgradeVault) {
                return "Error: Vault data not found";
            }
            
            let reset_count = 0;
            let already_reset = 0;
            
            for (let i = 0; i < upgradeVault.length; i++) {
                const category = upgradeVault[i];
                if (!category || !category[0]) continue;
                
                const categoryName = category[0].replace(/_/g, ' ');
                const currentLevel = upgVault[i] || 0;
                
                if (currentLevel > 0) {
                    upgVault[i] = 0;
                    reset_count++;
                } else {
                    already_reset++;
                }
            }
            
            if (reset_count === 0) {
                return `✅ All vault categories are already reset! (${already_reset} categories)`;
            } else {
                return `🔄 Reset ${reset_count} vault categories to level 0! (${already_reset} were already reset)`;
            }
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''




plugin_class = VaultUnlockerPlugin 