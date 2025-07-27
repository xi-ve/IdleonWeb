#!/usr/bin/env python
"""
IdleonWeb Windows Setup Script
This script sets up the development environment for IdleonWeb on Windows
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_status(message):
    print(f"[INFO] {message}")

def print_success(message):
    print(f"[SUCCESS] {message}")

def print_error(message):
    print(f"[ERROR] {message}")

def print_warning(message):
    print(f"[WARNING] {message}")

def check_command(command, name):
    """Check if a command is available"""
    try:
        result = subprocess.run([command, '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip().split('\n')[0]
            print_success(f"Found {name}: {version}")
            return True
        else:
            print_error(f"{name} is not installed or not working properly")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
        print_error(f"{name} is not installed.")
        return False

def check_chocolatey():
    """Check if Chocolatey is installed"""
    try:
        result = subprocess.run(['choco', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            print_success(f"Found Chocolatey: {version}")
            return True
        else:
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
        return False

def install_with_chocolatey(package_name, display_name):
    """Install a package using Chocolatey"""
    print_status(f"Installing {display_name} using Chocolatey...")
    if run_command(f"choco install {package_name} -y", f"Installing {display_name}"):
        print_success(f"{display_name} installed successfully")
        return True
    else:
        print_error(f"Failed to install {display_name}")
        return False

def refresh_environment():
    """Refresh environment variables after installation"""
    print_status("Refreshing environment variables...")
    try:
        # Import os to refresh environment
        import os
        # This will refresh the PATH and other environment variables
        os.environ.update(os.environ.copy())
        print_success("Environment refreshed")
        return True
    except Exception as e:
        print_warning(f"Could not refresh environment: {e}")
        return False

def install_chocolatey():
    """Install Chocolatey package manager"""
    print_status("Installing Chocolatey package manager...")
    install_script = '''
    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    '''
    if run_command(f'powershell -Command "{install_script}"', "Installing Chocolatey"):
        print_success("Chocolatey installed successfully")
        return True
    else:
        print_error("Failed to install Chocolatey")
        return False

def run_command(command, description, cwd=None, check=True):
    """Run a command and handle errors"""
    print_status(f"{description}...")
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, check=check,
                              capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print_success(f"{description} completed successfully")
            return True
        else:
            print_error(f"{description} failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print_error(f"{description} timed out")
        return False
    except subprocess.CalledProcessError as e:
        print_error(f"{description} failed: {e}")
        return False

def create_virtual_environment():
    """Create Python virtual environment"""
    venv_path = Path(".venv")
    
    if venv_path.exists():
        print_warning("Virtual environment already exists. Removing old one...")
        try:
            import shutil
            shutil.rmtree(venv_path)
        except Exception as e:
            print_warning(f"Failed to remove old virtual environment: {e}")
    
    print_status("Creating Python virtual environment...")
    if run_command("python -m venv .venv", "Creating virtual environment"):
        print_success("Virtual environment created successfully")
        return True
    else:
        print_error("Failed to create virtual environment")
        return False

def activate_and_install_python_deps():
    """Activate virtual environment and install Python dependencies"""
    print_status("Installing Python dependencies...")
    
    # Activate virtual environment and upgrade pip
    activate_cmd = ".venv\\Scripts\\activate && python -m pip install --upgrade pip"
    if not run_command(activate_cmd, "Upgrading pip"):
        return False
    
    # Install requirements
    if Path("requirements.txt").exists():
        install_cmd = ".venv\\Scripts\\activate && pip install -r requirements.txt"
        if run_command(install_cmd, "Installing requirements from requirements.txt"):
            print_success("Python dependencies installed successfully")
            return True
        else:
            print_error("Failed to install Python dependencies")
            return False
    else:
        print_warning("requirements.txt not found. Installing basic dependencies...")
        install_cmd = ".venv\\Scripts\\activate && pip install prompt_toolkit rich pychrome aiohttp aiohttp-jinja2 jinja2"
        if run_command(install_cmd, "Installing basic dependencies"):
            print_success("Basic Python dependencies installed")
            return True
        else:
            print_error("Failed to install basic Python dependencies")
            return False

def install_node_deps():
    """Install Node.js dependencies"""
    print_status("Installing Node.js dependencies...")
    
    core_path = Path("core")
    if not core_path.exists():
        print_warning("core directory not found")
        return False
    
    package_json = core_path / "package.json"
    if not package_json.exists():
        print_warning("package.json not found in core directory")
        return False
    
    if run_command("npm install", "Installing npm dependencies", cwd="core"):
        print_success("Node.js dependencies installed successfully")
        return True
    else:
        print_error("Failed to install Node.js dependencies")
        return False

def create_directories():
    """Create necessary directories"""
    print_status("Creating necessary directories...")
    
    directories = ["plugins", "core", "core/tmp_js"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print_success("Directories created successfully")

def create_initial_config():
    """Create initial configuration file"""
    print_status("Setting up initial configuration...")
    
    config_path = Path("core/conf.json")
    if config_path.exists():
        print_status("conf.json already exists")
        return True
    
    config = {
        "openDevTools": False,
        "interactive": True,
        "plugins": [
            "spawn_item",
            "instant_mob_respawn"
        ],
        "plugin_configs": {
            "spawn_item": {
                "debug": False
            },
            "instant_mob_respawn": {
                "debug": False,
                "toggle": False
            }
        },
        "debug": False,
        "injector": {
            "cdp_port": 32123,
            "njs_pattern": "*N.js",
            "idleon_url": "https://www.legendsofidleon.com/ytGl5oc/"
        }
    }
    
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print_success("Created initial conf.json")
        return True
    except Exception as e:
        print_error(f"Failed to create conf.json: {e}")
        return False

def main():
    """Main setup function"""
    print("Setting up IdleonWeb development environment for Windows...")
    print()
    
    # Check prerequisites
    print_status("Checking prerequisites...")
    python_ok = check_command("python", "Python")
    node_ok = check_command("node", "Node.js")
    npm_ok = check_command("npm", "npm")
    
    missing_deps = []
    if not python_ok:
        missing_deps.append("Python")
    if not node_ok:
        missing_deps.append("Node.js")
    if not npm_ok:
        missing_deps.append("npm")
    
    if missing_deps:
        print_error(f"Missing dependencies: {', '.join(missing_deps)}")
        print()
        
        # Check if Chocolatey is available
        chocolatey_ok = check_chocolatey()
        
        if not chocolatey_ok:
            print_status("Chocolatey package manager not found.")
            print("Chocolatey can automatically install missing dependencies.")
            response = input("Would you like to install Chocolatey? (y/n): ").lower().strip()
            
            if response in ['y', 'yes']:
                if install_chocolatey():
                    chocolatey_ok = True
                else:
                    print_error("Failed to install Chocolatey. Please install dependencies manually.")
                    input("Press Enter to exit...")
                    sys.exit(1)
            else:
                print_error("Please install the missing dependencies manually and try again.")
                input("Press Enter to exit...")
                sys.exit(1)
        
        if chocolatey_ok:
            print_status("Using Chocolatey to install missing dependencies...")
            
            # Install missing dependencies
            if not python_ok:
                if not install_with_chocolatey("python", "Python"):
                    print_error("Failed to install Python. Please install manually.")
                    input("Press Enter to exit...")
                    sys.exit(1)
            
            if not node_ok:
                if not install_with_chocolatey("nodejs", "Node.js"):
                    print_error("Failed to install Node.js. Please install manually.")
                    input("Press Enter to exit...")
                    sys.exit(1)
                # Refresh environment after Node.js installation
                refresh_environment()
            
            if not npm_ok:
                # npm comes with Node.js, but let's check again
                print_status("Checking npm again (should be installed with Node.js)...")
                npm_ok = check_command("npm", "npm")
                if not npm_ok:
                    # Try to find npm in common Node.js installation paths
                    print_status("npm not found in PATH, checking common installation paths...")
                    npm_paths = [
                        r"C:\Program Files\nodejs\npm.cmd",
                        r"C:\Program Files (x86)\nodejs\npm.cmd",
                        os.path.expanduser(r"~\AppData\Roaming\npm\npm.cmd"),
                        os.path.expanduser(r"~\AppData\Local\npm\npm.cmd")
                    ]
                    
                    npm_found = False
                    for npm_path in npm_paths:
                        if os.path.exists(npm_path):
                            print_success(f"Found npm at: {npm_path}")
                            # Add to PATH temporarily
                            current_path = os.environ.get('PATH', '')
                            npm_dir = os.path.dirname(npm_path)
                            os.environ['PATH'] = f"{npm_dir};{current_path}"
                            npm_found = True
                            break
                    
                    if not npm_found:
                        print_error("npm still not found after Node.js installation.")
                        print_status("Trying to install npm separately...")
                        if install_with_chocolatey("npm", "npm"):
                            refresh_environment()
                            npm_ok = check_command("npm", "npm")
                            if npm_ok:
                                print_success("npm installed and verified successfully")
                            else:
                                print_error("npm installation failed. Please install manually.")
                                input("Press Enter to exit...")
                                sys.exit(1)
                        else:
                            print_error("Failed to install npm. Please install manually.")
                            input("Press Enter to exit...")
                            sys.exit(1)
            
            print()
            print_success("All dependencies installed successfully!")
            print()
    
    print()
    print_status("All dependencies found successfully")
    print()
    
    # Create virtual environment
    if not create_virtual_environment():
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Install Python dependencies
    if not activate_and_install_python_deps():
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Install Node.js dependencies
    install_node_deps()  # Don't fail if this doesn't work
    
    # Create directories
    create_directories()
    
    # Create initial config
    if not create_initial_config():
        input("Press Enter to exit...")
        sys.exit(1)
    
    print()
    print_success("Setup completed successfully!")
    print()
    print("Next steps:")
    print("1. Activate the virtual environment: .venv\\Scripts\\activate")
    print("2. Run the application: python main.py")
    print()
    print("Setup complete.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main() 