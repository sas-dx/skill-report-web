-- TRN_ProjectRecord (案件実績) DDL
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE TRN_ProjectRecord (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    project_record_id VARCHAR(50),
    employee_id VARCHAR(50),
    project_name VARCHAR(200),
    project_code VARCHAR(50),
    client_name VARCHAR(100),
    project_type ENUM,
    project_scale ENUM,
    start_date DATE,
    end_date DATE,
    participation_rate DECIMAL(5,2),
    role_title VARCHAR(100),
    responsibilities TEXT,
    technologies_used TEXT,
    skills_applied TEXT,
    achievements TEXT,
    challenges_faced TEXT,
    lessons_learned TEXT,
    team_size INTEGER,
    budget_range ENUM,
    project_status ENUM DEFAULT 'ONGOING',
    evaluation_score DECIMAL(3,1),
    evaluation_comment TEXT,
    is_confidential BOOLEAN DEFAULT False,
    is_public_reference BOOLEAN DEFAULT False,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_project_record_id ON TRN_ProjectRecord (project_record_id);
CREATE INDEX idx_employee_id ON TRN_ProjectRecord (employee_id);
CREATE INDEX idx_project_name ON TRN_ProjectRecord (project_name);
CREATE INDEX idx_project_code ON TRN_ProjectRecord (project_code);
CREATE INDEX idx_project_type ON TRN_ProjectRecord (project_type);
CREATE INDEX idx_date_range ON TRN_ProjectRecord (start_date, end_date);
CREATE INDEX idx_project_status ON TRN_ProjectRecord (project_status);
CREATE INDEX idx_employee_period ON TRN_ProjectRecord (employee_id, start_date, end_date);

-- 外部キー制約
ALTER TABLE TRN_ProjectRecord ADD CONSTRAINT fk_project_record_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
