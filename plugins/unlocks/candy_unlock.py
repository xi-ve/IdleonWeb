from plugin_system import PluginBase, js_export, ui_toggle

class CandyUnlockPlugin(PluginBase):
    VERSION = "1.1.0"
    DESCRIPTION = "Allows the use of Time Candy anywhere, bypassing all map restrictions, dark places, and activity-specific blocks like Cooking/Laboratory."
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
        description="Allows using Time Candy in all maps, activities, and locations including dark places, World 6, Cooking, Laboratory, Worship, and any other restricted areas.",
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
            
            if (window.__candyUnlockPatched) {
                return "Candy usage restrictions already removed!";
            }
            
            const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            const events = function (num) {
                return ctx["scripts.ActorEvents_" + num];
            };
            
            if (events(38) && events(38).prototype && events(38).prototype._event_InvItem4custom) {
                const originalFn = events(38).prototype._event_InvItem4custom;
                
                events(38).prototype._event_InvItem4custom = function(...argumentsList) {
                    const inventoryOrder = bEngine.getGameAttribute("InventoryOrder");
                    
                    try {
                        const itemIndex = this.actor.getValue("ActorEvents_38", "_ItemDragID");
                        const itemName = inventoryOrder[itemIndex];
                        
                        if (itemDefs[itemName] && itemDefs[itemName].h.Type === "TIME_CANDY") {
                            let originalMap = bEngine.getGameAttribute("CurrentMap");
                            let originalTarget = bEngine.getGameAttribute("AFKtarget");
                            
                            try {
                                bEngine.getGameAttribute("PixelHelperActor")[23]
                                    .getValue("ActorEvents_577", "_GenINFO")[86] = 1;
                            } catch (e) {
                                console.log("Could not set PixelHelperActor flag:", e);
                            }
                            
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
                            
                            bEngine.setGameAttribute("CurrentMap", 1);
                            
                            let result = originalFn.apply(this, argumentsList);
                            
                            bEngine.setGameAttribute("CurrentMap", originalMap);
                            bEngine.setGameAttribute("AFKtarget", originalTarget);
                            
                            return result;
                        }
                    } catch (e) {
                        console.log("Error in candy unlock:", e);
                    }
                    
                    return originalFn.apply(this, argumentsList);
                };
                
                window.__candyUnlockPatched = true;
                return "✅ Candy usage restrictions removed! Time Candy can now be used anywhere using the same method as the built-in cheats.";
            } else {
                throw new Error("Could not find _event_InvItem4custom function in ActorEvents_38");
            }
        } catch (e) {
            return "Error unlocking candy usage: " + e.message;
        }
        '''
    async def enable_candy_unlock(self, injector):
        return self.run_js_export('enable_candy_unlock_js', injector)

plugin_class = CandyUnlockPlugin 