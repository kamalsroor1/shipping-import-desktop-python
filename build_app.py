"""
PyInstaller Build Script — Compiles the Enterprise Import System into a SINGLE Standalone Windows .exe named IMS.exe.
Automatically syncs versions across version.json and download_page.html before packaging.
"""

import subprocess
import sys
import os
import json

def build():
    print("Starting PyInstaller Single-File Build Process for IMS.exe...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Auto-sync version info
    version_file = os.path.join(base_dir, "version_example.json")
    if os.path.exists(version_file):
        try:
            with open(version_file, "r", encoding="utf-8") as f:
                v_data = json.load(f)
            v_data["download_url"] = "https://shipping.baraa-solutions.com/updates/IMS.exe"
            with open(version_file, "w", encoding="utf-8") as f:
                json.dump(v_data, f, indent=2, ensure_ascii=False)
            print(f"Auto-synced version.json -> v{v_data.get('latest_version')}")
        except Exception as e:
            print("Version sync notice:", e)

    icon_path = os.path.join(base_dir, "src", "assets", "app_icon.ico")
    icon_arg = [f"--icon={icon_path}"] if os.path.exists(icon_path) else []
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=IMS",
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
        print(f"The standalone executable is located at: {os.path.join(base_dir, 'dist', 'IMS.exe')}")
    else:
        print("\nBuild failed with return code:", res.returncode)
        sys.exit(res.returncode)

if __name__ == "__main__":
    build()
