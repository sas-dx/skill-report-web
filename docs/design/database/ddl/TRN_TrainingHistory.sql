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

-- 作成日: 2025-06-24 22:56:15
-- ============================================

DROP TABLE IF EXISTS TRN_TrainingHistory;

CREATE TABLE TRN_TrainingHistory (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    training_name VARCHAR(200) COMMENT '研修名',
    approved_by VARCHAR(50) COMMENT '承認者',
    attendance_status ENUM('COMPLETED', 'PARTIAL', 'ABSENT', 'CANCELLED') DEFAULT 'COMPLETED' COMMENT '出席状況',
    certificate_number VARCHAR(100) COMMENT '証明書番号',
    certificate_obtained BOOLEAN DEFAULT False COMMENT '修了証取得',
    completion_rate DECIMAL(5,2) COMMENT '完了率',
    cost DECIMAL(10,2) COMMENT '費用',
    cost_covered_by ENUM('COMPANY', 'EMPLOYEE', 'SHARED') COMMENT '費用負担者',
    duration_hours DECIMAL(5,1) COMMENT '研修時間',
    employee_id VARCHAR(50) COMMENT '社員ID',
    end_date DATE COMMENT '終了日',
    feedback TEXT COMMENT 'フィードバック',
    follow_up_date DATE COMMENT 'フォローアップ予定日',
    follow_up_required BOOLEAN DEFAULT False COMMENT 'フォローアップ要否',
    grade VARCHAR(10) COMMENT '成績',
    instructor_name VARCHAR(100) COMMENT '講師名',
    learning_objectives TEXT COMMENT '学習目標',
    learning_outcomes TEXT COMMENT '学習成果',
    location VARCHAR(200) COMMENT '開催場所',
    manager_approval BOOLEAN DEFAULT False COMMENT '上司承認',
    pdu_earned DECIMAL(5,1) COMMENT '獲得PDU',
    provider_name VARCHAR(100) COMMENT '提供機関名',
    recommendation_score DECIMAL(3,1) COMMENT '推奨度',
    satisfaction_score DECIMAL(3,1) COMMENT '満足度',
    skills_acquired TEXT COMMENT '習得スキル',
    start_date DATE COMMENT '開始日',
    test_score DECIMAL(5,2) COMMENT 'テスト点数',
    training_category ENUM('TECHNICAL', 'BUSINESS', 'MANAGEMENT', 'SOFT_SKILL', 'COMPLIANCE') COMMENT '研修カテゴリ',
    training_history_id VARCHAR(50) COMMENT '研修履歴ID',
    training_program_id VARCHAR(50) COMMENT '研修プログラムID',
    training_type ENUM('INTERNAL', 'EXTERNAL', 'ONLINE', 'CERTIFICATION', 'CONFERENCE') COMMENT '研修種別',
    traininghistory_id INT AUTO_INCREMENT NOT NULL COMMENT 'TRN_TrainingHistoryの主キー',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    created_by VARCHAR(50) COMMENT '作成者ID',
    updated_by VARCHAR(50) COMMENT '更新者ID',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
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
CREATE INDEX idx_trn_traininghistory_tenant_id ON TRN_TrainingHistory (tenant_id);

-- 外部キー制約
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT fk_training_history_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT fk_training_history_program FOREIGN KEY (training_program_id) REFERENCES MST_TrainingProgram(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT fk_training_history_approver FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
-- 制約DDL生成エラー: uk_training_history_id
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT chk_training_type CHECK (training_type IN ('INTERNAL', 'EXTERNAL', 'ONLINE', 'CERTIFICATION', 'CONFERENCE'));
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT chk_training_category CHECK (training_category IN ('TECHNICAL', 'BUSINESS', 'MANAGEMENT', 'SOFT_SKILL', 'COMPLIANCE'));
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT chk_cost_covered_by CHECK (cost_covered_by IN ('COMPANY', 'EMPLOYEE', 'SHARED'));
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT chk_attendance_status CHECK (attendance_status IN ('COMPLETED', 'PARTIAL', 'ABSENT', 'CANCELLED'));
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT chk_date_range CHECK (end_date IS NULL OR start_date <= end_date);
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT chk_duration_hours CHECK (duration_hours IS NULL OR duration_hours > 0);
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT chk_completion_rate CHECK (completion_rate IS NULL OR (completion_rate >= 0 AND completion_rate <= 100));
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT chk_test_score CHECK (test_score IS NULL OR test_score >= 0);
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT chk_satisfaction_score CHECK (satisfaction_score IS NULL OR (satisfaction_score >= 1.0 AND satisfaction_score <= 5.0));
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT chk_recommendation_score CHECK (recommendation_score IS NULL OR (recommendation_score >= 1.0 AND recommendation_score <= 5.0));
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT chk_cost CHECK (cost IS NULL OR cost >= 0);
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT chk_pdu_earned CHECK (pdu_earned IS NULL OR pdu_earned >= 0);
