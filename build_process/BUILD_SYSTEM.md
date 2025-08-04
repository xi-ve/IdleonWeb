# IdleonWeb Standalone Build System

This directory contains scripts to build standalone executables of IdleonWeb for distribution to end users.

## Overview

The build system creates self-contained executables that include:
- Python runtime
- All dependencies (Node.js core files, Python packages)
- Plugin system
- Web UI
- Configuration management

Users can run these executables without installing Python, Node.js, or any dependencies.

## Build Requirements

### Dependencies
```bash
# Install build dependencies
pip install -r build_process/build-requirements.txt
```

Required tools:
- **Python 3.8+** with PyInstaller
- **Node.js 22+** (for bundling core files)
- **npm** (for installing core dependencies)

### Platform-Specific Requirements

**Windows:**
- Visual Studio Build Tools (for some native dependencies)
- Optional: NSIS for creating installers

**Linux:**
- `gcc` and development headers
- Optional: `linuxdeploy` for AppImage creation

**macOS:**
- Xcode Command Line Tools
- Optional: `dmgbuild` for DMG creation

## Usage

### Basic Building

```bash
# Build for current platform
python build_process/build_standalone.py

# Build for specific platform
python build_process/build_standalone.py --platform windows
python build_process/build_standalone.py --platform linux
python build_process/build_standalone.py --platform macos

# Build for all platforms (requires cross-platform setup)
python build_process/build_standalone.py --platform all
```

### Advanced Options

```bash
# Custom output directory
python build_process/build_standalone.py --output-dir my_builds

# Keep temporary files for debugging
python build_process/build_standalone.py --no-cleanup

# Specify version
python build_process/build_standalone.py --version 1.2.3
```

### CI/CD Pipeline

For automated builds after integration tests:

**Linux/macOS:**
```bash
./build_process/build_pipeline.sh
```

**Windows:**
```cmd
build_process\build_pipeline.bat
```

## Output

Built executables are placed in:
```
build/
├── dist/
│   ├── windows/
│   │   └── IdleonWeb.exe      (~15-25 MB)
│   ├── linux/
│   │   └── IdleonWeb          (~15-25 MB)
│   └── macos/
│       └── IdleonWeb          (~15-25 MB)
└── temp/                      (cleaned up by default)
```

## Distribution

The generated executables are completely standalone and can be distributed as-is:

1. **Windows**: `IdleonWeb.exe` - Double-click to run
2. **Linux**: `IdleonWeb` - `chmod +x IdleonWeb && ./IdleonWeb`
3. **macOS**: `IdleonWeb` - `chmod +x IdleonWeb && ./IdleonWeb`

## Build Process Details

### What Gets Bundled

1. **Python Runtime**: Embedded Python interpreter
2. **Core Dependencies**: All required Python packages
3. **Node.js Assets**: Pre-built core JavaScript files
4. **Plugin System**: All plugins and plugin framework
5. **Web UI**: Complete web interface
6. **Configuration**: Default configuration and management

### Optimizations

- **Excluded Modules**: Large unnecessary packages (tkinter, matplotlib, etc.)
- **Hidden Imports**: Explicitly included required modules
- **Asset Bundling**: Pre-compiled JavaScript and CSS
- **Compression**: PyInstaller's built-in compression

### Size Optimization

The build system excludes unnecessary modules and optimizes for size:

- Typical executable size: 15-25 MB
- Startup time: 2-5 seconds
- Memory usage: Similar to regular Python version

## Cross-Platform Building

### Limitations

- **Best Practice**: Build on the target platform
- **Cross-compilation**: Limited support, may not work for all dependencies
- **Native Dependencies**: Some packages require platform-specific compilation

### Recommended Approach

For production releases:
1. Use CI/CD with platform-specific runners
2. Build Windows executables on Windows
3. Build Linux executables on Linux
4. Build macOS executables on macOS

## Troubleshooting

### Common Issues

**"Module not found" errors:**
- Add missing modules to `hidden_imports` in `build_process/build_standalone.py`
- Check if the module needs special handling in PyInstaller

**Large executable size:**
- Add unnecessary modules to `exclude_modules`
- Use `--debug` with PyInstaller to analyze what's included

**Slow startup:**
- Check for excessive imports in the main script
- Consider lazy loading for heavy modules

**Missing files at runtime:**
- Add data files to the `--add-data` arguments
- Check file paths are relative to the executable

### Debug Mode

```bash
# Build with debug info
python build_process/build_standalone.py --no-cleanup

# Check what's included
cd build/temp/work
find . -name "*.spec" -exec cat {} \;
```

### Testing Built Executables

Before distribution:
1. Test on clean systems without development tools
2. Verify all plugins work correctly
3. Test web UI functionality
4. Check auto-injection works
5. Verify configuration persistence

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Build Standalone
on:
  workflow_run:
    workflows: ["Integration Tests"]
    types: [completed]
    branches: [main]

jobs:
  build-windows:
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
      - run: build_process/build_pipeline.bat
      - uses: actions/upload-artifact@v4
        with:
          name: idleonweb-windows
          path: release-artifacts/

  # Similar jobs for Linux and macOS...
```

### GitLab CI Example

```yaml
build_standalone:
  stage: build
  needs: ["integration_tests"]
  script:
    - ./build_process/build_pipeline.sh
  artifacts:
    paths:
      - release-artifacts/
    expire_in: 1 week
  only:
    - main
```

## Future Enhancements

Potential improvements:
- **Auto-updater**: Built-in update mechanism
- **Installers**: Platform-specific installer packages
- **Code signing**: Signed executables for security
- **Portable mode**: USB-stick friendly version
- **Minimal builds**: Feature-specific executables

## Security Considerations

- Executables are not code-signed by default
- Users may see security warnings on first run
- Consider code signing for production releases
- Antivirus software may flag PyInstaller executables (false positive)

## Performance Notes

Standalone executables:
- **Startup**: 2-5 seconds (vs 1-2 seconds for Python script)
- **Memory**: +10-20 MB overhead for bundled runtime
- **Disk**: 15-25 MB (vs ~100 KB for Python script + dependencies)
- **Functionality**: Identical to Python version
