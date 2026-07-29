# 03. Real-World Egyptian Import Workflow & Business Processes

## 1. Real-World Egyptian Import Workflow (The 15 Operational Milestones)

In Egypt, import operations follow a strict, regulated lifecycle that involves the importer, foreign supplier, freight forwarder, shipping line, customs broker, Central Bank of Egypt (Form 4), Nafeza platform (ACID), CargoX (Blockchain Document Exchange), and GOEIC/Customs authorities.

```
 [1. PO Receipt]
        │
        ▼
 [2. PI & Packing Review] ➔ [CBM & Air Weight Calculation]
        │
        ▼
 [3. Shipping Scenarios & RFQ] (CRD, Form 4 Days, Line Delays, Warehouse ETA)
        │
        ▼
 [4. Customs Consultation] (HS Code Nafeza Check, Decree 43, Approvals)
        │
        ▼
 [5. Estimate Duties & Taxes] (Customs Duty %, VAT 14%, Development Tax)
        │
        ▼
 [6. Financial Payment Request] (Advance / Against BL Transfer & SWIFT)
        │
        ▼
 [7. ACID Issuance & Verification] (Nafeza Number & Expiry Audit)
        │
        ▼
 [8. Booking & Cut-Off] (Container Allocation, Sailing Schedule)
        │
        ▼
 [9. Production & Loading Audit] (Container Seals & Actual Weights)
        │
        ▼
[10. Dual Document Approval] (Importer + Broker Review of Draft BL/COO)
        │
        ▼
[11. CargoX Electronic Exchange] (Blockchain Upload & Verification)
        │
        ▼
[12. Original Documents Courier] (Chain of Custody Tracking)
        │
        ▼
[13. Bank Form 4 Issuance] (Original BL + PI + PL Submitted to Bank)
        │
        ▼
[14. Customs Clearance & Assessment] (Nafeza Physical Inspection & Tax Payment)
        │
        ▼
[15. Warehouse Receiving & Project Closure] (Seal Audit & Financial Settlement)
```

---

## 2. Business Process Specifications (BP-001 to BP-021)

---

### BP-001: Receive Purchase Order & Proforma Invoice
- **Purpose**: Creates a new import file upon receiving PO and Proforma Invoice (PI).
- **Inputs**: Importer Name, Tax ID, Foreign Exporter Name, Exporter Registration ID, Country, PI Number, PI Date, PO Number, Shipping Port, Destination Port.
- **Item Level**: HS Code, Item Code, Description, Quantity (PCS), Unit Price, Amount (`Qty * Price`).
- **Validations**: Invoice Amount = Sum of Line Amounts; HS Code required for every line; Duplicate PI check per supplier.

---

### BP-002: Review Proforma Invoice & HS Code Summary
- **Purpose**: Validates PI items and generates an HS Code Summary for customs and duty estimation.
- **Generated Summary**: Groups quantities and total values by unique HS Code.
- **Outputs**: HS Code Analysis Report, Invoice Validation Report.

---

### BP-003: Review Packing List & Package Audit
- **Purpose**: Audits carton/pallet quantities, net weight, gross weight, and dimensions.
- **Key Formulas**:
  - `Total Net Weight = Qty * Net Weight per Unit`
  - `Total Gross Weight = Qty * Gross Weight per Unit`
  - `Gross Weight >= Net Weight`
- **Reports**: Packing List Summary by HS Code (`HS Code | Qty PCS | Qty PKG | Net Weight | Gross Weight`).

---

### BP-004: Calculate CBM & Air Chargeable Weight
- **Purpose**: Computes cubic meter volume and air freight chargeable weight.
- **Formulas**:
  - **Ocean CBM**: `(Qty * Length_cm * Width_cm * Height_cm) / 1,000,000`
  - **Air Chargeable Weight (kg)**: `(Qty * Length_cm * Width_cm * Height_cm) / 6,000`

---

### BP-005: Cargo Loading Planning Engine & Container Optimization
- **Purpose**: Matches cargo CBM and weight against standard ISO container specifications (`MD-010`) before booking.
- **Calculations**:
  - `Used Volume (CBM)` vs `Container Cubic Capacity`
  - `Expected Cargo Weight (kg)` vs `Container Maximum Payload`
  - `Door Clearance (Width & Height)` vs `Pallet Dimensions`
- **Output Status**: `Fit`, `Partial Fit`, `Overweight`, `Oversized`, `Manual Review Required`.

---

### BP-006: Determine Shipping Method
- **Purpose**: Selects optimal shipping mode (`Ocean FCL`, `Ocean LCL`, `Air Freight`, `Road Freight`) based on cargo CBM, chargeable weight, CRD, and target delivery deadline.

---

### BP-007: Shipping Scenarios Evaluation & Warehouse Arrival Projection
- **Purpose**: Evaluates multiple shipping options and calculates estimated warehouse arrival dates based on Egyptian operational lead times.
- **Calculation Rules**:
  - `Vessel Lead Time = Arrival Date - Sailing Date`
  - `Ready for Shipping Days = Sailing Date - Cargo Ready Date (CRD)`
  - `Expected Total Days to Warehouse = Average Form 4 Days + Average Customs Clearance Days + Expected Line Delay + Vessel Lead Time + Ready for Shipping Days`
  - `Expected Warehouse Arrival Date = CRD + Expected Total Days to Warehouse`
- **Aggregations**: Computes Average Transit Days and Recommended Shipping Scenario across all quotes.

---

### BP-008: Freight Quotations Management (RFQ)
- **Purpose**: Manages Request for Quotations (RFQs) across multiple Freight Forwarders, comparing freight cost, transit time, and free time (demurrage allowance).

---

### BP-009: Pre-Shipment Customs Consultation
- **Purpose**: Reviews PI, Packing List, and HS Codes with the Customs Broker prior to shipping to verify Egyptian Customs compliance (Nafeza registration, GOEIC Decree 43 requirements, NTRA approvals).

---

### BP-010: Estimate Duties & Import Taxes
- **Purpose**: Calculates projected customs duties and taxes prior to financial transfers.
- **Formulas**:
  - `Customs Duty = Amount * (Customs Duty %)`
  - `VAT = (Amount + Customs Duty) * 14%`
  - `Development Tax = Amount * (Development Tax %)`
  - `Total Estimated Duties = Customs Duty + VAT + Development Tax + Additional Fees`

---

### BP-011: Import Requirements Assessment (Action List Engine)
- **Purpose**: Converts customs remarks, required approvals (GOEIC, NTRA, Ministry of Health), registrations, and missing documents into actionable Task Lists assigned to responsible users (`Supplier`, `Import Team`, `Customs Broker`).

---

### BP-012: Financial Payment Request & SWIFT Allocation
- **Purpose**: Issues formal payment requests to Finance for Advance Payment or Bill of Lading settlement.
- **Controls**: Pulls supplier bank SWIFT/IBAN from `MD-002`; enforces balance cap (`Requested + Previous Payments <= Total Invoice Value`).

---

### BP-013: Shipment Document Lifecycle Management
- **Purpose**: Tracks document versions (`Draft` -> `Final`) and physical chain of custody across Supplier, Forwarder, Company, Bank, and Broker.

---

### BP-014: ACID Request & Automated Verification
- **Purpose**: Manages Nafeza ACID number issuance and performs automated field-by-field verification between the ACID certificate and the Import File snapshot.
- **Verification Rule**: Importer Tax ID, Exporter Registration ID, Exporter Country, PI Number, and Port UN/LOCODE MUST match.

---

### BP-016: Freight Quotation Selection & Final Approval
- **Purpose**: Selects and locks the winning freight quote to auto-populate the draft Shipment Booking.

---

### BP-017: Shipment Booking Management & Multi-Container Charges
- **Purpose**: Manages booking confirmation, vessel allocation, container counts, and itemized freight charges (`Per Container` vs `Per Shipment`).

---

### BP-018: Cargo Loading Coordination & Container Seal Tracking
- **Purpose**: Audits actual container loading at supplier factory, capturing Container Numbers, Seal Numbers, and loaded carton counts.

---

### BP-019: Shipping Documents Review & Dual Approval Workflow
- **Purpose**: Implements mandatory **Dual Approval** for all final shipping documents.
- **Approvers**:
  1. `Import Operations Manager`
  2. `Licensed Customs Broker`
- **Rule**: Documents cannot be marked `Final` without both approvals recorded in the audit trail.

---

### BP-020: Original Documents Collection & Courier Tracking
- **Purpose**: Tracks dispatch and receipt of physical hardcopy documents via courier (DHL, FedEx, Aramex) with tracking numbers and receipt timestamps.

---

### BP-021: Electronic Document Exchange (CargoX / Blockchain Agnostic)
- **Purpose**: Manages electronic document verification and submission via blockchain providers (e.g., CargoX).
- **Validation Engine**: Runs `Document Verification Rules` checking Shipper Name, Importer Tax ID, ACID Number, Currency, Package Count, HS Code, and Invoice Total prior to blockchain upload.
