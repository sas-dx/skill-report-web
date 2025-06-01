-- MST_EmployeeJobType (社員職種関連) DDL
-- 生成日時: 2025-06-01 20:40:25

CREATE TABLE MST_EmployeeJobType (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    employee_job_type_id VARCHAR(50),
    employee_id VARCHAR(50),
    job_type_id VARCHAR(50),
    assignment_type ENUM,
    assignment_ratio DECIMAL(5,2) DEFAULT 100.0,
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
    mentor_id VARCHAR(50),
    supervisor_id VARCHAR(50),
    performance_rating ENUM,
    last_evaluation_date DATE,
    next_evaluation_date DATE,
    evaluation_frequency ENUM DEFAULT 'QUARTERLY',
    career_path TEXT,
    strengths TEXT,
    improvement_areas TEXT,
    achievements TEXT,
    goals TEXT,
    workload_percentage DECIMAL(5,2) DEFAULT 100.0,
    billable_flag BOOLEAN DEFAULT True,
    cost_center VARCHAR(20),
    budget_allocation DECIMAL(10,2),
    hourly_rate DECIMAL(8,2),
    overtime_eligible BOOLEAN DEFAULT True,
    remote_work_eligible BOOLEAN DEFAULT False,
    travel_required BOOLEAN DEFAULT False,
    security_clearance_required BOOLEAN DEFAULT False,
    created_by VARCHAR(50),
    approved_by VARCHAR(50),
    approval_date DATE,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

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

-- 外部キー制約
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_job_type FOREIGN KEY (job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_mentor FOREIGN KEY (mentor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_supervisor FOREIGN KEY (supervisor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_created_by FOREIGN KEY (created_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_approved_by FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
