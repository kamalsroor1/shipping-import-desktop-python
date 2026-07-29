"""
BP-019 Shipping Documents Dual Approval Manager
Requires separate digital approvals from Importer Operations Manager and Customs Broker before marking documents Final.
"""

from typing import Dict, Any, List

class DocumentDualApprovalManager:
    @staticmethod
    def process_approval(
        document_name: str,
        importer_approved: bool = False,
        importer_notes: str = "",
        broker_approved: bool = False,
        broker_notes: str = ""
    ) -> Dict[str, Any]:
        """
        Evaluates Dual Approval state for a shipment document.
        """
        is_final = importer_approved and broker_approved
        
        if is_final:
            status = "Final Approved"
            summary = "Document fully approved by both Importer Manager and Licensed Customs Broker."
        elif importer_approved and not broker_approved:
            status = "Pending Broker Approval"
            summary = "Approved by Importer Manager. Awaiting Customs Broker sign-off."
        elif not importer_approved and broker_approved:
            status = "Pending Importer Approval"
            summary = "Approved by Customs Broker. Awaiting Importer Manager sign-off."
        else:
            status = "Revision Required"
            summary = "Document requires review and revisions."

        return {
            "document_name": document_name,
            "status": status,
            "is_final": is_final,
            "importer_approval": {
                "approved": importer_approved,
                "notes": importer_notes
            },
            "broker_approval": {
                "approved": broker_approved,
                "notes": broker_notes
            },
            "summary": summary
        }
