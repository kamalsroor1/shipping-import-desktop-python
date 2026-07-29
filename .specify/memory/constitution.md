# Project Constitution & Architectural Rules: Import Operations Management Platform

## Principle 1: Pure Python & PySide6 Desktop Stack
The application is built 100% using the Python Desktop Ecosystem:
- **Core Runtime**: Python 3.13
- **GUI Engine**: PySide6 (Qt 6.8+) with native widgets, QThread concurrency, and dark theme QSS.
- **Persistence**: SQLite 3 with SQLAlchemy 2.0 ORM.
- **Reporting**: ReportLab (PDF) and openpyxl (Excel).
- **Packaging**: Single-file PyInstaller executable (`IMS.exe`) and Inno Setup installer.

---

## Principle 2: Architectural Patterns & Pythonic Design Patterns

The codebase strictly adheres to standard **Pythonic Design Patterns**:

| Pattern Category | Pattern Name | Core Purpose | Pythonic Implementation Advantage |
| :--- | :--- | :--- | :--- |
| **Creational** | **Factory Method** | Decouple object creation logic | Use functions / callables directly instead of custom creator classes. |
| **Creational** | **Singleton** | Guarantee exactly one instance of a class | Easily achieved natively by importing a module or using a metaclass. |
| **Structural** | **Decorator** | Add behavior to an object dynamically | Built into Python syntax via the `@decorator` symbol. |
| **Structural** | **Adapter** | Make incompatible interfaces work together | Simplified natively by Python's dynamic duck typing. |
| **Behavioral** | **Strategy** | Swap interchangeable algorithms at runtime | Avoids complex class trees by passing functions as parameters. |
| **Behavioral** | **Observer** | Notify multiple objects of state changes | Frequently built using simple callback lists or Qt Signals & Slots. |

---

## Principle 3: Model-View-Controller (MVC) & PySide6 Model/View Architecture

The application enforces strict separation of concerns using the **Model-View-Controller (MVC)** architectural pattern:

```
+------------------+         Signals & Events         +-----------------------+
|   PySide6 View   |  ------------------------------> |  Controller / Presenter|
|  (User Interface)|                                  |  (Application Logic)  |
+------------------+  <------------------------------ +-----------------------+
         ^                   UI Update / Refresh                  |
         |                                                        |
         +------------------ Data Updates / State ----------------+
                                                                  v
                                                      +-----------------------+
                                                      |     Domain Model      |
                                                      | (Data & Business Logic|
                                                      +-----------------------+
```

### 1. Model (Data & Domain Logic)
- Responsible exclusively for data persistence, SQLAlchemy ORM models, DB queries, and business calculations (CBM, Container Loading, Duty Estimations).
- **Zero GUI Dependency**: Must never import `PySide6.QtWidgets` or reference UI elements.

### 2. View (User Interface & Presentation)
- Responsible exclusively for layout structure, buttons, inputs, tables, dialogs, and QSS styling.
- **Zero Business Logic**: Must never perform direct DB writes or business calculations. Sends user interaction events via Qt Signals (`Signal`, `Slot`).

### 3. Controller / Presenter (Operational Bridge)
- Acts as the operational bridge connecting Views and Models.
- Listens to UI signals, calls Model methods / services, handles async `QThread` execution, and updates View widgets reactively.

### 4. PySide6 Model/View Native Alignment
- Utilizes PySide6 native `QAbstractTableModel`, `QTableView`, `QDataWidgetMapper`, and `Signal/Slot` event dispatchers for reactive table binding.

---

## Principle 4: Data-Driven Master Data Integrity
- All reference entities (Companies, Foreign Exporters, Service Providers, Incoterms Matrix, Customs Tariffs, Containers, Transport Locations) MUST be managed via Master Data tables.
- Transactional records (Import Files, Items, ACID Requests, Bookings) MUST reference Master Data IDs. Direct hardcoded string entry inside transactions is strictly prohibited.

---

## Principle 5: Flexible Egyptian Import Workflow
- Operational milestones follow the 15-stage Egyptian import lifecycle.
- Milestones act as **Operational Milestones** allowing milestone skipping, pausing, or backtracking based on shipment characteristics.
- Mandatory controls (e.g., Nafeza ACID Verification before Booking, Form 4 before Clearance) require explicit administrative authorization and audit log justification if overridden.
