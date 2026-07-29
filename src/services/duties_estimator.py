"""
BP-010 – Tariff-Driven Import Duties & Taxes Calculation Engine
Calculates customs duty, 14% VAT, development tax, and total estimated landed import cost in EGP.
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Any, Optional

class DutiesEstimator:
    @staticmethod
    def calculate_hs_duties(
        amount: float,
        customs_duty_pct: float,
        vat_pct: float = 0.14,
        development_tax_pct: float = 0.0,
        other_government_fees: float = 0.0,
        exchange_rate: float = 1.0
    ) -> Dict[str, Any]:
        amount_egp = amount * exchange_rate
        
        customs_duty_amount = amount_egp * customs_duty_pct
        vat_amount = (amount_egp + customs_duty_amount) * vat_pct
        development_tax_amount = amount_egp * development_tax_pct
        
        total_duties = customs_duty_amount + vat_amount + development_tax_amount + other_government_fees
        total_import_cost = amount_egp + total_duties

        def round_currency(val):
            return float(Decimal(str(val)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

        return {
            "invoice_amount_original": round_currency(amount),
            "invoice_amount_egp": round_currency(amount_egp),
            "customs_duty_pct": customs_duty_pct,
            "customs_duty_amount": round_currency(customs_duty_amount),
            "vat_pct": vat_pct,
            "vat_amount": round_currency(vat_amount),
            "development_tax_pct": development_tax_pct,
            "development_tax_amount": round_currency(development_tax_amount),
            "other_fees": round_currency(other_government_fees),
            "total_estimated_duties": round_currency(total_duties),
            "total_estimated_import_cost": round_currency(total_import_cost)
        }

    @classmethod
    def calculate_duties_from_tariff(cls, amount: float, tariff_record: Any, exchange_rate: float = 48.50) -> Dict[str, Any]:
        """Calculates duties using a CustomsTariff ORM object."""
        customs_duty_pct = float(getattr(tariff_record, "customs_duty_pct", 0.0))
        vat_pct = float(getattr(tariff_record, "vat_pct", 0.14))
        dev_tax_pct = float(getattr(tariff_record, "development_tax_pct", 0.0))
        add_fees_pct = float(getattr(tariff_record, "additional_fees_pct", 0.0))
        
        res = cls.calculate_hs_duties(
            amount=amount,
            customs_duty_pct=customs_duty_pct,
            vat_pct=vat_pct,
            development_tax_pct=dev_tax_pct,
            other_government_fees=(amount * exchange_rate * add_fees_pct),
            exchange_rate=exchange_rate
        )
        res["hs_code"] = getattr(tariff_record, "hs_code", "")
        res["regulatory_authority"] = getattr(tariff_record, "regulatory_authority", "")
        return res
