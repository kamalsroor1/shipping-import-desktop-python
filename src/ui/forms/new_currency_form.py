"""
New / Edit Currency Form Dialog (MD-006)
Allows adding and updating ISO currencies and symbols.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFormLayout, QGroupBox, QMessageBox, QSpinBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from src.database.session import SessionLocal
from src.utils.i18n import i18n
from src.database.models import Currency


class NewCurrencyForm(QDialog):
    def __init__(self, currency_id=None, parent=None):
        super().__init__(parent)
        self.currency_id = currency_id
        self.is_edit = bool(currency_id)

        title = "تعديل عملة" if self.is_edit else "إضافة عملة جديدة (MD-006)"
        self.setWindowTitle(title)
        self.resize(550, 360)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft if i18n.current_lang == "ar" else Qt.LayoutDirection.LeftToRight)

        self.session = SessionLocal()
        self.currency_obj = self.session.query(Currency).filter(Currency.currency_id == currency_id).first() if self.is_edit else None

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        hdr_text = f"💱  تعديل بيانات العملة: #{self.currency_id}" if self.is_edit else "💱  إضافة عملة جديدة (MD-006)"
        hdr = QLabel(hdr_text)
        hdr.setFont(QFont("Cairo", 15, QFont.Weight.Bold))
        hdr.setStyleSheet("color: #38bdf8; border-bottom: 2px solid #0284c7; padding-bottom: 8px;")
        layout.addWidget(hdr)

        form_group = QGroupBox("بيانات العملة والتنسيق")
        form_layout = QFormLayout(form_group)
        form_layout.setSpacing(12)

        self.txt_iso = QLineEdit(self.currency_obj.iso_code if self.currency_obj else "USD")
        self.txt_name = QLineEdit(self.currency_obj.currency_name if self.currency_obj else "US Dollar")
        self.txt_symbol = QLineEdit(self.currency_obj.symbol if self.currency_obj else "$")
        self.spin_decimals = QSpinBox()
        self.spin_decimals.setRange(0, 4)
        self.spin_decimals.setValue(self.currency_obj.decimal_places if self.currency_obj else 2)

        form_layout.addRow("كود العملة (ISO Code - 3 أحرف):", self.txt_iso)
        form_layout.addRow("اسم العملة:", self.txt_name)
        form_layout.addRow("رمز العملة (Symbol):", self.txt_symbol)
        form_layout.addRow("عدد الخانات العشرية:", self.spin_decimals)

        layout.addWidget(form_group)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        btn_cancel = QPushButton("إلغاء")
        btn_cancel.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_cancel.clicked.connect(self.reject)

        btn_save = QPushButton("💾 حفظ البيانات")
        btn_save.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_save.setStyleSheet("background-color: #27ae60; color: #ffffff; padding: 10px 24px;")
        btn_save.clicked.connect(self._save_currency)

        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_save)
        layout.addLayout(btn_row)

    def _save_currency(self):
        iso = self.txt_iso.text().strip().upper()
        if len(iso) != 3:
            QMessageBox.warning(self, "تنبيه", "يرجى إدخال كود ISO صحيح مكون من 3 أحرف بالضبط (مثل USD / EGP)!")
            return

        if self.is_edit and self.currency_obj:
            self.currency_obj.iso_code = iso
            self.currency_obj.currency_name = self.txt_name.text().strip()
            self.currency_obj.symbol = self.txt_symbol.text().strip()
            self.currency_obj.decimal_places = self.spin_decimals.value()
            self.session.commit()
            QMessageBox.information(self, "تم التحديث", f"✅ تم تحديث بيانات العملة {iso} بنجاح!")
        else:
            cur = Currency(
                iso_code=iso,
                currency_name=self.txt_name.text().strip(),
                symbol=self.txt_symbol.text().strip(),
                decimal_places=self.spin_decimals.value()
            )
            self.session.add(cur)
            self.session.commit()
            QMessageBox.information(self, "تم الحفظ", f"✅ تم إضافة العملة الجديدة ({iso}) بنجاح!")

        self.accept()
