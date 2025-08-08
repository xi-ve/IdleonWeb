# Plugin Development Quick Start

Want to create a plugin for IdleonWeb? This guide will get you up and running in minutes!

> **💡 Auto-Discovery**: Once you create your plugin, the system will automatically detect it on next startup and offer to enable it. No manual configuration needed!

## Table of Contents

- [1. Copy the Template](#1-copy-the-template)
- [2. Edit Your Plugin](#2-edit-your-plugin)
- [3. Add UI Elements](#3-add-ui-elements)
  - [Toggle Switch](#toggle-switch)
  - [Button](#button)
  - [Slider](#slider)
  - [Banner](#banner)
- [4. Add JavaScript Code](#4-add-javascript-code)
  - [JavaScript with Parameters](#javascript-with-parameters)
- [5. Test Your Plugin](#5-test-your-plugin)
- [Plugin Categories](#plugin-categories)
- [Folderized Plugins](#folderized-plugins)
- [Common Patterns](#common-patterns)
  - [Getting Game Data](#getting-game-data)
  - [Spawning Items](#spawning-items)
  - [Modifying Game Values](#modifying-game-values)
- [Tips](#tips)
- [Need Help?](#need-help)

## 1. Copy the Template

Start with the example plugin:

```bash
cp plugins/example_plugin.py plugins/my_plugin.py
```

## 2. Edit Your Plugin

Open `plugins/my_plugin.py` and modify:

```python
class MyPlugin(PluginBase):  # Change class name
    VERSION = "1.0.0"
    DESCRIPTION = "My awesome plugin"  # Change description
    PLUGIN_ORDER = 1  # Control display order (lower = first)
    CATEGORY = "Character"  # Choose category: Character, QoL, Unlocks, World 1, etc.

    def __init__(self, config=None):
        super().__init__(config or {})
        self.name = 'my_plugin'  # Change plugin name
```

## 3. Add UI Elements

### Toggle Switch
```python
@ui_toggle(
    label="My Feature",
    description="Enable my awesome feature",
    config_key="enabled",
    default_value=True,
    category="General Settings",  # Optional: group UI elements
    order=1  # Optional: control order within category
)
async def my_feature_ui(self, value=None):
    if value is not None:
        self.config["enabled"] = value
        self.save_to_global_config()
    return f"Feature {'enabled' if self.config.get('enabled', True) else 'disabled'}"
```

### Button
```python
@ui_button(
    label="Do Something",
    description="Click to perform an action",
    category="Actions",
    order=1
)
async def do_something_ui(self):
    if hasattr(self, 'injector') and self.injector:
        result = self.run_js_export('do_something_js', self.injector)
        return f"SUCCESS: {result}"
    return "ERROR: No injector available - run 'inject' first"
```

### Slider
```python
@ui_slider(
    label="Amount",
    description="Set the amount (1-100)",
    config_key="amount",
    default_value=50,
    min_value=1,
    max_value=100,
    category="Settings",
    order=1
)
async def amount_ui(self, value=None):
    if value is not None:
        self.config["amount"] = value
        self.save_to_global_config()
    return f"Amount set to {self.config.get('amount', 50)}"
```

### Banner
```python
@ui_banner(
    label="⚠️ High Risk Warning",
    description="This action may brick your account.",
    banner_type="warning",
    category="General",
    order=-100
)
async def warning_banner(self):
    pass
```

## 4. Add JavaScript Code

**Important**: JavaScript export functions must end with `_js` in their function name.

```python
@js_export()
def do_something_js(self):  # ← Must end with _js
    return '''
    try {
        const ctx = window.__idleon_cheats__;
        const engine = ctx["com.stencyl.Engine"].engine;
        
        // Your JavaScript code here
        console.log("Doing something awesome!");
        
        return "Action completed successfully!";
    } catch (e) {
        return `Error: ${e.message}`;
    }
    '''
```

### JavaScript with Parameters

```python
@js_export(params=["item", "amount"])
def spawn_item_js(self, item=None, amount=None):  # ← Must end with _js
    return f'''
    try {{
        const ctx = window.__idleon_cheats__;
        const engine = ctx["com.stencyl.Engine"].engine;
        const itemDefs = engine.getGameAttribute("ItemDefinitionsGET").h;
        
        const itemDef = itemDefs["{item}"];
        if (!itemDef) return `No item found: '{{item}}'`;
        
        console.log(`Spawning ${{amount}}x ${{itemDef.h.displayName}}`);
        return `Spawned ${{amount}}x ${{itemDef.h.displayName}}`;
    }} catch (e) {{
        return `Error: ${{e.message}}`;
    }}
    '''
```

**Note**: The system automatically wraps your JavaScript with game-ready checks and error handling. Your code becomes available as `window.plugin_name.do_something()` and `window.plugin_name.spawn_item(item, amount)` in the game.

**Naming Convention**: All `@js_export` functions must end with `_js` in their function name. The system automatically removes the `_js` suffix when creating the JavaScript function name and groups functions under the plugin's namespace.

## 5. Test Your Plugin

1. **Start the launcher:**
   ```bash
   python main.py
   ```

2. **Plugin Auto-Discovery:**
   - The system will automatically detect your new plugin
   - You'll be prompted to enable it - choose "yes" or type your plugin name

3. **Launch the game:**
   - If auto-inject is enabled (default), the game launches automatically
   - Or manually type `inject` to launch the game

4. **Open the web UI:**
   - Go to `http://localhost:8080`
   - Your plugin should appear in the appropriate category

5. **Test your UI elements:**
   - Click buttons
   - Toggle switches
   - Adjust sliders

## Plugin Categories

Organize your plugins by setting the `CATEGORY` attribute:

### Available Categories
- **`"Character"`** - Character-related features (stats, abilities, inventory)
- **`"QoL"`** - Quality of Life improvements (convenience features)
- **`"Unlocks"`** - Unlock-related features (cards, vault, packages)
- **`"World 1"`**, **`"World 2"`**, etc. - World-specific features
- **`"Sneaking"`** - Sneaking game related features

### Plugin Ordering
Set `PLUGIN_ORDER` to control display order:
```python
PLUGIN_ORDER = 1  # Lower numbers appear first
```

## Folderized Plugins

Organize plugins in subdirectories for better structure:

```text
plugins/
├── character/
│   ├── godlike_powers.py
│   ├── spawn_item.py
│   └── stats_multiplier.py
├── qol/
│   └── global_storage.py
├── unlocks/
│   ├── card_cheats.py
│   └── vault_unlocker.py
└── world1/
    └── anvil_cheats.py
```

**Plugin names** in subdirectories use dot notation:
- `plugins/character/godlike_powers.py` → Plugin name: `character.godlike_powers`
- `plugins/unlocks/card_cheats.py` → Plugin name: `unlocks.card_cheats`

## JavaScript Function Namespacing

JavaScript functions are automatically grouped under the plugin's namespace to avoid conflicts:

```javascript
// Functions are available as:
window.plugin_name.function_name()

// Examples:
window.spawn_item.spawn_item("Copper", 10)
window.godlike_powers.set_powers(true)
window.card_cheats.set_card_level("mushG", 5)
```

**Compatibility Layer**: The system includes a compatibility layer that automatically translates old-style `window.function_name()` calls to the appropriate plugin namespace, so existing code continues to work.

> **For detailed JavaScript generation documentation, see [DEVELOPMENT.md](DEVELOPMENT.md#javascript-generation-and-injection)**

## Common Patterns

### Getting Game Data
```javascript
const ctx = window.__idleon_cheats__;
const engine = ctx["com.stencyl.Engine"].engine;
const itemDefs = engine.getGameAttribute("ItemDefinitionsGET").h;
const character = engine.getGameAttribute("OtherPlayers").h[engine.getGameAttribute("UserInfo")[0]];
```

### Spawning Items
```javascript
const dropFn = events(189);
dropFn._customBlock_DropSomething(itemId, amount, 0, 0, 2, y, 0, x, y);
```

### Modifying Game Values
```javascript
// Example: Change player speed
character.setValue("ActorEvents_20", "_PlayerSpeed", newSpeed);
```

### Plugin Configuration Access
```javascript
// Access plugin config in JavaScript
if (window.pluginConfigs && window.pluginConfigs['my_plugin']) {
    const config = window.pluginConfigs['my_plugin'];
    if (config.enabled) {
        // Do something when enabled
    }
}
```

> **For detailed configuration system documentation, see [DEVELOPMENT.md](DEVELOPMENT.md#window-configuration-system)**

## Tips

- **Always check for injector**: `if hasattr(self, 'injector') and self.injector:`
- **Handle errors gracefully**: Wrap JavaScript in try-catch
- **Use descriptive labels**: Make UI elements clear and helpful
- **Test thoroughly**: Try different scenarios and edge cases
- **Check the console**: Look for error messages in browser DevTools
- **Use categories**: Group related UI elements with the `category` parameter
- **Set plugin order**: Use `PLUGIN_ORDER` to control display order
- **Follow naming conventions**: End UI functions with `_ui` and autocomplete functions with `_autocomplete`

## Hot Reload Development

The system supports hot reloading for rapid development:

**Quick Development Workflow:**
1. Start the system: `python main.py` then `inject`
2. Make changes to your plugin file
3. Type `reload` in the CLI to reload all plugins
4. Your changes are immediately available in the game!

> **For detailed hot reload documentation, see [DEVELOPMENT.md](DEVELOPMENT.md#hot-reload-system)**

**UI Category Organization:**
- Use `category` parameter to group related UI elements
- Categories are sorted alphabetically in the web UI
- Use `order` parameter to control element order within categories
- Common categories: "General", "Core Settings", "Performance", "Actions", "Debug"

**Example with Categories:**
```python
@ui_toggle(
    label="Enable Feature",
    category="Core Settings",  # Groups with other core settings
    order=1  # First in the category
)
async def enable_feature_ui(self, value=None):
    pass

@ui_slider(
    label="Speed Multiplier",
    category="Performance",  # Different category
    order=1
)
async def speed_ui(self, value=None):
    pass
```

> **For detailed UI category documentation, see [DEVELOPMENT.md](DEVELOPMENT.md#ui-category-system-and-sorting)**

## Need Help?

- Check `plugins/character/godlike_powers.py` and `plugins/character/spawn_item.py` for real examples
- See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed documentation
- Look at the browser console for JavaScript errors
- Check the launcher output for Python errors

Happy plugin development! 🎮 