-- ============================================
-- テーブル: HIS_TenantBilling
-- 論理名: テナント課金履歴
-- 説明: HIS_TenantBilling（テナント課金履歴）は、マルチテナントシステムにおける各テナントの課金情報を履歴として管理するテーブルです。

主な目的：
- テナント別課金履歴の管理
- 使用量ベース課金の計算履歴
- 請求書発行のための基礎データ管理
- 課金監査のための証跡管理
- 収益分析のためのデータ蓄積

このテーブルは、マルチテナント管理機能において課金・請求業務を支える重要な履歴データです。

-- 作成日: 2025-06-21 17:20:34
-- ============================================

DROP TABLE IF EXISTS HIS_TenantBilling;

CREATE TABLE HIS_TenantBilling (
    id VARCHAR,
    tenant_id VARCHAR,
    billing_period_start DATE,
    billing_period_end DATE,
    billing_type ENUM,
    plan_id VARCHAR,
    plan_name VARCHAR,
    base_amount DECIMAL DEFAULT 0.0,
    usage_amount DECIMAL DEFAULT 0.0,
    additional_amount DECIMAL DEFAULT 0.0,
    discount_amount DECIMAL DEFAULT 0.0,
    subtotal_amount DECIMAL,
    tax_rate DECIMAL,
    tax_amount DECIMAL,
    total_amount DECIMAL,
    currency_code VARCHAR DEFAULT 'JPY',
    usage_details TEXT,
    billing_status ENUM DEFAULT 'CALCULATED',
    invoice_number VARCHAR,
    invoice_date DATE,
    due_date DATE,
    paid_date DATE,
    payment_method ENUM,
    notes TEXT,
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_tenant_billing_tenant_period ON HIS_TenantBilling (tenant_id, billing_period_start, billing_period_end);
CREATE INDEX idx_tenant_billing_status ON HIS_TenantBilling (billing_status);
CREATE UNIQUE INDEX idx_tenant_billing_invoice ON HIS_TenantBilling (invoice_number);
CREATE INDEX idx_tenant_billing_dates ON HIS_TenantBilling (invoice_date, due_date, paid_date);
CREATE INDEX idx_tenant_billing_type ON HIS_TenantBilling (billing_type);
CREATE INDEX idx_tenant_billing_amount ON HIS_TenantBilling (total_amount);
