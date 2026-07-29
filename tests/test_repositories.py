"""
Unit Tests for Database Repositories
Tests MasterDataRepository, ImportFileRepository, and PaymentRepository CRUD operations.
"""

from datetime import date
from src.database.session import SessionLocal
from src.database.repositories.master_data_repository import MasterDataRepository
from src.database.repositories.import_file_repository import ImportFileRepository
from src.database.repositories.payment_repository import PaymentRepository


def test_import_file_repository_crud():
    session = SessionLocal()
    repo = ImportFileRepository(session)

    file_id = repo.generate_next_file_id()
    assert file_id.startswith("IMP-2026-")

    data = {
        "project_name": "مشروع اختبار الرفوف",
        "company_name": "شركة الاختيار للتوريدات",
        "supplier_name": "Tech Exporters Co.",
        "freight_mode": "Ocean FCL",
        "stage": "1. PO Received"
    }
    file_obj = repo.create_import_file(data)
    assert file_obj.import_file_id == file_id
    assert file_obj.stage == "1. PO Received"

    session.close()


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


def test_master_data_repository_full_crud():
    today = date.today()
    session = SessionLocal()
    repo = MasterDataRepository(session)

    # Company
    c = repo.create_company({
        "egyptian_importer_name": "شركة النيل للاستيراد السريع",
        "importer_id": "IMP-MOD-101",
        "importer_id_expiration_date": today,
        "vat_id": "111-222-333",
        "vat_id_expiration_date": today,
        "commercial_registration_no": "REG-8899",
        "commercial_registration_expiration": today,
        "address": "القاهرة",
        "country": "مصر"
    })
    assert c.company_id is not None

    # Supplier
    s = repo.create_supplier({
        "vendor_company_name": "Global Test Exporters Ltd",
        "registration_type": "Company",
        "foreign_exporter_id": "EXP-MOD-101",
        "foreign_exporter_country": "Germany",
        "foreign_exporter_country_code": "DE",
        "phone_number": "+49 30 123456"
    })
    assert s.supplier_id is not None

    # Service Provider
    p = repo.create_service_provider({
        "partner_name": "الفرع المتقدم للتخليص",
        "partner_type": "Customs Broker",
        "phone_number": "+20 100 000 1111"
    })
    assert p.partner_id is not None

    session.close()
