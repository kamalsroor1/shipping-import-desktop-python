from datetime import date
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from src.database.repositories.master_data_repository import MasterDataRepository
from src.database.models import Company, Supplier

class MasterDataService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = MasterDataRepository(session)

    def calculate_company_expiration_alerts(self, company: Company) -> Dict[str, Any]:
        """
        MD-001 Developer Note: 'Days to Renew' is computed dynamically at runtime,
        never stored in DB.
        """
        today = date.today()
        
        importer_days = (company.importer_id_expiration_date - today).days
        vat_days = (company.vat_id_expiration_date - today).days
        cr_days = (company.commercial_registration_expiration - today).days

        return {
            "company_id": company.company_id,
            "company_name": company.egyptian_importer_name,
            "importer_license": {
                "number": company.importer_id,
                "expiration_date": company.importer_id_expiration_date,
                "days_remaining": importer_days,
                "is_expired": importer_days <= 0,
                "warning_needed": 0 < importer_days <= 30
            },
            "vat_registration": {
                "number": company.vat_id,
                "expiration_date": company.vat_id_expiration_date,
                "days_remaining": vat_days,
                "is_expired": vat_days <= 0,
                "warning_needed": 0 < vat_days <= 30
            },
            "commercial_registration": {
                "number": company.commercial_registration_no,
                "expiration_date": company.commercial_registration_expiration,
                "days_remaining": cr_days,
                "is_expired": cr_days <= 0,
                "warning_needed": 0 < cr_days <= 30
            }
        }

    def validate_and_create_supplier(self, supplier_data: dict, user_id: int = 1) -> Supplier:
        """
        MD-002 Business Rule: 'لا يسمح بتكرار المورد بنفس Registration Type و Foreign Exporter ID'
        """
        existing = (
            self.session.query(Supplier)
            .filter_by(
                registration_type=supplier_data.get("registration_type"),
                foreign_exporter_id=supplier_data.get("foreign_exporter_id"),
                deleted_at=None
            )
            .first()
        )
        if existing:
            raise ValueError(f"المورد مكرر بنفس نوع التسجيل والرقم الرقمي: {existing.vendor_company_name}")

        return self.repo.create_supplier(supplier_data, user_id=user_id)
