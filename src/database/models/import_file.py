"""
Import File & Items ORM Models
BP-001 / BP-002 / BP-004 — Import Operations Data Models
"""

from sqlalchemy import Column, Integer, BigInteger, String, Text, Date, DateTime, Numeric, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from src.database.session import Base


class ImportFile(Base):
    """BP-001 & BP-002 Import File Header"""
    __tablename__ = "import_files"

    import_file_id = Column(String(32), primary_key=True)  # e.g. IMP-2026-0001
    file_number = Column(BigInteger, nullable=False, default=1)
    project_name = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=False)
    supplier_name = Column(String(255), nullable=False)
    freight_mode = Column(String(64), nullable=False, default="Ocean FCL 40HC")  # Ocean FCL, Ocean LCL, Air Freight
    stage = Column(String(64), nullable=False, default="Pre-Shipment")  # Pre-Shipment, Customs Clearance, Financial, Warehouse, Completed
    status = Column(String(32), nullable=False, default="active")  # active, completed, cancelled

    total_cbm = Column(Numeric(14, 4), nullable=False, default=0.0)
    total_gross_weight_kg = Column(Numeric(14, 2), nullable=False, default=0.0)
    total_invoice_usd = Column(Numeric(18, 4), nullable=False, default=0.0)

    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class ImportFileItem(Base):
    """BP-004 Packing List Item inside Import File"""
    __tablename__ = "import_file_items"

    item_id = Column(Integer, primary_key=True, autoincrement=True)
    import_file_id = Column(String(32), ForeignKey("import_files.import_file_id"), nullable=False)

    item_description = Column(String(255), nullable=False)
    hs_code = Column(String(32), nullable=True)
    qty = Column(Numeric(14, 2), nullable=False, default=1.0)
    unit_price_usd = Column(Numeric(14, 4), nullable=False, default=0.0)
    total_price_usd = Column(Numeric(18, 4), nullable=False, default=0.0)

    length_cm = Column(Numeric(10, 2), nullable=False, default=0.0)
    width_cm = Column(Numeric(10, 2), nullable=False, default=0.0)
    height_cm = Column(Numeric(10, 2), nullable=False, default=0.0)
    gross_weight_kg = Column(Numeric(14, 2), nullable=False, default=0.0)
    item_cbm = Column(Numeric(14, 6), nullable=False, default=0.0)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
