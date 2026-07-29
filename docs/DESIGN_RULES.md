# DESIGN_RULES.md — Import Management System
## Single Source of Truth for UI/UX, Component Guidelines, Theme Engine & Design System

---

## 1. Core Visual Principles & Design Philosophy

1. **Enterprise Modernity & High Contrast:**
   - Crisp, readable typography using **Cairo** for Arabic and **Segoe UI** for English.
   - 100% high contrast text ensuring zero blurry or invisible labels across all themes.

2. **Dual Theme Architecture (Light Theme ☀️ vs Dark Mode 🌙):**
   - **Light Theme ☀️:** `#ecf0f1` Canvas, `#ffffff` Surface Cards, `#2c3e50` Primary Text, `#16a085` Emerald Accent, `#34495e` Dark Slate Headers.
   - **Dark Mode 🌙:** `#0f172a` Deep Slate Canvas, `#1e293b` Surface Cards, `#f8fafc` Primary Text, `#38bdf8` Sky Blue Accent, `#0f3460` Table Headers.

3. **Sahl ERP Multi-Tab Workspace Architecture (Section 15.5):**
   - Dynamic `QTabWidget` workspace with permanent landing tab (`🏠 إبدأ مع التطبيق`).
   - Dynamic sub-screen instances opened on demand via Metro Tiles, Top Menu, or corner `+` tool button.
   - Keyboard shortcut `Ctrl+W` to close current active sub-screen tab.

---

## 2. Palette Tokens & Color Rules

| Token Name | Light Theme Value ☀️ | Dark Mode Value 🌙 | Application Usage |
|------------|----------------------|--------------------|-------------------|
| `COLOR_CANVAS` | `#ecf0f1` | `#0f172a` | Window & Main Shell Background |
| `COLOR_SURFACE` | `#ffffff` | `#1e293b` | QGroupBox, QFrame, & QTableWidget Background |
| `COLOR_TEXT_PRIMARY` | `#2c3e50` | `#f8fafc` | Primary Headings & Body Text |
| `COLOR_TEXT_SECONDARY` | `#7f8c8d` | `#94a3b8` | Subtitles, Captions, & Hints |
| `COLOR_ACCENT` | `#16a085` | `#38bdf8` | Primary Actions, Selected Tabs, Focus Borders |
| `COLOR_HEADER_BG` | `#34495e` | `#0f172a` | QHeaderView & Group Title Accent |
| `COLOR_SUCCESS` | `#27ae60` | `#22c55e` | Positive Badges & Save Buttons |
| `COLOR_WARNING` | `#e67e22` | `#f59e0b` | Pending Badges & Caution Alerts |
| `COLOR_DANGER` | `#c0392b` | `#ef4444` | Cancelled Badges & Delete Buttons |

---

## 3. Form Dialog & Interaction Rules

1. **Interactive Row Double-Clicking:**
   - Double-clicking any row in tables (`OperationsView`, `FinanceView`, `DashboardView`) MUST open a dedicated **Form Dialog** (`EditImportFileForm` / `EditPaymentRequestForm`).
   - Dialogs must use tokenized high-contrast QSS headers (`#38bdf8` in Dark Mode, `#16a085` in Light Mode) and clear action buttons.

2. **Button Contrast & State Styling:**
   - Buttons must have solid, non-transparent background colors and bold white text (`#ffffff`).
   - Primary Action (`#34495e` / `#0f3460`), Success (`#27ae60`), Info (`#2980b9`).

---

## 4. Report Exporting Standards (Excel & PDF)

1. **Excel Workbooks (`.xlsx` via openpyxl):**
   - Must use RTL layout (`sheetView[0].rightToLeft = True`).
   - Merged header banner with project title.
   - Solid styled header rows and explicit column width auto-fitting using `get_column_letter`.

2. **PDF Customs Statements (`.pdf` via reportlab):**
   - Formal calculation breakdown showing CIF USD, Customs Rate (EGP), Duty Amount, VAT (14%), and Landed Cost.
