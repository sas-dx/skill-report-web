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

-- 作成日: 2025-06-24 23:02:18
-- ============================================

DROP TABLE IF EXISTS MST_EmployeeJobType;

CREATE TABLE MST_EmployeeJobType (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    achievements TEXT COMMENT '実績',
    approval_date DATE COMMENT '承認日',
    approved_by VARCHAR(50) COMMENT '承認者',
    assignment_ratio DECIMAL(5,2) DEFAULT 100.0 COMMENT '配属比率',
    assignment_reason ENUM('NEW_HIRE', 'PROMOTION', 'TRANSFER', 'SKILL_DEVELOPMENT', 'PROJECT_NEED', 'REORGANIZATION') COMMENT '配属理由',
    assignment_status ENUM('ACTIVE', 'INACTIVE', 'PENDING', 'SUSPENDED') DEFAULT 'ACTIVE' COMMENT '配属状況',
    assignment_type ENUM('PRIMARY', 'SECONDARY', 'TEMPORARY', 'TRAINING', 'CANDIDATE') COMMENT '配属種別',
    billable_flag BOOLEAN DEFAULT True COMMENT '請求対象フラグ',
    budget_allocation DECIMAL(10,2) COMMENT '予算配分',
    career_path TEXT COMMENT 'キャリアパス',
    certification_requirements TEXT COMMENT '必要資格',
    cost_center VARCHAR(20) COMMENT 'コストセンター',
    created_by VARCHAR(50) COMMENT '作成者',
    development_plan TEXT COMMENT '育成計画',
    effective_end_date DATE COMMENT '有効終了日',
    effective_start_date DATE COMMENT '有効開始日',
    employee_id VARCHAR(50) COMMENT '社員ID',
    employee_job_type_id VARCHAR(50) COMMENT '社員職種関連ID',
    employeejobtype_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_EmployeeJobTypeの主キー',
    evaluation_frequency ENUM('MONTHLY', 'QUARTERLY', 'SEMI_ANNUAL', 'ANNUAL') DEFAULT 'QUARTERLY' COMMENT '評価頻度',
    experience_requirements TEXT COMMENT '必要経験',
    goals TEXT COMMENT '目標',
    hourly_rate DECIMAL(8,2) COMMENT '時間単価',
    improvement_areas TEXT COMMENT '改善領域',
    job_type_id VARCHAR(50) COMMENT '職種ID',
    last_evaluation_date DATE COMMENT '最終評価日',
    mentor_id VARCHAR(50) COMMENT 'メンターID',
    next_evaluation_date DATE COMMENT '次回評価日',
    notes TEXT COMMENT '備考',
    overtime_eligible BOOLEAN DEFAULT True COMMENT '残業対象フラグ',
    performance_rating ENUM('EXCELLENT', 'GOOD', 'SATISFACTORY', 'NEEDS_IMPROVEMENT', 'UNSATISFACTORY') COMMENT 'パフォーマンス評価',
    proficiency_level ENUM('NOVICE', 'BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT') DEFAULT 'NOVICE' COMMENT '習熟度',
    remote_work_eligible BOOLEAN DEFAULT False COMMENT 'リモートワーク可否',
    security_clearance_required BOOLEAN DEFAULT False COMMENT 'セキュリティクリアランス要否',
    skill_requirements TEXT COMMENT '必要スキル',
    strengths TEXT COMMENT '強み',
    supervisor_id VARCHAR(50) COMMENT '上司ID',
    target_achievement_date DATE COMMENT '目標達成日',
    target_proficiency_level ENUM('NOVICE', 'BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT') COMMENT '目標習熟度',
    training_plan TEXT COMMENT '研修計画',
    travel_required BOOLEAN DEFAULT False COMMENT '出張要否',
    workload_percentage DECIMAL(5,2) DEFAULT 100.0 COMMENT '業務負荷率',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
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
CREATE INDEX idx_mst_employeejobtype_tenant_id ON MST_EmployeeJobType (tenant_id);

-- 外部キー制約
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_job_type FOREIGN KEY (job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_mentor FOREIGN KEY (mentor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_supervisor FOREIGN KEY (supervisor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_created_by FOREIGN KEY (created_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_approved_by FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
-- 制約DDL生成エラー: uk_employee_job_type_id
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_assignment_type CHECK (assignment_type IN ('PRIMARY', 'SECONDARY', 'TEMPORARY', 'TRAINING', 'CANDIDATE'));
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_assignment_status CHECK (assignment_status IN ('ACTIVE', 'INACTIVE', 'PENDING', 'SUSPENDED'));
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_proficiency_level CHECK (proficiency_level IN ('NOVICE', 'BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT'));
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_target_proficiency_level CHECK (target_proficiency_level IN ('NOVICE', 'BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT'));
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_assignment_reason CHECK (assignment_reason IN ('NEW_HIRE', 'PROMOTION', 'TRANSFER', 'SKILL_DEVELOPMENT', 'PROJECT_NEED', 'REORGANIZATION'));
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_performance_rating CHECK (performance_rating IN ('EXCELLENT', 'GOOD', 'SATISFACTORY', 'NEEDS_IMPROVEMENT', 'UNSATISFACTORY'));
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_evaluation_frequency CHECK (evaluation_frequency IN ('MONTHLY', 'QUARTERLY', 'SEMI_ANNUAL', 'ANNUAL'));
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_assignment_ratio_range CHECK (assignment_ratio >= 0 AND assignment_ratio <= 100);
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_workload_percentage_range CHECK (workload_percentage >= 0 AND workload_percentage <= 100);
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_effective_period CHECK (effective_end_date IS NULL OR effective_start_date <= effective_end_date);
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_budget_allocation_positive CHECK (budget_allocation IS NULL OR budget_allocation >= 0);
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_hourly_rate_positive CHECK (hourly_rate IS NULL OR hourly_rate >= 0);
