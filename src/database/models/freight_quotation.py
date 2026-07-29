"""
Freight Quotation ORM Model — BP-006 Freight Quotations & Carrier Comparison
"""

from sqlalchemy import Column, Integer, BigInteger, String, Text, Date, DateTime, Numeric, ForeignKey, func
from src.database.session import Base


class FreightQuotation(Base):
    """BP-006 Freight Quotation & Carrier Rate Comparison"""
    __tablename__ = "freight_quotations"

    quotation_id = Column(Integer, primary_key=True, autoincrement=True)
    import_file_id = Column(String(32), ForeignKey("import_files.import_file_id"), nullable=False)
    carrier_name = Column(String(255), nullable=False)  # Shipping Line or Forwarder Name
    vessel_name = Column(String(100), nullable=True)
    port_of_loading = Column(String(100), nullable=False)
    port_of_discharge = Column(String(100), nullable=False)
    sailing_date = Column(Date, nullable=True)
    arrival_date = Column(Date, nullable=True)
    transit_time_days = Column(Integer, nullable=True, default=14)
    freight_cost_usd = Column(Numeric(18, 4), nullable=False, default=0.0)
    free_time_days = Column(Integer, nullable=False, default=14)
    is_recommended = Column(String(16), nullable=False, default="No")  # Yes / No
    remarks = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
