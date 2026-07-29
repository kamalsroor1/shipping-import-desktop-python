"""
New / Edit Service Provider Form Dialog (MD-004)
Allows adding and updating shipping lines, customs brokers, and freight forwarders.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QFormLayout, QGroupBox, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from src.database.session import SessionLocal
from src.database.repositories.master_data_repository import MasterDataRepository
from src.utils.i18n import i18n
from src.database.models import ServiceProvider


class NewServiceProviderForm(QDialog):
    def __init__(self, provider_id=None, parent=None):
        super().__init__(parent)
        self.provider_id = provider_id
        self.is_edit = bool(provider_id)

        title = "تعديل بيانات شريك خدمة" if self.is_edit else "إضافة شريك خدمة وتخليص جديد (MD-004)"
        self.setWindowTitle(title)
        self.resize(600, 420)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft if i18n.current_lang == "ar" else Qt.LayoutDirection.LeftToRight)

        self.session = SessionLocal()
        self.repo = MasterDataRepository(self.session)
        self.provider = self.session.query(ServiceProvider).filter(ServiceProvider.partner_id == provider_id).first() if self.is_edit else None

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        hdr_text = f"🤝  تعديل بيانات شريك الخدمة: {self.provider_id}" if self.is_edit else "🤝  إضافة شريك خدمة جديد (MD-004)"
        hdr = QLabel(hdr_text)
        hdr.setFont(QFont("Cairo", 15, QFont.Weight.Bold))
        hdr.setStyleSheet("color: #38bdf8; border-bottom: 2px solid #0284c7; padding-bottom: 8px;")
        layout.addWidget(hdr)

        form_group = QGroupBox("بيانات شريك الخدمة والتواصل")
        form_layout = QFormLayout(form_group)
        form_layout.setSpacing(12)

        self.txt_name = QLineEdit(self.provider.partner_name if self.provider else "")
        self.cmb_type = QComboBox()
        self.cmb_type.addItems(["Customs Broker", "Shipping Line", "Freight Forwarder", "Transport Company"])
        if self.provider and self.provider.partner_type:
            self.cmb_type.setCurrentText(self.provider.partner_type)

        self.txt_contact = QLineEdit(self.provider.contact_person if self.provider else "")
        self.txt_phone = QLineEdit(self.provider.phone_number if self.provider else "")
        self.txt_email = QLineEdit(self.provider.email if self.provider else "")

        form_layout.addRow("اسم الشركة / الشريك:", self.txt_name)
        form_layout.addRow("نوع الخدمة:", self.cmb_type)
        form_layout.addRow("الشخص المسؤول للتواصل:", self.txt_contact)
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
        btn_save.setStyleSheet("background-color: #2980b9; color: #ffffff; padding: 10px 24px;")
        btn_save.clicked.connect(self._save_provider)

        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_save)
        layout.addLayout(btn_row)

    def _save_provider(self):
        name = self.txt_name.text().strip()
        if not name:
            QMessageBox.warning(self, "تنبيه", "يرجى إدخال اسم شريك الخدمة!")
            return

        if self.is_edit and self.provider:
            self.provider.partner_name = name
            self.provider.partner_type = self.cmb_type.currentText()
            self.provider.contact_person = self.txt_contact.text().strip()
            self.provider.phone_number = self.txt_phone.text().strip()
            self.provider.email = self.txt_email.text().strip()
            self.session.commit()
            QMessageBox.information(self, "تم التحديث", f"✅ تم تحديث بيانات الشريك {self.provider_id} بنجاح!")
        else:
            data = {
                "partner_name": name,
                "partner_type": self.cmb_type.currentText(),
                "contact_person": self.txt_contact.text().strip(),
                "phone_number": self.txt_phone.text().strip(),
                "email": self.txt_email.text().strip()
            }
            self.repo.create_service_provider(data)
            QMessageBox.information(self, "تم الحفظ", f"✅ تم إضافة شريك الخدمة الجديد بنجاح!")

        self.accept()
