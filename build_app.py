"""
PyInstaller Build Script — Compiles the Enterprise Import System into a standalone Windows .exe with custom branding logo icon.
"""

import subprocess
import sys
import os

def build():
    print("Starting PyInstaller Build Process...")
    icon_arg = ["--icon=src/assets/app_icon.ico"] if os.path.exists("src/assets/app_icon.ico") else []
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=ImportManagementSystem",
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
    res = subprocess.run(cmd, cwd="i:/disktop")
    if res.returncode == 0:
        print("\nBUILD SUCCESSFUL!")
        print(r"The compiled executable with custom logo is located at: i:\disktop\dist\ImportManagementSystem\ImportManagementSystem.exe")
    else:
        print("\nBuild failed with return code:", res.returncode)

if __name__ == "__main__":
    build()
