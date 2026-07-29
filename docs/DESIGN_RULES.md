# Architectural Design Rules & Pythonic Design Patterns

## 1. Comparison of Key Design Patterns

| Pattern Category | Pattern Name | Core Purpose | Pythonic Implementation Advantage |
| :--- | :--- | :--- | :--- |
| **Creational** | **Factory Method** | Decouple object creation logic | Use functions / callables directly instead of custom creator classes. |
| **Creational** | **Singleton** | Guarantee exactly one instance of a class | Easily achieved natively by importing a module or using a metaclass. |
| **Structural** | **Decorator** | Add behavior to an object dynamically | Built into Python syntax via the `@decorator` symbol. |
| **Structural** | **Adapter** | Make incompatible interfaces work together | Simplified natively by Python's dynamic duck typing. |
| **Behavioral** | **Strategy** | Swap interchangeable algorithms at runtime | Avoids complex class trees by passing functions as parameters. |
| **Behavioral** | **Observer** | Notify multiple objects of state changes | Frequently built using simple callback lists or Qt Signals & Slots. |

---

## 2. Model-View-Controller (MVC) Architecture in PySide6

The application strictly separates responsibilities into three distinct layers:

### 🧱 Component Breakdown
1. **Model (`src/database/models/` & `src/services/`)**:
   - Manages data schema, SQLAlchemy ORM entities, database queries, and pure business logic (CBM, Container Loading, Duty Estimations).
   - **Rule**: Completely independent of PySide6 UI widgets.

2. **View (`src/ui/views/` & `src/ui/components/`)**:
   - Manages visual UI widgets, layouts, QSS stylesheets, dialogs, forms, and tables.
   - **Rule**: Contains no business logic or SQL queries. Emits PySide6 `Signal` events upon user actions.

3. **Controller / Presenter (`src/ui/controllers/` or View Handlers)**:
   - Connects View signals to Model functions.
   - Handles async operations via `QThread` to prevent UI looper blocking.
   - Reactively updates View elements upon Model updates.

---

## 3. Benefits Enforced
- **Isolated Unit Testing**: Models can be tested with `pytest` without launching GUI dialogs.
- **Code Reusability**: Views can be redesigned or swapped without touching business logic or DB models.
- **Team Maintainability**: Clean, decoupled, scalable Python code.
