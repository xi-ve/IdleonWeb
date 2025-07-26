from typing import Dict, Any
from plugin_system import plugin_command, js_export, PluginBase, console, ui_toggle, ui_input_with_button, ui_search_with_results, ui_autocomplete_input
from config_manager import config_manager

class SpawnItemPlugin(PluginBase):
    VERSION = "1.0.1"
    DESCRIPTION = "Spawn / List / Search items"

    def __init__(self, config=None):
        super().__init__(config or {})
        self.injector = None
        self.name = 'spawn_item'
        self.debug = config_manager.get_path('plugin_configs.spawn_item.debug', True)
        self._item_cache = None
        self._cache_timestamp = 0
        self._cache_duration = 300  # 5 minutes cache

    async def cleanup(self) -> None:
        pass

    async def update(self) -> None:
        pass

    async def on_config_changed(self, config: Dict[str, Any]) -> None:
        self.debug = config_manager.get_path('plugin_configs.spawn_item.debug', True)
        if GLOBAL_DEBUG:
            console.print(f"[spawn_item] Config changed: {config}")
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)

    async def on_game_ready(self) -> None:
        pass

    @ui_toggle(
        label="Debug Mode",
        description="Enable debug logging for spawn item plugin",
        config_key="debug",
        default_value=True,
        category="Debug Settings",
        order=1
    )
    async def enable_debug(self, value: bool = None):
        """Enable or disable debug mode."""
        if value is not None:
            self.config["debug"] = value
            self.save_to_global_config()
        return f"Debug mode {'enabled' if self.config.get('debug', True) else 'disabled'}"

    @ui_autocomplete_input(
        label="Spawn Item",
        description="Enter item ID and amount to spawn (with autocomplete)",
        button_text="Spawn",
        placeholder="Item ID (e.g. Copper, Timecandy6)",
        category="Spawn Actions",
        order=1
    )
    async def spawn_item_ui(self, value: str = None):
        """Spawn an item using UI input with autocomplete."""
        if value:
            # Parse input (format: "item_id amount" or just "item_id")
            parts = value.strip().split()
            item_id = parts[0] if parts else "Copper"
            amount = int(parts[1]) if len(parts) > 1 else 1
            
            # Actually call the spawn function
            if hasattr(self, 'injector') and self.injector:
                try:
                    result = await self.spawn(item_id, amount, self.injector)
                    return f"SUCCESS: {result}"
                except Exception as e:
                    return f"ERROR: Error spawning item: {str(e)}"
            else:
                return "ERROR: No injector available - run 'inject' first"
        return "Enter item ID and optional amount (e.g. 'Copper 5')"

    async def get_spawn_autocomplete(self, query: str = ""):
        """Get autocomplete suggestions for spawn items."""
        return await self.get_item_autocomplete(query)

    @ui_search_with_results(
        label="Search Items",
        description="Search for items by name or ID",
        button_text="Search",
        placeholder="Enter search term...",
        category="Search",
        order=1
    )
    async def search_items_ui(self, value: str = None):
        """Search for items using UI input."""
        if value:
            # Actually call the search function
            if hasattr(self, 'injector') and self.injector:
                try:
                    result = await self.search_items(value, self.injector)
                    return result
                except Exception as e:
                    return f"ERROR: Error searching items: {str(e)}"
            else:
                return "ERROR: No injector available - run 'inject' first"
        return "Enter search term to find items"

    @ui_search_with_results(
        label="List All Items",
        description="List all available items in the game",
        button_text="List All",
        placeholder="(Leave empty to list all)",
        category="Search",
        order=2
    )
    async def list_all_items_ui(self, value: str = None):
        """List all items using UI input."""
        # Actually call the list function
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.get_cached_item_list()
                return result
            except Exception as e:
                return f"ERROR: Error listing items: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first"

    async def get_cached_item_list(self):
        """Get cached item list or fetch new one."""
        import time
        current_time = time.time()
        
        # Check if cache is valid
        if (self._item_cache is not None and 
            current_time - self._cache_timestamp < self._cache_duration):
            return self._item_cache
        
        # Fetch new data
        raw_result = await self.list_items(self.injector)
        
        # Format the result
        if raw_result and not raw_result.startswith("Error:"):
            try:
                # Split by newlines and format each item
                items = raw_result.split('\n')
                formatted_items = []
                
                for item in items:
                    if ' : ' in item:
                        item_id, display_name = item.split(' : ', 1)
                        formatted_items.append(f"• **{item_id}** : {display_name}")
                    else:
                        formatted_items.append(f"• {item}")
                
                formatted_result = f"**All Items** ({len(formatted_items)} items):\n\n" + "\n".join(formatted_items)
                
                # Cache the formatted result
                self._item_cache = formatted_result
                self._cache_timestamp = current_time
                
                return formatted_result
            except Exception as e:
                return f"**All Items**:\n\n{raw_result}"
        else:
            return f"ERROR: Error fetching items: {raw_result}"

    async def get_item_autocomplete(self, query: str = ""):
        """Get autocomplete suggestions for items."""
        if not hasattr(self, 'injector') or not self.injector:
            return []
        
        try:
            # Get cached or fresh item list
            await self.get_cached_item_list()
            
            if not self._item_cache:
                return []
            
            # Parse the cached items for autocomplete
            suggestions = []
            query_lower = query.lower()
            
            # Extract items from cached result
            lines = self._item_cache.split('\n')
            for line in lines:
                if '**' in line and ' : ' in line:
                    # Extract item ID from formatted line
                    item_id = line.split('**')[1]
                    if query_lower in item_id.lower():
                        suggestions.append(item_id)
            
            return suggestions[:10]  # Limit to 10 suggestions
            
        except Exception as e:
            return []

    @plugin_command(
        help="Spawn (drop) an item at your character's location.",
        params=[
            {"name": "item", "type": str, "help": "Item ID to spawn (e.g. 'Copper', 'Timecandy6')"},
            {"name": "amount", "type": int, "default": 1, "help": "Amount to spawn (default: 1)"},
        ],
    )
    async def spawn(self, item: str, amount: int = 1, injector=None, **kwargs):
        console.print(f"> Spawning item: {item} (amount: {amount})")
        return self.run_js_export('spawn_item_js', injector, item=item, amount=amount)

    @js_export(params=["item", "amount"])
    def spawn_item_js(self, item=None, amount=None):
        return '''
        try {
            console.log("Spawning item: ", item, " (amount: ", amount, ")");

            const ctx = window.__idleon_cheats__;
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
            
            console.log("Dropped item: ", itemDef.h.displayName.replace(/_/g, " "), " (x", amount, ")");

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
        if self.debug:
            console.print("[spawn_item] Listing all items...")
        result = self.run_js_export('list_items_js', injector)
        if self.debug:
            console.print(f"[spawn_item] Result: {result}")
        return result

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
        if self.debug:
            console.print(f"[spawn_item] Searching items with query: {query}")
        result = self.run_js_export('search_items_js', injector, query=query)
        if self.debug:
            console.print(f"[spawn_item] Result: {result}")
        return result

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