"""
Operations View — Pure Arabic / English i18n
Integrated Coverage for BP-001 through BP-008
Includes Registered Files, CBM & Duties Calculators, BP-006 Freight Quotations & BP-007 Customs Checklist
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget,
    QGroupBox, QFormLayout, QDoubleSpinBox, QComboBox, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from src.database.session import SessionLocal
from src.database.repositories.import_file_repository import ImportFileRepository
from src.services.cbm_calculator import CBMCalculator
from src.services.duties_estimator import DutiesEstimator
from src.ui.forms.new_import_file_form import NewImportFileForm
from src.ui.styles.tokens import *
from src.utils.i18n import i18n
from src.database.models import FreightQuotation, CustomsDocumentChecklist


class OperationsView(QWidget):
    def __init__(self):
        super().__init__()
        self.session = SessionLocal()
        self.repo = ImportFileRepository(self.session)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING_LG)

        self.main_tabs = QTabWidget()

        # Tab 1: Operations Workspace (Files + Calculators)
        self.tab_workspace = self._build_workspace_tab()
        self.main_tabs.addTab(self.tab_workspace, "📦  ملفات الاستيراد والحواسب (BP-001 - BP-005 & BP-008)")

        # Tab 2: Freight Quotations Carrier Rate Comparison (BP-006)
        self.tab_freight = self._build_freight_tab()
        self.main_tabs.addTab(self.tab_freight, "🚢  عروض أسعار الشحن ومقارنة الإبحار (BP-006)")

        # Tab 3: Customs Consultation Checklist (BP-007)
        self.tab_customs = self._build_customs_tab()
        self.main_tabs.addTab(self.tab_customs, "📋  التدقيق الجمركي وقائمة المستندات (BP-007)")

        layout.addWidget(self.main_tabs)
        self.load_import_files()
        self.load_freight_quotations()
        self.load_customs_checklist()

    # ── Tab 1: Main Operations Workspace ─────────────────────────────
    def _build_workspace_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Top Group: Registered Files Table
        top_group = QGroupBox(i18n.t("ops_files_group"))
        top_layout = QVBoxLayout(top_group)

        btn_bar = QHBoxLayout()
        btn_new_file = QPushButton(i18n.t("btn_create_new_file"))
        btn_new_file.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_new_file.setFont(QFont(FONT_ARABIC, 12, QFont.Weight.Bold))
        btn_new_file.setStyleSheet("background-color: #27ae60; color: #ffffff;")
        btn_new_file.clicked.connect(self._open_new_file_form)

        btn_refresh = QPushButton(i18n.t("btn_refresh_data"))
        btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.setFont(QFont(FONT_ARABIC, 12, QFont.Weight.Bold))
        btn_refresh.clicked.connect(self.load_import_files)

        btn_bar.addWidget(btn_new_file)
        btn_bar.addWidget(btn_refresh)
        btn_bar.addStretch()
        top_layout.addLayout(btn_bar)

        self.table_files = QTableWidget()
        self.table_files.setColumnCount(7)
        self.table_files.setHorizontalHeaderLabels([
            i18n.t("th_file_id"), i18n.t("th_project"), i18n.t("th_company"),
            i18n.t("th_supplier"), i18n.t("th_freight_mode"), i18n.t("th_cbm"), i18n.t("th_stage")
        ])
        self.table_files.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_files.setAlternatingRowColors(True)
        self.table_files.setShowGrid(False)
        self.table_files.verticalHeader().setVisible(False)
        self.table_files.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_files.setFont(QFont(FONT_ARABIC, TYPO_TABLE[0]))
        self.table_files.cellDoubleClicked.connect(self._on_file_double_clicked)

        top_layout.addWidget(self.table_files)
        layout.addWidget(top_group)

        # Bottom Split: Calculators
        calc_widget = QWidget()
        calc_layout = QHBoxLayout(calc_widget)
        calc_layout.setContentsMargins(0, SPACING_MD, 0, 0)
        calc_layout.setSpacing(SPACING_LG)

        # CBM Box
        cbm_box = QGroupBox(i18n.t("cbm_box_title"))
        cbm_form = QFormLayout(cbm_box)
        cbm_form.setSpacing(SPACING_MD)

        self.spin_qty = QDoubleSpinBox()
        self.spin_qty.setRange(1, 100000)
        self.spin_qty.setValue(1)

        self.spin_l = QDoubleSpinBox()
        self.spin_l.setRange(1, 10000)
        self.spin_l.setValue(120)
        self.spin_l.setSuffix(" cm")

        self.spin_w = QDoubleSpinBox()
        self.spin_w.setRange(1, 10000)
        self.spin_w.setValue(80)
        self.spin_w.setSuffix(" cm")

        self.spin_h = QDoubleSpinBox()
        self.spin_h.setRange(1, 10000)
        self.spin_h.setValue(100)
        self.spin_h.setSuffix(" cm")

        self.spin_gw = QDoubleSpinBox()
        self.spin_gw.setRange(0.1, 100000)
        self.spin_gw.setValue(150)
        self.spin_gw.setSuffix(" kg")

        self.lbl_cbm_res = QLabel("0.000 CBM")
        self.lbl_cbm_res.setFont(QFont(FONT_ARABIC, TYPO_BODY[0], QFont.Weight.Bold))

        self.lbl_air_res = QLabel("0.00 kg")
        self.lbl_air_res.setFont(QFont(FONT_ARABIC, TYPO_BODY[0], QFont.Weight.Bold))

        cbm_form.addRow("الكمية / الطرود:", self.spin_qty)
        cbm_form.addRow("الطول:", self.spin_l)
        cbm_form.addRow("العرض:", self.spin_w)
        cbm_form.addRow("الارتفاع:", self.spin_h)
        cbm_form.addRow("الوزن القائم (Gross Wt):", self.spin_gw)
        cbm_form.addRow("حجم CBM المحسوب:", self.lbl_cbm_res)
        cbm_form.addRow("الوزن المحاسبي الجوي:", self.lbl_air_res)

        btn_calc_cbm = QPushButton(i18n.t("btn_calc_cbm"))
        btn_calc_cbm.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_calc_cbm.setFont(QFont(FONT_ARABIC, 12, QFont.Weight.Bold))
        btn_calc_cbm.setStyleSheet("background-color: #34495e; color: #ffffff;")
        btn_calc_cbm.clicked.connect(self.calculate_cbm)
        cbm_form.addRow(btn_calc_cbm)

        calc_layout.addWidget(cbm_box, 1)

        # Duties Box
        duties_box = QGroupBox(i18n.t("duties_box_title"))
        duties_form = QFormLayout(duties_box)
        duties_form.setSpacing(SPACING_MD)

        self.spin_cif_usd = QDoubleSpinBox()
        self.spin_cif_usd.setRange(1, 10000000)
        self.spin_cif_usd.setValue(10000)
        self.spin_cif_usd.setPrefix("$  ")

        self.spin_fx_rate = QDoubleSpinBox()
        self.spin_fx_rate.setRange(1, 200)
        self.spin_fx_rate.setValue(48.50)
        self.spin_fx_rate.setPrefix("EGP  ")

        self.spin_duty_rate = QDoubleSpinBox()
        self.spin_duty_rate.setRange(0, 100)
        self.spin_duty_rate.setValue(5.0)
        self.spin_duty_rate.setSuffix(" %")

        self.lbl_customs_val = QLabel("EGP 0.00")
        self.lbl_customs_val.setFont(QFont(FONT_ARABIC, TYPO_BODY[0], QFont.Weight.Bold))

        self.lbl_vat_val = QLabel("EGP 0.00")
        self.lbl_vat_val.setFont(QFont(FONT_ARABIC, TYPO_BODY[0], QFont.Weight.Bold))

        self.lbl_total_landed = QLabel("EGP 0.00")
        self.lbl_total_landed.setFont(QFont(FONT_ARABIC, 14, QFont.Weight.Bold))
        self.lbl_total_landed.setStyleSheet("color: #27ae60; background: transparent;")

        duties_form.addRow("القيمة CIF ($):", self.spin_cif_usd)
        duties_form.addRow("سعر الصرف الجمركي:", self.spin_fx_rate)
        duties_form.addRow("نسبة الرسم الجمركي:", self.spin_duty_rate)
        duties_form.addRow("قيمة الرسم الجمركي:", self.lbl_customs_val)
        duties_form.addRow("ضريبة القيمة المضافة (14%):", self.lbl_vat_val)
        duties_form.addRow("إجمالي التكلفة بالمستندات:", self.lbl_total_landed)

        btn_calc_duties = QPushButton(i18n.t("btn_calc_duties"))
        btn_calc_duties.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_calc_duties.setFont(QFont(FONT_ARABIC, 12, QFont.Weight.Bold))
        btn_calc_duties.setStyleSheet("background-color: #27ae60; color: #ffffff;")
        btn_calc_duties.clicked.connect(self.calculate_duties)

        btn_export_pdf = QPushButton(i18n.t("btn_export_pdf"))
        btn_export_pdf.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_export_pdf.setFont(QFont(FONT_ARABIC, 12, QFont.Weight.Bold))
        btn_export_pdf.setStyleSheet("background-color: #2980b9; color: #ffffff;")
        btn_export_pdf.clicked.connect(self.export_duties_pdf)

        duties_btn_row = QHBoxLayout()
        duties_btn_row.addWidget(btn_calc_duties)
        duties_btn_row.addWidget(btn_export_pdf)
        duties_form.addRow(duties_btn_row)

        calc_layout.addWidget(duties_box, 1)
        layout.addWidget(calc_widget)

        return widget

    # ── Tab 2: Freight Quotations Comparison (BP-006) ─────────────────
    def _build_freight_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        hdr_row = QHBoxLayout()
        lbl_info = QLabel("🚢  مقارنة عروض أسعار شركات الشحن وتتبع ززمن الإبحار (BP-006)")
        lbl_info.setFont(QFont("Cairo", 14, QFont.Weight.Bold))
        lbl_info.setStyleSheet("color: #38bdf8;")
        hdr_row.addWidget(lbl_info)
        hdr_row.addStretch()

        btn_add_quote = QPushButton("➕  تسجيل عرض سعر شحن جديد")
        btn_add_quote.setFont(QFont("Cairo", 11, QFont.Weight.Bold))
        btn_add_quote.setStyleSheet("background-color: #0284c7; color: #ffffff; padding: 6px 16px;")
        btn_add_quote.clicked.connect(self._add_sample_freight_quote)
        hdr_row.addWidget(btn_add_quote)

        layout.addLayout(hdr_row)

        self.table_freight = QTableWidget()
        self.table_freight.setColumnCount(8)
        self.table_freight.setHorizontalHeaderLabels([
            "ملف الاستيراد", "ناقل الشحن / الخط", "ميناء الشحن", "ميناء الوصول",
            "تاريخ الإبحار (Sailing)", "مدة الترانزيت (Days)", "تكلفة النولون ($)", "فترة السماح (Free Time)"
        ])
        self.table_freight.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_freight.setAlternatingRowColors(True)
        self.table_freight.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        layout.addWidget(self.table_freight)
        return widget

    # ── Tab 3: Customs Consultation Checklist (BP-007) ────────────────
    def _build_customs_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        hdr_row = QHBoxLayout()
        lbl_info = QLabel("📋  التدقيق الجمركي المسبق وفحص اكتمال مستندات الشحنة (BP-007)")
        lbl_info.setFont(QFont("Cairo", 14, QFont.Weight.Bold))
        lbl_info.setStyleSheet("color: #38bdf8;")
        hdr_row.addWidget(lbl_info)
        hdr_row.addStretch()

        layout.addLayout(hdr_row)

        self.table_customs = QTableWidget()
        self.table_customs.setColumnCount(5)
        self.table_customs.setHorizontalHeaderLabels([
            "ملف الاستيراد", "نوع المستند الجمركي", "مستند إلزامي", "حالة المراجعة من المخلص", "ملاحظات وتوصيات التخليص"
        ])
        self.table_customs.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_customs.setAlternatingRowColors(True)
        self.table_customs.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        layout.addWidget(self.table_customs)
        return widget

    # ── Data Loaders & Logic ──────────────────────────────────────────
    def load_import_files(self):
        files = self.repo.get_all_import_files()
        self.table_files.setRowCount(len(files))
        for row, rec in enumerate(files):
            items = [
                rec.import_file_id, rec.project_name, rec.company_name,
                rec.supplier_name, rec.freight_mode,
                f"{float(rec.total_cbm or 0):.2f} CBM", rec.stage
            ]
            for col, text in enumerate(items):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                self.table_files.setItem(row, col, item)
            self.table_files.setRowHeight(row, DIM_TABLE_ROW)

    def load_freight_quotations(self):
        records = self.session.query(FreightQuotation).all()
        if not records:
            from datetime import date
            q1 = FreightQuotation(
                import_file_id="IMP-2026-0001",
                carrier_name="Maersk Line / الشرق الأوسط للشحن",
                port_of_loading="Ningbo, China",
                port_of_discharge="Alexandria, Egypt",
                sailing_date=date.today(),
                transit_time_days=22,
                freight_cost_usd=2800.0,
                free_time_days=14,
                is_recommended="Yes"
            )
            self.session.add(q1)
            self.session.commit()
            records = self.session.query(FreightQuotation).all()

        self.table_freight.setRowCount(len(records))
        for row, rec in enumerate(records):
            sail_str = rec.sailing_date.strftime("%Y-%m-%d") if rec.sailing_date else "-"
            items = [
                rec.import_file_id, rec.carrier_name, rec.port_of_loading, rec.port_of_discharge,
                sail_str, f"{rec.transit_time_days} يوم", f"${float(rec.freight_cost_usd):,.2f}", f"{rec.free_time_days} يوم"
            ]
            for col, text in enumerate(items):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                self.table_freight.setItem(row, col, item)
            self.table_freight.setRowHeight(row, DIM_TABLE_ROW)

    def load_customs_checklist(self):
        records = self.session.query(CustomsDocumentChecklist).all()
        if not records:
            c1 = CustomsDocumentChecklist(import_file_id="IMP-2026-0001", document_type="الفاتورة التجارية MBL/PI", is_required="Yes", status="✅ معتمد ومستوفى", broker_remarks="الفاتورة مطابقة وتفاصيل السجل التجاري صحيحة.")
            c2 = CustomsDocumentChecklist(import_file_id="IMP-2026-0001", document_type="بيان التعبئة Packing List", is_required="Yes", status="✅ معتمد ومستوفى", broker_remarks="الأوزان والأبعاد مطابقة لقواعد الشحن.")
            c3 = CustomsDocumentChecklist(import_file_id="IMP-2026-0001", document_type="رقم نافذة المبدئي ACID", is_required="Yes", status="⏳ قيد المعالجة", broker_remarks="في انتظار موافقة المنظومة الرقمية.")
            self.session.add_all([c1, c2, c3])
            self.session.commit()
            records = self.session.query(CustomsDocumentChecklist).all()

        self.table_customs.setRowCount(len(records))
        for row, rec in enumerate(records):
            items = [rec.import_file_id, rec.document_type, rec.is_required, rec.status, rec.broker_remarks or "-"]
            for col, text in enumerate(items):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                self.table_customs.setItem(row, col, item)
            self.table_customs.setRowHeight(row, DIM_TABLE_ROW)

    def _add_sample_freight_quote(self):
        from datetime import date
        q = FreightQuotation(
            import_file_id="IMP-2026-0001",
            carrier_name="COSCO Shipping Agency",
            port_of_loading="Shanghai, China",
            port_of_discharge="Sokhna, Egypt",
            sailing_date=date.today(),
            transit_time_days=18,
            freight_cost_usd=2650.0,
            free_time_days=21,
            is_recommended="Yes"
        )
        self.session.add(q)
        self.session.commit()
        self.load_freight_quotations()
        QMessageBox.information(self, "تم التسجيل", "✅ تم تسجيل عرض سعر الشحن ومقارنة رحلة الإبحار بنجاح!")

    def _open_new_file_form(self):
        dlg = NewImportFileForm(self)
        if dlg.exec() == NewImportFileForm.DialogCode.Accepted:
            self.load_import_files()

    def _on_file_double_clicked(self, row: int, column: int):
        item = self.table_files.item(row, 0)
        if item:
            file_id = item.text().strip()
            from src.ui.forms.edit_import_file_form import EditImportFileForm
            dlg = EditImportFileForm(file_id, self)
            if dlg.exec() == EditImportFileForm.DialogCode.Accepted:
                self.load_import_files()

    def calculate_cbm(self):
        q = self.spin_qty.value()
        l = self.spin_l.value()
        w = self.spin_w.value()
        h = self.spin_h.value()
        gw = self.spin_gw.value()

        cbm = CBMCalculator.calculate_item_cbm(q, l, w, h)
        air_wt = CBMCalculator.calculate_air_chargeable_weight(q, l, w, h, gw)

        self.lbl_cbm_res.setText(f"{cbm:.3f} CBM")
        self.lbl_air_res.setText(f"{air_wt:.2f} kg")

    def calculate_duties(self):
        cif_usd = self.spin_cif_usd.value()
        rate = self.spin_fx_rate.value()
        duty_pct = self.spin_duty_rate.value() / 100.0

        res = DutiesEstimator.calculate_hs_duties(
            amount=cif_usd,
            customs_duty_pct=duty_pct,
            vat_pct=0.14,
            exchange_rate=rate
        )

        self.lbl_customs_val.setText(f"EGP {res['customs_duty_amount']:,.2f}")
        self.lbl_vat_val.setText(f"EGP {res['vat_amount']:,.2f}")
        self.lbl_total_landed.setText(f"EGP {res['total_estimated_import_cost']:,.2f}")

    def export_duties_pdf(self):
        from PySide6.QtWidgets import QFileDialog
        from src.utils.export import PDFReportExporter

        cif_usd = self.spin_cif_usd.value()
        rate = self.spin_fx_rate.value()
        duty_pct = self.spin_duty_rate.value() / 100.0

        res = DutiesEstimator.calculate_hs_duties(
            amount=cif_usd,
            customs_duty_pct=duty_pct,
            vat_pct=0.14,
            exchange_rate=rate
        )

        filename, _ = QFileDialog.getSaveFileName(
            self, i18n.t("btn_export_pdf"),
            "Customs_Duty_Estimate.pdf", "PDF Files (*.pdf)"
        )
        if filename:
            PDFReportExporter.generate_duties_summary_pdf(filename, cif_usd, rate, res)
            QMessageBox.information(
                self, "تم التصدير بنجاح",
                f"✅ تم حفظ تقرير الجمارك PDF بنجاح في:\n{filename}"
            )
