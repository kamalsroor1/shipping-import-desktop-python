# SpecKit Implementation Plan: Import Operations Management Platform (v1.1.0)

## Technical Context
- **Language**: Python 3.13
- **GUI**: PySide6 (Qt 6.8+)
- **Database**: SQLite 3 with SQLAlchemy 2.0 ORM
- **Export Engines**: ReportLab (PDF) & openpyxl (Excel)
- **Deployment**: Single-file PyInstaller (`IMS.exe`) + Inno Setup

---

## Architecture & Data Specifications

### 1. New & Refactored Models
1. `Company` (`MD-001`): Document expiry dates (`importer_id_expiration_date`, `vat_id_expiration_date`, `commercial_registration_expiration`) with dynamic `days_to_renew`.
2. `Supplier` (`MD-002`): Composite unique constraint `(registration_type, foreign_exporter_id)` + SWIFT/IBAN fields.
3. `ExternalServiceProvider` (`MD-003`): Partner types and credit limits.
4. `IncotermsMatrix` (`MD-006`): `CostItem` and `IncotermResponsibility` models.
5. `CustomsTariff` (`MD-008`): HS Code, Duty %, 14% VAT, Development Tax %, Regulatory Approvals.
6. `ContainerSpec` (`MD-010`): ISO Container dimensions, tare weights, maximum payloads.
7. `ShippingScenario` (`BP-007`): Carrier options, vessel lead times, line delays, warehouse ETA.

### 2. Core Service Modules
1. `LoadingCalculationEngine` (`src/services/loading_calculator.py`): Container space and payload optimization.
2. `ShippingScenarioEvaluator` (`src/services/shipping_scenario_service.py`): Multi-carrier ETA projection engine.
3. `DutiesEstimator` (`src/services/duties_estimator.py`): Tariff-driven import tax calculator.
4. `ACIDVerificationService` (`src/services/acid_service.py`): Nafeza certificate cross-matching.
5. `DocumentDualApprovalManager` (`src/services/document_approval_service.py`): Importer + Customs Broker dual sign-off.
6. `ElectronicDocumentExchangeService` (`src/services/electronic_exchange_service.py`): CargoX / Blockchain verification.

---

## Phased Implementation Roadmap

### Phase 1: Database & Model Expansion
- Add new SQLAlchemy models to `src/database/models/`.
- Run table creation migrations.
- Expand `MasterDataRepository` and `ImportFileRepository`.

### Phase 2: Domain Logic & Engines
- Implement `LoadingCalculationEngine`.
- Implement `ShippingScenarioEvaluator`.
- Refactor `DutiesEstimator`.
- Implement `ACIDVerificationService` & `DocumentDualApprovalManager`.

### Phase 3: PySide6 View & Dashboard Upgrades
- Upgrade `MasterDataView` tabs (Companies, Suppliers, Providers, Incoterms Matrix, Tariffs, Containers).
- Upgrade `ImportFileView` tabs (Operational State Header, Container Optimization, Shipping Scenarios, Dual Approval).
- Upgrade `DashboardView` operational workspace widgets.

### Phase 4: Automated Verification & Packaging
- Expand unit test suite in `tests/test_all.py` (100% pass).
- Verify single-file PyInstaller build (`IMS.exe`).

---

## Verification Criteria
- All pytest test cases pass cleanly.
- `IMS.exe` compiles without missing DLLs or dependencies.
- Zero Git pushes executed during plan approval.
