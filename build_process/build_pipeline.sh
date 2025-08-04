#!/bin/bash
# Build script for CI/CD pipeline
# This script is designed to run after integration tests succeed

set -e  # Exit on any error

echo "IdleonWeb Standalone Build Pipeline"
echo "==================================="

# Get the current platform
PLATFORM=$(python3 -c "import platform; print(platform.system().lower())")
echo "Detected platform: $PLATFORM"

# Install build dependencies
echo "Installing build dependencies..."
pip install -r build_process/build-requirements.txt

# Get version from VERSION file if it exists
VERSION=""
if [ -f "VERSION" ]; then
    VERSION=$(cat VERSION)
    echo "Version: $VERSION"
fi

# Run the build
echo "Starting build process..."
if [ -n "$VERSION" ]; then
    python3 build_process/build_standalone.py --platform current --version "$VERSION"
else
    python3 build_process/build_standalone.py --platform current
fi

# Check if build was successful
if [ -d "build/dist" ]; then
    echo "Build successful!"
    echo "Generated files:"
    find build/dist -type f -exec ls -lh {} \;
    
    # Create release artifacts directory
    mkdir -p release-artifacts
    
    # Copy executables to release artifacts
    if [ "$PLATFORM" = "windows" ]; then
        cp build/dist/windows/IdleonWeb.exe release-artifacts/IdleonWeb-windows.exe
    elif [ "$PLATFORM" = "linux" ]; then
        cp build/dist/linux/IdleonWeb release-artifacts/IdleonWeb-linux
        chmod +x release-artifacts/IdleonWeb-linux
    elif [ "$PLATFORM" = "darwin" ]; then
        cp build/dist/macos/IdleonWeb release-artifacts/IdleonWeb-macos
        chmod +x release-artifacts/IdleonWeb-macos
    fi
    
    echo "Release artifacts created in release-artifacts/"
    ls -la release-artifacts/
else
    echo "Build failed - no output directory found"
    exit 1
fi

echo "Build pipeline completed successfully!"
