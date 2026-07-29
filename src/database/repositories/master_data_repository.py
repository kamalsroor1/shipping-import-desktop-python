from typing import List, Optional
from datetime import datetime, date
from sqlalchemy.orm import Session
from src.database.models import (
    Company, Supplier, ServiceProvider, ShippingLine,
    Currency, Incoterm, CostItem, IncotermCostRule, HSCode, Project
)
from src.database.models.customs_tariff import CustomsTariff
from src.database.models.container_spec import ContainerSpec
from src.database.models.shipping_scenario import ShippingScenario
from src.services.audit_service import AuditService

class MasterDataRepository:
    def __init__(self, session: Session):
        self.session = session

    # --- MD-001 Company Operations ---
    def create_company(self, company_data: dict, user_id: int = 1) -> Company:
        company = Company(**company_data, created_by=user_id)
        self.session.add(company)
        self.session.commit()
        
        AuditService.log_action(
            self.session, "companies", company.company_id, "create",
            screen_name="MD-001 Company", change_summary=f"Created Company {company.egyptian_importer_name}",
            performed_by=user_id
        )
        return company

    def get_all_companies(self, include_inactive: bool = False) -> List[Company]:
        query = self.session.query(Company).filter(Company.deleted_at == None)
        if not include_inactive:
            query = query.filter(Company.status == 'active')
        return query.all()

    def update_company(self, company_id: int, update_data: dict, user_id: int = 1) -> Optional[Company]:
        company = self.session.query(Company).filter_by(company_id=company_id).first()
        if not company:
            return None
        
        for key, value in update_data.items():
            setattr(company, key, value)
        company.updated_by = user_id
        company.updated_at = datetime.utcnow()
        self.session.commit()

        AuditService.log_action(
            self.session, "companies", company.company_id, "update",
            screen_name="MD-001 Company", change_summary=f"Updated Company {company.egyptian_importer_name}",
            performed_by=user_id
        )
        return company

    # --- MD-002 Supplier Operations ---
    def create_supplier(self, supplier_data: dict, user_id: int = 1) -> Supplier:
        supplier = Supplier(**supplier_data, created_by=user_id)
        self.session.add(supplier)
        self.session.commit()

        AuditService.log_action(
            self.session, "suppliers", supplier.supplier_id, "create",
            screen_name="MD-002 Supplier", change_summary=f"Created Supplier {supplier.vendor_company_name}",
            performed_by=user_id
        )
        return supplier

    def get_all_suppliers(self, include_inactive: bool = False) -> List[Supplier]:
        query = self.session.query(Supplier).filter(Supplier.deleted_at == None)
        if not include_inactive:
            query = query.filter(Supplier.status == 'active')
        return query.all()

    # --- MD-004 Service Providers ---
    def create_service_provider(self, provider_data: dict, user_id: int = 1) -> ServiceProvider:
        provider = ServiceProvider(**provider_data, created_by=user_id)
        self.session.add(provider)
        self.session.commit()

        AuditService.log_action(
            self.session, "service_providers", provider.partner_id, "create",
            screen_name="MD-004 Service Provider", change_summary=f"Created Partner {provider.partner_name}",
            performed_by=user_id
        )
        return provider

    def get_all_service_providers(self, partner_type: Optional[str] = None) -> List[ServiceProvider]:
        query = self.session.query(ServiceProvider).filter(ServiceProvider.deleted_at == None, ServiceProvider.status == 'active')
        if partner_type:
            query = query.filter(ServiceProvider.partner_type == partner_type)
        return query.all()

    # --- MD-006 Currencies ---
    def get_all_currencies(self) -> List[Currency]:
        return self.session.query(Currency).filter_by(status='active').all()

    # --- MD-007 Incoterms ---
    def get_all_incoterms(self) -> List[Incoterm]:
        return self.session.query(Incoterm).filter_by(status='active').all()

    # --- MD-008 Customs Tariff ---
    def create_customs_tariff(self, tariff_data: dict) -> CustomsTariff:
        tariff = CustomsTariff(**tariff_data)
        self.session.add(tariff)
        self.session.commit()
        return tariff

    def get_all_customs_tariffs(self) -> List[CustomsTariff]:
        return self.session.query(CustomsTariff).filter_by(status='active').all()

    # --- MD-010 Container Specs ---
    def create_container_spec(self, spec_data: dict) -> ContainerSpec:
        spec = ContainerSpec(**spec_data)
        self.session.add(spec)
        self.session.commit()
        return spec

    def get_all_container_specs(self) -> List[ContainerSpec]:
        return self.session.query(ContainerSpec).filter_by(status='active').all()

    # --- BP-007 Shipping Scenarios ---
    def create_shipping_scenario(self, scenario_data: dict) -> ShippingScenario:
        sc = ShippingScenario(**scenario_data)
        self.session.add(sc)
        self.session.commit()
        return sc

    def get_scenarios_for_file(self, import_file_id: str) -> List[ShippingScenario]:
        return self.session.query(ShippingScenario).filter_by(import_file_id=import_file_id).all()
