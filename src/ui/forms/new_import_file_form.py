"""
New Import File Form Dialog — PySide6 Enterprise Form
Allows creating a new import file (IMP-2026-xxxx) and adding items with CBM calculation.
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
from src.database.repositories.master_data_repository import MasterDataRepository
from src.services.cbm_calculator import CBMCalculator
from src.ui.styles.tokens import *
from src.utils.i18n import i18n


class NewImportFileForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📦  إنشاء ملف استيراد جديد  |  New Import File")
        self.resize(750, 580)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.session = SessionLocal()
        self.file_repo = ImportFileRepository(self.session)
        self.md_repo = MasterDataRepository(self.session)

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # Title
        hdr = QLabel("📦  إنشاء ملف استيراد جديد  |  Create New Import File (BP-001)")
        hdr.setFont(QFont("Cairo", 15, QFont.Weight.Bold))
        hdr.setStyleSheet("color: #2c3e50; border-bottom: 2px solid #16a085; padding-bottom: 8px;")
        layout.addWidget(hdr)

        # Header Info Group
        form_group = QGroupBox("بيانات ملف الاستيراد الرئيسي")
        form_layout = QFormLayout(form_group)
        form_layout.setSpacing(12)

        # Company selection
        self.cmb_company = QComboBox()
        companies = self.md_repo.get_all_companies()
        if companies:
            for c in companies:
                self.cmb_company.addItem(c.egyptian_importer_name, c.company_id)
        else:
            self.cmb_company.addItem("الشركة المصرية للاستيراد والتصدير", 1)

        # Supplier selection
        self.cmb_supplier = QComboBox()
        suppliers = self.md_repo.get_all_suppliers()
        if suppliers:
            for s in suppliers:
                self.cmb_supplier.addItem(s.vendor_company_name, s.supplier_id)
        else:
            self.cmb_supplier.addItem("Global Tech Exporters Ltd", 1)

        self.txt_project = QLineEdit("توسعات الخط الثالث 2026")
        self.cmb_freight_mode = QComboBox()
        self.cmb_freight_mode.addItems([
            "Ocean FCL 40HC (شحن بحري حاوية كاملة)",
            "Ocean FCL 20GP",
            "Ocean LCL (شحن بحري جزئي)",
            "Air Freight (شحن جوي طارئ)"
        ])

        form_layout.addRow("الشركة المستوردة:", self.cmb_company)
        form_layout.addRow("المورد الأجنبي:", self.cmb_supplier)
        form_layout.addRow("اسم المشروع / الصفقة:", self.txt_project)
        form_layout.addRow("وسيلة ونوع الشحن:", self.cmb_freight_mode)

        layout.addWidget(form_group)

        # Quick Item Entry Group
        item_group = QGroupBox("إضافة بنود الشحنة والحجم (Packing List & CBM)")
        item_layout = QFormLayout(item_group)

        self.txt_item_desc = QLineEdit("أجهزة كمبيوتر ومعدات إلكترونية")
        self.txt_hs_code = QLineEdit("8471.30.00")
        self.spin_qty = QDoubleSpinBox()
        self.spin_qty.setRange(1, 10000)
        self.spin_qty.setValue(10)

        self.spin_l = QDoubleSpinBox()
        self.spin_l.setRange(1, 1000)
        self.spin_l.setValue(120)
        self.spin_l.setSuffix(" cm")

        self.spin_w = QDoubleSpinBox()
        self.spin_w.setRange(1, 1000)
        self.spin_w.setValue(80)
        self.spin_w.setSuffix(" cm")

        self.spin_h = QDoubleSpinBox()
        self.spin_h.setRange(1, 1000)
        self.spin_h.setValue(100)
        self.spin_h.setSuffix(" cm")

        self.spin_gw = QDoubleSpinBox()
        self.spin_gw.setRange(1, 100000)
        self.spin_gw.setValue(450)
        self.spin_gw.setSuffix(" kg")

        item_layout.addRow("وصف البند المورد:", self.txt_item_desc)
        item_layout.addRow("كود البند الجمركي (HS Code):", self.txt_hs_code)
        item_layout.addRow("الكمية:", self.spin_qty)

        dim_row = QHBoxLayout()
        dim_row.addWidget(QLabel("الطول:"))
        dim_row.addWidget(self.spin_l)
        dim_row.addWidget(QLabel("العرض:"))
        dim_row.addWidget(self.spin_w)
        dim_row.addWidget(QLabel("الارتفاع:"))
        dim_row.addWidget(self.spin_h)
        dim_row.addWidget(QLabel("الوزن القائم:"))
        dim_row.addWidget(self.spin_gw)
        item_layout.addRow(dim_row)

        layout.addWidget(item_group)

        # Action Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        btn_cancel = QPushButton("إلغاء  |  Cancel")
        btn_cancel.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_cancel.clicked.connect(self.reject)

        btn_save = QPushButton("💾  حفظ ملف الاستيراد  |  Save Import File")
        btn_save.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: #ffffff;
                border: none;
                padding: 10px 24px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        btn_save.clicked.connect(self._save_file)

        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_save)
        layout.addLayout(btn_row)

    def _save_file(self):
        project = self.txt_project.text().strip()
        comp_name = self.cmb_company.currentText()
        supp_name = self.cmb_supplier.currentText()
        mode = self.cmb_freight_mode.currentText().split(" (")[0]

        if not project:
            QMessageBox.warning(self, "تحذير", "برجاء إدخال اسم المشروع أو الصفقة")
            return

        # Calculate CBM for item
        l = self.spin_l.value()
        w = self.spin_w.value()
        h = self.spin_h.value()
        qty = self.spin_qty.value()
        gw = self.spin_gw.value()

        item_cbm = CBMCalculator.calculate_item_cbm(qty, l, w, h)

        file_data = {
            "project_name": project,
            "company_name": comp_name,
            "supplier_name": supp_name,
            "freight_mode": mode,
            "stage": "Pre-Shipment",
            "total_cbm": item_cbm,
            "total_gross_weight_kg": gw,
            "total_invoice_usd": 15000.0
        }

        # Save header to DB
        new_file = self.file_repo.create_import_file(file_data)

        # Save item
        item_data = {
            "item_description": self.txt_item_desc.text().strip(),
            "hs_code": self.txt_hs_code.text().strip(),
            "qty": qty,
            "unit_price_usd": 1500.0,
            "total_price_usd": 15000.0,
            "length_cm": l,
            "width_cm": w,
            "height_cm": h,
            "gross_weight_kg": gw,
            "item_cbm": item_cbm
        }
        self.file_repo.add_item_to_file(new_file.import_file_id, item_data)

        QMessageBox.information(
            self, "تم الحفظ بنجاح",
            f"✅ تم إنشاء ملف الاستيراد رقم: {new_file.import_file_id}\nبحجم محاسبي: {item_cbm:.3f} CBM"
        )
        self.accept()
