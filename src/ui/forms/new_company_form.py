"""
New / Edit Company Form Dialog (MD-001)
Allows adding and updating importer company records in the database.
"""

from datetime import date
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFormLayout, QGroupBox, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from src.database.session import SessionLocal
from src.database.repositories.master_data_repository import MasterDataRepository
from src.utils.i18n import i18n


class NewCompanyForm(QDialog):
    def __init__(self, company_id=None, parent=None):
        super().__init__(parent)
        self.company_id = company_id
        self.is_edit = bool(company_id)

        title = "تعديل شركة مستوردة" if self.is_edit else "إضافة شركة مستوردة جديدة (MD-001)"
        self.setWindowTitle(title)
        self.resize(600, 420)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft if i18n.current_lang == "ar" else Qt.LayoutDirection.LeftToRight)

        self.session = SessionLocal()
        self.repo = MasterDataRepository(self.session)
        self.company = self.session.query(self.repo.get_all_companies().__class__ if hasattr(self.repo, 'get_all_companies') else None).filter_by(company_id=company_id).first() if self.is_edit else None

        from src.database.models import Company
        self.company = self.session.query(Company).filter(Company.company_id == company_id).first() if self.is_edit else None

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        hdr_text = f"🏢  تعديل بيانات الشركة: {self.company_id}" if self.is_edit else "🏢  إضافة شركة مستوردة جديدة (MD-001)"
        hdr = QLabel(hdr_text)
        hdr.setFont(QFont("Cairo", 15, QFont.Weight.Bold))
        hdr.setStyleSheet("color: #38bdf8; border-bottom: 2px solid #0284c7; padding-bottom: 8px;")
        layout.addWidget(hdr)

        form_group = QGroupBox("بيانات الشركة والسجل التجاري والتراخيص")
        form_layout = QFormLayout(form_group)
        form_layout.setSpacing(12)

        self.txt_name = QLineEdit(self.company.egyptian_importer_name if self.company else "")
        self.txt_importer_id = QLineEdit(self.company.importer_id if self.company else "IMP-889900")
        self.txt_vat_id = QLineEdit(self.company.vat_id if self.company else "100-200-300")
        self.txt_comm_reg = QLineEdit(self.company.commercial_registration_no if self.company else "REG-776655")
        self.txt_address = QLineEdit(self.company.address if self.company else "القاهرة - مصر")
        self.txt_country = QLineEdit(self.company.country if self.company else "مصر - Egypt")

        form_layout.addRow("اسم الشركة المستوردة:", self.txt_name)
        form_layout.addRow("رقم بطاقة المتعاملين (Importer ID):", self.txt_importer_id)
        form_layout.addRow("رقم التسجيل الضريبي (VAT ID):", self.txt_vat_id)
        form_layout.addRow("رقم السجل التجاري:", self.txt_comm_reg)
        form_layout.addRow("عنوان الشركة:", self.txt_address)
        form_layout.addRow("بلد التسجيل:", self.txt_country)

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
        btn_save.clicked.connect(self._save_company)

        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_save)
        layout.addLayout(btn_row)

    def _save_company(self):
        name = self.txt_name.text().strip()
        if not name:
            QMessageBox.warning(self, "تنبيه", "يرجى إدخال اسم الشركة!")
            return

        today = date.today()

        if self.is_edit and self.company:
            self.company.egyptian_importer_name = name
            self.company.importer_id = self.txt_importer_id.text().strip()
            self.company.vat_id = self.txt_vat_id.text().strip()
            self.company.commercial_registration_no = self.txt_comm_reg.text().strip()
            self.company.address = self.txt_address.text().strip()
            self.company.country = self.txt_country.text().strip()
            self.session.commit()
            QMessageBox.information(self, "تم التحديث", f"✅ تم تحديث بيانات الشركة {self.company_id} بنجاح!")
        else:
            data = {
                "egyptian_importer_name": name,
                "importer_id": self.txt_importer_id.text().strip(),
                "importer_id_expiration_date": today,
                "vat_id": self.txt_vat_id.text().strip(),
                "vat_id_expiration_date": today,
                "commercial_registration_no": self.txt_comm_reg.text().strip(),
                "commercial_registration_expiration": today,
                "address": self.txt_address.text().strip(),
                "country": self.txt_country.text().strip()
            }
            self.repo.create_company(data)
            QMessageBox.information(self, "تم الحفظ", f"✅ تم إضافة الشركة الجديدة بنجاح!")

        self.accept()
