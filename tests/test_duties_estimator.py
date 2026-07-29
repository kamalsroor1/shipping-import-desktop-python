"""
Unit Tests for Customs Duties Estimator Service (BP-008)
Tests customs duties, 14% VAT, EGP currency conversion, and landed cost estimations.
"""

import pytest
from src.services.duties_estimator import DutiesEstimator


def test_calculate_hs_duties_standard_rate():
    # CIF $10,000 @ 48.50 EGP/USD = 485,000 EGP
    # Customs Duty 5% = 24,250 EGP
    # VAT Base = 485,000 + 24,250 = 509,250 EGP
    # VAT 14% = 71,295 EGP
    # Total Import Cost = 485,000 + 24,250 + 71,295 = 580,545 EGP
    res = DutiesEstimator.calculate_hs_duties(
        amount=10000.0,
        customs_duty_pct=0.05,
        vat_pct=0.14,
        exchange_rate=48.50
    )

    assert res['invoice_amount_egp'] == 485000.0
    assert res['customs_duty_amount'] == 24250.0
    assert res['vat_amount'] == 71295.0
    assert res['total_estimated_import_cost'] == 580545.0


def test_calculate_hs_duties_zero_duty():
    # Duty 0% (Duty free item)
    res = DutiesEstimator.calculate_hs_duties(
        amount=5000.0,
        customs_duty_pct=0.0,
        vat_pct=0.14,
        exchange_rate=50.0
    )
    assert res['invoice_amount_egp'] == 250000.0
    assert res['customs_duty_amount'] == 0.0
    assert res['vat_amount'] == 35000.0
    assert res['total_estimated_import_cost'] == 285000.0
