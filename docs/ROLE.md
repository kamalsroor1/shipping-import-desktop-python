# 📌 SYSTEM ROLE & COMPONENT ARCHITECTURE (ROLE.md)

## 🏢 Overview
This system is an **Enterprise Import Operations Management System** for Egyptian importers, handling multi-company master data, foreign supplier profiles, shipping line registers, currency rates, Incoterms 2020 matrices, CBM volume calculation, customs duty estimations, SWIFT payment requests, freight quotation rate comparisons, and customs clearance checklists.

---

## 🏛️ Architecture & Component Responsibilities

### 1. Database & Models Layer (`src/database/`)
- `models/master_data.py`: `Company` (MD-001), `Supplier` (MD-002), `ServiceProvider` (MD-004), `ShippingLine` (MD-005), `Currency` (MD-006), `Incoterm`, `CostItem`, `IncotermCostRule` (MD-007), `HSCode`, `Project` (MD-008).
- `models/import_file.py`: `ImportFile` & `ImportFileItem` (BP-001 - BP-005).
- `models/payment_request.py`: `PaymentRequest` (BP-009).
- `models/freight_quotation.py`: `FreightQuotation` (BP-006).
- `models/customs_checklist.py`: `CustomsDocumentChecklist` (BP-007).
- `models/audit.py`: `AuditLog` (GP-004 Audit Trail).

### 2. Repositories Layer (`src/database/repositories/`)
- `master_data_repository.py`: CRUD operations for Companies, Suppliers, Service Providers, Shipping Lines, Currencies, Incoterms, and Projects.
- `import_file_repository.py`: File creation, item additions, status updates.
- `payment_repository.py`: Financial requests and SWIFT tracking.

### 3. Business Services (`src/services/`)
- `cbm_calculator.py`: Ocean CBM `(L×W×H/1,000,000)` & Air Chargeable Weight `(L×W×H/6000)`.
- `duties_estimator.py`: CIF EGP conversion, customs duty %, 14% VAT, total landed cost.
- `audit_service.py`: Automated action logging for compliance.

### 4. User Interface Layer (`src/ui/`)
- `views/dashboard_view.py`: Dynamic KPIs, recent files, and financial outflow overview.
- `views/operations_view.py`: Registered import files, CBM calculator, duties calculator, BP-006 Freight Quotation comparison, and BP-007 Customs document checklist.
- `views/master_data_view.py`: Full 7-tab Master Data workspace (`MD-001` - `MD-008`) with interactive form dialogs.
- `views/finance_view.py`: Payment requests overview and SWIFT status updates.
- `views/settings_view.py`: Theme toggle (Light ☀️ / Dark Mode 🌙) and Language switch (Arabic / English).
- `forms/`: Interactive QDialog forms for Companies, Suppliers, Service Providers, Shipping Lines, Currencies, Incoterms, Projects, Import Files, and Payment Requests.

---

## 🛠️ Design System & i18n
- **Theme Engine (`src/ui/styles/theme.py`):** High-contrast QSS for Light & Dark modes, including explicit `QMessageBox` alert styling.
- **i18n Manager (`src/utils/i18n.py`):** Pure Arabic (`STRINGS_AR`) and English (`STRINGS_EN`) dictionaries without merged pipe labels.
- **Dynamic Workspace (`src/ui/workspace.py`):** Multi-tab Sahl ERP container with permanent home screen, corner `+` tool button, and `Ctrl+W` shortcut.
