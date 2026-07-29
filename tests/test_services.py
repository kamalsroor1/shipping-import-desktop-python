import os
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.services.cbm_calculator import CBMCalculator
from src.services.duties_estimator import DutiesEstimator
from src.services.master_data_service import MasterDataService
from src.database.session import SessionLocal, init_db
from src.database.models import Company, Supplier

def run_tests():
    print("--- Running Business Logic & Services Unit Tests ---")

    # 1. CBM Calculator Tests
    cbm = CBMCalculator.calculate_item_cbm(qty=100, length_cm=50, width_cm=40, height_cm=30)
    print(f"✅ Ocean CBM (100 pkgs x 50x40x30 cm): {cbm} CBM (Expected: 6.0 CBM)")
    assert cbm == 6.0

    air_weight = CBMCalculator.calculate_air_chargeable_weight(qty=100, length_cm=50, width_cm=40, height_cm=30, gross_weight_kg=800)
    print(f"✅ Air Chargeable Weight: {air_weight} kg (Expected: 1000.0 kg vs 800 kg gross)")
    assert air_weight == 1000.0

    # 2. Duties Estimator Tests
    duties = DutiesEstimator.calculate_hs_duties(
        amount=10000.0,
        customs_duty_pct=0.10,  # 10% duty
        vat_pct=0.14,            # 14% VAT
        exchange_rate=50.0       # 50 EGP per USD
    )
    print(f"✅ Duties Breakdown: Invoice EGP={duties['invoice_amount_egp']}, Duty={duties['customs_duty_amount']}, VAT={duties['vat_amount']}, Total Duties={duties['total_estimated_duties']}")
    assert duties["invoice_amount_egp"] == 500000.0
    assert duties["customs_duty_amount"] == 50000.0
    assert duties["vat_amount"] == 77000.0  # (500k + 50k) * 14% = 77k
    assert duties["total_estimated_duties"] == 127000.0

    # 3. Master Data Service Tests
    init_db()
    session = SessionLocal()
    md_service = MasterDataService(session)

    today = date.today()
    company = Company(
        egyptian_importer_name="شركة النصر للاستيراد",
        address="القاهرة",
        country="Egypt",
        importer_id="IMP-990011",
        importer_id_expiration_date=today + timedelta(days=20),  # 20 days remaining -> Warning
        vat_id="VAT-112233",
        vat_id_expiration_date=today + timedelta(days=100),
        commercial_registration_no="CR-778899",
        commercial_registration_expiration=today - timedelta(days=5),  # Expired
        status="active"
    )

    alerts = md_service.calculate_company_expiration_alerts(company)
    print(f"✅ Expiration Alerts Calculated: Importer License Days={alerts['importer_license']['days_remaining']} (Warning: {alerts['importer_license']['warning_needed']})")
    assert alerts["importer_license"]["warning_needed"] == True
    assert alerts["commercial_registration"]["is_expired"] == True

    # Supplier Duplicate Prevention Test
    supplier_data = {
        "vendor_company_name": "Global Tech Exporters Ltd",
        "registration_type": "Company",
        "foreign_exporter_id": "REG-EX-887766",
        "foreign_exporter_country": "China",
        "foreign_exporter_country_code": "CN"
    }
    supplier1 = md_service.validate_and_create_supplier(supplier_data)
    print(f"✅ Created Supplier ID: {supplier1.supplier_id} - {supplier1.vendor_company_name}")

    try:
        md_service.validate_and_create_supplier(supplier_data)
        print("❌ FAILED: Duplicate supplier was not blocked!")
        assert False
    except ValueError as e:
        print(f"✅ Successfully blocked duplicate supplier: {e}")

    session.close()
    print("\n🎉 ALL BUSINESS LOGIC & SERVICE TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
