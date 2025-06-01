-- SYS_TenantUsage (テナント使用量) DDL
-- 生成日時: 2025-06-01 20:40:26

CREATE TABLE SYS_TenantUsage (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    usage_date DATE,
    tenant_id VARCHAR(50),
    active_users INTEGER DEFAULT 0,
    total_logins INTEGER DEFAULT 0,
    api_requests BIGINT DEFAULT 0,
    data_storage_mb DECIMAL(15,2) DEFAULT 0.0,
    file_storage_mb DECIMAL(15,2) DEFAULT 0.0,
    backup_storage_mb DECIMAL(15,2) DEFAULT 0.0,
    cpu_usage_minutes DECIMAL(10,2) DEFAULT 0.0,
    memory_usage_mb_hours DECIMAL(15,2) DEFAULT 0.0,
    network_transfer_mb DECIMAL(15,2) DEFAULT 0.0,
    report_generations INTEGER DEFAULT 0,
    skill_assessments INTEGER DEFAULT 0,
    notification_sent INTEGER DEFAULT 0,
    peak_concurrent_users INTEGER DEFAULT 0,
    peak_time TIME,
    error_count INTEGER DEFAULT 0,
    response_time_avg_ms DECIMAL(8,2),
    uptime_percentage DECIMAL(5,2) DEFAULT 100.0,
    billing_amount DECIMAL(10,2),
    collection_timestamp TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_SYS_TenantUsage_date_tenant ON SYS_TenantUsage (usage_date, tenant_id);
CREATE INDEX idx_SYS_TenantUsage_tenant_id ON SYS_TenantUsage (tenant_id);
CREATE INDEX idx_SYS_TenantUsage_usage_date ON SYS_TenantUsage (usage_date);
CREATE INDEX idx_SYS_TenantUsage_collection_timestamp ON SYS_TenantUsage (collection_timestamp);
CREATE INDEX idx_SYS_TenantUsage_billing_amount ON SYS_TenantUsage (billing_amount);

-- 外部キー制約
ALTER TABLE SYS_TenantUsage ADD CONSTRAINT fk_SYS_TenantUsage_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(id) ON UPDATE CASCADE ON DELETE CASCADE;
