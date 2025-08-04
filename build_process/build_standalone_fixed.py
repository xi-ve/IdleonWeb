#!/usr/bin/env python3
"""
IdleonWeb Standalone Build Script
Builds standalone executables for multiple platforms using PyInstaller.

Supported platforms:
- Windows (.exe)
- Linux (binary)
- macOS (.app)

Requirements:
- PyInstaller
- Node.js and npm (for core file bundling)
- Python virtual environment with all dependencies

Usage:
    python build_standalone.py --platform all --output build
    python build_standalone.py --platform linux --output myapp_v1.0
    python build_standalone.py --platform windows --optimize --clean
"""

import argparse
import subprocess
import sys
import shutil
import json
from pathlib import Path
from typing import List, Dict, Any

# Build configuration
BUILD_CONFIG = {
    "hidden_imports": [
        "aiohttp", "aiohttp_jinja2", "jinja2", "rich", "prompt_toolkit", "pychrome",
        "pathlib", "json", "asyncio", "logging", "importlib", "inspect"
    ],
    "exclude_modules": [
        "tkinter", "matplotlib", "numpy", "scipy", "pandas", "PIL",
        "PyQt5", "PyQt6", "PySide2", "PySide6", "jupyter", "IPython", "notebook"
    ]
}

def print_status(message: str):
    """Print a status message."""
    print(f"[BUILD] {message}")

def print_success(message: str):
    """Print a success message."""
    print(f"[SUCCESS] {message}")

def print_error(message: str):
    """Print an error message."""
    print(f"[ERROR] {message}")

def print_warning(message: str):
    """Print a warning message."""
    print(f"[WARNING] {message}")

def check_dependencies():
    """Check if required build dependencies are available."""
    print_status("Checking build dependencies...")
    
    # Check PyInstaller
    try:
        import PyInstaller
        print_success(f"PyInstaller {PyInstaller.__version__} found")
    except ImportError:
        print_error("PyInstaller not found. Install with: pip install pyinstaller")
        return False
    
    # Check Node.js
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, check=True)
        print_success(f"Node.js {result.stdout.strip()} found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_error("Node.js not found. Please install Node.js")
        return False
    
    # Check npm
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True, check=True)
        print_success(f"npm {result.stdout.strip()} found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_error("npm not found. Please install npm")
        return False
    
    return True

def run_command(command: List[str], cwd: Path = None, check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    print_status(f"Running: {' '.join(command)}")
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=check,
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.stdout:
            print(f"[STDOUT] {result.stdout.strip()}")
        if result.stderr and result.returncode != 0:
            print(f"[STDERR] {result.stderr.strip()}")
        return result
    except subprocess.TimeoutExpired:
        print_error("Command timed out")
        raise
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed with exit code {e.returncode}")
        if e.stderr:
            print_error(f"Error output: {e.stderr}")
        if not check:
            # Return a mock CompletedProcess for failed commands when check=False
            return subprocess.CompletedProcess(command, e.returncode, e.stdout, e.stderr)
        raise

def prepare_build_environment(build_dir: Path) -> Path:
    """Prepare the build environment."""
    print_status("Preparing build environment...")
    
    # Create build directory structure
    temp_dir = build_dir / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    return temp_dir

def bundle_core_files(temp_dir: Path) -> bool:
    """Bundle core files using npm."""
    print_status("Bundling core files...")
    
    core_src = Path("core")
    core_dest = temp_dir / "core"
    
    if not core_src.exists():
        print_warning("Core directory not found, skipping core bundling")
        return True
    
    # Copy core files
    if core_dest.exists():
        shutil.rmtree(core_dest)
    shutil.copytree(core_src, core_dest)
    
    # Install dependencies if package.json exists
    package_json = core_dest / "package.json"
    if package_json.exists():
        print_status("Installing core dependencies...")
        try:
            run_command(["npm", "install"], cwd=core_dest)
        except subprocess.CalledProcessError:
            print_error("Failed to install core dependencies")
            return False
    
    return True

def copy_essential_files(temp_dir: Path):
    """Copy essential Python files to the temp directory."""
    print_status("Copying essential files...")
    
    # Essential files to copy
    essential_files = [
        "config_manager.py",
        "plugin_system.py", 
        "main.py",
        "launch.py",
        "requirements.txt",
        "VERSION",
        "LICENSE"
    ]
    
    for file_name in essential_files:
        src_file = Path(file_name)
        if src_file.exists():
            dest_file = temp_dir / file_name
            shutil.copy2(src_file, dest_file)
            print_status(f"Copied {file_name}")
        else:
            print_warning(f"File {file_name} not found, skipping")
    
    # Copy directories
    essential_dirs = ["plugins", "webui"]
    for dir_name in essential_dirs:
        src_dir = Path(dir_name)
        if src_dir.exists():
            dest_dir = temp_dir / dir_name
            if dest_dir.exists():
                shutil.rmtree(dest_dir)
            shutil.copytree(src_dir, dest_dir)
            print_status(f"Copied {dir_name}/")
        else:
            print_warning(f"Directory {dir_name} not found, skipping")

def create_launcher_script(temp_dir: Path):
    """Create a simplified launcher script for the standalone build."""
    launcher_content = '''#!/usr/bin/env python3
"""
IdleonWeb Standalone Launcher
This is the entry point for the standalone IdleonWeb application.
"""

import sys
import os
from pathlib import Path

# Add the application directory to the path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

# Set up environment
os.environ["IDLEONWEB_STANDALONE"] = "1"

# Import and run the main application
try:
    from main import main
    if __name__ == "__main__":
        main()
except ImportError as e:
    print(f"Error importing main module: {e}")
    print("Please ensure all required files are present.")
    sys.exit(1)
except Exception as e:
    print(f"Error starting IdleonWeb: {e}")
    sys.exit(1)
'''
    
    launcher_path = temp_dir / "idleonweb_launcher.py"
    with open(launcher_path, "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    print_status("Created launcher script")
    return launcher_path

def get_pyinstaller_args(platform: str, temp_dir: Path, launcher_script: Path, output_dir: Path) -> List[str]:
    """Get PyInstaller arguments for the specified platform."""
    
    # Get PyInstaller path from virtual environment
    python_path = Path(sys.executable)
    venv_bin = python_path.parent
    pyinstaller_path = venv_bin / "pyinstaller"
    if not pyinstaller_path.exists():
        pyinstaller_path = "pyinstaller"  # Fallback to PATH
    
    args = [
        str(pyinstaller_path),
        "--onefile",  # Create a single executable file
        "--clean",    # Clean cache and remove temporary files
        "--noconfirm", # Replace output directory without asking
        f"--distpath={output_dir}",
        f"--workpath={temp_dir / 'work'}",
        f"--specpath={temp_dir}",
        f"--name=IdleonWeb",
    ]
    
    # Add icon if available
    icon_files = ["icon.ico", "icon.png", "icon.icns"]
    for icon_file in icon_files:
        if Path(icon_file).exists():
            args.extend(["--icon", icon_file])
            break
    
    # Add hidden imports
    for module in BUILD_CONFIG["hidden_imports"]:
        args.extend(["--hidden-import", module])
    
    # Exclude unnecessary modules to reduce size
    for module in BUILD_CONFIG["exclude_modules"]:
        args.extend(["--exclude-module", module])
    
    # Add data directories with correct separator
    separator = ":" if platform in ["linux", "macos"] else ";"
    
    core_dir = temp_dir / "core"
    if core_dir.exists():
        args.append(f"--add-data={core_dir.absolute()}{separator}core")
    
    plugins_dir = temp_dir / "plugins"
    if plugins_dir.exists():
        args.append(f"--add-data={plugins_dir.absolute()}{separator}plugins")
    
    webui_dir = temp_dir / "webui"
    if webui_dir.exists():
        args.append(f"--add-data={webui_dir.absolute()}{separator}webui")
    
    # Add the launcher script
    args.append(str(launcher_script.absolute()))
    
    return args

def build_platform(platform: str, build_dir: Path):
    """Build for a specific platform."""
    print_status(f"Building for {platform}...")
    
    # Prepare build environment
    temp_dir = prepare_build_environment(build_dir)
    
    # Bundle core files
    if not bundle_core_files(temp_dir):
        return False
    
    # Copy essential files
    copy_essential_files(temp_dir)
    
    # Create launcher script
    launcher_script = create_launcher_script(temp_dir)
    
    # Debug: Check if launcher script exists
    if launcher_script.exists():
        print_status(f"Launcher script created at: {launcher_script}")
    else:
        print_error(f"Launcher script not found at: {launcher_script}")
        return False
    
    # Create output directory
    output_dir = build_dir / "dist" / platform
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get PyInstaller arguments
    pyinstaller_args = get_pyinstaller_args(platform, temp_dir, launcher_script, output_dir)
    
    # Run PyInstaller
    try:
        run_command(pyinstaller_args, cwd=Path.cwd())  # Run from project root
        print_success(f"Build completed for {platform}")
        return True
    except subprocess.CalledProcessError:
        print_error(f"Build failed for {platform}")
        return False

def cleanup_build_files(build_dir: Path, keep_dist: bool = True):
    """Clean up temporary build files."""
    print_status("Cleaning temporary build files...")
    
    temp_dir = build_dir / "temp"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    
    if not keep_dist:
        dist_dir = build_dir / "dist"
        if dist_dir.exists():
            shutil.rmtree(dist_dir)
    
    print_success("Cleanup completed")

def main():
    """Main build function."""
    parser = argparse.ArgumentParser(description="Build IdleonWeb standalone executables")
    parser.add_argument("--platform", choices=["all", "windows", "linux", "macos"], 
                       default="all", help="Target platform(s) to build for")
    parser.add_argument("--output", default="build", 
                       help="Output directory for build artifacts")
    parser.add_argument("--clean", action="store_true", 
                       help="Clean build directory before building")
    parser.add_argument("--optimize", action="store_true", 
                       help="Optimize build for size (experimental)")
    
    args = parser.parse_args()
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    build_dir = Path(args.output)
    
    # Clean build directory if requested
    if args.clean and build_dir.exists():
        shutil.rmtree(build_dir)
    
    # Determine platforms to build
    if args.platform == "all":
        platforms = ["windows", "linux", "macos"]
    else:
        platforms = [args.platform]
    
    print("=" * 50)
    print(f"Building for {args.platform.upper()}")
    print("=" * 50)
    
    successful_builds = 0
    failed_builds = []
    
    for platform in platforms:
        print_status(f"Building for {platform}...")
        try:
            if build_platform(platform, build_dir):
                successful_builds += 1
            else:
                failed_builds.append(platform)
                print_error(f"Failed to build for {platform}")
        except Exception as e:
            print_error(f"Unexpected error building for {platform}: {e}")
            failed_builds.append(platform)
    
    # Cleanup temporary files
    cleanup_build_files(build_dir, keep_dist=True)
    
    # Print summary
    print("=" * 50)
    print("BUILD SUMMARY")
    print("=" * 50)
    print(f"Successfully built: {successful_builds}/{len(platforms)} platforms")
    
    if failed_builds:
        print_error(f"Failed builds: {', '.join(failed_builds)}")
        return 1
    else:
        print_success("All builds completed successfully!")
        return 0

if __name__ == "__main__":
    sys.exit(main())
