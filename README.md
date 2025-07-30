# IdleonWeb

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat-square)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-14+-green.svg?style=flat-square)](https://nodejs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg?style=flat-square)](https://github.com/xi-ve/IdleonWeb)
[![Integration Tests](https://github.com/xi-ve/IdleonWeb/actions/workflows/combined-tests-and-release.yml/badge.svg?style=flat-square)](https://github.com/xi-ve/IdleonWeb/actions/workflows/combined-tests-and-release.yml)

A modern, user-friendly launcher and plugin system for enhancing Legends of Idleon with a beautiful web interface.

> **For developers:** See [PLUGIN_QUICKSTART.md](PLUGIN_QUICKSTART.md) for a quick guide to creating plugins, or [DEVELOPMENT.md](DEVELOPMENT.md) for detailed technical documentation.

## Screenshots

<p align="center">
  <img src="images/screenshot1.png" alt="IdleonWeb - Dashboard" width="800">
  <br/>
  <img src="images/screenshot2.png" alt="IdleonWeb - Plugin Configuration" width="800">
  <br/>
  <img src="images/screenshot3.png" alt="IdleonWeb - Dark Mode" width="800">
  <br/>
  <img src="images/screenshot4.png" alt="IdleonWeb - Game Integration" width="800">
</p>

## Features

- **Easy-to-Use Web Interface** - Configure plugins and manage game enhancements through a modern web browser
- **Plugin System** - Add new features by simply dropping plugin files into the `plugins/` folder
- **Real-Time Updates** - See changes instantly as you configure plugins
- **Cross-Platform** - Works on Windows, Linux, and macOS
- **One-Click Setup** - Automated installation scripts for all platforms
- **Plugin Categories** - Organized plugin management with categories like Character, QoL, Unlocks, and World-specific
- **Folderized Plugins** - Support for organizing plugins in subdirectories for better organization

---

## Quick Start

### Universal Setup (Recommended)
1. Download and extract the files
2. Run `python setup.py` to install dependencies (works on all platforms)
3. Run `python main.py` to start the launcher
4. Type `inject` to launch the game with enhancements
5. Open `http://localhost:8080` in your browser to configure plugins

### Platform-Specific Setup
**All Platforms:**
- Run `python setup.py` (recommended)
- The universal setup script automatically detects your platform and installs the appropriate dependencies

---

## How to Use

### Starting the Launcher
```bash
python main.py
```

### Launching the Game
1. In the launcher, type `inject` and press Enter
2. The game will open in a browser window
3. Open `http://localhost:8080` in another browser tab
4. Configure your plugins using the web interface

> **Note:** On first launch, if the game requires you to log in, the injection process may fail. Simply close the browser, then run the `inject` command again in the launcher after logging in. This is normal for the first run.

### Web Interface
- **Plugin Configuration** - Toggle features on/off, adjust settings
- **Real-Time Updates** - See changes immediately
- **Search & Filter** - Find items and manage game data
- **Mobile Friendly** - Works on phones and tablets
- **Categorized Interface** - Browse plugins by category (Character, QoL, Unlocks, World-specific)
- **Visual Feedback** - Shimmer effects and visual indicators for selected plugins

---

## Available Plugins

### Character Plugins
- **Godlike Powers** - Comprehensive character enhancements (reach, crit, abilities, invincibility)
- **Instant Mob Respawn** - Toggle instant mob respawning
- **Inventory Storage** - Unlock all inventory packages and storage spaces
- **Quest Helper** - List and complete quests instantly
- **Spawn Item** - Drop any item in the game with autocomplete
- **Stats Multiplier** - Multiply various game stats by configurable amounts
- **Sneaking Items** - Item cheats for the sneaking game

### QoL (Quality of Life) Plugins
- **Global Storage** - Provides global storage functionality

### Unlocks Plugins
- **Candy Unlock** - Use Time Candy anywhere, bypassing map restrictions
- **Card Cheats** - Comprehensive card system cheats (set levels, add/remove cards)
- **Grimoire Unlocker** - Unlock and manage grimoire upgrades for Death Bringer class
- **Package Toggle** - Toggle bought packages and bundles
- **Vault Unlocker** - Unlock and manage vault upgrades with category-based controls
- **Sneaking Cheats** - Comprehensive cheats for the sneaking game

### World-Specific Plugins
- **Anvil Cheats** (World 1) - Cheats for anvil and smithing related features

---

## Project Structure

```
IdleonWeb/
├── plugins/           # Plugin files (add your own here)
│   ├── character/     # Character-related plugins
│   ├── qol/          # Quality of Life plugins
│   ├── unlocks/      # Unlock-related plugins
│   ├── world1/       # World 1 specific plugins
│   └── ...           # Additional plugin categories
├── core/             # Core system files
├── webui/            # Web interface files
├── main.py           # Main launcher
├── setup.py          # Universal setup script
└── README.md         # This file
```

---

## Troubleshooting

### Common Issues

**Game doesn't launch?**
- Make sure you have Chrome or Chromium installed
- Try running `inject` again after a few seconds

**Web interface not loading?**
- Check that the launcher shows "Plugin UI web server started"
- Try refreshing the browser page

**Plugins not working?**
- Ensure you typed `inject` in the launcher
- Check the browser console for error messages

**Setup fails?**
- Make sure Python 3.8+ and Node.js are installed
- Try running `python setup.py` - it can automatically install missing dependencies using package managers
- Run as administrator if needed (Windows)

### Getting Help

- Check the browser console for error messages
- Look for red error messages in the launcher
- Ensure all dependencies are properly installed

---

## Plugin Development

Want to create your own plugins? It's easy!

### Quick Start
1. Copy the example plugin: `cp plugins/example_plugin.py plugins/my_plugin.py`
2. Edit your plugin file
3. Add UI elements with decorators like `@ui_toggle`, `@ui_button`, `@ui_slider`
4. Add JavaScript code with `@js_export`
5. Test your plugin in the web UI

See [PLUGIN_QUICKSTART.md](PLUGIN_QUICKSTART.md) for a complete guide with examples!

### Available UI Elements
- **Toggles** - On/off switches
- **Buttons** - Action buttons
- **Sliders** - Range controls
- **Text Inputs** - Text fields
- **Search** - Search with results
- **Autocomplete** - Input with suggestions

### Plugin Categories
Plugins can be organized into categories by setting the `CATEGORY` attribute:
- `"Character"` - Character-related features
- `"QoL"` - Quality of Life improvements
- `"Unlocks"` - Unlock-related features
- `"World 1"`, `"World 2"`, etc. - World-specific features

### Plugin Ordering
Set the `PLUGIN_ORDER` attribute to control the display order in the UI (lower numbers appear first).

## Contributing

Want to add new features or fix bugs? See [DEVELOPMENT.md](DEVELOPMENT.md) for:

- Plugin development guide
- Architecture documentation
- Technical setup instructions
- Code contribution guidelines

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Credits

This project was inspired by and builds upon the excellent work of the original [Idleon-Injector](https://github.com/MrJoiny/Idleon-Injector) project by [@MrJoiny](https://github.com/MrJoiny). The original injector demonstrated the core concepts of browser automation and script injection for Legends of Idleon, which served as the foundation for this Python-based plugin system.

Key inspirations from the original project:
- Browser automation using Chrome DevTools Protocol
- Script interception and injection techniques
- Game context detection and integration
- Cross-platform compatibility approaches

This project extends those concepts with:
- Modern Python-based plugin architecture
- Web UI for plugin configuration
- Enhanced CLI with autocompletion
- Centralized configuration management
- Real-time plugin development workflow
- Categorized plugin organization
- Folderized plugin structure 