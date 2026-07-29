-- =====================================================================
-- Import Management System - Database Schema (PostgreSQL)
-- Consolidated from: BRD (Master Data + Business Process), raw workflow
-- narrative, and the working Excel prototype (work_flow-2.xlsx)
-- =====================================================================
-- Conventions used throughout:
--   * All PKs are BIGSERIAL (int8, auto-increment)
--   * Soft delete via deleted_at (per GP-003/GP-004 developer notes)
--   * Audit columns (created_at, updated_at, created_by, updated_by)
--     on every table to satisfy GP-004 Audit Trail
--   * Money stored as NUMERIC(18,4); rates as NUMERIC(7,4)
--   * Lookup-style master tables use a `code` unique text column so
--     they read/insert without depending on surrogate IDs from the UI
-- =====================================================================

-- ---------------------------------------------------------------------
-- 0. Shared audit trail (GP-004) - generic, works for any table
-- ---------------------------------------------------------------------
CREATE TABLE audit_log (
    audit_log_id     BIGSERIAL PRIMARY KEY,
    table_name        VARCHAR(64)  NOT NULL,
    record_id         BIGINT       NOT NULL,
    action            VARCHAR(32)  NOT NULL, -- create / update / status_change / delete / approve / reject
    screen_name       VARCHAR(128),
    change_summary    TEXT,
    performed_by      BIGINT       NOT NULL, -- FK to users, users table not modeled here
    performed_at      TIMESTAMPTZ  NOT NULL DEFAULT now()
);
CREATE INDEX idx_audit_log_table_record ON audit_log(table_name, record_id);

-- =====================================================================
-- 1. MASTER DATA (reference tables - MD-001 .. MD-011)
-- =====================================================================

-- MD-001 Company (Egyptian Importer)
CREATE TABLE companies (
    company_id                          BIGSERIAL PRIMARY KEY,
    egyptian_importer_name              VARCHAR(255) NOT NULL,
    address                             TEXT NOT NULL,
    country                             VARCHAR(100) NOT NULL,
    importer_id                         VARCHAR(64)  NOT NULL,
    importer_id_expiration_date         DATE NOT NULL,
    vat_id                              VARCHAR(64)  NOT NULL,
    vat_id_expiration_date              DATE NOT NULL,
    commercial_registration_no          VARCHAR(64)  NOT NULL,
    commercial_registration_expiration  DATE NOT NULL,
    status                              VARCHAR(16)  NOT NULL DEFAULT 'active'
                                         CHECK (status IN ('active','inactive')),
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by   BIGINT,
    updated_by   BIGINT,
    deleted_at   TIMESTAMPTZ
);
-- Note: "days to renew" fields are NEVER stored - computed as
--   (expiration_date - CURRENT_DATE) at query time.

-- MD-002 Supplier (Foreign Exporter)
CREATE TABLE suppliers (
    supplier_id           BIGSERIAL PRIMARY KEY,
    vendor_company_name   VARCHAR(255) NOT NULL,
    registration_type     VARCHAR(32)  NOT NULL CHECK (registration_type IN ('Company','Individual')),
    foreign_exporter_id   VARCHAR(64)  NOT NULL,
    foreign_exporter_country      VARCHAR(100) NOT NULL,
    foreign_exporter_country_code VARCHAR(8)   NOT NULL,
    address               TEXT,
    phone_number          VARCHAR(32),
    email                 VARCHAR(255),
    brands                TEXT,
    status                VARCHAR(16) NOT NULL DEFAULT 'active' CHECK (status IN ('active','inactive')),
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by   BIGINT,
    updated_by   BIGINT,
    deleted_at   TIMESTAMPTZ,
    UNIQUE (registration_type, foreign_exporter_id)
);

-- MD-004 External Service Providers / Business Partners (merged MD-003+MD-004)
CREATE TABLE service_providers (
    partner_id       BIGSERIAL PRIMARY KEY,
    partner_name     VARCHAR(255) NOT NULL,
    partner_type     VARCHAR(32)  NOT NULL
                      CHECK (partner_type IN
                        ('Freight Forwarder','Customs Broker','Inspection Company',
                         'Insurance Company','Courier','Shipping Agent','Bank','Trucking Company')),
    contact_person   VARCHAR(255),
    phone_number     VARCHAR(32),
    mobile_number    VARCHAR(32),
    email            VARCHAR(255),
    address          TEXT,
    country          VARCHAR(100),
    payment_type     VARCHAR(16) CHECK (payment_type IN ('cash','credit')),
    credit_limit     NUMERIC(18,4) CHECK (credit_limit >= 0),
    notes            TEXT,
    status           VARCHAR(16) NOT NULL DEFAULT 'active' CHECK (status IN ('active','inactive')),
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by   BIGINT,
    updated_by   BIGINT,
    deleted_at   TIMESTAMPTZ,
    UNIQUE (partner_name, partner_type)
);

-- MD-005 Shipping Lines
CREATE TABLE shipping_lines (
    shipping_line_id  BIGSERIAL PRIMARY KEY,
    shipping_line_name VARCHAR(255) NOT NULL UNIQUE,
    scac_code         VARCHAR(16),
    country           VARCHAR(100),
    website           VARCHAR(255),
    status            VARCHAR(16) NOT NULL DEFAULT 'active' CHECK (status IN ('active','inactive')),
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at   TIMESTAMPTZ
);

-- MD-006 Currency
CREATE TABLE currencies (
    currency_id     BIGSERIAL PRIMARY KEY,
    iso_code        CHAR(3) NOT NULL UNIQUE CHECK (char_length(iso_code) = 3),
    currency_name   VARCHAR(100) NOT NULL,
    symbol          VARCHAR(8),
    decimal_places  SMALLINT NOT NULL DEFAULT 2,
    status          VARCHAR(16) NOT NULL DEFAULT 'active' CHECK (status IN ('active','inactive'))
);

-- MD-007 Incoterms + Cost Items + Responsibilities (data-driven, per GP design notes)
CREATE TABLE incoterms (
    incoterm_id   BIGSERIAL PRIMARY KEY,
    incoterm_code VARCHAR(8)  NOT NULL UNIQUE,  -- EXW / FOB / CIF / CFR ...
    name          VARCHAR(100) NOT NULL,
    description   TEXT,
    version       VARCHAR(16) NOT NULL DEFAULT 'Incoterms 2020',
    status        VARCHAR(16) NOT NULL DEFAULT 'active' CHECK (status IN ('active','inactive'))
);

CREATE TABLE cost_items (
    cost_item_id   BIGSERIAL PRIMARY KEY,
    cost_item_name VARCHAR(100) NOT NULL UNIQUE, -- Origin Trucking, OTHC, O/F, DTHC, Demurrage, ...
    category       VARCHAR(64)
);

CREATE TABLE incoterm_cost_rules (
    id                 BIGSERIAL PRIMARY KEY,
    incoterm_id        BIGINT NOT NULL REFERENCES incoterms(incoterm_id),
    cost_item_id        BIGINT NOT NULL REFERENCES cost_items(cost_item_id),
    responsible_party   VARCHAR(16) NOT NULL CHECK (responsible_party IN ('Importer','Exporter','Shared')),
    is_included         BOOLEAN NOT NULL DEFAULT true,
    notes               TEXT,
    UNIQUE (incoterm_id, cost_item_id)
);

-- MD-009 Ports (new - referenced throughout BP-001..BP-006 but undefined before)
CREATE TABLE ports (
    port_id     BIGSERIAL PRIMARY KEY,
    port_name   VARCHAR(150) NOT NULL,
    port_code   VARCHAR(16),
    country     VARCHAR(100),
    status      VARCHAR(16) NOT NULL DEFAULT 'active' CHECK (status IN ('active','inactive')),
    UNIQUE (port_name, country)
);

-- MD-010 HS Code / Customs Tariff (new - closes the BP-008 gap; rates are
-- read at estimate time, then snapshotted onto the estimate row itself)
CREATE TABLE hs_codes (
    hs_code           VARCHAR(20) PRIMARY KEY,
    description       TEXT,
    customs_duty_pct  NUMERIC(7,4) NOT NULL DEFAULT 0,  -- current rate, e.g. 0.40
    vat_pct           NUMERIC(7,4) NOT NULL DEFAULT 0.14,
    development_tax_pct NUMERIC(7,4) NOT NULL DEFAULT 0,
    -- air-shipment "sample" threshold rule captured as data, not hardcoded logic
    max_sample_weight_kg  NUMERIC(10,2),
    max_sample_value_usd  NUMERIC(18,4),
    status            VARCHAR(16) NOT NULL DEFAULT 'active' CHECK (status IN ('active','inactive')),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Generic document reference system (replaces the 4 hardcoded checklists
-- found in BP-007 / supplier docs / customs docs / final review in the xlsx)
CREATE TABLE document_types (
    doc_type_id      BIGSERIAL PRIMARY KEY,
    document_category VARCHAR(32) NOT NULL
                       CHECK (document_category IN
                         ('Commercial','Certificate','Shipping','Egypt Import','Customs')),
    document_name    VARCHAR(150) NOT NULL,
    default_required VARCHAR(16) NOT NULL DEFAULT 'Yes'
                       CHECK (default_required IN ('Yes','No','Conditional')),
    default_responsible_party VARCHAR(32), -- Supplier / Freight Forwarder / Customs Broker / Company / Finance / Warehouse / Bank
    UNIQUE (document_category, document_name)
);

-- MD - Container types (20GP / 40HC / LCL ...), used for freight cost breakdown
CREATE TABLE container_types (
    container_type_id BIGSERIAL PRIMARY KEY,
    code              VARCHAR(16) NOT NULL UNIQUE, -- 20GP, 40HC, LCL
    description       VARCHAR(100)
);

-- Simple fixed lookups (Mode, Import Type, Priority, Shipment Category)
CREATE TABLE shipping_modes (
    mode_id BIGSERIAL PRIMARY KEY,
    code    VARCHAR(16) NOT NULL UNIQUE  -- Sea / Air
);

CREATE TABLE import_types (
    import_type_id BIGSERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL UNIQUE -- Commercial Import / Sample / Spare Parts / Machinery / ...
);

CREATE TABLE priorities (
    priority_id BIGSERIAL PRIMARY KEY,
    name VARCHAR(32) NOT NULL UNIQUE -- High / Medium / Low
);

CREATE TABLE shipment_categories (
    shipment_category_id BIGSERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL UNIQUE -- New Purchase / Repeat Order / Urgent / Project / Consolidated / Partial
);

-- =====================================================================
-- 2. PROJECT & IMPORT FILE (the transactional hub)
-- =====================================================================

-- MD-008 Projects
CREATE TABLE projects (
    project_id             BIGSERIAL PRIMARY KEY,
    project_code            VARCHAR(64) NOT NULL UNIQUE,
    project_name            VARCHAR(255) NOT NULL,
    project_owner            VARCHAR(255) NOT NULL,
    company_id               BIGINT NOT NULL REFERENCES companies(company_id),
    supplier_id               BIGINT NOT NULL REFERENCES suppliers(supplier_id),
    incoterm_id               BIGINT NOT NULL REFERENCES incoterms(incoterm_id),
    import_type_id            BIGINT NOT NULL REFERENCES import_types(import_type_id),
    priority_id               BIGINT NOT NULL REFERENCES priorities(priority_id),
    shipment_category_id      BIGINT NOT NULL REFERENCES shipment_categories(shipment_category_id),
    status                    VARCHAR(16) NOT NULL DEFAULT 'open' CHECK (status IN ('open','closed','on_hold')),
    notes                     TEXT,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by   BIGINT,
    updated_by   BIGINT,
    deleted_at   TIMESTAMPTZ
);

-- Import File = one shipment. This is the central hub every other
-- transactional table hangs off of. current_stage mirrors the
-- Module/Stage state machine found in the xlsx "Current Stage" table.
CREATE TABLE import_files (
    import_file_id     BIGSERIAL PRIMARY KEY,
    import_file_code    VARCHAR(64) NOT NULL UNIQUE,  -- e.g. IMP-2026-0001
    project_id           BIGINT NOT NULL REFERENCES projects(project_id),
    mode_id              BIGINT NOT NULL REFERENCES shipping_modes(mode_id),
    shipping_port_id      BIGINT REFERENCES ports(port_id),
    destination_port_id   BIGINT REFERENCES ports(port_id),
    current_module        VARCHAR(32) NOT NULL DEFAULT 'Pre-Shipment'
                           CHECK (current_module IN
                             ('Pre-Shipment','Shipment','Customs Clearance','Financial','Warehouse','Closing')),
    current_stage         VARCHAR(64) NOT NULL DEFAULT 'Planning',
    crd_date              DATE,  -- Cargo Ready Date
    is_closed              BOOLEAN NOT NULL DEFAULT false,
    last_modified_notes    TEXT,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by   BIGINT,
    updated_by   BIGINT,
    deleted_at   TIMESTAMPTZ
);
CREATE INDEX idx_import_files_project ON import_files(project_id);
CREATE INDEX idx_import_files_stage ON import_files(current_module, current_stage);

-- =====================================================================
-- 3. PROFORMA INVOICE / PACKING LIST (BP-001, BP-002, BP-003)
-- =====================================================================

CREATE TABLE proforma_invoices (
    pi_id               BIGSERIAL PRIMARY KEY,
    import_file_id       BIGINT NOT NULL REFERENCES import_files(import_file_id),
    pi_no                 VARCHAR(64) NOT NULL,
    pi_date               DATE NOT NULL,
    invoice_date           DATE NOT NULL,
    invoice_type           VARCHAR(32) NOT NULL, -- PI / Sample / Replacement
    purchase_order_no      VARCHAR(64) NOT NULL,
    purchase_order_date    DATE NOT NULL,
    currency_id            BIGINT NOT NULL REFERENCES currencies(currency_id),
    total_value            NUMERIC(18,4) NOT NULL DEFAULT 0, -- = SUM(invoice_items.amount)
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (import_file_id, pi_no)
);
-- Note: BP-001 Validation says "no duplicate PI number for the same
-- supplier" ("لا يسمح بتكرار رقم الفاتورة لنفس المورد"). Since supplier
-- lives on projects (not on this table), the true rule needs either a
-- denormalized supplier_id column here with UNIQUE(supplier_id, pi_no),
-- or an application-layer check joining projects -> import_files. The
-- UNIQUE(import_file_id, pi_no) above is the safe DB-level minimum.

CREATE TABLE invoice_items (
    invoice_item_id  BIGSERIAL PRIMARY KEY,
    pi_id             BIGINT NOT NULL REFERENCES proforma_invoices(pi_id),
    hs_code            VARCHAR(20) NOT NULL REFERENCES hs_codes(hs_code),
    item_code          VARCHAR(64) NOT NULL,
    description        TEXT,
    qty                NUMERIC(18,4) NOT NULL CHECK (qty > 0),
    unit_price         NUMERIC(18,4) NOT NULL CHECK (unit_price > 0),
    amount             NUMERIC(18,4) GENERATED ALWAYS AS (qty * unit_price) STORED
);
CREATE INDEX idx_invoice_items_pi ON invoice_items(pi_id);
CREATE INDEX idx_invoice_items_hscode ON invoice_items(hs_code);

CREATE TABLE packing_list_items (
    pl_item_id        BIGSERIAL PRIMARY KEY,
    import_file_id     BIGINT NOT NULL REFERENCES import_files(import_file_id),
    hs_code             VARCHAR(20) NOT NULL REFERENCES hs_codes(hs_code),
    item_code           VARCHAR(64) NOT NULL,
    qty_pcs             NUMERIC(18,4) NOT NULL,
    qty_pkg             NUMERIC(18,4) NOT NULL,
    package_type        VARCHAR(32), -- Carton / Pallet / Bag
    length_cm           NUMERIC(10,2),
    width_cm            NUMERIC(10,2),
    height_cm           NUMERIC(10,2),
    net_weight_unit     NUMERIC(18,4) NOT NULL,
    gross_weight_unit   NUMERIC(18,4) NOT NULL CHECK (gross_weight_unit >= net_weight_unit),
    total_net_weight    NUMERIC(18,4) GENERATED ALWAYS AS (qty_pcs * net_weight_unit) STORED,
    total_gross_weight  NUMERIC(18,4) GENERATED ALWAYS AS (qty_pcs * gross_weight_unit) STORED,
    cbm_ocean           NUMERIC(18,6), -- qty*L*W*H/1,000,000 - computed in application layer per package
    chargeable_weight_air NUMERIC(18,6) -- qty*L*W*H/6,000
);
CREATE INDEX idx_packing_list_import_file ON packing_list_items(import_file_id);

-- Cross-validation: PI vs ACID vs Invoice, mirrors the 3-column
-- reconciliation block found in the xlsx (Proforma Invoice | ACID
-- Requested | ACID Generated) plus the PI-vs-Final-Invoice variance check
CREATE TABLE document_reconciliation (
    reconciliation_id  BIGSERIAL PRIMARY KEY,
    import_file_id       BIGINT NOT NULL REFERENCES import_files(import_file_id),
    field_name            VARCHAR(100) NOT NULL, -- e.g. 'Foreign Exporter Name'
    pi_value               TEXT,
    acid_requested_value   TEXT,
    acid_generated_value   TEXT,
    final_invoice_value    TEXT,
    variance_flag          BOOLEAN GENERATED ALWAYS AS
                            (pi_value IS DISTINCT FROM final_invoice_value) STORED,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =====================================================================
-- 4. FREIGHT QUOTATIONS / BOOKING / BILL OF LADING (BP-004..BP-006, BP-010/011)
-- =====================================================================

CREATE TABLE freight_quotations (
    quotation_id     BIGSERIAL PRIMARY KEY,
    import_file_id    BIGINT NOT NULL REFERENCES import_files(import_file_id),
    crd_date           DATE NOT NULL,
    port_of_loading_id  BIGINT REFERENCES ports(port_id),
    port_of_discharge_id BIGINT REFERENCES ports(port_id),
    average_form4_days   INT NOT NULL DEFAULT 0,
    average_clearance_days INT NOT NULL DEFAULT 0,
    selected_option_id   BIGINT, -- FK added after quotation_options exists (see ALTER below)
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE quotation_options (
    option_id            BIGSERIAL PRIMARY KEY,
    quotation_id          BIGINT NOT NULL REFERENCES freight_quotations(quotation_id),
    option_rank            SMALLINT NOT NULL, -- 1st / 2nd / 3rd ...
    partner_id             BIGINT NOT NULL REFERENCES service_providers(partner_id), -- shipping provider
    shipping_line_id        BIGINT REFERENCES shipping_lines(shipping_line_id),
    vessel_name             VARCHAR(150),
    sailing_date             DATE,
    arrival_date              DATE,
    lead_time_days            INT GENERATED ALWAYS AS
                               (CASE WHEN arrival_date IS NOT NULL AND sailing_date IS NOT NULL
                                     THEN (arrival_date - sailing_date) ELSE NULL END) STORED,
    expected_line_delay_days   INT NOT NULL DEFAULT 0,
    freight_cost               NUMERIC(18,4),
    free_time_days              INT,
    remarks                     TEXT,
    UNIQUE (quotation_id, option_rank)
);
ALTER TABLE freight_quotations
    ADD CONSTRAINT fk_selected_option FOREIGN KEY (selected_option_id)
    REFERENCES quotation_options(option_id);

CREATE TABLE acid_requests (
    acid_id          BIGSERIAL PRIMARY KEY,
    import_file_id     BIGINT NOT NULL UNIQUE REFERENCES import_files(import_file_id),
    acid_number         VARCHAR(64),
    requested_date       DATE NOT NULL DEFAULT CURRENT_DATE,
    generated_date       DATE,
    generated_by_partner_id BIGINT REFERENCES service_providers(partner_id), -- customs broker
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE bookings (
    booking_id       BIGSERIAL PRIMARY KEY,
    import_file_id     BIGINT NOT NULL UNIQUE REFERENCES import_files(import_file_id),
    acid_id             BIGINT NOT NULL REFERENCES acid_requests(acid_id), -- booking requires ACID
    booking_no           VARCHAR(64),
    cut_off_date          TIMESTAMPTZ NOT NULL,
    cob_date              DATE, -- Closing on Board
    shipping_line_id       BIGINT REFERENCES shipping_lines(shipping_line_id),
    port_of_loading_id      BIGINT REFERENCES ports(port_id),
    port_of_discharge_id    BIGINT REFERENCES ports(port_id),
    -- Business rule: cut_off_date must not precede cargo readiness -
    -- enforce in application layer against import_files.crd_date
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE bills_of_lading (
    bl_id            BIGSERIAL PRIMARY KEY,
    booking_id         BIGINT NOT NULL REFERENCES bookings(booking_id),
    hbl_no              VARCHAR(64),
    mbl_no              VARCHAR(64),
    bl_status            VARCHAR(16) NOT NULL DEFAULT 'draft' CHECK (bl_status IN ('draft','final')),
    shipper              TEXT,
    consignee            TEXT,
    notify_party          TEXT,
    vessel_name           VARCHAR(150),
    port_of_loading_id     BIGINT REFERENCES ports(port_id),
    port_of_discharge_id   BIGINT REFERENCES ports(port_id),
    place_of_delivery      VARCHAR(150),
    release_letter_received BOOLEAN NOT NULL DEFAULT false,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE bl_containers (
    container_id      BIGSERIAL PRIMARY KEY,
    bl_id               BIGINT NOT NULL REFERENCES bills_of_lading(bl_id),
    container_type_id     BIGINT NOT NULL REFERENCES container_types(container_type_id),
    container_no          VARCHAR(32),
    seal_no                VARCHAR(32),
    qty                    NUMERIC(18,4),
    description             TEXT,
    gross_weight             NUMERIC(18,4)
);

-- =====================================================================
-- 5. CUSTOMS, TAXES & FORM 4 (BP-007, BP-008)
-- =====================================================================

-- Rates are copied ("snapshotted") from hs_codes at estimate time so the
-- historical estimate never drifts if the tariff changes later.
CREATE TABLE customs_duty_estimates (
    estimate_id         BIGSERIAL PRIMARY KEY,
    import_file_id        BIGINT NOT NULL REFERENCES import_files(import_file_id),
    hs_code                VARCHAR(20) NOT NULL REFERENCES hs_codes(hs_code),
    currency_id             BIGINT NOT NULL REFERENCES currencies(currency_id),
    exchange_rate            NUMERIC(18,6) NOT NULL,
    amount                    NUMERIC(18,4) NOT NULL,
    customs_duty_pct_snapshot  NUMERIC(7,4) NOT NULL,
    vat_pct_snapshot            NUMERIC(7,4) NOT NULL,
    development_tax_pct_snapshot NUMERIC(7,4) NOT NULL DEFAULT 0,
    other_government_fees        NUMERIC(18,4) NOT NULL DEFAULT 0,
    total_estimated_duties        NUMERIC(18,4) GENERATED ALWAYS AS (
        amount * (customs_duty_pct_snapshot + vat_pct_snapshot + development_tax_pct_snapshot)
        + other_government_fees
    ) STORED,
    prepared_by       BIGINT NOT NULL,
    reviewed_by        BIGINT,
    estimate_date        DATE NOT NULL DEFAULT CURRENT_DATE,
    remarks              TEXT
);

CREATE TABLE form4_requests (
    form4_id           BIGSERIAL PRIMARY KEY,
    import_file_id       BIGINT NOT NULL UNIQUE REFERENCES import_files(import_file_id),
    form4_no               VARCHAR(64),
    requested_date          DATE,
    received_date            DATE,
    -- Validation: requires original BL + stamped invoice + stamped
    -- packing list - tracked via document_tracking rows, not columns here
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =====================================================================
-- 6. PAYMENTS (BP-009, PI Payment / SWIFT, Shipping & Broker Invoices)
-- =====================================================================

CREATE TABLE payment_requests (
    payment_id         BIGSERIAL PRIMARY KEY,
    import_file_id       BIGINT NOT NULL REFERENCES import_files(import_file_id),
    project_id            BIGINT NOT NULL REFERENCES projects(project_id), -- project name mandatory on every request
    pi_id                  BIGINT REFERENCES proforma_invoices(pi_id),
    payment_type           VARCHAR(24) NOT NULL
                           CHECK (payment_type IN ('Advance Payment','Against BL','Final Settlement',
                                                    'Freight Invoice','Broker Invoice')),
    requested_amount        NUMERIC(18,4) NOT NULL CHECK (requested_amount > 0),
    currency_id              BIGINT NOT NULL REFERENCES currencies(currency_id),
    bank_charge_bearer         VARCHAR(8) CHECK (bank_charge_bearer IN ('SHA','BEN','OUR')),
    due_date                    DATE NOT NULL,
    request_date                 DATE NOT NULL DEFAULT CURRENT_DATE,
    status                        VARCHAR(24) NOT NULL DEFAULT 'draft'
                                  CHECK (status IN ('draft','pending_approval','approved','paid','rejected')),
    swift_no                       VARCHAR(64),
    swift_requested_date             DATE,
    swift_generated_date              DATE,
    swift_copy_document_id             BIGINT, -- FK to a documents/attachments table (not modeled here)
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_payment_requests_import_file ON payment_requests(import_file_id);

CREATE TABLE supplier_bank_details (
    id             BIGSERIAL PRIMARY KEY,
    supplier_id      BIGINT NOT NULL REFERENCES suppliers(supplier_id),
    bank_name          VARCHAR(150) NOT NULL,
    swift_code           VARCHAR(16) NOT NULL,
    iban_account_no        VARCHAR(64) NOT NULL,
    beneficiary_name         VARCHAR(255) NOT NULL,
    is_current                BOOLEAN NOT NULL DEFAULT true,
    requires_admin_approval     BOOLEAN NOT NULL DEFAULT true, -- security rule: changes need approval
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =====================================================================
-- 7. FREIGHT COST BREAKDOWN (per container type, per cost item)
-- =====================================================================

CREATE TABLE freight_costs (
    cost_id            BIGSERIAL PRIMARY KEY,
    import_file_id       BIGINT NOT NULL REFERENCES import_files(import_file_id),
    cost_item_id           BIGINT NOT NULL REFERENCES cost_items(cost_item_id),
    container_type_id       BIGINT REFERENCES container_types(container_type_id), -- null for LCL-wide costs
    currency_id              BIGINT NOT NULL REFERENCES currencies(currency_id),
    rate                      NUMERIC(18,4) NOT NULL DEFAULT 0,
    quantity                   NUMERIC(18,4) NOT NULL DEFAULT 1,
    amount                      NUMERIC(18,4) GENERATED ALWAYS AS (rate * quantity) STORED,
    is_estimate                  BOOLEAN NOT NULL DEFAULT true, -- Est.* vs actual invoiced
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_freight_costs_import_file ON freight_costs(import_file_id);

-- Storage / demurrage tracking (extra-day logic seen in the xlsx)
CREATE TABLE storage_charges (
    id                BIGSERIAL PRIMARY KEY,
    import_file_id      BIGINT NOT NULL REFERENCES import_files(import_file_id),
    free_time_days         INT NOT NULL DEFAULT 0,
    applied_days             INT NOT NULL DEFAULT 0,
    extra_days                INT GENERATED ALWAYS AS (GREATEST(applied_days - free_time_days, 0)) STORED,
    daily_rate                 NUMERIC(18,4) NOT NULL DEFAULT 0,
    currency_id                 BIGINT NOT NULL REFERENCES currencies(currency_id),
    total_storage_fees            NUMERIC(18,4) GENERATED ALWAYS AS
                                  (GREATEST(applied_days - free_time_days, 0) * daily_rate) STORED
);

-- =====================================================================
-- 8. DOCUMENT TRACKING (generic - replaces the 4 hardcoded checklists)
-- =====================================================================

CREATE TABLE document_tracking (
    tracking_id        BIGSERIAL PRIMARY KEY,
    import_file_id        BIGINT NOT NULL REFERENCES import_files(import_file_id),
    doc_type_id             BIGINT NOT NULL REFERENCES document_types(doc_type_id),
    checkpoint               VARCHAR(64) NOT NULL, -- e.g. 'Customs pre-shipping review', 'Final Shipment Documents review'
    responsible_partner_id      BIGINT REFERENCES service_providers(partner_id),
    required                     VARCHAR(16) NOT NULL DEFAULT 'Yes' CHECK (required IN ('Yes','No','Conditional')),
    is_blocking                    BOOLEAN NOT NULL DEFAULT true, -- blocks shipment progress if not satisfied
    received                        BOOLEAN NOT NULL DEFAULT false,
    received_date                     DATE,
    verified                           BOOLEAN NOT NULL DEFAULT false,
    verified_by                         BIGINT,
    verification_date                    DATE,
    approval_status                       VARCHAR(24) NOT NULL DEFAULT 'Pending'
                                          CHECK (approval_status IN
                                            ('Pending','Received','Under Review','Approved','Rejected','Not Required')),
    courier_no                             VARCHAR(64),
    courier_date                             DATE,
    remarks                                   TEXT,
    UNIQUE (import_file_id, doc_type_id, checkpoint)
);
CREATE INDEX idx_document_tracking_import_file ON document_tracking(import_file_id);

-- =====================================================================
-- 9. WAREHOUSE RECEIVING (Closing)
-- =====================================================================

CREATE TABLE warehouse_receiving (
    receiving_id       BIGSERIAL PRIMARY KEY,
    import_file_id        BIGINT NOT NULL UNIQUE REFERENCES import_files(import_file_id),
    customs_release_no       VARCHAR(64) NOT NULL, -- must match before opening cargo
    driver_name                VARCHAR(150),
    driver_arrival_datetime      TIMESTAMPTZ,
    received_qty_matches           BOOLEAN,
    discrepancy_type                 VARCHAR(16) CHECK (discrepancy_type IN ('none','shortage','damage')),
    discrepancy_notes                  TEXT,
    received_at                          TIMESTAMPTZ,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =====================================================================
-- 10. VIEWS - convenience aggregates
-- =====================================================================

CREATE VIEW v_hs_code_summary AS
    SELECT ii.pi_id, ii.hs_code, SUM(ii.qty) AS total_qty, SUM(ii.amount) AS total_amount
    FROM invoice_items ii
    GROUP BY ii.pi_id, ii.hs_code;

CREATE VIEW v_packing_list_summary AS
    SELECT pl.import_file_id, pl.hs_code,
           SUM(pl.qty_pcs) AS total_qty_pcs, SUM(pl.qty_pkg) AS total_qty_pkg,
           SUM(pl.total_net_weight) AS total_net_weight,
           SUM(pl.total_gross_weight) AS total_gross_weight
    FROM packing_list_items pl
    GROUP BY pl.import_file_id, pl.hs_code;
