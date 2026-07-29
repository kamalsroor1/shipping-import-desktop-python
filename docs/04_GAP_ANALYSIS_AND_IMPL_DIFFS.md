# 04. Gap Analysis & Implementation Plan (Python / PySide6 / SQLAlchemy Stack)

## 1. Tech Stack Commitment Notice

> [!IMPORTANT]
> **Strict Tech Stack Preservation**:
> No new programming languages or external stack changes are introduced. All enhancements will be built 100% using our established Python ecosystem:
> - **Language**: Python 3.13
> - **GUI Framework**: PySide6 (Qt 6.8+ Widgets, Signals/Slots, Custom Styling)
> - **Database / ORM**: SQLite 3 with SQLAlchemy 2.0 ORM & Alembic/DDL Migrations
> - **Reporting & Exports**: ReportLab (PDF generation) & openpyxl (Excel export)
> - **Packaging & Distribution**: PyInstaller (`IMS.exe` standalone bundle) & Inno Setup

---

## 2. Comprehensive Gap Analysis Matrix

| Business Requirement Area | Current Codebase Status | Required Enhancement in Python Architecture | Target Modules |
| :--- | :--- | :--- | :--- |
| **MD-001: Egyptian Importers** | Model `Company` exists | Add document expiry tracking (`importer_id_expiration_date`, `vat_id_expiration_date`, `commercial_registration_expiration`) & dynamic `days_to_renew` logic | `src/database/models/master_data.py`<br>`src/ui/views/master_data_view.py` |
| **MD-002: Foreign Suppliers** | Model `Supplier` exists | Enforce composite unique constraint `(registration_type, foreign_exporter_id)` and add beneficiary bank SWIFT/IBAN fields | `src/database/models/master_data.py`<br>`src/database/repositories/master_data_repository.py` |
| **MD-003: External Providers** | Basic model exists | Add support for partner types (`Freight Forwarder`, `Customs Broker`, `Inspection Agency`, `Courier`) and credit limits | `src/database/models/master_data.py` |
| **MD-006: Incoterms 2020** | Basic Incoterms lookup table | Implement relational 3-tier structure (`Incoterms` ➔ `Cost Items` ➔ `Incoterm Responsibilities`) | `src/database/models/incoterms.py`<br>`src/services/incoterm_service.py` |
| **MD-008: Customs Tariff (HS Code)** | Basic HS Code field | Build dedicated `CustomsTariff` master model storing Duty %, VAT %, Development Tax %, and Regulatory Approvals | `src/database/models/customs_tariff.py` |
| **MD-010: Container Master** | Hardcoded CBM divisors | Build `ContainerSpec` model (20GP, 40GP, 40HC, 45HC) with Tare Weight, Payload, Door Dimensions, and Cubic Capacity | `src/database/models/container.py` |
| **BP-005: Cargo Loading Optimization** | Basic CBM formula | Build `LoadingCalculationEngine` service matching cargo dimensions against `ContainerSpec` with space/payload utilization % | `src/services/loading_calculator.py` |
| **BP-007: Shipping Scenarios** | Single ETA field | Build `ShippingScenarioEvaluator` service computing Lead Time, CRD Delay, Line Delay, and Average Warehouse ETA across N quotes | `src/services/shipping_scenario_service.py` |
| **BP-011: Import Requirements** | Simple Task entity | Build `ImportRequirementsAssessment` engine converting broker remarks & regulatory approvals into actionable System Tasks | `src/services/requirements_engine.py` |
| **BP-014: ACID Verification** | Text field for ACID | Build `ACIDVerificationService` snapshotting request data and performing automated matching against Nafeza certificate data | `src/services/acid_service.py` |
| **BP-019: Dual Document Approval** | Single user approval | Build `DocumentDualApprovalManager` requiring separate digital approvals from Importer Manager & Customs Broker | `src/services/document_approval_service.py` |
| **BP-021: Electronic Exchange** | Generic upload | Build provider-agnostic `ElectronicDocumentExchange` framework with `DocumentVerificationRules` check before upload | `src/services/electronic_exchange_service.py` |

---

## 3. Implementation Plan & Database Schema Roadmap

### Phase 1: Database Schema Expansion (SQLAlchemy 2.0)
1. Update `src/database/models/master_data.py`:
   - Add Expiration Dates to `Company`.
   - Add Bank SWIFT/IBAN & unique constraint to `Supplier`.
   - Add Partner Types & Credit Limits to `ExternalServiceProvider`.
2. Add `src/database/models/incoterms_matrix.py`:
   - `CostItem` and `IncotermResponsibility`.
3. Add `src/database/models/customs_tariff.py`:
   - `CustomsTariff` with Duty %, VAT %, Development Tax %.
4. Add `src/database/models/container_spec.py`:
   - ISO Container dimensions and maximum payloads.

### Phase 2: Domain Services & Calculation Engines
1. Refactor `src/services/cbm_calculator.py` to integrate container optimization (`BP-005`).
2. Add `src/services/shipping_scenario_service.py` (`BP-007`).
3. Add `src/services/duties_estimator.py` to pull directly from `CustomsTariff` (`BP-010`).
4. Add `src/services/acid_verification_service.py` (`BP-014`).
5. Add `src/services/document_dual_approval_service.py` (`BP-019`).

### Phase 3: PySide6 UI View Enhancements
1. Upgrade `MasterDataView` (`src/ui/views/master_data_view.py`) with tabbed managers for Companies, Suppliers, Providers, Incoterms Matrix, Customs Tariffs, and Containers.
2. Upgrade `ImportFileView` (`src/ui/views/import_file_view.py`) with state milestone tracker bar, Shipping Scenario comparison tab, and Dual Document Approval tab.
3. Update `SettingsView` (`src/ui/views/settings_view.py`) to reflect live system documentation and version `1.0.1`.

---

## 4. Summary of Saved Raw Documentation Files

For reference, the exact raw business text submitted by the user has been persisted in:
- 📂 [`docs/raw_import_brd_part1.txt`](file:///i:/disktop/docs/raw_import_brd_part1.txt)
- 📂 [`docs/raw_import_brd_part2.txt`](file:///i:/disktop/docs/raw_import_brd_part2.txt)
