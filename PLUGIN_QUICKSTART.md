# Plugin Development Quick Start

Want to create a plugin for IdleonWeb? This guide will get you up and running in minutes!

## Table of Contents

- [1. Copy the Template](#1-copy-the-template)
- [2. Edit Your Plugin](#2-edit-your-plugin)
- [3. Add UI Elements](#3-add-ui-elements)
  - [Toggle Switch](#toggle-switch)
  - [Button](#button)
  - [Slider](#slider)
- [4. Add JavaScript Code](#4-add-javascript-code)
  - [JavaScript with Parameters](#javascript-with-parameters)
- [5. Test Your Plugin](#5-test-your-plugin)
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
    default_value=True
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
    description="Click to perform an action"
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
    max_value=100
)
async def amount_ui(self, value=None):
    if value is not None:
        self.config["amount"] = value
        self.save_to_global_config()
    return f"Amount set to {self.config.get('amount', 50)}"
```

## 4. Add JavaScript Code

```python
@js_export()
def do_something_js(self):
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
def spawn_item_js(self, item=None, amount=None):
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

**Note**: The system automatically wraps your JavaScript with game-ready checks and error handling. Your code becomes available as `window.do_something()` and `window.spawn_item(item, amount)` in the game.

## 5. Test Your Plugin

1. **Start the launcher:**
   ```bash
   python main.py
   ```

2. **Type `inject` to launch the game**

3. **Open the web UI:**
   - Go to `http://localhost:8080`
   - Your plugin should appear in the list

4. **Test your UI elements:**
   - Click buttons
   - Toggle switches
   - Adjust sliders

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

## Tips

- **Always check for injector**: `if hasattr(self, 'injector') and self.injector:`
- **Handle errors gracefully**: Wrap JavaScript in try-catch
- **Use descriptive labels**: Make UI elements clear and helpful
- **Test thoroughly**: Try different scenarios and edge cases
- **Check the console**: Look for error messages in browser DevTools

## Need Help?

- Check `plugins/spawn_item.py` and `plugins/instant_mob_respawn.py` for real examples
- See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed documentation
- Look at the browser console for JavaScript errors
- Check the launcher output for Python errors

Happy plugin development! 🎮 