# Project Constitution: Import Operations Management Platform

## Principle 1: Pure Python & PySide6 Desktop Stack
The application is built 100% using the Python Desktop Ecosystem:
- **Core Runtime**: Python 3.13
- **GUI Engine**: PySide6 (Qt 6.8+) with native widgets, QThread concurrency, and dark theme QSS.
- **Persistence**: SQLite 3 with SQLAlchemy 2.0 ORM.
- **Reporting**: ReportLab (PDF) and openpyxl (Excel).
- **Packaging**: Single-file PyInstaller executable (`IMS.exe`) and Inno Setup installer.

*Violation Rule*: No web frameworks (React, Next.js, Node.js) or secondary programming languages are permitted.

---

## Principle 2: Data-Driven Master Data Integrity
- All reference entities (Companies, Foreign Exporters, Service Providers, Incoterms Matrix, Customs Tariffs, Containers, Transport Locations) MUST be managed via Master Data tables.
- Transactional records (Import Files, Items, ACID Requests, Bookings) MUST reference Master Data IDs. Direct hardcoded string entry inside transactions is strictly prohibited.

---

## Principle 3: Flexible Egyptian Import Workflow
- Operational milestones follow the 15-stage Egyptian import lifecycle.
- Milestones act as **Operational Milestones** allowing milestone skipping, pausing, or backtracking based on shipment characteristics (Ocean FCL/LCL, Air, Road).
- Mandatory controls (e.g., Nafeza ACID Verification before Booking, Form 4 before Clearance) require explicit administrative authorization and audit log justification if overridden.

---

## Principle 4: Local Workspace Safety & Versioning
- No code commits or `git push` actions shall be executed without explicit user instruction.
- Import Files and Documents maintain complete audit trails and version history (`Last Modified By`, `Last Modified Date`, `Version Number`, `Modification Notes`).
