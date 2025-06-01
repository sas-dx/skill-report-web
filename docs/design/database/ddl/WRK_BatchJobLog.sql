-- WRK_BatchJobLog (一括登録ジョブログ) DDL
-- 生成日時: 2025-06-01 20:24:51

CREATE TABLE WRK_BatchJobLog (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    job_id VARCHAR(50),
    job_name VARCHAR(200),
    job_type ENUM DEFAULT 'SKILL_IMPORT',
    status ENUM DEFAULT 'PENDING',
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    total_records INTEGER DEFAULT 0,
    processed_records INTEGER DEFAULT 0,
    success_records INTEGER DEFAULT 0,
    error_records INTEGER DEFAULT 0,
    error_details TEXT,
    input_file_path VARCHAR(500),
    output_file_path VARCHAR(500),
    executed_by VARCHAR(50),
    progress_percentage DECIMAL(5,2) DEFAULT 0.0,
    execution_environment VARCHAR(100),
    job_parameters TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_WRK_BatchJobLog_job_id ON WRK_BatchJobLog (job_id);
CREATE INDEX idx_WRK_BatchJobLog_status ON WRK_BatchJobLog (status);
CREATE INDEX idx_WRK_BatchJobLog_start_time ON WRK_BatchJobLog (start_time);
CREATE INDEX idx_WRK_BatchJobLog_executed_by ON WRK_BatchJobLog (executed_by);
CREATE INDEX idx_WRK_BatchJobLog_job_type ON WRK_BatchJobLog (job_type);
CREATE INDEX idx_WRK_BatchJobLog_status_start_time ON WRK_BatchJobLog (status, start_time);

-- 外部キー制約
ALTER TABLE WRK_BatchJobLog ADD CONSTRAINT fk_WRK_BatchJobLog_executed_by FOREIGN KEY (executed_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT;
