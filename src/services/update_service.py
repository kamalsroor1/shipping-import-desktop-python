"""
Auto-Update Service — Shared Hosting Integration
Checks remote JSON manifest on shared hosting, downloads updates, and restarts the application.
"""

import json
import urllib.request
import os
import sys
import subprocess
from PySide6.QtCore import QThread, Signal
from src.utils.i18n import i18n

CURRENT_VERSION = "1.0.0"
DEFAULT_UPDATE_URL = "https://shipping.baraa-solutions.com/updates/version.json"


class UpdateCheckerThread(QThread):
    update_available = Signal(dict)
    no_update = Signal()
    error_occurred = Signal(str)

    def __init__(self, update_url: str = DEFAULT_UPDATE_URL, parent=None):
        super().__init__(parent)
        self.update_url = update_url

    def run(self):
        try:
            req = urllib.request.Request(
                self.update_url,
                headers={'User-Agent': 'ImportERP-UpdateChecker/1.0'}
            )
            with urllib.request.urlopen(req, timeout=8) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    remote_ver = data.get("latest_version", "1.0.0")

                    if self._is_newer(remote_ver, CURRENT_VERSION):
                        self.update_available.emit(data)
                    else:
                        self.no_update.emit()
                else:
                    self.no_update.emit()
        except Exception as e:
            self.error_occurred.emit(str(e))

    @staticmethod
    def _is_newer(remote: str, current: str) -> bool:
        try:
            r_parts = [int(x) for x in remote.split('.')]
            c_parts = [int(x) for x in current.split('.')]
            return r_parts > c_parts
        except Exception:
            return remote > current


class UpdateDownloaderThread(QThread):
    progress = Signal(int)
    completed = Signal(str)
    failed = Signal(str)

    def __init__(self, download_url: str, save_path: str, parent=None):
        super().__init__(parent)
        self.download_url = download_url
        self.save_path = save_path

    def run(self):
        try:
            req = urllib.request.Request(
                self.download_url,
                headers={'User-Agent': 'ImportERP-Downloader/1.0'}
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                total_size = int(response.headers.get('Content-Length', 0))
                downloaded = 0
                chunk_size = 8192

                os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
                with open(self.save_path, 'wb') as f:
                    while True:
                        chunk = response.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            pct = int((downloaded / total_size) * 100)
                            self.progress.emit(pct)

            self.completed.emit(self.save_path)
        except Exception as e:
            self.failed.emit(str(e))


class AutoUpdateManager:
    @staticmethod
    def apply_update_and_restart(new_exe_path: str):
        """Creates a temporary updater.bat script to replace running binary and restart."""
        bat_content = f"""@echo off
timeout /t 2 /nobreak > NUL
taskkill /F /IM ImportManagementSystem.exe > NUL 2>&1
copy /Y "{new_exe_path}" "ImportManagementSystem.exe"
start ImportManagementSystem.exe
del "{new_exe_path}"
del "%~f0"
"""
        bat_path = os.path.join(os.getcwd(), "updater.bat")
        with open(bat_path, "w", encoding="utf-8") as f:
            f.write(bat_content)

        subprocess.Popen(["cmd.exe", "/c", bat_path], shell=True)
        sys.exit(0)
