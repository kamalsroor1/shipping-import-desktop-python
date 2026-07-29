# Import Management System - Python Desktop App Requirements & Setup

وثيقة المتطلبات والمعمارية التقنية لبناء تطبيق سطح المكتب (Desktop Application) بلغة Python لإدارة دورة الاستيراد بالكامل (Import Management System).

---

## 1. التقنيات والمكتبات المستخدمة (Tech Stack)

| المجال | التقنية / المكتبة | السبب والوظيفة |
| :--- | :--- | :--- |
| **واجهة المستخدم (GUI)** | **PySide6 (Qt 6 for Python)** | الإطار الرسمي المعتمد لبناء واجهات سطح مكتب احترافية وسريعة، تدعم المظهر العصري (Dark/Light Modes) والتقارير والداشبورد الداخلي. |
| **قاعدة البيانات (Database)** | **PostgreSQL + SQLAlchemy 2.0** | التعامل مع قاعدة البيانات بالاعتماد على ORM قوي يدعم المعاملات المعقدة (Transactions) والتحقق من العلاقات والـ Audit Log. |
| **إدارة الهجرة (Migrations)** | **Alembic** | تتبع وتحديث هيكل قاعدة البيانات بدون فقدان البيانات المسجلة. |
| **التحقق من البيانات (Validation)** | **Pydantic v2** | التحقق من صحة المدخلات حسب القواعد الجمركية قبل إرسالها لقاعدة البيانات. |
| **تصدير التقارير (Reports/PDF/Excel)** | **ReportLab + OpenPyXL** | طباعة الفواتير المبدئية، طلبات نموذج 4، طلبات الدفع، وتصدير التقارير الإحصائية لإكسل. |
| **التصميم والمظهر (Styling)** | **PySide6 / qdarktheme** | تطبيق تصميم عصري وجذاب مخصص لإدارة اللوجستيات مع تخصيص الـ QSS. |
| **حزم التشغيل (Packaging)** | **PyInstaller** | تحويل تطبيق البايثون إلى ملف تنفيذي مستقل (`.exe`) يشتغل مباشرة على ويندوز بدون الحاجة لتثبيت بايثون لدى المستخدم. |

---

## 4. Multi-Tab Sub-Screen Workspace Architecture (نظام الشاشات المتعددة والتبويبات الفرعية)
- **QTabWidget Workspace Manager**:
  - Main workspace replaces static view container with a dynamic `QTabWidget` (Sub-Screen workspace).
  - Clicking any import file, supplier, or document opens a new **Sub-Tab**.
  - Closable tabs with `setTabsClosable(True)` and `tabCloseRequested` signal handling.
  - Shortcut `Ctrl+W` closes current active sub-tab.

---

## 5. الهيكل التنظيمي للمشروع (Project Directory Structure)

```text
i:/disktop/
├── docs/
│   ├── Import_System_Specification.md   # وثيقة دورة العمل والبيانات المرجعية
│   ├── schema.sql                        # مخطط قاعدة البيانات (PostgreSQL)
│   └── desktop_app_requirements.md      # وثيقة متطلبات تطبيق سطح المكتب
├── requirements.txt                      # متطلبات المكتبات البايثون
├── src/
│   ├── __init__.py
│   ├── main.py                           # نقطة تشغيل التطبيق (Entry Point)
│   ├── config.py                         # إعدادات التطبيق والاتصال بقاعدة البيانات
│   ├── database/                         # طبقة قاعدة البيانات
│   │   ├── session.py                    # Connection Pool & Session
│   │   ├── models/                       # SQLAlchemy Models لكل جداول MD و BP
│   │   └── repositories/                 # Data Access Object (DAO) Layer
│   ├── services/                         # المنطق التجاري (Business Logic Services)
│   │   ├── cbm_calculator.py             # حساب CBM و Chargeable Weight
│   │   ├── duties_estimator.py           # حساب الرسوم الجمركية والضرائب
│   │   ├── payment_service.py            # إدارة طلبات الدفع والتحقق من الرصيد
│   │   └── audit_service.py              # تتبع سجل التعديلات GP-004
│   ├── ui/                               # طبقة واجهة المستخدم (PySide6)
│   │   ├── components/                   # مكونات مخصصة (Tables, Widgets, Cards)
│   │   ├── views/                        # الشاشات الرئيسية
│   │   │   ├── dashboard_view.py         # لوحة التتبع والمؤشرات KPIs
│   │   │   ├── master_data_view.py       # إدارة الشركات والموردين والشركاء
│   │   │   ├── project_view.py           # إدارة المشاريع ملفات الاستيراد
│   │   │   ├── shipments_view.py         # مراحل الشحن والباكينج ليست والـ PI
│   │   │   ├── customs_view.py           # الاستشارات الجمركية وتقدير الرسوم
│   │   │   └── finance_view.py           # طلبات السداد ونموذج 4
│   │   └── styles/                       # ملفات التنسيق QSS والمظهر
│   └── utils/                            # أدوات مساعدة (Export, PDF, Helpers)
└── tests/                                # الاختبارات المؤتمتة (Pytest)
```

---

## 3. المهارات المضافة للذكاء الاصطناعي (AI Skills)

تم تزويد البيئة بالمهارات البرمجية لدعم التطوير بأعلى جودة:

1. **`python-design-patterns`** (تثبيت عام مفعل):
   - تزويد النموذج بأنماط التصميم المتقدمة في البايثون مثل Repository Pattern و Factory Pattern و Singleton المخصصة لتطبيقات سطح المكتب.
2. **`postgresql-table-design` & `supabase-postgres-best-practices`**:
   - إرشادات الأداء والاستعلامات السريعة لـ PostgreSQL.

---

## 4. خطوات التثبيت للبدء في التطوير (Quick Start)

### الخطوة 1: إنشاء البيئة الافتراضية
```bash
python -m venv venv
venv\Scripts\activate
```

### الخطوة 2: تثبيت المكتبات المطلوبة
```bash
pip install -r requirements.txt
```

### الخطوة 3: تشغيل التطبيق
```bash
python src/main.py
```
