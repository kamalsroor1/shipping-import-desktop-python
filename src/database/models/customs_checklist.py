"""
Customs Document Checklist ORM Model — BP-007 Customs Consultation
"""

from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, func
from src.database.session import Base


class CustomsDocumentChecklist(Base):
    """BP-007 Customs Pre-Clearance Documents Verification Checklist"""
    __tablename__ = "customs_checklists"

    checklist_id = Column(Integer, primary_key=True, autoincrement=True)
    import_file_id = Column(String(32), ForeignKey("import_files.import_file_id"), nullable=False)
    document_type = Column(String(100), nullable=False)  # Commercial Invoice, Packing List, C/O, Inspection, ACID
    is_required = Column(String(16), nullable=False, default="Yes")
    status = Column(String(32), nullable=False, default="⏳ قيد المراجعة")  # Received, Verified, Approved, Rejected
    broker_remarks = Column(Text, nullable=True)
    verified_date = Column(Date, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
