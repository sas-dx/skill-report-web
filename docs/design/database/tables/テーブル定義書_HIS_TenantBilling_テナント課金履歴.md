# テーブル定義書_HIS_TenantBilling_テナント課金履歴

## 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | HIS_TenantBilling |
| 論理名 | テナント課金履歴 |
| 用途 | テナントの課金履歴を記録・管理 |
| カテゴリ | 履歴系 |
| 作成日 | 2025-05-31 |
| 最終更新日 | 2025-05-31 |

## 概要

テナントごとの課金履歴を記録し、請求書発行、支払い管理、収益分析等に活用するテーブル。使用量ベースの課金計算結果と実際の請求・支払い状況を管理する。

## カラム定義

| No | カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト値 | 主キー | 外部キー | 説明 |
|----|----------|--------|----------|------|------|-------------|--------|----------|------|
| 1 | billing_id | 課金ID | BIGINT | - | NOT NULL | AUTO_INCREMENT | ○ | - | 課金履歴の一意識別子 |
| 2 | tenant_id | テナントID | VARCHAR | 50 | NOT NULL | - | - | MST_Tenant.tenant_id | 対象テナントID |
| 3 | billing_period_start | 課金期間開始日 | DATE | - | NOT NULL | - | - | - | 課金対象期間の開始日 |
| 4 | billing_period_end | 課金期間終了日 | DATE | - | NOT NULL | - | - | - | 課金対象期間の終了日 |
| 5 | billing_type | 課金タイプ | VARCHAR | 20 | NOT NULL | - | - | - | 課金種別 |
| 6 | plan_id | プランID | VARCHAR | 50 | NULL | NULL | - | - | 適用された料金プランID |
| 7 | plan_name | プラン名 | VARCHAR | 100 | NULL | NULL | - | - | 適用された料金プラン名 |
| 8 | base_amount | 基本料金 | DECIMAL | 10,2 | NOT NULL | 0.00 | - | - | 基本料金（固定費） |
| 9 | usage_amount | 使用量料金 | DECIMAL | 10,2 | NOT NULL | 0.00 | - | - | 使用量ベースの料金 |
| 10 | additional_amount | 追加料金 | DECIMAL | 10,2 | NOT NULL | 0.00 | - | - | 追加サービス料金 |
| 11 | discount_amount | 割引額 | DECIMAL | 10,2 | NOT NULL | 0.00 | - | - | 適用された割引額 |
| 12 | tax_amount | 税額 | DECIMAL | 10,2 | NOT NULL | 0.00 | - | - | 消費税等の税額 |
| 13 | total_amount | 合計金額 | DECIMAL | 10,2 | NOT NULL | 0.00 | - | - | 請求合計金額 |
| 14 | currency | 通貨 | VARCHAR | 3 | NOT NULL | 'JPY' | - | - | 通貨コード |
| 15 | tax_rate | 税率 | DECIMAL | 5,2 | NOT NULL | 0.00 | - | - | 適用税率（%） |
| 16 | active_users | アクティブユーザー数 | INT | - | NULL | 0 | - | - | 課金対象期間のアクティブユーザー数 |
| 17 | total_users | 総ユーザー数 | INT | - | NULL | 0 | - | - | 課金対象期間の総ユーザー数 |
| 18 | storage_used_gb | ストレージ使用量(GB) | DECIMAL | 10,2 | NULL | 0.00 | - | - | ストレージ使用量（ギガバイト） |
| 19 | api_calls | API呼び出し数 | BIGINT | - | NULL | 0 | - | - | API呼び出し総数 |
| 20 | data_transfer_gb | データ転送量(GB) | DECIMAL | 10,2 | NULL | 0.00 | - | - | データ転送量（ギガバイト） |
| 21 | backup_size_gb | バックアップサイズ(GB) | DECIMAL | 10,2 | NULL | 0.00 | - | - | バックアップデータサイズ |
| 22 | usage_details_json | 使用量詳細 | JSON | - | NULL | NULL | - | - | 詳細な使用量データ（JSON形式） |
| 23 | pricing_details_json | 料金詳細 | JSON | - | NULL | NULL | - | - | 料金計算詳細（JSON形式） |
| 24 | invoice_number | 請求書番号 | VARCHAR | 50 | NULL | NULL | - | - | 発行された請求書番号 |
| 25 | invoice_date | 請求書発行日 | DATE | - | NULL | NULL | - | - | 請求書発行日 |
| 26 | due_date | 支払期限 | DATE | - | NULL | NULL | - | - | 支払期限日 |
| 27 | payment_status | 支払いステータス | VARCHAR | 20 | NOT NULL | 'PENDING' | - | - | 支払い状況 |
| 28 | payment_date | 支払日 | DATE | - | NULL | NULL | - | - | 実際の支払日 |
| 29 | payment_method | 支払方法 | VARCHAR | 30 | NULL | NULL | - | - | 支払方法 |
| 30 | payment_reference | 支払参照番号 | VARCHAR | 100 | NULL | NULL | - | - | 支払い時の参照番号 |
| 31 | billing_status | 課金ステータス | VARCHAR | 20 | NOT NULL | 'CALCULATED' | - | - | 課金処理状況 |
| 32 | calculation_date | 計算日 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP | - | - | 課金計算実行日時 |
| 33 | approval_status | 承認ステータス | VARCHAR | 20 | NOT NULL | 'PENDING' | - | - | 課金承認状況 |
| 34 | approved_by | 承認者 | VARCHAR | 50 | NULL | NULL | - | - | 課金承認者 |
| 35 | approved_at | 承認日時 | TIMESTAMP | - | NULL | NULL | - | - | 課金承認日時 |
| 36 | adjustment_amount | 調整額 | DECIMAL | 10,2 | NOT NULL | 0.00 | - | - | 手動調整額 |
| 37 | adjustment_reason | 調整理由 | TEXT | - | NULL | NULL | - | - | 調整理由 |
| 38 | credit_amount | クレジット額 | DECIMAL | 10,2 | NOT NULL | 0.00 | - | - | 適用されたクレジット額 |
| 39 | refund_amount | 返金額 | DECIMAL | 10,2 | NOT NULL | 0.00 | - | - | 返金額 |
| 40 | external_billing_id | 外部課金ID | VARCHAR | 100 | NULL | NULL | - | - | 外部課金システムでのID |
| 41 | billing_cycle | 課金サイクル | VARCHAR | 20 | NOT NULL | 'MONTHLY' | - | - | 課金サイクル |
| 42 | proration_factor | 日割り係数 | DECIMAL | 5,4 | NOT NULL | 1.0000 | - | - | 日割り計算係数 |
| 43 | contract_start_date | 契約開始日 | DATE | - | NULL | NULL | - | - | 契約開始日 |
| 44 | contract_end_date | 契約終了日 | DATE | - | NULL | NULL | - | - | 契約終了日 |
| 45 | notes | 備考 | TEXT | - | NULL | NULL | - | - | 課金に関する備考 |
| 46 | created_at | 作成日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP | - | - | レコード作成日時 |
| 47 | updated_at | 更新日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | レコード更新日時 |
| 48 | created_by | 作成者 | VARCHAR | 50 | NOT NULL | 'SYSTEM' | - | - | レコード作成者 |
| 49 | updated_by | 更新者 | VARCHAR | 50 | NOT NULL | 'SYSTEM' | - | - | レコード更新者 |

## 制約

### 主キー制約
- PRIMARY KEY (billing_id)

### 外部キー制約
- FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id)

### ユニーク制約
- UNIQUE KEY uk_tenant_period (tenant_id, billing_period_start, billing_period_end, billing_type)

### チェック制約
- CHECK (billing_type IN ('MONTHLY', 'ANNUAL', 'USAGE_BASED', 'ONE_TIME', 'ADJUSTMENT'))
- CHECK (payment_status IN ('PENDING', 'PAID', 'OVERDUE', 'CANCELLED', 'REFUNDED', 'PARTIAL'))
- CHECK (billing_status IN ('CALCULATED', 'INVOICED', 'SENT', 'COMPLETED', 'CANCELLED'))
- CHECK (approval_status IN ('PENDING', 'APPROVED', 'REJECTED', 'REVIEW_REQUIRED'))
- CHECK (billing_cycle IN ('MONTHLY', 'QUARTERLY', 'ANNUAL', 'USAGE_BASED'))
- CHECK (billing_period_start <= billing_period_end)
- CHECK (base_amount >= 0)
- CHECK (usage_amount >= 0)
- CHECK (additional_amount >= 0)
- CHECK (discount_amount >= 0)
- CHECK (tax_amount >= 0)
- CHECK (total_amount >= 0)
- CHECK (tax_rate >= 0 AND tax_rate <= 100)
- CHECK (proration_factor > 0 AND proration_factor <= 1)

## インデックス

| インデックス名 | 種別 | 対象カラム | 説明 |
|---------------|------|------------|------|
| idx_tenant_period | BTREE | tenant_id, billing_period_start | テナント・期間での検索用 |
| idx_billing_period | BTREE | billing_period_start, billing_period_end | 課金期間での検索用 |
| idx_payment_status | BTREE | payment_status | 支払いステータスでの検索用 |
| idx_billing_status | BTREE | billing_status | 課金ステータスでの検索用 |
| idx_invoice_number | BTREE | invoice_number | 請求書番号での検索用 |
| idx_due_date | BTREE | due_date | 支払期限での検索用 |
| idx_calculation_date | BTREE | calculation_date | 計算日での検索用 |
| idx_approval_status | BTREE | approval_status | 承認ステータスでの検索用 |
| idx_created_at | BTREE | created_at | 作成日時での検索用 |

## DDL

```sql
CREATE TABLE HIS_TenantBilling (
    billing_id BIGINT NOT NULL AUTO_INCREMENT COMMENT '課金ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    billing_period_start DATE NOT NULL COMMENT '課金期間開始日',
    billing_period_end DATE NOT NULL COMMENT '課金期間終了日',
    billing_type VARCHAR(20) NOT NULL COMMENT '課金タイプ',
    plan_id VARCHAR(50) COMMENT 'プランID',
    plan_name VARCHAR(100) COMMENT 'プラン名',
    base_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT '基本料金',
    usage_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT '使用量料金',
    additional_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT '追加料金',
    discount_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT '割引額',
    tax_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT '税額',
    total_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT '合計金額',
    currency VARCHAR(3) NOT NULL DEFAULT 'JPY' COMMENT '通貨',
    tax_rate DECIMAL(5,2) NOT NULL DEFAULT 0.00 COMMENT '税率',
    active_users INT DEFAULT 0 COMMENT 'アクティブユーザー数',
    total_users INT DEFAULT 0 COMMENT '総ユーザー数',
    storage_used_gb DECIMAL(10,2) DEFAULT 0.00 COMMENT 'ストレージ使用量(GB)',
    api_calls BIGINT DEFAULT 0 COMMENT 'API呼び出し数',
    data_transfer_gb DECIMAL(10,2) DEFAULT 0.00 COMMENT 'データ転送量(GB)',
    backup_size_gb DECIMAL(10,2) DEFAULT 0.00 COMMENT 'バックアップサイズ(GB)',
    usage_details_json JSON COMMENT '使用量詳細',
    pricing_details_json JSON COMMENT '料金詳細',
    invoice_number VARCHAR(50) COMMENT '請求書番号',
    invoice_date DATE COMMENT '請求書発行日',
    due_date DATE COMMENT '支払期限',
    payment_status VARCHAR(20) NOT NULL DEFAULT 'PENDING' COMMENT '支払いステータス',
    payment_date DATE COMMENT '支払日',
    payment_method VARCHAR(30) COMMENT '支払方法',
    payment_reference VARCHAR(100) COMMENT '支払参照番号',
    billing_status VARCHAR(20) NOT NULL DEFAULT 'CALCULATED' COMMENT '課金ステータス',
    calculation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '計算日',
    approval_status VARCHAR(20) NOT NULL DEFAULT 'PENDING' COMMENT '承認ステータス',
    approved_by VARCHAR(50) COMMENT '承認者',
    approved_at TIMESTAMP COMMENT '承認日時',
    adjustment_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT '調整額',
    adjustment_reason TEXT COMMENT '調整理由',
    credit_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT 'クレジット額',
    refund_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT '返金額',
    external_billing_id VARCHAR(100) COMMENT '外部課金ID',
    billing_cycle VARCHAR(20) NOT NULL DEFAULT 'MONTHLY' COMMENT '課金サイクル',
    proration_factor DECIMAL(5,4) NOT NULL DEFAULT 1.0000 COMMENT '日割り係数',
    contract_start_date DATE COMMENT '契約開始日',
    contract_end_date DATE COMMENT '契約終了日',
    notes TEXT COMMENT '備考',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL DEFAULT 'SYSTEM' COMMENT '作成者',
    updated_by VARCHAR(50) NOT NULL DEFAULT 'SYSTEM' COMMENT '更新者',
    
    PRIMARY KEY (billing_id),
    UNIQUE KEY uk_tenant_period (tenant_id, billing_period_start, billing_period_end, billing_type),
    
    CONSTRAINT fk_tenant_billing_tenant 
        FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id),
    
    CONSTRAINT chk_billing_type 
        CHECK (billing_type IN ('MONTHLY', 'ANNUAL', 'USAGE_BASED', 'ONE_TIME', 'ADJUSTMENT')),
    CONSTRAINT chk_payment_status 
        CHECK (payment_status IN ('PENDING', 'PAID', 'OVERDUE', 'CANCELLED', 'REFUNDED', 'PARTIAL')),
    CONSTRAINT chk_billing_status 
        CHECK (billing_status IN ('CALCULATED', 'INVOICED', 'SENT', 'COMPLETED', 'CANCELLED')),
    CONSTRAINT chk_approval_status 
        CHECK (approval_status IN ('PENDING', 'APPROVED', 'REJECTED', 'REVIEW_REQUIRED')),
    CONSTRAINT chk_billing_cycle 
        CHECK (billing_cycle IN ('MONTHLY', 'QUARTERLY', 'ANNUAL', 'USAGE_BASED')),
    CONSTRAINT chk_billing_period 
        CHECK (billing_period_start <= billing_period_end),
    CONSTRAINT chk_base_amount 
        CHECK (base_amount >= 0),
    CONSTRAINT chk_usage_amount 
        CHECK (usage_amount >= 0),
    CONSTRAINT chk_additional_amount 
        CHECK (additional_amount >= 0),
    CONSTRAINT chk_discount_amount 
        CHECK (discount_amount >= 0),
    CONSTRAINT chk_tax_amount 
        CHECK (tax_amount >= 0),
    CONSTRAINT chk_total_amount 
        CHECK (total_amount >= 0),
    CONSTRAINT chk_tax_rate 
        CHECK (tax_rate >= 0 AND tax_rate <= 100),
    CONSTRAINT chk_proration_factor 
        CHECK (proration_factor > 0 AND proration_factor <= 1)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='テナント課金履歴管理テーブル';

-- インデックス作成
CREATE INDEX idx_tenant_period ON HIS_TenantBilling(tenant_id, billing_period_start);
CREATE INDEX idx_billing_period ON HIS_TenantBilling(billing_period_start, billing_period_end);
CREATE INDEX idx_payment_status ON HIS_TenantBilling(payment_status);
CREATE INDEX idx_billing_status ON HIS_TenantBilling(billing_status);
CREATE INDEX idx_invoice_number ON HIS_TenantBilling(invoice_number);
CREATE INDEX idx_due_date ON HIS_TenantBilling(due_date);
CREATE INDEX idx_calculation_date ON HIS_TenantBilling(calculation_date);
CREATE INDEX idx_approval_status ON HIS_TenantBilling(approval_status);
CREATE INDEX idx_created_at ON HIS_TenantBilling(created_at);
```

## 関連テーブル

| テーブル名 | 関係 | 説明 |
|------------|------|------|
| MST_Tenant | 親 | テナント基本情報 |
| SYS_TenantUsage | 関連 | テナント使用量データ |
| MST_TenantSettings | 関連 | テナント設定情報 |
| SYS_SystemLog | 関連 | システムログ |
| SYS_AuditLog | 関連 | 監査ログ |

## 利用API

| API ID | API名 | 説明 |
|--------|-------|------|
| API-025 | テナント管理API | 課金履歴取得 |
| API-026 | テナント設定API | 課金設定管理 |

## 利用バッチ

| バッチ ID | バッチ名 | 説明 |
|-----------|----------|------|
| BATCH-018-02 | テナント課金計算バッチ | 課金額計算と履歴作成 |
| BATCH-018-01 | テナント使用量集計バッチ | 使用量データ集計 |
| BATCH-302 | テナント課金計算バッチ | 月次課金計算 |

## 運用考慮事項

### セキュリティ
- 課金データの機密性保護
- アクセス権限の厳格な制御
- 監査ログの記録
- データ改ざん防止

### 精度
- 課金計算の正確性確保
- 四捨五入ルールの統一
- 通貨換算の精度管理
- 税計算の正確性

### 監査
- 課金計算過程の透明性
- 変更履歴の完全な記録
- 承認プロセスの実装
- 外部監査への対応

### パフォーマンス
- 大量データの効率的な処理
- 集計処理の最適化
- インデックスの適切な設計
- アーカイブ戦略

## データサンプル

```sql
-- 月次課金履歴例
INSERT INTO HIS_TenantBilling (
    tenant_id, billing_period_start, billing_period_end,
    billing_type, plan_name, base_amount, usage_amount,
    tax_amount, total_amount, active_users, total_users,
    storage_used_gb, api_calls, billing_status,
    created_by, updated_by
) VALUES (
    'tenant001', '2025-05-01', '2025-05-31',
    'MONTHLY', 'スタンダードプラン', 10000.00, 5000.00,
    1500.00, 16500.00, 45, 100,
    50.5, 150000, 'CALCULATED',
    'SYSTEM', 'SYSTEM'
);

-- 使用量ベース課金例
INSERT INTO HIS_TenantBilling (
    tenant_id, billing_period_start, billing_period_end,
    billing_type, usage_amount, tax_amount, total_amount,
    api_calls, data_transfer_gb, billing_status,
    created_by, updated_by
) VALUES (
    'tenant002', '2025-05-01', '2025-05-31',
    'USAGE_BASED', 25000.00, 2500.00, 27500.00,
    500000, 100.0, 'CALCULATED',
    'SYSTEM', 'SYSTEM'
);

-- 調整課金例
INSERT INTO HIS_TenantBilling (
    tenant_id, billing_period_start, billing_period_end,
    billing_type, adjustment_amount, adjustment_reason,
    total_amount, billing_status, created_by, updated_by
) VALUES (
    'tenant001', '2025-05-15', '2025-05-15',
    'ADJUSTMENT', -5000.00, 'システム障害による返金',
    -5000.00, 'APPROVED', 'admin', 'admin'
);
```

## 変更履歴

| 版数 | 変更日 | 変更者 | 変更内容 |
|------|--------|--------|----------|
| 1.0 | 2025-05-31 | システム管理者 | 初版作成 |
