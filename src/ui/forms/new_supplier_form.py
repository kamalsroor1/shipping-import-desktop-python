"""
New / Edit Foreign Supplier Form Dialog (MD-002)
Allows adding and updating foreign supplier profiles and bank SWIFT details.
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
from src.database.models import Supplier


class NewSupplierForm(QDialog):
    def __init__(self, supplier_id=None, parent=None):
        super().__init__(parent)
        self.supplier_id = supplier_id
        self.is_edit = bool(supplier_id)

        title = "تعديل بيانات مورد أجنبي" if self.is_edit else "إضافة مورد أجنبي جديد (MD-002)"
        self.setWindowTitle(title)
        self.resize(620, 460)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft if i18n.current_lang == "ar" else Qt.LayoutDirection.LeftToRight)

        self.session = SessionLocal()
        self.repo = MasterDataRepository(self.session)
        self.supplier = self.session.query(Supplier).filter(Supplier.supplier_id == supplier_id).first() if self.is_edit else None

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        hdr_text = f"🏭  تعديل بيانات المورد: {self.supplier_id}" if self.is_edit else "🏭  إضافة مورد أجنبي جديد (MD-002)"
        hdr = QLabel(hdr_text)
        hdr.setFont(QFont("Cairo", 15, QFont.Weight.Bold))
        hdr.setStyleSheet("color: #38bdf8; border-bottom: 2px solid #0284c7; padding-bottom: 8px;")
        layout.addWidget(hdr)

        form_group = QGroupBox("بيانات المورد وتفاصيل التصدير")
        form_layout = QFormLayout(form_group)
        form_layout.setSpacing(12)

        self.txt_name_en = QLineEdit(self.supplier.vendor_company_name if self.supplier else "")
        self.txt_exporter_id = QLineEdit(self.supplier.foreign_exporter_id if self.supplier else "EXP-998877")
        self.txt_country = QLineEdit(self.supplier.foreign_exporter_country if self.supplier else "China / الصين")
        self.txt_country_code = QLineEdit(self.supplier.foreign_exporter_country_code if self.supplier else "CN")
        self.txt_phone = QLineEdit(self.supplier.phone_number if self.supplier else "+86 21 8899 0000")
        self.txt_email = QLineEdit(self.supplier.email if self.supplier else "info@exporter.cn")

        form_layout.addRow("اسم شركة المورد بالإنجليزية:", self.txt_name_en)
        form_layout.addRow("رقم تسجيل المورد الأجنبي:", self.txt_exporter_id)
        form_layout.addRow("دولة التصدير:", self.txt_country)
        form_layout.addRow("كود الدولة (ISO):", self.txt_country_code)
        form_layout.addRow("رقم الهاتف:", self.txt_phone)
        form_layout.addRow("البريد الإلكتروني:", self.txt_email)

        layout.addWidget(form_group)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        btn_cancel = QPushButton("إلغاء")
        btn_cancel.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_cancel.clicked.connect(self.reject)

        btn_save = QPushButton("💾 حفظ البيانات")
        btn_save.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_save.setStyleSheet("background-color: #8e44ad; color: #ffffff; padding: 10px 24px;")
        btn_save.clicked.connect(self._save_supplier)

        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_save)
        layout.addLayout(btn_row)

    def _save_supplier(self):
        name_en = self.txt_name_en.text().strip()
        if not name_en:
            QMessageBox.warning(self, "تنبيه", "يرجى إدخال اسم شركة المورد!")
            return

        if self.is_edit and self.supplier:
            self.supplier.vendor_company_name = name_en
            self.supplier.foreign_exporter_id = self.txt_exporter_id.text().strip()
            self.supplier.foreign_exporter_country = self.txt_country.text().strip()
            self.supplier.foreign_exporter_country_code = self.txt_country_code.text().strip()
            self.supplier.phone_number = self.txt_phone.text().strip()
            self.supplier.email = self.txt_email.text().strip()
            self.session.commit()
            QMessageBox.information(self, "تم التحديث", f"✅ تم تحديث بيانات المورد {self.supplier_id} بنجاح!")
        else:
            data = {
                "vendor_company_name": name_en,
                "registration_type": "Company",
                "foreign_exporter_id": self.txt_exporter_id.text().strip(),
                "foreign_exporter_country": self.txt_country.text().strip(),
                "foreign_exporter_country_code": self.txt_country_code.text().strip(),
                "phone_number": self.txt_phone.text().strip(),
                "email": self.txt_email.text().strip()
            }
            self.repo.create_supplier(data)
            QMessageBox.information(self, "تم الحفظ", f"✅ تم إضافة المورد الأجنبي الجديد بنجاح!")

        self.accept()
