from plugin_system import PluginBase, ui_toggle, ui_button, ui_search_with_results, plugin_command, ui_autocomplete_input, ui_banner, js_export, console
import time

class CardCheatsPlugin(PluginBase):
    VERSION = "2.0.0"
    DESCRIPTION = "Comprehensive card system cheats: search, unlock, level management, stats viewer, and complete card collection tools."
    PLUGIN_ORDER = 4
    CATEGORY = "Unlocks"

    def __init__(self, config=None):
        super().__init__(config or {})  
        self.name = 'card_cheats'
        self.debug = config.get('debug', False) if config else False
        self._card_cache = None
        self._cache_timestamp = 0
        self._cache_duration = 300

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

    @ui_autocomplete_input(
        label="Search Card Details",
        description="Search for cards and view their detailed information",
        button_text="View Details",
        placeholder="Card name (e.g. Copper, Amarok, Boop)",
        category="Card Search",
        order=1
    )
    async def search_card_details_ui(self, value: str = None):
        if value:
            if hasattr(self, 'injector') and self.injector:
                try:
                    result = await self.get_card_details(value.strip(), self.injector)
                    return result
                except Exception as e:
                    return f"ERROR: {str(e)}"
            else:
                return "ERROR: No injector available - run 'inject' first"
        return "Enter a card name to view its details"

    async def get_search_card_details_ui_autocomplete(self, query: str = ""):
        return await self.get_card_autocomplete(query)

    @ui_search_with_results(
        label="Card Collection Stats",
        description="View comprehensive statistics about your card collection",
        button_text="View Stats",
        placeholder="Optional: filter by card name",
        category="Card Search",
        order=2
    )
    async def view_card_stats_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if value and value.strip():
                    result = await self.search_cards(value.strip(), self.injector)
                    return result
                else:
                    result = await self.get_card_summary(self.injector)
                    return result
            except Exception as e:
                return f"ERROR: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first"

    @ui_autocomplete_input(
        label="Unlock Specific Card",
        description="Unlock a specific card by name",
        button_text="Unlock",
        placeholder="Card name (e.g. Copper, Amarok)",
        category="Card Management",
        order=3
    )
    async def unlock_card_ui(self, value: str = None):
        if value:
            if hasattr(self, 'injector') and self.injector:
                try:
                    result = await self.unlock_card(value.strip(), self.injector)
                    return f"SUCCESS: {result}"
                except Exception as e:
                    return f"ERROR: {str(e)}"
            else:
                return "ERROR: No injector available - run 'inject' first"
        return "Enter a card name to unlock"

    async def get_unlock_card_ui_autocomplete(self, query: str = ""):
        return await self.get_card_autocomplete(query)

    @ui_autocomplete_input(
        label="Set Card to Max Level",
        description="Set a specific card to maximum level (requires card ownership)",
        button_text="Max Level",
        placeholder="Card name (e.g. Copper, Amarok)",
        category="Card Management",
        order=4
    )
    async def max_level_card_ui(self, value: str = None):
        if value:
            if hasattr(self, 'injector') and self.injector:
                try:
                    result = await self.set_card_max_level(value.strip(), self.injector)
                    return f"SUCCESS: {result}"
                except Exception as e:
                    return f"ERROR: {str(e)}"
            else:
                return "ERROR: No injector available - run 'inject' first"
        return "Enter a card name to set to max level"

    async def get_max_level_card_ui_autocomplete(self, query: str = ""):
        return await self.get_card_autocomplete(query)

    @ui_autocomplete_input(
        label="Reset Card Level",
        description="Reset a card to level 1 (quantity = 1)",
        button_text="Reset",
        placeholder="Card name (e.g. Copper, Amarok)",
        category="Card Management",
        order=5
    )
    async def reset_card_level_ui(self, value: str = None):
        if value:
            if hasattr(self, 'injector') and self.injector:
                try:
                    result = await self.reset_card_level(value.strip(), self.injector)
                    return f"SUCCESS: {result}"
                except Exception as e:
                    return f"ERROR: {str(e)}"
            else:
                return "ERROR: No injector available - run 'inject' first"
        return "Enter a card name to reset its level"

    async def get_reset_card_level_ui_autocomplete(self, query: str = ""):
        return await self.get_card_autocomplete(query)

    @ui_button(
        label="Set All Cards to Max Level",
        description="Set all owned cards to maximum level (level 5)",
        category="Bulk Actions",
        order=6
    )
    async def max_all_cards_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.set_all_cards_max_level(self.injector)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "ERROR: No injector available - run 'inject' first"

    @ui_button(
        label="Unlock All Missing Cards",
        description="Unlock all cards that you don't currently own",
        category="Bulk Actions",
        order=7
    )
    async def unlock_all_missing_cards_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.unlock_all_missing_cards(self.injector)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "ERROR: No injector available - run 'inject' first"

    @ui_button(
        label="Remove All Cards",
        description="⚠️ DANGER: Remove all cards from your collection",
        category="Bulk Actions",
        order=8
    )
    async def remove_all_cards_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.remove_all_cards(self.injector)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "ERROR: No injector available - run 'inject' first"

    async def get_card_autocomplete(self, query: str = ""):
        if not hasattr(self, 'injector') or not self.injector:
            return []
        
        try:
            # Get raw card list directly instead of using formatted cache
            raw_result = await self.list_all_cards(self.injector)
            
            if not raw_result or raw_result.startswith("Error:"):
                return []
            
            suggestions = []
            query_lower = query.lower()
            
            lines = raw_result.split('\n')
            for line in lines:
                if ' | ' in line:
                    # Format: "CardName | Status | Description"
                    card_name = line.split(' | ')[0].strip()
                    if query_lower in card_name.lower():
                        suggestions.append(card_name)
            
            return suggestions[:10]
            
        except Exception as e:
            if self.debug:
                console.print(f"[card_cheats] Autocomplete error: {e}")
            return []

    async def get_cached_card_list(self):
        current_time = time.time()
        
        if (self._card_cache is not None and 
            current_time - self._cache_timestamp < self._cache_duration):
            return self._card_cache
        
        raw_result = await self.list_all_cards(self.injector)
        
        if raw_result and not raw_result.startswith("Error:"):
            try:
                lines = raw_result.split('\n')
                formatted_cards = []
                
                for line in lines:
                    if ' | ' in line:
                        parts = line.split(' | ')
                        if len(parts) >= 2:
                            card_name = parts[0]
                            details = ' | '.join(parts[1:])
                            formatted_cards.append(f"• **{card_name}** : {details}")
                    else:
                        formatted_cards.append(f"• {line}")
                
                formatted_result = f"**All Cards** ({len(formatted_cards)} cards):\n\n" + "\n".join(formatted_cards)
                
                self._card_cache = formatted_result
                self._cache_timestamp = current_time
                
                return formatted_result
            except Exception as e:
                return f"**All Cards**:\n\n{raw_result}"
        else:
            return f"ERROR: Error fetching cards: {raw_result}"

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
        help="Get detailed information about a specific card.",
        params=[
            {"name": "card_name", "type": str, "help": "Name of the card to get details for"},
        ],
    )
    async def get_card_details(self, card_name: str, injector=None, **kwargs):
        if self.debug:
            console.print(f"[card_cheats] Getting details for card: {card_name}")
        result = self.run_js_export('get_card_details_js', injector, card_name=card_name)
        return result

    @plugin_command(
        help="Get comprehensive card collection summary.",
        params=[],
    )
    async def get_card_summary(self, injector=None, **kwargs):
        if self.debug:
            console.print("[card_cheats] Getting card summary...")
        result = self.run_js_export('get_card_summary_js', injector)
        return result

    @plugin_command(
        help="Search for cards by name or description.",
        params=[
            {"name": "search_term", "type": str, "help": "Term to search for in card names/descriptions"},
        ],
    )
    async def search_cards(self, search_term: str, injector=None, **kwargs):
        if self.debug:
            console.print(f"[card_cheats] Searching cards with term: {search_term}")
        result = self.run_js_export('search_cards_js', injector, search_term=search_term)
        return result

    @plugin_command(
        help="List all available cards with their details.",
        params=[],
    )
    async def list_all_cards(self, injector=None, **kwargs):
        if self.debug:
            console.print("[card_cheats] Listing all cards...")
        result = self.run_js_export('list_all_cards_js', injector)
        return result

    @plugin_command(
        help="Unlock a specific card by name.",
        params=[
            {"name": "card_name", "type": str, "help": "Name of the card to unlock"},
        ],
    )
    async def unlock_card(self, card_name: str, injector=None, **kwargs):
        if self.debug:
            console.print(f"[card_cheats] Unlocking card: {card_name}")
        result = self.run_js_export('unlock_card_js', injector, card_name=card_name)
        return result

    @plugin_command(
        help="Set a specific card to maximum level.",
        params=[
            {"name": "card_name", "type": str, "help": "Name of the card to set to max level"},
        ],
    )
    async def set_card_max_level(self, card_name: str, injector=None, **kwargs):
        if self.debug:
            console.print(f"[card_cheats] Setting card to max level: {card_name}")
        result = self.run_js_export('set_card_max_level_js', injector, card_name=card_name)
        return result

    @plugin_command(
        help="Reset a card to level 1.",
        params=[
            {"name": "card_name", "type": str, "help": "Name of the card to reset"},
        ],
    )
    async def reset_card_level(self, card_name: str, injector=None, **kwargs):
        if self.debug:
            console.print(f"[card_cheats] Resetting card level: {card_name}")
        result = self.run_js_export('reset_card_level_js', injector, card_name=card_name)
        return result

    @plugin_command(
        help="Set all owned cards to maximum level.",
        params=[],
    )
    async def set_all_cards_max_level(self, injector=None, **kwargs):
        if self.debug:
            console.print("[card_cheats] Setting all cards to max level...")
        result = self.run_js_export('set_all_cards_max_level_js', injector)
        return result

    @plugin_command(
        help="Unlock all missing cards.",
        params=[],
    )
    async def unlock_all_missing_cards(self, injector=None, **kwargs):
        if self.debug:
            console.print("[card_cheats] Unlocking all missing cards...")
        result = self.run_js_export('unlock_all_missing_cards_js', injector)
        return result

    @plugin_command(
        help="Remove all cards from collection.",
        params=[],
    )
    async def remove_all_cards(self, injector=None, **kwargs):
        if self.debug:
            console.print("[card_cheats] Removing all cards...")
        result = self.run_js_export('remove_all_cards_js', injector)
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

    @js_export(params=["card_name"])
    def get_card_details_js(self, card_name=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            const engine = ctx["com.stencyl.Engine"].engine;
            const pixelHelper = engine.getGameAttribute("PixelHelperActor");
            
            if (!pixelHelper || !pixelHelper[6]) {
                throw new Error("Card definitions not found");
            }
            
            const cardDefs = pixelHelper[6].behaviors.getBehavior("ActorEvents_312")._GenINFO[45];
            if (!cardDefs?.h) {
                throw new Error("Card definitions not accessible");
            }
            
            const cardData = engine.getGameAttribute("Cards");
            if (!cardData || !cardData[0]) {
                throw new Error("Card data not found");
            }
            
            function calculateCardLevel(cardId, quantity) {
                if (quantity <= 0) return 1;
                
                const baseReq = cardDefs.h[cardId][2] || 1;
                let level = 1;
                
                for (let i = 2; i <= 5; i++) {
                    let required;
                    if (cardId === "Boss3B") {
                        required = Math.ceil(1.5 * Math.pow(i + Math.floor((i-1) / 3), 2));
                    } else {
                        required = Math.ceil(baseReq * Math.pow(i + Math.floor((i-1) / 3) + 16 * Math.floor((i-1) / 4), 2));
                    }
                    
                    if (quantity >= required) {
                        level = i;
                    } else {
                        break;
                    }
                }
                
                return Math.min(level, 5);
            }
            
            function getCardsNeededForNextLevel(cardId, currentQuantity, currentLevel) {
                if (currentLevel >= 5) return 0;
                
                const baseReq = cardDefs.h[cardId][2] || 1;
                const nextLevel = currentLevel + 1;
                let nextLevelReq;
                
                if (cardId === "Boss3B") {
                    nextLevelReq = Math.ceil(1.5 * Math.pow(nextLevel + Math.floor((nextLevel-1) / 3), 2));
                } else {
                    nextLevelReq = Math.ceil(baseReq * Math.pow(nextLevel + Math.floor((nextLevel-1) / 3) + 16 * Math.floor((nextLevel-1) / 4), 2));
                }
                
                return Math.max(0, nextLevelReq - currentQuantity);
            }
            
            // Find card by name (case-insensitive partial match)
            let foundCardId = null;
            const searchTerm = card_name.toLowerCase();
            
            for (const cardId in cardDefs.h) {
                const cardDef = cardDefs.h[cardId];
                if (cardDef && cardDef[0]) {
                    const cardName = cardDef[0].toLowerCase();
                    if (cardName.includes(searchTerm) || cardId.toLowerCase().includes(searchTerm)) {
                        foundCardId = cardId;
                        if (cardName === searchTerm) break; // Exact match takes priority
                    }
                }
            }
            
            if (!foundCardId) {
                return `No card found matching: "${card_name}"`;
            }
            
            const cardDef = cardDefs.h[foundCardId];
            const quantity = cardData[0].h[foundCardId] || 0;
            const isOwned = quantity > 0;
            const isEquipped = cardData[2] && cardData[2].includes(foundCardId);
            const level = calculateCardLevel(foundCardId, quantity);
            const cardsNeeded = getCardsNeededForNextLevel(foundCardId, quantity, level);
            
            let result = `<div class="card-details">`;
            result += `<h3>${cardDef[0]} <span class="card-id">(${foundCardId})</span></h3>`;
            result += `<div class="card-info">`;
            result += `<div class="info-item"><strong>Level:</strong> ${level}/5</div>`;
            result += `<div class="info-item"><strong>Quantity:</strong> ${quantity}</div>`;
            result += `<div class="info-item"><strong>Owned:</strong> ${isOwned ? '✅' : '❌'}</div>`;
            result += `<div class="info-item"><strong>Equipped:</strong> ${isEquipped ? '✅' : '❌'}</div>`;
            result += `<div class="info-item"><strong>Rarity:</strong> ${cardDef[1] || 'Unknown'}</div>`;
            result += `<div class="info-item"><strong>Base Value:</strong> ${cardDef[2] || 0}</div>`;
            result += `<div class="info-item"><strong>Bonus:</strong> ${cardDef[3] || 'No description'}</div>`;
            
            if (level < 5 && isOwned) {
                result += `<div class="info-item status-info"><strong>Cards needed for level ${level + 1}:</strong> ${cardsNeeded}</div>`;
            } else if (level >= 5) {
                result += `<div class="info-item status-info max-level"><strong>Status:</strong> ⭐ MAX LEVEL ⭐</div>`;
            } else {
                result += `<div class="info-item status-info"><strong>Status:</strong> Not owned</div>`;
            }
            result += `</div></div>`;
            
            return result;
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @js_export()
    def get_card_summary_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            const engine = ctx["com.stencyl.Engine"].engine;
            const pixelHelper = engine.getGameAttribute("PixelHelperActor");
            const cardData = engine.getGameAttribute("Cards");
            
            if (!pixelHelper || !pixelHelper[6] || !cardData) {
                throw new Error("Card data not accessible");
            }
            
            const cardDefs = pixelHelper[6].behaviors.getBehavior("ActorEvents_312")._GenINFO[45].h;
            const cardQuantities = cardData[0].h;
            const cardInventory = cardData[1] || [];
            const equippedCards = cardData[2] || [];
            
            function calculateCardLevel(cardId, quantity) {
                if (quantity <= 0) return 1;
                
                const baseReq = cardDefs[cardId][2] || 1;
                let level = 1;
                
                for (let i = 2; i <= 5; i++) {
                    let required;
                    if (cardId === "Boss3B") {
                        required = Math.ceil(1.5 * Math.pow(i + Math.floor((i-1) / 3), 2));
                    } else {
                        required = Math.ceil(baseReq * Math.pow(i + Math.floor((i-1) / 3) + 16 * Math.floor((i-1) / 4), 2));
                    }
                    
                    if (quantity >= required) {
                        level = i;
                    } else {
                        break;
                    }
                }
                
                return Math.min(level, 5);
            }
            
            let totalCards = 0;
            let ownedCards = 0;
            let maxLevelCards = 0;
            let totalQuantity = 0;
            let highestLevel = 0;
            const levelCounts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0};
            
            for (const cardId in cardDefs) {
                if (cardDefs[cardId] && cardDefs[cardId][0]) {
                    totalCards++;
                    const quantity = cardQuantities[cardId] || 0;
                    
                    if (quantity > 0) {
                        ownedCards++;
                        totalQuantity += quantity;
                        const level = calculateCardLevel(cardId, quantity);
                        levelCounts[level]++;
                        
                        if (level > highestLevel) {
                            highestLevel = level;
                        }
                        
                        if (level === 5) {
                            maxLevelCards++;
                        }
                    }
                }
            }
            
            const completionRate = ((ownedCards / totalCards) * 100).toFixed(1);
            const equippedCount = equippedCards.filter(card => card !== "B").length;
            
            let result = `<div class="card-summary">`;
            result += `<h3>📊 Card Collection Summary</h3>`;
            result += `<div class="summary-stats">`;
            result += `<div class="stat-item">🎴 <strong>Total Cards Available:</strong> ${totalCards}</div>`;
            result += `<div class="stat-item">✅ <strong>Cards Owned:</strong> ${ownedCards} (${completionRate}%)</div>`;
            result += `<div class="stat-item">❌ <strong>Cards Missing:</strong> ${totalCards - ownedCards}</div>`;
            result += `<div class="stat-item">⚔️ <strong>Cards Equipped:</strong> ${equippedCount}</div>`;
            result += `<div class="stat-item">⭐ <strong>Max Level Cards:</strong> ${maxLevelCards}</div>`;
            result += `<div class="stat-item">🏆 <strong>Highest Level:</strong> ${highestLevel}</div>`;
            result += `<div class="stat-item">📦 <strong>Total Card Quantity:</strong> ${totalQuantity.toLocaleString()}</div>`;
            result += `</div>`;
            
            result += `<h4>📈 Level Distribution:</h4>`;
            result += `<div class="level-distribution">`;
            for (let level = 1; level <= 5; level++) {
                const count = levelCounts[level];
                const percentage = ownedCards > 0 ? ((count / ownedCards) * 100).toFixed(1) : 0;
                const barWidth = ownedCards > 0 ? (count / ownedCards) * 100 : 0;
                result += `<div class="level-item">`;
                result += `<span class="level-label">Level ${level}:</span>`;
                result += `<span class="level-count">${count} cards (${percentage}%)</span>`;
                result += `<div class="level-bar"><div class="level-fill" style="width: ${barWidth}%"></div></div>`;
                result += `</div>`;
            }
            result += `</div></div>`;
            
            return result;
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @js_export(params=["search_term"])
    def search_cards_js(self, search_term=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            const engine = ctx["com.stencyl.Engine"].engine;
            const pixelHelper = engine.getGameAttribute("PixelHelperActor");
            const cardData = engine.getGameAttribute("Cards");
            
            if (!pixelHelper || !pixelHelper[6] || !cardData) {
                throw new Error("Card data not accessible");
            }
            
            const cardDefs = pixelHelper[6].behaviors.getBehavior("ActorEvents_312")._GenINFO[45].h;
            const cardQuantities = cardData[0].h;
            const searchTerm = search_term.toLowerCase();
            
            function calculateCardLevel(cardId, quantity) {
                if (quantity <= 0) return 1;
                
                const baseReq = cardDefs[cardId][2] || 1;
                let level = 1;
                
                for (let i = 2; i <= 5; i++) {
                    let required;
                    if (cardId === "Boss3B") {
                        required = Math.ceil(1.5 * Math.pow(i + Math.floor((i-1) / 3), 2));
                    } else {
                        required = Math.ceil(baseReq * Math.pow(i + Math.floor((i-1) / 3) + 16 * Math.floor((i-1) / 4), 2));
                    }
                    
                    if (quantity >= required) {
                        level = i;
                    } else {
                        break;
                    }
                }
                
                return Math.min(level, 5);
            }
            
            const matches = [];
            
            for (const cardId in cardDefs) {
                const cardDef = cardDefs[cardId];
                if (cardDef && cardDef[0]) {
                    const cardName = cardDef[0].toLowerCase();
                    const description = (cardDef[3] || '').toLowerCase();
                    
                    if (cardName.includes(searchTerm) || description.includes(searchTerm) || cardId.toLowerCase().includes(searchTerm)) {
                        const quantity = cardQuantities[cardId] || 0;
                        const level = calculateCardLevel(cardId, quantity);
                        
                        matches.push({
                            id: cardId,
                            name: cardDef[0],
                            quantity: quantity,
                            level: level,
                            isOwned: quantity > 0,
                            exactMatch: cardName === searchTerm
                        });
                    }
                }
            }
            
            matches.sort((a, b) => {
                if (a.exactMatch && !b.exactMatch) return -1;
                if (!a.exactMatch && b.exactMatch) return 1;
                return a.name.localeCompare(b.name);
            });
            
            if (matches.length === 0) {
                return `<div class="no-results">No cards found matching: "<strong>${search_term}</strong>"</div>`;
            }
            
            let result = `<div class="search-results">`;
            result += `<h3>🔍 Search Results for "${search_term}" (${matches.length} found)</h3>`;
            result += `<div class="card-list">`;
            
            matches.forEach((card, index) => {
                const status = card.isOwned ? `Lv.${card.level} (${card.quantity})` : 'Not owned';
                const statusClass = card.isOwned ? 'owned' : 'not-owned';
                result += `<div class="card-result">`;
                result += `<strong class="card-name">${card.name}</strong>`;
                result += `<span class="card-id">(${card.id})</span>`;
                result += `<span class="card-status ${statusClass}">${status}</span>`;
                result += `</div>`;
            });
            
            result += `</div></div>`;
            
            return result;
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @js_export()
    def list_all_cards_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            const engine = ctx["com.stencyl.Engine"].engine;
            const pixelHelper = engine.getGameAttribute("PixelHelperActor");
            const cardData = engine.getGameAttribute("Cards");
            
            if (!pixelHelper || !pixelHelper[6] || !cardData) {
                throw new Error("Card data not accessible");
            }
            
            const cardDefs = pixelHelper[6].behaviors.getBehavior("ActorEvents_312")._GenINFO[45].h;
            const cardQuantities = cardData[0].h;
            
            function calculateCardLevel(cardId, quantity) {
                if (quantity <= 0) return 1;
                
                const baseReq = cardDefs[cardId][2] || 1;
                let level = 1;
                
                for (let i = 2; i <= 5; i++) {
                    let required;
                    if (cardId === "Boss3B") {
                        required = Math.ceil(1.5 * Math.pow(i + Math.floor((i-1) / 3), 2));
                    } else {
                        required = Math.ceil(baseReq * Math.pow(i + Math.floor((i-1) / 3) + 16 * Math.floor((i-1) / 4), 2));
                    }
                    
                    if (quantity >= required) {
                        level = i;
                    } else {
                        break;
                    }
                }
                
                return Math.min(level, 5);
            }
            
            const allCards = [];
            
            for (const cardId in cardDefs) {
                const cardDef = cardDefs[cardId];
                if (cardDef && cardDef[0]) {
                    const quantity = cardQuantities[cardId] || 0;
                    const level = calculateCardLevel(cardId, quantity);
                    const status = quantity > 0 ? `Lv.${level} (${quantity})` : 'Not owned';
                    
                    allCards.push(`${cardDef[0]} | ${status} | ${cardDef[3] || 'No description'}`);
                }
            }
            
            allCards.sort((a, b) => a.split(' | ')[0].localeCompare(b.split(' | ')[0]));
            
            return allCards.join('\\n');
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @js_export(params=["card_name"])
    def unlock_card_js(self, card_name=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            const engine = ctx["com.stencyl.Engine"].engine;
            const pixelHelper = engine.getGameAttribute("PixelHelperActor");
            const cardData = engine.getGameAttribute("Cards");
            
            if (!pixelHelper || !pixelHelper[6] || !cardData) {
                throw new Error("Card data not accessible");
            }
            
            const cardDefs = pixelHelper[6].behaviors.getBehavior("ActorEvents_312")._GenINFO[45].h;
            
            // Find card by name
            let foundCardId = null;
            const searchTerm = card_name.toLowerCase();
            
            for (const cardId in cardDefs) {
                const cardDef = cardDefs[cardId];
                if (cardDef && cardDef[0]) {
                    const cardName = cardDef[0].toLowerCase();
                    if (cardName.includes(searchTerm) || cardId.toLowerCase().includes(searchTerm)) {
                        foundCardId = cardId;
                        if (cardName === searchTerm) break;
                    }
                }
            }
            
            if (!foundCardId) {
                return `No card found matching: "${card_name}"`;
            }
            
            const cardDef = cardDefs[foundCardId];
            const currentQuantity = cardData[0].h[foundCardId] || 0;
            
            if (currentQuantity > 0) {
                return `Card "${cardDef[0]}" is already unlocked (quantity: ${currentQuantity})`;
            }
            
            // Unlock the card
            cardData[0].h[foundCardId] = 1;
            
            if (!cardData[1].includes(foundCardId)) {
                cardData[1].push(foundCardId);
            }
            
            return `Successfully unlocked card: "${cardDef[0]}" (${foundCardId})`;
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @js_export(params=["card_name"])
    def set_card_max_level_js(self, card_name=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            const engine = ctx["com.stencyl.Engine"].engine;
            const pixelHelper = engine.getGameAttribute("PixelHelperActor");
            const cardData = engine.getGameAttribute("Cards");
            
            if (!pixelHelper || !pixelHelper[6] || !cardData) {
                throw new Error("Card data not accessible");
            }
            
            const cardDefs = pixelHelper[6].behaviors.getBehavior("ActorEvents_312")._GenINFO[45].h;
            
            // Find card by name
            let foundCardId = null;
            const searchTerm = card_name.toLowerCase();
            
            for (const cardId in cardDefs) {
                const cardDef = cardDefs[cardId];
                if (cardDef && cardDef[0]) {
                    const cardName = cardDef[0].toLowerCase();
                    if (cardName.includes(searchTerm) || cardId.toLowerCase().includes(searchTerm)) {
                        foundCardId = cardId;
                        if (cardName === searchTerm) break;
                    }
                }
            }
            
            if (!foundCardId) {
                return `No card found matching: "${card_name}"`;
            }
            
            const cardDef = cardDefs[foundCardId];
            const baseReq = cardDef[2] || 1;
            
            // Calculate level 5 requirement
            let level5Req;
            if (foundCardId === "Boss3B") {
                level5Req = Math.ceil(1.5 * Math.pow(5 + Math.floor((5-1) / 3), 2));
            } else {
                level5Req = Math.ceil(baseReq * Math.pow(5 + Math.floor((5-1) / 3) + 16 * Math.floor((5-1) / 4), 2));
            }
            
            // Set card to max level
            cardData[0].h[foundCardId] = level5Req;
            
            if (!cardData[1].includes(foundCardId)) {
                cardData[1].push(foundCardId);
            }
            
            return `Set "${cardDef[0]}" to max level (quantity: ${level5Req})`;
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @js_export(params=["card_name"])
    def reset_card_level_js(self, card_name=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            const engine = ctx["com.stencyl.Engine"].engine;
            const pixelHelper = engine.getGameAttribute("PixelHelperActor");
            const cardData = engine.getGameAttribute("Cards");
            
            if (!pixelHelper || !pixelHelper[6] || !cardData) {
                throw new Error("Card data not accessible");
            }
            
            const cardDefs = pixelHelper[6].behaviors.getBehavior("ActorEvents_312")._GenINFO[45].h;
            
            // Find card by name
            let foundCardId = null;
            const searchTerm = card_name.toLowerCase();
            
            for (const cardId in cardDefs) {
                const cardDef = cardDefs[cardId];
                if (cardDef && cardDef[0]) {
                    const cardName = cardDef[0].toLowerCase();
                    if (cardName.includes(searchTerm) || cardId.toLowerCase().includes(searchTerm)) {
                        foundCardId = cardId;
                        if (cardName === searchTerm) break;
                    }
                }
            }
            
            if (!foundCardId) {
                return `No card found matching: "${card_name}"`;
            }
            
            const cardDef = cardDefs[foundCardId];
            const currentQuantity = cardData[0].h[foundCardId] || 0;
            
            if (currentQuantity === 0) {
                return `Card "${cardDef[0]}" is not owned`;
            }
            
            // Reset to level 1 (quantity = 1)
            cardData[0].h[foundCardId] = 1;
            
            return `Reset "${cardDef[0]}" to level 1 (quantity: 1)`;
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @js_export()
    def set_all_cards_max_level_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            const engine = ctx["com.stencyl.Engine"].engine;
            const pixelHelper = engine.getGameAttribute("PixelHelperActor");
            const cardData = engine.getGameAttribute("Cards");
            
            if (!pixelHelper || !pixelHelper[6] || !cardData) {
                throw new Error("Card data not accessible");
            }
            
            const cardDefs = pixelHelper[6].behaviors.getBehavior("ActorEvents_312")._GenINFO[45].h;
            const cardQuantities = cardData[0].h;
            
            let updatedCount = 0;
            
            for (const cardId in cardDefs) {
                const cardDef = cardDefs[cardId];
                if (cardDef && cardDef[0] && cardQuantities[cardId] && cardQuantities[cardId] > 0) {
                    const baseReq = cardDef[2] || 1;
                    
                    // Calculate level 5 requirement
                    let level5Req;
                    if (cardId === "Boss3B") {
                        level5Req = Math.ceil(1.5 * Math.pow(5 + Math.floor((5-1) / 3), 2));
                    } else {
                        level5Req = Math.ceil(baseReq * Math.pow(5 + Math.floor((5-1) / 3) + 16 * Math.floor((5-1) / 4), 2));
                    }
                    
                    if (cardQuantities[cardId] < level5Req) {
                        cardQuantities[cardId] = level5Req;
                        updatedCount++;
                    }
                }
            }
            
            return `Set ${updatedCount} owned cards to maximum level!`;
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @js_export()
    def unlock_all_missing_cards_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            const engine = ctx["com.stencyl.Engine"].engine;
            const pixelHelper = engine.getGameAttribute("PixelHelperActor");
            const cardData = engine.getGameAttribute("Cards");
            
            if (!pixelHelper || !pixelHelper[6] || !cardData) {
                throw new Error("Card data not accessible");
            }
            
            const cardDefs = pixelHelper[6].behaviors.getBehavior("ActorEvents_312")._GenINFO[45].h;
            const cardQuantities = cardData[0].h;
            
            let unlockedCount = 0;
            const unlockedCards = [];
            
            for (const cardId in cardDefs) {
                const cardDef = cardDefs[cardId];
                if (cardDef && cardDef[0]) {
                    const currentQuantity = cardQuantities[cardId] || 0;
                    
                    if (currentQuantity === 0) {
                        cardQuantities[cardId] = 1;
                        
                        if (!cardData[1].includes(cardId)) {
                            cardData[1].push(cardId);
                        }
                        
                        unlockedCards.push(cardDef[0]);
                        unlockedCount++;
                    }
                }
            }
            
            if (unlockedCount === 0) {
                return "All cards are already unlocked!";
            }
            
            return `Successfully unlocked ${unlockedCount} missing cards!`;
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @js_export()
    def remove_all_cards_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            const engine = ctx["com.stencyl.Engine"].engine;
            const cardData = engine.getGameAttribute("Cards");
            
            if (!cardData) {
                throw new Error("Card data not accessible");
            }
            
            // Clear all card quantities
            const cardQuantities = cardData[0].h;
            let removedCount = 0;
            
            for (const cardId in cardQuantities) {
                if (cardQuantities[cardId] > 0) {
                    removedCount++;
                }
                cardQuantities[cardId] = 0;
            }
            
            // Clear card inventory
            cardData[1].length = 0;
            
            // Clear equipped cards
            if (cardData[2]) {
                for (let i = 0; i < cardData[2].length; i++) {
                    cardData[2][i] = "B"; // B represents empty slot
                }
            }
            
            return `⚠️ Removed all cards! (${removedCount} cards were deleted)`;
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

plugin_class = CardCheatsPlugin
