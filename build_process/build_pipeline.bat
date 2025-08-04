@echo off
REM Build script for Windows CI/CD pipeline
REM This script is designed to run after integration tests succeed

echo IdleonWeb Standalone Build Pipeline
echo ===================================

REM Check Node.js availability
echo Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found. Please install Node.js first.
    exit /b 1
)

REM Install build dependencies
echo Installing build dependencies...
pip install -r build_process\build-requirements.txt
if errorlevel 1 (
    echo Failed to install build dependencies
    exit /b 1
)

REM Get version from VERSION file if it exists
set VERSION=
if exist VERSION (
    set /p VERSION=<VERSION
    echo Version: %VERSION%
)

REM Run the build with current platform detection
echo Starting build process...
python build_process\build_standalone.py --platform current --output build_windows --clean

if errorlevel 1 (
    echo Build failed
    exit /b 1
)

REM Check if build was successful
if exist "build_windows\dist" (
    echo Build successful!
    echo Generated files:
    dir build_windows\dist\windows\ /s
    
    REM Create release artifacts directory
    if not exist release-artifacts mkdir release-artifacts
    
    REM Copy executable to release artifacts
    copy build_windows\dist\windows\IdleonWeb.exe release-artifacts\IdleonWeb-windows.exe
    
    echo Release artifacts created in release-artifacts\
    dir release-artifacts\
    
    echo.
    echo NOTE: This executable requires Node.js to be installed on the target system
    echo Node.js dependencies will be installed automatically on first run
) else (
    echo Build failed - no output directory found
    exit /b 1
)

echo Build pipeline completed successfully!
