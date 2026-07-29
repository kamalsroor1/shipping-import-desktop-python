"""
Report Exporter Utility — Excel & PDF Export Services
Provides export functionality for Import Files, Customs Duties Statements, and Financial Requests.
"""

import os
from typing import List
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class ExcelReportExporter:
    """Exports Import Files & Master Data tables to formatted Excel workbooks (.xlsx)."""

    @staticmethod
    def export_import_files(filepath: str, files_data: list) -> bool:
        wb = Workbook()
        ws = wb.active
        ws.title = "ملفات الاستيراد"
        ws.sheet_properties.tabColor = "34495E"
        ws.views.sheetView[0].rightToLeft = True  # RTL layout in Excel

        # Title Header
        ws.merge_cells("A1:G1")
        title_cell = ws["A1"]
        title_cell.value = "نظام إدارة الاستيراد — تقرير ملفات الاستيراد الشامل"
        title_cell.font = Font(name="Segoe UI", size=16, bold=True, color="FFFFFF")
        title_cell.fill = PatternFill(start_color="34495E", end_color="34495E", fill_type="solid")
        title_cell.alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[1].height = 40

        # Table Column Headers
        headers = [
            "رقم الملف (File ID)", "اسم المشروع (Project)", "الشركة المستوردة (Company)",
            "المورد الأجنبي (Supplier)", "وسيلة الشحن (Mode)", "الحجم (CBM)", "المرحلة (Stage)"
        ]
        ws.append([])  # Row 2 blank
        ws.append(headers)  # Row 3 headers

        header_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="16A085", end_color="16A085", fill_type="solid")
        header_align = Alignment(horizontal="center", vertical="center")

        ws.row_dimensions[3].height = 28
        for col_num in range(1, len(headers) + 1):
            cell = ws.cell(row=3, column=col_num)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_align

        # Data Rows
        thin_border = Border(
            left=Side(style='thin', color='DFE6E9'),
            right=Side(style='thin', color='DFE6E9'),
            top=Side(style='thin', color='DFE6E9'),
            bottom=Side(style='thin', color='DFE6E9')
        )

        for row_idx, file_item in enumerate(files_data, start=4):
            row_data = [
                file_item.get("import_file_id", ""),
                file_item.get("project_name", ""),
                file_item.get("company_name", ""),
                file_item.get("supplier_name", ""),
                file_item.get("freight_mode", ""),
                f"{file_item.get('total_cbm', 0):.2f} CBM",
                file_item.get("stage", "")
            ]
            ws.append(row_data)
            ws.row_dimensions[row_idx].height = 24

            for col_num in range(1, len(headers) + 1):
                cell = ws.cell(row=row_idx, column=col_num)
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.border = thin_border
                cell.font = Font(name="Segoe UI", size=10)

        # Explicit column widths without MergedCell error
        widths = [18, 28, 28, 28, 20, 16, 20]
        for idx, width in enumerate(widths, start=1):
            col_letter = get_column_letter(idx)
            ws.column_dimensions[col_letter].width = width

        wb.save(filepath)
        return True


class PDFReportExporter:
    """Generates PDF Reports for Customs Duties & Tax Estimates."""

    @staticmethod
    def generate_duties_summary_pdf(filepath: str, cif_usd: float, fx_rate: float, duties_res: dict) -> bool:
        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter

        # Header Title
        c.setFont("Helvetica-Bold", 18)
        c.setFillColorRGB(0.2, 0.28, 0.36)  # #34495e
        c.drawString(50, height - 50, "Import Management System — Customs Duty Estimate")

        c.setFont("Helvetica", 10)
        c.setFillColorRGB(0.5, 0.5, 0.5)
        c.drawString(50, height - 70, "BP-008 Statement of Estimated Customs Duties and Taxes")
        c.line(50, height - 80, width - 50, height - 80)

        # Content Table Block
        y = height - 120
        c.setFont("Helvetica-Bold", 12)
        c.setFillColorRGB(0.1, 0.6, 0.5)  # #16a085
        c.drawString(50, y, "Calculation Summary:")
        y -= 25

        c.setFont("Helvetica", 11)
        c.setFillColorRGB(0, 0, 0)

        items = [
            ("Invoice Amount (CIF USD):", f"${cif_usd:,.2f}"),
            ("Customs Exchange Rate (EGP):", f"EGP {fx_rate:.2f}"),
            ("Invoice Value in EGP:", f"EGP {duties_res.get('invoice_amount_egp', 0):,.2f}"),
            ("Customs Duty Amount:", f"EGP {duties_res.get('customs_duty_amount', 0):,.2f}"),
            ("VAT Amount (14%):", f"EGP {duties_res.get('vat_amount', 0):,.2f}"),
            ("Total Landed Import Cost:", f"EGP {duties_res.get('total_estimated_import_cost', 0):,.2f}"),
        ]

        for label, val in items:
            c.drawString(70, y, label)
            c.drawRightString(width - 70, y, val)
            c.line(70, y - 5, width - 70, y - 5)
            y -= 28

        # Footer Notice
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColorRGB(0.5, 0.5, 0.5)
        c.drawString(50, 40, "Generated automatically by Import Management System v1.0")

        c.save()
        return True
