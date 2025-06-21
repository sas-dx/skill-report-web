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

-- 作成日: 2025-06-21 17:20:34
-- ============================================

DROP TABLE IF EXISTS WRK_BatchJobLog;

CREATE TABLE WRK_BatchJobLog (
    job_id VARCHAR,
    job_name VARCHAR,
    job_type ENUM DEFAULT 'SKILL_IMPORT',
    status ENUM DEFAULT 'PENDING',
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    total_records INTEGER DEFAULT 0,
    processed_records INTEGER DEFAULT 0,
    success_records INTEGER DEFAULT 0,
    error_records INTEGER DEFAULT 0,
    error_details TEXT,
    input_file_path VARCHAR,
    output_file_path VARCHAR,
    executed_by VARCHAR,
    progress_percentage DECIMAL DEFAULT 0.0,
    execution_environment VARCHAR,
    job_parameters TEXT,
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
