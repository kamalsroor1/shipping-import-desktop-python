"""
Main Window — Import Management System
Dynamic Multi-Tab Workspace Engine with Pure i18n (Arabic / English)
DESIGN_RULES.md Section 3, Section 13, Section 15.5
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFrame, QTabWidget, QTabBar, QToolButton,
    QMenu, QMenuBar, QMessageBox, QScrollArea
)
from PySide6.QtCore import Qt, QTime, QTimer
from PySide6.QtGui import QFont, QAction, QShortcut, QKeySequence

from src.database.session import init_db
from src.ui.styles.theme import UITheme
from src.ui.styles.tokens import *
from src.utils.i18n import i18n
from src.ui.views.dashboard_view import DashboardView
from src.ui.views.master_data_view import MasterDataView
from src.ui.views.operations_view import OperationsView
from src.ui.views.finance_view import FinanceView
from src.ui.views.settings_view import SettingsView


class MetroTileCard(QFrame):
    """High-contrast Metro Tile Card with dynamic pure i18n text."""

    def __init__(self, key_ar: str, key_en: str, color: str,
                 icon: str, view_key: str, click_callback, parent=None):
        super().__init__(parent)
        self.view_key = view_key
        self.key_ar = key_ar
        self.key_en = key_en
        self.click_callback = click_callback
        self.base_color = color

        self.setFixedSize(190, 130)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.set_style(hover=False)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 14, 12, 12)
        lay.setSpacing(4)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lbl_icon = QLabel(icon)
        self.lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_icon.setFont(QFont("Segoe UI Emoji", 26))
        self.lbl_icon.setStyleSheet("color: #ffffff; background: transparent; border: none;")

        self.lbl_title = QLabel(key_ar if i18n.current_lang == "ar" else key_en)
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_title.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        self.lbl_title.setStyleSheet("color: #ffffff; background: transparent; border: none;")
        self.lbl_title.setWordWrap(True)

        lay.addWidget(self.lbl_icon)
        lay.addWidget(self.lbl_title)

    def set_style(self, hover: bool):
        border_css = "border: 2px solid #ffffff;" if hover else "border: 1px solid rgba(255,255,255,0.25);"
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {self.base_color};
                border-radius: 6px;
                {border_css}
            }}
        """)

    def enterEvent(self, event):
        self.set_style(hover=True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.set_style(hover=False)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            title = self.key_ar if i18n.current_lang == "ar" else self.key_en
            self.click_callback(self.view_key, title)
        super().mousePressEvent(event)


class DynamicHomeScreen(QWidget):
    """Metro Tile Landing Page with direct action launchers."""

    def __init__(self, open_tab_callback, parent=None):
        super().__init__(parent)
        self.open_tab_callback = open_tab_callback
        self._build()

    def _build(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        scroll.setWidget(container)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(20)

        # Welcome Banner
        banner = QFrame()
        banner.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        banner.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-radius: 8px;
                border: 1px solid #1a252f;
            }
        """)
        banner.setMinimumHeight(96)
        bl = QHBoxLayout(banner)
        bl.setContentsMargins(24, 16, 24, 16)

        tb = QVBoxLayout()
        tb.setSpacing(4)
        t1 = QLabel(i18n.t("welcome_title"))
        t1.setFont(QFont("Cairo", 15, QFont.Weight.Bold))
        t1.setStyleSheet("color:#ffffff; background:transparent; border:none;")

        t2 = QLabel(i18n.t("welcome_subtitle"))
        t2.setFont(QFont("Cairo", 11))
        t2.setStyleSheet("color:#bdc3c7; background:transparent; border:none;")

        tb.addWidget(t1)
        tb.addWidget(t2)
        bl.addLayout(tb)
        bl.addStretch()

        logo = QLabel("📦")
        logo.setFont(QFont("Segoe UI Emoji", 36))
        logo.setStyleSheet("background: transparent; border:none;")
        bl.addWidget(logo)
        layout.addWidget(banner)

        # Section 1: Quick Actions
        self._add_section(layout, i18n.t("quick_actions_header"), [
            ("tile_new_file_ar", "tile_new_file_en", "#27ae60", "📦", "ops"),
            ("tile_new_pay_ar", "tile_new_pay_en", "#2980b9", "💳", "finance"),
            ("tile_add_supplier_ar", "tile_add_supplier_en", "#8e44ad", "🏭", "master"),
            ("tile_cbm_calc_ar", "tile_cbm_calc_en", "#d35400", "🧾", "ops"),
        ])

        # Section 2: Main Modules
        self._add_section(layout, i18n.t("main_modules_header"), [
            ("tile_dashboard_ar", "tile_dashboard_en", "#34495e", "📊", "dashboard"),
            ("tile_companies_ar", "tile_companies_en", "#16a085", "🏢", "master"),
            ("tile_partners_ar", "tile_partners_en", "#2980b9", "🤝", "master"),
            ("tile_settings_ar", "tile_settings_en", "#7f8c8d", "⚙️", "settings"),
        ])

        layout.addStretch()

    def _add_section(self, parent_layout, title: str, tiles):
        hdr = QLabel(title)
        hdr.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        hdr.setStyleSheet("""
            color: #38bdf8;
            font-size: 13px;
            font-weight: bold;
            background: transparent;
            border-left: 4px solid #16a085;
            padding-left: 10px;
        """)
        parent_layout.addWidget(hdr)

        grid = QHBoxLayout()
        grid.setSpacing(16)
        grid.setAlignment(Qt.AlignmentFlag.AlignLeft)

        for ar_key, en_key, color, icon, view_key in tiles:
            tile_card = MetroTileCard(
                key_ar=i18n.t(ar_key),
                key_en=i18n.t(en_key),
                color=color,
                icon=icon,
                view_key=view_key,
                click_callback=self.open_tab_callback
            )
            grid.addWidget(tile_card)

        parent_layout.addLayout(grid)


class InfoBar(QFrame):
    """Top info strip."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("infoBar")
        self.setFixedHeight(32)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(0)

        self._user_lbl  = QLabel()
        self._comp_lbl  = QLabel()
        self._ver_lbl   = QLabel()
        self._time_lbl  = QLabel("🕐  --:--:--")

        for lbl in (self._user_lbl, self._comp_lbl, self._ver_lbl, self._time_lbl):
            lbl.setFont(QFont(FONT_ARABIC, 11, QFont.Weight.Bold))
            lbl.setStyleSheet("color: #ffffff; background: transparent; padding: 0 14px; border: none;")

        self._time_lbl.setStyleSheet("color: #38ef7d; font-weight: bold; background: transparent; padding: 0 14px; border: none;")

        layout.addWidget(self._user_lbl)
        layout.addWidget(self._vdiv())
        layout.addWidget(self._comp_lbl)
        layout.addStretch()
        layout.addWidget(self._ver_lbl)
        layout.addWidget(self._vdiv())
        layout.addWidget(self._time_lbl)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(1000)
        self._tick()
        self.retranslate()

    def _vdiv(self) -> QFrame:
        f = QFrame()
        f.setFrameShape(QFrame.Shape.VLine)
        f.setStyleSheet("background: #34495e; max-width: 1px; margin: 6px 0; border: none;")
        return f

    def _tick(self):
        t = QTime.currentTime().toString("hh:mm:ss")
        self._time_lbl.setText(f"🕐  {t}")

    def retranslate(self):
        self._user_lbl.setText(f"👤  {i18n.t('system_admin')}")
        self._comp_lbl.setText(f"🏢  {i18n.t('company_name')}")
        self._ver_lbl.setText(i18n.t('version'))


class MainWindow(QMainWindow):
    """Main Window featuring Sahl ERP Multi-Tab Workspace Architecture with Pure i18n."""

    def __init__(self):
        super().__init__()
        self.resize(1440, 860)
        self.setMinimumSize(1280, 720)

        init_db()

        # Shell
        shell = QWidget()
        shell.setObjectName("centralwidget")
        self.setCentralWidget(shell)

        shell_layout = QVBoxLayout(shell)
        shell_layout.setContentsMargins(0, 0, 0, 0)
        shell_layout.setSpacing(0)

        self._info_bar = InfoBar()
        shell_layout.addWidget(self._info_bar)

        # Multi-Tab Workspace Bar
        self.tab_counter = 1
        self.workspace_tabs = QTabWidget()
        self.workspace_tabs.setTabsClosable(True)
        self.workspace_tabs.setMovable(True)
        self.workspace_tabs.tabCloseRequested.connect(self._close_tab)

        # Plus (+) button to open new tab menu
        self.add_tab_btn = QToolButton()
        self.add_tab_btn.setText("  +  ")
        self.add_tab_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.add_tab_btn.setToolTip("فتح تبويب جديد")
        self.add_tab_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_tab_btn.setStyleSheet("""
            QToolButton {
                background-color: #16a085;
                color: #ffffff;
                border-radius: 4px;
                padding: 4px 10px;
                margin: 4px;
                font-weight: bold;
            }
            QToolButton:hover {
                background-color: #1abc9c;
            }
        """)
        self.add_tab_btn.clicked.connect(self._show_new_tab_menu)
        self.workspace_tabs.setCornerWidget(self.add_tab_btn, Qt.Corner.TopLeftCorner)

        # Permanent Landing Tab
        self.home_tab_widget = DynamicHomeScreen(open_tab_callback=self.open_new_sub_screen)
        idx = self.workspace_tabs.addTab(self.home_tab_widget, i18n.t("home_tab"))
        self.workspace_tabs.tabBar().setTabButton(idx, QTabBar.ButtonPosition.RightSide, None)

        shell_layout.addWidget(self.workspace_tabs, 1)

        self._build_menubar()

        # Shortcut Ctrl+W
        self.shortcut_close = QShortcut(QKeySequence("Ctrl+W"), self)
        self.shortcut_close.activated.connect(self._close_current_tab)

        # Status Bar
        self.sb_label = QLabel()
        self.sb_label.setFont(QFont(FONT_ARABIC, 11))
        self.sb_label.setStyleSheet("color: #7f8c8d;")
        self.statusBar().addWidget(self.sb_label)
        self.retranslate_ui()

    def open_new_sub_screen(self, view_key: str, title: str):
        """Opens a brand new independent sub-screen tab instance."""
        if view_key == "dashboard":
            view_instance = DashboardView(navigate_callback=self.open_new_sub_screen)
        elif view_key == "master":
            view_instance = MasterDataView()
        elif view_key == "ops":
            view_instance = OperationsView()
        elif view_key == "finance":
            view_instance = FinanceView()
        elif view_key == "settings":
            view_instance = SettingsView(
                toggle_theme_callback=self.toggle_theme,
                toggle_lang_callback=self.toggle_language
            )
        else:
            view_instance = DashboardView(navigate_callback=self.open_new_sub_screen)

        tab_title = f"{title} #{self.tab_counter}"
        self.tab_counter += 1

        idx = self.workspace_tabs.addTab(view_instance, tab_title)
        self.workspace_tabs.setCurrentIndex(idx)

    def _show_new_tab_menu(self):
        menu = QMenu(self)
        menu.setFont(QFont(FONT_ARABIC, 12))

        act_ops = QAction(f"📦  {i18n.t('ops_tab')}", self)
        act_ops.triggered.connect(lambda: self.open_new_sub_screen("ops", i18n.t("ops_tab")))

        act_fin = QAction(f"💰  {i18n.t('finance_tab')}", self)
        act_fin.triggered.connect(lambda: self.open_new_sub_screen("finance", i18n.t("finance_tab")))

        act_md = QAction(f"🏢  {i18n.t('master_tab')}", self)
        act_md.triggered.connect(lambda: self.open_new_sub_screen("master", i18n.t("master_tab")))

        act_dash = QAction(f"📊  {i18n.t('dashboard_tab')}", self)
        act_dash.triggered.connect(lambda: self.open_new_sub_screen("dashboard", i18n.t("dashboard_tab")))

        act_settings = QAction(f"⚙️  {i18n.t('settings_tab')}", self)
        act_settings.triggered.connect(lambda: self.open_new_sub_screen("settings", i18n.t("settings_tab")))

        menu.addAction(act_ops)
        menu.addAction(act_fin)
        menu.addAction(act_md)
        menu.addAction(act_dash)
        menu.addAction(act_settings)

        menu.exec(self.add_tab_btn.mapToGlobal(self.add_tab_btn.rect().bottomLeft()))

    def _close_tab(self, index: int):
        if index == 0:
            return
        widget = self.workspace_tabs.widget(index)
        self.workspace_tabs.removeTab(index)
        if widget:
            widget.deleteLater()

    def _close_current_tab(self):
        curr_idx = self.workspace_tabs.currentIndex()
        if curr_idx > 0:
            self._close_tab(curr_idx)

    def toggle_theme(self):
        UITheme.toggle_theme()
        QApplication.instance().setStyleSheet(UITheme.get_style())

    def toggle_language(self):
        i18n.toggle()
        self.retranslate_ui()

    def retranslate_ui(self):
        is_ar = (i18n.current_lang == "ar")
        direction = Qt.LayoutDirection.RightToLeft if is_ar else Qt.LayoutDirection.LeftToRight

        self.setLayoutDirection(direction)
        QApplication.setLayoutDirection(direction)

        self.setWindowTitle(f"{i18n.t('app_name')} v1.0")
        self._info_bar.retranslate()
        self.workspace_tabs.setTabText(0, i18n.t("home_tab"))

        self.menuBar().clear()
        self._build_menubar()
        self.sb_label.setText(f"✅  {i18n.t('connected')}  |  {i18n.t('app_name')} v1.0")

    def _build_menubar(self):
        mb = self.menuBar()
        is_ar = (i18n.current_lang == "ar")
        mb.setLayoutDirection(Qt.LayoutDirection.RightToLeft if is_ar else Qt.LayoutDirection.LeftToRight)
        mb.setFont(QFont(FONT_ARABIC, 13, QFont.Weight.Bold))

        def m(title: str) -> QMenu:
            menu = QMenu(title, self)
            menu.setLayoutDirection(mb.layoutDirection())
            menu.setFont(QFont(FONT_ARABIC, 13))
            return menu

        m_home = m(i18n.t("menu_home"))
        act_home = QAction(i18n.t("home_tab"), self)
        act_home.triggered.connect(lambda: self.workspace_tabs.setCurrentIndex(0))
        m_home.addAction(act_home)
        mb.addMenu(m_home)

        m_imp = m(i18n.t("menu_import"))
        act_ops = QAction(i18n.t("ops_tab"), self)
        act_ops.triggered.connect(lambda: self.open_new_sub_screen("ops", i18n.t("ops_tab")))
        m_imp.addAction(act_ops)
        mb.addMenu(m_imp)

        m_md = m(i18n.t("menu_master"))
        act_md = QAction(i18n.t("master_tab"), self)
        act_md.triggered.connect(lambda: self.open_new_sub_screen("master", i18n.t("master_tab")))
        m_md.addAction(act_md)
        mb.addMenu(m_md)

        m_fin = m(i18n.t("menu_finance"))
        act_fin = QAction(i18n.t("finance_tab"), self)
        act_fin.triggered.connect(lambda: self.open_new_sub_screen("finance", i18n.t("finance_tab")))
        m_fin.addAction(act_fin)
        mb.addMenu(m_fin)

        m_set = m(i18n.t("menu_settings"))
        act_settings = QAction(i18n.t("settings_tab"), self)
        act_settings.triggered.connect(lambda: self.open_new_sub_screen("settings", i18n.t("settings_tab")))
        m_set.addAction(act_settings)
        mb.addMenu(m_set)


def get_asset_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller bundle."""
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname(__file__))
    return os.path.normpath(os.path.join(base_path, relative_path))


def main():
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Enterprise.ImportManagement.System.v1")
        except Exception:
            pass

    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    app.setFont(QFont(FONT_ARABIC, 13))
    app.setStyleSheet(UITheme.get_style())

    ico_path = get_asset_path("src/assets/app_icon.ico")
    png_path = get_asset_path("src/assets/app_icon.png")
    
    target_icon_path = ico_path if os.path.exists(ico_path) else png_path
    if os.path.exists(target_icon_path):
        from PySide6.QtGui import QIcon
        app_icon = QIcon(target_icon_path)
        app.setWindowIcon(app_icon)

    window = MainWindow()
    if os.path.exists(target_icon_path):
        window.setWindowIcon(app_icon)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
