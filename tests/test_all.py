"""
Master Comprehensive Test Suite (test_all.py)
Executes unit tests across all domain services, ORM repositories, exporters, and i18n modules.
"""

import pytest
import os
import tempfile
from datetime import date

from src.services.cbm_calculator import CBMCalculator
from src.services.duties_estimator import DutiesEstimator
from src.utils.i18n import i18n
from src.utils.export import ExcelReportExporter, PDFReportExporter

from src.database.session import SessionLocal, engine, Base
from src.database.repositories.master_data_repository import MasterDataRepository
from src.database.repositories.import_file_repository import ImportFileRepository
from src.database.repositories.payment_repository import PaymentRepository
from src.database.models import (
    ShippingLine, Currency, Incoterm, Project,
    FreightQuotation, CustomsDocumentChecklist
)


# Ensure database tables exist before running ORM tests
Base.metadata.create_all(bind=engine)


# ── 1. CBM Calculator Service Tests (BP-004) ─────────────────────────
def test_cbm_calculator_ocean():
    cbm = CBMCalculator.calculate_item_cbm(10, 100, 100, 100)
    assert cbm == 10.0


def test_cbm_calculator_air_chargeable_weight():
    air_wt = CBMCalculator.calculate_air_chargeable_weight(10, 100, 100, 100, 500.0)
    assert pytest.approx(air_wt, 0.01) == 1666.67


# ── 2. Duties Estimator Service Tests (BP-008) ───────────────────────
def test_duties_estimator():
    res = DutiesEstimator.calculate_hs_duties(
        amount=10000.0,
        customs_duty_pct=0.05,
        vat_pct=0.14,
        exchange_rate=48.50
    )
    assert res['invoice_amount_egp'] == 485000.0
    assert res['customs_duty_amount'] == 24250.0
    assert res['vat_amount'] == 71295.0
    assert res['total_estimated_import_cost'] == 580545.0


# ── 3. Import File Repository CRUD Tests (BP-001 - BP-005) ─────────────
def test_import_file_repository_crud():
    session = SessionLocal()
    repo = ImportFileRepository(session)

    file_id = repo.generate_next_file_id()
    assert file_id.startswith("IMP-2026-")

    data = {
        "project_name": "مشروع توريد ومعدات اختبار",
        "company_name": "شركة الاختيار الفني",
        "supplier_name": "Global Tech Co",
        "freight_mode": "Ocean FCL",
        "stage": "1. PO Received"
    }
    file_obj = repo.create_import_file(data)
    assert file_obj.import_file_id == file_id
    session.close()


# ── 4. Payment Repository CRUD Tests (BP-009) ─────────────────────────
def test_payment_repository_crud():
    session = SessionLocal()
    repo = PaymentRepository(session)

    req_id = repo.generate_next_request_id()
    assert req_id.startswith("PAY-2026-")

    pay_data = {
        "import_file_id": "IMP-2026-0001",
        "beneficiary_name": "Test Beneficiary Ltd",
        "payment_type": "Advance Payment",
        "requested_amount_usd": 12500.0,
        "swift_code": "TESTSWIFT100",
        "status": "⏳ قيد المعالجة"
    }
    pay_obj = repo.create_payment_request(pay_data)
    assert pay_obj.request_id == req_id
    assert pay_obj.requested_amount_usd == 12500.0
    session.close()


# ── 5. Master Data Repository CRUD & Advanced Models (MD-001 - MD-008) ─
def test_master_data_repository_crud():
    today = date.today()
    session = SessionLocal()
    repo = MasterDataRepository(session)

    # Company Test
    c_data = {
        "egyptian_importer_name": "شركة النيل للاستيراد والتصدير الاختباري السريع",
        "importer_id": "IMP-ALL-999",
        "importer_id_expiration_date": today,
        "vat_id": "999-888-777",
        "vat_id_expiration_date": today,
        "commercial_registration_no": "REG-12345",
        "commercial_registration_expiration": today,
        "address": "القاهرة - مصر",
        "country": "مصر - Egypt"
    }
    comp = repo.create_company(c_data)
    assert comp.company_id is not None

    # Supplier Test
    s_data = {
        "vendor_company_name": "Shenzhen Electric All Test Ltd",
        "registration_type": "Company",
        "foreign_exporter_id": "EXP-ALL-999",
        "foreign_exporter_country": "China",
        "foreign_exporter_country_code": "CN",
        "phone_number": "+86 755 8899 0000",
        "email": "contact@szel.cn"
    }
    supp = repo.create_supplier(s_data)
    assert supp.supplier_id is not None

    # Service Provider Test
    p_data = {
        "partner_name": "الشرق الأوسط للتخليص الجمركي والاختبار التام",
        "partner_type": "Customs Broker",
        "phone_number": "+20 122 333 4444",
        "email": "info@customs.eg"
    }
    prv = repo.create_service_provider(p_data)
    assert prv.partner_id is not None

    # MD-005 Shipping Line Test
    sl = ShippingLine(shipping_line_name="CMA CGM Test Line", scac_code="CMDU", website="www.cma-cgm.com")
    session.add(sl)

    # MD-006 Currency Test
    cur = Currency(iso_code="JPY", currency_name="Japanese Yen", symbol="¥", decimal_places=0)
    session.add(cur)

    # MD-007 Incoterm Test
    inco = Incoterm(incoterm_code="CPT", name="Carriage Paid To", version="Incoterms 2020")
    session.add(inco)

    # BP-006 Freight Quotation Test
    fq = FreightQuotation(import_file_id="IMP-2026-0001", carrier_name="Evergreen Line", port_of_loading="Yantian", port_of_discharge="Damietta", freight_cost_usd=2400.0)
    session.add(fq)

    # BP-007 Customs Checklist Test
    chk = CustomsDocumentChecklist(import_file_id="IMP-2026-0001", document_type="Certificate of Origin", status="Approved")
    session.add(chk)

    session.commit()
    assert sl.shipping_line_id is not None
    assert cur.iso_code == "JPY"
    assert inco.incoterm_code == "CPT"
    assert fq.quotation_id is not None
    assert chk.checklist_id is not None

    session.close()


# ── 6. Pure i18n Translation Engine Tests ──────────────────────────────
def test_i18n_manager():
    i18n.set_language("ar")
    assert i18n.t("app_name") == "نظام إدارة الاستيراد"

    i18n.set_language("en")
    assert i18n.t("app_name") == "Import Management System"

    i18n.set_language("ar")


# ── 7. Report Exporters Tests (Excel & PDF) ───────────────────────────
def test_report_exporters():
    temp_dir = tempfile.gettempdir()
    excel_path = os.path.join(temp_dir, "test_out.xlsx")
    pdf_path = os.path.join(temp_dir, "test_out.pdf")

    sample_files = [{
        "import_file_id": "IMP-2026-0001", "project_name": "Test", "company_name": "Test Co",
        "supplier_name": "Test Sup", "freight_mode": "Ocean FCL", "total_cbm": 10.0, "stage": "PO"
    }]
    ExcelReportExporter.export_import_files(excel_path, sample_files)
    assert os.path.exists(excel_path)

    duties_res = {
        "invoice_amount_egp": 485000.0, "customs_duty_amount": 24250.0,
        "vat_amount": 71295.0, "total_estimated_import_cost": 580545.0
    }
    PDFReportExporter.generate_duties_summary_pdf(pdf_path, 10000.0, 48.50, duties_res)
    assert os.path.exists(pdf_path)

    os.remove(excel_path)
    os.remove(pdf_path)
