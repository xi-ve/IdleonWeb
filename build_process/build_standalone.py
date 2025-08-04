#!/usr/bin/env python3
"""
IdleonWeb Standalone Build Script
Builds standalone executables using PyInstaller on native platforms.

Supported platforms (native builds only):
- Windows (.exe) - build on Windows runner
- Linux (binary) - build on Linux runner  
- macOS (.app) - build on macOS runner

Note: PyInstaller cannot cross-compile between different operating systems.
Each platform must be built on its native environment for compatibility.

Requirements:
- PyInstaller
- Node.js and npm (for core file bundling)
- Python virtual environment with all dependencies

Usage:
    python build_standalone.py --platform linux --output release_linux
    python build_standalone.py --platform windows --output release_windows  
    python build_standalone.py --platform macos --output release_macos
"""

import argparse
import os
import subprocess
import sys
import shutil
import json
import platform
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

# Platform compatibility mapping
PLATFORM_COMPATIBILITY = {
    "linux": ["linux"],
    "windows": ["windows", "win32"],
    "darwin": ["macos", "darwin"],
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

def check_platform_compatibility(target_platform: str) -> bool:
    """Check if the target platform can be built on the current platform."""
    current_platform = platform.system().lower()
    
    # Normalize platform names
    platform_map = {
        "linux": "linux",
        "windows": "windows", 
        "win32": "windows",
        "darwin": "macos",
        "macos": "macos"
    }
    
    current_normalized = platform_map.get(current_platform, current_platform)
    target_normalized = platform_map.get(target_platform, target_platform)
    
    if current_normalized != target_normalized:
        print_warning(f"Cross-compilation detected: Building {target_platform} on {current_platform}")
        print_warning("PyInstaller cannot cross-compile between different operating systems.")
        print_warning("The build may fail or produce an incompatible executable.")
        print_warning("For best results, build on the target platform.")
        
        # Check if running in CI environment (GitHub Actions, etc.)
        ci_environment = os.environ.get('CI') or os.environ.get('GITHUB_ACTIONS') or os.environ.get('JENKINS_URL')
        
        if ci_environment:
            print_status("CI environment detected - skipping cross-compilation")
            print_status("Cross-platform builds should use native runners for each platform")
            return False
        
        # Ask user if they want to continue in interactive mode
        try:
            response = input("Continue anyway? (y/N): ").strip().lower()
            if response not in ['y', 'yes']:
                print_status("Build cancelled by user")
                return False
        except (EOFError, KeyboardInterrupt):
            print_status("\nBuild cancelled")
            return False
    
    return True

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
    
    # Check npm (use npm.cmd on Windows)
    npm_command = "npm.cmd" if platform.system().lower() == "windows" else "npm"
    try:
        result = subprocess.run([npm_command, "--version"], capture_output=True, text=True, check=True)
        print_success(f"npm {result.stdout.strip()} found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_error(f"{npm_command} not found. Please install npm")
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
    
    # Copy core files but exclude node_modules to prevent OpenSSL conflicts
    if core_dest.exists():
        shutil.rmtree(core_dest)
    
    # Copy core files selectively, excluding node_modules
    print_status("Copying core files (excluding node_modules)...")
    shutil.copytree(core_src, core_dest, ignore=shutil.ignore_patterns('node_modules', '*.log', '.npm'))
    
    # Note: We don't install npm dependencies in the build
    # The standalone executable will require Node.js to be installed on the target system
    print_status("Core files bundled (Node.js will be required on target system)")
    
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

def copy_config_to_output(output_dir: Path):
    """Copy the default config file to the output directory for standalone use."""
    print_status("Copying standalone config...")
    
    # Copy the core config file to the output directory
    core_config = Path("core/conf.json")
    if core_config.exists():
        output_config = output_dir / "conf.json"
        shutil.copy2(core_config, output_config)
        print_status(f"Copied config to {output_config}")
    else:
        print_warning("Core config file not found, creating default config")
        # Create a minimal default config
        default_config = {
            "openDevTools": False,
            "debugMode": False,
            "chromePath": "",
            "webui": {
                "enabled": True,
                "host": "localhost",
                "port": 8080
            },
            "injector": {
                "cdp_port": 32123,
                "njs_pattern": "*N.js",
                "idleon_url": "https://www.legendsofidleon.com/ytGl5oc/",
                "timeout": 120000,
                "autoInject": True
            }
        }
        output_config = output_dir / "conf.json"
        with open(output_config, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2)
        print_status(f"Created default config at {output_config}")

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
        "--noupx",    # Disable UPX compression (can cause issues)
    ]
    
    # Add compatibility flags for Linux builds
    if platform == "linux":
        args.extend([
            "--strip",  # Strip debug symbols to reduce size
            "--exclude-module=tkinter",  # Remove GUI modules
            "--exclude-module=matplotlib",
            "--exclude-module=PIL",
        ])
    
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

def build_platform(target_platform: str, build_dir: Path):
    """Build for a specific platform."""
    print_status(f"Building for {target_platform}...")
    
    # Check platform compatibility
    if not check_platform_compatibility(target_platform):
        return False
    
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
    output_dir = build_dir / "dist" / target_platform
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get PyInstaller arguments
    pyinstaller_args = get_pyinstaller_args(target_platform, temp_dir, launcher_script, output_dir)
    
    # Run PyInstaller
    try:
        run_command(pyinstaller_args, cwd=Path.cwd())  # Run from project root
        
        # Copy config file to output directory for standalone use
        copy_config_to_output(output_dir)
        
        print_success(f"Build completed for {target_platform}")
        return True
    except subprocess.CalledProcessError:
        print_error(f"Build failed for {target_platform}")
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
    
    for target_platform in platforms:
        print_status(f"Building for {target_platform}...")
        try:
            if build_platform(target_platform, build_dir):
                successful_builds += 1
            else:
                failed_builds.append(target_platform)
                print_error(f"Failed to build for {target_platform}")
        except Exception as e:
            print_error(f"Unexpected error building for {target_platform}: {e}")
            failed_builds.append(target_platform)
    
    # Cleanup temporary files
    cleanup_build_files(build_dir, keep_dist=True)
    
    # Print summary
    print("=" * 50)
    print("BUILD SUMMARY")
    print("=" * 50)
    print(f"Successfully built: {successful_builds}/{len(platforms)} platforms")
    
    if failed_builds:
        print_error(f"Failed builds: {', '.join(failed_builds)}")
        print("")
        print_status("For multi-platform builds, consider:")
        print_status("1. GitHub Actions with matrix builds (see integration_tests/)")
        print_status("2. Building on each target platform separately")
        print_status("3. Using containerized build environments")
        return 1
    else:
        print_success("All builds completed successfully!")
        return 0

if __name__ == "__main__":
    sys.exit(main())
