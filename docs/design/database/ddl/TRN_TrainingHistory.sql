-- ============================================
-- テーブル: TRN_TrainingHistory
-- 論理名: 研修参加履歴
-- 説明: TRN_TrainingHistory（研修参加履歴）は、社員が参加した研修・教育プログラムの履歴を管理するトランザクションテーブルです。

主な目的：
- 研修参加履歴の記録・管理
- 学習成果・評価の記録
- スキル向上の追跡
- 継続教育ポイント（PDU）の管理
- 人材育成計画の進捗管理

このテーブルにより、社員の学習履歴を体系的に記録し、
スキル開発やキャリア形成の支援を効率的に行うことができます。

-- 作成日: 2025-06-21 17:20:34
-- ============================================

DROP TABLE IF EXISTS TRN_TrainingHistory;

CREATE TABLE TRN_TrainingHistory (
    training_history_id VARCHAR,
    employee_id VARCHAR,
    training_program_id VARCHAR,
    training_name VARCHAR,
    training_type ENUM,
    training_category ENUM,
    provider_name VARCHAR,
    instructor_name VARCHAR,
    start_date DATE,
    end_date DATE,
    duration_hours DECIMAL,
    location VARCHAR,
    cost DECIMAL,
    cost_covered_by ENUM,
    attendance_status ENUM DEFAULT 'COMPLETED',
    completion_rate DECIMAL,
    test_score DECIMAL,
    grade VARCHAR,
    certificate_obtained BOOLEAN DEFAULT False,
    certificate_number VARCHAR,
    pdu_earned DECIMAL,
    skills_acquired TEXT,
    learning_objectives TEXT,
    learning_outcomes TEXT,
    feedback TEXT,
    satisfaction_score DECIMAL,
    recommendation_score DECIMAL,
    follow_up_required BOOLEAN DEFAULT False,
    follow_up_date DATE,
    manager_approval BOOLEAN DEFAULT False,
    approved_by VARCHAR,
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    created_by VARCHAR(50) NOT NULL COMMENT 'レコード作成者のユーザーID',
    updated_by VARCHAR(50) NOT NULL COMMENT 'レコード更新者のユーザーID',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時',
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_training_history_id ON TRN_TrainingHistory (training_history_id);
CREATE INDEX idx_employee_id ON TRN_TrainingHistory (employee_id);
CREATE INDEX idx_training_program_id ON TRN_TrainingHistory (training_program_id);
CREATE INDEX idx_training_type ON TRN_TrainingHistory (training_type);
CREATE INDEX idx_training_category ON TRN_TrainingHistory (training_category);
CREATE INDEX idx_date_range ON TRN_TrainingHistory (start_date, end_date);
CREATE INDEX idx_attendance_status ON TRN_TrainingHistory (attendance_status);
CREATE INDEX idx_employee_period ON TRN_TrainingHistory (employee_id, start_date, end_date);
CREATE INDEX idx_certificate ON TRN_TrainingHistory (certificate_obtained, certificate_number);
