"""
PyInstaller Build Script — Compiles the Enterprise Import System into a SINGLE Standalone Windows .exe (--onefile).
Works both locally and in CI/CD environments (GitHub Actions).
"""

import subprocess
import sys
import os

def build():
    print("Starting PyInstaller Single-File Build Process...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir, "src", "assets", "app_icon.ico")
    icon_arg = [f"--icon={icon_path}"] if os.path.exists(icon_path) else []
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=ImportManagementSystem",
        "--onefile",
        "--windowed",
        "--noconfirm",
        "--clean",
        "--add-data=src/assets;src/assets",
        "--add-data=src;src",
        *icon_arg,
        "--hidden-import=PySide6.QtCore",
        "--hidden-import=PySide6.QtGui",
        "--hidden-import=PySide6.QtWidgets",
        "--hidden-import=sqlalchemy",
        "--hidden-import=reportlab",
        "--hidden-import=openpyxl",
        "src/main.py"
    ]
    
    print("Executing build command:", " ".join(cmd))
    res = subprocess.run(cmd, cwd=base_dir)
    if res.returncode == 0:
        print("\nSINGLE-FILE BUILD SUCCESSFUL!")
        print(f"The standalone executable is located at: {os.path.join(base_dir, 'dist', 'ImportManagementSystem.exe')}")
    else:
        print("\nBuild failed with return code:", res.returncode)
        sys.exit(res.returncode)

if __name__ == "__main__":
    build()
