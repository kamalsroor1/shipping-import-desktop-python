"""
Dashboard View — Pure Arabic / English i18n
No merged pipe labels in buttons, table headers, or cards.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QGroupBox, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from src.ui.styles.tokens import *
from src.utils.i18n import i18n
from src.database.session import SessionLocal
from src.database.repositories.import_file_repository import ImportFileRepository


def make_kpi_card(title_key: str, value: str, color: str, icon: str) -> QFrame:
    card = QFrame()
    card.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
    card.setObjectName("kpiCard")
    card.setStyleSheet(f"""
        QFrame#kpiCard {{
            border: 1px solid {COLOR_BORDER_SUBTLE};
            border-top: 4px solid {color};
            border-radius: {RADIUS_MD}px;
        }}
    """)
    card.setMinimumHeight(110)

    lay = QVBoxLayout(card)
    lay.setContentsMargins(SPACING_MD, SPACING_MD, SPACING_MD, SPACING_MD)
    lay.setSpacing(4)

    top_row = QHBoxLayout()
    icon_lbl = QLabel(icon)
    icon_lbl.setStyleSheet(f"font-size: 24px; color: {color}; background: transparent; border: none;")
    top_row.addStretch()
    top_row.addWidget(icon_lbl)
    lay.addLayout(top_row)

    title_lbl = QLabel(i18n.t(title_key))
    title_lbl.setFont(QFont(FONT_ARABIC, TYPO_LABEL[0], QFont.Weight.Bold))
    title_lbl.setStyleSheet("color: #7f8c8d; background: transparent; border: none;")

    val_lbl = QLabel(value)
    val_lbl.setFont(QFont(FONT_ARABIC, 22, QFont.Weight.Bold))
    val_lbl.setStyleSheet(f"color: {color}; background: transparent; border: none;")

    lay.addWidget(title_lbl)
    lay.addStretch()
    lay.addWidget(val_lbl)
    return card


class DashboardView(QWidget):
    def __init__(self, navigate_callback=None):
        super().__init__()
        self.navigate_callback = navigate_callback
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(SPACING_LG, SPACING_LG, SPACING_LG, SPACING_LG)
        root.setSpacing(SPACING_LG)

        # ── 1. KPI Cards Row ──────────────────────────────────────────
        kpi_row = QHBoxLayout()
        kpi_row.setSpacing(SPACING_MD)

        c1 = make_kpi_card("kpi_active_files", "12 ملف", COLOR_PRIMARY, "📦")
        c2 = make_kpi_card("kpi_pending_payments", "$185,000", COLOR_WARNING, "💳")
        c3 = make_kpi_card("kpi_shipments_enroute", "5 شحنات", COLOR_INFO, "🚢")
        c4 = make_kpi_card("kpi_alerts", "2 تنبيهات", COLOR_DANGER, "⚠️")

        kpi_row.addWidget(c1)
        kpi_row.addWidget(c2)
        kpi_row.addWidget(c3)
        kpi_row.addWidget(c4)

        root.addLayout(kpi_row)

        # ── 2. Quick Actions Group ────────────────────────────────────
        self.qa_group = QGroupBox(i18n.t("quick_actions_header"))
        qa_layout = QHBoxLayout(self.qa_group)
        qa_layout.setContentsMargins(16, 20, 16, 16)
        qa_layout.setSpacing(12)

        self.btn_new_file = QPushButton(i18n.t("btn_new_import_file"))
        self.btn_new_file.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_new_file.setFont(QFont(FONT_ARABIC, 12, QFont.Weight.Bold))
        self.btn_new_file.setStyleSheet("background-color: #34495e; color: #ffffff;")
        self.btn_new_file.clicked.connect(self._on_new_file)

        self.btn_new_pay = QPushButton(i18n.t("btn_new_payment_request"))
        self.btn_new_pay.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_new_pay.setFont(QFont(FONT_ARABIC, 12, QFont.Weight.Bold))
        self.btn_new_pay.setStyleSheet("background-color: #2980b9; color: #ffffff;")
        self.btn_new_pay.clicked.connect(self._on_new_pay)

        self.btn_export = QPushButton(i18n.t("btn_export_reports"))
        self.btn_export.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_export.setFont(QFont(FONT_ARABIC, 12, QFont.Weight.Bold))
        self.btn_export.setStyleSheet("background-color: #27ae60; color: #ffffff;")
        self.btn_export.clicked.connect(self._on_export_reports)

        self.btn_refresh = QPushButton(i18n.t("btn_refresh_data"))
        self.btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_refresh.setFont(QFont(FONT_ARABIC, 12, QFont.Weight.Bold))
        self.btn_refresh.clicked.connect(self._on_refresh)

        qa_layout.addWidget(self.btn_new_file)
        qa_layout.addWidget(self.btn_new_pay)
        qa_layout.addWidget(self.btn_export)
        qa_layout.addWidget(self.btn_refresh)
        qa_layout.addStretch()

        root.addWidget(self.qa_group)

        # ── 3. Recent Files Table ─────────────────────────────────────
        self.table_group = QGroupBox(i18n.t("table_recent_files"))
        table_layout = QVBoxLayout(self.table_group)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            i18n.t("th_file_id"), i18n.t("th_project"), i18n.t("th_company"),
            i18n.t("th_supplier"), i18n.t("th_freight_mode"), i18n.t("th_cbm"), i18n.t("th_stage")
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setFont(QFont(FONT_ARABIC, TYPO_TABLE[0]))

        table_layout.addWidget(self.table)
        root.addWidget(self.table_group, 1)

        self.load_data()

    def load_data(self):
        session = SessionLocal()
        repo = ImportFileRepository(session)
        files = repo.get_all_import_files()
        session.close()

        self.table.setRowCount(len(files))
        for row, rec in enumerate(files):
            items = [
                rec.import_file_id,
                rec.project_name,
                rec.company_name,
                rec.supplier_name,
                rec.freight_mode,
                f"{float(rec.total_cbm or 0):.2f} CBM",
                rec.stage
            ]
            for col, val in enumerate(items):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row, col, item)
            self.table.setRowHeight(row, DIM_TABLE_ROW)

    def _on_new_file(self):
        if self.navigate_callback:
            self.navigate_callback("ops", i18n.t("ops_tab"))

    def _on_new_pay(self):
        if self.navigate_callback:
            self.navigate_callback("finance", i18n.t("finance_tab"))

    def _on_export_reports(self):
        from PySide6.QtWidgets import QFileDialog
        from src.utils.export import ExcelReportExporter

        filename, _ = QFileDialog.getSaveFileName(
            self, i18n.t("btn_export_reports"),
            "Import_Files_Report.xlsx", "Excel Files (*.xlsx)"
        )
        if filename:
            session = SessionLocal()
            repo = ImportFileRepository(session)
            files = repo.get_all_import_files()
            session.close()

            files_data = [
                {
                    "import_file_id": f.import_file_id,
                    "project_name": f.project_name,
                    "company_name": f.company_name,
                    "supplier_name": f.supplier_name,
                    "freight_mode": f.freight_mode,
                    "total_cbm": float(f.total_cbm or 0),
                    "stage": f.stage
                }
                for f in files
            ]
            ExcelReportExporter.export_import_files(filename, files_data)
            QMessageBox.information(
                self, "تم التصدير بنجاح",
                f"✅ تم حفظ تقرير Excel بنجاح في:\n{filename}"
            )

    def _on_refresh(self):
        self.load_data()
