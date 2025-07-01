-- ============================================
-- テーブル: SYS_TenantUsage
-- 論理名: テナント利用状況
-- 説明: テナント利用状況テーブルは、マルチテナント環境における各テナントのシステム利用状況を管理するシステムテーブルです。

主な目的：
- テナント別のリソース使用量監視
- 課金情報の基礎データ収集
- システム負荷分析とキャパシティプランニング
- SLA監視とパフォーマンス分析

このテーブルは、マルチテナントシステムの運用管理と課金処理を支える重要なテーブルで、
テナント毎の公平なリソース配分と適切な課金を実現します。

-- 作成日: 2025-06-24 23:05:57
-- ============================================

DROP TABLE IF EXISTS SYS_TenantUsage;

CREATE TABLE SYS_TenantUsage (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) COMMENT 'テナントID',
    active_users INTEGER DEFAULT 0 COMMENT 'アクティブユーザー数',
    api_requests BIGINT DEFAULT 0 COMMENT 'API リクエスト数',
    backup_storage_mb DECIMAL(15,2) DEFAULT 0.0 COMMENT 'バックアップ使用量MB',
    billing_amount DECIMAL(10,2) COMMENT '課金額',
    collection_timestamp TIMESTAMP COMMENT '収集日時',
    cpu_usage_minutes DECIMAL(10,2) DEFAULT 0.0 COMMENT 'CPU使用時間分',
    data_storage_mb DECIMAL(15,2) DEFAULT 0.0 COMMENT 'データ使用量MB',
    error_count INTEGER DEFAULT 0 COMMENT 'エラー発生回数',
    file_storage_mb DECIMAL(15,2) DEFAULT 0.0 COMMENT 'ファイル使用量MB',
    memory_usage_mb_hours DECIMAL(15,2) DEFAULT 0.0 COMMENT 'メモリ使用量MB時',
    network_transfer_mb DECIMAL(15,2) DEFAULT 0.0 COMMENT 'ネットワーク転送量MB',
    notification_sent INTEGER DEFAULT 0 COMMENT '通知送信回数',
    peak_concurrent_users INTEGER DEFAULT 0 COMMENT '最大同時接続ユーザー数',
    peak_time TIME COMMENT 'ピーク時刻',
    report_generations INTEGER DEFAULT 0 COMMENT 'レポート生成回数',
    response_time_avg_ms DECIMAL(8,2) COMMENT '平均応答時間ms',
    skill_assessments INTEGER DEFAULT 0 COMMENT 'スキル評価回数',
    tenantusage_id INT AUTO_INCREMENT NOT NULL COMMENT 'SYS_TenantUsageの主キー',
    total_logins INTEGER DEFAULT 0 COMMENT '総ログイン回数',
    uptime_percentage DECIMAL(5,2) DEFAULT 100.0 COMMENT '稼働率',
    usage_date DATE COMMENT '利用日',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
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
-- 制約DDL生成エラー: uk_SYS_TenantUsage_date_tenant
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
