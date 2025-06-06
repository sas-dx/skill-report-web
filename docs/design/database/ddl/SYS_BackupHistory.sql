-- ============================================
-- テーブル: SYS_BackupHistory
-- 論理名: バックアップ履歴
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS SYS_BackupHistory;

CREATE TABLE SYS_BackupHistory (
    backup_id VARCHAR(50) COMMENT 'バックアップの一意識別子',
    backup_type ENUM DEFAULT 'FULL' COMMENT 'バックアップの種別（FULL:フルバックアップ、INCREMENTAL:増分バックアップ、DIFFERENTIAL:差分バックアップ）',
    backup_scope ENUM DEFAULT 'DATABASE' COMMENT 'バックアップ対象範囲（DATABASE:データベース全体、TABLE:特定テーブル、SCHEMA:特定スキーマ）',
    target_objects TEXT COMMENT 'バックアップ対象のテーブル名やスキーマ名（JSON配列形式）',
    backup_start_time TIMESTAMP COMMENT 'バックアップ処理の開始日時',
    backup_end_time TIMESTAMP COMMENT 'バックアップ処理の終了日時',
    backup_status ENUM DEFAULT 'RUNNING' COMMENT 'バックアップの実行状況（RUNNING:実行中、SUCCESS:成功、FAILED:失敗、CANCELLED:キャンセル）',
    backup_file_path VARCHAR(1000) COMMENT 'バックアップファイルの保存先パス',
    backup_file_size BIGINT COMMENT 'バックアップファイルのサイズ（バイト）',
    compression_type ENUM COMMENT 'バックアップファイルの圧縮形式（NONE:無圧縮、GZIP:gzip圧縮、ZIP:zip圧縮）',
    encryption_enabled BOOLEAN DEFAULT False COMMENT 'バックアップファイルの暗号化有無',
    checksum VARCHAR(128) COMMENT 'バックアップファイルの整合性チェック用ハッシュ値',
    retention_period_days INTEGER DEFAULT 30 COMMENT 'バックアップファイルの保持期間（日数）',
    expiry_date DATE COMMENT 'バックアップファイルの有効期限日',
    backup_trigger ENUM DEFAULT 'SCHEDULED' COMMENT 'バックアップ実行の契機（SCHEDULED:スケジュール、MANUAL:手動、EMERGENCY:緊急）',
    executed_by VARCHAR(100) COMMENT 'バックアップを実行したユーザーまたはシステム',
    error_message TEXT COMMENT 'バックアップ失敗時のエラーメッセージ',
    recovery_tested BOOLEAN DEFAULT False COMMENT 'このバックアップからの復旧テストが実施済みかどうか',
    recovery_test_date DATE COMMENT '復旧テストを実施した日付',
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

-- その他の制約
ALTER TABLE SYS_BackupHistory ADD CONSTRAINT uk_SYS_BackupHistory_backup_id UNIQUE ();
ALTER TABLE SYS_BackupHistory ADD CONSTRAINT chk_SYS_BackupHistory_backup_type CHECK (backup_type IN ('FULL', 'INCREMENTAL', 'DIFFERENTIAL'));
ALTER TABLE SYS_BackupHistory ADD CONSTRAINT chk_SYS_BackupHistory_backup_scope CHECK (backup_scope IN ('DATABASE', 'TABLE', 'SCHEMA'));
ALTER TABLE SYS_BackupHistory ADD CONSTRAINT chk_SYS_BackupHistory_backup_status CHECK (backup_status IN ('RUNNING', 'SUCCESS', 'FAILED', 'CANCELLED'));
ALTER TABLE SYS_BackupHistory ADD CONSTRAINT chk_SYS_BackupHistory_compression_type CHECK (compression_type IS NULL OR compression_type IN ('NONE', 'GZIP', 'ZIP'));
ALTER TABLE SYS_BackupHistory ADD CONSTRAINT chk_SYS_BackupHistory_backup_trigger CHECK (backup_trigger IN ('SCHEDULED', 'MANUAL', 'EMERGENCY'));
ALTER TABLE SYS_BackupHistory ADD CONSTRAINT chk_SYS_BackupHistory_retention_period CHECK (retention_period_days > 0);
ALTER TABLE SYS_BackupHistory ADD CONSTRAINT chk_SYS_BackupHistory_file_size CHECK (backup_file_size IS NULL OR backup_file_size >= 0);
ALTER TABLE SYS_BackupHistory ADD CONSTRAINT chk_SYS_BackupHistory_end_time CHECK (backup_end_time IS NULL OR backup_end_time >= backup_start_time);
