"""
Edit / Update Import File Form Dialog
Allows viewing and editing existing import file details, updating status/stage, and adding items.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QDoubleSpinBox, QPushButton, QFormLayout, QGroupBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from src.database.session import SessionLocal
from src.database.repositories.import_file_repository import ImportFileRepository
from src.services.cbm_calculator import CBMCalculator


class EditImportFileForm(QDialog):
    def __init__(self, file_id: str, parent=None):
        super().__init__(parent)
        self.file_id = file_id
        self.setWindowTitle(f"📦  تعديل ملف الاستيراد {file_id}  |  Edit Import File")
        self.resize(780, 600)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.session = SessionLocal()
        self.file_repo = ImportFileRepository(self.session)
        self.import_file = self.file_repo.get_file_by_id(file_id)

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # Header Title
        hdr = QLabel(f"📦  تفاصيل وتعديل ملف الاستيراد: {self.file_id}")
        hdr.setFont(QFont("Cairo", 15, QFont.Weight.Bold))
        hdr.setStyleSheet("color: #38bdf8; border-bottom: 2px solid #0284c7; padding-bottom: 8px;")
        layout.addWidget(hdr)

        if not self.import_file:
            layout.addWidget(QLabel("❌ ملف الاستيراد غير موجود بملفات النظام"))
            return

        # Form Info Group
        form_group = QGroupBox("بيانات الملف الحالية والتعديل")
        form_layout = QFormLayout(form_group)
        form_layout.setSpacing(12)

        self.txt_project = QLineEdit(self.import_file.project_name)
        self.txt_company = QLineEdit(self.import_file.company_name)
        self.txt_supplier = QLineEdit(self.import_file.supplier_name)

        self.cmb_stage = QComboBox()
        stages = ["Pre-Shipment", "Customs Clearance", "Financial", "Warehouse", "Completed"]
        self.cmb_stage.addItems(stages)
        if self.import_file.stage in stages:
            self.cmb_stage.setCurrentText(self.import_file.stage)

        self.cmb_status = QComboBox()
        self.cmb_status.addItems(["active (نشط)", "completed (مكتمل)", "cancelled (ملغي)"])
        if self.import_file.status == "completed":
            self.cmb_status.setCurrentIndex(1)
        elif self.import_file.status == "cancelled":
            self.cmb_status.setCurrentIndex(2)

        form_layout.addRow("اسم المشروع / الصفقة:", self.txt_project)
        form_layout.addRow("الشركة المستوردة:", self.txt_company)
        form_layout.addRow("المورد الأجنبي:", self.txt_supplier)
        form_layout.addRow("مرحلة الملف الحالية:", self.cmb_stage)
        form_layout.addRow("حالة الملف:", self.cmb_status)

        layout.addWidget(form_group)

        # Stats Summary Group
        stats_group = QGroupBox("إحصائيات الحجم والوزن والفاتورة")
        stats_layout = QHBoxLayout(stats_group)

        lbl_cbm = QLabel(f"📐 الحجم: {float(self.import_file.total_cbm or 0):.2f} CBM")
        lbl_cbm.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        lbl_cbm.setStyleSheet("color: #16a085;")

        lbl_gw = QLabel(f"⚖️ الوزن: {float(self.import_file.total_gross_weight_kg or 0):,.2f} kg")
        lbl_gw.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        lbl_gw.setStyleSheet("color: #2980b9;")

        lbl_inv = QLabel(f"💵 الفاتورة: ${float(self.import_file.total_invoice_usd or 0):,.2f}")
        lbl_inv.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        lbl_inv.setStyleSheet("color: #27ae60;")

        stats_layout.addWidget(lbl_cbm)
        stats_layout.addWidget(lbl_gw)
        stats_layout.addWidget(lbl_inv)
        layout.addWidget(stats_group)

        # Action Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        btn_cancel = QPushButton("إلغاء  |  Cancel")
        btn_cancel.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_cancel.clicked.connect(self.reject)

        btn_update = QPushButton("💾  تحديث وحفظ البيانات  |  Save Changes")
        btn_update.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_update.setStyleSheet("""
            QPushButton {
                background-color: #16a085;
                color: #ffffff;
                border: none;
                padding: 10px 24px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1abc9c;
            }
        """)
        btn_update.clicked.connect(self._update_file)

        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_update)
        layout.addLayout(btn_row)

    def _update_file(self):
        if not self.import_file:
            return

        self.import_file.project_name = self.txt_project.text().strip()
        self.import_file.company_name = self.txt_company.text().strip()
        self.import_file.supplier_name = self.txt_supplier.text().strip()
        self.import_file.stage = self.cmb_stage.currentText()
        st_val = self.cmb_status.currentText().split(" (")[0]
        self.import_file.status = st_val

        self.session.commit()

        QMessageBox.information(
            self, "تم التحديث بنجاح",
            f"✅ تم تحديث بيانات ملف الاستيراد رقم: {self.file_id} بنجاح!"
        )
        self.accept()
