---
name: import-domain-rules
description: Business rules, calculations, and domain logic for the Egyptian Import Management System including CBM, Incoterms, Duties Estimation, and Audit Trails.
---

# Import Domain Rules & Business Logic

Core business calculation rules and validations for the Import Management System.

## Key Rules & Formulas

### 1. GP-001 Progressive Data Entry
- Allow creating Import Files and Packing Lists without dimensions (Length, Width, Height, Unit Price).
- Block ONLY actions dependent on missing data (e.g. block `Calculate CBM` until dimensions are entered).

### 2. GP-003 & GP-004 Audit Trail & Modification Tracking
- Every modification to an Import File must update `last_modified_by`, `last_modified_date`, and log an entry into `audit_log`.

### 3. CBM & Weight Calculations (BP-004)
- **Ocean CBM Formula**:
  $$CBM = \frac{Qty \times Length(cm) \times Width(cm) \times Height(cm)}{1,000,000}$$
- **Air Chargeable Weight Formula**:
  $$Chargeable Weight (kg) = \frac{Qty \times Length(cm) \times Width(cm) \times Height(cm)}{6,000}$$

### 4. Customs Duties Estimation (BP-008)
- Duties are calculated per HS Code line.
- Snapshot current `customs_duty_pct`, `vat_pct` (14%), and `development_tax_pct` onto `customs_duty_estimates` at calculation time so historical estimates remain unaffected by future tariff changes.

### 5. Payment Requests (BP-009)
- Total requested amounts for a Proforma Invoice must not exceed `total_value`.
- Require administrative approval if Supplier Bank Details differ from Master Data.
