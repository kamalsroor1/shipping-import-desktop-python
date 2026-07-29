# BRD Part 2: Master Data Specifications (MD-001 to MD-007)

## MD-001 Company (Egyptian Importers)
يستخدم هذا الجدول لإدارة جميع الشركات المصرية التي يتم الاستيراد باسمها.
- **الحقول المفتاحية**: `Egyptian Importer Name`, `Address`, `Importer ID`, `Importer ID Expiration Date`, `VAT ID`, `VAT ID Expiration Date`, `Commercial Registration No`, `Commercial Registration Expiration Date`.
- **قواعد العمل**: حساب أيام التجديد تلقائياً (`Days to Renew`) دون تخزينها بل حسابها ديناميكياً.

## MD-002 Supplier (Foreign Exporters)
يستخدم هذا الجدول لتخزين جميع بيانات الموردين الأجانب (Foreign Exporters).
- **الحقول المفتاحية**: `Vendor Company Name`, `Registration Type`, `Foreign Exporter ID`, `Foreign Exporter Country`, `Country Code`, `Address`, `Bank SWIFT/IBAN`.
- **قواعد العمل**: قيد الفرادة المركب على `(Registration Type, Foreign Exporter ID)`.

## MD-003 External Service Providers
مرجع موحد لـ: `Freight Forwarder`, `Customs Broker`, `Inspection Company`, `Insurance Company`, `Courier Company`, `Shipping Agent`, `Trucking Company`.

## MD-004 Shipping Lines & MD-005 Currency
- توحيد أسماء وعناوين الخطوط الملاحية والـ SCAC Codes.
- كود ISO العملة، الرمز، والكسور العشرية.

## MD-006 Incoterms 2020 Matrix
توزيع المسئوليات والتكاليف بين المستورد والمورد عبر ربط `Incoterms` بـ `Cost Items` وقواعد المسئوليات (`Importer / Exporter / Shared`).

## MD-007 Projects Hub
ربط ملفات الاستيراد بالمشاريع والشركة المستوردة والمورد وشرط التسليم الأساسي.
