-- ============================================
-- テーブル: WRK_BatchJobLog
-- 論理名: 一括登録ジョブログ
-- 説明: 一括登録・更新処理のジョブ実行ログを管理するワーク系テーブル。

主な目的：
- バッチ処理の実行状況監視
- エラー発生時の原因調査・トラブルシューティング
- 処理結果の統計情報管理
- 一括処理の進捗追跡

このテーブルは一時的なワークテーブルとして機能し、
処理完了後は定期的にアーカイブ・削除される。
主に管理者画面での監視とAPI経由での状況確認に使用される。

-- 作成日: 2025-06-24 22:56:14
-- ============================================

DROP TABLE IF EXISTS WRK_BatchJobLog;

CREATE TABLE WRK_BatchJobLog (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    job_id VARCHAR(50) COMMENT 'ジョブID',
    batchjoblog_id INT AUTO_INCREMENT NOT NULL COMMENT 'WRK_BatchJobLogの主キー',
    end_time TIMESTAMP COMMENT '終了時刻',
    error_details TEXT COMMENT 'エラー詳細',
    error_records INTEGER DEFAULT 0 COMMENT 'エラーレコード数',
    executed_by VARCHAR(50) COMMENT '実行者',
    execution_environment VARCHAR(100) COMMENT '実行環境',
    input_file_path VARCHAR(500) COMMENT '入力ファイルパス',
    job_name VARCHAR(200) COMMENT 'ジョブ名',
    job_parameters TEXT COMMENT 'ジョブパラメータ',
    job_type ENUM('SKILL_IMPORT', 'EMPLOYEE_IMPORT', 'BULK_UPDATE', 'BULK_DELETE', 'DATA_EXPORT') DEFAULT 'SKILL_IMPORT' COMMENT 'ジョブ種別',
    output_file_path VARCHAR(500) COMMENT '出力ファイルパス',
    processed_records INTEGER DEFAULT 0 COMMENT '処理済みレコード数',
    progress_percentage DECIMAL(5,2) DEFAULT 0.0 COMMENT '進捗率',
    start_time TIMESTAMP COMMENT '開始時刻',
    status ENUM('PENDING', 'RUNNING', 'COMPLETED', 'FAILED', 'CANCELLED') DEFAULT 'PENDING' COMMENT '実行ステータス',
    success_records INTEGER DEFAULT 0 COMMENT '成功レコード数',
    total_records INTEGER DEFAULT 0 COMMENT '総レコード数',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_WRK_BatchJobLog_job_id ON WRK_BatchJobLog (job_id);
CREATE INDEX idx_WRK_BatchJobLog_status ON WRK_BatchJobLog (status);
CREATE INDEX idx_WRK_BatchJobLog_start_time ON WRK_BatchJobLog (start_time);
CREATE INDEX idx_WRK_BatchJobLog_executed_by ON WRK_BatchJobLog (executed_by);
CREATE INDEX idx_WRK_BatchJobLog_job_type ON WRK_BatchJobLog (job_type);
CREATE INDEX idx_WRK_BatchJobLog_status_start_time ON WRK_BatchJobLog (status, start_time);
CREATE INDEX idx_wrk_batchjoblog_tenant_id ON WRK_BatchJobLog (tenant_id);

-- 外部キー制約
ALTER TABLE WRK_BatchJobLog ADD CONSTRAINT fk_WRK_BatchJobLog_executed_by FOREIGN KEY (executed_by) REFERENCES MST_UserAuth(id) ON UPDATE CASCADE ON DELETE RESTRICT;

-- その他の制約
ALTER TABLE WRK_BatchJobLog ADD CONSTRAINT chk_WRK_BatchJobLog_status CHECK (status IN ('PENDING', 'RUNNING', 'COMPLETED', 'FAILED', 'CANCELLED'));
ALTER TABLE WRK_BatchJobLog ADD CONSTRAINT chk_WRK_BatchJobLog_job_type CHECK (job_type IN ('SKILL_IMPORT', 'EMPLOYEE_IMPORT', 'BULK_UPDATE', 'BULK_DELETE', 'DATA_EXPORT'));
ALTER TABLE WRK_BatchJobLog ADD CONSTRAINT chk_WRK_BatchJobLog_records_positive CHECK (total_records >= 0 AND processed_records >= 0 AND success_records >= 0 AND error_records >= 0);
ALTER TABLE WRK_BatchJobLog ADD CONSTRAINT chk_WRK_BatchJobLog_progress_range CHECK (progress_percentage >= 0.00 AND progress_percentage <= 100.00);
ALTER TABLE WRK_BatchJobLog ADD CONSTRAINT chk_WRK_BatchJobLog_time_consistency CHECK (end_time IS NULL OR start_time IS NULL OR start_time <= end_time);
ALTER TABLE WRK_BatchJobLog ADD CONSTRAINT chk_WRK_BatchJobLog_record_consistency CHECK (processed_records <= total_records AND (success_records + error_records) <= processed_records);
