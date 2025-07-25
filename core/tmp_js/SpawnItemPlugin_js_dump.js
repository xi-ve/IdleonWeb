window.list_items = function() {

        let out = [];
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            } else {
                out.push(id);
            }
        }
        return out.join("
");
        
}
window.list_items = function() {

        let out = [];
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            } else {
                out.push(id);
            }
        }
        return out.join("
");
        
}
window.list_items = function() {

        let out = [];
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            } else {
                out.push(id);
            }
        }
        return out.join("
");
        
}
window.list_items = function() {

        let out = [];
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            } else {
                out.push(id);
            }
        }
        return out.join("
");
        
}
window.list_items = function() {

        let out = [];
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            } else {
                out.push(id);
            }
        }
        return out.join("
");
        
}
window.search_items = function(query) {

        let out = [];
        let q = "".toLowerCase();
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName && def.h.displayName.toLowerCase().includes(q)) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            }
        }
        return out.length ? out.join("
") : `No items found for query: `;
        
}
window.spawn_item = function(item, amount) {

        // The following JS code runs in the browser context
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
        const itemDefinition = itemDefs[item];
        if (itemDefinition) {
            let x = character.getXCenter();
            let y = character.getValue("ActorEvents_20", "_PlayerNode");
            if (item.includes("SmithingRecipes"))
                actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
            else
                actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
            return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
        } else {
            return `No item found for '${item}'`;
        }
        
}
window.list_items = function() {

        let out = [];
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            } else {
                out.push(id);
            }
        }
        return out.join("
");
        
}
window.search_items = function(query) {

        let out = [];
        let q = "".toLowerCase();
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName && def.h.displayName.toLowerCase().includes(q)) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            }
        }
        return out.length ? out.join("
") : `No items found for query: `;
        
}
window.spawn_item = function(item, amount) {

        // The following JS code runs in the browser context
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
        const itemDefinition = itemDefs[item];
        if (itemDefinition) {
            let x = character.getXCenter();
            let y = character.getValue("ActorEvents_20", "_PlayerNode");
            if (item.includes("SmithingRecipes"))
                actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
            else
                actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
            return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
        } else {
            return `No item found for '${item}'`;
        }
        
}
window.list_items = function() {

        let out = [];
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            } else {
                out.push(id);
            }
        }
        return out.join("
");
        
}
window.search_items = function(query) {

        let out = [];
        let q = "".toLowerCase();
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName && def.h.displayName.toLowerCase().includes(q)) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            }
        }
        return out.length ? out.join("
") : `No items found for query: `;
        
}
window.spawn_item = function(item, amount) {

        // The following JS code runs in the browser context
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
        const itemDefinition = itemDefs[item];
        if (itemDefinition) {
            let x = character.getXCenter();
            let y = character.getValue("ActorEvents_20", "_PlayerNode");
            if (item.includes("SmithingRecipes"))
                actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
            else
                actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
            return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
        } else {
            return `No item found for '${item}'`;
        }
        
}
window.list_items = function() {

        let out = [];
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            } else {
                out.push(id);
            }
        }
        return out;
        
}
window.search_items = function(query) {

        let out = [];
        let q = "".toLowerCase();
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName && def.h.displayName.toLowerCase().includes(q)) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            }
        }
        return out.length ? out.join("
") : `No items found for query: `;
        
}
window.spawn_item = function(item, amount) {

        // The following JS code runs in the browser context
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
        const itemDefinition = itemDefs[item];
        if (itemDefinition) {
            let x = character.getXCenter();
            let y = character.getValue("ActorEvents_20", "_PlayerNode");
            if (item.includes("SmithingRecipes"))
                actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
            else
                actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
            return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
        } else {
            return `No item found for '${item}'`;
        }
        
}
window.list_items = function() {

        let out = [];
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            } else {
                out.push(id);
            }
        }
        return out;
        
}
window.search_items = function(query) {

        let out = [];
        let q = "".toLowerCase();
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName && def.h.displayName.toLowerCase().includes(q)) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            }
        }
        return out.length ? out.join("
") : `No items found for query: `;
        
}
window.spawn_item = function(item, amount) {

        // The following JS code runs in the browser context
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
        const itemDefinition = itemDefs[item];
        if (itemDefinition) {
            let x = character.getXCenter();
            let y = character.getValue("ActorEvents_20", "_PlayerNode");
            if (item.includes("SmithingRecipes"))
                actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
            else
                actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
            return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
        } else {
            return `No item found for '${item}'`;
        }
        
}
window.list_items = function() {

        let out = [];
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            } else {
                out.push(id);
            }
        }
        return out;
        
}
window.search_items = function(query) {

        let out = [];
        let q = "".toLowerCase();
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName && def.h.displayName.toLowerCase().includes(q)) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            }
        }
        return out.length ? out.join("
") : `No items found for query: `;
        
}
window.spawn_item = function(item, amount) {

        // The following JS code runs in the browser context
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
        const itemDefinition = itemDefs[item];
        if (itemDefinition) {
            let x = character.getXCenter();
            let y = character.getValue("ActorEvents_20", "_PlayerNode");
            if (item.includes("SmithingRecipes"))
                actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
            else
                actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
            return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
        } else {
            return `No item found for '${item}'`;
        }
        
}
window.list_items = function() {

        let out = [];
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            } else {
                out.push(id);
            }
        }
        return out;
        
}
window.search_items = function(query) {

        let out = [];
        let q = "".toLowerCase();
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName && def.h.displayName.toLowerCase().includes(q)) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            }
        }
        return out.length ? out.join("
") : `No items found for query: `;
        
}
window.spawn_item = function(item, amount) {

        // The following JS code runs in the browser context
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
        const itemDefinition = itemDefs[item];
        if (itemDefinition) {
            let x = character.getXCenter();
            let y = character.getValue("ActorEvents_20", "_PlayerNode");
            if (item.includes("SmithingRecipes"))
                actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
            else
                actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
            return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
        } else {
            return `No item found for '${item}'`;
        }
        
}
window.list_items = function() {

        let out = [];
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            } else {
                out.push(id);
            }
        }
        return out;
        
}
window.search_items = function(query) {

        let out = [];
        let q = "Filler".toLowerCase();
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName && def.h.displayName.toLowerCase().includes(q)) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            }
        }
        return out.length ? out.join("
") : `No items found for query: Filler`;
        
}
window.spawn_item = function(item, amount) {

        // The following JS code runs in the browser context
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
        const itemDefinition = itemDefs[item];
        if (itemDefinition) {
            let x = character.getXCenter();
            let y = character.getValue("ActorEvents_20", "_PlayerNode");
            if (item.includes("SmithingRecipes"))
                actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
            else
                actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
            return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
        } else {
            return `No item found for '${item}'`;
        }
        
}
window.list_items = function() {

        let out = [];
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            } else {
                out.push(id);
            }
        }
        return out;
        
}
window.search_items = function(query) {

        let out = [];
        let q = "Filler".toLowerCase();
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName && def.h.displayName.toLowerCase().includes(q)) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            }
        }
        return out.length ? out.join("OK") : `No items found for query: Filler`;
        
}
window.spawn_item = function(item, amount) {

        // The following JS code runs in the browser context
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
        const itemDefinition = itemDefs[item];
        if (itemDefinition) {
            let x = character.getXCenter();
            let y = character.getValue("ActorEvents_20", "_PlayerNode");
            if (item.includes("SmithingRecipes"))
                actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
            else
                actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
            return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
        } else {
            return `No item found for '${item}'`;
        }
        
}
window.list_items = function() {

        let out = [];
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            } else {
                out.push(id);
            }
        }
        return out;
        
}
window.search_items = function(query) {

        let out = [];
        let q = "Filler".toLowerCase();
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName && def.h.displayName.toLowerCase().includes(q)) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            }
        }
        return out.length ? out.join("OK") : `No items found for query: Filler`;
        
}
window.spawn_item = function(item, amount) {

        // The following JS code runs in the browser context
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
        const itemDefinition = itemDefs[item];
        if (itemDefinition) {
            let x = character.getXCenter();
            let y = character.getValue("ActorEvents_20", "_PlayerNode");
            if (item.includes("SmithingRecipes"))
                actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
            else
                actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
            return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
        } else {
            return `No item found for '${item}'`;
        }
        
}
window.list_items = function() {

        let out = [];
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            } else {
                out.push(id);
            }
        }
        return out;
        
}
window.search_items = function(query) {

        let out = [];
        let q = "Filler".toLowerCase();
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName && def.h.displayName.toLowerCase().includes(q)) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            }
        }
        return out.length ? out.join("\n") : `No items found for query: Filler`;
        
}
window.spawn_item = function(item, amount) {

        // The following JS code runs in the browser context
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
        const itemDefinition = itemDefs[item];
        if (itemDefinition) {
            let x = character.getXCenter();
            let y = character.getValue("ActorEvents_20", "_PlayerNode");
            if (item.includes("SmithingRecipes"))
                actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
            else
                actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
            return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
        } else {
            return `No item found for '${item}'`;
        }
        
}
window.list_items = function() {

        let out = [];
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            } else {
                out.push(id);
            }
        }
        return out;
        
}
window.search_items = function(query) {

        let out = [];
        let q = "Filler".toLowerCase();
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName && def.h.displayName.toLowerCase().includes(q)) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            }
        }
        return out.length ? out.join("\n") : `No items found for query: Filler`;
        
}
window.spawn_item = function(item, amount) {

        // The following JS code runs in the browser context
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
        const itemDefinition = itemDefs[item];
        if (itemDefinition) {
            let x = character.getXCenter();
            let y = character.getValue("ActorEvents_20", "_PlayerNode");
            if (item.includes("SmithingRecipes"))
                actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
            else
                actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
            return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
        } else {
            return `No item found for '${item}'`;
        }
        
}
window.list_items = function() {

        let out = [];
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            } else {
                out.push(id);
            }
        }
        return out;
        
}
window.search_items = function(query) {

        let out = [];
        let q = "Filler".toLowerCase();
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName && def.h.displayName.toLowerCase().includes(q)) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            }
        }
        return out.length ? out.join("\n") : `No items found for query: Filler`;
        
}
window.spawn_item = function(item, amount) {

        // The following JS code runs in the browser context
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
        const itemDefinition = itemDefs[item];
        if (itemDefinition) {
            let x = character.getXCenter();
            let y = character.getValue("ActorEvents_20", "_PlayerNode");
            if (item.includes("SmithingRecipes"))
                actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
            else
                actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
            return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
        } else {
            return `No item found for '${item}'`;
        }
        
}
window.list_items = function() {

        // Ensure itemDefs is available
        const itemDefs = (typeof window.itemDefs !== 'undefined')
            ? window.itemDefs
            : bEngine.getGameAttribute("ItemDefinitionsGET").h;
        let out = [];
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            } else {
                out.push(id);
            }
        }
        return out.join("
");
        
}
window.search_items = function(query) {

        // Ensure itemDefs is available
        const itemDefs = (typeof window.itemDefs !== 'undefined')
            ? window.itemDefs
            : bEngine.getGameAttribute("ItemDefinitionsGET").h;
        let out = [];
        let q = "".toLowerCase();
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName && def.h.displayName.toLowerCase().includes(q)) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            }
        }
        return out.length ? out.join("
") : `No items found for query: `;
        
}
window.spawn_item = function(item, amount) {

        // Ensure itemDefs is available
        const itemDefs = (typeof window.itemDefs !== 'undefined')
            ? window.itemDefs
            : bEngine.getGameAttribute("ItemDefinitionsGET").h;
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
        const itemDefinition = itemDefs[item];
        if (itemDefinition) {
            let x = character.getXCenter();
            let y = character.getValue("ActorEvents_20", "_PlayerNode");
            if (item.includes("SmithingRecipes"))
                actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
            else
                actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
            return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
        } else {
            return `No item found for '${item}'`;
        }
        
}
window.list_items = function() {

        // Ensure itemDefs is available
        const itemDefs = (typeof window.itemDefs !== 'undefined')
            ? window.itemDefs
            : bEngine.getGameAttribute("ItemDefinitionsGET").h;
        let out = [];
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            } else {
                out.push(id);
            }
        }
        return out.join("
");
        
}
window.search_items = function(query) {

        // Ensure itemDefs is available
        const itemDefs = (typeof window.itemDefs !== 'undefined')
            ? window.itemDefs
            : bEngine.getGameAttribute("ItemDefinitionsGET").h;
        let out = [];
        let q = "".toLowerCase();
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName && def.h.displayName.toLowerCase().includes(q)) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            }
        }
        return out.length ? out.join("\n") : `No items found for query: `;
        
}
window.spawn_item = function(item, amount) {

        // Ensure itemDefs is available
        const itemDefs = (typeof window.itemDefs !== 'undefined')
            ? window.itemDefs
            : bEngine.getGameAttribute("ItemDefinitionsGET").h;
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
        const itemDefinition = itemDefs[item];
        if (itemDefinition) {
            let x = character.getXCenter();
            let y = character.getValue("ActorEvents_20", "_PlayerNode");
            if (item.includes("SmithingRecipes"))
                actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
            else
                actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
            return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
        } else {
            return `No item found for '${item}'`;
        }
        
}
window.list_items = function() {

        // Ensure itemDefs is available
        const itemDefs = (typeof window.itemDefs !== 'undefined')
            ? window.itemDefs
            : bEngine.getGameAttribute("ItemDefinitionsGET").h;
        let out = [];
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            } else {
                out.push(id);
            }
        }
        return out.join("\n");
        
}
window.search_items = function(query) {

        // Ensure itemDefs is available
        const itemDefs = (typeof window.itemDefs !== 'undefined')
            ? window.itemDefs
            : bEngine.getGameAttribute("ItemDefinitionsGET").h;
        let out = [];
        let q = "".toLowerCase();
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName && def.h.displayName.toLowerCase().includes(q)) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            }
        }
        return out.length ? out.join("\n") : `No items found for query: `;
        
}
window.spawn_item = function(item, amount) {

        // Ensure itemDefs is available
        const itemDefs = (typeof window.itemDefs !== 'undefined')
            ? window.itemDefs
            : bEngine.getGameAttribute("ItemDefinitionsGET").h;
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
        const itemDefinition = itemDefs[item];
        if (itemDefinition) {
            let x = character.getXCenter();
            let y = character.getValue("ActorEvents_20", "_PlayerNode");
            if (item.includes("SmithingRecipes"))
                actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
            else
                actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
            return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
        } else {
            return `No item found for '${item}'`;
        }
        
}
window.list_items = function() {

        // Robust bEngine detection
        let bEngine = null;
        if (typeof window !== 'undefined') {
            if (window["com"] && window["com"].stencyl && window["com"].stencyl.Engine && window["com"].stencyl.Engine.engine) {
                bEngine = window["com"].stencyl.Engine.engine;
            } else if (window.u && window.u["com.stencyl.Engine"] && window.u["com.stencyl.Engine"].engine) {
                bEngine = window.u["com.stencyl.Engine"].engine;
            }
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
        return out.join("\n");
        
}
window.search_items = function(query) {

        // Robust bEngine detection
        let bEngine = null;
        if (typeof window !== 'undefined') {
            if (window["com"] && window["com"].stencyl && window["com"].stencyl.Engine && window["com"].stencyl.Engine.engine) {
                bEngine = window["com"].stencyl.Engine.engine;
            } else if (window.u && window.u["com.stencyl.Engine"] && window.u["com.stencyl.Engine"].engine) {
                bEngine = window.u["com.stencyl.Engine"].engine;
            }
        }
        if (!bEngine) {
            throw new Error("bEngine (game engine) not found in this context");
        }
        const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
        let out = [];
        let q = "".toLowerCase();
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName && def.h.displayName.toLowerCase().includes(q)) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            }
        }
        return out.length ? out.join("\n") : `No items found for query: `;
        
}
window.spawn_item = function(item, amount) {

        // Robust bEngine detection
        let bEngine = null;
        if (typeof window !== 'undefined') {
            if (window["com"] && window["com"].stencyl && window["com"].stencyl.Engine && window["com"].stencyl.Engine.engine) {
                bEngine = window["com"].stencyl.Engine.engine;
            } else if (window.u && window.u["com.stencyl.Engine"] && window.u["com.stencyl.Engine"].engine) {
                bEngine = window.u["com.stencyl.Engine"].engine;
            }
        }
        if (!bEngine) {
            throw new Error("bEngine (game engine) not found in this context");
        }
        const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
        const itemDefinition = itemDefs[item];
        if (itemDefinition) {
            let x = character.getXCenter();
            let y = character.getValue("ActorEvents_20", "_PlayerNode");
            if (item.includes("SmithingRecipes"))
                actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
            else
                actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
            return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
        } else {
            return `No item found for '${item}'`;
        }
        
}
window.list_items = function() {

        // Robust bEngine detection
        let bEngine = null;
        if (typeof window !== 'undefined') {
            if (window["com"] && window["com"].stencyl && window["com"].stencyl.Engine && window["com"].stencyl.Engine.engine) {
                bEngine = window["com"].stencyl.Engine.engine;
            } else if (window.u && window.u["com.stencyl.Engine"] && window.u["com.stencyl.Engine"].engine) {
                bEngine = window.u["com.stencyl.Engine"].engine;
            }
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
        return out.join("\n");
        
}
window.search_items = function(query) {

        // Robust bEngine detection
        let bEngine = null;
        if (typeof window !== 'undefined') {
            if (window["com"] && window["com"].stencyl && window["com"].stencyl.Engine && window["com"].stencyl.Engine.engine) {
                bEngine = window["com"].stencyl.Engine.engine;
            } else if (window.u && window.u["com.stencyl.Engine"] && window.u["com.stencyl.Engine"].engine) {
                bEngine = window.u["com.stencyl.Engine"].engine;
            }
        }
        if (!bEngine) {
            throw new Error("bEngine (game engine) not found in this context");
        }
        const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
        let out = [];
        let q = "".toLowerCase();
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName && def.h.displayName.toLowerCase().includes(q)) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            }
        }
        return out.length ? out.join("\n") : `No items found for query: `;
        
}
window.spawn_item = function(item, amount) {

        // Robust bEngine detection
        let bEngine = null;
        if (typeof window !== 'undefined') {
            if (window["com"] && window["com"].stencyl && window["com"].stencyl.Engine && window["com"].stencyl.Engine.engine) {
                bEngine = window["com"].stencyl.Engine.engine;
            } else if (window.u && window.u["com.stencyl.Engine"] && window.u["com.stencyl.Engine"].engine) {
                bEngine = window.u["com.stencyl.Engine"].engine;
            }
        }
        if (!bEngine) {
            throw new Error("bEngine (game engine) not found in this context");
        }
        const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
        const itemDefinition = itemDefs[item];
        if (itemDefinition) {
            let x = character.getXCenter();
            let y = character.getValue("ActorEvents_20", "_PlayerNode");
            if (item.includes("SmithingRecipes"))
                actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
            else
                actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
            return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
        } else {
            return `No item found for '${item}'`;
        }
        
}
window.list_items = function() {

        // Robust bEngine detection with wait
        async function waitForEngine(timeoutMs = 5000) {
            const start = Date.now();
            while (Date.now() - start < timeoutMs) {
                if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
                    return window.__idleon_cheats__["com.stencyl.Engine"].engine;
                }
                await new Promise(r => setTimeout(r, 50));
            }
            throw new Error("bEngine (game engine) not found in this context after waiting");
        }
        let bEngine = await waitForEngine();
        const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
        let out = [];
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            } else {
                out.push(id);
            }
        }
        return out.join("\n");
        
}
window.search_items = function(query) {

        // Robust bEngine detection with wait
        async function waitForEngine(timeoutMs = 5000) {
            const start = Date.now();
            while (Date.now() - start < timeoutMs) {
                if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
                    return window.__idleon_cheats__["com.stencyl.Engine"].engine;
                }
                await new Promise(r => setTimeout(r, 50));
            }
            throw new Error("bEngine (game engine) not found in this context after waiting");
        }
        let bEngine = await waitForEngine();
        const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
        let out = [];
        let q = "".toLowerCase();
        for (const [id, def] of Object.entries(itemDefs)) {
            if (def && def.h && def.h.displayName && def.h.displayName.toLowerCase().includes(q)) {
                out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
            }
        }
        return out.length ? out.join("\n") : `No items found for query: `;
        
}
window.spawn_item = function(item, amount) {

        // Robust bEngine detection with wait
        async function waitForEngine(timeoutMs = 5000) {
            const start = Date.now();
            while (Date.now() - start < timeoutMs) {
                if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
                    return window.__idleon_cheats__["com.stencyl.Engine"].engine;
                }
                await new Promise(r => setTimeout(r, 50));
            }
            throw new Error("bEngine (game engine) not found in this context after waiting");
        }
        let bEngine = await waitForEngine();
        const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
        const itemDefinition = itemDefs[item];
        if (itemDefinition) {
            let x = character.getXCenter();
            let y = character.getValue("ActorEvents_20", "_PlayerNode");
            if (item.includes("SmithingRecipes"))
                actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
            else
                actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
            return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
        } else {
            return `No item found for '${item}'`;
        }
        
}
window.list_items = function() {

        return (async () => {
            async function waitForEngine(timeoutMs = 5000) {
                const start = Date.now();
                while (Date.now() - start < timeoutMs) {
                    if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
                        return window.__idleon_cheats__["com.stencyl.Engine"].engine;
                    }
                    await new Promise(r => setTimeout(r, 50));
                }
                throw new Error("bEngine (game engine) not found in this context after waiting");
            }
            let bEngine = await waitForEngine();
            const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            let out = [];
            for (const [id, def] of Object.entries(itemDefs)) {
                if (def && def.h && def.h.displayName) {
                    out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
                } else {
                    out.push(id);
                }
            }
            return out.join("\n");
        })();
        
}
window.search_items = function(query) {

        return (async () => {
            async function waitForEngine(timeoutMs = 5000) {
                const start = Date.now();
                while (Date.now() - start < timeoutMs) {
                    if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
                        return window.__idleon_cheats__["com.stencyl.Engine"].engine;
                    }
                    await new Promise(r => setTimeout(r, 50));
                }
                throw new Error("bEngine (game engine) not found in this context after waiting");
            }
            let bEngine = await waitForEngine();
            const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            let out = [];
            let q = "".toLowerCase();
            for (const [id, def] of Object.entries(itemDefs)) {
                if (def && def.h && def.h.displayName && def.h.displayName.toLowerCase().includes(q)) {
                    out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
                }
            }
            return out.length ? out.join("\n") : `No items found for query: `;
        })();
        
}
window.spawn_item = function(item, amount) {

        return (async () => {
            async function waitForEngine(timeoutMs = 5000) {
                const start = Date.now();
                while (Date.now() - start < timeoutMs) {
                    if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
                        return window.__idleon_cheats__["com.stencyl.Engine"].engine;
                    }
                    await new Promise(r => setTimeout(r, 50));
                }
                throw new Error("bEngine (game engine) not found in this context after waiting");
            }
            let bEngine = await waitForEngine();
            const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            const actorEvents189 = events(189);
            const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
            const itemDefinition = itemDefs[item];
            if (itemDefinition) {
                let x = character.getXCenter();
                let y = character.getValue("ActorEvents_20", "_PlayerNode");
                if (item.includes("SmithingRecipes"))
                    actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
                else
                    actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
                return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
            } else {
                return `No item found for '${item}'`;
            }
        })();
        
}
window.list_items = function() {

        return (async () => {
            async function waitForEngine(timeoutMs = 5000) {
                const start = Date.now();
                while (Date.now() - start < timeoutMs) {
                    if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
                        return window.__idleon_cheats__["com.stencyl.Engine"].engine;
                    }
                    await new Promise(r => setTimeout(r, 50));
                }
                throw new Error("bEngine (game engine) not found in this context after waiting");
            }
            let bEngine = await waitForEngine();
            const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            let out = [];
            for (const [id, def] of Object.entries(itemDefs)) {
                if (def && def.h && def.h.displayName) {
                    out.push(`${id} : ${def.h.displayName.replace(/_/g, ' ')}`);
                } else {
                    out.push(id);
                }
            }
            return out.join("\n");
        })();
        
}
window.search_items = function(query) {

        return (async () => {
            async function waitForEngine(timeoutMs = 5000) {
                const start = Date.now();
                while (Date.now() - start < timeoutMs) {
                    if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
                        return window.__idleon_cheats__["com.stencyl.Engine"].engine;
                    }
                    await new Promise(r => setTimeout(r, 50));
                }
                throw new Error("bEngine (game engine) not found in this context after waiting");
            }
            let bEngine = await waitForEngine();
            const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            let out = [];
            let q = "".toLowerCase().trim();
            for (const [id, def] of Object.entries(itemDefs)) {
                let displayName = def && def.h && typeof def.h.displayName === 'string' ? def.h.displayName : '';
                if (
                    (id && id.toLowerCase().includes(q)) ||
                    (displayName && displayName.toLowerCase().includes(q))
                ) {
                    out.push(`${id} : ${displayName.replace(/_/g, ' ')}`);
                }
            }
            return out.length ? out.join("\n") : `No items found for query: `;
        })();
        
}
window.spawn_item = function(item, amount) {

        return (async () => {
            async function waitForEngine(timeoutMs = 5000) {
                const start = Date.now();
                while (Date.now() - start < timeoutMs) {
                    if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
                        return window.__idleon_cheats__["com.stencyl.Engine"].engine;
                    }
                    await new Promise(r => setTimeout(r, 50));
                }
                throw new Error("bEngine (game engine) not found in this context after waiting");
            }
            let bEngine = await waitForEngine();
            const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            const actorEvents189 = events(189);
            const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
            const itemDefinition = itemDefs[item];
            if (itemDefinition) {
                let x = character.getXCenter();
                let y = character.getValue("ActorEvents_20", "_PlayerNode");
                if (item.includes("SmithingRecipes"))
                    actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
                else
                    actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
                return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
            } else {
                return `No item found for '${item}'`;
            }
        })();
        
}
window.list_items = function() {

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
        return out.join("\n");
        
}
window.search_items = function(query) {

        let bEngine = null;
        if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
            bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
        }
        if (!bEngine) {
            throw new Error("bEngine (game engine) not found in this context");
        }
        const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
        let out = [];
        let q = "".toLowerCase().trim();
        for (const [id, def] of Object.entries(itemDefs)) {
            let displayName = def && def.h && typeof def.h.displayName === 'string' ? def.h.displayName : '';
            if (
                (id && id.toLowerCase().includes(q)) ||
                (displayName && displayName.toLowerCase().includes(q))
            ) {
                out.push(`${id} : ${displayName.replace(/_/g, ' ')}`);
            }
        }
        return out.length ? out.join("\n") : `No items found for query: `;
        
}
window.spawn_item = function(item, amount) {

        let bEngine = null;
        if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
            bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
        }
        if (!bEngine) {
            throw new Error("bEngine (game engine) not found in this context");
        }
        const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
        const itemDefinition = itemDefs[item];
        if (itemDefinition) {
            let x = character.getXCenter();
            let y = character.getValue("ActorEvents_20", "_PlayerNode");
            if (item.includes("SmithingRecipes"))
                actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
            else
                actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
            return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
        } else {
            return `No item found for '${item}'`;
        }
        
}
window.list_items = function() {

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
        return out.join("\n");
        
}
window.search_items = function(query) {

        let bEngine = null;
        if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
            bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
        }
        if (!bEngine) {
            throw new Error("bEngine (game engine) not found in this context");
        }
        const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
        let out = [];
        let q = "".toLowerCase().trim();
        for (const [id, def] of Object.entries(itemDefs)) {
            let displayName = def && def.h && typeof def.h.displayName === 'string' ? def.h.displayName : '';
            if (
                (id && id.toLowerCase().includes(q)) ||
                (displayName && displayName.toLowerCase().includes(q))
            ) {
                out.push(`${id} : ${displayName.replace(/_/g, ' ')}`);
            }
        }
        return out.length ? out.join("\n") : `No items found for query: `;
        
}
window.spawn_item = function(item, amount) {

        let bEngine = null;
        if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
            bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
        }
        if (!bEngine) {
            throw new Error("bEngine (game engine) not found in this context");
        }
        const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
        const itemDefinition = itemDefs[item];
        if (itemDefinition) {
            let x = character.getXCenter();
            let y = character.getValue("ActorEvents_20", "_PlayerNode");
            if (item.includes("SmithingRecipes"))
                actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
            else
                actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
            return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
        } else {
            return `No item found for '${item}'`;
        }
        
}
window.list_items = function() {

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
        console.log(result);
        return result;
        
}
window.search_items = function(query) {

        let bEngine = null;
        if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
            bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
        }
        if (!bEngine) {
            throw new Error("bEngine (game engine) not found in this context");
        }
        const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
        let out = [];
        let q = "".toLowerCase().trim();
        for (const [id, def] of Object.entries(itemDefs)) {
            let displayName = def && def.h && typeof def.h.displayName === 'string' ? def.h.displayName : '';
            if (
                (id && id.toLowerCase().includes(q)) ||
                (displayName && displayName.toLowerCase().includes(q))
            ) {
                out.push(`${id} : ${displayName.replace(/_/g, ' ')}`);
            }
        }
        let result = out.length ? out.join("\n") : `No items found for query: `;
        console.log(result);
        return result;
        
}
window.spawn_item = function(item, amount) {

        let bEngine = null;
        if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
            bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
        }
        if (!bEngine) {
            throw new Error("bEngine (game engine) not found in this context");
        }
        const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
        const itemDefinition = itemDefs[item];
        let result;
        if (itemDefinition) {
            let x = character.getXCenter();
            let y = character.getValue("ActorEvents_20", "_PlayerNode");
            if (item.includes("SmithingRecipes"))
                actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
            else
                actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
            result = `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
        } else {
            result = `No item found for '${item}'`;
        }
        console.log(result);
        return result;
        
}
window.list_items = function() {

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
        console.log('[PLUGIN_OUTPUT]:', result);
        return result;
        
}
window.search_items = function(query) {

        let bEngine = null;
        if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
            bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
        }
        if (!bEngine) {
            throw new Error("bEngine (game engine) not found in this context");
        }
        const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
        let out = [];
        let q = "".toLowerCase().trim();
        for (const [id, def] of Object.entries(itemDefs)) {
            let displayName = def && def.h && typeof def.h.displayName === 'string' ? def.h.displayName : '';
            if (
                (id && id.toLowerCase().includes(q)) ||
                (displayName && displayName.toLowerCase().includes(q))
            ) {
                out.push(`${id} : ${displayName.replace(/_/g, ' ')}`);
            }
        }
        let result = out.length ? out.join("\n") : `No items found for query: `;
        console.log('[PLUGIN_OUTPUT]:', result);
        return result;
        
}
window.spawn_item = function(item, amount) {

        let bEngine = null;
        if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
            bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
        }
        if (!bEngine) {
            throw new Error("bEngine (game engine) not found in this context");
        }
        const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
        const itemDefinition = itemDefs[item];
        let result;
        if (itemDefinition) {
            let x = character.getXCenter();
            let y = character.getValue("ActorEvents_20", "_PlayerNode");
            if (item.includes("SmithingRecipes"))
                actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
            else
                actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
            result = `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
        } else {
            result = `No item found for '${item}'`;
        }
        console.log('[PLUGIN_OUTPUT]:', result);
        return result;
        
}
window.list_items = function() {

        console.log('starting list_items');
        let bEngine = null;
        if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
            bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
            console.log('bEngine found');
        }
        if (!bEngine) {
            console.log('bEngine not found');
            throw new Error("bEngine (game engine) not found in this context");
        }
        console.log('Listing items');
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
        console.log('[PLUGIN_OUTPUT]:', result);
        return result;
        
}
window.search_items = function(query) {

        let bEngine = null;
        if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
            bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
        }
        if (!bEngine) {
            throw new Error("bEngine (game engine) not found in this context");
        }
        const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
        let out = [];
        let q = "".toLowerCase().trim();
        for (const [id, def] of Object.entries(itemDefs)) {
            let displayName = def && def.h && typeof def.h.displayName === 'string' ? def.h.displayName : '';
            if (
                (id && id.toLowerCase().includes(q)) ||
                (displayName && displayName.toLowerCase().includes(q))
            ) {
                out.push(`${id} : ${displayName.replace(/_/g, ' ')}`);
            }
        }
        let result = out.length ? out.join("\n") : `No items found for query: `;
        console.log('[PLUGIN_OUTPUT]:', result);
        return result;
        
}
window.spawn_item = function(item, amount) {

        let bEngine = null;
        if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
            bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
        }
        if (!bEngine) {
            throw new Error("bEngine (game engine) not found in this context");
        }
        const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
        const itemDefinition = itemDefs[item];
        let result;
        if (itemDefinition) {
            let x = character.getXCenter();
            let y = character.getValue("ActorEvents_20", "_PlayerNode");
            if (item.includes("SmithingRecipes"))
                actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
            else
                actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
            result = `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
        } else {
            result = `No item found for '${item}'`;
        }
        console.log('[PLUGIN_OUTPUT]:', result);
        return result;
        
}
window.list_items = function() {

        console.log('starting list_items');
        let bEngine = null;
        if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
            bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
            console.log('bEngine found');
        }
        if (!bEngine) {
            console.log('bEngine not found');
            throw new Error("bEngine (game engine) not found in this context");
        }
        console.log('Listing items');
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
        console.log('[PLUGIN_OUTPUT]:', result);
        return result;
        
}
window.search_items = function(query) {

        let bEngine = null;
        if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
            bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
        }
        if (!bEngine) {
            throw new Error("bEngine (game engine) not found in this context");
        }
        const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
        let out = [];
        let q = "".toLowerCase().trim();
        for (const [id, def] of Object.entries(itemDefs)) {
            let displayName = def && def.h && typeof def.h.displayName === 'string' ? def.h.displayName : '';
            if (
                (id && id.toLowerCase().includes(q)) ||
                (displayName && displayName.toLowerCase().includes(q))
            ) {
                out.push(`${id} : ${displayName.replace(/_/g, ' ')}`);
            }
        }
        let result = out.length ? out.join("\n") : `No items found for query: `;
        console.log('[PLUGIN_OUTPUT]:', result);
        return result;
        
}
window.spawn_item = function(item, amount) {

        let bEngine = null;
        if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
            bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
        }
        if (!bEngine) {
            throw new Error("bEngine (game engine) not found in this context");
        }
        const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
        const itemDefinition = itemDefs[item];
        let result;
        if (itemDefinition) {
            let x = character.getXCenter();
            let y = character.getValue("ActorEvents_20", "_PlayerNode");
            if (item.includes("SmithingRecipes"))
                actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
            else
                actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
            result = `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
        } else {
            result = `No item found for '${item}'`;
        }
        console.log('[PLUGIN_OUTPUT]:', result);
        return result;
        
}
window.list_items = function() {

        console.log('starting list_items');
        let bEngine = null;
        if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
            bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
            console.log('bEngine found');
        }
        if (!bEngine) {
            console.log('bEngine not found');
            throw new Error("bEngine (game engine) not found in this context");
        }
        console.log('Listing items');
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
        console.log('[PLUGIN_OUTPUT]:', result);
        return result;
        
}
window.search_items = function(query) {

        let bEngine = null;
        if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
            bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
        }
        if (!bEngine) {
            throw new Error("bEngine (game engine) not found in this context");
        }
        const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
        let out = [];
        let q = "".toLowerCase().trim();
        for (const [id, def] of Object.entries(itemDefs)) {
            let displayName = def && def.h && typeof def.h.displayName === 'string' ? def.h.displayName : '';
            if (
                (id && id.toLowerCase().includes(q)) ||
                (displayName && displayName.toLowerCase().includes(q))
            ) {
                out.push(`${id} : ${displayName.replace(/_/g, ' ')}`);
            }
        }
        let result = out.length ? out.join("\n") : `No items found for query: `;
        console.log('[PLUGIN_OUTPUT]:', result);
        return result;
        
}
window.spawn_item = function(item, amount) {

        let bEngine = null;
        if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
            bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
        }
        if (!bEngine) {
            throw new Error("bEngine (game engine) not found in this context");
        }
        const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
        const itemDefinition = itemDefs[item];
        let result;
        if (itemDefinition) {
            let x = character.getXCenter();
            let y = character.getValue("ActorEvents_20", "_PlayerNode");
            if (item.includes("SmithingRecipes"))
                actorEvents189._customBlock_DropSomething(item, 0, 1, 0, 2, y, 0, x, y);
            else
                actorEvents189._customBlock_DropSomething(item, 1, 0, 0, 2, y, 0, x, y);
            result = `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x1)`;
        } else {
            result = `No item found for '${item}'`;
        }
        console.log('[PLUGIN_OUTPUT]:', result);
        return result;
        
}
window.list_items = function() {

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
        
}
window.search_items = function(query) {

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
        let result = out.length ? out.join("
") : `No items found for query: ${query}`;
        return result;
        
}
window.spawn_item = function(item, amount) {

        let bEngine = null;
        if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
            bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
        }
        if (!bEngine) {
            throw new Error("bEngine (game engine) not found in this context");
        }
        const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
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
        return result;
        
}
window.list_items = function() {

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
        
}
window.search_items = function(query) {

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
        
}
window.spawn_item = function(item, amount) {

        let bEngine = null;
        if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
            bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
        }
        if (!bEngine) {
            throw new Error("bEngine (game engine) not found in this context");
        }
        const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
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
        return result;
        
}
window.list_items = function() {

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
        
}
window.search_items = function(query) {

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
        
}
window.spawn_item = function(item, amount) {

        let bEngine = null;
        if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
            bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
        }
        if (!bEngine) {
            throw new Error("bEngine (game engine) not found in this context");
        }
        const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
        const actorEvents189 = events(189);
        const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
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
        return result;
        
}
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

        console.log('spawn_item called', item, amount);
        try {
            let bEngine = null;
            if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
                bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
            }
            if (!bEngine) {
                throw new Error("bEngine (game engine) not found in this context");
            }
            const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            const actorEvents189 = events(189);
            const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
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
            return result;
        } catch (e) {
            return "JS ERROR: " + (e && e.stack ? e.stack : e);
        }
        
}
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

        console.log('spawn_item called', item, amount);
        try {
            let bEngine = null;
            if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
                bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
            }
            if (!bEngine) {
                throw new Error("bEngine (game engine) not found in this context");
            }
            const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            const actorEvents189 = events(189);
            const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
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
            return result;
        } catch (e) {
            return "JS ERROR: " + (e && e.stack ? e.stack : e);
        }
        
}
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

        console.log('spawn_item called', item, amount);
        try {
            let bEngine = null;
            if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
                bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
            }
            if (!bEngine) {
                throw new Error("bEngine (game engine) not found in this context");
            }
            console.log('bEngine keys:', Object.keys(bEngine));
            let actorEvents189;
            if (typeof events === 'function') {
                actorEvents189 = events(189);
            } else if (bEngine && typeof bEngine.events === 'function') {
                actorEvents189 = bEngine.events(189);
            } else if (bEngine && typeof bEngine._events === 'function') {
                actorEvents189 = bEngine._events(189);
            } else if (window && typeof window.events === 'function') {
                actorEvents189 = window.events(189);
            } else {
                throw new Error('Could not find events function for actorEvents189');
            }
            const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
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
            return result;
        } catch (e) {
            return "JS ERROR: " + (e && e.stack ? e.stack : e);
        }
        
}
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

        console.log('spawn_item called', item, amount);
        try {
            let bEngine = null;
            if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
                bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
            }
            if (!bEngine) {
                throw new Error("bEngine (game engine) not found in this context");
            }
            console.log('bEngine keys:', Object.keys(bEngine));
            let actorEvents189;
            if (typeof events === 'function') {
                actorEvents189 = events(189);
            } else if (bEngine && typeof bEngine.events === 'function') {
                actorEvents189 = bEngine.events(189);
            } else if (bEngine && typeof bEngine._events === 'function') {
                actorEvents189 = bEngine._events(189);
            } else if (window && typeof window.events === 'function') {
                actorEvents189 = window.events(189);
            } else {
                throw new Error('Could not find events function for actorEvents189');
            }
            const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
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
            return result;
        } catch (e) {
            return "JS ERROR: " + (e && e.stack ? e.stack : e);
        }
        
}
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

        console.log('spawn_item called', item, amount);
        try {
            let bEngine = null;
            if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
                bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
            }
            if (!bEngine) {
                throw new Error("bEngine (game engine) not found in this context");
            }
            // Robust drop function resolution
            let actorEvents189 = null;
            if (typeof events === "function") {
                actorEvents189 = events(189);
                console.log("Found actorEvents189 via events(189)");
            } else if (window.scripts && window.scripts.ActorEvents_189) {
                actorEvents189 = window.scripts.ActorEvents_189;
                console.log("Found actorEvents189 via window.scripts.ActorEvents_189");
            } else {
                for (const key of Object.keys(bEngine)) {
                    const val = bEngine[key];
                    if (val && typeof val === 'object' && '_customBlock_DropSomething' in val) {
                        actorEvents189 = val;
                        console.log('Found actorEvents189 in bEngine["' + key + '"]');
                        break;
                    }
                }
            }
            if (!actorEvents189) {
                throw new Error('Could not find actorEvents189 (drop function)');
            }
            const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
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
            return result;
        } catch (e) {
            return "JS ERROR: " + (e && e.stack ? e.stack : e);
        }
        
}
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

        console.log('spawn_item called', item, amount);
        try {
            let bEngine = null;
            if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
                bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
            }
            if (!bEngine) {
                throw new Error("bEngine (game engine) not found in this context");
            }
            // Robust drop function resolution
            let actorEvents189 = null;
            if (typeof events === "function") {
                actorEvents189 = events(189);
                console.log("Found actorEvents189 via events(189)");
            } else if (window.scripts && window.scripts.ActorEvents_189) {
                actorEvents189 = window.scripts.ActorEvents_189;
                console.log("Found actorEvents189 via window.scripts.ActorEvents_189");
            } else {
                for (const key of Object.keys(bEngine)) {
                    const val = bEngine[key];
                    if (val && typeof val === 'object' && '_customBlock_DropSomething' in val) {
                        actorEvents189 = val;
                        console.log('Found actorEvents189 in bEngine["' + key + '"]');
                        break;
                    }
                }
            }
            if (!actorEvents189) {
                throw new Error('Could not find actorEvents189 (drop function)');
            }
            const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
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
            return result;
        } catch (e) {
            return "JS ERROR: " + (e && e.stack ? e.stack : e);
        }
        
}
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

        console.log('spawn_item called', item, amount);
        try {
            let bEngine = null;
            if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
                bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
            }
            if (!bEngine) {
                throw new Error("bEngine (game engine) not found in this context");
            }
            // Deep search for _customBlock_DropSomething
            function findDropObj(obj, path, seen) {
                if (!obj || typeof obj !== 'object' || seen.has(obj)) return null;
                seen.add(obj);
                for (const key of Object.keys(obj)) {
                    try {
                        const val = obj[key];
                        if (val && typeof val === 'object') {
                            if (typeof val._customBlock_DropSomething === 'function') {
                                console.log('Found _customBlock_DropSomething at ' + path + '.' + key);
                                return val;
                            }
                            const found = findDropObj(val, path + '.' + key, seen);
                            if (found) return found;
                        }
                    } catch (e) { /* ignore */ }
                }
                return null;
            }
            let actorEvents189 = findDropObj(bEngine, 'bEngine', new Set());
            if (!actorEvents189) {
                throw new Error('Could not find _customBlock_DropSomething in bEngine (deep search)');
            }
            const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
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
            return result;
        } catch (e) {
            return "JS ERROR: " + (e && e.stack ? e.stack : e);
        }
        
}
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

        console.log('spawn_item called', item, amount);
        try {
            let bEngine = null;
            if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
                bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
            }
            if (!bEngine) {
                throw new Error("bEngine (game engine) not found in this context");
            }
            // Try window.scripts.ActorEvents_189 first
            let actorEvents189 = null;
            if (window.scripts && window.scripts.ActorEvents_189 && typeof window.scripts.ActorEvents_189._customBlock_DropSomething === 'function') {
                actorEvents189 = window.scripts.ActorEvents_189;
                console.log('Found actorEvents189 via window.scripts.ActorEvents_189');
            } else {
                // Deep search for _customBlock_DropSomething
                function findDropObj(obj, path, seen) {
                    if (!obj || typeof obj !== 'object' || seen.has(obj)) return null;
                    seen.add(obj);
                    for (const key of Object.keys(obj)) {
                        try {
                            const val = obj[key];
                            if (val && typeof val === 'object') {
                                if (typeof val._customBlock_DropSomething === 'function') {
                                    console.log('Found _customBlock_DropSomething at ' + path + '.' + key);
                                    return val;
                                }
                                const found = findDropObj(val, path + '.' + key, seen);
                                if (found) return found;
                            }
                        } catch (e) { /* ignore */ }
                    }
                    return null;
                }
                actorEvents189 = findDropObj(bEngine, 'bEngine', new Set());
            }
            if (!actorEvents189) {
                throw new Error('Could not find _customBlock_DropSomething (tried window.scripts and deep search)');
            }
            const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
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
            return result;
        } catch (e) {
            return "JS ERROR: " + (e && e.stack ? e.stack : e);
        }
        
}
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

        // Plugin context bootstrap
        if (!window.__idleon_cheats__.plugins) window.__idleon_cheats__.plugins = {};
        if (!window.__idleon_cheats__.plugins.spawn_item) {
            window.__idleon_cheats__.plugins.spawn_item = {
                ctx: this,
                events: typeof events === 'function' ? events : (this.scripts ? (num) => this.scripts['ActorEvents_' + num] : null),
                scripts: this.scripts || (window.scripts || null)
            };
        }
        const pluginCtx = window.__idleon_cheats__.plugins.spawn_item;
        try {
            let bEngine = null;
            if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
                bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
            }
            if (!bEngine) {
                throw new Error("bEngine (game engine) not found in this context");
            }
            // Use saved context and helpers
            let actorEvents189 = null;
            if (pluginCtx.events && typeof pluginCtx.events === 'function') {
                actorEvents189 = pluginCtx.events(189);
                if (actorEvents189 && typeof actorEvents189._customBlock_DropSomething === 'function') {
                    console.log('Found actorEvents189 via saved events helper');
                } else {
                    actorEvents189 = null;
                }
            }
            if (!actorEvents189 && pluginCtx.scripts && pluginCtx.scripts.ActorEvents_189 && typeof pluginCtx.scripts.ActorEvents_189._customBlock_DropSomething === 'function') {
                actorEvents189 = pluginCtx.scripts.ActorEvents_189;
                console.log('Found actorEvents189 via saved scripts');
            }
            if (!actorEvents189) {
                // fallback: deep search
                function findDropObj(obj, path, seen) {
                    if (!obj || typeof obj !== 'object' || seen.has(obj)) return null;
                    seen.add(obj);
                    for (const key of Object.keys(obj)) {
                        try {
                            const val = obj[key];
                            if (val && typeof val === 'object') {
                                if (typeof val._customBlock_DropSomething === 'function') {
                                    console.log('Found _customBlock_DropSomething at ' + path + '.' + key);
                                    return val;
                                }
                                const found = findDropObj(val, path + '.' + key, seen);
                                if (found) return found;
                            }
                        } catch (e) { /* ignore */ }
                    }
                    return null;
                }
                actorEvents189 = findDropObj(bEngine, 'bEngine', new Set());
            }
            if (!actorEvents189) {
                throw new Error('Could not find _customBlock_DropSomething (tried saved context, scripts, and deep search)');
            }
            const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
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
            return result;
        } catch (e) {
            return "JS ERROR: " + (e && e.stack ? e.stack : e);
        }
        
}
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

        // Plugin context bootstrap
        if (!window.__idleon_cheats__.plugins) window.__idleon_cheats__.plugins = {};
        if (!window.__idleon_cheats__.plugins.spawn_item) {
            window.__idleon_cheats__.plugins.spawn_item = {
                ctx: this,
                events: typeof events === 'function' ? events : (this.scripts ? (num) => this.scripts['ActorEvents_' + num] : null),
                scripts: this.scripts || (window.scripts || null)
            };
        }
        const pluginCtx = window.__idleon_cheats__.plugins.spawn_item;
        try {
            let bEngine = null;
            if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
                bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
            }
            if (!bEngine) {
                throw new Error("bEngine (game engine) not found in this context");
            }
            // Use saved context and helpers
            let actorEvents189 = null;
            if (pluginCtx.events && typeof pluginCtx.events === 'function') {
                actorEvents189 = pluginCtx.events(189);
                if (actorEvents189 && typeof actorEvents189._customBlock_DropSomething === 'function') {
                    console.log('Found actorEvents189 via saved events helper');
                } else {
                    actorEvents189 = null;
                }
            }
            if (!actorEvents189 && pluginCtx.scripts && pluginCtx.scripts.ActorEvents_189 && typeof pluginCtx.scripts.ActorEvents_189._customBlock_DropSomething === 'function') {
                actorEvents189 = pluginCtx.scripts.ActorEvents_189;
                console.log('Found actorEvents189 via saved scripts');
            }
            if (!actorEvents189) {
                // fallback: deep search
                function findDropObj(obj, path, seen) {
                    if (!obj || typeof obj !== 'object' || seen.has(obj)) return null;
                    seen.add(obj);
                    for (const key of Object.keys(obj)) {
                        try {
                            const val = obj[key];
                            if (val && typeof val === 'object') {
                                if (typeof val._customBlock_DropSomething === 'function') {
                                    console.log('Found _customBlock_DropSomething at ' + path + '.' + key);
                                    return val;
                                }
                                const found = findDropObj(val, path + '.' + key, seen);
                                if (found) return found;
                            }
                        } catch (e) { /* ignore */ }
                    }
                    return null;
                }
                actorEvents189 = findDropObj(bEngine, 'bEngine', new Set());
            }
            if (!actorEvents189) {
                throw new Error('Could not find _customBlock_DropSomething (tried saved context, scripts, and deep search)');
            }
            const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
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
            return result;
        } catch (e) {
            return "JS ERROR: " + (e && e.stack ? e.stack : e);
        }
        
}
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

        // Plugin context bootstrap
        if (!window.__idleon_cheats__.plugins) window.__idleon_cheats__.plugins = {};
        if (!window.__idleon_cheats__.plugins.spawn_item) {
            window.__idleon_cheats__.plugins.spawn_item = {
                ctx: this,
                events: typeof events === 'function' ? events : (this.scripts ? (num) => this.scripts['ActorEvents_' + num] : null),
                scripts: this.scripts || (window.scripts || null)
            };
        }
        const pluginCtx = window.__idleon_cheats__.plugins.spawn_item;
        try {
            let bEngine = null;
            if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
                bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
            }
            if (!bEngine) {
                throw new Error("bEngine (game engine) not found in this context");
            }
            // Use saved context and helpers
            let actorEvents189 = null;
            if (pluginCtx.events && typeof pluginCtx.events === 'function') {
                actorEvents189 = pluginCtx.events(189);
                if (actorEvents189 && typeof actorEvents189._customBlock_DropSomething === 'function') {
                    console.log('Found actorEvents189 via saved events helper');
                } else {
                    actorEvents189 = null;
                }
            }
            if (!actorEvents189 && pluginCtx.scripts && pluginCtx.scripts.ActorEvents_189 && typeof pluginCtx.scripts.ActorEvents_189._customBlock_DropSomething === 'function') {
                actorEvents189 = pluginCtx.scripts.ActorEvents_189;
                console.log('Found actorEvents189 via saved scripts');
            }
            if (!actorEvents189) {
                // fallback: deep search
                function findDropObj(obj, path, seen) {
                    if (!obj || typeof obj !== 'object' || seen.has(obj)) return null;
                    seen.add(obj);
                    for (const key of Object.keys(obj)) {
                        try {
                            const val = obj[key];
                            if (val && typeof val === 'object') {
                                if (typeof val._customBlock_DropSomething === 'function') {
                                    console.log('Found _customBlock_DropSomething at ' + path + '.' + key);
                                    return val;
                                }
                                const found = findDropObj(val, path + '.' + key, seen);
                                if (found) return found;
                            }
                        } catch (e) { /* ignore */ }
                    }
                    return null;
                }
                actorEvents189 = findDropObj(bEngine, 'bEngine', new Set());
            }
            if (!actorEvents189) {
                throw new Error('Could not find _customBlock_DropSomething (tried saved context, scripts, and deep search)');
            }
            const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
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
            return result;
        } catch (e) {
            return "JS ERROR: " + (e && e.stack ? e.stack : e);
        }
        
}
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

        // Plugin context bootstrap
        if (!window.__idleon_cheats__.plugins) window.__idleon_cheats__.plugins = {};
        if (!window.__idleon_cheats__.plugins.spawn_item) {
            window.__idleon_cheats__.plugins.spawn_item = {
                ctx: this,
                events: typeof events === 'function' ? events : (this.scripts ? (num) => this.scripts['ActorEvents_' + num] : null),
                scripts: this.scripts || (window.scripts || null)
            };
        }
        const pluginCtx = window.__idleon_cheats__.plugins.spawn_item;
        try {
            let bEngine = null;
            if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
                bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
            }
            if (!bEngine) {
                throw new Error("bEngine (game engine) not found in this context");
            }
            // Use saved context and helpers
            let actorEvents189 = null;
            if (pluginCtx.events && typeof pluginCtx.events === 'function') {
                actorEvents189 = pluginCtx.events(189);
                if (actorEvents189 && typeof actorEvents189._customBlock_DropSomething === 'function') {
                    console.log('Found actorEvents189 via saved events helper');
                } else {
                    actorEvents189 = null;
                }
            }
            if (!actorEvents189 && pluginCtx.scripts && pluginCtx.scripts.ActorEvents_189 && typeof pluginCtx.scripts.ActorEvents_189._customBlock_DropSomething === 'function') {
                actorEvents189 = pluginCtx.scripts.ActorEvents_189;
                console.log('Found actorEvents189 via saved scripts');
            }
            if (!actorEvents189) {
                // fallback: deep search
                function findDropObj(obj, path, seen) {
                    if (!obj || typeof obj !== 'object' || seen.has(obj)) return null;
                    seen.add(obj);
                    for (const key of Object.keys(obj)) {
                        try {
                            const val = obj[key];
                            if (val && typeof val === 'object') {
                                if (typeof val._customBlock_DropSomething === 'function') {
                                    console.log('Found _customBlock_DropSomething at ' + path + '.' + key);
                                    return val;
                                }
                                const found = findDropObj(val, path + '.' + key, seen);
                                if (found) return found;
                            }
                        } catch (e) { /* ignore */ }
                    }
                    return null;
                }
                actorEvents189 = findDropObj(bEngine, 'bEngine', new Set());
            }
            if (!actorEvents189) {
                throw new Error('Could not find _customBlock_DropSomething (tried saved context, scripts, and deep search)');
            }
            const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
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
            return result;
        } catch (e) {
            return "JS ERROR: " + (e && e.stack ? e.stack : e);
        }
        
}
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

        // Plugin context bootstrap
        if (!window.__idleon_cheats__.plugins) window.__idleon_cheats__.plugins = {};
        if (!window.__idleon_cheats__.plugins.spawn_item) {
            window.__idleon_cheats__.plugins.spawn_item = {
                ctx: this,
                events: typeof events === 'function' ? events : (this.scripts ? (num) => this.scripts['ActorEvents_' + num] : null),
                scripts: this.scripts || (window.scripts || null)
            };
        }
        const pluginCtx = window.__idleon_cheats__.plugins.spawn_item;
        try {
            let bEngine = null;
            if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
                bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
            }
            if (!bEngine) {
                throw new Error("bEngine (game engine) not found in this context");
            }
            // Use saved context and helpers
            let actorEvents189 = null;
            if (pluginCtx.events && typeof pluginCtx.events === 'function') {
                actorEvents189 = pluginCtx.events(189);
                if (actorEvents189 && typeof actorEvents189._customBlock_DropSomething === 'function') {
                    console.log('Found actorEvents189 via saved events helper');
                } else {
                    actorEvents189 = null;
                }
            }
            if (!actorEvents189 && pluginCtx.scripts && pluginCtx.scripts.ActorEvents_189 && typeof pluginCtx.scripts.ActorEvents_189._customBlock_DropSomething === 'function') {
                actorEvents189 = pluginCtx.scripts.ActorEvents_189;
                console.log('Found actorEvents189 via saved scripts');
            }
            if (!actorEvents189) {
                // fallback: deep search
                function findDropObj(obj, path, seen) {
                    if (!obj || typeof obj !== 'object' || seen.has(obj)) return null;
                    seen.add(obj);
                    for (const key of Object.keys(obj)) {
                        try {
                            const val = obj[key];
                            if (val && typeof val === 'object') {
                                if (typeof val._customBlock_DropSomething === 'function') {
                                    console.log('Found _customBlock_DropSomething at ' + path + '.' + key);
                                    return val;
                                }
                                const found = findDropObj(val, path + '.' + key, seen);
                                if (found) return found;
                            }
                        } catch (e) { /* ignore */ }
                    }
                    return null;
                }
                actorEvents189 = findDropObj(bEngine, 'bEngine', new Set());
            }
            if (!actorEvents189) {
                throw new Error('Could not find _customBlock_DropSomething (tried saved context, scripts, and deep search)');
            }
            const itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            const character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
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
            return result;
        } catch (e) {
            return "JS ERROR: " + (e && e.stack ? e.stack : e);
        }
        
}
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
            // Find the Stencyl engine and item definitions as in cheats.js
            let bEngine = this["com.stencyl.Engine"] && this["com.stencyl.Engine"].engine;
            if (!bEngine) throw new Error("bEngine (game engine) not found in this context");
            let itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            let character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
            let actorEvents189 = this.scripts && this.scripts["ActorEvents_189"];
            if (!actorEvents189 || typeof actorEvents189._customBlock_DropSomething !== 'function') {
                // fallback: try events helper if available
                if (typeof events === 'function') {
                    actorEvents189 = events(189);
                }
            }
            if (!actorEvents189 || typeof actorEvents189._customBlock_DropSomething !== 'function') {
                throw new Error('Could not find _customBlock_DropSomething');
            }
            const itemDefinition = itemDefs[item];
            if (itemDefinition) {
                let x = character.getXCenter();
                let y = character.getValue("ActorEvents_20", "_PlayerNode");
                if (item.includes("SmithingRecipes"))
                    actorEvents189._customBlock_DropSomething(item, 0, amount, 0, 2, y, 0, x, y);
                else
                    actorEvents189._customBlock_DropSomething(item, amount, 0, 0, 2, y, 0, x, y);
                return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x${amount})`;
            } else {
                return `No item found for '${item}'`;
            }
        } catch (err) {
            return `Error: ${err && err.stack ? err.stack : err}`;
        }
        
}
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
            // Find the Stencyl engine and item definitions as in cheats.js
            let bEngine = this["com.stencyl.Engine"] && this["com.stencyl.Engine"].engine;
            if (!bEngine) throw new Error("bEngine (game engine) not found in this context");
            let itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            let character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
            let actorEvents189 = this.scripts && this.scripts["ActorEvents_189"];
            if (!actorEvents189 || typeof actorEvents189._customBlock_DropSomething !== 'function') {
                // fallback: try events helper if available
                if (typeof events === 'function') {
                    actorEvents189 = events(189);
                }
            }
            if (!actorEvents189 || typeof actorEvents189._customBlock_DropSomething !== 'function') {
                throw new Error('Could not find _customBlock_DropSomething');
            }
            const itemDefinition = itemDefs[item];
            if (itemDefinition) {
                let x = character.getXCenter();
                let y = character.getValue("ActorEvents_20", "_PlayerNode");
                if (item.includes("SmithingRecipes"))
                    actorEvents189._customBlock_DropSomething(item, 0, amount, 0, 2, y, 0, x, y);
                else
                    actorEvents189._customBlock_DropSomething(item, amount, 0, 0, 2, y, 0, x, y);
                return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x${amount})`;
            } else {
                return `No item found for '${item}'`;
            }
        } catch (err) {
            return `Error: ${err && err.stack ? err.stack : err}`;
        }
        
}
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
            // Find the Stencyl engine and item definitions as in cheats.js
            let bEngine = null;
            if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
                bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
            }
            if (!bEngine) {
                throw new Error("bEngine (game engine) not found in this context");
            }
            if (!bEngine) throw new Error("bEngine (game engine) not found in this context");
            let itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            let character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
            let actorEvents189 = this.scripts && this.scripts["ActorEvents_189"];
            if (!actorEvents189 || typeof actorEvents189._customBlock_DropSomething !== 'function') {
                // fallback: try events helper if available
                if (typeof events === 'function') {
                    actorEvents189 = events(189);
                }
            }
            if (!actorEvents189 || typeof actorEvents189._customBlock_DropSomething !== 'function') {
                throw new Error('Could not find _customBlock_DropSomething');
            }
            const itemDefinition = itemDefs[item];
            if (itemDefinition) {
                let x = character.getXCenter();
                let y = character.getValue("ActorEvents_20", "_PlayerNode");
                if (item.includes("SmithingRecipes"))
                    actorEvents189._customBlock_DropSomething(item, 0, amount, 0, 2, y, 0, x, y);
                else
                    actorEvents189._customBlock_DropSomething(item, amount, 0, 0, 2, y, 0, x, y);
                return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x${amount})`;
            } else {
                return `No item found for '${item}'`;
            }
        } catch (err) {
            return `Error: ${err && err.stack ? err.stack : err}`;
        }
        
}
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

        async function waitForGameReady(ctx) {
            let retries = 0;
            while ((!ctx["com.stencyl.Engine"] || !ctx["com.stencyl.Engine"].engine) && retries < 20) {
                await new Promise(resolve => setTimeout(resolve, 500));
                retries++;
            }
            if (!ctx["com.stencyl.Engine"] || !ctx["com.stencyl.Engine"].engine) {
                throw new Error("Game engine not ready after waiting.");
            }
        }
        try {
            let ctx = this;
            if (!ctx["com.stencyl.Engine"] && typeof getIdleonContext === 'function') {
                ctx = getIdleonContext();
            }
            console.log('spawn_item this:', ctx);
            console.log('this.com.stencyl.Engine:', ctx && ctx["com.stencyl.Engine"]);
            if (typeof waitForGameReady === 'function') {
                await waitForGameReady(ctx);
            } else {
                let retries = 0;
                while ((!ctx["com.stencyl.Engine"] || !ctx["com.stencyl.Engine"].engine) && retries < 20) {
                    await new Promise(resolve => setTimeout(resolve, 500));
                    retries++;
                }
                if (!ctx["com.stencyl.Engine"] || !ctx["com.stencyl.Engine"].engine) {
                    throw new Error("Game engine not ready after waiting.");
                }
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
                throw new Error('Could not find _customBlock_DropSomething');
            }
            const itemDefinition = itemDefs[item];
            if (itemDefinition) {
                let x = character.getXCenter();
                let y = character.getValue("ActorEvents_20", "_PlayerNode");
                if (item.includes("SmithingRecipes"))
                    actorEvents189._customBlock_DropSomething(item, 0, amount, 0, 2, y, 0, x, y);
                else
                    actorEvents189._customBlock_DropSomething(item, amount, 0, 0, 2, y, 0, x, y);
                return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x${amount})`;
            } else {
                return `No item found for '${item}'`;
            }
        } catch (err) {
            return `Error: ${err && err.stack ? err.stack : err}`;
        }
        
}
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

        async function waitForGameReady(ctx) {
            let retries = 0;
            while ((!ctx["com.stencyl.Engine"] || !ctx["com.stencyl.Engine"].engine) && retries < 20) {
                await new Promise(resolve => setTimeout(resolve, 500));
                retries++;
            }
            if (!ctx["com.stencyl.Engine"] || !ctx["com.stencyl.Engine"].engine) {
                throw new Error("Game engine not ready after waiting.");
            }
        }
        try {
            let ctx = this;
            if (!ctx["com.stencyl.Engine"] && typeof getIdleonContext === 'function') {
                ctx = getIdleonContext();
            }
            console.log('spawn_item this:', ctx);
            console.log('this.com.stencyl.Engine:', ctx && ctx["com.stencyl.Engine"]);
            if (typeof waitForGameReady === 'function') {
                await waitForGameReady(ctx);
            } else {
                let retries = 0;
                while ((!ctx["com.stencyl.Engine"] || !ctx["com.stencyl.Engine"].engine) && retries < 20) {
                    await new Promise(resolve => setTimeout(resolve, 500));
                    retries++;
                }
                if (!ctx["com.stencyl.Engine"] || !ctx["com.stencyl.Engine"].engine) {
                    throw new Error("Game engine not ready after waiting.");
                }
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
                throw new Error('Could not find _customBlock_DropSomething');
            }
            const itemDefinition = itemDefs[item];
            if (itemDefinition) {
                let x = character.getXCenter();
                let y = character.getValue("ActorEvents_20", "_PlayerNode");
                if (item.includes("SmithingRecipes"))
                    actorEvents189._customBlock_DropSomething(item, 0, amount, 0, 2, y, 0, x, y);
                else
                    actorEvents189._customBlock_DropSomething(item, amount, 0, 0, 2, y, 0, x, y);
                return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x${amount})`;
            } else {
                return `No item found for '${item}'`;
            }
        } catch (err) {
            return `Error: ${err && err.stack ? err.stack : err}`;
        }
        
}
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
            console.log('spawn_item this:', ctx);
            console.log('this.com.stencyl.Engine:', ctx && ctx["com.stencyl.Engine"]);
            // Synchronous readiness check (no await)
            if (!ctx["com.stencyl.Engine"] || !ctx["com.stencyl.Engine"].engine) {
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
                throw new Error('Could not find _customBlock_DropSomething');
            }
            const itemDefinition = itemDefs[item];
            if (itemDefinition) {
                let x = character.getXCenter();
                let y = character.getValue("ActorEvents_20", "_PlayerNode");
                if (item.includes("SmithingRecipes"))
                    actorEvents189._customBlock_DropSomething(item, 0, amount, 0, 2, y, 0, x, y);
                else
                    actorEvents189._customBlock_DropSomething(item, amount, 0, 0, 2, y, 0, x, y);
                return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x${amount})`;
            } else {
                return `No item found for '${item}'`;
            }
        } catch (err) {
            return `Error: ${err && err.stack ? err.stack : err}`;
        }
        
}
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
            console.log('spawn_item this:', ctx);
            console.log('this.com.stencyl.Engine:', ctx && ctx["com.stencyl.Engine"]);
            // Synchronous readiness check (no await)
            if (!ctx["com.stencyl.Engine"] || !ctx["com.stencyl.Engine"].engine) {
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
                throw new Error('Could not find _customBlock_DropSomething');
            }
            const itemDefinition = itemDefs[item];
            if (itemDefinition) {
                let x = character.getXCenter();
                let y = character.getValue("ActorEvents_20", "_PlayerNode");
                if (item.includes("SmithingRecipes"))
                    actorEvents189._customBlock_DropSomething(item, 0, amount, 0, 2, y, 0, x, y);
                else
                    actorEvents189._customBlock_DropSomething(item, amount, 0, 0, 2, y, 0, x, y);
                return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x${amount})`;
            } else {
                return `No item found for '${item}'`;
            }
        } catch (err) {
            return `Error: ${err && err.stack ? err.stack : err}`;
        }
        
}
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
            console.log('spawn_item this:', ctx);
            console.log('this.com.stencyl.Engine:', ctx && ctx["com.stencyl.Engine"]);
            // Synchronous readiness check (no await)
            if (!ctx["com.stencyl.Engine"] || !ctx["com.stencyl.Engine"].engine) {
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
                throw new Error('Could not find _customBlock_DropSomething');
            }
            const itemDefinition = itemDefs[item];
            if (itemDefinition) {
                let x = character.getXCenter();
                let y = character.getValue("ActorEvents_20", "_PlayerNode");
                if (item.includes("SmithingRecipes"))
                    actorEvents189._customBlock_DropSomething(item, 0, amount, 0, 2, y, 0, x, y);
                else
                    actorEvents189._customBlock_DropSomething(item, amount, 0, 0, 2, y, 0, x, y);
                return `Dropped ${itemDefinition.h.displayName.replace(/_/g, " ")}. (x${amount})`;
            } else {
                return `No item found for '${item}'`;
            }
        } catch (err) {
            return `Error: ${err && err.stack ? err.stack : err}`;
        }
        
}
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
