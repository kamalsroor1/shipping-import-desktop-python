"""
Payment Repository — Database CRUD Operations for BP-009 Payment Requests
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.database.models.payment_request import PaymentRequest


class PaymentRepository:
    def __init__(self, session: Session):
        self.session = session

    def generate_next_request_number(self) -> int:
        count = self.session.query(func.count(PaymentRequest.request_id)).scalar() or 0
        return count + 1

    def generate_next_request_id(self) -> str:
        num = self.generate_next_request_number()
        return f"PAY-2026-{num:04d}"

    def create_payment_request(self, data: dict) -> PaymentRequest:
        req_id = self.generate_next_request_id()
        req_num = self.generate_next_request_number()

        pay_req = PaymentRequest(
            request_id=req_id,
            request_number=req_num,
            import_file_id=data.get("import_file_id", "IMP-2026-0001"),
            beneficiary_name=data.get("beneficiary_name", "Global Tech Exporters Ltd"),
            payment_type=data.get("payment_type", "Advance Payment"),
            requested_amount_usd=data.get("requested_amount_usd", 5000.0),
            swift_code=data.get("swift_code", "BKCHCNBJ100"),
            iban_account=data.get("iban_account", "CN88 1002 9988 7766 5544"),
            status=data.get("status", "⏳ قيد المعالجة"),
            swift_reference=data.get("swift_reference", "قيد الإصدار"),
            notes=data.get("notes", "")
        )
        self.session.add(pay_req)
        self.session.commit()
        self.session.refresh(pay_req)
        return pay_req

    def get_all_payment_requests(self) -> List[PaymentRequest]:
        return self.session.query(PaymentRequest).order_by(PaymentRequest.created_at.desc()).all()
