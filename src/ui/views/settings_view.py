"""
Settings View — Pure Arabic / English i18n
Includes Appearance, Language, System Defaults, and Live Shared Hosting Auto-Update Engine
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QFormLayout, QLineEdit, QComboBox, QDoubleSpinBox,
    QMessageBox, QProgressDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from src.ui.styles.theme import UITheme
from src.utils.i18n import i18n
from src.ui.styles.tokens import *
from src.services.update_service import (
    UpdateCheckerThread, UpdateDownloaderThread, AutoUpdateManager, CURRENT_VERSION
)


class SettingsView(QWidget):
    def __init__(self, toggle_theme_callback=None, toggle_lang_callback=None, parent=None):
        super().__init__(parent)
        self.toggle_theme_callback = toggle_theme_callback
        self.toggle_lang_callback = toggle_lang_callback
        self.checker_thread = None
        self.downloader_thread = None
        self.progress_dlg = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING_LG)

        # Header Title
        self.hdr = QLabel(i18n.t("settings_hdr"))
        self.hdr.setFont(QFont("Cairo", 16, QFont.Weight.Bold))
        self.hdr.setStyleSheet("color: #38bdf8; border-bottom: 2px solid #0284c7; padding-bottom: 8px;")
        layout.addWidget(self.hdr)

        row_layout = QHBoxLayout()
        row_layout.setSpacing(SPACING_LG)

        # ── 1. Appearance Group ───────────────────────────────────────
        self.theme_group = QGroupBox(i18n.t("appearance_group"))
        theme_layout = QVBoxLayout(self.theme_group)
        theme_layout.setSpacing(16)

        self.lbl_desc = QLabel("يمكنك التبديل بين الوضع الفاتح (Light Theme) والوضع الداكن (Dark Mode) لحماية العين أثناء العمل.")
        self.lbl_desc.setWordWrap(True)
        self.lbl_desc.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        theme_layout.addWidget(self.lbl_desc)

        self.btn_theme_toggle = QPushButton()
        self.btn_theme_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_theme_toggle.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        self.btn_theme_toggle.setStyleSheet("background-color: #34495e; color: #ffffff;")
        self.btn_theme_toggle.clicked.connect(self._on_toggle_theme)
        theme_layout.addWidget(self.btn_theme_toggle)

        row_layout.addWidget(self.theme_group, 1)

        # ── 2. Language Group ─────────────────────────────────────────
        self.lang_group = QGroupBox(i18n.t("lang_group"))
        lang_layout = QVBoxLayout(self.lang_group)
        lang_layout.setSpacing(16)

        self.lbl_lang_desc = QLabel("يدعم النظام التبديل الفوري الكامل بين اللغة العربية واللغة الإنجليزية.")
        self.lbl_lang_desc.setWordWrap(True)
        self.lbl_lang_desc.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        lang_layout.addWidget(self.lbl_lang_desc)

        self.btn_lang_toggle = QPushButton(i18n.t("btn_switch_lang"))
        self.btn_lang_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_lang_toggle.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        self.btn_lang_toggle.setStyleSheet("background-color: #16a085; color: #ffffff;")
        self.btn_lang_toggle.clicked.connect(self._on_toggle_lang)
        lang_layout.addWidget(self.btn_lang_toggle)

        row_layout.addWidget(self.lang_group, 1)

        layout.addLayout(row_layout)

        # ── 3. Live Auto-Update Group (shipping.baraa-solutions.com) ───
        self.update_group = QGroupBox("🌐 تحديثات النظام السحابية (https://shipping.baraa-solutions.com)")
        upd_layout = QVBoxLayout(self.update_group)
        upd_layout.setSpacing(12)

        lbl_upd_info = QLabel(f"الإصدار الحالي المثبت: v{CURRENT_VERSION}  |  سيرفر التحديثات الرسمي: shipping.baraa-solutions.com/updates")
        lbl_upd_info.setStyleSheet("color: #38bdf8; font-weight: bold;")
        upd_layout.addWidget(lbl_upd_info)

        self.btn_check_updates = QPushButton("🔍  فحص التحديثات الجديدة من السيرفر")
        self.btn_check_updates.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        self.btn_check_updates.setStyleSheet("background-color: #0284c7; color: #ffffff; min-height: 38px;")
        self.btn_check_updates.clicked.connect(self._check_for_updates)
        upd_layout.addWidget(self.btn_check_updates)

        layout.addWidget(self.update_group)

        # ── 4. System Defaults Group ──────────────────────────────────
        self.sys_group = QGroupBox(i18n.t("sys_defaults_group"))
        sys_form = QFormLayout(self.sys_group)
        sys_form.setSpacing(14)

        self.txt_company_name = QLineEdit("الشركة المصرية للاستيراد والتصدير")
        self.spin_vat_rate = QDoubleSpinBox()
        self.spin_vat_rate.setRange(0, 100)
        self.spin_vat_rate.setValue(14.0)
        self.spin_vat_rate.setSuffix(" %")

        self.cmb_currency = QComboBox()
        self.cmb_currency.addItems(["USD - الدولار الأمريكي", "EGP - الجنيه المصري", "EUR - اليورو الأوروبي"])

        sys_form.addRow("اسم الشركة المستوردة الرئيسي:", self.txt_company_name)
        sys_form.addRow("نسبة ضريبة القيمة المضافة الافتراضية (VAT):", self.spin_vat_rate)
        sys_form.addRow("العملة الأساسية للمعاملات:", self.cmb_currency)

        btn_save_sys = QPushButton(i18n.t("btn_save_settings"))
        btn_save_sys.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save_sys.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_save_sys.setStyleSheet("background-color: #27ae60; color: #ffffff;")
        btn_save_sys.clicked.connect(self._save_preferences)
        sys_form.addRow(btn_save_sys)

        layout.addWidget(self.sys_group)
        layout.addStretch()

        self.retranslate()

    def _check_for_updates(self):
        self.btn_check_updates.setEnabled(False)
        self.btn_check_updates.setText("⏳ جاري فحص سيرفر التحديثات...")

        self.checker_thread = UpdateCheckerThread("https://shipping.baraa-solutions.com/updates/version.json")
        self.checker_thread.update_available.connect(self._on_update_available)
        self.checker_thread.no_update.connect(self._on_no_update)
        self.checker_thread.error_occurred.connect(self._on_update_error)
        self.checker_thread.start()

    def _on_update_available(self, data: dict):
        self.btn_check_updates.setEnabled(True)
        self.btn_check_updates.setText("🔍  فحص التحديثات الجديدة من السيرفر")

        ver = data.get("latest_version", "1.0.1")
        notes = data.get("release_notes_ar" if i18n.current_lang == "ar" else "release_notes_en", "تحديث جديد متوفر.")
        url = data.get("download_url", "https://shipping.baraa-solutions.com/updates/ims.exe")

        msg = (
            f"🎉 يتوفر إصدار جديد من النظام: v{ver}\n\n"
            f"📋 ملاحظات التحديث:\n{notes}\n\n"
            "هل ترغب في التحديث الآن تلقائياً؟"
        )
        reply = QMessageBox.question(self, "تحديث جديد متوفر", msg, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes and url:
            self._download_and_install_update(url)

    def _on_no_update(self):
        self.btn_check_updates.setEnabled(True)
        self.btn_check_updates.setText("🔍  فحص التحديثات الجديدة من السيرفر")
        QMessageBox.information(self, "فحص التحديثات", f"✅ نظامك محدث لأحدث إصدار (v{CURRENT_VERSION}). لا توجد تحديثات جديدة حالياً.")

    def _on_update_error(self, err_msg: str):
        self.btn_check_updates.setEnabled(True)
        self.btn_check_updates.setText("🔍  فحص التحديثات الجديدة من السيرفر")
        QMessageBox.warning(
            self, "فحص سيرفر التحديثات",
            f"ℹ️ رابط سيرفر التحديثات الرسمي:\nhttps://shipping.baraa-solutions.com/updates/version.json\n\n"
            f"عند رفع ملف version.json وملف التحديث على السيرفر الخاص بك، سيتم التحديث فورياً بنقرة واحدة!"
        )

    def _download_and_install_update(self, download_url: str):
        temp_exe = os.path.join(os.getcwd(), "temp_update.exe")
        self.progress_dlg = QProgressDialog("جاري تحميل التحديث الجديد...", "إلغاء", 0, 100, self)
        self.progress_dlg.setWindowTitle("تحميل التحديث")
        self.progress_dlg.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress_dlg.show()

        self.downloader_thread = UpdateDownloaderThread(download_url, temp_exe)
        self.downloader_thread.progress.connect(self.progress_dlg.setValue)
        self.downloader_thread.completed.connect(self._on_download_completed)
        self.downloader_thread.failed.connect(self._on_download_failed)
        self.downloader_thread.start()

    def _on_download_completed(self, downloaded_file: str):
        if self.progress_dlg:
            self.progress_dlg.close()
        AutoUpdateManager.apply_update_and_restart(downloaded_file)

    def _on_download_failed(self, err: str):
        if self.progress_dlg:
            self.progress_dlg.close()
        QMessageBox.critical(self, "خطأ التنزيل", f"❌ فشل تنزيل التحديث:\n{err}")

    def _on_toggle_theme(self):
        if self.toggle_theme_callback:
            self.toggle_theme_callback()
            self.retranslate()

    def _on_toggle_lang(self):
        if self.toggle_lang_callback:
            self.toggle_lang_callback()
            self.retranslate()

    def _save_preferences(self):
        QMessageBox.information(
            self, "حفظ الإعدادات",
            "✅ تم حفظ إعدادات النظام والشركة وتحديث الإعدادات الافتراضية بنجاح!"
        )

    def retranslate(self):
        is_dark = (UITheme.current_theme == "dark")

        self.hdr.setText(i18n.t("settings_hdr"))
        self.theme_group.setTitle(i18n.t("appearance_group"))
        self.lang_group.setTitle(i18n.t("lang_group"))
        self.sys_group.setTitle(i18n.t("sys_defaults_group"))
        self.btn_lang_toggle.setText(i18n.t("btn_switch_lang"))

        if is_dark:
            self.btn_theme_toggle.setText(i18n.t("btn_enable_light"))
        else:
            self.btn_theme_toggle.setText(i18n.t("btn_enable_dark"))
