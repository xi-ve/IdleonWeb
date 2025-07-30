from typing import Dict, Any
from plugin_system import plugin_command, js_export, PluginBase, console, ui_toggle, ui_search_with_results, ui_autocomplete_input, ui_button
from config_manager import config_manager

class InventoryStoragePlugin(PluginBase):
    VERSION = "1.0.2"
    DESCRIPTION = "Automatically unlock all inventory packages and storage spaces"
    PLUGIN_ORDER = 3
    CATEGORY = "Character"

    def __init__(self, config=None):
        super().__init__(config or {})
        self.injector = None
        self.name = 'inventory_storage'
        self.debug = config_manager.get_path('plugin_configs.inventory_storage.debug', True)
        self._cache_timestamp = 0
        self._cache_duration = 300

    async def cleanup(self) -> None:
        pass

    async def update(self) -> None:
        pass

    async def on_config_changed(self, config: Dict[str, Any]) -> None:
        self.debug = config_manager.get_path('plugin_configs.inventory_storage.debug', True)
        if self.debug:
            console.print(f"[inventory_storage] Config changed: {config}")
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)

    async def on_game_ready(self) -> None:
        pass

    @ui_toggle(
        label="Debug Mode",
        description="Enable debug logging for inventory storage plugin",
        config_key="debug",
        default_value=True
    )
    async def enable_debug(self, value: bool = None):
        if value is not None:
            self.config["debug"] = value
            self.save_to_global_config()
        return f"Debug mode {'enabled' if self.config.get('debug', True) else 'disabled'}"

    @ui_button(
        label="Unlock All Inventory Packages",
        description="Unlock all inventory-related packages (bun_c, bun_i, bon_a)",
        category="Actions",
        order=1
    )
    async def auto_unlock_packages_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.unlock_all_inventory_packages(self.injector)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: Error unlocking packages: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first"

    @ui_button(
        label="Set Max Inventory Slots",
        description="Set inventory slots to maximum (112 slots)",
        category="Actions",
        order=2
    )
    async def max_inventory_slots_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.set_max_inventory_slots(self.injector)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: Error setting inventory slots: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first"

    @ui_button(
        label="Set Max Chest Slots",
        description="Set chest slots to maximum (200+ slots)",
        category="Actions",
        order=3
    )
    async def max_chest_slots_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.set_max_chest_slots(self.injector)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: Error setting chest slots: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first"

    @ui_button(
        label="Unlock All Inventory Bags",
        description="Unlock all inventory bags (InvBag1-112)",
        category="Actions",
        order=4
    )
    async def unlock_inventory_bags_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.unlock_all_inventory_bags(self.injector)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: Error unlocking inventory bags: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first"

    @ui_button(
        label="Unlock All Storage Boxes",
        description="Unlock all storage boxes (InvStorage1-99)",
        category="Actions",
        order=5
    )
    async def unlock_storage_boxes_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.unlock_all_storage_boxes(self.injector)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: Error unlocking storage boxes: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first"

    @ui_search_with_results(
        label="Current Storage Status",
        description="Show current inventory and chest slot counts",
        button_text="Check Status",
        placeholder="Enter filter term (leave empty to show all)",
    )
    async def check_storage_status_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.check_storage_status(self.injector)
                if value and value.strip():
                    lines = result.split('\n')
                    filtered_lines = []
                    query_lower = value.lower()
                    for line in lines:
                        if query_lower in line.lower():
                            filtered_lines.append(line)
                    return '\n'.join(filtered_lines) if filtered_lines else f"No status info found matching: {value}"
                else:
                    return result
            except Exception as e:
                return f"ERROR: Error checking storage status: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_search_with_results(
        label="Complete Storage List",
        description="Show detailed list of all packages, bags, and storage boxes with ownership status",
        button_text="Show Complete List",
        placeholder="Enter filter term (leave empty to show all)",
    )
    async def complete_storage_list_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.get_complete_storage_list(self.injector)
                if value and value.strip():
                    lines = result.split('\n')
                    filtered_lines = []
                    query_lower = value.lower()
                    for line in lines:
                        if query_lower in line.lower():
                            filtered_lines.append(line)
                    return '\n'.join(filtered_lines) if filtered_lines else f"No items found matching: {value}"
                else:
                    return result
            except Exception as e:
                return f"ERROR: Error getting complete storage list: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @plugin_command(
        help="Unlock all inventory-related packages (bun_c, bun_i, bon_a).",
        params=[],
    )
    async def unlock_all_inventory_packages(self, injector=None, **kwargs):
        if self.debug:
            console.print("[inventory_storage] Unlocking all inventory packages...")
        result = self.run_js_export('unlock_all_inventory_packages_js', injector)
        if self.debug:
            console.print(f"[inventory_storage] Result: {result}")
        return result

    @js_export()
    def unlock_all_inventory_packages_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const bundles_received = bEngine.gameAttributes.h.BundlesReceived.h;
            
            const inventoryPackages = [
                "bun_c",
                "bun_i",
                "bon_a"
            ];
            
            let unlocked_count = 0;
            const results = [];
            
            for (const package_code of inventoryPackages) {
                if (bundles_received[package_code] !== 1) {
                    bundles_received[package_code] = 1;
                    unlocked_count++;
                    results.push(`✅ Unlocked: ${package_code}`);
                } else {
                    results.push(`🟢 Already owned: ${package_code}`);
                }
            }
            
            if (bundles_received.bun_c === 1) {
                const current_chest_slots = bEngine.gameAttributes.h.ChestSlotsOwned || 0;
                bEngine.gameAttributes.h.ChestSlotsOwned = Math.round(current_chest_slots + 16);
            }
            
            if (bundles_received.bun_i === 1) {
                const current_inv_slots = bEngine.gameAttributes.h.InventorySlotsOwned || 0;
                const current_chest_slots = bEngine.gameAttributes.h.ChestSlotsOwned || 0;
                bEngine.gameAttributes.h.InventorySlotsOwned = Math.min(112, current_inv_slots + 5);
                bEngine.gameAttributes.h.ChestSlotsOwned = Math.round(current_chest_slots + 8);
            }
            
            if (bundles_received.bon_a === 1) {
                const current_chest_slots = bEngine.gameAttributes.h.ChestSlotsOwned || 0;
                bEngine.gameAttributes.h.ChestSlotsOwned = Math.round(current_chest_slots + 10);
            }
            
            const summary = `\\n\\n**Summary:** Unlocked ${unlocked_count} new packages`;
            return results.join("\\n") + summary;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @plugin_command(
        help="Set inventory slots to maximum (112 slots).",
        params=[],
    )
    async def set_max_inventory_slots(self, injector=None, **kwargs):
        if self.debug:
            console.print("[inventory_storage] Setting max inventory slots...")
        result = self.run_js_export('set_max_inventory_slots_js', injector)
        if self.debug:
            console.print(f"[inventory_storage] Result: {result}")
        return result

    @js_export()
    def set_max_inventory_slots_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const max_slots = 112;
            
            const current_slots = bEngine.gameAttributes.h.InventorySlotsOwned || 0;
            
            if (current_slots >= max_slots) {
                return `✅ Inventory already at maximum (${current_slots}/${max_slots} slots)`;
            }
            
            bEngine.gameAttributes.h.InventorySlotsOwned = max_slots;
            
            const inventory_order = bEngine.gameAttributes.h.InventoryOrder || [];
            for (let i = 0; i < max_slots; i++) {
                if (inventory_order[i] === "LockedInvSpace") {
                    inventory_order[i] = "Blank";
                }
            }
            
            return `🎁 Set inventory slots to maximum: ${max_slots} slots (was ${current_slots})`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @plugin_command(
        help="Set chest slots to maximum (200+ slots).",
        params=[],
    )
    async def set_max_chest_slots(self, injector=None, **kwargs):
        if self.debug:
            console.print("[inventory_storage] Setting max chest slots...")
        result = self.run_js_export('set_max_chest_slots_js', injector)
        if self.debug:
            console.print(f"[inventory_storage] Result: {result}")
        return result

    @js_export()
    def set_max_chest_slots_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const max_slots = 250;
            
            const current_slots = bEngine.gameAttributes.h.ChestSlotsOwned || 0;
            
            if (current_slots >= max_slots) {
                return `✅ Chest already at maximum (${current_slots}/${max_slots} slots)`;
            }
            
            bEngine.gameAttributes.h.ChestSlotsOwned = max_slots;
            
            const chest_order = bEngine.gameAttributes.h.ChestOrder || [];
            for (let i = 0; i < max_slots; i++) {
                if (chest_order[i] === "LockedInvSpace") {
                    chest_order[i] = "Blank";
                }
            }
            
            return `🎁 Set chest slots to maximum: ${max_slots} slots (was ${current_slots})`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @plugin_command(
        help="Unlock all inventory bags (InvBag1-112).",
        params=[],
    )
    async def unlock_all_inventory_bags(self, injector=None, **kwargs):
        if self.debug:
            console.print("[inventory_storage] Unlocking all inventory bags...")
        result = self.run_js_export('unlock_all_inventory_bags_js', injector)
        if self.debug:
            console.print(f"[inventory_storage] Result: {result}")
        return result

    @js_export()
    def unlock_all_inventory_bags_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const inv_bags_used = bEngine.gameAttributes.h.InvBagsUsed.h;
            
            let unlocked_count = 0;
            const results = [];
            
            for (let i = 1; i <= 112; i++) {
                const bag_key = i.toString();
                if (!inv_bags_used[bag_key] || inv_bags_used[bag_key] === 0) {
                    inv_bags_used[bag_key] = 1;
                    unlocked_count++;
                    results.push(`🎒 Unlocked: InvBag${i}`);
                }
            }
            
            const bag_keys = Object.keys(inv_bags_used);
            let total_bag_slots = 0;
            
            for (const bag_key of bag_keys) {
                if (inv_bags_used[bag_key] > 0) {
                    total_bag_slots += parseInt(inv_bags_used[bag_key]);
                }
            }
            
            const current_inv_slots = bEngine.gameAttributes.h.InventorySlotsOwned || 0;
            const new_inv_slots = Math.min(112, current_inv_slots + total_bag_slots);
            
            if (new_inv_slots > current_inv_slots) {
                bEngine.gameAttributes.h.InventorySlotsOwned = new_inv_slots;
                results.push(`📦 Added ${total_bag_slots} inventory slots from bags`);
            }
            
            const summary = `\\n\\n**Summary:** Unlocked ${unlocked_count} new inventory bags`;
            return results.join("\\n") + summary;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @plugin_command(
        help="Unlock all storage boxes (InvStorage1-99).",
        params=[],
    )
    async def unlock_all_storage_boxes(self, injector=None, **kwargs):
        if self.debug:
            console.print("[inventory_storage] Unlocking all storage boxes...")
        result = self.run_js_export('unlock_all_storage_boxes_js', injector)
        if self.debug:
            console.print(f"[inventory_storage] Result: {result}")
        return result

    @js_export()
    def unlock_all_storage_boxes_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const inv_storage_used = bEngine.gameAttributes.h.InvStorageUsed.h;
            
            let unlocked_count = 0;
            const results = [];
            
            for (let i = 1; i <= 99; i++) {
                const box_key = i.toString();
                if (!inv_storage_used[box_key] || inv_storage_used[box_key] === 0) {
                    inv_storage_used[box_key] = 1;
                    unlocked_count++;
                    results.push(`📦 Unlocked: InvStorage${i}`);
                }
            }
            
            const box_keys = Object.keys(inv_storage_used);
            let total_box_slots = 0;
            
            for (const box_key of box_keys) {
                if (inv_storage_used[box_key] > 0) {
                    total_box_slots += parseInt(inv_storage_used[box_key]);
                }
            }
            
            const current_chest_slots = bEngine.gameAttributes.h.ChestSlotsOwned || 0;
            const max_chest_slots = 250;
            const new_chest_slots = Math.min(max_chest_slots, current_chest_slots + total_box_slots);
            
            if (new_chest_slots > current_chest_slots) {
                bEngine.gameAttributes.h.ChestSlotsOwned = new_chest_slots;
                results.push(`🗄️ Added ${new_chest_slots - current_chest_slots} chest slots from storage boxes (capped at ${max_chest_slots})`);
            }
            
            const summary = `\\n\\n**Summary:** Unlocked ${unlocked_count} new storage boxes`;
            return results.join("\\n") + summary;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @plugin_command(
        help="Get complete list of all storage items with ownership status.",
        params=[],
    )
    async def get_complete_storage_list(self, injector=None, **kwargs):
        if self.debug:
            console.print("[inventory_storage] Getting complete storage list...")
        result = self.run_js_export('get_complete_storage_list_js', injector)
        if self.debug:
            console.print(f"[inventory_storage] Result: {result}")
        return result

    @js_export()
    def get_complete_storage_list_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const bundles_received = bEngine.gameAttributes.h.BundlesReceived.h;
            const inv_bags_used = bEngine.gameAttributes.h.InvBagsUsed.h;
            const inv_storage_used = bEngine.gameAttributes.h.InvStorageUsed.h;
            
            const results = [];
            
            results.push(`🎁 INVENTORY PACKAGES`);
            
            const inventoryPackages = [
                { code: "bun_c", name: "Starter Pack", effect: "+16 chest slots" },
                { code: "bun_i", name: "Auto Loot Pack", effect: "+5 inventory, +8 chest slots" },
                { code: "bon_a", name: "Storage Ram Pack", effect: "+10 chest slots" }
            ];
            
            let owned_packages = 0;
            for (const pkg of inventoryPackages) {
                const is_owned = bundles_received[pkg.code] === 1;
                if (is_owned) owned_packages++;
                
                const status = is_owned ? "🟢 OWNED" : "⚪ NOT OWNED";
                results.push(`${status} **${pkg.code}** : ${pkg.name} (${pkg.effect})`);
            }
            
            results.push(``);
            results.push(`Summary: ${owned_packages}/${inventoryPackages.length} packages owned`);
            
            results.push(``);
            results.push(`🎒 INVENTORY BAGS (InvBag1-112)`);
            
            let owned_bags = 0;
            let total_bag_slots = 0;
            
            for (let i = 1; i <= 112; i++) {
                const bag_key = i.toString();
                const is_owned = inv_bags_used[bag_key] && inv_bags_used[bag_key] > 0;
                const slots_provided = is_owned ? inv_bags_used[bag_key] : 0;
                
                if (is_owned) {
                    owned_bags++;
                    total_bag_slots += parseInt(slots_provided);
                }
                
                const status = is_owned ? "🟢 OWNED" : "⚪ NOT OWNED";
                results.push(`${status} **InvBag${i.toString().padStart(3, '0')}** : ${slots_provided} slots`);
            }
            
            results.push(``);
            results.push(`Summary: ${owned_bags}/112 bags owned (${total_bag_slots} total slots)`);
            
            results.push(``);
            results.push(`📦 STORAGE BOXES (InvStorage1-99)`);
            
            let owned_boxes = 0;
            let total_box_slots = 0;
            
            for (let i = 1; i <= 99; i++) {
                const box_key = i.toString();
                const is_owned = inv_storage_used[box_key] && inv_storage_used[box_key] > 0;
                const slots_provided = is_owned ? inv_storage_used[box_key] : 0;
                
                if (is_owned) {
                    owned_boxes++;
                    total_box_slots += parseInt(slots_provided);
                }
                
                const status = is_owned ? "🟢 OWNED" : "⚪ NOT OWNED";
                results.push(`${status} **InvStorage${i.toString().padStart(2, '0')}** : ${slots_provided} slots`);
            }
            
            results.push(``);
            results.push(`Summary: ${owned_boxes}/99 storage boxes owned (${total_box_slots} total slots)`);
            
            const inventory_slots = bEngine.gameAttributes.h.InventorySlotsOwned || 0;
            const chest_slots = bEngine.gameAttributes.h.ChestSlotsOwned || 0;
            
            results.push(``);
            results.push(`📊 CURRENT SLOT STATUS`);
            results.push(`Inventory Slots: ${inventory_slots}/112 (${Math.round(inventory_slots/112*100)}%)`);
            results.push(`Chest Slots: ${chest_slots}/250 (${Math.round(chest_slots/250*100)}%)`);
            
            results.push(``);
            results.push(`🎯 OVERALL SUMMARY`);
            results.push(`• Packages: ${owned_packages}/${inventoryPackages.length} (${Math.round(owned_packages/inventoryPackages.length*100)}%)`);
            results.push(`• Inventory Bags: ${owned_bags}/112 (${Math.round(owned_bags/112*100)}%)`);
            results.push(`• Storage Boxes: ${owned_boxes}/99 (${Math.round(owned_boxes/99*100)}%)`);
            results.push(`• Total Bag Slots: ${total_bag_slots}`);
            results.push(`• Total Storage Box Slots: ${total_box_slots}`);
            
            return results.join("\\n");
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @plugin_command(
        help="Check current storage status (inventory and chest slots).",
        params=[],
    )
    async def check_storage_status(self, injector=None, **kwargs):
        if self.debug:
            console.print("[inventory_storage] Checking storage status...")
        result = self.run_js_export('check_storage_status_js', injector)
        if self.debug:
            console.print(f"[inventory_storage] Result: {result}")
        return result

    @js_export()
    def check_storage_status_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const bundles_received = bEngine.gameAttributes.h.BundlesReceived.h;
            const inv_bags_used = bEngine.gameAttributes.h.InvBagsUsed.h;
            const inv_storage_used = bEngine.gameAttributes.h.InvStorageUsed.h;
            
            const inventory_slots = bEngine.gameAttributes.h.InventorySlotsOwned || 0;
            const chest_slots = bEngine.gameAttributes.h.ChestSlotsOwned || 0;
            
            const inventoryPackages = [
                { code: "bun_c", name: "Starter Pack", effect: "+16 chest slots" },
                { code: "bun_i", name: "Auto Loot Pack", effect: "+5 inventory, +8 chest slots" },
                { code: "bon_a", name: "Storage Ram Pack", effect: "+10 chest slots" }
            ];
            
            const results = [];
            results.push(`📦 **Storage Status**`);
            results.push(`Inventory Slots: ${inventory_slots}/112`);
            results.push(`Chest Slots: ${chest_slots}/250`);
            results.push(``);
            results.push(`🎁 **Inventory Packages Status**`);
            
            let owned_count = 0;
            for (const pkg of inventoryPackages) {
                const is_owned = bundles_received[pkg.code] === 1;
                if (is_owned) owned_count++;
                
                const status = is_owned ? "🟢 OWNED" : "⚪ NOT OWNED";
                results.push(`${status} **${pkg.code}** : ${pkg.name} (${pkg.effect})`);
            }
            
            results.push(``);
            results.push(`🎒 **Inventory Bags Status**`);
            
            let bag_count = 0;
            let total_bag_slots = 0;
            for (let i = 1; i <= 112; i++) {
                const bag_key = i.toString();
                const is_owned = inv_bags_used[bag_key] && inv_bags_used[bag_key] > 0;
                if (is_owned) {
                    bag_count++;
                    total_bag_slots += parseInt(inv_bags_used[bag_key]);
                }
            }
            results.push(`Owned Bags: ${bag_count}/112`);
            results.push(`Total Bag Slots: ${total_bag_slots}`);
            
            results.push(``);
            results.push(`📦 **Storage Boxes Status**`);
            
            let box_count = 0;
            let total_box_slots = 0;
            for (let i = 1; i <= 99; i++) {
                const box_key = i.toString();
                const is_owned = inv_storage_used[box_key] && inv_storage_used[box_key] > 0;
                if (is_owned) {
                    box_count++;
                    total_box_slots += parseInt(inv_storage_used[box_key]);
                }
            }
            results.push(`Owned Storage Boxes: ${box_count}/99`);
            results.push(`Total Storage Box Slots: ${total_box_slots}`);
            
            const summary = `\\n\\n**Summary:** ${owned_count}/${inventoryPackages.length} packages, ${bag_count}/112 bags, ${box_count}/99 storage boxes`;
            return results.join("\\n") + summary;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @plugin_command(
        help="Unlock all storage spaces (inventory + chest + packages).",
        params=[],
    )
    async def unlock_all_storage(self, injector=None, **kwargs):
        if self.debug:
            console.print("[inventory_storage] Unlocking all storage...")
        result = self.run_js_export('unlock_all_storage_js', injector)
        if self.debug:
            console.print(f"[inventory_storage] Result: {result}")
        return result

    @js_export()
    def unlock_all_storage_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const bundles_received = bEngine.gameAttributes.h.BundlesReceived.h;
            const inv_bags_used = bEngine.gameAttributes.h.InvBagsUsed.h;
            const inv_storage_used = bEngine.gameAttributes.h.InvStorageUsed.h;
            
            const results = [];
            
            const inventoryPackages = ["bun_c", "bun_i", "bon_a"];
            let unlocked_packages = 0;
            
            for (const package_code of inventoryPackages) {
                if (bundles_received[package_code] !== 1) {
                    bundles_received[package_code] = 1;
                    unlocked_packages++;
                }
            }
            
            if (unlocked_packages > 0) {
                results.push(`🎁 Unlocked ${unlocked_packages} inventory packages`);
            }
            
            let unlocked_bags = 0;
            for (let i = 1; i <= 112; i++) {
                const bag_key = i.toString();
                if (!inv_bags_used[bag_key] || inv_bags_used[bag_key] === 0) {
                    inv_bags_used[bag_key] = 1;
                    unlocked_bags++;
                }
            }
            
            if (unlocked_bags > 0) {
                results.push(`🎒 Unlocked ${unlocked_bags} inventory bags`);
            }
            
            let unlocked_boxes = 0;
            for (let i = 1; i <= 99; i++) {
                const box_key = i.toString();
                if (!inv_storage_used[box_key] || inv_storage_used[box_key] === 0) {
                    inv_storage_used[box_key] = 1;
                    unlocked_boxes++;
                }
            }
            
            if (unlocked_boxes > 0) {
                results.push(`📦 Unlocked ${unlocked_boxes} storage boxes`);
            }
            
            const current_inv = bEngine.gameAttributes.h.InventorySlotsOwned || 0;
            const max_inv = 112;
            if (current_inv < max_inv) {
                bEngine.gameAttributes.h.InventorySlotsOwned = max_inv;
                results.push(`📦 Set inventory slots to ${max_inv} (was ${current_inv})`);
            }
            
            const current_chest = bEngine.gameAttributes.h.ChestSlotsOwned || 0;
            const max_chest = 250;
            if (current_chest < max_chest) {
                bEngine.gameAttributes.h.ChestSlotsOwned = max_chest;
                results.push(`🗄️ Set chest slots to ${max_chest} (was ${current_chest})`);
            }
            
            let unlocked_inv_spaces = 0;
            let unlocked_chest_spaces = 0;
            
            const inventory_order = bEngine.gameAttributes.h.InventoryOrder || [];
            for (let i = 0; i < max_inv; i++) {
                if (inventory_order[i] === "LockedInvSpace") {
                    inventory_order[i] = "Blank";
                    unlocked_inv_spaces++;
                }
            }
            
            const chest_order = bEngine.gameAttributes.h.ChestOrder || [];
            for (let i = 0; i < max_chest; i++) {
                if (chest_order[i] === "LockedInvSpace") {
                    chest_order[i] = "Blank";
                    unlocked_chest_spaces++;
                }
            }
            
            if (unlocked_inv_spaces > 0) {
                results.push(`🔓 Unlocked ${unlocked_inv_spaces} inventory spaces`);
            }
            
            if (unlocked_chest_spaces > 0) {
                results.push(`🔓 Unlocked ${unlocked_chest_spaces} chest spaces`);
            }
            
            if (results.length === 0) {
                return `✅ All storage already unlocked and at maximum!`;
            }
            
            return results.join("\\n");
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

plugin_class = InventoryStoragePlugin 