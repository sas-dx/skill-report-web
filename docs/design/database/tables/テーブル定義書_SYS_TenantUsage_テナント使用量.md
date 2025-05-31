# テーブル定義書_SYS_TenantUsage_テナント使用量

## 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | SYS_TenantUsage |
| 論理名 | テナント使用量 |
| 用途 | テナントごとのシステム使用量を記録・管理 |
| カテゴリ | システム系 |
| 作成日 | 2025-05-31 |
| 最終更新日 | 2025-05-31 |

## 概要

テナントごとのシステム使用量（ユーザー数、ストレージ使用量、API呼び出し数等）を記録し、課金計算やリソース管理の基礎データとして活用するテーブル。

## カラム定義

| No | カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト値 | 主キー | 外部キー | 説明 |
|----|----------|--------|----------|------|------|-------------|--------|----------|------|
| 1 | usage_id | 使用量ID | BIGINT | - | NOT NULL | AUTO_INCREMENT | ○ | - | 使用量レコードの一意識別子 |
| 2 | tenant_id | テナントID | VARCHAR | 50 | NOT NULL | - | - | MST_Tenant.tenant_id | 対象テナントID |
| 3 | measurement_date | 計測日 | DATE | - | NOT NULL | - | - | - | 使用量計測日 |
| 4 | measurement_type | 計測タイプ | VARCHAR | 20 | NOT NULL | - | - | - | 計測種別（DAILY/MONTHLY/YEARLY） |
| 5 | active_users | アクティブユーザー数 | INT | - | NULL | 0 | - | - | 当日のアクティブユーザー数 |
| 6 | total_users | 総ユーザー数 | INT | - | NULL | 0 | - | - | 登録済み総ユーザー数 |
| 7 | storage_used_mb | ストレージ使用量(MB) | BIGINT | - | NULL | 0 | - | - | ストレージ使用量（メガバイト） |
| 8 | api_calls | API呼び出し数 | BIGINT | - | NULL | 0 | - | - | API呼び出し総数 |
| 9 | login_count | ログイン回数 | INT | - | NULL | 0 | - | - | ログイン回数 |
| 10 | skill_records | スキル記録数 | INT | - | NULL | 0 | - | - | スキル評価記録数 |
| 11 | report_generated | 生成レポート数 | INT | - | NULL | 0 | - | - | 生成されたレポート数 |
| 12 | backup_size_mb | バックアップサイズ(MB) | BIGINT | - | NULL | 0 | - | - | バックアップデータサイズ |
| 13 | cpu_usage_percent | CPU使用率 | DECIMAL | 5,2 | NULL | 0.00 | - | - | 平均CPU使用率（%） |
| 14 | memory_usage_mb | メモリ使用量(MB) | BIGINT | - | NULL | 0 | - | - | 平均メモリ使用量 |
| 15 | network_traffic_mb | ネットワーク通信量(MB) | BIGINT | - | NULL | 0 | - | - | ネットワーク通信量 |
| 16 | error_count | エラー発生数 | INT | - | NULL | 0 | - | - | エラー発生回数 |
| 17 | response_time_avg | 平均応答時間(ms) | DECIMAL | 8,2 | NULL | 0.00 | - | - | 平均応答時間（ミリ秒） |
| 18 | concurrent_users_max | 最大同時接続数 | INT | - | NULL | 0 | - | - | 最大同時接続ユーザー数 |
| 19 | data_transfer_mb | データ転送量(MB) | BIGINT | - | NULL | 0 | - | - | データ転送量 |
| 20 | feature_usage_json | 機能使用状況 | JSON | - | NULL | NULL | - | - | 機能別使用状況（JSON形式） |
| 21 | billing_amount | 課金額 | DECIMAL | 10,2 | NULL | 0.00 | - | - | 計算された課金額 |
| 22 | usage_status | 使用状況 | VARCHAR | 20 | NOT NULL | 'NORMAL' | - | - | 使用状況（NORMAL/WARNING/CRITICAL） |
| 23 | notes | 備考 | TEXT | - | NULL | NULL | - | - | 特記事項・備考 |
| 24 | created_at | 作成日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP | - | - | レコード作成日時 |
| 25 | updated_at | 更新日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | レコード更新日時 |
| 26 | created_by | 作成者 | VARCHAR | 50 | NOT NULL | 'SYSTEM' | - | - | レコード作成者 |
| 27 | updated_by | 更新者 | VARCHAR | 50 | NOT NULL | 'SYSTEM' | - | - | レコード更新者 |

## 制約

### 主キー制約
- PRIMARY KEY (usage_id)

### 外部キー制約
- FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id)

### ユニーク制約
- UNIQUE KEY uk_tenant_date_type (tenant_id, measurement_date, measurement_type)

### チェック制約
- CHECK (measurement_type IN ('DAILY', 'MONTHLY', 'YEARLY'))
- CHECK (usage_status IN ('NORMAL', 'WARNING', 'CRITICAL'))
- CHECK (active_users >= 0)
- CHECK (total_users >= 0)
- CHECK (storage_used_mb >= 0)
- CHECK (api_calls >= 0)
- CHECK (cpu_usage_percent >= 0 AND cpu_usage_percent <= 100)
- CHECK (billing_amount >= 0)

## インデックス

| インデックス名 | 種別 | 対象カラム | 説明 |
|---------------|------|------------|------|
| idx_tenant_date | BTREE | tenant_id, measurement_date | テナント・日付での検索用 |
| idx_measurement_date | BTREE | measurement_date | 日付での検索用 |
| idx_measurement_type | BTREE | measurement_type | 計測タイプでの検索用 |
| idx_usage_status | BTREE | usage_status | 使用状況での検索用 |
| idx_billing_amount | BTREE | billing_amount | 課金額での検索用 |
| idx_created_at | BTREE | created_at | 作成日時での検索用 |

## DDL

```sql
CREATE TABLE SYS_TenantUsage (
    usage_id BIGINT NOT NULL AUTO_INCREMENT COMMENT '使用量ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    measurement_date DATE NOT NULL COMMENT '計測日',
    measurement_type VARCHAR(20) NOT NULL COMMENT '計測タイプ',
    active_users INT DEFAULT 0 COMMENT 'アクティブユーザー数',
    total_users INT DEFAULT 0 COMMENT '総ユーザー数',
    storage_used_mb BIGINT DEFAULT 0 COMMENT 'ストレージ使用量(MB)',
    api_calls BIGINT DEFAULT 0 COMMENT 'API呼び出し数',
    login_count INT DEFAULT 0 COMMENT 'ログイン回数',
    skill_records INT DEFAULT 0 COMMENT 'スキル記録数',
    report_generated INT DEFAULT 0 COMMENT '生成レポート数',
    backup_size_mb BIGINT DEFAULT 0 COMMENT 'バックアップサイズ(MB)',
    cpu_usage_percent DECIMAL(5,2) DEFAULT 0.00 COMMENT 'CPU使用率',
    memory_usage_mb BIGINT DEFAULT 0 COMMENT 'メモリ使用量(MB)',
    network_traffic_mb BIGINT DEFAULT 0 COMMENT 'ネットワーク通信量(MB)',
    error_count INT DEFAULT 0 COMMENT 'エラー発生数',
    response_time_avg DECIMAL(8,2) DEFAULT 0.00 COMMENT '平均応答時間(ms)',
    concurrent_users_max INT DEFAULT 0 COMMENT '最大同時接続数',
    data_transfer_mb BIGINT DEFAULT 0 COMMENT 'データ転送量(MB)',
    feature_usage_json JSON COMMENT '機能使用状況',
    billing_amount DECIMAL(10,2) DEFAULT 0.00 COMMENT '課金額',
    usage_status VARCHAR(20) NOT NULL DEFAULT 'NORMAL' COMMENT '使用状況',
    notes TEXT COMMENT '備考',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL DEFAULT 'SYSTEM' COMMENT '作成者',
    updated_by VARCHAR(50) NOT NULL DEFAULT 'SYSTEM' COMMENT '更新者',
    
    PRIMARY KEY (usage_id),
    UNIQUE KEY uk_tenant_date_type (tenant_id, measurement_date, measurement_type),
    
    CONSTRAINT fk_tenant_usage_tenant 
        FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id),
    
    CONSTRAINT chk_measurement_type 
        CHECK (measurement_type IN ('DAILY', 'MONTHLY', 'YEARLY')),
    CONSTRAINT chk_usage_status 
        CHECK (usage_status IN ('NORMAL', 'WARNING', 'CRITICAL')),
    CONSTRAINT chk_active_users 
        CHECK (active_users >= 0),
    CONSTRAINT chk_total_users 
        CHECK (total_users >= 0),
    CONSTRAINT chk_storage_used 
        CHECK (storage_used_mb >= 0),
    CONSTRAINT chk_api_calls 
        CHECK (api_calls >= 0),
    CONSTRAINT chk_cpu_usage 
        CHECK (cpu_usage_percent >= 0 AND cpu_usage_percent <= 100),
    CONSTRAINT chk_billing_amount 
        CHECK (billing_amount >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='テナント使用量管理テーブル';

-- インデックス作成
CREATE INDEX idx_tenant_date ON SYS_TenantUsage(tenant_id, measurement_date);
CREATE INDEX idx_measurement_date ON SYS_TenantUsage(measurement_date);
CREATE INDEX idx_measurement_type ON SYS_TenantUsage(measurement_type);
CREATE INDEX idx_usage_status ON SYS_TenantUsage(usage_status);
CREATE INDEX idx_billing_amount ON SYS_TenantUsage(billing_amount);
CREATE INDEX idx_created_at ON SYS_TenantUsage(created_at);
```

## 関連テーブル

| テーブル名 | 関係 | 説明 |
|------------|------|------|
| MST_Tenant | 親 | テナント基本情報 |
| MST_TenantSettings | 関連 | テナント設定情報 |
| SYS_SystemLog | 関連 | システムログ |
| SYS_AuditLog | 関連 | 監査ログ |

## 利用API

| API ID | API名 | 説明 |
|--------|-------|------|
| API-025 | テナント管理API | テナント使用量取得 |
| API-026 | テナント設定API | 使用量制限設定 |

## 利用バッチ

| バッチ ID | バッチ名 | 説明 |
|-----------|----------|------|
| BATCH-018-01 | テナント使用量集計バッチ | 日次使用量集計 |
| BATCH-018-02 | テナント課金計算バッチ | 課金額計算 |
| BATCH-018-03 | テナント状態監視バッチ | 使用量監視 |

## 運用考慮事項

### パフォーマンス
- 大量データが蓄積されるため、パーティショニング（月別）を検討
- 古いデータのアーカイブ戦略が必要
- 集計処理の最適化が重要

### セキュリティ
- テナント間のデータ分離を厳密に実施
- 使用量データの機密性保護
- 課金情報の改ざん防止

### 監査
- 使用量データの変更履歴を記録
- 課金計算の透明性確保
- データ整合性の定期チェック

### バックアップ
- 課金に関わる重要データのため、頻繁なバックアップが必要
- 長期保存要件への対応

## データサンプル

```sql
-- 日次使用量データ例
INSERT INTO SYS_TenantUsage (
    tenant_id, measurement_date, measurement_type,
    active_users, total_users, storage_used_mb, api_calls,
    login_count, skill_records, report_generated,
    cpu_usage_percent, memory_usage_mb, billing_amount,
    usage_status
) VALUES (
    'tenant001', '2025-05-31', 'DAILY',
    45, 100, 2048, 15000,
    120, 25, 5,
    65.50, 1024, 150.00,
    'NORMAL'
);

-- 月次集計データ例
INSERT INTO SYS_TenantUsage (
    tenant_id, measurement_date, measurement_type,
    active_users, total_users, storage_used_mb, api_calls,
    billing_amount, usage_status
) VALUES (
    'tenant001', '2025-05-01', 'MONTHLY',
    1200, 100, 65536, 450000,
    4500.00, 'NORMAL'
);
```

## 変更履歴

| 版数 | 変更日 | 変更者 | 変更内容 |
|------|--------|--------|----------|
| 1.0 | 2025-05-31 | システム管理者 | 初版作成 |
