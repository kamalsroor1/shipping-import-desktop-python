from decimal import Decimal, ROUND_HALF_UP

class DutiesEstimator:
    """
    BP-008 – Estimate Duties & Taxes Calculation Engine.
    """

    @staticmethod
    def calculate_hs_duties(
        amount: float,
        customs_duty_pct: float,
        vat_pct: float = 0.14,
        development_tax_pct: float = 0.0,
        other_government_fees: float = 0.0,
        exchange_rate: float = 1.0
    ) -> dict:
        """
        Calculates customs duty, VAT, development tax, and total estimated import cost in local currency (EGP).
        """
        amount_egp = amount * exchange_rate
        
        customs_duty_amount = amount_egp * customs_duty_pct
        vat_amount = (amount_egp + customs_duty_amount) * vat_pct  # VAT applies to Value + Duty
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
