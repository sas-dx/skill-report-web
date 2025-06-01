-- 全テーブル統合DDL
-- 生成日時: 2025-06-01 16:05:54

-- MST_SkillHierarchy (スキル階層マスタ) DDL
-- 生成日時: 2025-06-01 16:05:54

CREATE TABLE MST_SkillHierarchy (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    skill_id VARCHAR(50),
    parent_skill_id VARCHAR(50),
    hierarchy_level INTEGER,
    skill_path VARCHAR(500),
    sort_order INTEGER DEFAULT 0,
    is_leaf BOOLEAN DEFAULT True,
    skill_category ENUM,
    description TEXT,
    is_active BOOLEAN DEFAULT True,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE INDEX idx_skill_id ON MST_SkillHierarchy (skill_id);
CREATE INDEX idx_parent_skill ON MST_SkillHierarchy (parent_skill_id);
CREATE INDEX idx_hierarchy_level ON MST_SkillHierarchy (hierarchy_level);
CREATE INDEX idx_skill_path ON MST_SkillHierarchy (skill_path);
CREATE INDEX idx_category_level ON MST_SkillHierarchy (skill_category, hierarchy_level);
CREATE INDEX idx_parent_sort ON MST_SkillHierarchy (parent_skill_id, sort_order);

-- 外部キー制約
ALTER TABLE MST_SkillHierarchy ADD CONSTRAINT fk_hierarchy_skill FOREIGN KEY (skill_id) REFERENCES MST_SkillItem(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_SkillHierarchy ADD CONSTRAINT fk_hierarchy_parent FOREIGN KEY (parent_skill_id) REFERENCES MST_SkillHierarchy(skill_id) ON UPDATE CASCADE ON DELETE CASCADE;


-- MST_Certification (資格情報) DDL
-- 生成日時: 2025-06-01 16:05:54

CREATE TABLE MST_Certification (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    certification_code VARCHAR(50),
    certification_name VARCHAR(200),
    certification_name_en VARCHAR(200),
    issuer VARCHAR(100),
    issuer_country VARCHAR(10),
    certification_category ENUM,
    certification_level ENUM,
    validity_period_months INTEGER,
    renewal_required BOOLEAN DEFAULT False,
    renewal_requirements TEXT,
    exam_fee DECIMAL(10,2),
    exam_language VARCHAR(50),
    exam_format ENUM,
    official_url VARCHAR(500),
    description TEXT,
    skill_category_id VARCHAR(50),
    is_recommended BOOLEAN DEFAULT False,
    is_active BOOLEAN DEFAULT True,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_certification_code ON MST_Certification (certification_code);
CREATE INDEX idx_certification_name ON MST_Certification (certification_name);
CREATE INDEX idx_issuer ON MST_Certification (issuer);
CREATE INDEX idx_category_level ON MST_Certification (certification_category, certification_level);
CREATE INDEX idx_recommended ON MST_Certification (is_recommended, is_active);
CREATE INDEX idx_skill_category ON MST_Certification (skill_category_id);

-- 外部キー制約
ALTER TABLE MST_Certification ADD CONSTRAINT fk_certification_skill_category FOREIGN KEY (skill_category_id) REFERENCES MST_SkillCategory(id) ON UPDATE CASCADE ON DELETE SET NULL;


-- MST_SystemConfig (システム設定) DDL
-- 生成日時: 2025-06-01 16:05:54

CREATE TABLE MST_SystemConfig (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    config_key VARCHAR(100),
    config_name VARCHAR(200),
    config_value TEXT,
    config_type ENUM,
    config_category ENUM,
    default_value TEXT,
    validation_rule TEXT,
    description TEXT,
    is_encrypted BOOLEAN DEFAULT False,
    is_system_only BOOLEAN DEFAULT False,
    is_user_configurable BOOLEAN DEFAULT True,
    requires_restart BOOLEAN DEFAULT False,
    environment ENUM DEFAULT 'ALL',
    tenant_specific BOOLEAN DEFAULT False,
    last_modified_by VARCHAR(50),
    last_modified_reason TEXT,
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT True,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_config_key ON MST_SystemConfig (config_key);
CREATE INDEX idx_config_category ON MST_SystemConfig (config_category);
CREATE INDEX idx_config_type ON MST_SystemConfig (config_type);
CREATE INDEX idx_user_configurable ON MST_SystemConfig (is_user_configurable, is_active);
CREATE INDEX idx_environment ON MST_SystemConfig (environment, is_active);
CREATE INDEX idx_tenant_specific ON MST_SystemConfig (tenant_specific, is_active);
CREATE INDEX idx_sort_order ON MST_SystemConfig (sort_order);

-- 外部キー制約


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
