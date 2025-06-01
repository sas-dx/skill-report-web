-- HIS_TenantBilling (テナント課金履歴) DDL
-- 生成日時: 2025-06-01 20:40:26

CREATE TABLE HIS_TenantBilling (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    id VARCHAR(50),
    tenant_id VARCHAR(50),
    billing_period_start DATE,
    billing_period_end DATE,
    billing_type ENUM,
    plan_id VARCHAR(50),
    plan_name VARCHAR(200),
    base_amount DECIMAL(12,2) DEFAULT 0.0,
    usage_amount DECIMAL(12,2) DEFAULT 0.0,
    additional_amount DECIMAL(12,2) DEFAULT 0.0,
    discount_amount DECIMAL(12,2) DEFAULT 0.0,
    subtotal_amount DECIMAL(12,2),
    tax_rate DECIMAL(5,3),
    tax_amount DECIMAL(12,2),
    total_amount DECIMAL(12,2),
    currency_code VARCHAR(3) DEFAULT 'JPY',
    usage_details TEXT,
    billing_status ENUM DEFAULT 'CALCULATED',
    invoice_number VARCHAR(50),
    invoice_date DATE,
    due_date DATE,
    paid_date DATE,
    payment_method ENUM,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE INDEX idx_tenant_billing_tenant_period ON HIS_TenantBilling (tenant_id, billing_period_start, billing_period_end);
CREATE INDEX idx_tenant_billing_status ON HIS_TenantBilling (billing_status);
CREATE UNIQUE INDEX idx_tenant_billing_invoice ON HIS_TenantBilling (invoice_number);
CREATE INDEX idx_tenant_billing_dates ON HIS_TenantBilling (invoice_date, due_date, paid_date);
CREATE INDEX idx_tenant_billing_type ON HIS_TenantBilling (billing_type);
CREATE INDEX idx_tenant_billing_amount ON HIS_TenantBilling (total_amount);

-- 外部キー制約
ALTER TABLE HIS_TenantBilling ADD CONSTRAINT fk_tenant_billing_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;
