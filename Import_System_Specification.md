# Master Data & Import Business Process Specification

جميع جداول الـ Master Data تمثل البيانات المرجعية للنظام، ويتم إدخالها مرة واحدة وإعادة استخدامها في جميع مراحل دورة الاستيراد. يهدف هذا التصميم إلى منع تكرار البيانات، تقليل أخطاء الإدخال، ضمان توحيد المعلومات، ودعم إنشاء المستندات الرسمية والتقارير بشكل آلي. لا يجوز إدخال بيانات مرجعية مباشرة داخل المعاملات (Transactions)، بل يجب اختيارها من جداول الـ Master Data.

---

## General System Principles

هذه القواعد تطبق على جميع العمليات داخل النظام.

### GP-001 Progressive Data Entry

#### Purpose
يسمح النظام بإنشاء ملف الاستيراد حتى فى حالة عدم اكتمال جميع البيانات، مع استكمال البيانات تدريجيًا خلال مراحل العمل المختلفة.

#### Rules
- لا يشترط اكتمال جميع الحقول عند إنشاء ملف الاستيراد.
- يتم إدخال البيانات حسب المستندات المتوفرة فى كل مرحلة.
- لا يمنع النظام حفظ البيانات بسبب حقول غير مطلوبة فى المرحلة الحالية.
- يمنع النظام فقط تنفيذ العمليات التى تعتمد على بيانات غير مكتملة.

#### Example
يمكن إنشاء Packing List بدون:
- Length
- Width
- Height
- Unit Price

ولكن لا يمكن تنفيذ Calculate CBM قبل استكمال الأبعاد.

---

### GP-002 Stage-Based Validation

#### Purpose
تطبيق التحقق من صحة البيانات بناءً على المرحلة الحالية وليس عند إدخال البيانات فقط.

#### Rules
- لكل عملية متطلبات خاصة بها.
- يتم التحقق من البيانات عند تنفيذ العملية.
- لا يتم إجبار المستخدم على إدخال بيانات غير مطلوبة فى المرحلة الحالية.

---

### GP-003 Editable Import Files

#### Purpose
السماح بتعديل ملفات الاستيراد طوال دورة العمل مع الاحتفاظ بسجل كامل لجميع التعديلات لضمان المرونة وإمكانية المراجعة.

#### Rules
- يمكن فتح أى Import File فى أى وقت.
- يمكن تعديل البيانات طالما أن الملف لم يتم إغلاقه (Closed).
- يسمح بتعديل بيانات الفاتورة أو الباكينج ليست أو بيانات الشحنة عند استلام مستندات محدثة من المورد.
- لا يتم حذف البيانات السابقة، وإنما يتم تسجيل عملية التعديل.
- يجب أن يحتفظ النظام بآخر نسخة من البيانات مع إمكانية معرفة أن الملف تم تعديله.

#### Audit Information
يعرض النظام دائمًا معلومات آخر تعديل داخل كل ملف:

| Field | Description |
| :--- | :--- |
| Last Modified By | آخر مستخدم قام بالتعديل |
| Last Modified Date | تاريخ ووقت آخر تعديل |
| Version Number | رقم الإصدار (اختيارى إذا تم تطبيق نظام الإصدارات) |
| Modification Notes | سبب التعديل (اختيارى أو إلزامى حسب نوع التعديل) |

---

### GP-004 Audit Trail

#### Purpose
توفير سجل تاريخى لجميع العمليات التى تمت على ملف الاستيراد.

#### Rules
يقوم النظام بتسجيل جميع الأحداث المهمة مثل:
- إنشاء الملف.
- تعديل البيانات.
- اعتماد المستندات.
- تغيير حالة العملية.
- إضافة أو حذف بنود.
- رفع مستند جديد.
- اعتماد أو رفض مستند.
- إغلاق ملف الاستيراد.

ويحتوى كل سجل على:
- التاريخ والوقت.
- المستخدم.
- نوع العملية.
- اسم الشاشة أو العملية.
- وصف مختصر للتغيير.

---

## Master Data Specification

### MD-001 Company (Egyptian Importers)

#### 1. Purpose
- يستخدم هذا الجدول لإدارة جميع الشركات المصرية التي يتم الاستيراد باسمها.
- يسمح النظام بإدارة أكثر من شركة داخل نفس قاعدة البيانات، حيث تمتلك كل شركة بياناتها القانونية ومستنداتها الخاصة.
- يعتبر هذا الجدول المرجع الرئيسي (Master Data) لجميع عمليات الاستيراد، ولا يمكن إنشاء أي مشروع أو ملف استيراد بدون اختيار شركة.

#### 2. Business Objective
الغرض من هذا الجدول هو:
- تخزين البيانات القانونية للشركات.
- متابعة صلاحية المستندات الرسمية.
- إعادة استخدام بيانات الشركة داخل جميع أجزاء النظام.
- منع إدخال نفس البيانات فى كل عملية استيراد.
- تقليل الأخطاء الناتجة عن الإدخال اليدوي.

#### 3. System Usage
يستخدم النظام بيانات هذا الجدول فى العمليات التالية:
- إنشاء Project جديد.
- إنشاء Import File.
- إنشاء طلب ACID.
- تجهيز المراسلات الرسمية.
- إنشاء النماذج الحكومية.
- تعبئة بيانات المستورد تلقائياً داخل المستندات.
- متابعة انتهاء المستندات القانونية وإظهار التنبيهات.

#### 4. Main Fields

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| Company ID | Auto Number | Yes | Primary Key |
| Egyptian Importer Name | Text | Yes | Legal Company Name |
| Address | Text | Yes | Registered Address |
| Country | Text | Yes | Country |
| Importer ID | Text | Yes | Import License Number |
| Importer ID Expiration Date | Date | Yes | License Expiry Date |
| VAT ID | Text | Yes | Tax Registration Number |
| VAT ID Expiration Date | Date | Yes | Tax Registration Expiry |
| Commercial Registration No | Text | Yes | Commercial Registration |
| Commercial Registration Expiration Date | Date | Yes | Registration Expiry |

#### 5. Business Rules
- لا يسمح بإنشاء Import File بدون اختيار شركة.
- لا يسمح بحذف شركة مرتبطة بمشروعات أو ملفات استيراد.
- يجب أن تكون بيانات الشركة مطابقة للمستندات الرسمية.
- النظام يحسب عدد الأيام المتبقية لانتهاء كل مستند تلقائياً.
- إذا انتهى أحد المستندات القانونية يتم إصدار تنبيه.
- يمكن تعطيل الشركة (Inactive) دون حذفها من النظام.

#### 6. Relationships
Company
→ Projects
→ Import Files
→ ACID Requests
→ Official Documents

#### 7. Notes for Developer
- لا تقم بحفظ حقول "Days to Renew" داخل قاعدة البيانات، بل يتم حسابها ديناميكياً.
- استخدم Soft Delete بدلاً من الحذف النهائي.
- جميع الحقول القانونية يجب أن تدعم البحث (Searchable).

---

### MD-002 Supplier

#### Purpose
- يستخدم هذا الجدول لتخزين جميع بيانات الموردين الأجانب (Foreign Exporters).
- تستخدم هذه البيانات فى جميع عمليات الاستيراد لتجنب إعادة إدخال بيانات المورد فى كل شحنة.

#### Business Objective
- إنشاء قاعدة بيانات موحدة للموردين.
- ضمان تطابق بيانات المورد مع المستندات الرسمية.
- إعادة استخدام البيانات فى جميع مراحل النظام.
- تقليل أخطاء الإدخال اليدوي.

#### System Usage
يتم استخدام بيانات المورد فى:
- إنشاء Project.
- إنشاء Import File.
- إصدار ACID.
- إنشاء مستندات CargoX.
- تجهيز الفواتير.
- تجهيز المستندات الجمركية.
- تعبئة بيانات المصدر فى جميع المراسلات.

#### Important Note
يجب أن تكون بيانات المورد مطابقة تماماً للمستندات الرسمية.

أى اختلاف فى:
- Registration Type
- Foreign Exporter ID
- Country Code
- Company Name

قد يؤدى إلى رفض طلب ACID أو تأخير إجراءات التخليص الجمركى.

لهذا السبب تعتبر بيانات المورد بيانات قانونية (Legal Master Data) ويجب مراجعتها بدقة قبل استخدامها.

#### Business Rules
- لا يسمح بتكرار المورد بنفس Registration Type و Foreign Exporter ID.
- لا يسمح بحذف مورد مرتبط بأى Import File.
- يمكن تعديل بيانات المورد مع الاحتفاظ بسجل التعديلات (Audit Log).

---

### MD-003 Business Partners

#### Purpose
- يستخدم هذا الجدول لإدارة جميع مقدمى الخدمات الخارجيين.
- بدلاً من إنشاء جدول مستقل لكل نوع، يتم تخزين جميع مقدمى الخدمات داخل جدول واحد مع تحديد نوع الخدمة.

#### Supported Partner Types
- Freight Forwarder
- Customs Broker
- Inspection Company
- Insurance Company
- Courier
- Shipping Agent
- Bank
- Trucking Company

#### Business Objective
- توحيد إدارة جميع مقدمى الخدمات.
- إعادة استخدام نفس البيانات فى جميع الشحنات.
- منع تكرار بيانات الشركات.
- تسهيل عمليات البحث والتقارير.

#### Business Rules
- كل شحنة يجب أن تحتوى على Freight Forwarder.
- كل شحنة يجب أن تحتوى على Customs Broker.
- شركة الفحص اختيارية وتعتمد على نوع الشحنة.
- لا يسمح بحذف مقدم خدمة مرتبط بشحنات سابقة.

| Field | Type |
| :--- | :--- |
| Partner ID | |
| Partner Name | |
| Partner Type | |
| Contact Name | |
| Mobile | |
| Email | |
| Address | |
| Country | |
| Payment Type | |
| Credit Limit | |
| Status | |

---

### MD-004 External Service Providers

#### Purpose
- يستخدم هذا الجدول لإدارة جميع مقدمى الخدمات الخارجيين الذين يشاركون فى دورة الاستيراد.
- بدلاً من إنشاء جدول مستقل لكل نوع من مقدمى الخدمة، يتم تخزين جميع الشركات داخل جدول واحد مع تحديد نوع الخدمة التى تقدمها.
- يسمح هذا التصميم بإضافة أنواع جديدة من مقدمى الخدمات مستقبلاً دون الحاجة إلى تعديل قاعدة البيانات.

#### Business Objective
- إنشاء قاعدة بيانات موحدة لجميع مقدمى الخدمات.
- إعادة استخدام بيانات الشركات فى جميع الشحنات.
- منع تكرار إدخال نفس البيانات.
- تسهيل عمليات البحث والتقارير.
- إمكانية إضافة أنواع خدمات جديدة مستقبلاً.

#### System Usage
يستخدم هذا الجدول فى:
- اختيار Freight Forwarder للشحنة.
- اختيار Customs Broker.
- اختيار Inspection Company (عند الحاجة).
- متابعة بيانات الاتصال.
- إصدار طلبات عروض الأسعار.
- إنشاء تقارير الأداء لكل مقدم خدمة.

#### Supported Partner Types
- Freight Forwarder
- Customs Broker
- Inspection Company
- Insurance Company
- Courier Company
- Shipping Agent
- Trucking Company

#### Main Fields

| Field | Type | Required | Notes |
| :--- | :--- | :--- | :--- |
| Partner ID | Auto Number | Yes | Primary Key |
| Partner Name | Text | Yes | Company Legal Name |
| Partner Type | Lookup | Yes | Freight Forwarder / Customs Broker / Inspection ... |
| Contact Person | Text | No | Main Contact |
| Phone Number | Text | No | |
| Mobile Number | Text | No | |
| Email | Text | No | |
| Address | Text | No | |
| Country | Lookup | No | |
| Payment Type | Lookup | No | Cash / Credit |
| Credit Limit | Decimal | No | |
| Notes | Long Text | No | |
| Status | Lookup | Yes | Active / Inactive |

#### Relationships
External Service Provider
↓
Shipping Quotations
↓
Import Files
↓
Financial Requests
↓
Performance Reports

#### Business Rules
- كل شحنة يجب أن تحتوي على Freight Forwarder.
- كل شحنة يجب أن تحتوي على Customs Broker.
- شركة الفحص اختيارية حسب نوع الشحنة.
- لا يسمح بحذف مقدم خدمة مرتبط بشحنات سابقة.
- يمكن تعطيل مقدم الخدمة دون حذف بياناته.

#### Validation
- Partner Name يجب أن يكون فريداً داخل نفس Partner Type.
- Email إن وجد يجب أن يكون بصيغة صحيحة.
- Credit Limit يجب ألا يكون أقل من صفر.

#### Edge Cases
- بعض الشحنات لا تحتاج Inspection Company.
- يمكن أن تكون نفس الشركة Freight Forwarder و Customs Broker فى نفس الوقت.

#### Notes for Developer
- استخدم Lookup Table منفصل لـ Partner Types.
- استخدم Soft Delete.

---

### MD-005 Shipping Lines

#### Purpose
يستخدم هذا الجدول كمرجع لجميع الخطوط الملاحية المستخدمة فى النظام.

#### Business Objective
- توحيد أسماء الخطوط الملاحية.
- منع اختلاف كتابة نفس الخط.
- دعم البحث والتقارير.

#### System Usage
- Shipping Quotations
- Booking
- Shipment Tracking
- Transit Time Reports

#### Main Fields

| Field | Type | Required | Notes |
| :--- | :--- | :--- | :--- |
| Shipping Line ID | Auto Number | Yes | Primary Key |
| Shipping Line Name | Text | Yes | |
| SCAC Code | Text | No | إذا كان متاحاً |
| Country | Lookup | No | |
| Website | Text | No | |
| Status | Lookup | Yes | Active / Inactive |

#### Relationships
Shipping Line
↓
Shipping Quotations
↓
Bookings
↓
Import Files

#### Business Rules
- لا يسمح بتكرار اسم الخط.
- لا يسمح بحذف خط مستخدم فى شحنات سابقة.

#### Validation
- Shipping Line Name Required.
- SCAC Code اختياري.

#### Edge Cases
بعض الخطوط تعمل كشركات تشغيل فقط وليس لديها موقع إلكترونى.

#### Notes for Developer
يدعم البحث (Autocomplete).

---

### MD-006 Currency

#### Purpose
يستخدم كمرجع لجميع العملات المستخدمة داخل النظام.

#### Business Objective
- توحيد العملات.
- منع كتابة العملات يدوياً.
- دعم الحسابات المالية.

#### System Usage
- PI
- Final Invoice
- Freight Quotations
- Customs Estimate
- Supplier Invoice
- Service Provider Invoice

#### Main Fields

| Field | Type | Required | Notes |
| :--- | :--- | :--- | :--- |
| Currency ID | Auto Number | Yes | |
| ISO Code | Text | Yes | USD / EUR / EGP |
| Currency Name | Text | Yes | |
| Symbol | Text | No | $, €, £ |
| Decimal Places | Number | Yes | غالباً 2 |
| Status | Lookup | Yes | Active / Inactive |

#### Relationships
Currency
↓
Invoices
↓
Shipping Quotations
↓
Payment Requests

#### Business Rules
- لا يسمح بتكرار ISO Code.
- لا يسمح بحذف عملة مستخدمة.

#### Validation
ISO Code يجب أن يتكون من 3 أحرف.

#### Edge Cases
قد توجد شحنات تحتوي على أكثر من عملة.

#### Notes for Developer
جميع القيم المالية تشير إلى Currency ID وليس إلى النص.

---

### MD-007 Incoterms

هذا هو أهم Master Data فى النظام لأنه يتحكم فى توزيع المسؤوليات والتكاليف طوال دورة الاستيراد.

#### Purpose
يستخدم هذا الجدول لتحديد مسؤوليات كل من المستورد (Importer) والمصدر (Exporter) وفقاً لقواعد Incoterms 2020.

لا يقتصر استخدامه على عرض نوع الـ Incoterm فقط، بل يستخدم لتحديد:
- من يتحمل كل بند تكلفة.
- من المسؤول عن كل مرحلة من مراحل الشحن.
- ما هى التكاليف المتوقع إضافتها إلى تكلفة الاستيراد.
- ما هى الخدمات التى يجب طلب عروض أسعار لها.
- مقارنة التكلفة الفعلية بالتكلفة المتوقعة.

#### Business Objective
- تطبيق قواعد Incoterms 2020.
- توزيع المسؤوليات تلقائياً.
- حساب التكلفة المتوقعة.
- تقليل أخطاء احتساب المصروفات.
- دعم التقارير المالية.

#### Table 1 : Incoterms

| Field | Type | Required | Notes |
| :--- | :--- | :--- | :--- |
| Incoterm ID | Auto Number | Yes | |
| Incoterm Code | Text | Yes | EXW / FOB / CIF |
| Name | Text | Yes | |
| Description | Long Text | No | |
| Version | Text | Yes | Incoterms 2020 |
| Status | Lookup | Yes | Active |

#### Table 2 : Cost Items

| Field | Type | Required |
| :--- | :--- | :--- |
| Cost Item ID | Auto | |
| Cost Item Name | Text | |
| Category | Lookup | |

##### Examples
- Origin Trucking
- Export Clearance
- OTHC
- Ocean Freight
- Insurance
- Origin Inspection
- Documentation
- DTHC
- Customs Clearance
- Form 4
- Duties
- Storage
- Demurrage
- Port Congestion
- Compliance Fees

#### Table 3 : Incoterm Responsibilities

| Field | Type | Required | Notes |
| :--- | :--- | :--- | :--- |
| ID | Auto | Yes | |
| Incoterm ID | FK | Yes | |
| Cost Item ID | FK | Yes | |
| Responsible Party | Lookup | Yes | Importer / Exporter / Shared |
| Is Included | Boolean | Yes | Included in Incoterm |
| Notes | Text | No | |

##### Example

| Incoterm | Cost Item | Responsible Party |
| :--- | :--- | :--- |
| EXW | Origin Trucking | Importer |
| EXW | Export Clearance | Importer |
| EXW | Ocean Freight | Importer |
| CIF | Ocean Freight | Exporter |
| CIF | Insurance | Exporter |
| CIF | Customs Clearance | Importer |

#### لماذا هذا التصميم؟
بدلاً من وجود 18 عمود Yes / No داخل جدول Incoterms، أصبح النظام يعتمد على بيانات مرنة (Data-Driven).

إذا أضيف بند تكلفة جديد مثل:
- Carbon Tax
- Security Surcharge
- Green Fuel Surcharge

لن نحتاج لتعديل قاعدة البيانات أو الكود، بل نضيف Cost Item جديد ثم نربطه بالـ Incoterm المناسب.

#### Relationships
Incoterms
↓
Projects
↓
Import Files
↓
Shipping Cost Estimation
↓
Cost Analysis
↓
Financial Reports

#### Business Rules
- كل مشروع يجب أن يحتوى على Incoterm واحد.
- لا يسمح بتكرار نفس Cost Item لنفس Incoterm.
- المسؤول عن بند التكلفة يجب أن يكون:
  - Importer
  - Exporter
  - Shared

#### Validation
- Incoterm Code Unique.
- Cost Item Unique داخل نفس Incoterm.

#### Edge Cases
قد يتفق الطرفان تعاقدياً على توزيع مختلف لبعض البنود، لذلك يجب أن يسمح النظام بعمل Override على مستوى الشحنة مع الاحتفاظ بالقيمة الأصلية الخاصة بالـ Incoterm.

#### Notes for Developer
لا تعتمد على أعمدة Yes/No.

اعتمد على العلاقة بين:
- Incoterms
- Cost Items
- Responsibilities

حتى يصبح النظام قابلاً للتوسع دون تعديل هيكل قاعدة البيانات.

---

### MD-008 Projects

#### Purpose
يمثل هذا الجدول نقطة البداية لكل عملية استيراد.

كل مشروع يحدد الإطار العام الذى سيتم تنفيذ عمليات الاستيراد داخله، ويربط بين الشركة المستوردة، المورد، نوع الاستيراد، والأولوية.

#### Business Objective
- تجميع الشحنات تحت مشروع واحد.
- ربط العمليات بالمورد والشركة.
- تسهيل متابعة الأداء والتكاليف على مستوى المشروع.

#### Main Fields

| Field | Type | Required | Notes |
| :--- | :--- | :--- | :--- |
| Project ID | Auto Number | Yes | Primary Key |
| Project Code | Text | Yes | Unique |
| Project Name | Text | Yes | |
| Project Owner | Text | Yes | |
| Company ID | FK | Yes | Company |
| Supplier ID | FK | Yes | Supplier |
| Incoterm ID | FK | Yes | Incoterm |
| Import Type ID | FK | Yes | Import Type |
| Priority ID | FK | Yes | Priority |
| Shipment Category ID | FK | Yes | Shipment Category |
| Status | Lookup | Yes | Open / Closed / On Hold |
| Notes | Long Text | No | |

#### Relationships
Project
↓
Import Files
↓
Purchase Orders
↓
Financial Requests
↓
Reports

#### Business Rules
- لا يمكن إنشاء مشروع بدون Company وSupplier.
- كل مشروع يرتبط بـ Incoterm واحد كإعداد افتراضي، مع إمكانية تغييره على مستوى الشحنة إذا استدعت الحاجة.
- لا يسمح بحذف مشروع يحتوي على ملفات استيراد.
- يمكن إغلاق المشروع بعد انتهاء جميع الشحنات المرتبطة به.

#### Validation
- Project Code يجب أن يكون فريداً.
- جميع المفاتيح الخارجية (FK) يجب أن تشير إلى سجلات نشطة.

#### Edge Cases
- قد يحتوي المشروع على عدة ملفات استيراد (Import Files).
- قد يستخدم المشروع أكثر من عملة أو أكثر من شركة شحن، لكن تظل هوية المشروع ثابتة.

---

## Import Business Process (As-Is Process)

### Purpose
تهدف هذه الوثيقة إلى توثيق دورة العمل الحالية الخاصة بعمليات الاستيراد كما يتم تنفيذها داخل الشركة، دون إجراء أي تعديل أو تحسين على الإجراءات الحالية.

ستكون هذه الوثيقة المرجع الأساسي لفهم النظام قبل البدء في تصميم قاعدة البيانات أو واجهات المستخدم أو منطق النظام.

### Business Objective
- توثيق جميع خطوات دورة الاستيراد الفعلية.
- تحديد ترتيب العمليات والعلاقات بينها.
- تحديد جميع الجهات المشاركة في كل مرحلة.
- تحديد المستندات المستخدمة في كل عملية.
- تحديد نقاط اتخاذ القرار (Decision Points).
- تحديد المدخلات والمخرجات لكل خطوة.
- اكتشاف العمليات المتكررة والاعتمادات المتبادلة.
- تجهيز الأساس الذي سيتم بناء النظام عليه.

### Scope
تبدأ دورة العمل من:
- استلام Purchase Order (PO)

وتنتهي عند:
- إغلاق ملف الاستيراد بعد الانتهاء من جميع الإجراءات التشغيلية والمالية واستلام البضاعة بالمخزن.

### Workflow Approach
سيتم شرح كل عملية داخل دورة الاستيراد بشكل مستقل، وسيتم توثيقها باستخدام القالب التالي:

#### Operation Template

- **Operation Name**: اسم العملية.
- **Purpose**: ما الهدف من هذه العملية؟
- **Trigger**: ما الذي يبدأ هذه العملية؟
- **Prerequisites**: ما المتطلبات التي يجب توفرها قبل تنفيذها؟
- **Inputs**: ما البيانات أو المستندات المطلوبة لتنفيذ العملية؟
- **Process Description**: شرح تفصيلي لما يحدث داخل هذه العملية خطوة بخطوة.
- **Outputs**: ما النتائج أو المستندات الناتجة عن العملية؟
- **Related Documents**: ما المستندات المستخدمة أو الناتجة؟
- **Related Master Data**: ما الجداول المرجعية المستخدمة أثناء تنفيذ العملية؟
- **Business Rules**: القواعد المنظمة لهذه العملية.
- **Validation**: ما الذي يجب أن يتحقق منه النظام قبل اعتماد العملية؟
- **Exception Cases (Edge Cases)**: الحالات غير المعتادة أو الاستثنائية وكيفية التعامل معها.
- **Dependencies**: ما العمليات السابقة التي تعتمد عليها هذه العملية؟ وما العمليات التالية التي تعتمد عليها؟
- **Notifications**: هل ينتج عن هذه العملية أي إشعارات أو تنبيهات؟
- **Dashboard Impact**: كيف تؤثر هذه العملية على لوحة المتابعة؟ هل تغير المرحلة الحالية؟ هل تحدث مؤشرات الأداء (KPIs)؟ هل تنقل الشحنة إلى مرحلة جديدة؟
- **Notes for Developer**: أي ملاحظات تقنية أو اعتبارات يجب مراعاتها عند تنفيذ هذه العملية داخل النظام.

### Implementation Methodology
سيتم توثيق جميع عمليات الاستيراد بنفس الأسلوب وبالترتيب الفعلي لتنفيذها داخل الشركة، بدءًا من استلام أمر الشراء وحتى إغلاق ملف الاستيراد.

كل عملية سيتم تحليلها ومراجعتها بشكل مستقل قبل الانتقال إلى العملية التالية، لضمان أن يكون النظام النهائي مطابقًا لطريقة العمل الفعلية وقابلًا للتطوير والتوسع مستقبلاً.

---

### BP-001 – Receive Purchase Order

#### Purpose
استلام أمر الشراء (Purchase Order) والـ Proforma Invoice من المورد، وإنشاء ملف استيراد جديد يمثل نقطة البداية لجميع عمليات الاستيراد داخل النظام.

#### Business Objective
- إنشاء Import File جديد.
- تسجيل بيانات المورد والفاتورة المبدئية.
- تسجيل جميع أصناف الشحنة.
- مراجعة القيم الأساسية قبل بدء إجراءات الاستيراد.
- تجهيز البيانات اللازمة للمراحل التالية.

#### System Usage
تستخدم هذه العملية فى:
- إنشاء Import File.
- مراجعة Proforma Invoice.
- مراجعة Packing List.
- حساب CBM.
- تحديد طريقة الشحن.
- طلب عروض أسعار الشحن.
- حساب الرسوم الجمركية.
- إنشاء ACID.
- إصدار Form 4.

#### Inputs

##### Header Information

| Field | Type | Required | Notes |
| :--- | :--- | :--- | :--- |
| Egyptian Importer Name | Text | Yes | اسم الشركة المستوردة |
| Egyptian Importer Tax ID | Text | Yes | الرقم الضريبى |
| Foreign Exporter Name | Text | Yes | المورد |
| Registration Type | Lookup | Yes | Company / Individual |
| Foreign Exporter ID | Text | Yes | رقم التسجيل |
| Country | Lookup | Yes | دولة المورد |
| Country Code | Text | Yes | ISO Country Code |
| Address | Text | Yes | عنوان المورد |
| Proforma Invoice No | Text | Yes | رقم الفاتورة |
| Proforma Invoice Date | Date | Yes | |
| Invoice Date | Date | Yes | |
| Invoice Type | Lookup | Yes | PI / Sample / Replacement |
| Purchase Order No | Text | Yes | |
| Purchase Order Date | Date | Yes | |
| Shipping Port | Lookup | Yes | |
| Destination Port | Lookup | Yes | |

##### Shipment Items

| Field | Type | Required | Notes |
| :--- | :--- | :--- | :--- |
| HS Code | Text | Yes | |
| Item Code | Text | Yes | |
| Description | Text | No | |
| Quantity | Decimal | Yes | PCS |
| Unit Price | Decimal | Yes | |
| Amount | Calculated | Yes | Qty × Unit Price |

#### Outputs
- إنشاء Import File.
- حفظ بيانات Proforma Invoice.
- حفظ جميع الأصناف.
- حساب إجمالى قيمة الفاتورة.
- تجهيز البيانات للمراجعة.

#### Business Rules
- إجمالى Amount لكل سطر = Qty × Unit Price.
- إجمالى الفاتورة = مجموع جميع Amount.
- لا يسمح بتكرار نفس Item داخل نفس الفاتورة إلا إذا اختلفت بياناته الفعلية.
- يجب ربط كل Item بـ HS Code.
- لا يسمح بحفظ فاتورة بدون أصناف.

#### Validation
- مراجعة حاصل الضرب لكل سطر.
- مراجعة إجمالى الفاتورة.
- التأكد من وجود HS Code.
- التأكد من صحة التواريخ.
- التأكد من عدم تكرار رقم الفاتورة لنفس المورد.

#### Edge Cases
- قد يحتوى نفس الـ HS Code على أكثر من Item.
- قد يتكرر نفس Item بأسعار مختلفة.
- قد تكون الفاتورة بدون Packing List فى هذه المرحلة.
- قد تكون الفاتورة قابلة للتعديل قبل اعتمادها.

---

### BP-002 – Review Proforma Invoice

#### Purpose
مراجعة الفاتورة المبدئية (Proforma Invoice) والتأكد من صحة جميع بياناتها قبل بدء إجراءات الاستيراد، مع إنشاء ملخص حسب البند الجمركي (HS Code) ليكون الأساس لجميع المراحل التالية.

#### Business Objective
- مراجعة صحة بيانات الفاتورة.
- التأكد من صحة الكميات والأسعار.
- مراجعة إجمالي قيمة الفاتورة.
- تجميع البيانات حسب HS Code.
- تجهيز البيانات لمراجعة الجمارك.
- تجهيز البيانات لتقدير الرسوم الجمركية.
- تجهيز البيانات لطلب عروض أسعار الشحن.

#### System Usage
تستخدم هذه العملية فى:
- Customs Consultation
- Estimate Duties
- Freight Quotations
- ACID
- Final Invoice Review

#### Inputs
- Import File
- Proforma Invoice
- Shipment Items

#### Generated Summary

| Field | Type | Notes |
| :--- | :--- | :--- |
| HS Code | Text | Unique |
| Total Qty | Decimal | Sum(Qty) |
| Total Amount | Decimal | Sum(Amount) |

#### Outputs
- HS Code Summary
- Invoice Validation Report
- Total Invoice Amount
- HS Code Analysis Report

#### Business Rules
- تجميع جميع الأصناف التى تحمل نفس HS Code.
- مراجعة إجمالى قيمة كل HS Code.
- مراجعة إجمالى الفاتورة.
- مراجعة عدم وجود HS Code مفقود.
- مراجعة عدم وجود Item بدون قيمة.

#### Validation
- Qty > 0
- Price > 0
- Amount = Qty × Price
- Invoice Total = Sum(All Amount)

#### Edge Cases
- أكثر من Item بنفس HS Code.
- نفس الصنف بأكثر من سعر.
- HS Code جديد غير مستخدم سابقاً.
- اختلاف إجمالى الفاتورة عن مجموع البنود.

#### Deliverables
- HS Code Summary
- Invoice Summary
- Validation Report

#### Next Operation
➡ BP-003 Review Packing List

---

### BP-003 – Review Packing List

#### Purpose
مراجعة Packing List والتأكد من صحة بيانات التعبئة والأوزان والأبعاد قبل احتساب حجم الشحنة واختيار وسيلة النقل.

#### Business Objective
- مراجعة الكميات.
- مراجعة عدد الطرود.
- مراجعة الأوزان.
- مراجعة أبعاد الطرود.
- احتساب إجمالى الأوزان.
- تجهيز البيانات لحساب CBM.

#### System Usage
تستخدم هذه العملية فى:
- Calculate CBM
- Determine Shipping Method
- Freight Quotations
- Draft BL Review
- Warehouse Receiving

#### Inputs
- Packing List
- Shipment Items

#### Required Fields

| Field | Type | Required | Notes |
| :--- | :--- | :--- | :--- |
| HS Code | Text | Yes | |
| Item Code | Text | Yes | |
| Qty PCS | Decimal | Yes | |
| Qty PKG | Decimal | Yes | |
| Package Type | Lookup | No | Carton / Pallet / Bag |
| Length | Decimal | No | cm |
| Width | Decimal | No | cm |
| Height | Decimal | No | cm |
| Net Weight / Unit | Decimal | Yes | kg |
| Gross Weight / Unit | Decimal | Yes | kg |

#### Generated Values
- Total Net Weight
- Total Gross Weight
- Total Packages
- CBM
- Chargeable Weight

#### Reports

##### Packing List Summary By HS Code

| HS Code | Qty PCS | Qty PKG | Total Net | Total Gross |
| :--- | :--- | :--- | :--- | :--- |

#### Business Rules
- Total Net = Qty × Net Weight.
- Total Gross = Qty × Gross Weight.
- Gross Weight ≥ Net Weight.
- Qty PCS و Qty PKG يجب أن تتطابق مع الفاتورة.

#### Validation
- عدم وجود أوزان سالبة.
- عدم وجود أبعاد صفرية عند الحاجة لحساب CBM.
- مطابقة إجمالى الكميات مع الفاتورة.

#### Edge Cases
- المورد لا يرسل أبعاد الطرود.
- المورد لا يرسل عدد البالتات.
- المورد لا يذكر الأسعار داخل Packing List.
- اختلاف Packing List عن الفاتورة.

#### Deliverables
- Packing List Validation Report
- Packing List Summary
- Shipment Items Details

#### Next Operation
➡ BP-004 Calculate CBM

---

### BP-004 – Calculate CBM

#### Purpose
احتساب الحجم الفعلى للشحنة (CBM) والوزن المحاسبى للشحن الجوى (Chargeable Weight) لتحديد وسيلة الشحن الأنسب.

#### Business Objective
- حساب CBM.
- حساب Chargeable Weight.
- تجهيز بيانات التسعير.
- تجهيز بيانات شركات الشحن.

#### System Usage
تستخدم فى:
- Determine Shipping Method
- Freight Quotations

#### Inputs
- Shipment Items

#### Required Fields

| Field | Type | Required | Notes |
| :--- | :--- | :--- | :--- |
| Qty PKG | Number | Yes | |
| Length | Decimal | Yes | cm |
| Width | Decimal | Yes | cm |
| Height | Decimal | Yes | cm |

#### Calculations

##### Ocean CBM
$$CBM = \frac{Qty \times Length \times Width \times Height}{1,000,000}$$

##### Air Chargeable Weight
$$Chargeable Weight = \frac{Qty \times Length \times Width \times Height}{6000}$$

#### Outputs
- Total CBM
- Total Chargeable Weight

#### Business Rules
- الحساب لكل طرد.
- ثم إجمالى الشحنة.
- الأبعاد بالسنتيمتر.

#### Validation
- جميع الأبعاد أكبر من صفر.
- Qty أكبر من صفر.

#### Edge Cases
- اختلاف أحجام الطرود.
- أكثر من نوع Package.

#### Deliverables
- CBM Report
- Air Chargeable Weight Report

#### Next Operation
➡ BP-005 Determine Shipping Method

---

### BP-005 – Determine Shipping Method

#### Purpose
اختيار وسيلة الشحن الأنسب بناءً على خصائص الشحنة، ومتطلبات التسليم، والوقت المتوقع، والتكلفة.

#### Business Objective
- اختيار وسيلة النقل.
- تقليل تكلفة الشحن.
- تحقيق موعد التسليم المطلوب.

#### System Usage
تستخدم فى:
- Freight Quotations
- Booking

#### Inputs
- CBM
- Chargeable Weight
- CRD
- Destination
- Shipment Priority

#### Possible Shipping Methods
- Ocean FCL
- Ocean LCL
- Air Freight
- Road Freight

#### Business Rules
يعتمد القرار على:
- حجم الشحنة.
- الوزن.
- موعد جاهزية الشحنة.
- موعد وصول العميل.
- تكلفة كل وسيلة.

#### Validation
- لا يمكن اختيار FCL بدون سعة مناسبة.
- لا يمكن اختيار Air إذا تجاوزت القيود التشغيلية أو التجارية.

#### Edge Cases
- إمكانية تقسيم الشحنة.
- تغيير وسيلة الشحن بسبب التأخير.

#### Deliverables
- Recommended Shipping Method
- Shipping Decision Report

#### Next Operation
➡ BP-006 Freight Quotations

---

### BP-006 – Freight Quotations

#### Purpose
الحصول على عروض أسعار الشحن من أكثر من مقدم خدمة ومقارنة التكلفة، ومواعيد الإبحار، وموعد الوصول المتوقع لاختيار أفضل عرض.

#### Business Objective
- مقارنة الأسعار.
- مقارنة Transit Time.
- اختيار أفضل رحلة.
- توقع موعد وصول البضاعة للمخزن.

#### System Usage
تستخدم فى:
- Booking
- ETA Calculation
- Purchase Planning

#### Inputs
- Shipment Summary
- CBM
- Chargeable Weight
- CRD
- Shipping Method

#### Required Fields

##### Header

| Field | Type | Required |
| :--- | :--- | :--- |
| CRD | Date | Yes |
| Port of Loading | Lookup | Yes |
| Port of Discharge | Lookup | Yes |
| Average Form 4 Days | Number | Yes |
| Average Clearance Days | Number | Yes |

##### Quotation Lines

| Field | Type |
| :--- | :--- |
| Shipping Provider | |
| Vessel | |
| Sailing Date | |
| Arrival Date | |
| Transit Time | |
| Expected Line Delay | |
| Freight Cost | |
| Free Time | |
| Remarks | |

#### Generated Values
- Transit Time
- Days Until Sailing
- Expected Arrival Date at Warehouse
- Average ETA
- Best Option

#### Business Rules
- يمكن إدخال أى عدد من عروض الأسعار.
- يتم حساب المتوسط تلقائياً.
- يمكن اختيار العرض الأفضل يدوياً.

#### Validation
- Arrival أكبر من Sailing.
- Sailing بعد CRD.
- جميع الأسعار مرتبطة بنفس وسيلة الشحن.

#### Edge Cases
- عدم توفر رحلة فى الموعد المطلوب.
- اختلاف Free Time.
- تغيير الخط الملاحى أثناء التفاوض.

#### Deliverables
- Freight Comparison Report
- ETA Report
- Recommended Shipping Option
- RFQ Email History

#### Next Operation
➡ BP-007 Customs Consultation

---

### BP-007 – Customs Consultation

#### Purpose
مراجعة مستندات الشحنة مع المخلص الجمركى قبل بدء الشحن للتأكد من توافقها مع متطلبات الجمارك المصرية، واعتماد البنود الجمركية، واكتشاف أى متطلبات أو مخاطر قبل تنفيذ عملية الاستيراد.

#### Business Objective
- اعتماد HS Code.
- مراجعة المستندات.
- التأكد من استيفاء جميع المتطلبات.
- تقدير الرسوم والضرائب.
- منع أى تأخير أو غرامات بعد الشحن.

#### System Usage
تستخدم فى:
- Estimate Duties
- Payment Request
- ACID
- Booking
- Final Documents Review

#### Inputs
- Proforma Invoice
- Packing List
- HS Code Summary
- Freight Summary
- Certificate of Origin (إن وجدت)

#### Customs Checklist

| Document | Required | Responsible | Received | Verified | Approval Status | Blocking Shipment | Received Date | Verified Date | Remarks |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| Proforma Invoice | ✔ | Customs Broker | | | | | | | |
| Commercial Invoice | ✔ | Customs Broker | | | | | | | |
| Packing List | ✔ | Customs Broker | | | | | | | |
| HS Code Confirmation | ✔ | Customs Broker | | | | | | | |
| Gross Weight Confirmation | ✔ | Customs Broker | | | | | | | |
| Certificate of Origin | حسب الحالة | Customs Broker | | | | | | | |
| Inspection Certificate | حسب الحالة | Customs Broker | | | | | | | |
| ACID Information | لاحقًا | Customs Broker | | | | | | | |
| Booking Confirmation | لاحقًا | Freight Forwarder | | | | | | | |
| Insurance Certificate | حسب Incoterm | Logistics Team | | | | | | | |

#### Business Rules
- لا يجوز الانتقال إلى مرحلة الحجز إذا كانت هناك متطلبات جمركية إلزامية غير مستوفاة.
- لكل مستند حالة مستقلة (Received / Verified / Approved).
- يمكن للمخلص طلب تعديل المستند أكثر من مرة مع الاحتفاظ بتاريخ جميع المراجعات والملاحظات.
- يجب تسجيل جميع الملاحظات والطلبات الصادرة من المخلص وربطها بالمستند المعني.

#### Validation
- التحقق من تسجيل الـ HS Code واعتماده.
- التأكد من توافق بيانات الفاتورة والـ Packing List.
- التحقق من وجود جميع المستندات الإلزامية.
- التحقق من توافق أوزان وقيم الشحنة مع القيود الجمركية الخاصة بنوع البضاعة.

#### Edge Cases
- HS Code يحتاج إلى إعادة تصنيف.
- الصنف يتطلب تسجيل مصنع (قرار 43 أو غيره).
- الصنف يحتاج موافقات من جهات رقابية (مثل الأمن العام أو الاتصالات أو جهات فنية أخرى).
- اختلاف بيانات المستندات يتطلب إعادة إصدارها من المورد.
- اكتشاف أن الشحنة لا تستوفي شروط الاستيراد قبل السداد.

#### Deliverables
- Customs Review Report.
- Approved / Rejected Documents Checklist.
- HS Code Validation Report.
- Required Actions List.
- Estimated Customs Requirements.

---

### BP-008 – Estimate Duties

#### Purpose
حساب وتقدير الرسوم الجمركية والضرائب المتوقعة للشحنة قبل تنفيذ عملية الشراء أو الشحن، وذلك بناءً على البنود الجمركية (HS Code) والقيمة الواردة فى الفاتورة المبدئية (Proforma Invoice)، بهدف معرفة التكلفة الإجمالية المتوقعة للاستيراد واتخاذ قرار الاستمرار فى العملية.

#### Business Objective
- تقدير الرسوم الجمركية قبل الشحن.
- حساب الضرائب المتوقعة لكل HS Code.
- معرفة التكلفة النهائية المتوقعة للاستيراد.
- دعم الإدارة فى اتخاذ قرار الشراء.
- تجهيز البيانات لطلب اعتماد الميزانية من الإدارة أو المالية.
- مقارنة التكلفة المتوقعة مع التكلفة الفعلية بعد التخليص الجمركى.

#### System Usage
تستخدم هذه العملية فى:
- Payment Request.
- Budget Approval.
- Landed Cost Calculation.
- Cost Analysis.
- Profitability Analysis.
- Customs Clearance Comparison.
- Financial Planning.

#### Inputs
- Import File.
- Proforma Invoice Summary.
- Packing List Summary.
- HS Code Summary.
- Customs Consultation Results.
- Customs Tariff Master Data.

#### Required Fields

##### Shipment Header

| Field | Type | Required | Notes |
| :--- | :--- | :--- | :--- |
| Import File ID | Lookup | Yes | |
| Currency | Lookup | Yes | عملة الفاتورة |
| Exchange Rate | Decimal | Yes | سعر الصرف المستخدم فى التقدير |
| Estimate Date | Date | Yes | تاريخ إعداد التقدير |
| Prepared By | User | Yes | |
| Reviewed By | User | No | |

##### Estimate Details

| Field | Type | Required | Notes |
| :--- | :--- | :--- | :--- |
| HS Code | Text | Yes | |
| Description | Text | No | |
| Amount | Decimal | Yes | إجمالى قيمة البند |
| Customs Duty % | Decimal | Yes | نسبة الرسوم الجمركية |
| Customs Duty Amount | Calculated | Yes | |
| VAT % | Decimal | Yes | غالباً 14% حسب اللوائح السارية |
| VAT Amount | Calculated | Yes | |
| Development Tax % | Decimal | No | حسب نوع الصنف |
| Development Tax Amount | Calculated | No | |
| Other Government Fees | Decimal | No | أى رسوم إضافية |
| Total Estimated Duties | Calculated | Yes | إجمالى الرسوم والضرائب للبند |
| Remarks | Text | No | |

#### Outputs
- Estimated Duties Report.
- Estimated Taxes Report.
- Total Estimated Import Cost.
- Duties Summary by HS Code.
- Budget Estimate.

#### Reports

##### Estimated Duties Summary

| HS Code | Amount | Customs Duties | VAT | Development Tax | Other Fees | Total Estimated Duties |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |

##### Shipment Estimated Cost Summary

| Description | Amount |
| :--- | :--- |
| Invoice Value | |
| Estimated Customs Duties | |
| Estimated VAT | |
| Estimated Development Tax | |
| Other Government Fees | |
| Total Estimated Import Cost | |

#### Business Rules
- يتم احتساب الرسوم لكل HS Code بشكل مستقل.
- تختلف نسب الرسوم والضرائب حسب التعريفة الجمركية الخاصة بكل HS Code.
- يمكن أن تحتوى الشحنة الواحدة على عدة بنود جمركية، ولكل بند نسب مختلفة.
- يتم حفظ نسب الضرائب المستخدمة وقت إعداد التقدير حتى لو تغيرت التعريفة لاحقًا.
- لا يجوز تعديل نسب الرسوم يدويًا إلا من مستخدم مخول، مع تسجيل سبب التعديل.
- هذا التقدير استرشادى ولا يمثل المطالبة الجمركية النهائية الصادرة من مصلحة الجمارك.

#### Validation
- يجب أن يكون لكل Item HS Code معتمد.
- يجب أن تكون قيمة البند أكبر من صفر.
- يجب وجود تعريف جمركى لكل HS Code.
- التحقق من صحة العملة وسعر الصرف المستخدم.
- مراجعة إجمالى قيمة الفاتورة مع إجمالى البنود المستخدمة فى الحساب.

#### Edge Cases
- وجود HS Code غير معرف فى جدول التعريفة الجمركية.
- وجود بند يحتاج إلى موافقات خاصة تؤثر على الرسوم.
- اختلاف الرسوم بين التقدير الأولى والمطالبة الجمركية النهائية.
- تعديل التعريفة الجمركية أثناء فترة الشحن.
- تطبيق إعفاءات أو اتفاقيات تجارية (مثل اتفاقيات المنشأ أو الإعفاءات الجمركية) تؤثر على الرسوم.
- وجود رسوم إضافية خاصة بجهات رقابية أو سلع معينة.

#### Deliverables
- Estimated Duties Report.
- Estimated Import Cost Report.
- HS Code Tax Analysis.
- Budget Approval Summary.
- Estimated Landed Cost.

#### Dependencies

##### Previous Operations
- BP-002 Review Proforma Invoice.
- BP-003 Review Packing List.
- BP-007 Customs Consultation.

##### Next Operation
➡ BP-009 – Payment Request

#### Dashboard Impact
- تحديث حالة عملية Estimate Duties إلى Completed.
- إظهار إجمالى الرسوم والضرائب المتوقعة فى لوحة متابعة الشحنة.
- إظهار مؤشر يوضح ما إذا كانت تكلفة الاستيراد التقديرية تقع ضمن الميزانية المعتمدة للمشروع.
- السماح بالانتقال إلى Payment Request بعد اعتماد التقدير.

#### Notes for Developer
- لا يتم تخزين نسب الرسوم والضرائب داخل هذا الجدول بشكل ثابت؛ يجب قراءتها من Customs Tariff Master Data وقت إنشاء التقدير، ثم حفظ نسخة (Snapshot) من القيم المستخدمة داخل سجل التقدير حتى تظل مرجعًا تاريخيًا حتى إذا تغيرت التعريفة لاحقًا.
- يجب تصميم النظام بحيث يدعم إضافة أنواع جديدة من الرسوم أو الضرائب مستقبلًا دون الحاجة إلى تعديل هيكل قاعدة البيانات، وذلك بالاعتماد على جدول مرجعى لأنواع الرسوم (Duty & Tax Types) وربطه بتفاصيل التقدير، بدلاً من إنشاء أعمدة ثابتة لكل نوع رسم. هذا سيجعل النظام مرنًا وقابلًا للتوسع مع تغير التشريعات الجمركية.

---

### BP-009 – Payment Request

#### Purpose
إصدار طلب رسمي للإدارة المالية لسداد قيمة الفاتورة المبدئية (Proforma Invoice) أو جزء منها (مثل الدفعة المقدمة Advance Payment) للمورد الأجنبي، وذلك لتأكيد الطلب وبدء عملية التصنيع أو الشحن.

#### Business Objective
- توثيق واعتماد طلبات السداد الموجهة للإدارة المالية.
- ربط الدفعات المالية بملف الاستيراد (Import File) والفاتورة المبدئية.
- متابعة حالة الدفع (مدفوع جزئياً، مدفوع بالكامل).
- دعم تخطيط التدفقات النقدية (Cash Flow Planning).
- ضمان عدم تجاوز إجمالي المدفوعات لقيمة الفاتورة المعتمدة.

#### System Usage
تستخدم هذه العملية فى:
- Financial Approvals.
- Cash Flow Management.
- Form 4 Preparation (نموذج 4).
- Supplier Account Statement.
- Cost Allocation.

#### Inputs
- Import File.
- Approved Proforma Invoice.
- Supplier Bank Details (من جدول Supplier Master Data).
- Estimated Duties (لإعطاء الإدارة المالية رؤية كاملة عن التكلفة).

#### Required Fields

##### Header Information

| Field | Type | Required | Notes |
| :--- | :--- | :--- | :--- |
| Payment Request ID | Auto Number | Yes | Primary Key |
| Import File ID | Lookup | Yes | رقم ملف الاستيراد |
| Proforma Invoice No | Lookup | Yes | الفاتورة المرتبطة بالطلب |
| Supplier Name | Read-Only | Yes | يسحب تلقائياً من الملف |
| Payment Type | Lookup | Yes | Advance Payment / Against BL / Final Settlement |
| Requested Amount | Decimal | Yes | المبلغ المطلوب تحويله |
| Currency | Read-Only | Yes | عملة الفاتورة المبدئية |
| Due Date | Date | Yes | تاريخ الاستحقاق المطلوب |
| Request Date | Date | Yes | تاريخ إنشاء الطلب |
| Status | Lookup | Yes | Draft / Pending Approval / Approved / Paid / Rejected |

##### Supplier Bank Details

| Field | Type | Required | Notes |
| :--- | :--- | :--- | :--- |
| Bank Name | Text | Yes | بنك المورد المستفيد |
| Swift Code | Text | Yes | |
| IBAN / Account No | Text | Yes | |
| Beneficiary Name | Text | Yes | يجب أن يتطابق مع اسم المورد الرسمي |

#### Outputs
- Payment Request Document (مستند طلب الدفع).
- Pending Payment Notification للإدارة المالية.
- تحديث الرصيد المتبقي (Remaining Balance) للفاتورة.

#### Business Rules
- لا يمكن إنشاء طلب دفع لفاتورة لم يتم اعتمادها.
- إجمالي مبالغ طلبات الدفع المرتبطة بفاتورة واحدة يجب ألا يتجاوز القيمة الإجمالية للـ Proforma Invoice (إلا في حدود نسبة سماحية محددة مسبقاً إذا لزم الأمر).
- يجب أن يتم سحب بيانات بنك المورد تلقائياً من الـ Master Data، وفي حال تغييرها يجب أن يتطلب ذلك موافقة إدارية (لأسباب أمنية لمنع الاحتيال).
- بمجرد تحويل حالة الطلب إلى "Paid"، يجب إرفاق مستند التحويل البنكي (Swift Copy).

#### Validation
- التحقق من أن (Requested Amount > 0).
- التحقق من أن (Requested Amount + Previous Payments ≤ Total Invoice Amount).
- التأكد من اكتمال بيانات البنك الخاصة بالمورد (Swift, IBAN).

#### Edge Cases
- تغير بيانات الحساب البنكي للمورد بناءً على تعليمات جديدة (يتطلب تحديث Master Data مع Audit Trail).
- دفع عمولات التحويل البنكي (Bank Charges) هل يتحملها المورد (SHA/BEN) أم المستورد (OUR)؟ يجب تحديدها في الطلب.
- تقلبات أسعار الصرف القوية بين تاريخ طلب الدفع وتاريخ التنفيذ الفعلي من البنك.
- رفض البنك للتحويل بسبب نقص المستندات أو أخطاء في الـ Swift Code.

#### Dependencies

##### Previous Operations
- BP-002 Review Proforma Invoice.
- BP-008 Estimate Duties (يفضل وجود تقدير التكلفة قبل الدفع).

##### Next Operation
➡ BP-010 – ACID Request & Form 4 Issuance (حسب الترتيب الفعلي للشركة، غالباً يتم إصدار رقم نافذة ونموذج 4 بالتزامن مع التحويل البنكي).

#### Notifications
- إشعار للإدارة المالية بوجود طلب دفع جديد معلق للاعتماد.
- إشعار لمدير المشتريات/الاستيراد عند تغيير حالة الطلب إلى "Paid" لإبلاغ المورد بالبدء.

#### Dashboard Impact
- تغيير حالة الشحنة المالي إلى "Payment Processing" أو "Partially Paid".
- ظهور المبلغ في مؤشرات "Cash Outflow" الخاصة بالشهر الحالي.
- تحديث شريط التقدم (Progress Bar) لملف الاستيراد للإشارة إلى تخطي مرحلة الدفع الأولي.

#### Notes for Developer
- يجب فصل صلاحيات إنشاء طلب الدفع (مختص الاستيراد) عن صلاحيات تغيير حالة الطلب إلى Paid (الإدارة المالية).
- تأكد من تطبيق Lock على حقل Requested Amount بمجرد انتقال الطلب إلى حالة Pending Approval لمنع التعديل أثناء مراجعة الحسابات.
- قم ببرمجة نظام تحذير (Alert) إذا كانت بيانات بنك المورد المرفقة في الفاتورة مختلفة عن تلك المسجلة في الـ Master Data.
