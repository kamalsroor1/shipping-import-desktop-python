"""
MD-008 Customs Tariff (HS Code Master Data Specification)
Stores Egyptian Customs Tariff, Duty %, 14% VAT, Development Tax %, and Regulatory Approvals.
"""

from sqlalchemy import Column, String, Text, Numeric, Boolean, DateTime, func
from src.database.session import Base

class CustomsTariff(Base):
    __tablename__ = "customs_tariffs"

    hs_code = Column(String(20), primary_key=True)
    hs_description = Column(Text, nullable=False)
    customs_duty_pct = Column(Numeric(7, 4), nullable=False, default=0.0)
    vat_pct = Column(Numeric(7, 4), nullable=False, default=0.14)
    development_tax_pct = Column(Numeric(7, 4), nullable=False, default=0.0)
    additional_fees_pct = Column(Numeric(7, 4), nullable=False, default=0.0)
    
    requires_coo = Column(Boolean, nullable=False, default=True)
    requires_inspection = Column(Boolean, nullable=False, default=False)
    requires_acid = Column(Boolean, nullable=False, default=True)
    regulatory_authority = Column(String(64), nullable=True)  # GOEIC, NTRA, MOH, Security
    
    status = Column(String(16), nullable=False, default="active")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
