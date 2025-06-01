-- MST_EmployeeJobType (社員職種関連) DDL
-- 生成日時: 2025-06-01 17:03:29

CREATE TABLE MST_EmployeeJobType (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    employee_job_type_id VARCHAR(50) NOT NULL,
    employee_id VARCHAR(50) NOT NULL,
    job_type_id VARCHAR(50) NOT NULL,
    assignment_type ENUM('PRIMARY', 'SECONDARY', 'TEMPORARY', 'TRAINING', 'CANDIDATE') NOT NULL,
    assignment_ratio DECIMAL(5,2) NOT NULL DEFAULT 100.00,
    effective_start_date DATE NOT NULL,
    effective_end_date DATE,
    assignment_reason ENUM('NEW_HIRE', 'PROMOTION', 'TRANSFER', 'SKILL_DEVELOPMENT', 'PROJECT_NEED', 'REORGANIZATION') NOT NULL,
    assignment_status ENUM('ACTIVE', 'INACTIVE', 'PENDING', 'SUSPENDED') NOT NULL DEFAULT 'ACTIVE',
    proficiency_level ENUM('NOVICE', 'BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT') NOT NULL DEFAULT 'NOVICE',
    target_proficiency_level ENUM('NOVICE', 'BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT'),
    target_achievement_date DATE,
    certification_requirements TEXT,
    skill_requirements TEXT,
    experience_requirements TEXT,
    development_plan TEXT,
    training_plan TEXT,
    mentor_id VARCHAR(50),
    supervisor_id VARCHAR(50),
    performance_rating ENUM('EXCELLENT', 'GOOD', 'SATISFACTORY', 'NEEDS_IMPROVEMENT', 'UNSATISFACTORY'),
    last_evaluation_date DATE,
    next_evaluation_date DATE,
    evaluation_frequency ENUM('MONTHLY', 'QUARTERLY', 'SEMI_ANNUAL', 'ANNUAL') NOT NULL DEFAULT 'QUARTERLY',
    career_path TEXT,
    strengths TEXT,
    improvement_areas TEXT,
    achievements TEXT,
    goals TEXT,
    workload_percentage DECIMAL(5,2) NOT NULL DEFAULT 100.00,
    billable_flag BOOLEAN NOT NULL DEFAULT true,
    cost_center VARCHAR(20),
    budget_allocation DECIMAL(10,2),
    hourly_rate DECIMAL(8,2),
    overtime_eligible BOOLEAN NOT NULL DEFAULT true,
    remote_work_eligible BOOLEAN NOT NULL DEFAULT false,
    travel_required BOOLEAN NOT NULL DEFAULT false,
    security_clearance_required BOOLEAN NOT NULL DEFAULT false,
    approved_by VARCHAR(50),
    approval_date DATE,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

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

-- 制約追加
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT uk_employee_job_type_id UNIQUE (employee_job_type_id);
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_assignment_ratio_range CHECK (assignment_ratio >= 0 AND assignment_ratio <= 100);
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_workload_percentage_range CHECK (workload_percentage >= 0 AND workload_percentage <= 100);
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_effective_period CHECK (effective_end_date IS NULL OR effective_start_date <= effective_end_date);
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_budget_allocation_positive CHECK (budget_allocation IS NULL OR budget_allocation >= 0);
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_hourly_rate_positive CHECK (hourly_rate IS NULL OR hourly_rate >= 0);

-- 外部キー制約
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_job_type FOREIGN KEY (job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_mentor FOREIGN KEY (mentor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_supervisor FOREIGN KEY (supervisor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_created_by FOREIGN KEY (created_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_approved_by FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
