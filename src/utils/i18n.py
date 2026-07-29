"""
Internationalization (i18n) Manager — Pure Arabic / Pure English Translations
Clean separate translations for Arabic (ar) and English (en) without merged pipe strings.
"""

from typing import Dict


STRINGS_AR = {
    # System & Main Shell
    "app_name": "نظام إدارة الاستيراد",
    "version": "الإصدار v1.0.0",
    "system_admin": "مدير النظام",
    "company_name": "الشركة المصرية للاستيراد والتصدير",
    "connected": "متصل بقاعدة البيانات",
    "home_tab": "🏠 إبدأ مع التطبيق",
    "dashboard_tab": "📊 لوحة المتابعة والـ KPIs",
    "ops_tab": "📦 ملفات الاستيراد والتخليص",
    "finance_tab": "💰 المعاملات والطلبات المالية",
    "master_tab": "🏢 البيانات المرجعية والشركات",
    "settings_tab": "⚙️ إعدادات النظام والمظهر",

    # Menus
    "menu_home": "🏠 الرئيسية",
    "menu_import": "📦 الاستيراد",
    "menu_master": "🏢 البيانات المرجعية",
    "menu_finance": "💰 المالية",
    "menu_settings": "⚙️ الإعدادات",

    # Home Screen & Metro Tiles
    "welcome_title": "🚢 نظام إدارة عمليات الاستيراد والبيانات المرجعية",
    "welcome_subtitle": "اضغط على أي بلاطة لفتح شاشة عمل جديدة في تبويب جديد دون إغلاق الشاشات السابقة",
    "quick_actions_header": "🚀 الإجراءات السريعة",
    "main_modules_header": "📊 الأقسام والوحدات الرئيسية",
    "tile_new_file_ar": "فتح ملف استيراد جديد",
    "tile_new_file_en": "New Import File",
    "tile_new_pay_ar": "طلب دفع مالي للمورد",
    "tile_new_pay_en": "New Payment Request",
    "tile_add_supplier_ar": "إضافة مورد أجنبي",
    "tile_add_supplier_en": "Add Foreign Supplier",
    "tile_cbm_calc_ar": "حاسبة CBM والجمارك",
    "tile_cbm_calc_en": "CBM & Tax Estimator",
    "tile_dashboard_ar": "لوحة المتابعة والـ KPIs",
    "tile_dashboard_en": "Executive Dashboard",
    "tile_companies_ar": "سجل الشركات المستوردة",
    "tile_companies_en": "Importing Companies",
    "tile_partners_ar": "شركاء الخدمات والبنك",
    "tile_partners_en": "Service Partners",
    "tile_settings_ar": "إعدادات النظام والوضع الداكن",
    "tile_settings_en": "System Settings",

    # Dashboard View
    "kpi_active_files": "ملفات الاستيراد النشطة",
    "kpi_pending_payments": "تدفقات نقدية معلقة",
    "kpi_shipments_enroute": "شحنات في الطريق",
    "kpi_alerts": "تنبيهات مستندية",
    "btn_new_import_file": "➕ ملف استيراد جديد",
    "btn_new_payment_request": "📑 طلب دفع جديد",
    "btn_export_reports": "📊 تصدير التقارير",
    "btn_refresh_data": "🔄 تحديث البيانات",
    "table_recent_files": "📋 أحدث ملفات الاستيراد المسجلة",

    # Operations View
    "ops_files_group": "📂 ملفات الاستيراد المسجلة بالنظام",
    "btn_create_new_file": "➕ إنشاء ملف استيراد جديد",
    "cbm_box_title": "📐 حاسبة الحجم والوزن المحاسبي (BP-004)",
    "btn_calc_cbm": "📐 حساب CBM",
    "duties_box_title": "🧾 حاسبة الجمارك والضرائب (BP-008)",
    "btn_calc_duties": "🧾 حساب الجمارك",
    "btn_export_pdf": "📄 تصدير تقرير الجمارك PDF",

    # Finance View
    "fin_form_group": "💳 إنشاء طلب دفع مالي للمورد (BP-009)",
    "fin_table_group": "سجل طلبات الدفع ومتابعة التحويل البنكي SWIFT",
    "btn_submit_payment": "📩 إرسال طلب الدفع",

    # Settings View
    "settings_hdr": "⚙️ إعدادات النظام والمظهر",
    "appearance_group": "🎨 إعدادات المظهر والوضع الداكن",
    "lang_group": "🌐 إعدادات اللغة والاتجاه",
    "sys_defaults_group": "⚙️ إعدادات النظام والضريبة",
    "btn_enable_dark": "🌙 تفعيل الوضع الداكن",
    "btn_enable_light": "☀️ تفعيل الوضع الفاتح",
    "btn_switch_lang": "🌐 Switch to English",
    "btn_save_settings": "💾 حفظ إعدادات النظام",

    # Common Table Headers
    "th_file_id": "رقم الملف",
    "th_project": "اسم المشروع",
    "th_company": "الشركة",
    "th_supplier": "المورد",
    "th_freight_mode": "وسيلة الشحن",
    "th_cbm": "الحجم الإجمالي",
    "th_stage": "المرحلة",
    "th_amount": "المبلغ ($)",
    "th_payment_type": "نوع الدفعة",
    "th_status": "حالة الطلب",
    "th_swift": "رقم التحويل SWIFT",
}


STRINGS_EN = {
    # System & Main Shell
    "app_name": "Import Management System",
    "version": "Version v1.0.0",
    "system_admin": "System Administrator",
    "company_name": "Egyptian Import & Export Co.",
    "connected": "Connected to Database",
    "home_tab": "🏠 Start / Home Workspace",
    "dashboard_tab": "📊 Dashboard & KPIs",
    "ops_tab": "📦 Import Files & Operations",
    "finance_tab": "💰 Financial Transactions & Payments",
    "master_tab": "🏢 Master Data & Directory",
    "settings_tab": "⚙️ Settings & Theme",

    # Menus
    "menu_home": "🏠 Home",
    "menu_import": "📦 Import",
    "menu_master": "🏢 Master Data",
    "menu_finance": "💰 Finance",
    "menu_settings": "⚙️ Settings",

    # Home Screen & Metro Tiles
    "welcome_title": "🚢 Import Operations & Master Data Management System",
    "welcome_subtitle": "Click any tile to open a new sub-screen workspace without losing open tabs",
    "quick_actions_header": "🚀 Quick Actions",
    "main_modules_header": "📊 Main System Modules",
    "tile_new_file_ar": "New Import File",
    "tile_new_file_en": "New Import File",
    "tile_new_pay_ar": "New Payment Request",
    "tile_new_pay_en": "New Payment Request",
    "tile_add_supplier_ar": "Add Foreign Supplier",
    "tile_add_supplier_en": "Add Foreign Supplier",
    "tile_cbm_calc_ar": "CBM & Tax Estimator",
    "tile_cbm_calc_en": "CBM & Tax Estimator",
    "tile_dashboard_ar": "Executive Dashboard",
    "tile_dashboard_en": "Executive Dashboard",
    "tile_companies_ar": "Importing Companies",
    "tile_companies_en": "Importing Companies",
    "tile_partners_ar": "Service Partners",
    "tile_partners_en": "Service Partners",
    "tile_settings_ar": "System Settings",
    "tile_settings_en": "System Settings",

    # Dashboard View
    "kpi_active_files": "Active Import Files",
    "kpi_pending_payments": "Pending Cash Flow",
    "kpi_shipments_enroute": "Shipments En Route",
    "kpi_alerts": "Document Alerts",
    "btn_new_import_file": "➕ New Import File",
    "btn_new_payment_request": "📑 New Payment Request",
    "btn_export_reports": "📊 Export Reports",
    "btn_refresh_data": "🔄 Refresh Data",
    "table_recent_files": "📋 Recent Registered Import Files",

    # Operations View
    "ops_files_group": "📂 Registered Import Files in System",
    "btn_create_new_file": "➕ Create New Import File",
    "cbm_box_title": "📐 CBM Volume & Chargeable Weight Calculator (BP-004)",
    "btn_calc_cbm": "📐 Calculate CBM",
    "duties_box_title": "🧾 Customs Duties & Tax Estimator (BP-008)",
    "btn_calc_duties": "🧾 Estimate Duties",
    "btn_export_pdf": "📄 Export Customs PDF",

    # Finance View
    "fin_form_group": "💳 Create Supplier Payment Request (BP-009)",
    "fin_table_group": "Payment Requests & SWIFT Transfer Tracking",
    "btn_submit_payment": "📩 Submit Payment Request",

    # Settings View
    "settings_hdr": "⚙️ System & Appearance Settings",
    "appearance_group": "🎨 Appearance & Dark Mode",
    "lang_group": "🌐 Language & Locale Settings",
    "sys_defaults_group": "⚙️ System Defaults & Tax Rates",
    "btn_enable_dark": "🌙 Enable Dark Mode",
    "btn_enable_light": "☀️ Enable Light Theme",
    "btn_switch_lang": "🌐 التحويل للغة العربية",
    "btn_save_settings": "💾 Save System Settings",

    # Common Table Headers
    "th_file_id": "File ID",
    "th_project": "Project Name",
    "th_company": "Company",
    "th_supplier": "Supplier",
    "th_freight_mode": "Freight Mode",
    "th_cbm": "Total CBM",
    "th_stage": "Stage",
    "th_amount": "Amount ($)",
    "th_payment_type": "Payment Type",
    "th_status": "Status",
    "th_swift": "SWIFT Ref",
}


class I18nManager:
    def __init__(self, default_lang: str = "ar"):
        self.current_lang = default_lang

    def t(self, key: str) -> str:
        dict_source = STRINGS_AR if self.current_lang == "ar" else STRINGS_EN
        return dict_source.get(key, key)

    def switch_language(self, lang: str):
        if lang in ["ar", "en"]:
            self.current_lang = lang

    def set_language(self, lang: str):
        self.switch_language(lang)

    def toggle(self) -> str:
        self.current_lang = "en" if self.current_lang == "ar" else "ar"
        return self.current_lang


i18n = I18nManager()
