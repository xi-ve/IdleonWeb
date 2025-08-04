@echo off
REM Build script for Windows CI/CD pipeline
REM This script is designed to run after integration tests succeed

echo IdleonWeb Standalone Build Pipeline
echo ===================================

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

REM Run the build
echo Starting build process...
if defined VERSION (
    python build_process\build_standalone.py --platform current --version %VERSION%
) else (
    python build_process\build_standalone.py --platform current
)

if errorlevel 1 (
    echo Build failed
    exit /b 1
)

REM Check if build was successful
if exist "build\dist" (
    echo Build successful!
    echo Generated files:
    dir build\dist\windows\ /s
    
    REM Create release artifacts directory
    if not exist release-artifacts mkdir release-artifacts
    
    REM Copy executable to release artifacts
    copy build\dist\windows\IdleonWeb.exe release-artifacts\IdleonWeb-windows.exe
    
    echo Release artifacts created in release-artifacts\
    dir release-artifacts\
) else (
    echo Build failed - no output directory found
    exit /b 1
)

echo Build pipeline completed successfully!
