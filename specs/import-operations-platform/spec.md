# Feature Specification: Import Operations Management Platform (v1.1.0)

## 1. Problem Statement & User Story
As an Egyptian Import Operations Manager, I need a specialized desktop operations platform that guides my team through the complete 15-stage Egyptian import lifecycle, automates CBM/Container loading optimization, projects realistic warehouse arrival dates across carrier quotes, enforces Nafeza ACID verification and Central Bank Form 4 compliance, and mandates Dual Document Approval before CargoX blockchain uploads.

---

## 2. Functional Requirements (SpecKit Functional Specification)

### FR-01: Flexible Operational Milestone Tracking
- The system shall track shipments across 15 operational milestones (PO Receipt, PI/PL Review, CBM/Weight Calc, Shipping Scenarios, Customs Consultation, Duty Estimation, Financial Transfer, ACID Verification, Booking, Production Audit, Dual Document Approval, CargoX Exchange, Courier Tracking, Bank Form 4, Clearance & Warehouse Receiving).
- Each shipment maintains a single `Current Stage` and `Waiting For` state.

### FR-02: Advanced Master Data Management (MD-001 to MD-010)
- **MD-001 Importers**: Track legal license, VAT, and commercial register expiration dates with dynamic `days_to_renew` calculation.
- **MD-002 Exporters**: Enforce unique constraint `(registration_type, foreign_exporter_id)` and store beneficiary bank SWIFT/IBAN details.
- **MD-003 Service Providers**: Support Freight Forwarders, Customs Brokers, Inspection Agencies, and Courier Companies with credit limits.
- **MD-006 Incoterms Matrix**: Relational mapping between Incoterms 2020, Cost Items, and Importer/Exporter/Shared responsibility.
- **MD-008 Customs Tariff**: Store HS Codes, Customs Duty %, 14% VAT, Development Tax %, and Regulatory Agency approvals (GOEIC, NTRA, MOH).
- **MD-010 Container Master**: Store standard ISO metrics (20GP, 40GP, 40HC, 45HC) including Tare Weight, Max Payload, and Door Clearances.

### FR-03: Cargo Loading Optimization Engine (BP-005)
- Automatically evaluate carton volume and gross weight against ISO Container Specs.
- Calculate Space Utilization %, Payload Utilization %, Door Clearance validation, and output fit status (`Fit`, `Partial Fit`, `Overweight`, `Oversized`).

### FR-04: Shipping Scenarios & Warehouse ETA Projection (BP-007)
- Evaluate N shipping options per shipment.
- Calculate Vessel Lead Time (`Arrival - Sailing`), Ready for Shipping Days (`Sailing - CRD`), Expected Line Delay, and Expected Warehouse Arrival Date (`CRD + Total Days`).
- Aggregate Average Expected Transit Days and Recommended Carrier Scenario.

### FR-05: Tariff-Driven Import Duty Estimator (BP-010)
- Calculate Customs Duty, 14% VAT, Development Tax, and Total Import Cost directly from `CustomsTariff` master records.

### FR-06: Actionable Import Requirements Assessment (BP-011)
- Transform customs remarks and regulatory approvals into actionable Task Lists assigned to responsible parties (`Supplier`, `Import Team`, `Customs Broker`).

### FR-07: ACID Verification & Snapshot Audit (BP-014)
- Snapshot ACID request data and execute automated field matching against importer/exporter IDs, PI numbers, and UN/LOCODE ports.

### FR-08: Shipping Documents Review & Dual Approval (BP-019)
- Require independent digital sign-offs from both the Import Operations Manager and Licensed Customs Broker before marking documents `Final`.

### FR-09: Provider-Agnostic Electronic Document Exchange (BP-021)
- Run `Document Verification Rules` checking Shipper Name, Importer Tax ID, ACID Number, Currency, Package Count, HS Code, and Invoice Total prior to CargoX/blockchain upload.

---

## 3. Non-Functional Requirements
- **NFR-01**: 100% Python 3.13, PySide6 (Qt 6.8+), and SQLAlchemy 2.0 implementation.
- **NFR-02**: Offline SQLite database with zero external server dependencies.
- **NFR-03**: Single-file PyInstaller binary distribution (`IMS.exe`).
- **NFR-04**: Local workspace safety — zero Git commits/pushes executed automatically.
