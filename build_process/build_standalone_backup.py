#!/usr/bin/env python3
"""
IdleonWeb Standalone Build Script
=================================

This script builds standalone executables for IdleonWeb that can be distributed
to end users without requiring Python, Node.js, or any dependencies.

Supports:
- Windows (.exe)
- Linux (AppImage and binary)
- macOS (.app     # Add data    # Add data files
    core_dir = temp_dir / "core"
    if core_dir.exists():
        separator = ":" if platform in ["linux", "macos"] else ";"
        args.append(f"--add-data={core_dir.absolute()}{separator}core")
    
    plugins_dir = temp_dir / "plugins"
    if plugins_dir.exists():
        separator = ":" if platform in ["linux", "macos"] else ";"
        args.append(f"--add-data={plugins_dir.absolute()}{separator}plugins")
    
    webui_dir = temp_dir / "webui"
    if webui_dir.exists():
        separator = ":" if platform in ["linux", "macos"] else ";"
        args.append(f"--add-data={webui_dir.absolute()}{separator}webui")
    
    # Add the launcher script
    args.append(str(launcher_script.absolute()))ore_dir = temp_dir / "core"
    if core_dir.exists():
        separator = ":" if platform in ["linux", "macos"] else ";"
        args.append(f"--add-data={core_dir.absolute()}{separator}core")
    
    plugins_dir = temp_dir / "plugins"
    if plugins_dir.exists():
        separator = ":" if platform in ["linux", "macos"] else ";"
        args.append(f"--add-data={plugins_dir.absolute()}{separator}plugins")
    
    webui_dir = temp_dir / "webui"
    if webui_dir.exists():
        separator = ":" if platform in ["linux", "macos"] else ";"
        args.append(f"--add-data={webui_dir.absolute()}{separator}webui")inary)

Requirements:
- PyInstaller
- Node.js (for bundling core files)

Usage:
    python build_standalone.py --platform windows
    python build_standalone.py --platform linux
    python build_standalone.py --platform macos
    python build_standalone.py --platform all
"""

import os
import sys
import platform
import subprocess
import shutil
import argparse
import json
import tempfile
from pathlib import Path
from typing import List, Dict, Any

# Build configuration
BUILD_CONFIG = {
    "app_name": "IdleonWeb",
    "version": "1.0.0",
    "description": "Legends of Idleon Plugin Launcher",
    "author": "IdleonWeb Team",
    "url": "https://github.com/xi-ve/IdleonWeb",
    "icon": None,  # Will be set if icon file exists
    "exclude_modules": [
        "tkinter",
        "matplotlib",
        "numpy",
        "scipy",
        "pandas",
        "PIL",
        "PyQt5",
        "PyQt6",
        "PySide2",
        "PySide6",
        "jupyter",
        "IPython",
        "notebook",
    ],
    "hidden_imports": [
        "aiohttp",
        "aiohttp_jinja2",
        "jinja2",
        "rich",
        "prompt_toolkit",
        "pychrome",
        "pathlib",
        "json",
        "asyncio",
        "logging",
        "importlib",
        "inspect",
    ]
}

def print_status(message: str):
    print(f"[BUILD] {message}")

def print_success(message: str):
    print(f"[SUCCESS] {message}")

def print_error(message: str):
    print(f"[ERROR] {message}")

def print_warning(message: str):
    print(f"[WARNING] {message}")

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
        raise

def get_current_platform() -> str:
    """Get the current platform name."""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "darwin":
        return "macos"
    elif system == "linux":
        return "linux"
    else:
        raise ValueError(f"Unsupported platform: {system}")

def check_dependencies():
    """Check if required build dependencies are installed."""
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
        result = run_command(["node", "--version"], check=False)
        if result.returncode == 0:
            print_success(f"Node.js {result.stdout.strip()} found")
        else:
            print_error("Node.js not found. Please install Node.js")
            return False
    except FileNotFoundError:
        print_error("Node.js not found. Please install Node.js")
        return False
    
    # Check npm
    try:
        result = run_command(["npm", "--version"], check=False)
        if result.returncode == 0:
            print_success(f"npm {result.stdout.strip()} found")
        else:
            print_error("npm not found. Please install npm")
            return False
    except FileNotFoundError:
        print_error("npm not found. Please install npm")
        return False
    
    return True

def prepare_build_environment(build_dir: Path):
    """Prepare the build environment."""
    print_status("Preparing build environment...")
    
    # Create build directory
    build_dir.mkdir(parents=True, exist_ok=True)
    
    # Create temp directory for bundled files
    temp_dir = build_dir / "temp"
    temp_dir.mkdir(exist_ok=True)
    
    return temp_dir

def bundle_core_files(temp_dir: Path):
    """Bundle Node.js core files into the build."""
    print_status("Bundling core files...")
    
    core_dir = Path("core")
    if not core_dir.exists():
        print_error("Core directory not found")
        return False
    
    # Install core dependencies
    if (core_dir / "package.json").exists():
        print_status("Installing core dependencies...")
        run_command(["npm", "install"], cwd=core_dir)
    
    # Copy core files to temp directory
    core_temp = temp_dir / "core"
    if core_temp.exists():
        shutil.rmtree(core_temp)
    shutil.copytree(core_dir, core_temp)
    
    return True

def copy_essential_files(temp_dir: Path):
    """Copy essential files to the build directory."""
    print_status("Copying essential files...")
    
    essential_files = [
        "config_manager.py",
        "plugin_system.py",
        "main.py",
        "launch.py",
        "requirements.txt",
        "VERSION",
        "LICENSE",
    ]
    
    essential_dirs = [
        "plugins",
        "webui",
    ]
    
    # Copy files
    for file_name in essential_files:
        file_path = Path(file_name)
        if file_path.exists():
            shutil.copy2(file_path, temp_dir / file_name)
            print_status(f"Copied {file_name}")
        else:
            print_warning(f"File {file_name} not found, skipping")
    
    # Copy directories
    for dir_name in essential_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            dest_dir = temp_dir / dir_name
            if dest_dir.exists():
                shutil.rmtree(dest_dir)
            shutil.copytree(dir_path, dest_dir)
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
            args.extend(["--icon", str(Path(icon_file).resolve())])
            break
    
    # Hide console on Windows
    if platform == "windows":
        args.append("--noconsole")
    
    # Add hidden imports
    for module in BUILD_CONFIG["hidden_imports"]:
        args.extend(["--hidden-import", module])
    
    # Exclude modules
    for module in BUILD_CONFIG["exclude_modules"]:
        args.extend(["--exclude-module", module])
    
    # Add data files
    core_dir = temp_dir / "core"
    if core_dir.exists():
        separator = ":" if platform in ["linux", "macos"] else ";"
        args.append(f"--add-data={core_dir}{separator}core")
    
    plugins_dir = temp_dir / "plugins"
    if plugins_dir.exists():
        separator = ":" if platform in ["linux", "macos"] else ";"
        args.append(f"--add-data={plugins_dir}{separator}plugins")
    
    webui_dir = temp_dir / "webui"
    if webui_dir.exists():
        separator = ":" if platform in ["linux", "macos"] else ";"
        args.append(f"--add-data={webui_dir}{separator}webui")
    
    # Add the launcher script
    args.append(str(launcher_script))
    
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
        run_command(pyinstaller_args, cwd=Path.cwd())  # Run from project root instead of temp_dir
        print_success(f"Build completed for {platform}")
        
        # Show output files
        exe_name = "IdleonWeb.exe" if platform == "windows" else "IdleonWeb"
        exe_path = output_dir / exe_name
        
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print_success(f"Executable created: {exe_path} ({size_mb:.1f} MB)")
        
        return True
        
    except subprocess.CalledProcessError:
        print_error(f"Build failed for {platform}")
        return False

def create_appimage(build_dir: Path):
    """Create AppImage for Linux (optional)."""
    print_status("Creating AppImage for Linux...")
    
    # This would require additional tools like linuxdeploy
    # For now, we'll just note that the binary is available
    print_warning("AppImage creation not implemented yet. Use the binary directly.")

def create_macos_app(build_dir: Path):
    """Create macOS .app bundle (optional)."""
    print_status("Creating macOS .app bundle...")
    
    # The --onedir option with proper Info.plist would be needed
    print_warning("macOS .app bundle creation not implemented yet. Use the binary directly.")

def clean_build_files(build_dir: Path):
    """Clean temporary build files."""
    print_status("Cleaning temporary build files...")
    
    temp_dir = build_dir / "temp"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    
    print_success("Cleanup completed")

def main():
    parser = argparse.ArgumentParser(description="Build IdleonWeb standalone executables")
    parser.add_argument(
        "--platform",
        choices=["windows", "linux", "macos", "all", "current"],
        default="current",
        help="Platform to build for (default: current platform)"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("build"),
        help="Output directory for build files (default: build/)"
    )
    parser.add_argument(
        "--no-cleanup",
        action="store_true",
        help="Don't clean temporary files after build"
    )
    parser.add_argument(
        "--version",
        help="Override version number"
    )
    
    args = parser.parse_args()
    
    # Override version if specified
    if args.version:
        BUILD_CONFIG["version"] = args.version
    
    # Check dependencies
    if not check_dependencies():
        print_error("Missing required dependencies")
        return 1
    
    # Determine platforms to build
    if args.platform == "current":
        platforms = [get_current_platform()]
    elif args.platform == "all":
        platforms = ["windows", "linux", "macos"]
    else:
        platforms = [args.platform]
    
    # Warn about cross-platform limitations
    current_platform = get_current_platform()
    for platform in platforms:
        if platform != current_platform:
            print_warning(f"Cross-platform building to {platform} from {current_platform} may not work")
            print_warning("Consider building on the target platform for best results")
    
    build_dir = args.output_dir
    build_dir.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    
    # Build for each platform
    for platform in platforms:
        print(f"\n{'='*50}")
        print(f"Building for {platform.upper()}")
        print(f"{'='*50}")
        
        try:
            if build_platform(platform, build_dir):
                success_count += 1
            else:
                print_error(f"Failed to build for {platform}")
        except Exception as e:
            print_error(f"Unexpected error building for {platform}: {e}")
    
    # Clean up
    if not args.no_cleanup:
        clean_build_files(build_dir)
    
    # Summary
    print(f"\n{'='*50}")
    print("BUILD SUMMARY")
    print(f"{'='*50}")
    print(f"Successfully built: {success_count}/{len(platforms)} platforms")
    
    if success_count > 0:
        print_success("Build completed!")
        print(f"Output directory: {build_dir / 'dist'}")
        print("\nDistribution files:")
        
        dist_dir = build_dir / "dist"
        if dist_dir.exists():
            for platform_dir in dist_dir.iterdir():
                if platform_dir.is_dir():
                    print(f"  {platform_dir.name}/")
                    for exe_file in platform_dir.iterdir():
                        if exe_file.is_file():
                            size_mb = exe_file.stat().st_size / (1024 * 1024)
                            print(f"    {exe_file.name} ({size_mb:.1f} MB)")
    else:
        print_error("All builds failed")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
