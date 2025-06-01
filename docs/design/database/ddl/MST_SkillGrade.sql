-- MST_SkillGrade (スキルグレードマスタ) DDL
-- 生成日時: 2025-06-01 16:05:54

CREATE TABLE MST_SkillGrade (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    grade_code VARCHAR(20),
    grade_name VARCHAR(50),
    grade_name_short VARCHAR(10),
    grade_level INTEGER,
    description TEXT,
    evaluation_criteria TEXT,
    required_experience_months INTEGER,
    skill_indicators TEXT,
    competency_requirements TEXT,
    certification_requirements TEXT,
    project_complexity ENUM,
    mentoring_capability BOOLEAN DEFAULT False,
    leadership_level ENUM,
    salary_impact_factor DECIMAL(3,2),
    promotion_eligibility BOOLEAN DEFAULT False,
    color_code VARCHAR(7),
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT True,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_grade_code ON MST_SkillGrade (grade_code);
CREATE UNIQUE INDEX idx_grade_level ON MST_SkillGrade (grade_level);
CREATE INDEX idx_grade_name ON MST_SkillGrade (grade_name);
CREATE INDEX idx_mentoring ON MST_SkillGrade (mentoring_capability, is_active);
CREATE INDEX idx_promotion ON MST_SkillGrade (promotion_eligibility, is_active);
CREATE INDEX idx_sort_order ON MST_SkillGrade (sort_order);

-- 外部キー制約
