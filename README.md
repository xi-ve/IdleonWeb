# IdleonWeb

A modern, user-friendly launcher and plugin system for enhancing Legends of Idleon with a beautiful web interface.

> **For developers:** See [DEVELOPMENT.md](DEVELOPMENT.md) for technical documentation, plugin development guides, and architecture details.

---

## Features

- **Easy-to-Use Web Interface** - Configure plugins and manage game enhancements through a modern web browser
- **Plugin System** - Add new features by simply dropping plugin files into the `plugins/` folder
- **Real-Time Updates** - See changes instantly as you configure plugins
- **Cross-Platform** - Works on Windows, Linux, and macOS
- **One-Click Setup** - Automated installation scripts for all platforms

---

## Quick Start

### Windows
1. Download and extract the files
2. Double-click `setup.bat` to install dependencies
3. Run `python main.py` to start the launcher
4. Type `inject` to launch the game with enhancements
5. Open `http://localhost:8080` in your browser to configure plugins

### Linux/macOS
1. Download and extract the files
2. Run `./setup.sh` to install dependencies
3. Run `python main.py` to start the launcher
4. Type `inject` to launch the game with enhancements
5. Open `http://localhost:8080` in your browser to configure plugins

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

### Web Interface
- **Plugin Configuration** - Toggle features on/off, adjust settings
- **Real-Time Updates** - See changes immediately
- **Search & Filter** - Find items and manage game data
- **Mobile Friendly** - Works on phones and tablets

---

## Available Plugins

### Spawn Item Plugin
- **Spawn Items** - Drop any item in the game with autocomplete
- **List All Items** - Browse the complete item database
- **Search Items** - Find items by name or ID

### Instant Mob Respawn Plugin
- **Toggle Respawn** - Enable/disable instant mob respawning
- **Debug Mode** - Enable detailed logging

---

## Project Structure

```
IdleonWeb/
├── plugins/           # Plugin files (add your own here)
├── core/             # Core system files
├── webui/            # Web interface files
├── main.py           # Main launcher
├── setup.sh          # Linux/macOS setup
├── setup.bat         # Windows setup
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
- Try running the setup script as administrator (Windows)

### Getting Help

- Check the browser console for error messages
- Look for red error messages in the launcher
- Ensure all dependencies are properly installed

---

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

This project was inspired by the excellent work of the original [Idleon-Injector](https://github.com/MrJoiny/Idleon-Injector) project by [@MrJoiny](https://github.com/MrJoiny). 