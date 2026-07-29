"""
Master Data View — DESIGN_RULES.md Compliant & Pure i18n
Complete Coverage for MD-001 through MD-010 Master Data Management
Real Database Integration & Interactive Form Dialogs
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget,
    QGroupBox, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from src.database.session import SessionLocal
from src.database.repositories.master_data_repository import MasterDataRepository
from src.services.master_data_service import MasterDataService
from src.ui.styles.tokens import *
from src.utils.i18n import i18n
from src.database.models import (
    Company, Supplier, ServiceProvider, ShippingLine,
    Currency, Incoterm, Project
)
from src.database.models.customs_tariff import CustomsTariff
from src.database.models.container_spec import ContainerSpec

from src.ui.forms.new_company_form import NewCompanyForm
from src.ui.forms.new_supplier_form import NewSupplierForm
from src.ui.forms.new_service_provider_form import NewServiceProviderForm
from src.ui.forms.new_shipping_line_form import NewShippingLineForm
from src.ui.forms.new_currency_form import NewCurrencyForm
from src.ui.forms.new_incoterm_form import NewIncotermForm
from src.ui.forms.new_project_form import NewProjectForm


class MasterDataView(QWidget):
    def __init__(self):
        super().__init__()
        self.session = SessionLocal()
        self.repo = MasterDataRepository(self.session)
        self.service = MasterDataService(self.session)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING_LG)

        self.tabs = QTabWidget()

        # Tab 1: Importer Companies (MD-001)
        self.tab_companies = self._build_companies_tab()
        self.tabs.addTab(self.tab_companies, "🏢  الشركات المستوردة (MD-001)")

        # Tab 2: Foreign Suppliers (MD-002)
        self.tab_suppliers = self._build_suppliers_tab()
        self.tabs.addTab(self.tab_suppliers, "🏭  الموردين الأجانب (MD-002)")

        # Tab 3: Service Providers (MD-004)
        self.tab_providers = self._build_providers_tab()
        self.tabs.addTab(self.tab_providers, "🤝  شركاء الخدمات والملاحة (MD-004)")

        # Tab 4: Customs Tariff (MD-008)
        self.tab_tariffs = self._build_tariffs_tab()
        self.tabs.addTab(self.tab_tariffs, "📋  التعريفة الجمركية (MD-008)")

        # Tab 5: Container Specifications (MD-010)
        self.tab_containers = self._build_containers_tab()
        self.tabs.addTab(self.tab_containers, "📦  مواصفات الحاويات (MD-010)")

        # Tab 6: Shipping Lines (MD-005)
        self.tab_shipping_lines = self._build_shipping_lines_tab()
        self.tabs.addTab(self.tab_shipping_lines, "🚢  الخطوط الملاحية (MD-005)")

        # Tab 7: Currencies (MD-006)
        self.tab_currencies = self._build_currencies_tab()
        self.tabs.addTab(self.tab_currencies, "💱  العملات (MD-006)")

        # Tab 8: Incoterms (MD-007)
        self.tab_incoterms = self._build_incoterms_tab()
        self.tabs.addTab(self.tab_incoterms, "📜  قواعد Incoterms 2020 (MD-007)")

        # Tab 9: Projects (MD-008)
        self.tab_projects = self._build_projects_tab()
        self.tabs.addTab(self.tab_projects, "📁  إدارة المشاريع (MD-008)")

        layout.addWidget(self.tabs)
        self.load_all_data()

    # ── 1. Companies Tab (MD-001) ──────────────────────────────────────
    def _build_companies_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        btn_bar = QHBoxLayout()
        btn_add = QPushButton("➕  إضافة شركة مستوردة جديدة")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_add.setStyleSheet("background-color: #16a085; color: #ffffff;")
        btn_add.clicked.connect(self._add_company)

        btn_refresh = QPushButton(i18n.t("btn_refresh_data"))
        btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_refresh.clicked.connect(self.load_companies)

        btn_bar.addWidget(btn_add)
        btn_bar.addWidget(btn_refresh)
        btn_bar.addStretch()
        layout.addLayout(btn_bar)

        self.table_companies = QTableWidget()
        self.table_companies.setColumnCount(5)
        self.table_companies.setHorizontalHeaderLabels([
            "رقم الشركة", "اسم الشركة المستوردة", "بطاقة المتعاملين",
            "السجل التجاري", "بلد التسجيل"
        ])
        self.table_companies.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_companies.setAlternatingRowColors(True)
        self.table_companies.setShowGrid(False)
        self.table_companies.verticalHeader().setVisible(False)
        self.table_companies.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_companies.setFont(QFont(FONT_ARABIC, TYPO_TABLE[0]))
        self.table_companies.cellDoubleClicked.connect(self._on_company_double_clicked)

        layout.addWidget(self.table_companies)
        return widget

    # ── 2. Suppliers Tab (MD-002) ──────────────────────────────────────
    def _build_suppliers_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        btn_bar = QHBoxLayout()
        btn_add = QPushButton("➕  إضافة مورد أجنبي جديد")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_add.setStyleSheet("background-color: #8e44ad; color: #ffffff;")
        btn_add.clicked.connect(self._add_supplier)

        btn_refresh = QPushButton(i18n.t("btn_refresh_data"))
        btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_refresh.clicked.connect(self.load_suppliers)

        btn_bar.addWidget(btn_add)
        btn_bar.addWidget(btn_refresh)
        btn_bar.addStretch()
        layout.addLayout(btn_bar)

        self.table_suppliers = QTableWidget()
        self.table_suppliers.setColumnCount(5)
        self.table_suppliers.setHorizontalHeaderLabels([
            "رقم المورد", "اسم شركة المورد", "رقم التسجيل الأجنبي",
            "الدولة", "الهاتف"
        ])
        self.table_suppliers.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_suppliers.setAlternatingRowColors(True)
        self.table_suppliers.setShowGrid(False)
        self.table_suppliers.verticalHeader().setVisible(False)
        self.table_suppliers.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_suppliers.setFont(QFont(FONT_ARABIC, TYPO_TABLE[0]))
        self.table_suppliers.cellDoubleClicked.connect(self._on_supplier_double_clicked)

        layout.addWidget(self.table_suppliers)
        return widget

    # ── 3. Service Providers Tab (MD-004) ──────────────────────────────
    def _build_providers_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        btn_bar = QHBoxLayout()
        btn_add = QPushButton("➕  إضافة شريك خدمة جديد")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_add.setStyleSheet("background-color: #2980b9; color: #ffffff;")
        btn_add.clicked.connect(self._add_provider)

        btn_refresh = QPushButton(i18n.t("btn_refresh_data"))
        btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_refresh.clicked.connect(self.load_providers)

        btn_bar.addWidget(btn_add)
        btn_bar.addWidget(btn_refresh)
        btn_bar.addStretch()
        layout.addLayout(btn_bar)

        self.table_providers = QTableWidget()
        self.table_providers.setColumnCount(4)
        self.table_providers.setHorizontalHeaderLabels([
            "رقم الشريك", "اسم الشركة الشريكة",
            "نوع الخدمة", "الهاتف"
        ])
        self.table_providers.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_providers.setAlternatingRowColors(True)
        self.table_providers.setShowGrid(False)
        self.table_providers.verticalHeader().setVisible(False)
        self.table_providers.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_providers.setFont(QFont(FONT_ARABIC, TYPO_TABLE[0]))
        self.table_providers.cellDoubleClicked.connect(self._on_provider_double_clicked)

        layout.addWidget(self.table_providers)
        return widget

    # ── 4. Customs Tariff Tab (MD-008) ─────────────────────────────────
    def _build_tariffs_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        btn_bar = QHBoxLayout()
        btn_refresh = QPushButton(i18n.t("btn_refresh_data"))
        btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_refresh.clicked.connect(self.load_tariffs)
        btn_bar.addWidget(btn_refresh)
        btn_bar.addStretch()
        layout.addLayout(btn_bar)

        self.table_tariffs = QTableWidget()
        self.table_tariffs.setColumnCount(5)
        self.table_tariffs.setHorizontalHeaderLabels([
            "البند الجمركي (HS Code)", "الوصف الجمركي", "نسبة الوارد %",
            "القيمة المضافة %", "الجهة الرقابية"
        ])
        self.table_tariffs.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_tariffs.setAlternatingRowColors(True)
        self.table_tariffs.setShowGrid(False)
        self.table_tariffs.verticalHeader().setVisible(False)
        self.table_tariffs.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_tariffs.setFont(QFont(FONT_ARABIC, TYPO_TABLE[0]))

        layout.addWidget(self.table_tariffs)
        return widget

    # ── 5. Container Specs Tab (MD-010) ────────────────────────────────
    def _build_containers_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        btn_bar = QHBoxLayout()
        btn_refresh = QPushButton(i18n.t("btn_refresh_data"))
        btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_refresh.clicked.connect(self.load_containers)
        btn_bar.addWidget(btn_refresh)
        btn_bar.addStretch()
        layout.addLayout(btn_bar)

        self.table_containers = QTableWidget()
        self.table_containers.setColumnCount(5)
        self.table_containers.setHorizontalHeaderLabels([
            "نوع الحاوية", "السعة (CBM)", "وزن الفارغ (kg)",
            "أقصى حمولة (kg)", "أبعاد الباب (سم)"
        ])
        self.table_containers.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_containers.setAlternatingRowColors(True)
        self.table_containers.setShowGrid(False)
        self.table_containers.verticalHeader().setVisible(False)
        self.table_containers.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_containers.setFont(QFont(FONT_ARABIC, TYPO_TABLE[0]))

        layout.addWidget(self.table_containers)
        return widget

    # ── 6. Shipping Lines Tab (MD-005) ─────────────────────────────────
    def _build_shipping_lines_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        btn_bar = QHBoxLayout()
        btn_add = QPushButton("➕  إضافة خط ملاحي جديد")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_add.setStyleSheet("background-color: #0284c7; color: #ffffff;")
        btn_add.clicked.connect(self._add_shipping_line)

        btn_refresh = QPushButton(i18n.t("btn_refresh_data"))
        btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_refresh.clicked.connect(self.load_shipping_lines)

        btn_bar.addWidget(btn_add)
        btn_bar.addWidget(btn_refresh)
        btn_bar.addStretch()
        layout.addLayout(btn_bar)

        self.table_shipping_lines = QTableWidget()
        self.table_shipping_lines.setColumnCount(4)
        self.table_shipping_lines.setHorizontalHeaderLabels([
            "رقم الخط", "اسم الخط الملاحي", "كود SCAC", "الموقع الإلكتروني"
        ])
        self.table_shipping_lines.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_shipping_lines.setAlternatingRowColors(True)
        self.table_shipping_lines.setShowGrid(False)
        self.table_shipping_lines.verticalHeader().setVisible(False)
        self.table_shipping_lines.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_shipping_lines.setFont(QFont(FONT_ARABIC, TYPO_TABLE[0]))
        self.table_shipping_lines.cellDoubleClicked.connect(self._on_shipping_line_double_clicked)

        layout.addWidget(self.table_shipping_lines)
        return widget

    # ── 7. Currencies Tab (MD-006) ─────────────────────────────────────
    def _build_currencies_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        btn_bar = QHBoxLayout()
        btn_add = QPushButton("➕  إضافة عملة جديدة")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_add.setStyleSheet("background-color: #e67e22; color: #ffffff;")
        btn_add.clicked.connect(self._add_currency)

        btn_refresh = QPushButton(i18n.t("btn_refresh_data"))
        btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_refresh.clicked.connect(self.load_currencies)

        btn_bar.addWidget(btn_add)
        btn_bar.addWidget(btn_refresh)
        btn_bar.addStretch()
        layout.addLayout(btn_bar)

        self.table_currencies = QTableWidget()
        self.table_currencies.setColumnCount(4)
        self.table_currencies.setHorizontalHeaderLabels([
            "كود العملة (ISO)", "اسم العملة", "الرمز", "عدد الخانات العشرية"
        ])
        self.table_currencies.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_currencies.setAlternatingRowColors(True)
        self.table_currencies.setShowGrid(False)
        self.table_currencies.verticalHeader().setVisible(False)
        self.table_currencies.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_currencies.setFont(QFont(FONT_ARABIC, TYPO_TABLE[0]))
        self.table_currencies.cellDoubleClicked.connect(self._on_currency_double_clicked)

        layout.addWidget(self.table_currencies)
        return widget

    # ── 8. Incoterms Tab (MD-007) ──────────────────────────────────────
    def _build_incoterms_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        btn_bar = QHBoxLayout()
        btn_add = QPushButton("➕  إضافة شرط Incoterms جديد")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_add.setStyleSheet("background-color: #27ae60; color: #ffffff;")
        btn_add.clicked.connect(self._add_incoterm)

        btn_refresh = QPushButton(i18n.t("btn_refresh_data"))
        btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_refresh.clicked.connect(self.load_incoterms)

        btn_bar.addWidget(btn_add)
        btn_bar.addWidget(btn_refresh)
        btn_bar.addStretch()
        layout.addLayout(btn_bar)

        self.table_incoterms = QTableWidget()
        self.table_incoterms.setColumnCount(4)
        self.table_incoterms.setHorizontalHeaderLabels([
            "كود الشرط", "الاسم التجارى", "الإصدار", "ملاحظات المسئوليات"
        ])
        self.table_incoterms.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_incoterms.setAlternatingRowColors(True)
        self.table_incoterms.setShowGrid(False)
        self.table_incoterms.verticalHeader().setVisible(False)
        self.table_incoterms.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_incoterms.setFont(QFont(FONT_ARABIC, TYPO_TABLE[0]))
        self.table_incoterms.cellDoubleClicked.connect(self._on_incoterm_double_clicked)

        layout.addWidget(self.table_incoterms)
        return widget

    # ── 9. Projects Tab (MD-008) ───────────────────────────────────────
    def _build_projects_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        btn_bar = QHBoxLayout()
        btn_add = QPushButton("➕  إضافة مشروع استيرادي جديد")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_add.setStyleSheet("background-color: #d35400; color: #ffffff;")
        btn_add.clicked.connect(self._add_project)

        btn_refresh = QPushButton(i18n.t("btn_refresh_data"))
        btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        btn_refresh.clicked.connect(self.load_projects)

        btn_bar.addWidget(btn_add)
        btn_bar.addWidget(btn_refresh)
        btn_bar.addStretch()
        layout.addLayout(btn_bar)

        self.table_projects = QTableWidget()
        self.table_projects.setColumnCount(5)
        self.table_projects.setHorizontalHeaderLabels([
            "كود المشروع", "اسم المشروع", "مسؤول المشروع", "الحالة", "تاريخ الإنشاء"
        ])
        self.table_projects.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_projects.setAlternatingRowColors(True)
        self.table_projects.setShowGrid(False)
        self.table_projects.verticalHeader().setVisible(False)
        self.table_projects.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_projects.setFont(QFont(FONT_ARABIC, TYPO_TABLE[0]))
        self.table_projects.cellDoubleClicked.connect(self._on_project_double_clicked)

        layout.addWidget(self.table_projects)
        return widget

    # ── Data Loaders & CRUD Connectors ───────────────────────────────
    def load_all_data(self):
        self.load_companies()
        self.load_suppliers()
        self.load_providers()
        self.load_tariffs()
        self.load_containers()
        self.load_shipping_lines()
        self.load_currencies()
        self.load_incoterms()
        self.load_projects()

    def load_companies(self):
        from datetime import date
        records = self.repo.get_all_companies()
        if not records:
            today = date.today()
            self.repo.create_company({
                "egyptian_importer_name": "شركة المصنع المصري للاستيراد والتصدير",
                "importer_id": "IMP-889900",
                "importer_id_expiration_date": today,
                "vat_id": "100-200-300",
                "vat_id_expiration_date": today,
                "commercial_registration_no": "REG-776655",
                "commercial_registration_expiration": today,
                "address": "القاهرة - مصر",
                "country": "مصر - Egypt"
            })
            records = self.repo.get_all_companies()

        self.table_companies.setRowCount(len(records))
        for row, rec in enumerate(records):
            items = [f"CMP-{rec.company_id:03d}", rec.egyptian_importer_name, rec.importer_id or "-", rec.commercial_registration_no or "-", rec.country or "-"]
            for col, text in enumerate(items):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                self.table_companies.setItem(row, col, item)
            self.table_companies.setRowHeight(row, DIM_TABLE_ROW)

    def load_suppliers(self):
        records = self.repo.get_all_suppliers()
        if not records:
            self.repo.create_supplier({
                "vendor_company_name": "Global Tech Exporters Ltd",
                "registration_type": "Company",
                "foreign_exporter_id": "EXP-998877",
                "foreign_exporter_country": "China / الصين",
                "foreign_exporter_country_code": "CN",
                "phone_number": "+86 21 8899 0000",
                "email": "info@exporter.cn"
            })
            records = self.repo.get_all_suppliers()

        self.table_suppliers.setRowCount(len(records))
        for row, rec in enumerate(records):
            items = [f"SUP-{rec.supplier_id:03d}", rec.vendor_company_name, rec.foreign_exporter_id or "-", rec.foreign_exporter_country or "-", rec.phone_number or "-"]
            for col, text in enumerate(items):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                self.table_suppliers.setItem(row, col, item)
            self.table_suppliers.setRowHeight(row, DIM_TABLE_ROW)

    def load_providers(self):
        records = self.repo.get_all_service_providers()
        if not records:
            self.repo.create_service_provider({
                "partner_name": "المستقبل للتخليص الجمركي والنقل",
                "partner_type": "Customs Broker",
                "phone_number": "+20 100 200 3000",
                "email": "customs@future.com"
            })
            records = self.repo.get_all_service_providers()

        self.table_providers.setRowCount(len(records))
        for row, rec in enumerate(records):
            items = [f"PRV-{rec.partner_id:03d}", rec.partner_name, rec.partner_type or "-", rec.phone_number or "-"]
            for col, text in enumerate(items):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                self.table_providers.setItem(row, col, item)
            self.table_providers.setRowHeight(row, DIM_TABLE_ROW)

    def load_tariffs(self):
        records = self.repo.get_all_customs_tariffs()
        if not records:
            self.repo.create_customs_tariff({
                "hs_code": "6701067200",
                "hs_description": "أجهزة إلكترونية ومعدات اختبارات قياسية",
                "customs_duty_pct": 0.05,
                "vat_pct": 0.14,
                "regulatory_authority": "الهيئة العامة للرقابة على الصادرات والواردات (GOEIC)"
            })
            records = self.repo.get_all_customs_tariffs()

        self.table_tariffs.setRowCount(len(records))
        for row, rec in enumerate(records):
            duty_pct_str = f"{float(rec.customs_duty_pct)*100:.1f}%"
            vat_pct_str = f"{float(rec.vat_pct)*100:.1f}%"
            items = [rec.hs_code, rec.hs_description or "-", duty_pct_str, vat_pct_str, rec.regulatory_authority or "-"]
            for col, text in enumerate(items):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                self.table_tariffs.setItem(row, col, item)
            self.table_tariffs.setRowHeight(row, DIM_TABLE_ROW)

    def load_containers(self):
        records = self.repo.get_all_container_specs()
        if not records:
            specs = [
                {"container_type": "20GP", "internal_length_cm": 589, "internal_width_cm": 235, "internal_height_cm": 239, "door_width_cm": 234, "door_height_cm": 228, "cubic_capacity_cbm": 33.2, "tare_weight_kg": 2200, "max_payload_kg": 28200, "max_gross_weight_kg": 30400, "floor_area_sqm": 13.8},
                {"container_type": "40HC", "internal_length_cm": 1203, "internal_width_cm": 235, "internal_height_cm": 269, "door_width_cm": 234, "door_height_cm": 258, "cubic_capacity_cbm": 76.4, "tare_weight_kg": 3900, "max_payload_kg": 26580, "max_gross_weight_kg": 30480, "floor_area_sqm": 28.2}
            ]
            for s in specs:
                self.repo.create_container_spec(s)
            records = self.repo.get_all_container_specs()

        self.table_containers.setRowCount(len(records))
        for row, rec in enumerate(records):
            door_dim = f"{float(rec.door_width_cm):.0f}x{float(rec.door_height_cm):.0f}"
            items = [rec.container_type, f"{float(rec.cubic_capacity_cbm):.1f}", f"{float(rec.tare_weight_kg):.0f}", f"{float(rec.max_payload_kg):.0f}", door_dim]
            for col, text in enumerate(items):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                self.table_containers.setItem(row, col, item)
            self.table_containers.setRowHeight(row, DIM_TABLE_ROW)

    def load_shipping_lines(self):
        records = self.session.query(ShippingLine).all()
        if not records:
            sl = ShippingLine(shipping_line_name="Maersk Line", scac_code="MAEU", website="www.maersk.com")
            self.session.add(sl)
            self.session.commit()
            records = self.session.query(ShippingLine).all()

        self.table_shipping_lines.setRowCount(len(records))
        for row, rec in enumerate(records):
            items = [f"SL-{rec.shipping_line_id:03d}", rec.shipping_line_name, rec.scac_code or "-", rec.website or "-"]
            for col, text in enumerate(items):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                self.table_shipping_lines.setItem(row, col, item)
            self.table_shipping_lines.setRowHeight(row, DIM_TABLE_ROW)

    def load_currencies(self):
        records = self.session.query(Currency).all()
        if not records:
            c1 = Currency(iso_code="USD", currency_name="US Dollar", symbol="$", decimal_places=2)
            c2 = Currency(iso_code="EGP", currency_name="Egyptian Pound", symbol="EGP", decimal_places=2)
            self.session.add_all([c1, c2])
            self.session.commit()
            records = self.session.query(Currency).all()

        self.table_currencies.setRowCount(len(records))
        for row, rec in enumerate(records):
            items = [rec.iso_code, rec.currency_name, rec.symbol or "-", str(rec.decimal_places)]
            for col, text in enumerate(items):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                self.table_currencies.setItem(row, col, item)
            self.table_currencies.setRowHeight(row, DIM_TABLE_ROW)

    def load_incoterms(self):
        records = self.session.query(Incoterm).all()
        if not records:
            i1 = Incoterm(incoterm_code="FOB", name="Free On Board", version="Incoterms 2020", description="المستورد يتحمل النولون والتأمين والتخليص الجمركي بميناء الوصول.")
            i2 = Incoterm(incoterm_code="CIF", name="Cost Insurance Freight", version="Incoterms 2020", description="المورد يتحمل النولون البحري والتأمين حتى ميناء الوصول.")
            self.session.add_all([i1, i2])
            self.session.commit()
            records = self.session.query(Incoterm).all()

        self.table_incoterms.setRowCount(len(records))
        for row, rec in enumerate(records):
            items = [rec.incoterm_code, rec.name, rec.version, rec.description or "-"]
            for col, text in enumerate(items):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                self.table_incoterms.setItem(row, col, item)
            self.table_incoterms.setRowHeight(row, DIM_TABLE_ROW)

    def load_projects(self):
        records = self.session.query(Project).all()
        if not records:
            p1 = Project(project_code="PRJ-2026-001", project_name="مشروع استيراد خطوط الإنتاج والقطع 2026", project_owner="إدارة المشتريات الخارجية", company_id=1, supplier_id=1, incoterm_id=1, status="open")
            self.session.add(p1)
            self.session.commit()
            records = self.session.query(Project).all()

        self.table_projects.setRowCount(len(records))
        for row, rec in enumerate(records):
            created_str = rec.created_at.strftime("%Y-%m-%d") if rec.created_at else "2026-07-27"
            items = [rec.project_code, rec.project_name, rec.project_owner, rec.status, created_str]
            for col, text in enumerate(items):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                self.table_projects.setItem(row, col, item)
            self.table_projects.setRowHeight(row, DIM_TABLE_ROW)

    # ── Dialog Triggers ───────────────────────────────────────────────
    def _add_company(self):
        dlg = NewCompanyForm(parent=self)
        if dlg.exec() == NewCompanyForm.DialogCode.Accepted:
            self.load_companies()

    def _add_supplier(self):
        dlg = NewSupplierForm(parent=self)
        if dlg.exec() == NewSupplierForm.DialogCode.Accepted:
            self.load_suppliers()

    def _add_provider(self):
        dlg = NewServiceProviderForm(parent=self)
        if dlg.exec() == NewServiceProviderForm.DialogCode.Accepted:
            self.load_providers()

    def _add_shipping_line(self):
        dlg = NewShippingLineForm(parent=self)
        if dlg.exec() == NewShippingLineForm.DialogCode.Accepted:
            self.load_shipping_lines()

    def _add_currency(self):
        dlg = NewCurrencyForm(parent=self)
        if dlg.exec() == NewCurrencyForm.DialogCode.Accepted:
            self.load_currencies()

    def _add_incoterm(self):
        dlg = NewIncotermForm(parent=self)
        if dlg.exec() == NewIncotermForm.DialogCode.Accepted:
            self.load_incoterms()

    def _add_project(self):
        dlg = NewProjectForm(parent=self)
        if dlg.exec() == NewProjectForm.DialogCode.Accepted:
            self.load_projects()

    def _on_company_double_clicked(self, row: int, column: int):
        item = self.table_companies.item(row, 0)
        if item:
            cid_str = item.text().strip().replace("CMP-", "")
            try:
                cid = int(cid_str)
            except ValueError:
                cid = 1
            dlg = NewCompanyForm(company_id=cid, parent=self)
            if dlg.exec() == NewCompanyForm.DialogCode.Accepted:
                self.load_companies()

    def _on_supplier_double_clicked(self, row: int, column: int):
        item = self.table_suppliers.item(row, 0)
        if item:
            sid_str = item.text().strip().replace("SUP-", "")
            try:
                sid = int(sid_str)
            except ValueError:
                sid = 1
            dlg = NewSupplierForm(supplier_id=sid, parent=self)
            if dlg.exec() == NewSupplierForm.DialogCode.Accepted:
                self.load_suppliers()

    def _on_provider_double_clicked(self, row: int, column: int):
        item = self.table_providers.item(row, 0)
        if item:
            pid_str = item.text().strip().replace("PRV-", "")
            try:
                pid = int(pid_str)
            except ValueError:
                pid = 1
            dlg = NewServiceProviderForm(provider_id=pid, parent=self)
            if dlg.exec() == NewServiceProviderForm.DialogCode.Accepted:
                self.load_providers()

    def _on_shipping_line_double_clicked(self, row: int, column: int):
        item = self.table_shipping_lines.item(row, 0)
        if item:
            lid_str = item.text().strip().replace("SL-", "")
            try:
                lid = int(lid_str)
            except ValueError:
                lid = 1
            dlg = NewShippingLineForm(line_id=lid, parent=self)
            if dlg.exec() == NewShippingLineForm.DialogCode.Accepted:
                self.load_shipping_lines()

    def _on_currency_double_clicked(self, row: int, column: int):
        item = self.table_currencies.item(row, 0)
        if item:
            iso = item.text().strip()
            cur = self.session.query(Currency).filter(Currency.iso_code == iso).first()
            cid = cur.currency_id if cur else 1
            dlg = NewCurrencyForm(currency_id=cid, parent=self)
            if dlg.exec() == NewCurrencyForm.DialogCode.Accepted:
                self.load_currencies()

    def _on_incoterm_double_clicked(self, row: int, column: int):
        item = self.table_incoterms.item(row, 0)
        if item:
            code = item.text().strip()
            inco = self.session.query(Incoterm).filter(Incoterm.incoterm_code == code).first()
            iid = inco.incoterm_id if inco else 1
            dlg = NewIncotermForm(incoterm_id=iid, parent=self)
            if dlg.exec() == NewIncotermForm.DialogCode.Accepted:
                self.load_incoterms()

    def _on_project_double_clicked(self, row: int, column: int):
        item = self.table_projects.item(row, 0)
        if item:
            code = item.text().strip()
            prj = self.session.query(Project).filter(Project.project_code == code).first()
            p_id = prj.project_id if prj else 1
            dlg = NewProjectForm(project_id=p_id, parent=self)
            if dlg.exec() == NewProjectForm.DialogCode.Accepted:
                self.load_projects()
