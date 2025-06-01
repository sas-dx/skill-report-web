-- MST_SkillGradeRequirement (スキルグレード要件) DDL
-- 生成日時: 2025-06-01 20:40:25

CREATE TABLE MST_SkillGradeRequirement (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    skill_grade_id VARCHAR(50),
    requirement_category ENUM,
    requirement_name VARCHAR(200),
    requirement_description TEXT,
    evaluation_criteria TEXT,
    proficiency_level INTEGER,
    weight_percentage DECIMAL(5,2),
    minimum_score DECIMAL(5,2),
    evidence_requirements TEXT,
    learning_resources TEXT,
    prerequisite_requirements TEXT,
    assessment_method ENUM,
    assessment_frequency ENUM DEFAULT 'ANNUAL',
    validity_period INTEGER,
    certification_mapping TEXT,
    requirement_status ENUM DEFAULT 'ACTIVE',
    effective_date DATE,
    expiry_date DATE,
    revision_notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE INDEX idx_MST_SkillGradeRequirement_skill_grade_id ON MST_SkillGradeRequirement (skill_grade_id);
CREATE INDEX idx_MST_SkillGradeRequirement_category ON MST_SkillGradeRequirement (requirement_category);
CREATE INDEX idx_MST_SkillGradeRequirement_grade_category ON MST_SkillGradeRequirement (skill_grade_id, requirement_category);
CREATE INDEX idx_MST_SkillGradeRequirement_proficiency_level ON MST_SkillGradeRequirement (proficiency_level);
CREATE INDEX idx_MST_SkillGradeRequirement_assessment_method ON MST_SkillGradeRequirement (assessment_method);
CREATE INDEX idx_MST_SkillGradeRequirement_status ON MST_SkillGradeRequirement (requirement_status);
CREATE INDEX idx_MST_SkillGradeRequirement_effective_date ON MST_SkillGradeRequirement (effective_date);
CREATE INDEX idx_MST_SkillGradeRequirement_weight ON MST_SkillGradeRequirement (weight_percentage);

-- 外部キー制約
ALTER TABLE MST_SkillGradeRequirement ADD CONSTRAINT fk_MST_SkillGradeRequirement_skill_grade FOREIGN KEY (skill_grade_id) REFERENCES MST_SkillGrade(id) ON UPDATE CASCADE ON DELETE CASCADE;
