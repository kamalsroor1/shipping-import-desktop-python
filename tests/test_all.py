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
from src.services.loading_calculator import LoadingCalculationEngine
from src.services.shipping_scenario_service import ShippingScenarioEvaluator
from src.services.acid_service import ACIDVerificationService
from src.services.document_approval_service import DocumentDualApprovalManager
from src.services.electronic_exchange_service import ElectronicDocumentExchangeService

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


# ── 2. Container Loading Optimization Tests (BP-005) ────────────────
def test_loading_calculator_fit_status():
    res = LoadingCalculationEngine.evaluate_container_fit(total_cbm=45.0, total_gross_weight_kg=15000.0, container_type="40HC")
    assert res["status"] == "Fit"
    assert res["space_utilization_pct"] > 0
    assert res["door_clearance_passed"] is True


def test_loading_calculator_overweight():
    res = LoadingCalculationEngine.evaluate_container_fit(total_cbm=45.0, total_gross_weight_kg=30000.0, container_type="40HC")
    assert res["status"] == "Overweight"


# ── 3. Shipping Scenario Evaluator Tests (BP-007) ───────────────────
def test_shipping_scenario_evaluator_lead_times():
    crd = date(2026, 8, 1)
    opts = [
        {"provider_name": "Maersk", "vessel_name": "MSC Luna", "sailing_date": date(2026, 8, 5), "arrival_date": date(2026, 8, 25), "expected_line_delay_days": 2},
        {"provider_name": "CMA CGM", "vessel_name": "CMA Marco Polo", "sailing_date": date(2026, 8, 3), "arrival_date": date(2026, 8, 20), "expected_line_delay_days": 1}
    ]
    res = ShippingScenarioEvaluator.evaluate_all_scenarios(crd, opts, avg_form4_days=3, avg_clearance_days=4)
    assert res["total_options_evaluated"] == 2
    assert "average_expected_arrival_date" in res
    assert res["recommended_scenario"]["provider_name"] == "CMA CGM"


# ── 4. ACID Verification Tests (BP-014) ──────────────────────────────
def test_acid_verification_matching():
    system_data = {
        "importer_tax_id": "999-888-777",
        "foreign_exporter_id": "EXP-CN-100",
        "exporter_country_code": "CN",
        "proforma_invoice_no": "PI-2026-100",
        "shipping_port_locode": "CNSHA"
    }
    acid_data = {
        "acid_number": "EG-2026-999888777",
        "importer_tax_id": "999-888-777",
        "foreign_exporter_id": "EXP-CN-100",
        "exporter_country_code": "CN",
        "proforma_invoice_no": "PI-2026-100",
        "shipping_port_locode": "CNSHA"
    }
    res = ACIDVerificationService.verify_acid_certificate(system_data, acid_data)
    assert res["verification_status"] == "Verified"
    assert res["is_ready_for_booking"] is True


# ── 5. Dual Document Approval Tests (BP-019) ─────────────────────────
def test_document_dual_approval_workflow():
    res1 = DocumentDualApprovalManager.process_approval("Commercial Invoice", importer_approved=True, broker_approved=False)
    assert res1["status"] == "Pending Broker Approval"
    assert res1["is_final"] is False

    res2 = DocumentDualApprovalManager.process_approval("Commercial Invoice", importer_approved=True, broker_approved=True)
    assert res2["status"] == "Final Approved"
    assert res2["is_final"] is True


# ── 6. Electronic Document Exchange Tests (BP-021) ───────────────────
def test_electronic_document_exchange_validation():
    doc_fields = {
        "shipper_name": "Global Exporter Ltd",
        "egyptian_importer_tax_id": "999-888-777",
        "acid_number": "EG-2026-999888777",
        "currency": "USD",
        "number_of_packages": "500",
        "hs_code": "6701067200",
        "invoice_grand_total": "50000.00",
        "country_of_origin": "China",
        "bill_of_lading_number": "BL-123456"
    }
    res = ElectronicDocumentExchangeService.validate_for_upload(doc_fields, "CargoX")
    assert res["ready_for_upload"] is True
    assert res["upload_status"] == "Ready for Upload"


# ── 7. Duties Estimator Service Tests (BP-008) ───────────────────────
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


# ── 8. Import File Repository CRUD Tests (BP-001 - BP-005) ─────────────
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


# ── 9. Master Data Repository CRUD & Advanced Models (MD-001 - MD-008) ─
def test_master_data_repository_crud():
    today = date.today()
    session = SessionLocal()
    repo = MasterDataRepository(session)

    # Company Test
    c_data = {
        "egyptian_importer_name": "شركة النيل للاستيراد والتصدير السريع",
        "importer_id": "IMP-ALL-9999",
        "importer_id_expiration_date": today,
        "vat_id": "999-888-7779",
        "vat_id_expiration_date": today,
        "commercial_registration_no": "REG-123459",
        "commercial_registration_expiration": today,
        "address": "القاهرة - مصر",
        "country": "مصر - Egypt"
    }
    comp = repo.create_company(c_data)
    assert comp.company_id is not None

    # Supplier Test
    s_data = {
        "vendor_company_name": "Shenzhen Electric All Test Ltd 999",
        "registration_type": "Company",
        "foreign_exporter_id": "EXP-ALL-9999",
        "foreign_exporter_country": "China",
        "foreign_exporter_country_code": "CN",
        "phone_number": "+86 755 8899 0000",
        "email": "contact@szel.cn"
    }
    supp = repo.create_supplier(s_data)
    assert supp.supplier_id is not None

    session.close()


# ── 10. Pure i18n Translation Engine Tests ─────────────────────────────
def test_i18n_manager():
    i18n.set_language("ar")
    assert i18n.t("app_name") == "نظام إدارة الاستيراد"

    i18n.set_language("en")
    assert i18n.t("app_name") == "Import Management System"

    i18n.set_language("ar")


# ── 11. Report Exporters Tests (Excel & PDF) ───────────────────────────
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
