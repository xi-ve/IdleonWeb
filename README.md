# IdleonWeb Python Launcher

A modern, extensible launcher and plugin system for automating and enhancing Legends of Idleon in the browser, powered by Python and Node.js.

---

## Features

- **Highly Extensible Plugin System:** Easily add, remove, or update features by writing Python plugins. Each plugin can inject custom JavaScript, automate gameplay, or add new commands to the CLI.
- **Centralized Configuration Management:** All configuration is managed through a global, atomic ConfigManager, ensuring consistency and easy access for both core and plugins. Supports granular path-based access and automatic persistence.
- **Rich CLI:** Interactive command-line interface with autocompletion, help, and plugin command discovery. All plugin commands are automatically exposed in the CLI.
- **Automatic Dependency Management:** Installs Node.js dependencies on first run.
- **Chromium/Chrome Automation:** Launches and controls Idleon in a browser with Chrome DevTools Protocol.
- **Single JS Injection:** All plugin JS is merged and injected into the main game context (N.js) for maximum compatibility.
- **Easy Plugin Development:** Add new plugins by dropping Python files in the `plugins/` directory. Plugins are hot-reloadable and can react to configuration changes.

---

## Architecture Overview

IdleonWeb is designed for modularity and extensibility. The core components interact as follows:

```mermaid
graph TD
    A[main.py (CLI)] -->|Loads| B[PluginManager]
    B -->|Loads| C[Plugins (Python)]
    B -->|Uses| D[ConfigManager]
    A -->|Runs| E[injector.js (Node.js)]
    E -->|Injects| F[plugins_combined.js (JS)]
    F -->|Interacts| G[Idleon Game Context]
    C -->|Exports JS| F
    D -->|Manages| H[core/conf.json]
```

- **main.py**: Entry point, provides the CLI, manages plugin loading, configuration, and launches the injector.
- **PluginManager**: Loads and manages all plugins, handles lifecycle events, and exposes plugin commands to the CLI.
- **Plugins**: Python classes that can define CLI commands and export JavaScript to be injected into the game.
- **ConfigManager**: Singleton for all configuration, providing atomic get/set operations and automatic saving to `core/conf.json`.
- **injector.js**: Node.js script that launches Chromium, intercepts the game's JS, and injects the combined plugin code.
- **plugins_combined.js**: All plugin JS exports are merged here and injected into the game context.

---

## Configuration and Extensibility

- **Centralized Config:** All configuration (global and per-plugin) is stored in `core/conf.json` and managed by the ConfigManager singleton. Plugins and core code use `config_manager.get_path()` and `set_path()` for atomic, path-based access.
- **Plugin Config:** Each plugin can define and react to its own config section. Config changes are automatically propagated to the browser and plugin instances.
- **Dynamic Plugins:** Add new features by simply dropping a Python file in `plugins/`. Plugins can:
  - Expose CLI commands with `@plugin_command`
  - Export JavaScript with `@js_export`
  - React to config changes and game events
- **Hot Reload:** Plugins can be reloaded and reconfigured at runtime without restarting the application.

---

## How It Works

### main.py (Python CLI)
- Loads configuration and plugins using the ConfigManager and PluginManager.
- Provides an interactive CLI for running plugin commands, viewing config, and managing plugins.
- Runs the Node.js injector to launch the browser and inject plugin code.
- Handles plugin lifecycle: initialization, updates, config changes, and cleanup.

### injector.js (Node.js)
- Launches Chromium/Chrome with a custom user profile and remote debugging enabled.
- Intercepts the game's main JS file (N.js), injects the combined plugin JS and core setup code.
- Waits for the game to be fully loaded and ready before injecting plugins.
- Ensures all plugin JS is available in the game context for use by plugins and the CLI.

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
- **Plugins can react to config changes and game events** via lifecycle hooks.

---

## Usage

- **Start the CLI:**
  ```sh
  python main.py
  ```
- **Autocomplete:** Use Tab to discover commands and plugin functions.
- **Run a plugin command:**
  ```sh
  plugins.myplugin.hello "Hello world"
  ```
- **Show help:**
  ```sh
  help
  help plugins.myplugin.hello
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