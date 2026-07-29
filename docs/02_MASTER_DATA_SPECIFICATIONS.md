# 02. Master Data Specifications (MD-001 to MD-010)

Master Data represents the core reference entities of the system. All transactions (Projects, Import Files, ACID Requests, Bookings, Customs Clearances) reference Master Data records. Direct hardcoded string entry inside transactions is strictly prohibited.

---

## MD-001: Egyptian Importers (Company Master)
Manages legal entity data for Egyptian importing companies. Supports multi-company management within a single database.

### Main Fields
| Field Name | Data Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `company_id` | Auto Number | Yes | Primary Key |
| `egyptian_importer_name` | Text | Yes | Official Legal Name |
| `address` | Text | Yes | Registered Business Address |
| `country` | Text | Yes | Country (Default: Egypt) |
| `importer_id` | Text | Yes | Import Card / License Number |
| `importer_id_expiration_date` | Date | Yes | Expiration Date of Import Card |
| `vat_id` | Text | Yes | Tax Registration / VAT Number |
| `vat_id_expiration_date` | Date | Yes | VAT Expiration Date |
| `commercial_registration_no` | Text | Yes | Commercial Register Number |
| `commercial_registration_expiration` | Date | Yes | Commercial Register Expiry |
| `status` | Lookup | Yes | Active / Inactive / Soft Deleted |

### Business Rules
- **Days to Renew**: Calculated dynamically (`Expiry Date - Today`). Never stored as a static database column.
- **Expiration Alerts**: Automatic workspace warnings when documents are within 30 days of expiry.
- **Deletion**: Soft deletion (`deleted_at`) only. Companies linked to projects cannot be deleted.

---

## MD-002: Foreign Exporters (Supplier Master)
Stores legal information for foreign suppliers/exporters.

### Main Fields
| Field Name | Data Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `supplier_id` | Auto Number | Yes | Primary Key |
| `vendor_company_name` | Text | Yes | Official Legal Exporter Name |
| `registration_type` | Lookup | Yes | `Company` or `Individual` |
| `foreign_exporter_id` | Text | Yes | Official Foreign Tax/Company Registration ID |
| `foreign_exporter_country` | Text | Yes | Country of Origin/Export |
| `foreign_exporter_country_code` | Text | Yes | ISO 2-letter Country Code (e.g., CN, DE, US) |
| `address` | Text | No | Complete Factory / Office Address |
| `phone_number` | Text | No | Primary Contact Phone |
| `email` | Text | No | Official Business Email |
| `brands` | Text | No | Brands / Product Categories |
| `bank_name` | Text | No | Default Beneficiary Bank |
| `swift_code` | Text | No | Beneficiary Bank SWIFT |
| `iban_account_no` | Text | No | IBAN / Account Number |
| `status` | Lookup | Yes | Active / Inactive |

### Business Rules
- **Uniqueness Constraint**: `(registration_type, foreign_exporter_id)` MUST be unique.
- **Nafeza / CargoX Critical Alignment**: Vendor Name, Registration ID, Country Code, and Address MUST match official documents exactly to prevent ACID rejection.

---

## MD-003: External Service Providers
Unified partner database storing Freight Forwarders, Customs Brokers, Inspection Agencies, Courier Companies, Shipping Line Agents, and Insurance Providers.

### Main Fields
| Field Name | Data Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `partner_id` | Auto Number | Yes | Primary Key |
| `partner_name` | Text | Yes | Legal Company Name |
| `partner_type` | Lookup | Yes | `Freight Forwarder`, `Customs Broker`, `Inspection Company`, `Insurance Company`, `Courier Company`, `Shipping Agent`, `Trucking Company` |
| `contact_person` | Text | No | Primary Contact Person |
| `phone_number` | Text | No | Landline Phone |
| `mobile_number` | Text | No | Mobile Phone |
| `email` | Text | No | Contact Email |
| `address` | Text | No | Business Address |
| `payment_type` | Lookup | No | `Cash` or `Credit` |
| `credit_limit` | Decimal | No | Credit Limit Amount |
| `status` | Lookup | Yes | Active / Inactive |

### Business Rules
- A single entity can hold multiple partner roles (e.g., Freight Forwarder and Customs Broker).
- `(partner_name, partner_type)` must be unique.

---

## MD-004: Shipping Lines
Reference list of ocean and air carriers.

| Field Name | Data Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `shipping_line_id` | Auto Number | Yes | Primary Key |
| `shipping_line_name` | Text | Yes | Carrier Name (e.g., Maersk, MSC, COSCO) |
| `scac_code` | Text | No | Standard Carrier Alpha Code |
| `website` | Text | No | Tracking Portal URL |
| `status` | Lookup | Yes | Active / Inactive |

---

## MD-005: Currency Reference
Supported transactional currencies.

| Field Name | Data Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `currency_id` | Auto Number | Yes | Primary Key |
| `iso_code` | Text | Yes | ISO 4217 3-letter code (USD, EUR, EGP, GBP) |
| `currency_name` | Text | Yes | Currency Description |
| `symbol` | Text | No | Symbol ($, €, £, EGP) |
| `decimal_places` | Integer | Yes | Default: 2 |

---

## MD-006: Incoterms 2020 Matrix & Cost Items
Data-driven responsibility matrix based on Incoterms 2020. Eliminates static boolean columns by establishing relational mapping between Incoterms, Cost Items, and Responsible Parties.

### Table 1: `incoterms`
- `incoterm_id`, `incoterm_code` (EXW, FOB, CIF, CFR, DDP), `name`, `version` (Incoterms 2020).

### Table 2: `cost_items`
- `cost_item_id`, `cost_item_name`, `category`
- *Examples*: Origin Trucking, Export Clearance, OTHC, Ocean Freight, Insurance, Origin Inspection, Documentation, DTHC, Customs Clearance, Form 4 Fees, Duties & Taxes, Storage, Demurrage & Detention, Port Congestion, Compliance Fees.

### Table 3: `incoterm_responsibilities`
- `id`, `incoterm_id` (FK), `cost_item_id` (FK), `responsible_party` (`Importer`, `Exporter`, `Shared`), `is_included` (Boolean).

---

## MD-007: Projects Master
Primary operational grouping unit linking Importers, Foreign Exporters, Default Incoterms, and Import Types.

| Field Name | Data Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `project_id` | Auto Number | Yes | Primary Key |
| `project_code` | Text | Yes | Unique Project Code |
| `project_name` | Text | Yes | Descriptive Project Name |
| `project_owner` | Text | Yes | Responsible Operations Lead |
| `company_id` | FK | Yes | Importer Entity Reference |
| `supplier_id` | FK | Yes | Foreign Supplier Reference |
| `incoterm_id` | FK | Yes | Default Incoterm Reference |
| `import_type_id` | FK | Yes | Commercial, Sample, Spare Parts, Machinery, Raw Materials, Temporary Admission, Re-Import, Personal |
| `priority_id` | FK | Yes | `High`, `Medium`, `Low` |
| `shipment_category_id` | FK | Yes | New Purchase, Repeat Order, Urgent, Project Shipment, Consolidated, Partial |
| `status` | Lookup | Yes | Open, Closed, On Hold |

---

## MD-008: Customs Tariff (HS Code Master)
Master reference repository for Harmonized System Codes, tariff percentages, and regulatory authority approvals.

| Field Name | Data Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `tariff_id` | Auto Number | Yes | Primary Key |
| `hs_code` | Text | Yes | Harmonized System Code (e.g., 6701067200) |
| `hs_description` | Text | Yes | Official Egyptian Customs Description |
| `customs_duty_pct` | Decimal | Yes | Customs Duty Percentage (%) |
| `vat_pct` | Decimal | Yes | Value Added Tax Percentage (Default: 14%) |
| `development_tax_pct` | Decimal | No | Development Tax Percentage (%) |
| `additional_fees_pct` | Decimal | No | Additional Regulatory Fees (%) |
| `requires_coo` | Boolean | Yes | Requires Certificate of Origin |
| `requires_inspection` | Boolean | Yes | Requires Pre-Shipment Inspection Certificate |
| `requires_acid` | Boolean | Yes | Requires Nafeza ACID Number |
| `regulatory_authority` | Lookup | No | Regulatory Agency (GOEIC, NTRA, MOH, Security) |

---

## MD-009: Transport Locations (Ports & Airports)
Unified repository for international Sea Ports, Airports, Dry Ports, and Inland Depots.

| Field Name | Data Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `location_id` | Auto Number | Yes | Primary Key |
| `location_name` | Text | Yes | Official Location Name |
| `un_locode` | Text | Yes | UN/LOCODE (e.g., EGALY, CNSHA, DEHAM) |
| `location_type` | Lookup | Yes | `Sea Port`, `Airport`, `Dry Port`, `ICD`, `Rail Terminal` |
| `country` | Text | Yes | Country Name |
| `city` | Text | Yes | City Name |

---

## MD-010: Container Specifications Master
Standard ISO container specifications database for cargo loading optimization and weight/space calculations.

| Field Name | Data Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `container_spec_id` | Auto Number | Yes | Primary Key |
| `container_type` | Text | Yes | 20GP, 40GP, 40HC, 45HC, Open Top, Flat Rack |
| `iso_code` | Text | No | ISO Container Type Code |
| `internal_length_cm` | Decimal | Yes | Internal Length in cm |
| `internal_width_cm` | Decimal | Yes | Internal Width in cm |
| `internal_height_cm` | Decimal | Yes | Internal Height in cm |
| `door_width_cm` | Decimal | Yes | Door Opening Width in cm |
| `door_height_cm` | Decimal | Yes | Door Opening Height in cm |
| `cubic_capacity_cbm` | Decimal | Yes | Total Volume Capacity in CBM |
| `tare_weight_kg` | Decimal | Yes | Empty Container Weight in kg |
| `max_payload_kg` | Decimal | Yes | Maximum Allowed Payload in kg |
| `max_gross_weight_kg` | Decimal | Yes | Maximum Total Gross Weight in kg |
| `floor_area_sqm` | Decimal | Yes | Total Floor Area in m² |
| `supports_stacking` | Boolean | Yes | Supports pallet stacking |
