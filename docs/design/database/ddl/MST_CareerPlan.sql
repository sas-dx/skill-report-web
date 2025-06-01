-- MST_CareerPlan (目標・キャリアプラン) DDL
-- 生成日時: 2025-06-01 20:40:25

CREATE TABLE MST_CareerPlan (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    career_plan_id VARCHAR(50),
    employee_id VARCHAR(50),
    plan_name VARCHAR(200),
    plan_description TEXT,
    plan_type ENUM,
    target_position_id VARCHAR(50),
    target_job_type_id VARCHAR(50),
    target_department_id VARCHAR(50),
    current_level ENUM,
    target_level ENUM,
    plan_start_date DATE,
    plan_end_date DATE,
    milestone_1_date DATE,
    milestone_1_description VARCHAR(500),
    milestone_2_date DATE,
    milestone_2_description VARCHAR(500),
    milestone_3_date DATE,
    milestone_3_description VARCHAR(500),
    required_skills TEXT,
    required_certifications TEXT,
    required_experiences TEXT,
    development_actions TEXT,
    training_plan TEXT,
    mentor_id VARCHAR(50),
    supervisor_id VARCHAR(50),
    plan_status ENUM DEFAULT 'DRAFT',
    progress_percentage DECIMAL(5,2) DEFAULT 0.0,
    last_review_date DATE,
    next_review_date DATE,
    review_frequency ENUM DEFAULT 'QUARTERLY',
    success_criteria TEXT,
    risk_factors TEXT,
    support_resources TEXT,
    budget_allocated DECIMAL(10,2),
    budget_used DECIMAL(10,2) DEFAULT 0.0,
    priority_level ENUM DEFAULT 'NORMAL',
    visibility_level ENUM DEFAULT 'MANAGER',
    template_id VARCHAR(50),
    custom_fields TEXT,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_career_plan_id ON MST_CareerPlan (career_plan_id);
CREATE INDEX idx_employee_id ON MST_CareerPlan (employee_id);
CREATE INDEX idx_plan_type ON MST_CareerPlan (plan_type);
CREATE INDEX idx_target_position ON MST_CareerPlan (target_position_id);
CREATE INDEX idx_target_job_type ON MST_CareerPlan (target_job_type_id);
CREATE INDEX idx_plan_status ON MST_CareerPlan (plan_status);
CREATE INDEX idx_plan_period ON MST_CareerPlan (plan_start_date, plan_end_date);
CREATE INDEX idx_review_date ON MST_CareerPlan (next_review_date);
CREATE INDEX idx_mentor_id ON MST_CareerPlan (mentor_id);
CREATE INDEX idx_supervisor_id ON MST_CareerPlan (supervisor_id);
CREATE INDEX idx_priority_level ON MST_CareerPlan (priority_level);

-- 外部キー制約
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_target_position FOREIGN KEY (target_position_id) REFERENCES MST_Position(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_target_job_type FOREIGN KEY (target_job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_target_department FOREIGN KEY (target_department_id) REFERENCES MST_Department(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_mentor FOREIGN KEY (mentor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_supervisor FOREIGN KEY (supervisor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
