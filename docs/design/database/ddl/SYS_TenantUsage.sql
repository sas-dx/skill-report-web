-- ============================================
-- テーブル: SYS_TenantUsage
-- 論理名: テナント利用状況
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS SYS_TenantUsage;

CREATE TABLE SYS_TenantUsage (
    usage_date DATE COMMENT '利用状況を記録した日付',
    tenant_id VARCHAR(50) COMMENT '利用状況を記録するテナントのID',
    active_users INTEGER DEFAULT 0 COMMENT '当日にログインしたユーザー数',
    total_logins INTEGER DEFAULT 0 COMMENT '当日の総ログイン回数',
    api_requests BIGINT DEFAULT 0 COMMENT '当日のAPIリクエスト総数',
    data_storage_mb DECIMAL(15,2) DEFAULT 0.0 COMMENT '当日時点でのデータストレージ使用量（MB）',
    file_storage_mb DECIMAL(15,2) DEFAULT 0.0 COMMENT '当日時点でのファイルストレージ使用量（MB）',
    backup_storage_mb DECIMAL(15,2) DEFAULT 0.0 COMMENT '当日時点でのバックアップストレージ使用量（MB）',
    cpu_usage_minutes DECIMAL(10,2) DEFAULT 0.0 COMMENT '当日のCPU使用時間（分）',
    memory_usage_mb_hours DECIMAL(15,2) DEFAULT 0.0 COMMENT '当日のメモリ使用量（MB×時間）',
    network_transfer_mb DECIMAL(15,2) DEFAULT 0.0 COMMENT '当日のネットワーク転送量（MB）',
    report_generations INTEGER DEFAULT 0 COMMENT '当日のレポート生成回数',
    skill_assessments INTEGER DEFAULT 0 COMMENT '当日のスキル評価実行回数',
    notification_sent INTEGER DEFAULT 0 COMMENT '当日の通知送信回数',
    peak_concurrent_users INTEGER DEFAULT 0 COMMENT '当日の最大同時接続ユーザー数',
    peak_time TIME COMMENT '最大同時接続を記録した時刻',
    error_count INTEGER DEFAULT 0 COMMENT '当日のシステムエラー発生回数',
    response_time_avg_ms DECIMAL(8,2) COMMENT '当日のAPI平均応答時間（ミリ秒）',
    uptime_percentage DECIMAL(5,2) DEFAULT 100.0 COMMENT '当日のシステム稼働率（%）',
    billing_amount DECIMAL(10,2) COMMENT '当日の利用に基づく課金額',
    collection_timestamp TIMESTAMP COMMENT '利用状況データを収集した日時',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_SYS_TenantUsage_date_tenant ON SYS_TenantUsage (usage_date, tenant_id);
CREATE INDEX idx_SYS_TenantUsage_tenant_id ON SYS_TenantUsage (tenant_id);
CREATE INDEX idx_SYS_TenantUsage_usage_date ON SYS_TenantUsage (usage_date);
CREATE INDEX idx_SYS_TenantUsage_collection_timestamp ON SYS_TenantUsage (collection_timestamp);
CREATE INDEX idx_SYS_TenantUsage_billing_amount ON SYS_TenantUsage (billing_amount);

-- 外部キー制約
ALTER TABLE SYS_TenantUsage ADD CONSTRAINT fk_SYS_TenantUsage_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(id) ON UPDATE CASCADE ON DELETE CASCADE;

-- その他の制約
ALTER TABLE SYS_TenantUsage ADD CONSTRAINT uk_SYS_TenantUsage_date_tenant UNIQUE ();
ALTER TABLE SYS_TenantUsage ADD CONSTRAINT chk_SYS_TenantUsage_active_users CHECK (active_users >= 0);
ALTER TABLE SYS_TenantUsage ADD CONSTRAINT chk_SYS_TenantUsage_total_logins CHECK (total_logins >= 0);
ALTER TABLE SYS_TenantUsage ADD CONSTRAINT chk_SYS_TenantUsage_api_requests CHECK (api_requests >= 0);
ALTER TABLE SYS_TenantUsage ADD CONSTRAINT chk_SYS_TenantUsage_storage_usage CHECK (data_storage_mb >= 0 AND file_storage_mb >= 0 AND backup_storage_mb >= 0);
ALTER TABLE SYS_TenantUsage ADD CONSTRAINT chk_SYS_TenantUsage_resource_usage CHECK (cpu_usage_minutes >= 0 AND memory_usage_mb_hours >= 0 AND network_transfer_mb >= 0);
ALTER TABLE SYS_TenantUsage ADD CONSTRAINT chk_SYS_TenantUsage_counts CHECK (report_generations >= 0 AND skill_assessments >= 0 AND notification_sent >= 0);
ALTER TABLE SYS_TenantUsage ADD CONSTRAINT chk_SYS_TenantUsage_peak_concurrent_users CHECK (peak_concurrent_users >= 0);
ALTER TABLE SYS_TenantUsage ADD CONSTRAINT chk_SYS_TenantUsage_error_count CHECK (error_count >= 0);
ALTER TABLE SYS_TenantUsage ADD CONSTRAINT chk_SYS_TenantUsage_response_time CHECK (response_time_avg_ms IS NULL OR response_time_avg_ms >= 0);
ALTER TABLE SYS_TenantUsage ADD CONSTRAINT chk_SYS_TenantUsage_uptime_percentage CHECK (uptime_percentage >= 0 AND uptime_percentage <= 100);
ALTER TABLE SYS_TenantUsage ADD CONSTRAINT chk_SYS_TenantUsage_billing_amount CHECK (billing_amount IS NULL OR billing_amount >= 0);
