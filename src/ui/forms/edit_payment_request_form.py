"""
Edit / Update Payment Request Form Dialog
Allows viewing and updating existing payment requests (status, SWIFT reference, notes).
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QDoubleSpinBox, QPushButton, QFormLayout, QGroupBox,
    QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from src.database.session import SessionLocal
from src.database.repositories.payment_repository import PaymentRepository


class EditPaymentRequestForm(QDialog):
    def __init__(self, request_id: str, parent=None):
        super().__init__(parent)
        self.request_id = request_id
        self.setWindowTitle(f"💰  تعديل طلب الدفع {request_id}  |  Edit Payment Request")
        self.resize(650, 480)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.session = SessionLocal()
        self.pay_repo = PaymentRepository(self.session)
        self.payment_req = self.session.query(PaymentRepository(self.session).session.query.__self__.query).filter_by(request_id=request_id).first() if hasattr(PaymentRepository, "query") else None

        # Fetch payment request directly from DB
        from src.database.models.payment_request import PaymentRequest
        self.payment_req = self.session.query(PaymentRequest).filter(PaymentRequest.request_id == request_id).first()

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # Header Title
        hdr = QLabel(f"💰  تفاصيل وتعديل طلب الدفع رقم: {self.request_id}")
        hdr.setFont(QFont("Cairo", 15, QFont.Weight.Bold))
        hdr.setStyleSheet("color: #38bdf8; border-bottom: 2px solid #0284c7; padding-bottom: 8px;")
        layout.addWidget(hdr)

        if not self.payment_req:
            layout.addWidget(QLabel("❌ طلب الدفع المالي غير موجود بالنظام"))
            return

        # Form Group
        form_group = QGroupBox("بيانات الطلب المالية وحالة السداد")
        form_layout = QFormLayout(form_group)
        form_layout.setSpacing(12)

        self.lbl_file_id = QLabel(self.payment_req.import_file_id)
        self.lbl_file_id.setFont(QFont("Cairo", 12, QFont.Weight.Bold))

        self.lbl_beneficiary = QLabel(self.payment_req.beneficiary_name)
        self.lbl_beneficiary.setFont(QFont("Cairo", 12))

        self.lbl_amount = QLabel(f"${float(self.payment_req.requested_amount_usd or 0):,.2f}")
        self.lbl_amount.setFont(QFont("Cairo", 14, QFont.Weight.Bold))
        self.lbl_amount.setStyleSheet("color: #27ae60;")

        self.cmb_status = QComboBox()
        self.cmb_status.addItems([
            "⏳ قيد المعالجة",
            "✅ مدفوع (تم التحويل البنكي)",
            "⚠️ معلق (بانتظار مستندات)",
            "✕ ملغي"
        ])
        if self.payment_req.status in ["✅ مدفوع", "✅ مدفوع (تم التحويل البنكي)"]:
            self.cmb_status.setCurrentIndex(1)
        elif self.payment_req.status in ["⚠️ معلق"]:
            self.cmb_status.setCurrentIndex(2)

        self.txt_swift_ref = QLineEdit(self.payment_req.swift_reference or "SWIFT-88997766")
        self.txt_notes = QLineEdit(self.payment_req.notes or "")

        form_layout.addRow("ملف الاستيراد:", self.lbl_file_id)
        form_layout.addRow("المورد المستفيد:", self.lbl_beneficiary)
        form_layout.addRow("المبلغ المطلوب ($):", self.lbl_amount)
        form_layout.addRow("حالة الطلب والسداد:", self.cmb_status)
        form_layout.addRow("رقم التحويل البنكي SWIFT Ref:", self.txt_swift_ref)
        form_layout.addRow("ملاحظات البنك والإدارة:", self.txt_notes)

        layout.addWidget(form_group)

        # Action Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        btn_cancel = QPushButton("إلغاء  |  Cancel")
        btn_cancel.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_cancel.clicked.connect(self.reject)

        btn_update = QPushButton("💾  حفظ وتعديل الحالة  |  Update Payment")
        btn_update.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_update.setStyleSheet("""
            QPushButton {
                background-color: #2980b9;
                color: #ffffff;
                border: none;
                padding: 10px 24px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1a5276;
            }
        """)
        btn_update.clicked.connect(self._update_payment)

        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_update)
        layout.addLayout(btn_row)

    def _update_payment(self):
        if not self.payment_req:
            return

        self.payment_req.status = self.cmb_status.currentText()
        self.payment_req.swift_reference = self.txt_swift_ref.text().strip()
        self.payment_req.notes = self.txt_notes.text().strip()

        self.session.commit()

        QMessageBox.information(
            self, "تم التحديث بنجاح",
            f"✅ تم تحديث حالة طلب الدفع رقم: {self.request_id} إلى ({self.payment_req.status}) بنجاح!"
        )
        self.accept()
