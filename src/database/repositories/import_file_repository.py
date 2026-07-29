"""
Import File Repository — Database CRUD Operations for Import Files & Items
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.database.models.import_file import ImportFile, ImportFileItem


class ImportFileRepository:
    def __init__(self, session: Session):
        self.session = session

    def generate_next_file_number(self) -> int:
        """Calculates next sequential file number integer"""
        count = self.session.query(func.count(ImportFile.import_file_id)).scalar() or 0
        return count + 1

    def generate_next_file_id(self) -> str:
        """Generates sequential file number like IMP-2026-0001"""
        num = self.generate_next_file_number()
        return f"IMP-2026-{num:04d}"

    def create_import_file(self, data: dict) -> ImportFile:
        file_id = self.generate_next_file_id()
        file_num = self.generate_next_file_number()

        import_file = ImportFile(
            import_file_id=file_id,
            file_number=file_num,
            project_name=data.get("project_name", "مشروع جديد"),
            company_name=data.get("company_name", "شركة جديدة"),
            supplier_name=data.get("supplier_name", "مورد أجنبي"),
            freight_mode=data.get("freight_mode", "Ocean FCL 40HC"),
            stage=data.get("stage", "Pre-Shipment"),
            status=data.get("status", "active"),
            total_cbm=data.get("total_cbm", 0.0),
            total_gross_weight_kg=data.get("total_gross_weight_kg", 0.0),
            total_invoice_usd=data.get("total_invoice_usd", 0.0),
            notes=data.get("notes", "")
        )
        self.session.add(import_file)
        self.session.commit()
        self.session.refresh(import_file)
        return import_file

    def get_all_import_files(self) -> List[ImportFile]:
        return self.session.query(ImportFile).order_by(ImportFile.created_at.desc()).all()

    def get_file_by_id(self, file_id: str) -> Optional[ImportFile]:
        return self.session.query(ImportFile).filter(ImportFile.import_file_id == file_id).first()

    def add_item_to_file(self, file_id: str, item_data: dict) -> ImportFileItem:
        item = ImportFileItem(
            import_file_id=file_id,
            item_description=item_data.get("item_description", "بضائع مستوردة"),
            hs_code=item_data.get("hs_code", "8471.30"),
            qty=item_data.get("qty", 1.0),
            unit_price_usd=item_data.get("unit_price_usd", 0.0),
            total_price_usd=item_data.get("total_price_usd", 0.0),
            length_cm=item_data.get("length_cm", 0.0),
            width_cm=item_data.get("width_cm", 0.0),
            height_cm=item_data.get("height_cm", 0.0),
            gross_weight_kg=item_data.get("gross_weight_kg", 0.0),
            item_cbm=item_data.get("item_cbm", 0.0)
        )
        self.session.add(item)

        # Update file totals safely converting Decimal to float
        f = self.get_file_by_id(file_id)
        if f:
            f.total_cbm = float(f.total_cbm or 0) + float(item.item_cbm or 0)
            f.total_gross_weight_kg = float(f.total_gross_weight_kg or 0) + float(item.gross_weight_kg or 0)
            f.total_invoice_usd = float(f.total_invoice_usd or 0) + float(item.total_price_usd or 0)

        self.session.commit()
        self.session.refresh(item)
        return item
