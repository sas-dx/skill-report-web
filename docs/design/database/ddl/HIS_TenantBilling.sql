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

-- 作成日: 2025-06-24 23:05:57
-- ============================================

DROP TABLE IF EXISTS HIS_TenantBilling;

CREATE TABLE HIS_TenantBilling (
    id VARCHAR(50) COMMENT 'ID',
    tenant_id VARCHAR(50) COMMENT 'テナントID',
    plan_name VARCHAR(200) COMMENT 'プラン名',
    additional_amount DECIMAL(12,2) DEFAULT 0.0 COMMENT '追加料金',
    base_amount DECIMAL(12,2) DEFAULT 0.0 COMMENT '基本料金',
    billing_period_end DATE COMMENT '課金期間終了日',
    billing_period_start DATE COMMENT '課金期間開始日',
    billing_status ENUM('CALCULATED', 'INVOICED', 'PAID', 'CANCELLED') DEFAULT 'CALCULATED' COMMENT '課金状態',
    billing_type ENUM('MONTHLY', 'USAGE', 'SETUP', 'ADDITIONAL') COMMENT '課金タイプ',
    currency_code VARCHAR(3) DEFAULT 'JPY' COMMENT '通貨コード',
    discount_amount DECIMAL(12,2) DEFAULT 0.0 COMMENT '割引金額',
    due_date DATE COMMENT '支払期限',
    invoice_date DATE COMMENT '請求日',
    invoice_number VARCHAR(50) COMMENT '請求書番号',
    notes TEXT COMMENT '備考',
    paid_date DATE COMMENT '支払日',
    payment_method ENUM('CREDIT_CARD', 'BANK_TRANSFER', 'AUTO_DEBIT') COMMENT '支払方法',
    plan_id VARCHAR(50) COMMENT 'プランID',
    subtotal_amount DECIMAL(12,2) COMMENT '小計金額',
    tax_amount DECIMAL(12,2) COMMENT '税額',
    tax_rate DECIMAL(5,3) COMMENT '税率',
    tenantbilling_id INT AUTO_INCREMENT NOT NULL COMMENT 'HIS_TenantBillingの主キー',
    total_amount DECIMAL(12,2) COMMENT '合計金額',
    usage_amount DECIMAL(12,2) DEFAULT 0.0 COMMENT '従量料金',
    usage_details TEXT COMMENT '使用量詳細',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_tenant_billing_tenant_period ON HIS_TenantBilling (tenant_id, billing_period_start, billing_period_end);
CREATE INDEX idx_tenant_billing_status ON HIS_TenantBilling (billing_status);
CREATE UNIQUE INDEX idx_tenant_billing_invoice ON HIS_TenantBilling (invoice_number);
CREATE INDEX idx_tenant_billing_dates ON HIS_TenantBilling (invoice_date, due_date, paid_date);
CREATE INDEX idx_tenant_billing_type ON HIS_TenantBilling (billing_type);
CREATE INDEX idx_tenant_billing_amount ON HIS_TenantBilling (total_amount);
CREATE INDEX idx_his_tenantbilling_tenant_id ON HIS_TenantBilling (tenant_id);

-- 外部キー制約
ALTER TABLE HIS_TenantBilling ADD CONSTRAINT fk_tenant_billing_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;

-- その他の制約
-- 制約DDL生成エラー: uk_tenant_billing_invoice
ALTER TABLE HIS_TenantBilling ADD CONSTRAINT chk_tenant_billing_type CHECK (billing_type IN ('MONTHLY', 'USAGE', 'SETUP', 'ADDITIONAL'));
ALTER TABLE HIS_TenantBilling ADD CONSTRAINT chk_tenant_billing_status CHECK (billing_status IN ('CALCULATED', 'INVOICED', 'PAID', 'CANCELLED'));
ALTER TABLE HIS_TenantBilling ADD CONSTRAINT chk_tenant_billing_payment_method CHECK (payment_method IS NULL OR payment_method IN ('CREDIT_CARD', 'BANK_TRANSFER', 'AUTO_DEBIT'));
ALTER TABLE HIS_TenantBilling ADD CONSTRAINT chk_tenant_billing_period CHECK (billing_period_end >= billing_period_start);
ALTER TABLE HIS_TenantBilling ADD CONSTRAINT chk_tenant_billing_amounts_positive CHECK (base_amount >= 0 AND usage_amount >= 0 AND additional_amount >= 0 AND discount_amount >= 0 AND tax_amount >= 0 AND total_amount >= 0);
ALTER TABLE HIS_TenantBilling ADD CONSTRAINT chk_tenant_billing_tax_rate CHECK (tax_rate >= 0 AND tax_rate <= 1);
