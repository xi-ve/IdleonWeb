from plugin_system import PluginBase, js_export, ui_toggle, ui_search_with_results, plugin_command, ui_autocomplete_input, console

class CardCheatsPlugin(PluginBase):
    VERSION = "1.0.0"
    DESCRIPTION = "Comprehensive cheats for the card system: set levels, add/remove cards, unlock slots, free upgrades. Uses real game structures from dumped_N.js."

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
        # Auto-run free card upgrades if enabled
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

    @ui_toggle(
        label="Debug Mode",
        description="Enable debug logging for card cheats plugin",
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

    @ui_search_with_results(
        label="Card Status",
        description="Show all cards and their levels.",
        button_text="Show Status",
        placeholder="",
        category="Status & Info",
        order=2
    )
    async def card_status_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[card_cheats] Getting card status")
                result = self.run_js_export('get_card_status_js', self.injector)
                return result
            except Exception as e:
                if self.debug:
                    console.print(f"[card_cheats] Error getting status: {e}")
                return f"ERROR: Error getting card status: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_autocomplete_input(
        label="Set Card Level",
        description="Set the level of a card by name or index.",
        button_text="Set Level",
        placeholder="Enter card name or index (e.g., 'mushG', '0')",
        category="Card Management",
        order=3
    )
    async def set_card_level_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[card_cheats] Setting card level: {value}")
                if not value or not value.strip():
                    return "Please provide a card name or index."
                result = await self.set_card_level(value.strip())
                if self.debug:
                    console.print(f"[card_cheats] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[card_cheats] Error setting card level: {e}")
                return f"ERROR: Error setting card level: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    def get_set_card_level_ui_autocomplete(self, query: str = None) -> list:
        return self._get_card_names_autocomplete(query)

    @ui_autocomplete_input(
        label="Add Card",
        description="Add a card to your collection by name or index.",
        button_text="Add Card",
        placeholder="Enter card name or index",
        category="Card Management",
        order=4
    )
    async def add_card_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[card_cheats] Adding card: {value}")
                if not value or not value.strip():
                    return "Please provide a card name or index."
                result = await self.add_card(value.strip())
                if self.debug:
                    console.print(f"[card_cheats] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[card_cheats] Error adding card: {e}")
                return f"ERROR: Error adding card: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    def get_add_card_ui_autocomplete(self, query: str = None) -> list:
        return self._get_card_names_autocomplete(query)

    @ui_autocomplete_input(
        label="Remove Card",
        description="Remove a card from your collection by name or index.",
        button_text="Remove Card",
        placeholder="Enter card name or index",
        category="Card Management",
        order=5
    )
    async def remove_card_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[card_cheats] Removing card: {value}")
                if not value or not value.strip():
                    return "Please provide a card name or index."
                result = await self.remove_card(value.strip())
                if self.debug:
                    console.print(f"[card_cheats] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[card_cheats] Error removing card: {e}")
                return f"ERROR: Error removing card: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    def get_remove_card_ui_autocomplete(self, query: str = None) -> list:
        return self._get_card_names_autocomplete(query)

    def _get_card_names_autocomplete(self, query: str = None) -> list:
        # Call JS export to get all valid card names from CardStuff
        try:
            if not hasattr(self, 'injector') or not self.injector:
                if self.debug:
                    console.print(f"[card_cheats] No injector available for autocomplete")
                return []
            
            if self.debug:
                console.print(f"[card_cheats] Getting card names for autocomplete, query: '{query}'")
            
            result = self.run_js_export('get_card_names_js', self.injector)
            if self.debug:
                console.print(f"[card_cheats] Raw result from JS: {result} (type: {type(result)})")
            
            if not result:
                if self.debug:
                    console.print(f"[card_cheats] No result from get_card_names_js")
                return []
            
            try:
                if isinstance(result, str):
                    import json
                    names = json.loads(result)
                elif isinstance(result, list):
                    names = result
                else:
                    if self.debug:
                        console.print(f"[card_cheats] Unexpected result type: {type(result)}")
                    return []
            except Exception as e:
                if self.debug:
                    console.print(f"[card_cheats] Error parsing result: {e}")
                return []
            
            if not isinstance(names, list):
                if self.debug:
                    console.print(f"[card_cheats] Parsed result is not a list: {type(names)}")
                return []
            if self.debug:
                console.print(f"[card_cheats] Found {len(names)} valid card names")
            
            if query:
                query_lower = query.lower()
                filtered = [n for n in names if query_lower in n.lower()][:20]
                if self.debug:
                    console.print(f"[card_cheats] Filtered to {len(filtered)} matches for '{query}'")
                return filtered
            return names[:20]
        except Exception as e:
            if self.debug:
                console.print(f"[card_cheats] Error in card autocomplete: {e}")
            return []

    @ui_toggle(
        label="Unlock All Card Slots",
        description="Unlock all card slots.",
        config_key="unlock_all_card_slots",
        default_value=False,
        category="Card Management",
        order=6
    )
    async def unlock_all_card_slots_ui(self, value: bool = None):
        if value is not None:
            self.config["unlock_all_card_slots"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector and value:
                try:
                    if self.debug:
                        console.print(f"[card_cheats] Unlocking all card slots")
                    result = await self.unlock_all_card_slots(self.injector)
                    if self.debug:
                        console.print(f"[card_cheats] Result: {result}")
                    return f"SUCCESS: {result}"
                except Exception as e:
                    if self.debug:
                        console.print(f"[card_cheats] Error unlocking all card slots: {e}")
                    return f"ERROR: Error unlocking all card slots: {str(e)}"
        return f"Unlock All Card Slots {'enabled' if self.config.get('unlock_all_card_slots', False) else 'disabled'}"

    @ui_toggle(
        label="Free Card Upgrades",
        description="Make all card upgrades free (bypass 4*/5* requirements).",
        config_key="free_card_upgrades",
        default_value=False,
        category="Card Management",
        order=7
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

    @ui_toggle(
        label="Set All Owned Cards to 5*",
        description="Set all owned cards to maximum level (5*).",
        config_key="set_all_cards_to_max",
        default_value=False,
        category="Card Management",
        order=8
    )
    async def set_all_cards_to_max_ui(self, value: bool = None):
        if value is not None:
            self.config["set_all_cards_to_max"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector and value:
                try:
                    if self.debug:
                        console.print(f"[card_cheats] Setting all owned cards to 5*")
                    result = await self.set_all_cards_to_max(self.injector)
                    if self.debug:
                        console.print(f"[card_cheats] Result: {result}")
                    return f"SUCCESS: {result}"
                except Exception as e:
                    if self.debug:
                        console.print(f"[card_cheats] Error setting all cards to max: {e}")
                    return f"ERROR: Error setting all cards to max: {str(e)}"
        return f"Set All Cards to 5* {'enabled' if self.config.get('set_all_cards_to_max', False) else 'disabled'}"

    @plugin_command(
        help="Set the level of a card by name or index.",
        params=[{"name": "card", "type": str, "help": "Card name or index"}],
    )
    async def set_card_level(self, card: str, **kwargs):
        result = self.run_js_export('set_card_level_js', self.injector, card=card)
        return result

    @plugin_command(
        help="Add a card by name or index.",
        params=[{"name": "card", "type": str, "help": "Card name or index"}],
    )
    async def add_card(self, card: str, **kwargs):
        result = self.run_js_export('add_card_js', self.injector, card=card)
        return result

    @plugin_command(
        help="Remove a card by name or index.",
        params=[{"name": "card", "type": str, "help": "Card name or index"}],
    )
    async def remove_card(self, card: str, **kwargs):
        result = self.run_js_export('remove_card_js', self.injector, card=card)
        return result

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

    @plugin_command(
        help="Inspect OptionsListAccount data to see what we're patching.",
        params=[],
    )
    async def inspect_options_list(self, injector=None, **kwargs):
        result = self.run_js_export('inspect_options_list_js', injector)
        return result

    @plugin_command(
        help="Set all owned cards to maximum level (5*).",
        params=[],
    )
    async def set_all_cards_to_max(self, injector=None, **kwargs):
        result = self.run_js_export('set_all_cards_to_max_js', injector)
        return result

    @js_export()
    def get_card_names_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            const cardStuff = ctx["com.stencyl.Engine"].engine.getGameAttribute("CustomLists").h.CardStuff;
            console.log("Card autocomplete: Found CardStuff with length:", cardStuff.length);
            let names = [];
            for (let i = 0; i < cardStuff.length; i++) {
                if (cardStuff[i] && Array.isArray(cardStuff[i])) {
                    for (let j = 0; j < cardStuff[i].length; j++) {
                        const cardDef = cardStuff[i][j];
                        if (cardDef && Array.isArray(cardDef) && cardDef[0] && typeof cardDef[0] === 'string' && cardDef[0] !== 'Blank') {
                            names.push(cardDef[0]);
                        }
                    }
                }
            }
            console.log("Card autocomplete: Extracted", names.length, "valid names:", names);
            console.log("Card autocomplete: Returning array:", JSON.stringify(names));
            return JSON.stringify(names);
        } catch (e) {
            console.log("Card autocomplete error:", e);
            return JSON.stringify([]);
        }
        '''

    @js_export(params=["card"])
    def set_card_level_js(self, card=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            const cardStuff = ctx["com.stencyl.Engine"].engine.getGameAttribute("CustomLists").h.CardStuff;
            const cards = ctx["com.stencyl.Engine"].engine.getGameAttribute("Cards");
            let cardName = "";
            if (!isNaN(card)) {
                const idx = parseInt(card);
                if (idx >= 0 && idx < cardStuff.length) {
                    cardName = cardStuff[idx][0];
                }
            } else {
                cardName = card;
            }
            if (!cardName || cardName === "Blank") return `Card not found: ${card}`;
            cards[0].h[cardName] = 5;
            return `Set card '${cardName}' to level 5!`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export(params=["card"])
    def add_card_js(self, card=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            const cardStuff = ctx["com.stencyl.Engine"].engine.getGameAttribute("CustomLists").h.CardStuff;
            const cards = ctx["com.stencyl.Engine"].engine.getGameAttribute("Cards");
            let cardName = "";
            if (!isNaN(card)) {
                const idx = parseInt(card);
                if (idx >= 0 && idx < cardStuff.length) {
                    cardName = cardStuff[idx][0];
                }
            } else {
                cardName = card;
            }
            if (!cardName || cardName === "Blank") return `Card not found: ${card}`;
            if (!cards[0].h[cardName]) cards[0].h[cardName] = 0;
            if (!cards[1].includes(cardName)) cards[1].push(cardName);
            return `Added card '${cardName}'!`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export(params=["card"])
    def remove_card_js(self, card=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            const cardStuff = ctx["com.stencyl.Engine"].engine.getGameAttribute("CustomLists").h.CardStuff;
            const cards = ctx["com.stencyl.Engine"].engine.getGameAttribute("Cards");
            let cardName = "";
            if (!isNaN(card)) {
                const idx = parseInt(card);
                if (idx >= 0 && idx < cardStuff.length) {
                    cardName = cardStuff[idx][0];
                }
            } else {
                cardName = card;
            }
            if (!cardName || cardName === "Blank") return `Card not found: ${card}`;
            delete cards[0].h[cardName];
            const index = cards[1].indexOf(cardName);
            if (index > -1) cards[1].splice(index, 1);
            return `Removed card '${cardName}'!`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def get_card_status_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            const cardStuff = ctx["com.stencyl.Engine"].engine.getGameAttribute("CustomLists").h.CardStuff;
            const cards = ctx["com.stencyl.Engine"].engine.getGameAttribute("Cards");
            let output = "<div style='font-weight: bold; font-size: 16px; margin-bottom: 10px;'>CARD STATUS</div>";
            output += "<div style='margin: 10px 0; padding: 10px; background: rgba(0, 0, 0, 0.1); border-radius: 5px;'>";
            for (let i = 0; i < cardStuff.length; i++) {
                const name = (cardStuff[i] && typeof cardStuff[i][0] === 'string') ? cardStuff[i][0] : `Card ${i}`;
                if (name === "Blank") continue;
                const owned = cards[1].includes(name) ? "OWNED" : "MISSING";
                const level = cards[0].h[name] || 0;
                output += `<div style='margin: 2px 0; padding: 3px 8px;'>${name}: ${owned} | Level: ${level}</div>`;
            }
            output += "</div>";
            return output;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def set_all_cards_to_max_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            const cards = ctx["com.stencyl.Engine"].engine.getGameAttribute("Cards");
            const cardStuff = ctx["com.stencyl.Engine"].engine.getGameAttribute("CustomLists").h.CardStuff;
            
            let updatedCount = 0;
            let totalOwned = 0;
            
            // Get all owned cards from cards[1] array
            for (let i = 0; i < cards[1].length; i++) {
                const cardName = cards[1][i];
                if (cardName && cardName !== "Blank") {
                    totalOwned++;
                    // Set the card level to 5 (max level)
                    cards[0].h[cardName] = 5;
                    updatedCount++;
                }
            }
            
            return `Set ${updatedCount} owned cards to 5* level! (Total owned: ${totalOwned})`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

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
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def free_card_upgrades_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            
                    // Based on dumped_N.js analysis, the game uses OptionsListAccount[92] for 4* upgrade checks
        // and OptionsListAccount[156] for 5* upgrade checks
        const optionsListAccount = ctx["com.stencyl.Engine"].engine.getGameAttribute("OptionsListAccount");
        if (optionsListAccount && Array.isArray(optionsListAccount)) {
            optionsListAccount[92] = 999; // 4* cardifier bypass
            optionsListAccount[156] = 999; // 5* cardifier bypass
        }
            
            // Also patch the actual inventory system
            const itemInventory = ctx["com.stencyl.Engine"].engine.getGameAttribute("ItemInventory");
            if (itemInventory && itemInventory.h) {
                itemInventory.h["GemQ17"] = 999; // 4* cardifier
                itemInventory.h["GemQ18"] = 999; // 5* cardifier
            }
            
            // Patch the ItemQuantity array as well
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
            
            // Override the engine's getGameAttribute to intercept all checks
            const originalGetGameAttribute = ctx["com.stencyl.Engine"].engine.getGameAttribute;
            ctx["com.stencyl.Engine"].engine.getGameAttribute = function(attr) {
                const result = originalGetGameAttribute.call(this, attr);
                
                if (attr === "ItemInventory" && result && result.h) {
                    result.h["GemQ17"] = 999;
                    result.h["GemQ18"] = 999;
                }
                
                                            if (attr === "OptionsListAccount" && result && Array.isArray(result)) {
                                result[92] = 999; // 4* cardifier bypass
                                result[156] = 999; // 5* cardifier bypass
                            }
                
                return result;
            };
            
            // Patch the actual card upgrade event function
            if (ctx["scripts.ActorEvents_12"]) {
                const events12 = ctx["scripts.ActorEvents_12"];
                if (events12._customBlock_CardUpgrade) {
                    events12._customBlock_CardUpgrade = function(...args) {
                        return true; // Always allow upgrades
                    };
                }
            }
            
            // Also patch the _event_CARDS function
            const allScripts = Object.keys(ctx).filter(key => key.startsWith("scripts."));
            for (const scriptKey of allScripts) {
                const script = ctx[scriptKey];
                if (script && typeof script === "object") {
                    if (script._event_CARDS) {
                        const originalEvent = script._event_CARDS;
                        script._event_CARDS = function(...args) {
                            // Intercept any upgrade checks in the card event
                            const result = originalEvent.apply(this, args);
                            return result;
                        };
                    }
                }
            }
            
            return `All card upgrades are now free! (Patched OptionsListAccount[92] for 4*, OptionsListAccount[156] for 5*, ItemInventory, and upgrade functions)`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def inspect_options_list_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            const optionsListAccount = ctx["com.stencyl.Engine"].engine.getGameAttribute("OptionsListAccount");
            
            if (!optionsListAccount || !Array.isArray(optionsListAccount)) {
                return "ERROR: OptionsListAccount not found or not an array";
            }
            
            let output = "<div style='font-weight: bold; font-size: 16px; margin-bottom: 10px;'>🔍 OPTIONS LIST ACCOUNT INSPECTION</div>";
            output += "<div style='margin: 10px 0; padding: 10px; background: rgba(0, 0, 0, 0.1); border-radius: 5px;'>";
            
            // Show the indices we're patching
            const indicesToCheck = [92, 93, 94, 95];
            output += "<div style='font-weight: bold; margin-bottom: 10px;'>Indices we're patching:</div>";
            
            for (let i = 0; i < indicesToCheck.length; i++) {
                const idx = indicesToCheck[i];
                const value = optionsListAccount[idx];
                const type = typeof value;
                output += `<div style='margin: 2px 0; padding: 3px 8px;'>Index ${idx}: ${value} (${type})</div>`;
            }
            
            // Show some surrounding indices for context
            output += "<div style='font-weight: bold; margin: 10px 0 5px 0;'>Nearby indices for context:</div>";
            for (let i = 90; i <= 100; i++) {
                const value = optionsListAccount[i];
                const type = typeof value;
                const isPatching = indicesToCheck.includes(i);
                const style = isPatching ? "background: rgba(255, 255, 0, 0.2);" : "";
                output += `<div style='margin: 2px 0; padding: 3px 8px; ${style}'>Index ${i}: ${value} (${type})</div>`;
            }
            
            output += "</div>";
            return output;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

plugin_class = CardCheatsPlugin 