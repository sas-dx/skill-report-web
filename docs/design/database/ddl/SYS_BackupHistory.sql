-- ============================================
-- テーブル: SYS_BackupHistory
-- 論理名: バックアップ履歴
-- 説明: バックアップ履歴テーブルは、システムのデータバックアップ実行履歴を管理するシステムテーブルです。

主な目的：
- データベースバックアップの実行履歴管理
- バックアップの成功・失敗状況の記録
- バックアップファイルの保存場所管理
- 復旧時のバックアップ選択支援

このテーブルは、システムの可用性とデータ保護を支える重要なテーブルで、
障害時の迅速な復旧とデータ整合性の確保に貢献します。

-- 作成日: 2025-06-21 17:20:35
-- ============================================

DROP TABLE IF EXISTS SYS_BackupHistory;

CREATE TABLE SYS_BackupHistory (
    backup_id VARCHAR,
    backup_type ENUM DEFAULT 'FULL',
    backup_scope ENUM DEFAULT 'DATABASE',
    target_objects TEXT,
    backup_start_time TIMESTAMP,
    backup_end_time TIMESTAMP,
    backup_status ENUM DEFAULT 'RUNNING',
    backup_file_path VARCHAR,
    backup_file_size BIGINT,
    compression_type ENUM,
    encryption_enabled BOOLEAN DEFAULT False,
    checksum VARCHAR,
    retention_period_days INTEGER DEFAULT 30,
    expiry_date DATE,
    backup_trigger ENUM DEFAULT 'SCHEDULED',
    executed_by VARCHAR,
    error_message TEXT,
    recovery_tested BOOLEAN DEFAULT False,
    recovery_test_date DATE,
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_SYS_BackupHistory_backup_id ON SYS_BackupHistory (backup_id);
CREATE INDEX idx_SYS_BackupHistory_start_time ON SYS_BackupHistory (backup_start_time);
CREATE INDEX idx_SYS_BackupHistory_status ON SYS_BackupHistory (backup_status);
CREATE INDEX idx_SYS_BackupHistory_type_scope ON SYS_BackupHistory (backup_type, backup_scope);
CREATE INDEX idx_SYS_BackupHistory_expiry_date ON SYS_BackupHistory (expiry_date);
