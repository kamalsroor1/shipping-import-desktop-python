---
name: pyside6-gui-development
description: Guidelines and best practices for building responsive, modern PySide6 (Qt 6) Desktop GUI applications with QTableWidgets, async threads, styling, and forms.
---

# PySide6 GUI Development Best Practices

Guidelines for creating robust Desktop ERP interfaces using PySide6 (Qt 6 for Python).

## Core Principles

1. **Keep the Main Thread Free**: Never perform long database queries or HTTP network requests on the main UI loop. Use `QThread` or `QRunnable` with `Signal` and `Slot` for async work.
2. **Dynamic UI Construction**: Use layout managers (`QVBoxLayout`, `QHBoxLayout`, `QGridLayout`, `QFormLayout`) instead of fixed pixel positions.
3. **QTableWidget & Data Binding**:
   - Set column header auto-stretch: `table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)`.
   - Use `QTableWidgetItem` with proper flags for read-only vs editable cells.
4. **Validation & Feedback**:
   - Provide immediate visual feedback (red border / QToolTip / QMessageBox) when input validation fails.
   - Disable action buttons while processing transactions.
5. **QSS Styling**: Use central CSS-like stylesheets (QSS) for harmonious dark/light themes across all dialogs and widgets.
