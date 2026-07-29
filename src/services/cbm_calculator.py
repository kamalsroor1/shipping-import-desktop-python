from decimal import Decimal, ROUND_HALF_UP

class CBMCalculator:
    """
    BP-004 – Calculate CBM & Air Chargeable Weight Implementation.
    """

    @staticmethod
    def calculate_item_cbm(qty: float, length_cm: float, width_cm: float, height_cm: float) -> float:
        """
        Ocean CBM Formula:
        CBM = Qty * Length(cm) * Width(cm) * Height(cm) / 1,000,000
        """
        if qty <= 0 or length_cm <= 0 or width_cm <= 0 or height_cm <= 0:
            return 0.0
        
        cbm = (qty * length_cm * width_cm * height_cm) / 1_000_000.0
        return float(Decimal(str(cbm)).quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP))

    @staticmethod
    def calculate_air_chargeable_weight(qty: float, length_cm: float, width_cm: float, height_cm: float, gross_weight_kg: float) -> float:
        """
        Air Chargeable Weight Formula:
        Volumetric Weight = Qty * Length(cm) * Width(cm) * Height(cm) / 6,000
        Chargeable Weight = MAX(Volumetric Weight, Gross Weight)
        """
        if qty <= 0 or length_cm <= 0 or width_cm <= 0 or height_cm <= 0:
            return float(gross_weight_kg)
        
        volumetric_weight = (qty * length_cm * width_cm * height_cm) / 6000.0
        chargeable_weight = max(volumetric_weight, float(gross_weight_kg))
        return float(Decimal(str(chargeable_weight)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
