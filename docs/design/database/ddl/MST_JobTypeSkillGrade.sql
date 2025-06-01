-- MST_JobTypeSkillGrade (職種スキルグレード関連) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_JobTypeSkillGrade (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    job_type_id VARCHAR(50),
    skill_grade_id VARCHAR(50),
    grade_requirement_type ENUM DEFAULT 'STANDARD',
    required_experience_years DECIMAL(4,1),
    promotion_criteria TEXT,
    salary_range_min DECIMAL(10,0),
    salary_range_max DECIMAL(10,0),
    performance_expectations TEXT,
    leadership_requirements TEXT,
    technical_depth INTEGER,
    business_impact INTEGER,
    team_size_expectation INTEGER,
    certification_requirements TEXT,
    grade_status ENUM DEFAULT 'ACTIVE',
    effective_date DATE,
    expiry_date DATE,
    next_grade_path TEXT,
    evaluation_frequency ENUM DEFAULT 'ANNUAL',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE INDEX idx_MST_JobTypeSkillGrade_job_type_id ON MST_JobTypeSkillGrade (job_type_id);
CREATE INDEX idx_MST_JobTypeSkillGrade_skill_grade_id ON MST_JobTypeSkillGrade (skill_grade_id);
CREATE UNIQUE INDEX idx_MST_JobTypeSkillGrade_job_grade ON MST_JobTypeSkillGrade (job_type_id, skill_grade_id);
CREATE INDEX idx_MST_JobTypeSkillGrade_requirement_type ON MST_JobTypeSkillGrade (grade_requirement_type);
CREATE INDEX idx_MST_JobTypeSkillGrade_experience_years ON MST_JobTypeSkillGrade (required_experience_years);
CREATE INDEX idx_MST_JobTypeSkillGrade_status ON MST_JobTypeSkillGrade (grade_status);
CREATE INDEX idx_MST_JobTypeSkillGrade_effective_date ON MST_JobTypeSkillGrade (effective_date);
CREATE INDEX idx_MST_JobTypeSkillGrade_technical_depth ON MST_JobTypeSkillGrade (technical_depth);

-- 外部キー制約
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT fk_MST_JobTypeSkillGrade_job_type FOREIGN KEY (job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT fk_MST_JobTypeSkillGrade_skill_grade FOREIGN KEY (skill_grade_id) REFERENCES MST_SkillGrade(id) ON UPDATE CASCADE ON DELETE CASCADE;
