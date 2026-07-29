"""
Finance View — Pure Arabic / English i18n
No merged pipe labels in form fields, buttons, group titles, or table headers.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit,
    QFormLayout, QComboBox, QMessageBox, QGroupBox, QDoubleSpinBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from src.database.session import SessionLocal
from src.database.repositories.payment_repository import PaymentRepository
from src.database.repositories.import_file_repository import ImportFileRepository
from src.ui.styles.tokens import *
from src.utils.i18n import i18n


class FinanceView(QWidget):
    def __init__(self):
        super().__init__()
        self.session = SessionLocal()
        self.pay_repo = PaymentRepository(self.session)
        self.file_repo = ImportFileRepository(self.session)

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING_LG)

        # ── Left: Payment Request Form ────────────────────────────────
        form_group = QGroupBox(i18n.t("fin_form_group"))
        form_layout = QFormLayout(form_group)
        form_layout.setSpacing(SPACING_MD)

        self.cmb_import_file = QComboBox()
        self.load_import_file_options()

        self.txt_supplier_name = QLineEdit("Global Tech Exporters Ltd")
        self.txt_supplier_name.setReadOnly(True)

        self.cmb_payment_type = QComboBox()
        if i18n.current_lang == "ar":
            self.cmb_payment_type.addItems(["دفعة مقدمة", "ضد شحن", "تصفية نهائية"])
        else:
            self.cmb_payment_type.addItems(["Advance Payment", "Against BL", "Final Settlement"])

        self.spin_requested_amount = QDoubleSpinBox()
        self.spin_requested_amount.setRange(100, 10000000)
        self.spin_requested_amount.setValue(5000)
        self.spin_requested_amount.setPrefix("$  ")
        self.spin_requested_amount.setSingleStep(500)

        self.txt_swift_code = QLineEdit("BKCHCNBJ100")
        self.txt_iban = QLineEdit("CN88 1002 9988 7766 5544 3322")

        form_layout.addRow("ملف الاستيراد:", self.cmb_import_file)
        form_layout.addRow("المورد المستفيد:", self.txt_supplier_name)
        form_layout.addRow("نوع الدفعة المالية:", self.cmb_payment_type)
        form_layout.addRow("المبلغ المطلوب ($):", self.spin_requested_amount)
        form_layout.addRow("رمز السويفت SWIFT:", self.txt_swift_code)
        form_layout.addRow("رقم الحساب IBAN:", self.txt_iban)

        btn_submit = QPushButton(i18n.t("btn_submit_payment"))
        btn_submit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_submit.setFont(QFont(FONT_ARABIC, TYPO_BUTTON[0], QFont.Weight.Bold))
        btn_submit.setStyleSheet("background-color: #2980b9; color: #ffffff;")
        btn_submit.clicked.connect(self.submit_payment_request)
        form_layout.addRow(btn_submit)

        layout.addWidget(form_group, 1)

        # ── Right: Payment History Table ─────────────────────────────
        right_group = QGroupBox(i18n.t("fin_table_group"))
        right_layout = QVBoxLayout(right_group)
        right_layout.setContentsMargins(0, SPACING_MD, 0, 0)

        self.payment_table = QTableWidget()
        self.payment_table.setColumnCount(6)
        self.payment_table.setHorizontalHeaderLabels([
            i18n.t("th_file_id"), i18n.t("th_company"),
            i18n.t("th_amount"), i18n.t("th_payment_type"),
            i18n.t("th_status"), i18n.t("th_swift")
        ])
        self.payment_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.payment_table.setAlternatingRowColors(True)
        self.payment_table.setShowGrid(False)
        self.payment_table.verticalHeader().setVisible(False)
        self.payment_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.payment_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.payment_table.setFont(QFont(FONT_ARABIC, TYPO_TABLE[0]))
        self.payment_table.cellDoubleClicked.connect(self._on_payment_double_clicked)

        right_layout.addWidget(self.payment_table)
        layout.addWidget(right_group, 2)

        self.load_payment_history()

    def load_import_file_options(self):
        files = self.file_repo.get_all_import_files()
        self.cmb_import_file.clear()
        if files:
            for f in files:
                self.cmb_import_file.addItem(f"{f.import_file_id} — {f.project_name}", f.import_file_id)
        else:
            self.cmb_import_file.addItem("IMP-2026-0001 — توسعات المصنع 2026", "IMP-2026-0001")

    def _on_payment_double_clicked(self, row: int, column: int):
        item = self.payment_table.item(row, 0)
        if item:
            req_id = item.text().strip()
            from src.ui.forms.edit_payment_request_form import EditPaymentRequestForm
            dlg = EditPaymentRequestForm(req_id, self)
            if dlg.exec() == EditPaymentRequestForm.DialogCode.Accepted:
                self.load_payment_history()

    def submit_payment_request(self):
        amount = self.spin_requested_amount.value()
        pay_type = self.cmb_payment_type.currentText()
        file_id = self.cmb_import_file.currentData() or self.cmb_import_file.currentText().split(" — ")[0]

        data = {
            "import_file_id": file_id,
            "beneficiary_name": self.txt_supplier_name.text(),
            "payment_type": pay_type,
            "requested_amount_usd": amount,
            "swift_code": self.txt_swift_code.text(),
            "iban_account": self.txt_iban.text(),
            "status": "⏳ قيد المعالجة",
            "swift_reference": "قيد الإصدار"
        }

        # Save to DB
        req = self.pay_repo.create_payment_request(data)

        QMessageBox.information(
            self, "تم الإرسال",
            f"✅ تم تسجيل طلب الدفع رقم: {req.request_id}\nبمبلغ ${amount:,.2f} ({pay_type}) في قاعدة البيانات بنجاح!"
        )

        self.load_payment_history()

    def load_payment_history(self):
        records = self.pay_repo.get_all_payment_requests()

        # Seed sample payments if database is empty on first run
        if not records:
            sample_data = [
                {"import_file_id": "IMP-2026-0001", "beneficiary_name": "Global Tech Exporters Ltd", "payment_type": "Advance Payment", "requested_amount_usd": 15000.0, "status": "✅ مدفوع", "swift_reference": "SWIFT-88997766"},
                {"import_file_id": "IMP-2026-0002", "beneficiary_name": "Shanghai Machinery Corp",     "payment_type": "Against BL",      "requested_amount_usd": 45000.0, "status": "⏳ جاري المعالجة", "swift_reference": "قيد الإصدار"},
            ]
            for data in sample_data:
                self.pay_repo.create_payment_request(data)
            records = self.pay_repo.get_all_payment_requests()

        self.payment_table.setRowCount(len(records))
        for row, rec in enumerate(records):
            items = [
                rec.request_id,
                rec.import_file_id,
                f"${rec.requested_amount_usd:,.2f}",
                rec.payment_type,
                rec.status,
                rec.swift_reference or "قيد الإصدار"
            ]
            for col, text in enumerate(items):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                self.payment_table.setItem(row, col, item)
            self.payment_table.setRowHeight(row, DIM_TABLE_ROW)
