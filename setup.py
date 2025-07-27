#!/usr/bin/env python

import os
import sys
import subprocess
import json
import platform
from pathlib import Path

def print_status(message):
    print(f"[INFO] {message}")

def print_success(message):
    print(f"[SUCCESS] {message}")

def print_error(message):
    print(f"[ERROR] {message}")

def print_warning(message):
    print(f"[WARNING] {message}")

def is_windows():
    return platform.system().lower() == "windows"

def is_macos():
    return platform.system().lower() == "darwin"

def is_linux():
    return platform.system().lower() == "linux"

def get_shell_activate_cmd():
    if is_windows():
        return ".venv\\Scripts\\activate.bat"
    else:
        return "source .venv/bin/activate"

def check_command(command, name):
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

def check_package_manager():
    package_managers = {}
    
    if is_windows():
        try:
            result = subprocess.run(['choco', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                package_managers['chocolatey'] = result.stdout.strip()
                print_success(f"Found Chocolatey: {result.stdout.strip()}")
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            pass
    
    if is_macos() or is_linux():
        try:
            result = subprocess.run(['brew', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                package_managers['homebrew'] = result.stdout.strip().split('\n')[0]
                print_success(f"Found Homebrew: {result.stdout.strip().split(chr(10))[0]}")
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            pass
    
    if is_linux():
        try:
            result = subprocess.run(['apt', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                package_managers['apt'] = result.stdout.strip().split('\n')[0]
                print_success(f"Found apt: {result.stdout.strip().split(chr(10))[0]}")
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            pass
    
    if is_linux():
        try:
            result = subprocess.run(['pacman', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                package_managers['pacman'] = result.stdout.strip().split('\n')[0]
                print_success(f"Found pacman: {result.stdout.strip().split(chr(10))[0]}")
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            pass
    
    return package_managers

def install_package_manager(package_manager):
    if package_manager == 'chocolatey' and is_windows():
        print_status("Installing Chocolatey package manager...")
        install_script = '''
        Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        '''
        if run_command('powershell -Command "' + install_script + '"', "Installing Chocolatey"):
            print_success("Chocolatey installed successfully")
            return True
        else:
            print_error("Failed to install Chocolatey")
            return False
    
    elif package_manager == 'homebrew' and (is_macos() or is_linux()):
        print_status("Installing Homebrew package manager...")
        install_script = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        if run_command(install_script, "Installing Homebrew"):
            print_success("Homebrew installed successfully")
            return True
        else:
            print_error("Failed to install Homebrew")
            return False
    
    return False

def install_with_package_manager(package_manager, package_name, display_name):
    print_status(f"Installing {display_name} using {package_manager}...")
    
    if package_manager == 'chocolatey':
        cmd = f"choco install {package_name} -y"
    elif package_manager == 'homebrew':
        cmd = f"brew install {package_name}"
    elif package_manager == 'apt':
        cmd = f"sudo apt update && sudo apt install -y {package_name}"
    elif package_manager == 'pacman':
        cmd = f"sudo pacman -S --noconfirm {package_name}"
    else:
        print_error(f"Unsupported package manager: {package_manager}")
        return False
    
    if run_command(cmd, f"Installing {display_name}"):
        print_success(f"{display_name} installed successfully")
        return True
    else:
        print_error(f"Failed to install {display_name}")
        return False

def run_command(command, description, cwd=None, check=True):
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
    print_status("Installing Python dependencies...")
    
    activate_cmd = get_shell_activate_cmd()
    
    if is_windows():
        install_cmd = f"cmd /c \"{activate_cmd} && python -m pip install --upgrade pip\""
    else:
        install_cmd = f"bash -c '{activate_cmd} && python -m pip install --upgrade pip'"
    
    if not run_command(install_cmd, "Upgrading pip"):
        return False
    
    if Path("requirements.txt").exists():
        if is_windows():
            install_cmd = f"cmd /c \"{activate_cmd} && pip install -r requirements.txt\""
        else:
            install_cmd = f"bash -c '{activate_cmd} && pip install -r requirements.txt'"
        
        if run_command(install_cmd, "Installing requirements from requirements.txt"):
            print_success("Python dependencies installed successfully")
            return True
        else:
            print_error("Failed to install Python dependencies")
            return False
    else:
        print_warning("requirements.txt not found. Installing basic dependencies...")
        basic_deps = "prompt_toolkit rich pychrome aiohttp aiohttp-jinja2 jinja2"
        
        if is_windows():
            install_cmd = f"cmd /c \"{activate_cmd} && pip install {basic_deps}\""
        else:
            install_cmd = f"bash -c '{activate_cmd} && pip install {basic_deps}'"
        
        if run_command(install_cmd, "Installing basic dependencies"):
            print_success("Basic Python dependencies installed")
            return True
        else:
            print_error("Failed to install basic Python dependencies")
            return False

def install_node_deps():
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
    print_status("Creating necessary directories...")
    
    directories = ["plugins", "core", "core/tmp_js"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print_success("Directories created successfully")

def create_initial_config():
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
            "instant_mob_respawn",
            "package_toggle",
            "inventory_storage",
            "candy_unlock",
            "quest_helper",
            "vault_unlocker"
        ],
        "plugin_configs": {
            "spawn_item": {
                "debug": False
            },
            "instant_mob_respawn": {
                "debug": False,
                "toggle": False
            },
            "package_toggle": {
                "debug": False
            },
            "inventory_storage": {
                "debug": False
            },
            "candy_unlock": {
                "debug": False,
                "unlock_candy": True
            },
            "quest_helper": {
                "debug": False
            },
            "vault_unlocker": {
                "debug": False
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

def get_platform_info():
    system = platform.system()
    release = platform.release()
    version = platform.version()
    machine = platform.machine()
    
    print_status(f"Platform: {system} {release} ({machine})")
    print_status(f"Python: {sys.version}")
    
    return {
        'system': system,
        'release': release,
        'version': version,
        'machine': machine
    }

def main():
    platform_info = get_platform_info()
    print(f"Setting up IdleonWeb development environment for {platform_info['system']}...")
    print()
    
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
        
        package_managers = check_package_manager()
        
        if not package_managers:
            print_status("No package managers found.")
            print("Available package managers for automatic installation:")
            if is_windows():
                print("- Chocolatey (recommended)")
            if is_macos():
                print("- Homebrew (recommended)")
            if is_linux():
                print("- apt (Ubuntu/Debian)")
                print("- pacman (Arch Linux)")
                print("- Homebrew (cross-platform)")
            
            response = input("Would you like to install a package manager? (y/n): ").lower().strip()
            
            if response in ['y', 'yes']:
                if is_windows():
                    if install_package_manager('chocolatey'):
                        package_managers['chocolatey'] = 'installed'
                elif is_macos():
                    if install_package_manager('homebrew'):
                        package_managers['homebrew'] = 'installed'
                elif is_linux():
                    print("Choose a package manager to install:")
                    print("1. Homebrew (recommended)")
                    print("2. apt (Ubuntu/Debian)")
                    print("3. pacman (Arch Linux)")
                    choice = input("Enter choice (1-3): ").strip()
                    
                    if choice == '1':
                        if install_package_manager('homebrew'):
                            package_managers['homebrew'] = 'installed'
                    elif choice == '2':
                        package_managers['apt'] = 'available'
                    elif choice == '3':
                        package_managers['pacman'] = 'available'
            else:
                print_error("Please install the missing dependencies manually and try again.")
                input("Press Enter to exit...")
                sys.exit(1)
        
        if package_managers:
            print_status("Using package manager to install missing dependencies...")
            
            if not python_ok:
                if 'chocolatey' in package_managers:
                    install_with_package_manager('chocolatey', 'python', 'Python')
                elif 'homebrew' in package_managers:
                    install_with_package_manager('homebrew', 'python', 'Python')
                elif 'apt' in package_managers:
                    install_with_package_manager('apt', 'python3', 'Python')
                elif 'pacman' in package_managers:
                    install_with_package_manager('pacman', 'python', 'Python')
            
            if not node_ok:
                if 'chocolatey' in package_managers:
                    install_with_package_manager('chocolatey', 'nodejs', 'Node.js')
                elif 'homebrew' in package_managers:
                    install_with_package_manager('homebrew', 'node', 'Node.js')
                elif 'apt' in package_managers:
                    install_with_package_manager('apt', 'nodejs', 'Node.js')
                elif 'pacman' in package_managers:
                    install_with_package_manager('pacman', 'nodejs', 'Node.js')
            
            if not npm_ok:
                print_status("Checking npm again (should be installed with Node.js)...")
                npm_ok = check_command("npm", "npm")
                if not npm_ok:
                    print_error("npm still not found after Node.js installation.")
                    input("Press Enter to exit...")
                    sys.exit(1)
            
            print()
            print_success("All dependencies installed successfully!")
            print()
    
    print()
    print_status("All dependencies found successfully")
    print()
    
    if not create_virtual_environment():
        input("Press Enter to exit...")
        sys.exit(1)
    
    if not activate_and_install_python_deps():
        input("Press Enter to exit...")
        sys.exit(1)
    
    install_node_deps()
    
    create_directories()
    
    if not create_initial_config():
        input("Press Enter to exit...")
        sys.exit(1)
    
    print()
    print_success("Setup completed successfully!")
    print()
    
    if is_windows():
        print("Next steps:")
        print("1. Activate the virtual environment:")
        print("   - Command Prompt: .venv\\Scripts\\activate.bat")
        print("   - PowerShell: .venv\\Scripts\\Activate.ps1")
        print("2. Run the application: python main.py")
    else:
        print("Next steps:")
        print("1. Activate the virtual environment: source .venv/bin/activate")
        print("2. Run the application: python main.py")
    
    print()
    print("Setup complete.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main() 