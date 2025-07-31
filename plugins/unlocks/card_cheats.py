from plugin_system import PluginBase, ui_toggle, ui_button, ui_search_with_results, plugin_command, ui_autocomplete_input, ui_banner, js_export, console

class CardCheatsPlugin(PluginBase):
    VERSION = "1.0.1"
    DESCRIPTION = "Comprehensive cheats for the card system: set levels, add/remove cards, unlock slots, free upgrades. Uses real game structures from dumped_N.js."
    PLUGIN_ORDER = 4
    CATEGORY = "Unlocks"

    def __init__(self, config=None):
        super().__init__(config or {})  
        self.name = 'card_cheats'
        self.debug = config.get('debug', False) if config else False

    async def cleanup(self): pass
    async def update(self): pass
    async def on_config_changed(self, config):
        self.debug = config.get('debug', False)
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)
    async def on_game_ready(self):
        if self.config.get('free_card_upgrades', False):
            try:
                if self.debug:
                    console.print(f"[card_cheats] Auto-running free card upgrades on game ready")
                result = self.run_js_export('free_card_upgrades_js', self.injector)
                if self.debug:
                    console.print(f"[card_cheats] Auto-run result: {result}")
            except Exception as e:
                if self.debug:
                    console.print(f"[card_cheats] Error auto-running free card upgrades: {e}")

    @ui_banner(
        label="⚠️ HIGH RISK WARNING",
        description="This plugin is work-in-progress and has a high risk of bricking your quests permanently! Use at your own risk!",
        banner_type="warning",
        category="Actions",
        order=-100
    )
    async def warning_banner(self):
        return "Warning banner displayed"

    @ui_toggle(
        label="Debug Mode",
        description="Enable debug logging for card cheats plugin",
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
        label="Unlock All Card Slots",
        description="Unlock all card slots.",
        category="Actions",
        order=1
    )
    async def unlock_all_card_slots_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[card_cheats] Unlocking all card slots")
                result = await self.unlock_all_card_slots(self.injector)
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[card_cheats] Error unlocking all card slots: {e}")
                return f"ERROR: Error unlocking all card slots: {str(e)}"
        return "Injector not available"

    @ui_toggle(
        label="Free Card Upgrades",
        description="Make all card upgrades free (bypass 4*/5* requirements).",
        config_key="free_card_upgrades",
        default_value=False
    )
    async def free_card_upgrades_ui(self, value: bool = None):
        if value is not None:
            self.config["free_card_upgrades"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector and value:
                try:
                    if self.debug:
                        console.print(f"[card_cheats] Enabling free card upgrades")
                    result = await self.free_card_upgrades(self.injector)
                    if self.debug:
                        console.print(f"[card_cheats] Result: {result}")
                    return f"SUCCESS: {result}"
                except Exception as e:
                    if self.debug:
                        console.print(f"[card_cheats] Error enabling free card upgrades: {e}")
                    return f"ERROR: Error enabling free card upgrades: {str(e)}"
        return f"Free Card Upgrades {'enabled' if self.config.get('free_card_upgrades', False) else 'disabled'}"

    @plugin_command(
        help="Unlock all card slots.",
        params=[],
    )
    async def unlock_all_card_slots(self, injector=None, **kwargs):
        result = self.run_js_export('unlock_all_card_slots_js', injector)
        return result

    @plugin_command(
        help="Enable free card upgrades.",
        params=[],
    )
    async def free_card_upgrades(self, injector=None, **kwargs):
        result = self.run_js_export('free_card_upgrades_js', injector)
        return result

    @js_export()
    def unlock_all_card_slots_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            const cards = ctx["com.stencyl.Engine"].engine.getGameAttribute("Cards");
            const cardStuff = ctx["com.stencyl.Engine"].engine.getGameAttribute("CustomLists").h.CardStuff;
            
            for (let i = 0; i < cardStuff.length; i++) {
                const cardName = cardStuff[i][0];
                if (cardName && cardName !== "Blank") {
                    if (!cards[0].h[cardName]) cards[0].h[cardName] = 0;
                    if (!cards[1].includes(cardName)) cards[1].push(cardName);
                }
            }
            return "Unlocked all card slots!";
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @js_export()
    def free_card_upgrades_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            
            const optionsListAccount = ctx["com.stencyl.Engine"].engine.getGameAttribute("OptionsListAccount");
            if (optionsListAccount && Array.isArray(optionsListAccount)) {
                optionsListAccount[92] = 999;
                optionsListAccount[156] = 999;
            }
            
            const itemInventory = ctx["com.stencyl.Engine"].engine.getGameAttribute("ItemInventory");
            if (itemInventory && itemInventory.h) {
                itemInventory.h["GemQ17"] = 999;
                itemInventory.h["GemQ18"] = 999;
            }
            
            const itemQuantity = ctx["com.stencyl.Engine"].engine.getGameAttribute("ItemQuantity");
            if (itemQuantity && Array.isArray(itemQuantity)) {
                const inventoryOrder = ctx["com.stencyl.Engine"].engine.getGameAttribute("InventoryOrder");
                
                if (inventoryOrder && Array.isArray(inventoryOrder)) {
                    for (let i = 0; i < inventoryOrder.length; i++) {
                        const itemName = inventoryOrder[i];
                        if (itemName === "GemQ17" || itemName === "GemQ18") {
                            itemQuantity[i] = 999;
                        }
                    }
                }
            }
            
            const originalGetGameAttribute = ctx["com.stencyl.Engine"].engine.getGameAttribute;
            ctx["com.stencyl.Engine"].engine.getGameAttribute = function(attr) {
                const result = originalGetGameAttribute.call(this, attr);
                
                if (attr === "ItemInventory" && result && result.h) {
                    result.h["GemQ17"] = 999;
                    result.h["GemQ18"] = 999;
                }
                
                if (attr === "OptionsListAccount" && result && Array.isArray(result)) {
                    result[92] = 999;
                    result[156] = 999;
                }
                
                return result;
            };
            
            if (ctx["scripts.ActorEvents_12"]) {
                const events12 = ctx["scripts.ActorEvents_12"];
                if (events12._customBlock_CardUpgrade) {
                    events12._customBlock_CardUpgrade = function(...args) {
                        return true;
                    };
                }
            }
            
            const allScripts = Object.keys(ctx).filter(key => key.startsWith("scripts."));
            for (const scriptKey of allScripts) {
                const script = ctx[scriptKey];
                if (script && typeof script === "object") {
                    if (script._event_CARDS) {
                        const originalEvent = script._event_CARDS;
                        script._event_CARDS = function(...args) {
                            const result = originalEvent.apply(this, args);
                            return result;
                        };
                    }
                }
            }
            
            return "All card upgrades are now free! (Patched OptionsListAccount[92] for 4*, OptionsListAccount[156] for 5*, ItemInventory, and upgrade functions)";
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

plugin_class = CardCheatsPlugin 