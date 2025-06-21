-- ============================================
-- テーブル: MST_EmployeeJobType
-- 論理名: 社員職種関連
-- 説明: MST_EmployeeJobType（社員職種関連）は、社員と職種の関連付けを管理するマスタテーブルです。

主な目的：
- 社員の職種履歴管理
- 複数職種対応（兼任・転職）
- 職種変更の追跡
- 人材配置の最適化
- スキル要件との連携

このテーブルにより、社員の職種変遷を正確に管理し、
適切な人材配置とキャリア開発を支援できます。

-- 作成日: 2025-06-21 17:20:35
-- ============================================

DROP TABLE IF EXISTS MST_EmployeeJobType;

CREATE TABLE MST_EmployeeJobType (
    employee_job_type_id VARCHAR,
    employee_id VARCHAR,
    job_type_id VARCHAR,
    assignment_type ENUM,
    assignment_ratio DECIMAL DEFAULT 100.0,
    effective_start_date DATE,
    effective_end_date DATE,
    assignment_reason ENUM,
    assignment_status ENUM DEFAULT 'ACTIVE',
    proficiency_level ENUM DEFAULT 'NOVICE',
    target_proficiency_level ENUM,
    target_achievement_date DATE,
    certification_requirements TEXT,
    skill_requirements TEXT,
    experience_requirements TEXT,
    development_plan TEXT,
    training_plan TEXT,
    mentor_id VARCHAR,
    supervisor_id VARCHAR,
    performance_rating ENUM,
    last_evaluation_date DATE,
    next_evaluation_date DATE,
    evaluation_frequency ENUM DEFAULT 'QUARTERLY',
    career_path TEXT,
    strengths TEXT,
    improvement_areas TEXT,
    achievements TEXT,
    goals TEXT,
    workload_percentage DECIMAL DEFAULT 100.0,
    billable_flag BOOLEAN DEFAULT True,
    cost_center VARCHAR,
    budget_allocation DECIMAL,
    hourly_rate DECIMAL,
    overtime_eligible BOOLEAN DEFAULT True,
    remote_work_eligible BOOLEAN DEFAULT False,
    travel_required BOOLEAN DEFAULT False,
    security_clearance_required BOOLEAN DEFAULT False,
    created_by VARCHAR,
    approved_by VARCHAR,
    approval_date DATE,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_employee_job_type_id ON MST_EmployeeJobType (employee_job_type_id);
CREATE INDEX idx_employee_id ON MST_EmployeeJobType (employee_id);
CREATE INDEX idx_job_type_id ON MST_EmployeeJobType (job_type_id);
CREATE INDEX idx_employee_job_type ON MST_EmployeeJobType (employee_id, job_type_id);
CREATE INDEX idx_assignment_type ON MST_EmployeeJobType (assignment_type);
CREATE INDEX idx_assignment_status ON MST_EmployeeJobType (assignment_status);
CREATE INDEX idx_proficiency_level ON MST_EmployeeJobType (proficiency_level);
CREATE INDEX idx_effective_period ON MST_EmployeeJobType (effective_start_date, effective_end_date);
CREATE INDEX idx_mentor_id ON MST_EmployeeJobType (mentor_id);
CREATE INDEX idx_supervisor_id ON MST_EmployeeJobType (supervisor_id);
CREATE INDEX idx_performance_rating ON MST_EmployeeJobType (performance_rating);
