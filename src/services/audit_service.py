from sqlalchemy.orm import Session
from src.database.models.audit import AuditLog

class AuditService:
    @staticmethod
    def log_action(
        session: Session,
        table_name: str,
        record_id: int,
        action: str,
        screen_name: str = None,
        change_summary: str = None,
        performed_by: int = 1
    ) -> AuditLog:
        """
        GP-004 Audit Trail Logger.
        Logs every critical action (create, update, status_change, delete, approve, reject).
        """
        audit_entry = AuditLog(
            table_name=table_name,
            record_id=record_id,
            action=action,
            screen_name=screen_name,
            change_summary=change_summary,
            performed_by=performed_by
        )
        session.add(audit_entry)
        session.commit()
        return audit_entry

    @staticmethod
    def get_history_for_record(session: Session, table_name: str, record_id: int) -> list[AuditLog]:
        """Retrieves audit trail history for a specific record."""
        return (
            session.query(AuditLog)
            .filter_by(table_name=table_name, record_id=record_id)
            .order_by(AuditLog.performed_at.desc())
            .all()
        )
