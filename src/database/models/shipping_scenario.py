"""
BP-007 Shipping Scenario Evaluation Entity
Stores carrier quotation options, lead times, delays, and projected warehouse arrival dates.
"""

from sqlalchemy import Column, Integer, String, Text, Date, Numeric, Boolean, ForeignKey, DateTime, func
from src.database.session import Base

class ShippingScenario(Base):
    __tablename__ = "shipping_scenarios"

    scenario_id = Column(Integer, primary_key=True, autoincrement=True)
    import_file_id = Column(String(32), ForeignKey("import_files.import_file_id"), nullable=False)
    
    provider_name = Column(String(255), nullable=False)
    vessel_name = Column(String(255), nullable=False)
    sailing_date = Column(Date, nullable=False)
    arrival_date = Column(Date, nullable=False)
    
    vessel_lead_time_days = Column(Integer, nullable=False, default=0)
    ready_for_shipping_days = Column(Integer, nullable=False, default=0)
    expected_line_delay_days = Column(Integer, nullable=False, default=2)
    avg_form4_days = Column(Integer, nullable=False, default=3)
    avg_clearance_days = Column(Integer, nullable=False, default=4)
    
    expected_total_days_to_warehouse = Column(Integer, nullable=False, default=0)
    expected_warehouse_arrival_date = Column(Date, nullable=False)
    is_recommended = Column(Boolean, nullable=False, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
