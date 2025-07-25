from rich.panel import Panel
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
        print(f"> Spawning item: {item} (amount: {amount})")
        return self.run_js_export('spawn_item_js', injector, item=item, amount=amount)

    @js_export(params=["item", "amount"])
    def spawn_item_js(self, item=None, amount=None):
        return '''
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
        '''

    @plugin_command(
        help="List all available item IDs and their display names.",
        params=[],
    )
    async def list_items(self, injector=None, **kwargs):
        """List all available item IDs and their display names."""
        if self.debug:
            print("[spawn_item] Listing all items...")
        return self.run_js_export('list_items_js', injector)

    @js_export()
    def list_items_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const itemDefs = ctx["com.stencyl.Engine"].engine.getGameAttribute("ItemDefinitionsGET").h;
            
            return Object.entries(itemDefs)
                .map(([id, def]) => `${id} : ${def?.h?.displayName?.replace(/_/g, ' ') || id}`)
                .join("\\n");
        } catch (e) {
            return `Error: ${e.message}`;
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
        if self.debug:
            print(f"[spawn_item] Searching items with query: {query}")
        return self.run_js_export('search_items_js', injector, query=query)

    @js_export(params=["query"])
    def search_items_js(self, query=None):
        return '''
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
                ? matches.map(([id, def]) => `${id} : ${def?.h?.displayName?.replace(/_/g, ' ') || id}`).join("\\n")
                : `No items found for: ${query}`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        ''' 

plugin_class = SpawnItemPlugin