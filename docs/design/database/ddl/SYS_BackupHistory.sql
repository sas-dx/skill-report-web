-- SYS_BackupHistory (バックアップ履歴) DDL
-- 生成日時: 2025-06-01 20:40:26

CREATE TABLE SYS_BackupHistory (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    backup_id VARCHAR(50),
    backup_type ENUM DEFAULT 'FULL',
    backup_scope ENUM DEFAULT 'DATABASE',
    target_objects TEXT,
    backup_start_time TIMESTAMP,
    backup_end_time TIMESTAMP,
    backup_status ENUM DEFAULT 'RUNNING',
    backup_file_path VARCHAR(1000),
    backup_file_size BIGINT,
    compression_type ENUM,
    encryption_enabled BOOLEAN DEFAULT False,
    checksum VARCHAR(128),
    retention_period_days INTEGER DEFAULT 30,
    expiry_date DATE,
    backup_trigger ENUM DEFAULT 'SCHEDULED',
    executed_by VARCHAR(100),
    error_message TEXT,
    recovery_tested BOOLEAN DEFAULT False,
    recovery_test_date DATE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_SYS_BackupHistory_backup_id ON SYS_BackupHistory (backup_id);
CREATE INDEX idx_SYS_BackupHistory_start_time ON SYS_BackupHistory (backup_start_time);
CREATE INDEX idx_SYS_BackupHistory_status ON SYS_BackupHistory (backup_status);
CREATE INDEX idx_SYS_BackupHistory_type_scope ON SYS_BackupHistory (backup_type, backup_scope);
CREATE INDEX idx_SYS_BackupHistory_expiry_date ON SYS_BackupHistory (expiry_date);

-- 外部キー制約
