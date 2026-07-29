"""
New / Edit Shipping Line Form Dialog (MD-005)
Allows adding and updating ocean shipping lines and SCAC codes.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFormLayout, QGroupBox, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from src.database.session import SessionLocal
from src.database.repositories.master_data_repository import MasterDataRepository
from src.utils.i18n import i18n
from src.database.models import ShippingLine


class NewShippingLineForm(QDialog):
    def __init__(self, line_id=None, parent=None):
        super().__init__(parent)
        self.line_id = line_id
        self.is_edit = bool(line_id)

        title = "تعديل خط ملاحي" if self.is_edit else "إضافة خط ملاحي جديد (MD-005)"
        self.setWindowTitle(title)
        self.resize(550, 360)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft if i18n.current_lang == "ar" else Qt.LayoutDirection.LeftToRight)

        self.session = SessionLocal()
        self.shipping_line = self.session.query(ShippingLine).filter(ShippingLine.shipping_line_id == line_id).first() if self.is_edit else None

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        hdr_text = f"🚢  تعديل بيانات الخط الملاحي: #{self.line_id}" if self.is_edit else "🚢  إضافة خط ملاحي جديد (MD-005)"
        hdr = QLabel(hdr_text)
        hdr.setFont(QFont("Cairo", 15, QFont.Weight.Bold))
        hdr.setStyleSheet("color: #38bdf8; border-bottom: 2px solid #0284c7; padding-bottom: 8px;")
        layout.addWidget(hdr)

        form_group = QGroupBox("بيانات الخط الملاحي والتواصل")
        form_layout = QFormLayout(form_group)
        form_layout.setSpacing(12)

        self.txt_name = QLineEdit(self.shipping_line.shipping_line_name if self.shipping_line else "")
        self.txt_scac = QLineEdit(self.shipping_line.scac_code if self.shipping_line else "MAEU")
        self.txt_country = QLineEdit(self.shipping_line.country if self.shipping_line else "Denmark / الدنمارك")
        self.txt_website = QLineEdit(self.shipping_line.website if self.shipping_line else "www.maersk.com")

        form_layout.addRow("اسم الخط الملاحي:", self.txt_name)
        form_layout.addRow("كود الـ SCAC:", self.txt_scac)
        form_layout.addRow("بلد المقر الرئيسي:", self.txt_country)
        form_layout.addRow("الموقع الإلكتروني:", self.txt_website)

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
        btn_save.clicked.connect(self._save_shipping_line)

        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_save)
        layout.addLayout(btn_row)

    def _save_shipping_line(self):
        name = self.txt_name.text().strip()
        if not name:
            QMessageBox.warning(self, "تنبيه", "يرجى إدخال اسم الخط الملاحي!")
            return

        if self.is_edit and self.shipping_line:
            self.shipping_line.shipping_line_name = name
            self.shipping_line.scac_code = self.txt_scac.text().strip()
            self.shipping_line.country = self.txt_country.text().strip()
            self.shipping_line.website = self.txt_website.text().strip()
            self.session.commit()
            QMessageBox.information(self, "تم التحديث", f"✅ تم تحديث بيانات الخط الملاحي #{self.line_id} بنجاح!")
        else:
            sl = ShippingLine(
                shipping_line_name=name,
                scac_code=self.txt_scac.text().strip(),
                country=self.txt_country.text().strip(),
                website=self.txt_website.text().strip()
            )
            self.session.add(sl)
            self.session.commit()
            QMessageBox.information(self, "تم الحفظ", "✅ تم إضافة الخط الملاحي الجديد بنجاح!")

        self.accept()
