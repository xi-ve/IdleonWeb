window.list_items = function() {

        console.log('list_items called');
        try {
            let bEngine = null;
            if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
                bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
            }
            if (!bEngine) {
                throw new Error("bEngine (game engine) not found in this context");
            }
            const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            let out = [];
            for (const [id, def] of Object.entries(itemDefs)) {
                if (def && def.h && def.h.displayName) {
                    out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
                } else {
                    out.push(id);
                }
            }
            let result = out.join("\n");
            return result;
        } catch (e) {
            return "JS ERROR: " + (e && e.stack ? e.stack : e);
        }
        
}
window.search_items = function(query) {

        console.log('search_items called', query);
        try {
            let bEngine = null;
            if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
                bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
            }
            if (!bEngine) {
                throw new Error("bEngine (game engine) not found in this context");
            }
            const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            let out = [];
            let q = query.toLowerCase().trim();
            for (const [id, def] of Object.entries(itemDefs)) {
                let displayName = def && def.h && typeof def.h.displayName === 'string' ? def.h.displayName : '';
                if (
                    (id && id.toLowerCase().includes(q)) ||
                    (displayName && displayName.toLowerCase().includes(q))
                ) {
                    out.push(`${id} : ${displayName.replace(/_/g, ' ')}`);
                }
            }
            let result = out.length ? out.join("\n") : `No items found for query: ${query}`;
            return result;
        } catch (e) {
            return "JS ERROR: " + (e && e.stack ? e.stack : e);
        }
        
}
window.spawn_item = function(item, amount) {

        try {
            let ctx = this;
            if (!ctx["com.stencyl.Engine"] && typeof getIdleonContext === 'function') {
                ctx = getIdleonContext();
            }
            console.log('spawn_item called with', item, amount);
            if (!ctx["com.stencyl.Engine"] || !ctx["com.stencyl.Engine"].engine) {
                console.error('spawn_item: Game engine not ready.');
                throw new Error("Game engine not ready.");
            }
            let bEngine = ctx["com.stencyl.Engine"].engine;
            let itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            let character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
            let actorEvents189 = ctx.scripts && ctx.scripts["ActorEvents_189"];
            if (!actorEvents189 || typeof actorEvents189._customBlock_DropSomething !== 'function') {
                if (typeof events === 'function') {
                    actorEvents189 = events(189);
                }
            }
            if (!actorEvents189 || typeof actorEvents189._customBlock_DropSomething !== 'function') {
                console.error('spawn_item: Could not find _customBlock_DropSomething');
                throw new Error('Could not find _customBlock_DropSomething');
            }
            const itemDefinition = itemDefs[item];
            let result;
            if (itemDefinition) {
                let x = character.getXCenter();
                let y = character.getValue("ActorEvents_20", "_PlayerNode");
                if (item.includes("SmithingRecipes"))
                    actorEvents189._customBlock_DropSomething(item, 0, amount, 0, 2, y, 0, x, y);
                else
                    actorEvents189._customBlock_DropSomething(item, amount, 0, 0, 2, y, 0, x, y);
                result = `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x${amount})`;
            } else {
                result = `No item found for '${item}'`;
            }
            console.log('spawn_item result:', result);
            return result;
        } catch (err) {
            console.error('spawn_item error:', err && err.stack ? err.stack : err);
            return `Error: ${err && err.stack ? err.stack : err}`;
        }
        
}
