"""
New / Edit Incoterm Form Dialog (MD-007)
Allows adding and updating Incoterms 2020 rules and descriptions.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFormLayout, QGroupBox, QMessageBox, QTextEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from src.database.session import SessionLocal
from src.utils.i18n import i18n
from src.database.models import Incoterm


class NewIncotermForm(QDialog):
    def __init__(self, incoterm_id=None, parent=None):
        super().__init__(parent)
        self.incoterm_id = incoterm_id
        self.is_edit = bool(incoterm_id)

        title = "تعديل شرط Incoterms" if self.is_edit else "إضافة شرط تسليم جديد Incoterms 2020 (MD-007)"
        self.setWindowTitle(title)
        self.resize(600, 420)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft if i18n.current_lang == "ar" else Qt.LayoutDirection.LeftToRight)

        self.session = SessionLocal()
        self.incoterm_obj = self.session.query(Incoterm).filter(Incoterm.incoterm_id == incoterm_id).first() if self.is_edit else None

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        hdr_text = f"📜  تعديل شرط Incoterm: #{self.incoterm_id}" if self.is_edit else "📜  إضافة شرط تسليم جديد Incoterms 2020 (MD-007)"
        hdr = QLabel(hdr_text)
        hdr.setFont(QFont("Cairo", 15, QFont.Weight.Bold))
        hdr.setStyleSheet("color: #38bdf8; border-bottom: 2px solid #0284c7; padding-bottom: 8px;")
        layout.addWidget(hdr)

        form_group = QGroupBox("تفاصيل شرط الشحن والتسليم")
        form_layout = QFormLayout(form_group)
        form_layout.setSpacing(12)

        self.txt_code = QLineEdit(self.incoterm_obj.incoterm_code if self.incoterm_obj else "FOB")
        self.txt_name = QLineEdit(self.incoterm_obj.name if self.incoterm_obj else "Free On Board")
        self.txt_version = QLineEdit(self.incoterm_obj.version if self.incoterm_obj else "Incoterms 2020")
        self.txt_desc = QTextEdit(self.incoterm_obj.description if self.incoterm_obj else "المورد يتحمل مصاريف الشحن الداخلي والتخلبص بميناء التصدير، والمستورد يتحمل النولون البحري والتأمين والتخليص بميناء الوصول.")
        self.txt_desc.setMaximumHeight(90)

        form_layout.addRow("كود الشرط (مثل FOB / EXW / CIF):", self.txt_code)
        form_layout.addRow("الاسم التجاري الكامل:", self.txt_name)
        form_layout.addRow("الإصدار:", self.txt_version)
        form_layout.addRow("الوصف ومحتوى المسؤوليات:", self.txt_desc)

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
        btn_save.clicked.connect(self._save_incoterm)

        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_save)
        layout.addLayout(btn_row)

    def _save_incoterm(self):
        code = self.txt_code.text().strip().upper()
        if not code:
            QMessageBox.warning(self, "تنبيه", "يرجى إدخال كود شرط الـ Incoterm!")
            return

        if self.is_edit and self.incoterm_obj:
            self.incoterm_obj.incoterm_code = code
            self.incoterm_obj.name = self.txt_name.text().strip()
            self.incoterm_obj.version = self.txt_version.text().strip()
            self.incoterm_obj.description = self.txt_desc.toPlainText().strip()
            self.session.commit()
            QMessageBox.information(self, "تم التحديث", f"✅ تم تحديث بيانات الشرط {code} بنجاح!")
        else:
            inco = Incoterm(
                incoterm_code=code,
                name=self.txt_name.text().strip(),
                version=self.txt_version.text().strip(),
                description=self.txt_desc.toPlainText().strip()
            )
            self.session.add(inco)
            self.session.commit()
            QMessageBox.information(self, "تم الحفظ", f"✅ تم إضافة شرط الـ Incoterm الجديد ({code}) بنجاح!")

        self.accept()
