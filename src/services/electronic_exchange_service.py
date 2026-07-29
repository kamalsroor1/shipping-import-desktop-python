"""
BP-021 Electronic Document Exchange (CargoX / Blockchain Agnostic Engine)
Runs Document Verification Rules check before uploading shipping documents to blockchain platforms.
"""

from typing import Dict, Any, List

class ElectronicDocumentExchangeService:
    DEFAULT_VERIFICATION_RULES = [
        "Shipper Name",
        "Egyptian Importer Tax ID",
        "ACID Number",
        "Currency",
        "Number of Packages",
        "HS Code",
        "Invoice Grand Total",
        "Country of Origin",
        "Bill of Lading Number"
    ]

    @classmethod
    def validate_for_upload(cls, document_fields: Dict[str, Any], provider_name: str = "CargoX") -> Dict[str, Any]:
        """
        Validates document data against rules before authorizing blockchain upload.
        """
        checklist = []
        all_passed = True

        for rule in cls.DEFAULT_VERIFICATION_RULES:
            val = document_fields.get(rule.lower().replace(" ", "_"), "")
            passed = bool(val) and str(val).strip() != ""
            if not passed:
                all_passed = False
            
            checklist.append({
                "rule_name": rule,
                "value": str(val),
                "status": "Passed" if passed else "Failed / Missing"
            })

        return {
            "provider_name": provider_name,
            "ready_for_upload": all_passed,
            "upload_status": "Ready for Upload" if all_passed else "Verification Failed",
            "checklist": checklist
        }
