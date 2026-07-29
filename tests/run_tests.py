import sys
import os
from datetime import date

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.database.session import SessionLocal, init_db
from src.database.models import Company, Supplier, AuditLog
from src.services.audit_service import AuditService

def run():
    print("Initializing Database...")
    init_db()
    session = SessionLocal()

    print("Testing Company Creation (MD-001)...")
    company = Company(
        egyptian_importer_name="شركة الاستيراد المصرية ش.م.م",
        address="15 شارع التحرير، القاهرة",
        country="Egypt",
        importer_id="IMP-EG-998877",
        importer_id_expiration_date=date(2028, 12, 31),
        vat_id="VAT-99887766",
        vat_id_expiration_date=date(2029, 6, 30),
        commercial_registration_no="CR-554433",
        commercial_registration_expiration=date(2027, 5, 15),
        status="active"
    )
    session.add(company)
    session.commit()

    saved_company = session.query(Company).filter_by(importer_id="IMP-EG-998877").first()
    assert saved_company is not None
    print(f"✅ Saved Company ID: {saved_company.company_id} - Name: {saved_company.egyptian_importer_name}")

    print("Testing Audit Log Service (GP-004)...")
    audit_entry = AuditService.log_action(
        session=session,
        table_name="companies",
        record_id=saved_company.company_id,
        action="create",
        screen_name="MD-001 Company Setup",
        change_summary="Created company Egyptian Importer"
    )

    assert audit_entry.audit_log_id is not None
    print(f"✅ Audit Log Entry Created ID: {audit_entry.audit_log_id} Action: {audit_entry.action}")

    history = AuditService.get_history_for_record(session, "companies", saved_company.company_id)
    assert len(history) >= 1
    print(f"✅ Audit History Count: {len(history)} entries found for company record.")

    session.close()
    print("\n🎉 All Sprint 1 Database & Audit Tests Passed Successfully!")

if __name__ == "__main__":
    run()
