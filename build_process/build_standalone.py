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

# Project metadata
PROJECT_NAME = "IdleonWeb"
PROJECT_DESCRIPTION = "A modern, user-friendly launcher and plugin system for enhancing Legends of Idleon"
PROJECT_URL = "https://github.com/xi-ve/IdleonWeb"
PROJECT_AUTHOR = "xi-ve"
PROJECT_COPYRIGHT = "Copyright (C) 2025 xi-ve"

def get_project_version() -> str:
    """Get version from VERSION file"""
    version_file = Path("VERSION")
    if version_file.exists():
        try:
            version = version_file.read_text().strip()
            print_debug(f"Found version: {version}")
            return version
        except Exception as e:
            print_warning(f"Failed to read VERSION file: {e}")
    return "0.0.1"

BUILD_CONFIG = {
    "hidden_imports": [
        "aiohttp", "aiohttp_jinja2", "jinja2", "rich", "prompt_toolkit", "pychrome",
        "customtkinter", "darkdetect", "gui_main",
        "pathlib", "json", "asyncio", "logging", "importlib", "inspect"
    ],
    "exclude_modules": [
        "matplotlib", "numpy", "scipy", "pandas", "PIL",
        "PyQt5", "PyQt6", "PySide2", "PySide6", "jupyter", "IPython", "notebook"
    ]
}

PLATFORM_COMPATIBILITY = {
    "linux": ["linux"],
    "windows": ["windows", "win32"],
    "darwin": ["macos", "darwin"],
}

def print_status(message: str):
    print(f"[BUILD] {message}")
    sys.stdout.flush()

def print_success(message: str):
    print(f"[SUCCESS] {message}")
    sys.stdout.flush()

def print_error(message: str):
    print(f"[ERROR] {message}")
    sys.stderr.flush()

def print_warning(message: str):
    print(f"[WARNING] {message}")
    sys.stdout.flush()

def print_debug(message: str):
    print(f"[DEBUG] {message}")
    sys.stdout.flush()

def check_platform_compatibility(target_platform: str) -> bool:
    current_platform = platform.system().lower()
    
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
        
        ci_environment = os.environ.get('CI') or os.environ.get('GITHUB_ACTIONS') or os.environ.get('JENKINS_URL')
        
        if ci_environment:
            print_status("CI environment detected - skipping cross-compilation")
            print_status("Cross-platform builds should use native runners for each platform")
            return False
        
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
    print_status("Checking build dependencies...")
    print_debug("Starting dependency check...")
    
    try:
        import PyInstaller
        print_success(f"PyInstaller {PyInstaller.__version__} found")
        print_debug(f"PyInstaller path: {PyInstaller.__file__}")
    except ImportError as e:
        print_error("PyInstaller not found. Install with: pip install pyinstaller")
        print_debug(f"PyInstaller import error: {e}")
        return False
    
    # Check Node.js requirements
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, check=True)
        node_version = result.stdout.strip()
        print_success(f"Node.js {node_version} found")
        
        # Check if version is compatible (should be v20+)
        version_number = node_version.replace('v', '').split('.')[0]
        if int(version_number) >= 20:
            print_success("Node.js version is compatible (v20+)")
        else:
            print_warning(f"Node.js version {node_version} may not be compatible. Recommended: v20+")
            
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_error("Node.js not found!")
        print_status("Installation instructions:")
        
        current_platform = platform.system().lower()
        if current_platform == 'linux':
            print_status("For Arch Linux:")
            print_status("  # Install nvm (Node Version Manager)")
            print_status("  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash")
            print_status("  source ~/.bashrc")
            print_status("  nvm install 20")
            print_status("  nvm use 20")
            print_status("  nvm alias default 20")
            print_status("")
            print_status("For other Linux distributions:")
            print_status("  # Install Node.js v20 specifically")
            print_status("  curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -")
            print_status("  sudo apt-get install -y nodejs")
            print_status("")
            print_status("For macOS:")
            print_status("  brew install node@20")
            print_status("")
            print_status("For Windows:")
            print_status("  Download Node.js v20 from https://nodejs.org/")
        return False
    
    npm_command = "npm.cmd" if platform.system().lower() == "windows" else "npm"
    try:
        result = subprocess.run([npm_command, "--version"], capture_output=True, text=True, check=True)
        print_success(f"npm {result.stdout.strip()} found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_error(f"{npm_command} not found. Please install npm")
        return False
    
    return True

def run_command(command: List[str], cwd: Path = None, check: bool = True) -> subprocess.CompletedProcess:
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
            return subprocess.CompletedProcess(command, e.returncode, e.stdout, e.stderr)
        raise

def prepare_build_environment(build_dir: Path) -> Path:
    print_status("Preparing build environment...")
    temp_dir = build_dir / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    return temp_dir

def bundle_core_files(temp_dir: Path) -> bool:
    print_status("Bundling core files...")
    
    core_src = Path("core")
    core_dest = temp_dir / "core"
    
    if not core_src.exists():
        print_warning("Core directory not found, skipping core bundling")
        return True
    
    if core_dest.exists():
        shutil.rmtree(core_dest)
    
    print_status("Copying core files...")
    shutil.copytree(core_src, core_dest, ignore=shutil.ignore_patterns('*.log', '.npm', '__pycache__', 'node_modules'))
    
    # Install Node.js dependencies
    print_status("Installing Node.js dependencies...")
    try:
        # Get current Node.js version for logging
        node_version_result = subprocess.run(["node", "--version"], capture_output=True, text=True, check=True)
        node_version = node_version_result.stdout.strip()
        print_status(f"Using Node.js {node_version} for dependency installation")
        
        # Install dependencies in the bundled core directory
        npm_command = "npm.cmd" if platform.system().lower() == "windows" else "npm"
        install_result = subprocess.run([npm_command, "install"], cwd=core_dest, check=True, 
                                       capture_output=True, text=True)
        print_success("Node.js dependencies installed successfully")
        
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install Node.js dependencies: {e}")
        print_error(f"stdout: {e.stdout}")
        print_error(f"stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        print_error("npm not found. Please ensure Node.js and npm are installed.")
        return False
    
    print_status("Core files bundled with Node.js dependencies")
    
    return True

def copy_essential_files(temp_dir: Path):
    print_status("Copying essential files...")
    essential_files = [
        "config_manager.py",
        "plugin_system.py", 
        "main.py",
        "gui_main.py",
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
    print_status("Copying standalone config...")
    core_config = Path("core/conf.json")
    root_config = Path("conf.json")
    
    config_source = None
    if core_config.exists():
        config_source = core_config
        print_status(f"Using core config: {core_config}")
    elif root_config.exists():
        config_source = root_config
        print_status(f"Using root config: {root_config}")
    
    if config_source:
        output_config = output_dir / "conf.json"
        shutil.copy2(config_source, output_config)
        print_status(f"Copied config from {config_source} to {output_config}")
    else:
        print_warning("No config file found, creating default config")
        default_config = {
            "openDevTools": False,
            "debugMode": False,
            "chromePath": "",
            "webui": {
                "darkmode": False,
                "autoOpenOnInject": True,
                "url": "http://localhost:8080",
                "port": 8080
            },
            "browser": {
                "path": "",
                "name": "auto"
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

def create_version_file(temp_dir: Path, version: str, root_fallback: bool = False) -> Path:
    """Create version info file for Windows builds"""
    version_info_content = f'''# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0. Must be set as tuple, not list
    filevers=({version.replace('.', ',')},0),
    prodvers=({version.replace('.', ',')},0),
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x4,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'{PROJECT_AUTHOR}'),
        StringStruct(u'FileDescription', u'{PROJECT_DESCRIPTION}'),
        StringStruct(u'FileVersion', u'{version}'),
        StringStruct(u'InternalName', u'{PROJECT_NAME}'),
        StringStruct(u'LegalCopyright', u'{PROJECT_COPYRIGHT}'),
        StringStruct(u'OriginalFilename', u'{PROJECT_NAME}.exe'),
        StringStruct(u'ProductName', u'{PROJECT_NAME}'),
        StringStruct(u'ProductVersion', u'{version}'),
        StringStruct(u'Comments', u'Visit {PROJECT_URL} for more information')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    # Create version file in root directory to avoid PyInstaller path resolution issues
    if root_fallback:
        version_file = Path.cwd() / f"version_info_{version.replace('.', '_')}.txt"
    else:
        version_file = temp_dir / "version_info.txt"
        
    print_debug(f"Creating version file at: {version_file.absolute()}")
    
    with open(version_file, "w", encoding="utf-8") as f:
        f.write(version_info_content)
    
    print_status(f"Created version info file: {version_file}")
    return version_file

def create_launcher_script(temp_dir: Path):
    launcher_content = '''#!/usr/bin/env python3
import sys
import os
import json
import shutil
import subprocess
import shlex
import time
from pathlib import Path

enable_logging = False
try:
    conf_path_for_logging = Path(sys.executable).parent / 'conf.json'
    if conf_path_for_logging.exists():
        with open(conf_path_for_logging, 'r', encoding='utf-8') as _f:
            _conf_log = json.load(_f)
            enable_logging = bool(_conf_log.get('debug', False))
except Exception:
    pass
if os.environ.get('IDLEONWEB_DEBUG') == '1':
    enable_logging = True

log_path = Path(sys.executable).parent / 'idleonweb-launch.log'
def log(msg):
    if not enable_logging:
        return
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            ts = time.strftime('%Y-%m-%d %H:%M:%S')
            f.write('[' + ts + '] ' + str(msg) + os.linesep)
    except Exception:
        pass

def relaunch_in_terminal():
    log('relaunch_check_start')
    if not sys.platform.startswith('linux'):
        log('not_linux')
        return False
    if os.environ.get('IDLEONWEB_TERMINAL_WRAPPED') == '1':
        log('already_wrapped')
        return False
    try:
        stdout_tty = False
        stdin_tty = False
        try:
            stdout_tty = sys.stdout.isatty()
        except Exception:
            stdout_tty = False
        try:
            stdin_tty = sys.stdin.isatty()
        except Exception:
            stdin_tty = False
        log(f'stdout_tty={stdout_tty} stdin_tty={stdin_tty}')
        if stdout_tty or stdin_tty:
            log('tty_present_no_relaunch')
            return False
    except Exception:
        log('isatty_exception')
    exe = sys.executable or sys.argv[0]
    args = [exe] + sys.argv[1:]
    log(f'exec_path={exe} argv={sys.argv}')
    env = dict(os.environ)
    env['IDLEONWEB_TERMINAL_WRAPPED'] = '1'
    env['IDLEONWEB_FORCE_INTERACTIVE'] = '1'
    def exists(cmd):
        return shutil.which(cmd) is not None
    cmd_str = ' '.join(shlex.quote(a) for a in args)
    def build_cmd(name):
        if name == 'x-terminal-emulator':
            return ['x-terminal-emulator', '-e', 'bash', '-lc', cmd_str]
        if name == 'kgx':
            return ['kgx', '--', 'bash', '-lc', cmd_str]
        if name == 'gnome-terminal':
            return ['gnome-terminal', '--wait', '--', 'bash', '-lc', cmd_str]
        if name == 'konsole':
            return ['konsole', '--hold', '-e', 'bash', '-lc', cmd_str]
        if name == 'xfce4-terminal':
            return ['xfce4-terminal', '-e', 'bash', '-lc', cmd_str]
        if name == 'mate-terminal':
            return ['mate-terminal', '-e', 'bash', '-lc', cmd_str]
        if name == 'lxterminal':
            return ['lxterminal', '-e', 'bash', '-lc', cmd_str]
        if name == 'tilix':
            return ['tilix', '-e', 'bash', '-lc', cmd_str]
        if name == 'alacritty':
            return ['alacritty', '-e', exe] + sys.argv[1:]
        if name == 'kitty':
            return ['kitty', '-e', 'bash', '-lc', cmd_str]
        if name == 'terminator':
            return ['terminator', '-x', 'bash', '-lc', cmd_str]
        if name == 'xterm':
            return ['xterm', '-hold', '-e', 'bash', '-lc', cmd_str]
        if name == 'urxvt':
            return ['urxvt', '-e', 'bash', '-lc', cmd_str]
        return None
    preferred = 'auto'
    try:
        conf = {}
        conf_path = Path(sys.executable).parent / 'conf.json'
        if conf_path.exists():
            with open(conf_path, 'r', encoding='utf-8') as f:
                conf = json.load(f)
        if isinstance(conf, dict):
            if isinstance(conf.get('console'), dict):
                preferred = str(conf['console'].get('terminal', 'auto')).strip()
            elif 'terminal' in conf:
                preferred = str(conf.get('terminal', 'auto')).strip()
    except Exception as e:
        log(f'conf_read_error={e!r}')
    candidates = []
    known = ['kitty','alacritty','gnome-terminal','konsole','x-terminal-emulator','kgx','xfce4-terminal','terminator','tilix','xterm','urxvt','mate-terminal','lxterminal']
    if preferred and preferred != 'auto' and preferred in known and exists(preferred):
        c = build_cmd(preferred)
        if c:
            candidates.append(c)
    for name in known:
        if preferred and preferred != 'auto' and name == preferred:
            continue
        if exists(name):
            c = build_cmd(name)
            if c:
                candidates.append(c)
    log(f'terminal_candidates={len(candidates)}')
    for cmd in candidates:
        try:
            log(f'spawn_attempt={cmd}')
            proc = subprocess.Popen(cmd, env=env)
            log('spawn_success_waiting')
            rc = proc.wait()
            log(f'spawn_terminal_exit_code={rc}')
            return True
        except Exception as e:
            log(f'spawn_error={e!r}')
            continue
    log('spawn_all_failed')
    return False

if relaunch_in_terminal():
    log('relaunch_triggered_parent_exit')
    sys.exit(0)

app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))
os.environ['IDLEONWEB_STANDALONE'] = '1'
try:
    log('import_main_start')
    from main import main
    if __name__ == '__main__':
        log('main_call')
        main()
        log('main_return')
except ImportError as e:
    log(f'import_error={e!r}')
    print(f"Error importing main module: {e}")
    print('Please ensure all required files are present.')
    sys.exit(1)
except Exception as e:
    log(f'main_error={e!r}')
    print(f"Error starting IdleonWeb: {e}")
    sys.exit(1)
'''
    
    launcher_path = temp_dir / "idleonweb_launcher.py"
    with open(launcher_path, "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    print_status("Created launcher script")
    return launcher_path

def get_pyinstaller_args(platform: str, temp_dir: Path, launcher_script: Path, output_dir: Path, version: str, macos_arch: str | None = None) -> List[str]:
    python_path = Path(sys.executable)
    venv_bin = python_path.parent
    pyinstaller_path = venv_bin / "pyinstaller"
    if not pyinstaller_path.exists():
        pyinstaller_path = "pyinstaller"
    
    args = [
        str(pyinstaller_path),
        "--onefile",
        "--clean",
        "--noconfirm",
        f"--distpath={output_dir}",
        f"--workpath={temp_dir / 'work'}",
        f"--specpath={temp_dir}",
        f"--name={PROJECT_NAME}",
        "--noupx",
    ]
    
    if platform == "linux":
        args.extend([
            "--strip",
            "--exclude-module=matplotlib",
            "--exclude-module=PIL",
        ])
    elif platform == "windows":
         # Create version info file for Windows - use absolute path to avoid PyInstaller path resolution issues
        version_file = create_version_file(temp_dir, version, root_fallback=True)
        version_file_abs = str(version_file.absolute())
        print_debug(f"Version file absolute: {version_file.absolute()}")
        print_debug(f"Version file path for PyInstaller: {version_file_abs}")
        print_debug(f"Current working directory: {Path.cwd()}")
        args.extend([
            f"--version-file={version_file_abs}",  # Use absolute path to avoid specpath resolution
            "--exclude-module=matplotlib",
            "--exclude-module=PIL",
        ])
    elif platform == "macos":
        if macos_arch and macos_arch != "auto":
            args.extend(["--target-arch", macos_arch])
        # Add macOS specific info
        args.extend([
            f"--osx-bundle-identifier=com.{PROJECT_AUTHOR.lower()}.{PROJECT_NAME.lower()}",
            "--exclude-module=matplotlib",
            "--exclude-module=PIL",
        ])
    
    # Use platform-specific icon, fallback to icon.ico
    icon_file = None
    icon_path = None
    if platform == "windows":
        if Path("icon.ico").exists():
            icon_file = "icon.ico"
            icon_path = Path("icon.ico").absolute()
    elif platform == "macos":
        if Path("icon.icns").exists():
            icon_file = "icon.icns"
            icon_path = Path("icon.icns").absolute()
        elif Path("icon.ico").exists():
            icon_file = "icon.ico"
            icon_path = Path("icon.ico").absolute()
    elif platform == "linux":
        if Path("icon.png").exists():
            icon_file = "icon.png"
            icon_path = Path("icon.png").absolute()
        elif Path("icon.ico").exists():
            icon_file = "icon.ico"
            icon_path = Path("icon.ico").absolute()
    
    if icon_file and icon_path:
        args.extend(["--icon", str(icon_path)])
        print_debug(f"Using icon: {icon_file}")
        print_debug(f"Icon absolute path: {icon_path}")
    else:
        print_warning("No icon file found")
    
    for module in BUILD_CONFIG["hidden_imports"]:
        args.extend(["--hidden-import", module])
    
    for module in BUILD_CONFIG["exclude_modules"]:
        args.extend(["--exclude-module", module])
    
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
    
    args.append(str(launcher_script.absolute()))
    
    return args

def build_platform(target_platform: str, build_dir: Path, macos_arch: str = "auto"):
    print_status(f"Building for {target_platform}...")
    print_debug(f"Target platform: {target_platform}, Build dir: {build_dir}, macOS arch: {macos_arch}")
    
    print_debug("Checking platform compatibility...")
    if not check_platform_compatibility(target_platform):
        print_error("Platform compatibility check failed")
        return False
        
    print_debug("Preparing build environment...")
    temp_dir = prepare_build_environment(build_dir)
    print_debug(f"Temp directory: {temp_dir}")
    
    print_debug("Bundling core files...")
    if not bundle_core_files(temp_dir):
        print_error("Core file bundling failed")
        return False
        
    print_debug("Copying essential files...")
    copy_essential_files(temp_dir)
    
    print_debug("Creating launcher script...")
    launcher_script = create_launcher_script(temp_dir)
    if launcher_script.exists():
        print_status(f"Launcher script created at: {launcher_script}")
        print_debug(f"Launcher script size: {launcher_script.stat().st_size} bytes")
    else:
        print_error(f"Launcher script not found at: {launcher_script}")
        return False
        
    output_dir = build_dir / "dist" / target_platform
    print_debug(f"Output directory: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    mac_arch = macos_arch if target_platform == "macos" else None
    version = get_project_version()
    print_debug(f"Using project version: {version}")
    print_debug("Getting PyInstaller arguments...")
    pyinstaller_args = get_pyinstaller_args(target_platform, temp_dir, launcher_script, output_dir, version, mac_arch)
    print_debug(f"PyInstaller command: {' '.join(pyinstaller_args)}")
    
    try:
        print_debug("Running PyInstaller...")
        run_command(pyinstaller_args, cwd=Path.cwd())
        
        print_debug("Copying config to output...")
        copy_config_to_output(output_dir)
        print_success(f"Build completed for {target_platform}")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Build failed for {target_platform}: {e}")
        return False
    except Exception as e:
        print_error(f"Unexpected error during build for {target_platform}: {e}")
        return False

def cleanup_build_files(build_dir: Path, keep_dist: bool = True):
    print_status("Cleaning temporary build files...")
    
    temp_dir = build_dir / "temp"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    
    # Clean up temporary version files from root directory
    for version_file in Path.cwd().glob("version_info_*.txt"):
        try:
            version_file.unlink()
            print_debug(f"Cleaned up version file: {version_file}")
        except Exception as e:
            print_warning(f"Could not remove version file {version_file}: {e}")
    
    if not keep_dist:
        dist_dir = build_dir / "dist"
        if dist_dir.exists():
            shutil.rmtree(dist_dir)
    
    print_success("Cleanup completed")

def main():
    print_debug("Starting IdleonWeb build process...")
    print_debug(f"Python version: {sys.version}")
    print_debug(f"Working directory: {Path.cwd()}")
    print_debug(f"Command line args: {sys.argv}")
    
    parser = argparse.ArgumentParser(description="Build IdleonWeb standalone executables")
    parser.add_argument("--platform", choices=["all", "windows", "linux", "macos"], 
                       default="all", help="Target platform(s) to build for")
    parser.add_argument("--macos-arch", choices=["auto", "x86_64", "arm64", "universal2"], default="auto", help="macOS target architecture")
    parser.add_argument("--output", default="build", 
                       help="Output directory for build artifacts")
    parser.add_argument("--clean", action="store_true", 
                       help="Clean build directory before building")
    parser.add_argument("--optimize", action="store_true", 
                       help="Optimize build for size (experimental)")
    
    print_debug("Parsing command line arguments...")
    try:
        args = parser.parse_args()
        print_debug(f"Parsed arguments: {args}")
    except Exception as e:
        print_error(f"Failed to parse arguments: {e}")
        return 1
    
    print_debug("Checking build dependencies...")
    if not check_dependencies():
        print_error("Dependency check failed")
        return 1
    
    build_dir = Path(args.output)
    print_debug(f"Build directory: {build_dir.absolute()}")
    
    if args.clean and build_dir.exists():
        print_debug("Cleaning existing build directory...")
        shutil.rmtree(build_dir)
        
    if args.platform == "all":
        platforms = ["windows", "linux", "macos"]
    else:
        platforms = [args.platform]
    
    print_debug(f"Target platforms: {platforms}")
    
    print("=" * 50)
    print(f"Building for {args.platform.upper()}")
    print("=" * 50)
    
    successful_builds = 0
    failed_builds = []
    
    for target_platform in platforms:
        print_status(f"Building for {target_platform}...")
        print_debug(f"Starting build process for {target_platform}")
        try:
            mac_arch = args.macos_arch if target_platform == "macos" else "auto"
            print_debug(f"Using macOS arch: {mac_arch}")
            if build_platform(target_platform, build_dir, mac_arch):
                successful_builds += 1
                print_debug(f"Successfully built for {target_platform}")
            else:
                failed_builds.append(target_platform)
                print_error(f"Failed to build for {target_platform}")
        except Exception as e:
            print_error(f"Unexpected error building for {target_platform}: {e}")
            print_debug(f"Exception details: {type(e).__name__}: {str(e)}")
            import traceback
            print_debug(f"Traceback: {traceback.format_exc()}")
            failed_builds.append(target_platform)
    
    cleanup_build_files(build_dir, keep_dist=True)
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
    try:
        print_debug("Script started from command line")
        sys.exit(main())
    except Exception as e:
        print_error(f"Critical error in main: {e}")
        import traceback
        print_debug(f"Full traceback: {traceback.format_exc()}")
        sys.exit(1)
