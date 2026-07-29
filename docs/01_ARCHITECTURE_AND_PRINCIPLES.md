# 01. System Architecture & General Design Principles

## 1. System Vision: Import Operations Management Platform

The **Import Operations Management Platform** is an intelligent operational system designed specifically for import management teams in Egypt. Unlike traditional ERPs or static data entry tools, this platform focuses on **operational execution, real-time tracking, proactive decision support, and guided workflow execution**.

---

## 2. Core System Design Philosophy

### 2.1 Flexible Workflow Architecture
The system employs a **Flexible Workflow Engine**. Import operational milestones do not enforce rigid, linear progression across all shipments. Instead, phases act as **Operational Milestones** that accommodate operational variance based on:
- Shipment Mode (Ocean FCL/LCL, Air, Road).
- Supplier & Freight Forwarder constraints.
- Egyptian Customs (Nafeza, GOEIC) & Central Bank of Egypt (Form 4) regulations.

#### Key Rules:
1. **Milestone Flexibility**: Shipments can pause, resume, or skip non-mandatory milestones.
2. **Backtracking**: Allowed when document revisions or re-consultations occur.
3. **Mandatory Controls**: Mandatory milestones (e.g., ACID Verification before Booking, Form 4 before Customs Clearance) require administrative override with recorded justification if bypassed.
4. **Historical Event Log**: Every state transition is recorded in an immutable audit trail.

---

### 2.2 Operational State Management
Rather than tying a shipment's state to a specific UI screen, each import file possesses a unified **Current Operational State**.

```
[Pre-Shipment] ➔ [PI Review] ➔ [ACID Verified] ➔ [Booking Confirmed] ➔ [Form 4 Issued] ➔ [Clearance] ➔ [Warehouse Received] ➔ [Closed]
```

#### Status Indicators:
- **Current Stage**: (e.g., `Booking Confirmed`)
- **Waiting For**: (e.g., `Draft Bill of Lading`, `Bank Form 4 SWIFT`)
- **Blocking Requirements**: Unresolved Action Items or missing mandatory documents.

---

### 2.3 Operational Workspace (Daily Command Center)
The central operational dashboard serves as the daily entry point for import managers:
- **Today's Tasks**: High-priority tasks scheduled for execution today.
- **Pending Tasks**: Incomplete operational tasks.
- **Upcoming Shipments**: Shipments scheduled for departure or arrival.
- **Arriving This Week**: Shipments nearing port of discharge.
- **ETA Changes**: Alerts for modified sailing/arrival dates.
- **Waiting For Payment**: Shipments stalled due to pending financial transfers.
- **Waiting For Form 4**: Shipments awaiting bank Form 4 approval.
- **Pending Requirements**: Shipments with open GOEIC, NTRA, or Document remarks.
- **High-Priority Alerts**: Urgent delays, expiring licenses, or ACID expiry warnings.

---

### 2.4 Smart Task Management Engine
Splits tasks into two distinct categories:

#### A. System Generated Tasks (Automated Engine)
Triggered automatically by state transitions, upcoming deadlines, or milestone events:
- *Examples*: "Review Draft B/L within 24h", "Request Form 4 from Bank", "Audit CargoX Uploaded COO".
- Closed automatically when the associated milestone or document requirement is fulfilled.

#### B. Manual To-Do List
Allows operational users to create custom tasks and internal reminders:
- Title, Description, Related Import File, Assigned User, Priority, Due Date, Reminder Date, Status, Notes.

---

### 2.5 Reminder & Alert Engine
Proactive notification engine for critical follow-ups:
- Supplier Production & Cargo Ready Date (CRD) follow-ups.
- Central Bank & Form 4 processing status.
- Freight Forwarder ETD/ETA changes & Cut-Off deadlines.
- Customs Broker review & assessment deadlines.
- Expiration of Legal Master Data (Importer License, VAT Registration, Commercial Registration).

---

### 2.6 Milestone Progress & Visual Tracking
Visual progress indicators showing completed, active, and remaining milestones across all active import files.

---

### 2.7 Dynamic Reporting Engine
Data-driven reporting engine allowing users to build, filter, sort, group, save templates, and export custom reports:
- Selected & Reordered Columns.
- Dynamic Filters & Groupings.
- Live Data Aggregations (Total PI Value, Total CBM, Average Clearance Days).
- One-click export to Excel (`.xlsx`) and PDF (`.pdf`).

---

### 2.8 Audit Trail & System Traceability
Complete history of all actions executed on any import file:
- User ID, Timestamp, Action Type, Screen/Module Name, Previous Value, New Value, Justification Notes.

---

## 3. General System Principles (GP-001 to GP-004)

### GP-001: Progressive Data Entry
- Import files can be created with minimal initial information (e.g., Supplier & Proforma Invoice Number).
- Fields are populated progressively as documents arrive.
- The system only blocks actions dependent on missing data (e.g., CBM calculation is blocked until carton dimensions are provided).

### GP-002: Stage-Based Validation
- Validations are context-aware and evaluated at operational execution time, not during draft saving.

### GP-003: Editable Import Files with Version Control
- Import files remain open for modifications until explicitly marked `Closed`.
- Revisions to Proforma Invoices or Packing Lists preserve historical snapshots and update modification metadata:
  - `Last Modified By`, `Last Modified Date`, `Version Number`, `Modification Notes`.

### GP-004: Comprehensive Audit Log
- All key events (creation, edits, approvals, deletions, document uploads, state transitions) are recorded in an audit trail.
