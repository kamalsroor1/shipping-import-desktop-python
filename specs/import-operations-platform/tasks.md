# SpecKit Task Breakdown: Import Operations Management Platform

## Phase 1: Database & Model Expansion
- [ ] **Task 1.1**: Update `Company` model in `src/database/models/master_data.py` with document expiry fields and dynamic `days_to_renew` logic (`MD-001`).
- [ ] **Task 1.2**: Update `Supplier` model with composite unique constraint `(registration_type, foreign_exporter_id)` and bank SWIFT/IBAN fields (`MD-002`).
- [ ] **Task 1.3**: Update `ServiceProvider` with partner types and credit limits (`MD-003`).
- [ ] **Task 1.4**: Add `CustomsTariff` model for HS Codes, Duty %, VAT (14%), and Development Tax % (`MD-008`).
- [ ] **Task 1.5**: Add `ContainerSpec` model for ISO container capacity and door clearance metrics (`MD-010`).
- [ ] **Task 1.6**: Add `ShippingScenario` model for carrier quote options and warehouse ETA projections (`BP-007`).

---

## Phase 2: Core Domain Calculation Engines & Services
- [ ] **Task 2.1**: Implement `LoadingCalculationEngine` in `src/services/loading_calculator.py` (`BP-005`).
- [ ] **Task 2.2**: Implement `ShippingScenarioEvaluator` in `src/services/shipping_scenario_service.py` (`BP-007`).
- [ ] **Task 2.3**: Refactor `DutiesEstimator` in `src/services/duties_estimator.py` to pull directly from `CustomsTariff` (`BP-010`).
- [ ] **Task 2.4**: Implement `ACIDVerificationService` in `src/services/acid_service.py` (`BP-014`).
- [ ] **Task 2.5**: Implement `DocumentDualApprovalManager` in `src/services/document_approval_service.py` (`BP-019`).
- [ ] **Task 2.6**: Implement `ElectronicDocumentExchangeService` in `src/services/electronic_exchange_service.py` (`BP-021`).

---

## Phase 3: Repository & Business Logic Layer
- [ ] **Task 3.1**: Extend `MasterDataRepository` in `src/database/repositories/master_data_repository.py` for new master data entities.
- [ ] **Task 3.2**: Extend `ImportFileRepository` in `src/database/repositories/import_file_repository.py` with stage milestone filters.

---

## Phase 4: PySide6 Desktop UI Views & Dashboard
- [ ] **Task 4.1**: Upgrade `MasterDataView` in `src/ui/views/master_data_view.py` with tabs for Importers, Suppliers, Service Providers, Tariffs, Incoterms Matrix, and Containers.
- [ ] **Task 4.2**: Upgrade `ImportFileView` in `src/ui/views/import_file_view.py` with Operational State Header, Loading Optimization, Shipping Scenarios, and Dual Approval.
- [ ] **Task 4.3**: Update `DashboardView` in `src/ui/views/dashboard_view.py` with Daily Workspace widgets.

---

## Phase 5: Automated Verification & Bundling
- [ ] **Task 5.1**: Expand unit test suite in `tests/test_all.py` ensuring 100% test pass rate across all new domain engines.
- [ ] **Task 5.2**: Test standalone executable build using `python build_app.py` -> `dist/IMS.exe`.
