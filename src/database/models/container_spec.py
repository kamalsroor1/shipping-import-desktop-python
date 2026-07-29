"""
MD-010 Container Specifications Master Data
Stores standard ISO Container specs (20GP, 40GP, 40HC, 45HC) for loading optimization calculations.
"""

from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, func
from src.database.session import Base

class ContainerSpec(Base):
    __tablename__ = "container_specs"

    container_spec_id = Column(Integer, primary_key=True, autoincrement=True)
    container_type = Column(String(16), nullable=False, unique=True)  # 20GP, 40GP, 40HC, 45HC
    iso_code = Column(String(16), nullable=True)
    
    internal_length_cm = Column(Numeric(10, 2), nullable=False)
    internal_width_cm = Column(Numeric(10, 2), nullable=False)
    internal_height_cm = Column(Numeric(10, 2), nullable=False)
    door_width_cm = Column(Numeric(10, 2), nullable=False)
    door_height_cm = Column(Numeric(10, 2), nullable=False)
    
    cubic_capacity_cbm = Column(Numeric(10, 4), nullable=False)
    tare_weight_kg = Column(Numeric(10, 2), nullable=False)
    max_payload_kg = Column(Numeric(10, 2), nullable=False)
    max_gross_weight_kg = Column(Numeric(10, 2), nullable=False)
    floor_area_sqm = Column(Numeric(10, 2), nullable=False)
    supports_stacking = Column(Boolean, nullable=False, default=True)
    
    status = Column(String(16), nullable=False, default="active")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
