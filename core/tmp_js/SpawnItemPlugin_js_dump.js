window.list_items = async function() {

                        try {
                            // Wait for game to be ready before executing plugin function
                            await window.__idleon_wait_for_game_ready();
                            
                            
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const itemDefs = ctx["com.stencyl.Engine"].engine.getGameAttribute("ItemDefinitionsGET").h;
            
            return Object.entries(itemDefs)
                .map(([id, def]) => `${id} : ${def?.h?.displayName?.replace(/_/g, ' ') || id}`)
                .join("\n");
        } catch (e) {
            return `Error: ${e.message}`;
        }
        
                        } catch (e) {
                            console.error('[list_items] Error:', e);
                            return `Error: ${e.message}`;
                        }
                        
}
window.search_items = async function(query) {

                        try {
                            // Wait for game to be ready before executing plugin function
                            await window.__idleon_wait_for_game_ready();
                            
                            
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const itemDefs = ctx["com.stencyl.Engine"].engine.getGameAttribute("ItemDefinitionsGET").h;
            const q = query.toLowerCase().trim();
            
            const matches = Object.entries(itemDefs).filter(([id, def]) => {
                const name = def?.h?.displayName || '';
                return id.toLowerCase().includes(q) || name.toLowerCase().includes(q);
            });
            
            return matches.length 
                ? matches.map(([id, def]) => `${id} : ${def?.h?.displayName?.replace(/_/g, ' ') || id}`).join("\n")
                : `No items found for: ${query}`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        
                        } catch (e) {
                            console.error('[search_items] Error:', e);
                            return `Error: ${e.message}`;
                        }
                        
}
window.spawn_item = async function(item, amount) {

                        try {
                            // Wait for game to be ready before executing plugin function
                            await window.__idleon_wait_for_game_ready();
                            
                            
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const engine = ctx["com.stencyl.Engine"].engine;
            const itemDefs = engine.getGameAttribute("ItemDefinitionsGET").h;
            const character = engine.getGameAttribute("OtherPlayers").h[engine.getGameAttribute("UserInfo")[0]];
            
            let dropFn = typeof events === 'function' ? events(189) : ctx?.scripts?.["ActorEvents_189"];
            if (!dropFn?._customBlock_DropSomething) throw new Error("Drop function not found");
            
            const itemDef = itemDefs[item];
            if (!itemDef) return `No item found: '${item}'`;
            
            const x = character.getXCenter();
            const y = character.getValue("ActorEvents_20", "_PlayerNode");
            
            if (item.includes("SmithingRecipes")) {
                dropFn._customBlock_DropSomething(item, 0, amount, 0, 2, y, 0, x, y);
            } else {
                dropFn._customBlock_DropSomething(item, amount, 0, 0, 2, y, 0, x, y);
            }
            
            return `Dropped ${itemDef.h.displayName.replace(/_/g, " ")} (x${amount})`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        
                        } catch (e) {
                            console.error('[spawn_item] Error:', e);
                            return `Error: ${e.message}`;
                        }
                        
}
