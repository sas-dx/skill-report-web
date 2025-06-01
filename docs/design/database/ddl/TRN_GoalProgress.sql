-- TRN_GoalProgress (目標進捗) DDL
-- 生成日時: 2025-06-01 20:40:26

CREATE TABLE TRN_GoalProgress (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    goal_id VARCHAR(50),
    employee_id VARCHAR(50),
    goal_title VARCHAR(200),
    goal_description TEXT,
    goal_category ENUM,
    goal_type ENUM,
    priority_level ENUM DEFAULT 'MEDIUM',
    target_value DECIMAL(15,2),
    current_value DECIMAL(15,2),
    unit VARCHAR(50),
    start_date DATE,
    target_date DATE,
    progress_rate DECIMAL(5,2) DEFAULT 0.0,
    achievement_status ENUM DEFAULT 'NOT_STARTED',
    supervisor_id VARCHAR(50),
    approval_status ENUM DEFAULT 'DRAFT',
    approved_at TIMESTAMP,
    approved_by VARCHAR(50),
    completion_date DATE,
    achievement_rate DECIMAL(5,2),
    self_evaluation INTEGER,
    supervisor_evaluation INTEGER,
    evaluation_comments TEXT,
    related_career_plan_id VARCHAR(50),
    related_skill_items TEXT,
    milestones TEXT,
    obstacles TEXT,
    support_needed TEXT,
    last_updated_at TIMESTAMP,
    next_review_date DATE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_TRN_GoalProgress_goal_id ON TRN_GoalProgress (goal_id);
CREATE INDEX idx_TRN_GoalProgress_employee_id ON TRN_GoalProgress (employee_id);
CREATE INDEX idx_TRN_GoalProgress_supervisor_id ON TRN_GoalProgress (supervisor_id);
CREATE INDEX idx_TRN_GoalProgress_category ON TRN_GoalProgress (goal_category);
CREATE INDEX idx_TRN_GoalProgress_status ON TRN_GoalProgress (achievement_status);
CREATE INDEX idx_TRN_GoalProgress_approval_status ON TRN_GoalProgress (approval_status);
CREATE INDEX idx_TRN_GoalProgress_target_date ON TRN_GoalProgress (target_date);
CREATE INDEX idx_TRN_GoalProgress_priority ON TRN_GoalProgress (priority_level);
CREATE INDEX idx_TRN_GoalProgress_employee_period ON TRN_GoalProgress (employee_id, start_date, target_date);
CREATE INDEX idx_TRN_GoalProgress_next_review ON TRN_GoalProgress (next_review_date);

-- 外部キー制約
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_supervisor FOREIGN KEY (supervisor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_approved_by FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_career_plan FOREIGN KEY (related_career_plan_id) REFERENCES MST_CareerPlan(id) ON UPDATE CASCADE ON DELETE SET NULL;
