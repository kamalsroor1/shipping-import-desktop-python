from sqlalchemy import Column, Integer, BigInteger, String, Text, Date, DateTime, Numeric, Boolean, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import relationship
from datetime import date
from src.database.session import Base

class Company(Base):
    """MD-001 Egyptian Importer Company"""
    __tablename__ = "companies"

    company_id = Column(Integer, primary_key=True, autoincrement=True)
    egyptian_importer_name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    country = Column(String(100), nullable=False)
    importer_id = Column(String(64), nullable=False)
    importer_id_expiration_date = Column(Date, nullable=False)
    vat_id = Column(String(64), nullable=False)
    vat_id_expiration_date = Column(Date, nullable=False)
    commercial_registration_no = Column(String(64), nullable=False)
    commercial_registration_expiration = Column(Date, nullable=False)
    status = Column(String(16), nullable=False, default="active")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(BigInteger, nullable=True)
    updated_by = Column(BigInteger, nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    @property
    def days_to_renew_importer_id(self) -> int:
        if self.importer_id_expiration_date:
            return (self.importer_id_expiration_date - date.today()).days
        return 0

    @property
    def days_to_renew_vat_id(self) -> int:
        if self.vat_id_expiration_date:
            return (self.vat_id_expiration_date - date.today()).days
        return 0

    @property
    def days_to_renew_commercial_reg(self) -> int:
        if self.commercial_registration_expiration:
            return (self.commercial_registration_expiration - date.today()).days
        return 0

class Supplier(Base):
    """MD-002 Foreign Exporter Supplier"""
    __tablename__ = "suppliers"

    supplier_id = Column(Integer, primary_key=True, autoincrement=True)
    vendor_company_name = Column(String(255), nullable=False)
    registration_type = Column(String(32), nullable=False)  # Company / Individual
    foreign_exporter_id = Column(String(64), nullable=False)
    foreign_exporter_country = Column(String(100), nullable=False)
    foreign_exporter_country_code = Column(String(8), nullable=False)
    address = Column(Text, nullable=True)
    phone_number = Column(String(32), nullable=True)
    email = Column(String(255), nullable=True)
    brands = Column(Text, nullable=True)
    bank_name = Column(String(255), nullable=True)
    swift_code = Column(String(32), nullable=True)
    iban_account_no = Column(String(128), nullable=True)
    status = Column(String(16), nullable=False, default="active")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(BigInteger, nullable=True)
    updated_by = Column(BigInteger, nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        UniqueConstraint('registration_type', 'foreign_exporter_id', name='uq_supplier_registration_id'),
    )

class ServiceProvider(Base):
    """MD-004 External Service Provider / Business Partner"""
    __tablename__ = "service_providers"

    partner_id = Column(Integer, primary_key=True, autoincrement=True)
    partner_name = Column(String(255), nullable=False)
    partner_type = Column(String(32), nullable=False)  # Freight Forwarder, Customs Broker, Bank...
    contact_person = Column(String(255), nullable=True)
    phone_number = Column(String(32), nullable=True)
    mobile_number = Column(String(32), nullable=True)
    email = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)
    country = Column(String(100), nullable=True)
    payment_type = Column(String(16), nullable=True)  # cash / credit
    credit_limit = Column(Numeric(18, 4), nullable=True, default=0)
    notes = Column(Text, nullable=True)
    status = Column(String(16), nullable=False, default="active")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(BigInteger, nullable=True)
    updated_by = Column(BigInteger, nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        UniqueConstraint('partner_name', 'partner_type', name='uq_partner_name_type'),
    )

class ShippingLine(Base):
    """MD-005 Shipping Line"""
    __tablename__ = "shipping_lines"

    shipping_line_id = Column(Integer, primary_key=True, autoincrement=True)
    shipping_line_name = Column(String(255), nullable=False, unique=True)
    scac_code = Column(String(16), nullable=True)
    country = Column(String(100), nullable=True)
    website = Column(String(255), nullable=True)
    status = Column(String(16), nullable=False, default="active")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

class Currency(Base):
    """MD-006 Currency"""
    __tablename__ = "currencies"

    currency_id = Column(Integer, primary_key=True, autoincrement=True)
    iso_code = Column(String(3), nullable=False, unique=True)
    currency_name = Column(String(100), nullable=False)
    symbol = Column(String(8), nullable=True)
    decimal_places = Column(Integer, nullable=False, default=2)
    status = Column(String(16), nullable=False, default="active")

class Incoterm(Base):
    """MD-007 Incoterms"""
    __tablename__ = "incoterms"

    incoterm_id = Column(Integer, primary_key=True, autoincrement=True)
    incoterm_code = Column(String(8), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    version = Column(String(16), nullable=False, default="Incoterms 2020")
    status = Column(String(16), nullable=False, default="active")

class CostItem(Base):
    """MD-007 Cost Item Reference"""
    __tablename__ = "cost_items"

    cost_item_id = Column(Integer, primary_key=True, autoincrement=True)
    cost_item_name = Column(String(100), nullable=False, unique=True)
    category = Column(String(64), nullable=True)

class IncotermCostRule(Base):
    """MD-007 Incoterm Responsibility Matrix"""
    __tablename__ = "incoterm_cost_rules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    incoterm_id = Column(Integer, ForeignKey("incoterms.incoterm_id"), nullable=False)
    cost_item_id = Column(Integer, ForeignKey("cost_items.cost_item_id"), nullable=False)
    responsible_party = Column(String(16), nullable=False)  # Importer / Exporter / Shared
    is_included = Column(Boolean, nullable=False, default=True)
    notes = Column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint('incoterm_id', 'cost_item_id', name='uq_incoterm_cost_item'),
    )

class HSCode(Base):
    """Customs Tariff & HS Code Reference"""
    __tablename__ = "hs_codes"

    hs_code = Column(String(20), primary_key=True)
    description = Column(Text, nullable=True)
    customs_duty_pct = Column(Numeric(7, 4), nullable=False, default=0.0)
    vat_pct = Column(Numeric(7, 4), nullable=False, default=0.14)
    development_tax_pct = Column(Numeric(7, 4), nullable=False, default=0.0)
    max_sample_weight_kg = Column(Numeric(10, 2), nullable=True)
    max_sample_value_usd = Column(Numeric(18, 4), nullable=True)
    status = Column(String(16), nullable=False, default="active")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class Project(Base):
    """MD-008 Projects Hub"""
    __tablename__ = "projects"

    project_id = Column(Integer, primary_key=True, autoincrement=True)
    project_code = Column(String(64), nullable=False, unique=True)
    project_name = Column(String(255), nullable=False)
    project_owner = Column(String(255), nullable=False)
    company_id = Column(BigInteger, ForeignKey("companies.company_id"), nullable=False)
    supplier_id = Column(BigInteger, ForeignKey("suppliers.supplier_id"), nullable=False)
    incoterm_id = Column(BigInteger, ForeignKey("incoterms.incoterm_id"), nullable=False)
    status = Column(String(16), nullable=False, default="open")
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(BigInteger, nullable=True)
    updated_by = Column(BigInteger, nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
