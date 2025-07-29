from plugin_system import PluginBase, js_export, ui_toggle

class CandyUnlockPlugin(PluginBase):
    VERSION = "1.0.1"
    DESCRIPTION = "Allows the use of Time Candy anywhere, bypassing all map restrictions."
    PLUGIN_ORDER = 3
    CATEGORY = "Unlocks"

    def __init__(self, config=None):
        super().__init__(config or {})
        self.name = 'candy_unlock'

    async def cleanup(self): pass
    async def update(self): pass
    async def on_config_changed(self, config): 
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)
    async def on_game_ready(self): pass

    @ui_toggle(
        label="Unlock Candy Usage Everywhere",
        description="Allows using Time Candy in all maps, including dark places and World 6.",
        config_key="unlock_candy",
        default_value=True
    )
    async def unlock_candy_ui(self, value: bool = None):
        if value is not None:
            self.config["unlock_candy"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector and value:
                return await self.enable_candy_unlock(self.injector)
        return f"Candy unlock is {'enabled' if self.config.get('unlock_candy', False) else 'disabled'}"

    @js_export()
    def enable_candy_unlock_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            
            // Try different paths to find the item move function
            let itemMoveFn = null;
            let scriptsPath = null;
            
            // Try the events path first
            if (ctx["events"] && ctx["events"](38)) {
                itemMoveFn = ctx["events"](38).prototype._event_InvItem4custom;
                scriptsPath = ctx["events"](38);
            }
            // Try scripts path as fallback
            else if (ctx["scripts"] && ctx["scripts"]["ActorEvents_38"]) {
                itemMoveFn = ctx["scripts"]["ActorEvents_38"].prototype._event_InvItem4custom;
                scriptsPath = ctx["scripts"]["ActorEvents_38"];
            }
            // Try direct access
            else if (window.ActorEvents_38) {
                itemMoveFn = window.ActorEvents_38.prototype._event_InvItem4custom;
                scriptsPath = window.ActorEvents_38;
            }
            
            if (!itemMoveFn) {
                // Fallback: try to find any function that handles item usage
                console.log("Item move function not found, trying alternative approach...");
                
                // Set a global flag that can be checked by the game
                bEngine.getGameAttribute("PixelHelperActor")[23].getValue("ActorEvents_577", "_GenINFO")[86] = 1;
                
                // Try to patch the candy restriction check directly
                if (window.canUseCandy !== undefined) {
                    const originalCanUseCandy = window.canUseCandy;
                    window.canUseCandy = function() { return true; };
                }
                
                if (window.isCandyRestricted !== undefined) {
                    const originalIsCandyRestricted = window.isCandyRestricted;
                    window.isCandyRestricted = function() { return false; };
                }
                
                return "Candy restriction bypassed using fallback method (global flags set)";
            }
            
            // Create a proxy to intercept candy usage
            scriptsPath.prototype._event_InvItem4custom = new Proxy(itemMoveFn, {
                apply: function(originalFn, context, argumentsList) {
                    const inventoryOrder = bEngine.getGameAttribute("InventoryOrder");
                    try {
                        // Check if this is a TIME_CANDY item
                        const itemDragID = context.actor.getValue("ActorEvents_38", "_ItemDragID");
                        const itemType = bEngine.getGameAttribute("ItemDefinitionsGET").h[inventoryOrder[itemDragID]]?.h?.Type;
                        
                        if (itemType === "TIME_CANDY") {
                            // Store original values
                            let originalMap = bEngine.getGameAttribute("CurrentMap");
                            let originalTarget = bEngine.getGameAttribute("AFKtarget");
                            
                            // Set a flag to indicate candy usage
                            bEngine.getGameAttribute("PixelHelperActor")[23].getValue("ActorEvents_577", "_GenINFO")[86] = 1;
                            
                            // Handle special cases for Cooking/Laboratory
                            if (originalTarget === "Cooking" || originalTarget === "Laboratory") {
                                let newTarget = {
                                    calls: 0,
                                    [Symbol.toPrimitive](hint) {
                                        if (this.calls < 2) {
                                            this.calls = this.calls + 1;
                                            return "mushG";
                                        }
                                        bEngine.setGameAttribute("AFKtarget", originalTarget);
                                        return originalTarget;
                                    },
                                };
                                bEngine.setGameAttribute("AFKtarget", newTarget);
                            }
                            
                            // Temporarily change map to allow candy usage
                            bEngine.setGameAttribute("CurrentMap", 1);
                            
                            // Execute the original function
                            let result = Reflect.apply(originalFn, context, argumentsList);
                            
                            // Restore original values
                            bEngine.setGameAttribute("CurrentMap", originalMap);
                            bEngine.setGameAttribute("AFKtarget", originalTarget);
                            
                            return result;
                        }
                    } catch (e) {
                        console.log("Candy bypass error:", e);
                    }
                    
                    // For non-candy items, use original function
                    return Reflect.apply(originalFn, context, argumentsList);
                }
            });
            
            return "Candy usage restriction bypassed using proper proxy method!";
        } catch (e) {
            return "Error unlocking candy usage: " + e.message;
        }
        '''
    async def enable_candy_unlock(self, injector):
        return self.run_js_export('enable_candy_unlock_js', injector)

plugin_class = CandyUnlockPlugin 