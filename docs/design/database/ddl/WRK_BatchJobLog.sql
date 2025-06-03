-- ============================================
-- テーブル: WRK_BatchJobLog
-- 論理名: 一括登録ジョブログ
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS WRK_BatchJobLog;

CREATE TABLE WRK_BatchJobLog (
    job_id VARCHAR(50) COMMENT '一括処理ジョブの一意識別子（UUID形式）',
    job_name VARCHAR(200) COMMENT '実行されたジョブの名称（画面表示用）',
    job_type ENUM DEFAULT 'SKILL_IMPORT' COMMENT 'ジョブの種別（SKILL_IMPORT:スキル情報一括登録、EMPLOYEE_IMPORT:社員情報一括登録、BULK_UPDATE:一括更新、BULK_DELETE:一括削除、DATA_EXPORT:データエクスポート）',
    status ENUM DEFAULT 'PENDING' COMMENT 'ジョブの実行状況（PENDING:待機中、RUNNING:実行中、COMPLETED:完了、FAILED:失敗、CANCELLED:キャンセル）',
    start_time TIMESTAMP COMMENT 'ジョブ実行開始日時',
    end_time TIMESTAMP COMMENT 'ジョブ実行終了日時',
    total_records INTEGER DEFAULT 0 COMMENT '処理対象の総レコード数',
    processed_records INTEGER DEFAULT 0 COMMENT '実際に処理されたレコード数',
    success_records INTEGER DEFAULT 0 COMMENT '正常に処理されたレコード数',
    error_records INTEGER DEFAULT 0 COMMENT 'エラーが発生したレコード数',
    error_details TEXT COMMENT 'エラー内容の詳細情報（JSON形式でエラーメッセージ、行番号、カラム名等を格納）',
    input_file_path VARCHAR(500) COMMENT '処理対象の入力ファイルパス（CSVファイル等）',
    output_file_path VARCHAR(500) COMMENT '処理結果の出力ファイルパス（エラーレポート等）',
    executed_by VARCHAR(50) COMMENT 'ジョブを実行したユーザーのID',
    progress_percentage DECIMAL(5,2) DEFAULT 0.0 COMMENT 'ジョブの進捗率（0.00-100.00）',
    execution_environment VARCHAR(100) COMMENT 'ジョブが実行された環境情報（サーバー名、プロセスID等）',
    job_parameters TEXT COMMENT 'ジョブ実行時のパラメータ情報（JSON形式）',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_WRK_BatchJobLog_job_id ON WRK_BatchJobLog (job_id);
CREATE INDEX idx_WRK_BatchJobLog_status ON WRK_BatchJobLog (status);
CREATE INDEX idx_WRK_BatchJobLog_start_time ON WRK_BatchJobLog (start_time);
CREATE INDEX idx_WRK_BatchJobLog_executed_by ON WRK_BatchJobLog (executed_by);
CREATE INDEX idx_WRK_BatchJobLog_job_type ON WRK_BatchJobLog (job_type);
CREATE INDEX idx_WRK_BatchJobLog_status_start_time ON WRK_BatchJobLog (status, start_time);

-- 外部キー制約
ALTER TABLE WRK_BatchJobLog ADD CONSTRAINT fk_WRK_BatchJobLog_executed_by FOREIGN KEY (executed_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT;

-- その他の制約
ALTER TABLE WRK_BatchJobLog ADD CONSTRAINT chk_WRK_BatchJobLog_status CHECK (status IN ('PENDING', 'RUNNING', 'COMPLETED', 'FAILED', 'CANCELLED'));
ALTER TABLE WRK_BatchJobLog ADD CONSTRAINT chk_WRK_BatchJobLog_job_type CHECK (job_type IN ('SKILL_IMPORT', 'EMPLOYEE_IMPORT', 'BULK_UPDATE', 'BULK_DELETE', 'DATA_EXPORT'));
ALTER TABLE WRK_BatchJobLog ADD CONSTRAINT chk_WRK_BatchJobLog_records_positive CHECK (total_records >= 0 AND processed_records >= 0 AND success_records >= 0 AND error_records >= 0);
ALTER TABLE WRK_BatchJobLog ADD CONSTRAINT chk_WRK_BatchJobLog_progress_range CHECK (progress_percentage >= 0.00 AND progress_percentage <= 100.00);
ALTER TABLE WRK_BatchJobLog ADD CONSTRAINT chk_WRK_BatchJobLog_time_consistency CHECK (end_time IS NULL OR start_time IS NULL OR start_time <= end_time);
ALTER TABLE WRK_BatchJobLog ADD CONSTRAINT chk_WRK_BatchJobLog_record_consistency CHECK (processed_records <= total_records AND (success_records + error_records) <= processed_records);
