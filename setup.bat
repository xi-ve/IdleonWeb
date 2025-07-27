@echo off
REM IdleonWeb Setup Script for Windows
REM This script sets up the development environment for IdleonWeb on Windows

echo Setting up IdleonWeb development environment for Windows...

REM Check if Python 3 is installed
echo [INFO] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python 3.8+ and try again.
    pause
    exit /b 1
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do echo [SUCCESS] Found Python: %%i
)

REM Check if Node.js is installed
echo [INFO] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed. Please install Node.js and try again.
    pause
    exit /b 1
) else (
    for /f "tokens=1" %%i in ('node --version 2^>^&1') do echo [SUCCESS] Found Node.js: %%i
)

echo [INFO] Checking npm installation...
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm is not installed. Please install npm and try again.
    pause
    exit /b 1
) else (
    for /f "tokens=1" %%i in ('npm --version 2^>^&1') do echo [SUCCESS] Found npm: %%i
)

REM Create virtual environment
echo [INFO] Setting up Python virtual environment...
if exist ".venv" (
    echo [WARNING] Virtual environment already exists. Removing old one...
    rmdir /s /q .venv
)

python -m venv .venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
) else (
    echo [SUCCESS] Virtual environment created successfully
)

REM Activate virtual environment and install Python requirements
echo [INFO] Installing Python dependencies...
call .venv\Scripts\activate.bat

echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

if exist "requirements.txt" (
    echo [INFO] Installing requirements from requirements.txt...
    pip install -r requirements.txt
    echo [SUCCESS] Python dependencies installed successfully
) else (
    echo [WARNING] requirements.txt not found. Installing basic dependencies...
    pip install prompt_toolkit rich pychrome
    echo [SUCCESS] Basic Python dependencies installed
)

REM Install Node.js dependencies
echo [INFO] Installing Node.js dependencies...
if exist "core" (
    cd core
    if exist "package.json" (
        echo [INFO] Installing npm dependencies from package.json...
        npm install
        echo [SUCCESS] Node.js dependencies installed successfully
    ) else (
        echo [WARNING] package.json not found in core directory
    )
    cd ..
) else (
    echo [WARNING] core directory not found
)

REM Create necessary directories
echo [INFO] Creating necessary directories...
if not exist "plugins" mkdir plugins
echo [SUCCESS] Created plugins directory

if not exist "core" mkdir core
echo [SUCCESS] Created core directory

if not exist "core\tmp_js" mkdir core\tmp_js
echo [SUCCESS] Created core\tmp_js directory

REM Generate initial config if it doesn't exist
echo [INFO] Setting up initial configuration...
if not exist "core\conf.json" (
    echo {> core\conf.json
    echo   "openDevTools": false,>> core\conf.json
    echo   "interactive": true,>> core\conf.json
    echo   "plugins": [>> core\conf.json
    echo     "spawn_item",>> core\conf.json
    echo     "instant_mob_respawn">> core\conf.json
    echo   ],>> core\conf.json
    echo   "plugin_configs": {>> core\conf.json
    echo     "spawn_item": {>> core\conf.json
    echo       "debug": false>> core\conf.json
    echo     },>> core\conf.json
    echo     "instant_mob_respawn": {>> core\conf.json
    echo       "debug": true,>> core\conf.json
    echo       "toggle": false>> core\conf.json
    echo     }>> core\conf.json
    echo   },>> core\conf.json
    echo   "debug": false,>> core\conf.json
    echo   "injectFiles": [>> core\conf.json
    echo     "plugins_combined.js">> core\conf.json
    echo   ]>> core\conf.json
    echo }>> core\conf.json
    echo [SUCCESS] Created initial conf.json
) else (
    echo [INFO] conf.json already exists
)

echo.
echo [SUCCESS] Setup completed successfully!
echo.
echo Next steps:
echo 1. Activate the virtual environment: .venv\Scripts\activate
echo 2. Run the application: python main.py
echo.
echo Setup complete.
pause 