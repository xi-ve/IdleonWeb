from plugin_system import plugin_command, js_export, PluginBase

class SpawnItemPlugin(PluginBase):

    VERSION = "1.0.0"
    DESCRIPTION = "Spawn (drop) an item at your character's location."

    def __init__(self, config=None):
        super().__init__(config or {})
        self.injector = None
        self.debug = self.config.get('debug', True)
        self.name = self.__class__.__name__

    async def initialize(self, injector) -> bool:
        self.injector = injector
        return True

    async def cleanup(self) -> None:
        pass

    async def update(self) -> None:
        self.debug = self.config.get('debug', True)

    @plugin_command(
        help="Spawn (drop) an item at your character's location.",
        params=[
            {"name": "item", "type": str, "help": "Item ID to spawn (e.g. 'Copper', 'Timecandy6')"},
            {"name": "amount", "type": int, "default": 1, "help": "Amount to spawn (default: 1)"},
        ],
    )
    async def spawn(self, item: str, amount: int = 1, injector=None, **kwargs):
        """Spawn (drop) an item at your character's location."""
        print(f"[spawn_item] Spawning item: {item} (amount: {amount})")
        return self.run_js_export('spawn_item_js', injector, item=item, amount=amount)

    @js_export(params=["item", "amount"])
    def spawn_item_js(self, item=None, amount=None):
        return '''
        try {
            let bEngine = null;
            if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__["com.stencyl.Engine"] && window.__idleon_cheats__["com.stencyl.Engine"].engine) {
                bEngine = window.__idleon_cheats__["com.stencyl.Engine"].engine;
            }
            if (!bEngine) {
                console.error('spawn_item: bEngine (game engine) not found in this context');
                throw new Error("bEngine (game engine) not found in this context");
            }
            let itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
            let character = bEngine.getGameAttribute("OtherPlayers").h[bEngine.getGameAttribute("UserInfo")[0]];
            let actorEvents189 = null;
            if (typeof window !== 'undefined' && window.__idleon_cheats__ && window.__idleon_cheats__.scripts && window.__idleon_cheats__.scripts["ActorEvents_189"]) {
                actorEvents189 = window.__idleon_cheats__.scripts["ActorEvents_189"];
            }
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
        '''

    @plugin_command(
        help="List all available item IDs and their display names.",
        params=[],
    )
    async def list_items(self, injector=None, **kwargs):
        """List all available item IDs and their display names."""
        print("[spawn_item] Listing all items...")
        return self.run_js_export('list_items_js', injector)

    @js_export()
    def list_items_js(self):
        return '''
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
            let result = out.join("\\n");
            return result;
        } catch (e) {
            return "JS ERROR: " + (e && e.stack ? e.stack : e);
        }
        '''

    @plugin_command(
        help="Search for items by partial name.",
        params=[
            {"name": "query", "type": str, "help": "Partial name to search for (case-insensitive)", "default": "Filler"},
        ],
    )
    async def search_items(self, query: str, injector=None, **kwargs):
        """Search for items by partial name."""
        print(f"[spawn_item] Searching items with query: {query}")
        return self.run_js_export('search_items_js', injector, query=query)

    @js_export(params=["query"])
    def search_items_js(self, query=None):
        return '''
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
            let result = out.length ? out.join("\\n") : `No items found for query: ${query}`;
            return result;
        } catch (e) {
            return "JS ERROR: " + (e && e.stack ? e.stack : e);
        }
        ''' 

plugin_class = SpawnItemPlugin 