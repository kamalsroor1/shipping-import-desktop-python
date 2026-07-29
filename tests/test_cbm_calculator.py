"""
Unit Tests for CBM Calculator Service (BP-004)
Tests ocean container CBM calculations, air chargeable weight calculations, and volume conversions.
"""

import pytest
from src.services.cbm_calculator import CBMCalculator


def test_calculate_item_cbm_standard_carton():
    # 120cm x 80cm x 100cm carton = 0.96 CBM per carton
    qty = 5
    cbm = CBMCalculator.calculate_item_cbm(qty, 120, 80, 100)
    assert cbm == 4.8  # 5 * 0.96


def test_calculate_item_cbm_zero_dimensions():
    assert CBMCalculator.calculate_item_cbm(0, 120, 80, 100) == 0.0
    assert CBMCalculator.calculate_item_cbm(5, 0, 80, 100) == 0.0


def test_calculate_air_chargeable_weight_volume_heavy():
    # Volume weight: 10 * (100 * 100 * 100) / 6000 = 1666.67 kg
    # Gross weight: 500 kg
    # Chargeable weight should be Volume Weight = 1666.67 kg
    air_wt = CBMCalculator.calculate_air_chargeable_weight(10, 100, 100, 100, 500.0)
    assert pytest.approx(air_wt, 0.01) == 1666.67


def test_calculate_air_chargeable_weight_gross_heavy():
    # Volume weight: 10 * (50 * 50 * 50) / 6000 = 208.33 kg
    # Gross weight: 800 kg
    # Chargeable weight should be Gross Weight = 800 kg
    air_wt = CBMCalculator.calculate_air_chargeable_weight(10, 50, 50, 50, 800.0)
    assert air_wt == 800.0
