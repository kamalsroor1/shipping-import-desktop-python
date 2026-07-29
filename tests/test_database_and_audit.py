import pytest
from datetime import date
from src.database.session import SessionLocal, init_db
from src.database.models import Company, Supplier, AuditLog
from src.services.audit_service import AuditService

@pytest.fixture(scope="module")
def setup_db():
    init_db()
    session = SessionLocal()
    yield session
    session.close()

def test_database_initialization_and_company_creation(setup_db):
    session = setup_db

    company = Company(
        egyptian_importer_name="شركة الاستيراد المصرية ش.م.م",
        address="15 شارع التحرير، القاهرة",
        country="Egypt",
        importer_id="IMP-EG-12345",
        importer_id_expiration_date=date(2028, 12, 31),
        vat_id="VAT-99887766",
        vat_id_expiration_date=date(2029, 6, 30),
        commercial_registration_no="CR-554433",
        commercial_registration_expiration=date(2027, 5, 15),
        status="active"
    )
    session.add(company)
    session.commit()

    saved_company = session.query(Company).filter_by(importer_id="IMP-EG-12345").first()
    assert saved_company is not None
    assert saved_company.egyptian_importer_name == "شركة الاستيراد المصرية ش.م.م"

    # Test Audit Log (GP-004)
    audit_entry = AuditService.log_action(
        session=session,
        table_name="companies",
        record_id=saved_company.company_id,
        action="create",
        screen_name="MD-001 Company Setup",
        change_summary="Created company Egyptian Importer"
    )

    assert audit_entry.audit_log_id is not None
    assert audit_entry.action == "create"

    history = AuditService.get_history_for_record(session, "companies", saved_company.company_id)
    assert len(history) >= 1
    assert history[0].table_name == "companies"
