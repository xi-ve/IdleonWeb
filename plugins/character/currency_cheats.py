from plugin_system import PluginBase, js_export, ui_banner, ui_toggle, ui_button, ui_search_with_results, ui_autocomplete_input, plugin_command, console
from config_manager import config_manager

class CurrencyCheatsPlugin(PluginBase):
    VERSION = "1.0.0"
    DESCRIPTION = "Comprehensive currency management for Idleon: gems, coins, tokens, and all other currencies with display, add, set, and max functions."
    PLUGIN_ORDER = 5
    CATEGORY = "Character"

    def __init__(self, config=None):
        super().__init__(config or {})
        self.debug = config.get('debug', False) if config else False
        self._currencies_cache = None
        self._cache_timestamp = 0
        self._cache_duration = 300
        self.name = 'currency_cheats'

        self.currency_data = {
            'gems': {
                'name': 'Gems',
                'description': 'Premium currency for gem shop purchases',
                'attribute': 'GemsOwned',
                'max_safe': 50000,
                'icon': '💎'
            },
            'coins': {
                'name': 'Coins',
                'description': 'Basic currency for buying items and upgrades',
                'attribute': 'Money',
                'max_safe': 50000,
                'icon': '🪙'
            }
        }

    async def cleanup(self): pass
    async def update(self): pass
    async def on_config_changed(self, config): 
        self.debug = config.get('debug', False)
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)
    async def on_game_ready(self): pass

    @ui_toggle(
        label="Debug Mode",
        description="Enable debug logging for currency cheats plugin",
        config_key="debug",
        default_value=False
    )
    async def enable_debug(self, value: bool = None):
        if value is not None:
            self.config["debug"] = value
            self.save_to_global_config()
            self.debug = value
        return f"Debug mode {'enabled' if self.config.get('debug', False) else 'disabled'}"

    @ui_search_with_results(
        label="Currency Status",
        description="Show all currencies with their current amounts and descriptions",
        button_text="Show Currencies",
        placeholder="Enter filter term (leave empty to show all)",
        category="Display",
        order=1
    )
    async def currency_status_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[currency_cheats] Getting currency status, filter: {value}")
                result = self.run_js_export('get_currency_status_js', self.injector, filter_query=value or "")
                return result
            except Exception as e:
                if self.debug:
                    console.print(f"[currency_cheats] Error getting currency status: {e}")
                return f"ERROR: Error getting currency status: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_autocomplete_input(
        label="Add Currency",
        description="Add a specific amount to a currency. Syntax: 'currency_name amount' (e.g., 'gems 1000000')",
        button_text="Add",
        placeholder="Enter: currency_name amount (e.g., 'gems 1000000')",
        category="Actions",
        order=3
    )
    async def add_currency_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[currency_cheats] Adding currency, input: {value}")
                
                if not value or not value.strip():
                    return "Please provide currency name and amount (e.g., 'gems 1000000')"
                
                parts = value.strip().split()
                if len(parts) < 2:
                    return "Syntax: 'currency_name amount' (e.g., 'gems 1000000')"
                
                amount_str = parts[-1]
                currency_name = ' '.join(parts[:-1]).lower().replace(' ', '_')
                
                matching_currency = None
                for key, data in self.currency_data.items():
                    if (key.lower() == currency_name or 
                        data['name'].lower().replace(' ', '_') == currency_name):
                        matching_currency = key
                        break
                
                if not matching_currency:
                    available = ', '.join([data['name'] for data in self.currency_data.values()])
                    return f"Currency '{currency_name}' not found. Available: {available}"
                
                try:
                    amount = int(amount_str)
                    if amount < 0:
                        return "Amount must be 0 or higher"
                except ValueError:
                    return "Amount must be a valid number"
                
                result = self.run_js_export('add_currency_js', self.injector, 
                                          currency_key=matching_currency, amount=amount)
                if self.debug:
                    console.print(f"[currency_cheats] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[currency_cheats] Error adding currency: {e}")
                return f"ERROR: Error adding currency: {str(e)}"
        return "Injector not available"

    async def get_add_currency_ui_autocomplete(self, query: str = ""):
        suggestions = []
        query_lower = query.lower()
        
        for key, data in self.currency_data.items():
            if query_lower in key.lower() or query_lower in data['name'].lower():
                suggestions.append(f"{key} 1000000")
                suggestions.append(f"{data['name']} 1000000")
        
        return suggestions[:10]

    @ui_autocomplete_input(
        label="Set Currency",
        description="Set a currency to a specific amount. Syntax: 'currency_name amount' (e.g., 'gems 50000000')",
        button_text="Set",
        placeholder="Enter: currency_name amount (e.g., 'gems 50000000')",
        category="Actions",
        order=4
    )
    async def set_currency_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[currency_cheats] Setting currency, input: {value}")
                
                if not value or not value.strip():
                    return "Please provide currency name and amount (e.g., 'gems 50000000')"
                
                parts = value.strip().split()
                if len(parts) < 2:
                    return "Syntax: 'currency_name amount' (e.g., 'gems 50000000')"
                
                amount_str = parts[-1]
                currency_name = ' '.join(parts[:-1]).lower().replace(' ', '_')
                
                matching_currency = None
                for key, data in self.currency_data.items():
                    if (key.lower() == currency_name or 
                        data['name'].lower().replace(' ', '_') == currency_name):
                        matching_currency = key
                        break
                
                if not matching_currency:
                    available = ', '.join([data['name'] for data in self.currency_data.values()])
                    return f"Currency '{currency_name}' not found. Available: {available}"
                
                try:
                    amount = int(amount_str)
                    if amount < 0:
                        return "Amount must be 0 or higher"
                except ValueError:
                    return "Amount must be a valid number"
                
                result = self.run_js_export('set_currency_js', self.injector, 
                                          currency_key=matching_currency, amount=amount)
                if self.debug:
                    console.print(f"[currency_cheats] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[currency_cheats] Error setting currency: {e}")
                return f"ERROR: Error setting currency: {str(e)}"
        return "Injector not available"

    async def get_set_currency_ui_autocomplete(self, query: str = ""):
        suggestions = []
        query_lower = query.lower()
        
        for key, data in self.currency_data.items():
            if query_lower in key.lower() or query_lower in data['name'].lower():
                suggestions.append(f"{key} {data['max_safe']}")
                suggestions.append(f"{data['name']} {data['max_safe']}")
        
        return suggestions[:10]

    @plugin_command(
        help="Get current currency status.",
        params=[],
    )
    async def get_currency_status(self, injector=None, **kwargs):
        result = self.run_js_export('get_currency_status_js', injector, filter_query="")
        return result

    @plugin_command(
        help="Add amount to a specific currency.",
        params=[
            {"name": "currency", "type": str, "help": "Currency key or name"},
            {"name": "amount", "type": int, "help": "Amount to add"},
        ],
    )
    async def add_currency(self, currency: str, amount: int, **kwargs):
        matching_currency = None
        currency_lower = currency.lower().replace(' ', '_')
        for key, data in self.currency_data.items():
            if (key.lower() == currency_lower or 
                data['name'].lower().replace(' ', '_') == currency_lower):
                matching_currency = key
                break
        
        if not matching_currency:
            available = ', '.join([data['name'] for data in self.currency_data.values()])
            return f"Currency '{currency}' not found. Available: {available}"
        
        result = self.run_js_export('add_currency_js', self.injector, 
                                  currency_key=matching_currency, amount=amount)
        return result

    @plugin_command(
        help="Set a specific currency to an exact amount.",
        params=[
            {"name": "currency", "type": str, "help": "Currency key or name"},
            {"name": "amount", "type": int, "help": "Amount to set"},
        ],
    )
    async def set_currency(self, currency: str, amount: int, **kwargs):
        matching_currency = None
        currency_lower = currency.lower().replace(' ', '_')
        for key, data in self.currency_data.items():
            if (key.lower() == currency_lower or 
                data['name'].lower().replace(' ', '_') == currency_lower):
                matching_currency = key
                break
        
        if not matching_currency:
            available = ', '.join([data['name'] for data in self.currency_data.values()])
            return f"Currency '{currency}' not found. Available: {available}"
        
        result = self.run_js_export('set_currency_js', self.injector, 
                                  currency_key=matching_currency, amount=amount)
        return result

    @js_export(params=["filter_query"])
    def get_currency_status_js(self, filter_query=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            
            const currencyData = {
                'gems': {name: 'Gems', attribute: 'GemsOwned', icon: '💎', description: 'Premium currency for gem shop purchases'},
                'coins': {name: 'Coins', attribute: 'Money', icon: '🪙', description: 'Basic currency for buying items and upgrades'}
            };
            
            let output = "";
            output += "<div style='font-weight: bold; font-size: 16px; margin-bottom: 10px;'>💰 CURRENCY STATUS</div>";
            
            const currencies = [];
            const filterQuery = filter_query ? filter_query.toLowerCase() : "";
            
            for (const [key, data] of Object.entries(currencyData)) {
                let currentValue = 0;
                let found = false;
                
                try {
                    const attributeValue = bEngine.getGameAttribute(data.attribute);
                    if (attributeValue !== null && attributeValue !== undefined) {
                        currentValue = parseInt(attributeValue) || 0;
                        found = true;
                    }
                } catch (e) {
                }
                
                if (filterQuery && 
                    !data.name.toLowerCase().includes(filterQuery) && 
                    !key.toLowerCase().includes(filterQuery) && 
                    !data.description.toLowerCase().includes(filterQuery)) {
                    continue;
                }
                
                currencies.push({
                    key: key,
                    name: data.name,
                    icon: data.icon,
                    description: data.description,
                    value: currentValue,
                    found: found,
                    attribute: data.attribute
                });
            }
            
            currencies.sort((a, b) => b.value - a.value);
            
            let totalValue = 0;
            let foundCount = 0;
            
            for (const currency of currencies) {
                const status = currency.found ? (currency.value > 0 ? "💰" : "📍") : "❓";
                const statusText = currency.found ? (currency.value > 0 ? "Available" : "Zero") : "Not Found";
                const valueColor = currency.value > 1000000 ? '#ff6b6b' : currency.value > 10000 ? '#ffd93d' : '#6bcf7f';
                
                if (currency.found) {
                    foundCount++;
                    totalValue += currency.value;
                }
                
                output += "<div style='margin: 2px 0; padding: 3px 8px; background: rgba(0, 0, 0, 0.05); border-left: 3px solid " + (currency.found ? "#6bcf7f" : "#ff6b6b") + ";'>";
                output += status + " <strong>" + currency.icon + " " + currency.name + "</strong> (" + currency.key + ")<br>";
                output += "<span style='color: " + valueColor + "; font-weight: bold;'>Amount: " + currency.value.toLocaleString() + "</span> | ";
                output += "<span style='color: #888;'>Status: " + statusText + "</span><br>";
                output += "<span style='color: #888; font-size: 0.9em;'>" + currency.description + "</span><br>";
                output += "<span style='color: #666; font-size: 0.8em;'>Attribute: " + currency.attribute + "</span>";
                output += "</div>";
            }
            
            if (!filterQuery) {
                output += "<div style='margin-top: 15px; padding: 10px; background: rgba(0, 0, 0, 0.1); border-radius: 5px;'>";
                output += "<div style='font-weight: bold; margin-bottom: 5px;'>📊 SUMMARY</div>";
                output += "<div>Total Currencies Checked: " + currencies.length + "</div>";
                output += "<div>Found in Game: " + foundCount + "/" + currencies.length + "</div>";
                output += "<div>Total Value (found currencies): " + totalValue.toLocaleString() + "</div>";
                output += "</div>";
            }
            
            return output;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export(params=["currency_key", "amount"])
    def add_currency_js(self, currency_key=None, amount=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            
            const currencyData = {
                'gems': {name: 'Gems', attribute: 'GemsOwned'},
                'coins': {name: 'Coins', attribute: 'Money'}
            };
            
            const currency = currencyData[currency_key];
            if (!currency) {
                throw new Error(`Currency key '${currency_key}' not found`);
            }
            
            const currentValue = parseInt(bEngine.getGameAttribute(currency.attribute)) || 0;
            const newValue = currentValue + amount;
            
            bEngine.setGameAttribute(currency.attribute, newValue);
            
            return `Added ${amount.toLocaleString()} to ${currency.name}. New total: ${newValue.toLocaleString()} (was ${currentValue.toLocaleString()})`;
        } catch (e) {
            throw new Error(`Failed to add currency: ${e.message}`);
        }
        '''

    @js_export(params=["currency_key", "amount"])
    def set_currency_js(self, currency_key=None, amount=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            
            const currencyData = {
                'gems': {name: 'Gems', attribute: 'GemsOwned'},
                'coins': {name: 'Coins', attribute: 'Money'}
            };
            
            const currency = currencyData[currency_key];
            if (!currency) {
                throw new Error(`Currency key '${currency_key}' not found`);
            }
            
            const oldValue = parseInt(bEngine.getGameAttribute(currency.attribute)) || 0;
            
            bEngine.setGameAttribute(currency.attribute, amount);
            
            return `Set ${currency.name} to ${amount.toLocaleString()} (was ${oldValue.toLocaleString()})`;
        } catch (e) {
            throw new Error(`Failed to set currency: ${e.message}`);
        }
        '''

plugin_class = CurrencyCheatsPlugin
