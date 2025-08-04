# Build Process

This folder contains all the build-related scripts and documentation for creating standalone IdleonWeb executables.

## Files

- **`build_standalone.py`** - Main build script for creating standalone executables
- **`build-requirements.txt`** - Dependencies needed for building
- **`build_pipeline.sh`** - Linux/macOS CI/CD build script
- **`build_pipeline.bat`** - Windows CI/CD build script
- **`BUILD_SYSTEM.md`** - Comprehensive documentation for the build system

## Quick Start

From the project root directory:

```bash
# Install build dependencies
pip install -r build_process/build-requirements.txt

# Build for current platform
python build_process/build_standalone.py

# Run CI/CD pipeline (Linux/macOS)
./build_process/build_pipeline.sh

# Run CI/CD pipeline (Windows)
build_process\build_pipeline.bat
```

## Output

Built executables will be created in:
- `build/dist/` - Platform-specific executables
- `release-artifacts/` - Ready-to-distribute files

See `BUILD_SYSTEM.md` for complete documentation.
