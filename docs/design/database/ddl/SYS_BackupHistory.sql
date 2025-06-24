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

-- 作成日: 2025-06-24 23:02:18
-- ============================================

DROP TABLE IF EXISTS SYS_BackupHistory;

CREATE TABLE SYS_BackupHistory (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    backup_end_time TIMESTAMP COMMENT 'バックアップ終了時刻',
    backup_file_path VARCHAR(1000) COMMENT 'バックアップファイルパス',
    backup_file_size BIGINT COMMENT 'バックアップファイルサイズ',
    backup_id VARCHAR(50) COMMENT 'バックアップID',
    backup_scope ENUM('DATABASE', 'TABLE', 'SCHEMA') DEFAULT 'DATABASE' COMMENT 'バックアップ範囲',
    backup_start_time TIMESTAMP COMMENT 'バックアップ開始時刻',
    backup_status ENUM('RUNNING', 'SUCCESS', 'FAILED', 'CANCELLED') DEFAULT 'RUNNING' COMMENT 'バックアップ状況',
    backup_trigger ENUM('SCHEDULED', 'MANUAL', 'EMERGENCY') DEFAULT 'SCHEDULED' COMMENT 'バックアップ契機',
    backup_type ENUM('FULL', 'INCREMENTAL', 'DIFFERENTIAL') DEFAULT 'FULL' COMMENT 'バックアップ種別',
    backuphistory_id INT AUTO_INCREMENT NOT NULL COMMENT 'SYS_BackupHistoryの主キー',
    checksum VARCHAR(128) COMMENT 'チェックサム',
    compression_type ENUM('NONE', 'GZIP', 'ZIP') COMMENT '圧縮形式',
    encryption_enabled BOOLEAN DEFAULT False COMMENT '暗号化有無',
    error_message TEXT COMMENT 'エラーメッセージ',
    executed_by VARCHAR(100) COMMENT '実行者',
    expiry_date DATE COMMENT '有効期限',
    recovery_test_date DATE COMMENT '復旧テスト日',
    recovery_tested BOOLEAN DEFAULT False COMMENT '復旧テスト済み',
    retention_period_days INTEGER DEFAULT 30 COMMENT '保持期間日数',
    target_objects TEXT COMMENT '対象オブジェクト',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_SYS_BackupHistory_backup_id ON SYS_BackupHistory (backup_id);
CREATE INDEX idx_SYS_BackupHistory_start_time ON SYS_BackupHistory (backup_start_time);
CREATE INDEX idx_SYS_BackupHistory_status ON SYS_BackupHistory (backup_status);
CREATE INDEX idx_SYS_BackupHistory_type_scope ON SYS_BackupHistory (backup_type, backup_scope);
CREATE INDEX idx_SYS_BackupHistory_expiry_date ON SYS_BackupHistory (expiry_date);

-- その他の制約
-- 制約DDL生成エラー: uk_SYS_BackupHistory_backup_id
ALTER TABLE SYS_BackupHistory ADD CONSTRAINT chk_SYS_BackupHistory_backup_type CHECK (backup_type IN ('FULL', 'INCREMENTAL', 'DIFFERENTIAL'));
ALTER TABLE SYS_BackupHistory ADD CONSTRAINT chk_SYS_BackupHistory_backup_scope CHECK (backup_scope IN ('DATABASE', 'TABLE', 'SCHEMA'));
ALTER TABLE SYS_BackupHistory ADD CONSTRAINT chk_SYS_BackupHistory_backup_status CHECK (backup_status IN ('RUNNING', 'SUCCESS', 'FAILED', 'CANCELLED'));
ALTER TABLE SYS_BackupHistory ADD CONSTRAINT chk_SYS_BackupHistory_compression_type CHECK (compression_type IS NULL OR compression_type IN ('NONE', 'GZIP', 'ZIP'));
ALTER TABLE SYS_BackupHistory ADD CONSTRAINT chk_SYS_BackupHistory_backup_trigger CHECK (backup_trigger IN ('SCHEDULED', 'MANUAL', 'EMERGENCY'));
ALTER TABLE SYS_BackupHistory ADD CONSTRAINT chk_SYS_BackupHistory_retention_period CHECK (retention_period_days > 0);
ALTER TABLE SYS_BackupHistory ADD CONSTRAINT chk_SYS_BackupHistory_file_size CHECK (backup_file_size IS NULL OR backup_file_size >= 0);
ALTER TABLE SYS_BackupHistory ADD CONSTRAINT chk_SYS_BackupHistory_end_time CHECK (backup_end_time IS NULL OR backup_end_time >= backup_start_time);
