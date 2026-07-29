"""
New / Edit Project Form Dialog (MD-008)
Allows adding and updating import projects linking importers, foreign suppliers, and incoterms.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFormLayout, QGroupBox, QMessageBox, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from src.database.session import SessionLocal
from src.database.repositories.master_data_repository import MasterDataRepository
from src.utils.i18n import i18n
from src.database.models import Project, Company, Supplier, Incoterm


class NewProjectForm(QDialog):
    def __init__(self, project_id=None, parent=None):
        super().__init__(parent)
        self.project_id = project_id
        self.is_edit = bool(project_id)

        title = "تعديل مشروع استيرادي" if self.is_edit else "إضافة مشروع استيراد جديد (MD-008)"
        self.setWindowTitle(title)
        self.resize(620, 480)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft if i18n.current_lang == "ar" else Qt.LayoutDirection.LeftToRight)

        self.session = SessionLocal()
        self.repo = MasterDataRepository(self.session)
        self.project_obj = self.session.query(Project).filter(Project.project_id == project_id).first() if self.is_edit else None

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        hdr_text = f"📁  تعديل بيانات المشروع: #{self.project_id}" if self.is_edit else "📁  إضافة مشروع جديد (MD-008)"
        hdr = QLabel(hdr_text)
        hdr.setFont(QFont("Cairo", 15, QFont.Weight.Bold))
        hdr.setStyleSheet("color: #38bdf8; border-bottom: 2px solid #0284c7; padding-bottom: 8px;")
        layout.addWidget(hdr)

        form_group = QGroupBox("بيانات المشروع والأطراف المرتبطة")
        form_layout = QFormLayout(form_group)
        form_layout.setSpacing(12)

        self.txt_code = QLineEdit(self.project_obj.project_code if self.project_obj else "PRJ-2026-001")
        self.txt_name = QLineEdit(self.project_obj.project_name if self.project_obj else "مشروع استيراد خطوط إنتاج 2026")
        self.txt_owner = QLineEdit(self.project_obj.project_owner if self.project_obj else "إدارة المشتريات الخارجية")

        # Load Dropdowns from DB
        companies = self.repo.get_all_companies()
        suppliers = self.repo.get_all_suppliers()
        incoterms = self.repo.get_all_incoterms()

        self.cmb_company = QComboBox()
        for c in companies:
            self.cmb_company.addItem(c.egyptian_importer_name, c.company_id)

        self.cmb_supplier = QComboBox()
        for s in suppliers:
            self.cmb_supplier.addItem(s.vendor_company_name, s.supplier_id)

        self.cmb_incoterm = QComboBox()
        for i in incoterms:
            self.cmb_incoterm.addItem(f"{i.incoterm_code} - {i.name}", i.incoterm_id)

        self.cmb_status = QComboBox()
        self.cmb_status.addItems(["open", "closed", "on_hold"])
        if self.project_obj and self.project_obj.status:
            self.cmb_status.setCurrentText(self.project_obj.status)

        form_layout.addRow("كود المشروع الفريد:", self.txt_code)
        form_layout.addRow("اسم المشروع:", self.txt_name)
        form_layout.addRow("المسؤول / مالك المشروع:", self.txt_owner)
        form_layout.addRow("الشركة المستوردة:", self.cmb_company)
        form_layout.addRow("المورد الأجنبي الرئيسية:", self.cmb_supplier)
        form_layout.addRow("شرط التسليم الافتراضي (Incoterm):", self.cmb_incoterm)
        form_layout.addRow("حالة المشروع:", self.cmb_status)

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
        btn_save.clicked.connect(self._save_project)

        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_save)
        layout.addLayout(btn_row)

    def _save_project(self):
        code = self.txt_code.text().strip()
        name = self.txt_name.text().strip()
        if not code or not name:
            QMessageBox.warning(self, "تنبيه", "يرجى إدخال كود واسم المشروع!")
            return

        cid = self.cmb_company.currentData() or 1
        sid = self.cmb_supplier.currentData() or 1
        iid = self.cmb_incoterm.currentData() or 1

        if self.is_edit and self.project_obj:
            self.project_obj.project_code = code
            self.project_obj.project_name = name
            self.project_obj.project_owner = self.txt_owner.text().strip()
            self.project_obj.company_id = cid
            self.project_obj.supplier_id = sid
            self.project_obj.incoterm_id = iid
            self.project_obj.status = self.cmb_status.currentText()
            self.session.commit()
            QMessageBox.information(self, "تم التحديث", f"✅ تم تحديث بيانات المشروع {code} بنجاح!")
        else:
            prj = Project(
                project_code=code,
                project_name=name,
                project_owner=self.txt_owner.text().strip(),
                company_id=cid,
                supplier_id=sid,
                incoterm_id=iid,
                status=self.cmb_status.currentText()
            )
            self.session.add(prj)
            self.session.commit()
            QMessageBox.information(self, "تم الحفظ", f"✅ تم إضافة المشروع الجديد ({code}) بنجاح!")

        self.accept()
