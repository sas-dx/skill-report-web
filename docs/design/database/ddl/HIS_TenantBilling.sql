-- ============================================
-- テーブル: HIS_TenantBilling
-- 論理名: テナント課金履歴
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS HIS_TenantBilling;

CREATE TABLE HIS_TenantBilling (
    id VARCHAR(50) COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) COMMENT '課金対象のテナントID（MST_Tenantへの参照）',
    billing_period_start DATE COMMENT '課金期間の開始日',
    billing_period_end DATE COMMENT '課金期間の終了日',
    billing_type ENUM COMMENT '課金の種類（MONTHLY:月額、USAGE:従量、SETUP:初期費用、ADDITIONAL:追加費用）',
    plan_id VARCHAR(50) COMMENT '適用されたプランのID',
    plan_name VARCHAR(200) COMMENT '適用されたプランの名称',
    base_amount DECIMAL(12,2) DEFAULT 0.0 COMMENT '基本料金（税抜）',
    usage_amount DECIMAL(12,2) DEFAULT 0.0 COMMENT '使用量に基づく従量料金（税抜）',
    additional_amount DECIMAL(12,2) DEFAULT 0.0 COMMENT '追加サービス等の料金（税抜）',
    discount_amount DECIMAL(12,2) DEFAULT 0.0 COMMENT '適用された割引金額（税抜）',
    subtotal_amount DECIMAL(12,2) COMMENT '税抜小計金額',
    tax_rate DECIMAL(5,3) COMMENT '適用された税率（例：0.100 = 10%）',
    tax_amount DECIMAL(12,2) COMMENT '消費税額',
    total_amount DECIMAL(12,2) COMMENT '税込合計金額',
    currency_code VARCHAR(3) DEFAULT 'JPY' COMMENT '通貨コード（ISO 4217準拠、例：JPY、USD）',
    usage_details TEXT COMMENT '使用量の詳細情報（JSON形式）',
    billing_status ENUM DEFAULT 'CALCULATED' COMMENT '課金の状態（CALCULATED:計算済み、INVOICED:請求済み、PAID:支払済み、CANCELLED:キャンセル）',
    invoice_number VARCHAR(50) COMMENT '発行された請求書の番号',
    invoice_date DATE COMMENT '請求書の発行日',
    due_date DATE COMMENT '支払期限日',
    paid_date DATE COMMENT '実際の支払日',
    payment_method ENUM COMMENT '支払方法（CREDIT_CARD:クレジットカード、BANK_TRANSFER:銀行振込、AUTO_DEBIT:自動引落）',
    notes TEXT COMMENT '課金に関する備考・特記事項',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_tenant_billing_tenant_period ON HIS_TenantBilling (tenant_id, billing_period_start, billing_period_end);
CREATE INDEX idx_tenant_billing_status ON HIS_TenantBilling (billing_status);
CREATE UNIQUE INDEX idx_tenant_billing_invoice ON HIS_TenantBilling (invoice_number);
CREATE INDEX idx_tenant_billing_dates ON HIS_TenantBilling (invoice_date, due_date, paid_date);
CREATE INDEX idx_tenant_billing_type ON HIS_TenantBilling (billing_type);
CREATE INDEX idx_tenant_billing_amount ON HIS_TenantBilling (total_amount);

-- 外部キー制約
ALTER TABLE HIS_TenantBilling ADD CONSTRAINT fk_tenant_billing_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;

-- その他の制約
ALTER TABLE HIS_TenantBilling ADD CONSTRAINT uk_tenant_billing_invoice UNIQUE ();
ALTER TABLE HIS_TenantBilling ADD CONSTRAINT chk_tenant_billing_type CHECK (billing_type IN ('MONTHLY', 'USAGE', 'SETUP', 'ADDITIONAL'));
ALTER TABLE HIS_TenantBilling ADD CONSTRAINT chk_tenant_billing_status CHECK (billing_status IN ('CALCULATED', 'INVOICED', 'PAID', 'CANCELLED'));
ALTER TABLE HIS_TenantBilling ADD CONSTRAINT chk_tenant_billing_payment_method CHECK (payment_method IS NULL OR payment_method IN ('CREDIT_CARD', 'BANK_TRANSFER', 'AUTO_DEBIT'));
ALTER TABLE HIS_TenantBilling ADD CONSTRAINT chk_tenant_billing_period CHECK (billing_period_end >= billing_period_start);
ALTER TABLE HIS_TenantBilling ADD CONSTRAINT chk_tenant_billing_amounts_positive CHECK (base_amount >= 0 AND usage_amount >= 0 AND additional_amount >= 0 AND discount_amount >= 0 AND tax_amount >= 0 AND total_amount >= 0);
ALTER TABLE HIS_TenantBilling ADD CONSTRAINT chk_tenant_billing_tax_rate CHECK (tax_rate >= 0 AND tax_rate <= 1);
