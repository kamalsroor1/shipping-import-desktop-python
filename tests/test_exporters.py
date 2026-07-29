"""
Unit Tests for Excel & PDF Report Exporters
Tests generating Excel workbooks and PDF duty statements.
"""

import os
import tempfile
from src.utils.export import ExcelReportExporter, PDFReportExporter


def test_excel_export_registered_files():
    temp_dir = tempfile.gettempdir()
    filepath = os.path.join(temp_dir, "test_files_export.xlsx")

    sample_files = [
        {
            "import_file_id": "IMP-2026-0001",
            "project_name": "مشروع اختبار",
            "company_name": "شركة النيل",
            "supplier_name": "Tech Co",
            "freight_mode": "Ocean FCL",
            "total_cbm": 45.2,
            "stage": "1. PO Received"
        }
    ]
    ExcelReportExporter.export_import_files(filepath, sample_files)
    assert os.path.exists(filepath)
    assert os.path.getsize(filepath) > 0
    os.remove(filepath)


def test_pdf_export_duties_summary():
    temp_dir = tempfile.gettempdir()
    filepath = os.path.join(temp_dir, "test_duties_summary.pdf")

    res = {
        "invoice_amount_egp": 485000.0,
        "customs_duty_amount": 24250.0,
        "vat_amount": 71295.0,
        "total_estimated_import_cost": 580545.0
    }
    PDFReportExporter.generate_duties_summary_pdf(filepath, 10000.0, 48.50, res)
    assert os.path.exists(filepath)
    assert os.path.getsize(filepath) > 0
    os.remove(filepath)
