"""
Payment Request ORM Model — BP-009 Supplier Payment Requests & SWIFT Tracking
"""

from sqlalchemy import Column, BigInteger, String, Text, DateTime, Numeric, ForeignKey, func
from src.database.session import Base


class PaymentRequest(Base):
    """BP-009 Payment Request Header & SWIFT Transfer Tracking"""
    __tablename__ = "payment_requests"

    request_id = Column(String(32), primary_key=True)  # e.g. PAY-2026-0001
    request_number = Column(BigInteger, nullable=False, default=1)
    import_file_id = Column(String(32), ForeignKey("import_files.import_file_id"), nullable=False)
    beneficiary_name = Column(String(255), nullable=False)
    payment_type = Column(String(64), nullable=False, default="Advance Payment")  # Advance Payment, Against BL, Final Settlement
    requested_amount_usd = Column(Numeric(18, 4), nullable=False, default=0.0)
    swift_code = Column(String(32), nullable=True)
    iban_account = Column(String(100), nullable=True)
    status = Column(String(32), nullable=False, default="معالج")  # معالج, مدفوع, معلق
    swift_reference = Column(String(64), nullable=True)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
