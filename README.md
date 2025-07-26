# IdleonWeb Python Launcher

A modern, extensible launcher and plugin system for automating and enhancing Legends of Idleon in the browser, powered by Python and Node.js.

---

## Features

- **Plugin System:** Write Python plugins to inject custom JavaScript into Idleon, automate tasks, or add new features.
- **Rich CLI:** Beautiful, interactive command-line interface with autocompletion, help, and plugin command discovery.
- **Automatic Dependency Management:** Installs Node.js dependencies on first run.
- **Chromium/Chrome Automation:** Launches and controls Idleon in a browser with Chrome DevTools Protocol.
- **Single JS Injection:** All plugin JS is merged and injected into the main game context (N.js) for maximum compatibility.
- **Easy Plugin Development:** Add new plugins by dropping Python files in the `plugins/` directory.

---

## Setup

### Quick Setup (Recommended)
Run the automated setup script:
```sh
./setup.sh
```

This script will:
- Check for Python 3 and Node.js installations
- Create and configure the Python virtual environment
- Install all Python dependencies from `requirements.txt`
- Install Node.js dependencies in the `core/` directory
- Create necessary directories (`plugins/`, `core/tmp_js/`)
- Generate initial configuration file (`core/conf.json`)

### Manual Setup
If you prefer manual setup:

1. **Clone the repository and enter the directory:**
   ```sh
   git clone <repo-url>
   cd IdleonWeb
   ```
2. **Create and activate a Python virtual environment:**
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Install Node.js dependencies:**
   ```sh
   cd core
   npm install
   cd ..
   ```
4. **Run the launcher:**
   ```sh
   python main.py
   ```

---

## Plugin System Overview

- **Plugins are Python classes** in the `plugins/` directory, using the `@plugin_command` decorator to expose commands to the CLI.
- **Each plugin can export JavaScript** to be injected into Idleon via the browser.
- **All plugin JS is merged** into `core/plugins_combined.js` and injected into the game context by intercepting N.js.
- **Plugin commands** are accessed in the CLI as `plugins.pluginname.command`.

---

## Usage

- **Start the CLI:**
  ```sh
  python main.py
  ```
- **Autocomplete:** Use Tab to discover commands and plugin functions.
- **Run a plugin command:**
  ```sh
  plugins.schalom_popup.schalom_greet "Hello world" 3 1.23
  ```
- **Show help:**
  ```sh
  help
  help plugins.schalom_popup.schalom_greet
  ```
- **Exit:**
  ```sh
  exit
  ```

---

## Writing Your Own Plugin

1. **Create a new Python file in `plugins/`** (e.g., `myplugin.py`).
2. **Define a class inheriting from `PluginBase`.**
3. **Use `@plugin_command` to expose CLI commands.**
4. **Use `@js_export` to define JS functions to inject.**
5. **Reload the CLI to see your plugin and commands.**

Example skeleton:
```python
from plugin_system import PluginBase, plugin_command, js_export

class MyPlugin(PluginBase):
    @plugin_command(help="Say hello.")
    async def hello(self, name, injector=None, **kwargs):
        return self.run_js_export('hello_js', injector, name=name)

    @js_export(params=["name"])
    def hello_js(self, name="Idleon"): 
        return f'console.log("Hello, {name}!");'

plugin_class = MyPlugin
```

---

## Troubleshooting

- **Node.js not found?** Ensure Node.js and npm are installed and in your PATH.
- **Chromium/Chrome not found?** The injector tries common install locations. Install Chromium or Google Chrome if needed.
- **Plugin not showing up?** Check for syntax errors and ensure your plugin class is named and exported correctly.
- **Debug output:** Set `"debug": true` in `core/conf.json` for verbose logs.

---

## Project Structure

```
IdleonWeb/
  core/
    injector.js
    plugins_combined.js
    conf.json
  plugins/
    schalom_popup.py
    ...
  main.py
  plugin_system.py
  README.md
  requirements.txt
```

---

## License
MIT 