#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / ".venv"

if os.name == "nt":
    python_path = VENV_DIR / "Scripts" / "python.exe"
else:
    python_path = VENV_DIR / "bin" / "python"

if not python_path.exists():
    sys.stderr.write(f"[Launcher] Virtual environment not found at '{python_path}'.\n")
    sys.stderr.write("Run `python setup.py` (or `python3 setup.py`) first to create it.\n")
    sys.exit(1)

main_py = ROOT / "main.py"
cmd = [str(python_path), str(main_py), *sys.argv[1:]]

try:
    subprocess.run(cmd, check=True)
except KeyboardInterrupt:
    pass
except subprocess.CalledProcessError as exc:
    sys.stderr.write(f"[Launcher] IdleonWeb exited with status {exc.returncode}.\n")
    sys.exit(exc.returncode) 