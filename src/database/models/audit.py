from sqlalchemy import Column, Integer, BigInteger, String, Text, DateTime, func
from src.database.session import Base

class AuditLog(Base):
    __tablename__ = "audit_log"

    audit_log_id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String(64), nullable=False, index=True)
    record_id = Column(BigInteger, nullable=False, index=True)
    action = Column(String(32), nullable=False)  # create / update / status_change / delete / approve / reject
    screen_name = Column(String(128), nullable=True)
    change_summary = Column(Text, nullable=True)
    performed_by = Column(BigInteger, nullable=False, default=1)
    performed_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
