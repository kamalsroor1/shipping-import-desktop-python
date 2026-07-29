"""
Enterprise Theme System — Import Management System
Comprehensive QSS definitions for Light Theme ☀️ and Dark Mode 🌙.
Includes explicit QMessageBox styling for 100% readable alerts in both themes.
DESIGN_RULES.md Section 3 & Section 13
"""

LIGHT_QSS = """
/* ═══════════════════════════════════════════════════════════
   LIGHT THEME ☀️
   ═══════════════════════════════════════════════════════════ */
* {
    font-family: "Cairo", "Segoe UI", sans-serif;
    font-size: 13px;
    color: #2c3e50;
    outline: none;
    border: none;
    margin: 0;
    padding: 0;
}

QMainWindow, QDialog, QWidget#centralwidget, QWidget#contentArea {
    background-color: #ecf0f1;
}

/* MESSAGE BOX ALERTS */
QMessageBox {
    background-color: #ffffff;
}
QMessageBox QLabel {
    color: #2c3e50;
    font-size: 13px;
    font-weight: bold;
    background: transparent;
    padding: 8px;
}
QMessageBox QPushButton {
    background-color: #16a085;
    color: #ffffff;
    font-size: 13px;
    font-weight: bold;
    min-width: 90px;
    min-height: 32px;
    border-radius: 4px;
    border: none;
}
QMessageBox QPushButton:hover {
    background-color: #1abc9c;
}

/* Views Container Background */
QWidget {
    background-color: transparent;
}

/* SCROLLBARS */
QScrollBar:vertical {
    background: #ecf0f1;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #bdc3c7;
    border-radius: 4px;
    min-height: 24px;
}
QScrollBar::handle:vertical:hover {
    background: #7f8c8d;
}

/* TOP INFO BAR */
QFrame#infoBar {
    background-color: #1a252f;
    border-bottom: 1px solid #111820;
    min-height: 32px;
    max-height: 32px;
}
QLabel#infoBarLabel {
    color: #ffffff;
    font-size: 11px;
    font-weight: 600;
    background: transparent;
    padding: 0 12px;
}
QLabel#clockLabel {
    color: #38ef7d;
    font-size: 11px;
    font-weight: 700;
    background: transparent;
    padding: 0 12px;
}

/* MENU BAR */
QMenuBar {
    background-color: #ffffff;
    border-bottom: 2px solid #16a085;
    font-size: 13px;
    font-weight: 700;
    padding: 4px 8px;
}
QMenuBar::item {
    background: transparent;
    padding: 6px 14px;
    border-radius: 4px;
    color: #2c3e50;
}
QMenuBar::item:selected {
    background-color: #ecf0f1;
    color: #16a085;
}
QMenu {
    background-color: #ffffff;
    border: 1px solid #bdc3c7;
    border-radius: 6px;
    padding: 6px;
    color: #2c3e50;
}
QMenu::item {
    padding: 8px 24px 8px 16px;
    font-size: 13px;
    border-radius: 4px;
    color: #2c3e50;
}
QMenu::item:selected {
    background-color: #16a085;
    color: #ffffff;
}

/* TAB WORKSPACE */
QTabWidget::pane {
    border: 1px solid #dfe6e9;
    background: #ecf0f1;
}
QTabBar::tab {
    background: #2c3e50;
    color: #ffffff;
    padding: 8px 18px;
    font-weight: bold;
    border-radius: 4px 4px 0 0;
    margin-right: 3px;
    min-width: 130px;
}
QTabBar::tab:selected {
    background: #16a085;
    color: #ffffff;
    border-top: 3px solid #1abc9c;
}
QTabBar::tab:hover:!selected {
    background: #34495e;
}

/* LABELS */
QLabel {
    color: #2c3e50;
    background: transparent;
}

/* BUTTONS */
QPushButton {
    font-family: "Cairo", "Segoe UI", sans-serif;
    font-size: 13px;
    font-weight: bold;
    min-height: 36px;
    padding: 0 16px;
    border-radius: 4px;
    border: 1px solid #bdc3c7;
    background-color: #ffffff;
    color: #2c3e50;
}
QPushButton:hover {
    background-color: #dfe6e9;
    border-color: #7f8c8d;
}

/* INPUTS */
QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {
    font-family: "Cairo", "Segoe UI", sans-serif;
    font-size: 13px;
    background-color: #ffffff;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    padding: 0 12px;
    color: #2c3e50;
    min-height: 36px;
}
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
    border: 2px solid #16a085;
}

/* TABLES */
QTableWidget, QTableView {
    background-color: #ffffff;
    border: 1px solid #dfe6e9;
    border-radius: 6px;
    gridline-color: transparent;
    alternate-background-color: #f8f9fa;
    selection-background-color: rgba(22,160,133,0.15);
    selection-color: #2c3e50;
    font-size: 12px;
    color: #2c3e50;
}
QTableWidget::item, QTableView::item {
    padding: 0 16px;
    min-height: 40px;
    border-bottom: 1px solid #dfe6e9;
    color: #2c3e50;
    background-color: #ffffff;
}
QHeaderView::section {
    background-color: #34495e;
    color: #ffffff;
    font-size: 12px;
    font-weight: bold;
    padding: 0 16px;
    height: 38px;
    border: none;
}

/* GROUP BOX */
QGroupBox {
    background-color: #ffffff;
    border: 1px solid #dfe6e9;
    border-radius: 6px;
    margin-top: 22px;
    padding: 16px;
    font-size: 14px;
    font-weight: bold;
    color: #2c3e50;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top right;
    padding: 3px 10px;
    right: 16px;
    background-color: #ffffff;
    color: #34495e;
    border-radius: 3px;
}
"""

DARK_QSS = """
/* ═══════════════════════════════════════════════════════════
   DARK MODE 🌙
   ═══════════════════════════════════════════════════════════ */
* {
    font-family: "Cairo", "Segoe UI", sans-serif;
    font-size: 13px;
    color: #f8fafc;
    outline: none;
    border: none;
    margin: 0;
    padding: 0;
}

QMainWindow, QDialog, QWidget#centralwidget, QWidget#contentArea {
    background-color: #0f172a;
}

/* MESSAGE BOX ALERTS */
QMessageBox {
    background-color: #1e293b;
}
QMessageBox QLabel {
    color: #f8fafc;
    font-size: 13px;
    font-weight: bold;
    background: transparent;
    padding: 8px;
}
QMessageBox QPushButton {
    background-color: #0284c7;
    color: #ffffff;
    font-size: 13px;
    font-weight: bold;
    min-width: 90px;
    min-height: 32px;
    border-radius: 4px;
    border: none;
}
QMessageBox QPushButton:hover {
    background-color: #38bdf8;
}

/* Views Container Background */
QWidget {
    background-color: transparent;
}

/* SCROLLBARS */
QScrollBar:vertical {
    background: #0f172a;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #334155;
    border-radius: 4px;
    min-height: 24px;
}
QScrollBar::handle:vertical:hover {
    background: #475569;
}

/* TOP INFO BAR */
QFrame#infoBar {
    background-color: #020617;
    border-bottom: 1px solid #1e293b;
    min-height: 32px;
    max-height: 32px;
}
QLabel#infoBarLabel {
    color: #f8fafc;
    font-size: 11px;
    font-weight: 600;
    background: transparent;
    padding: 0 12px;
}
QLabel#clockLabel {
    color: #38ef7d;
    font-size: 11px;
    font-weight: 700;
    background: transparent;
    padding: 0 12px;
}

/* MENU BAR */
QMenuBar {
    background-color: #1e293b;
    border-bottom: 2px solid #38bdf8;
    font-size: 13px;
    font-weight: 700;
    padding: 4px 8px;
}
QMenuBar::item {
    background: transparent;
    padding: 6px 14px;
    border-radius: 4px;
    color: #f8fafc;
}
QMenuBar::item:selected {
    background-color: #334155;
    color: #38bdf8;
}
QMenu {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 6px;
    color: #f8fafc;
}
QMenu::item {
    padding: 8px 24px 8px 16px;
    font-size: 13px;
    border-radius: 4px;
    color: #f8fafc;
}
QMenu::item:selected {
    background-color: #0284c7;
    color: #ffffff;
}

/* TAB WORKSPACE */
QTabWidget::pane {
    border: 1px solid #334155;
    background: #0f172a;
}
QTabBar::tab {
    background: #1e293b;
    color: #94a3b8;
    padding: 8px 18px;
    font-weight: bold;
    border-radius: 4px 4px 0 0;
    margin-right: 3px;
    min-width: 130px;
}
QTabBar::tab:selected {
    background: #0284c7;
    color: #ffffff;
    border-top: 3px solid #38bdf8;
}
QTabBar::tab:hover:!selected {
    background: #334155;
    color: #f8fafc;
}

/* LABELS */
QLabel {
    color: #f8fafc;
    background: transparent;
}

/* BUTTONS */
QPushButton {
    font-family: "Cairo", "Segoe UI", sans-serif;
    font-size: 13px;
    font-weight: bold;
    min-height: 36px;
    padding: 0 16px;
    border-radius: 4px;
    border: 1px solid #334155;
    background-color: #1e293b;
    color: #ffffff;
}
QPushButton:hover {
    background-color: #334155;
    border-color: #38bdf8;
}

/* INPUTS */
QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {
    font-family: "Cairo", "Segoe UI", sans-serif;
    font-size: 13px;
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 4px;
    padding: 0 12px;
    color: #ffffff;
    min-height: 36px;
}
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
    border: 2px solid #38bdf8;
}

/* TABLES */
QTableWidget, QTableView {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    gridline-color: transparent;
    alternate-background-color: #0f172a;
    selection-background-color: rgba(56,189,248,0.25);
    selection-color: #ffffff;
    font-size: 12px;
    color: #ffffff;
}
QTableWidget::item, QTableView::item {
    padding: 0 16px;
    min-height: 40px;
    border-bottom: 1px solid #334155;
    color: #f8fafc;
    background-color: #1e293b;
}
QHeaderView::section {
    background-color: #0f172a;
    color: #38bdf8;
    font-size: 12px;
    font-weight: bold;
    padding: 0 16px;
    height: 38px;
    border: none;
    border-right: 1px solid #1e293b;
}

/* GROUP BOX */
QGroupBox {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    margin-top: 22px;
    padding: 16px;
    font-size: 14px;
    font-weight: bold;
    color: #f8fafc;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top right;
    padding: 3px 10px;
    right: 16px;
    background-color: #1e293b;
    color: #38bdf8;
    border-radius: 3px;
}
"""


class UITheme:
    current_theme = "light"

    @classmethod
    def get_style(cls) -> str:
        return DARK_QSS if cls.current_theme == "dark" else LIGHT_QSS

    @classmethod
    def toggle_theme(cls) -> str:
        cls.current_theme = "dark" if cls.current_theme == "light" else "light"
        return cls.current_theme

    MAIN_STYLE_QSS = LIGHT_QSS
