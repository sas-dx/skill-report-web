-- MST_JobType (職種マスタ) DDL
-- 生成日時: 2025-06-01 16:05:54

CREATE TABLE MST_JobType (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    job_type_code VARCHAR(20),
    job_type_name VARCHAR(100),
    job_type_name_en VARCHAR(100),
    job_category ENUM,
    job_level ENUM,
    description TEXT,
    required_experience_years INTEGER,
    salary_grade_min INTEGER,
    salary_grade_max INTEGER,
    career_path TEXT,
    required_certifications TEXT,
    required_skills TEXT,
    department_affinity TEXT,
    remote_work_eligible BOOLEAN DEFAULT False,
    travel_frequency ENUM,
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT True,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_job_type_code ON MST_JobType (job_type_code);
CREATE INDEX idx_job_type_name ON MST_JobType (job_type_name);
CREATE INDEX idx_job_category ON MST_JobType (job_category);
CREATE INDEX idx_job_level ON MST_JobType (job_level);
CREATE INDEX idx_category_level ON MST_JobType (job_category, job_level);
CREATE INDEX idx_remote_eligible ON MST_JobType (remote_work_eligible, is_active);
CREATE INDEX idx_sort_order ON MST_JobType (sort_order);

-- 外部キー制約
