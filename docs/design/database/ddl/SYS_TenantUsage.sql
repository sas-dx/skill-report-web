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

-- 作成日: 2025-06-21 17:20:34
-- ============================================

DROP TABLE IF EXISTS SYS_TenantUsage;

CREATE TABLE SYS_TenantUsage (
    usage_date DATE,
    tenant_id VARCHAR,
    active_users INTEGER DEFAULT 0,
    total_logins INTEGER DEFAULT 0,
    api_requests BIGINT DEFAULT 0,
    data_storage_mb DECIMAL DEFAULT 0.0,
    file_storage_mb DECIMAL DEFAULT 0.0,
    backup_storage_mb DECIMAL DEFAULT 0.0,
    cpu_usage_minutes DECIMAL DEFAULT 0.0,
    memory_usage_mb_hours DECIMAL DEFAULT 0.0,
    network_transfer_mb DECIMAL DEFAULT 0.0,
    report_generations INTEGER DEFAULT 0,
    skill_assessments INTEGER DEFAULT 0,
    notification_sent INTEGER DEFAULT 0,
    peak_concurrent_users INTEGER DEFAULT 0,
    peak_time TIME,
    error_count INTEGER DEFAULT 0,
    response_time_avg_ms DECIMAL,
    uptime_percentage DECIMAL DEFAULT 100.0,
    billing_amount DECIMAL,
    collection_timestamp TIMESTAMP,
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
