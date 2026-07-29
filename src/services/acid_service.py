"""
BP-014 ACID Request & Verification Service
Snapshots ACID request data and runs automated cross-verification against importer/exporter IDs, PI numbers, and UN/LOCODE ports.
"""

from typing import Dict, Any, List

class ACIDVerificationService:
    @staticmethod
    def verify_acid_certificate(import_file_data: Dict[str, Any], acid_certificate_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cross-verifies ACID certificate fields against Import File snapshot.
        Must match: Importer Tax ID, Exporter Registration ID, Exporter Country Code, PI Number, Shipping Port UN/LOCODE.
        """
        checks = []
        is_all_matched = True

        field_mappings = [
            ("importer_tax_id", "Egyptian Importer Tax ID"),
            ("foreign_exporter_id", "Foreign Exporter ID"),
            ("exporter_country_code", "Exporter Country Code"),
            ("proforma_invoice_no", "Proforma Invoice Number"),
            ("shipping_port_locode", "Shipping Port UN/LOCODE")
        ]

        for field_key, field_label in field_mappings:
            system_val = str(import_file_data.get(field_key, "")).strip().upper()
            acid_val = str(acid_certificate_data.get(field_key, "")).strip().upper()
            
            matched = (system_val == acid_val) and bool(system_val)
            if not matched:
                is_all_matched = False

            checks.append({
                "field_name": field_label,
                "system_value": system_val,
                "acid_value": acid_val,
                "status": "Match" if matched else "Mismatch"
            })

        verification_status = "Verified" if is_all_matched else "Mismatch Warning"

        return {
            "acid_number": acid_certificate_data.get("acid_number", ""),
            "verification_status": verification_status,
            "is_ready_for_booking": is_all_matched,
            "field_checks": checks
        }
