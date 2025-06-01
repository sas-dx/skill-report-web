-- MST_JobTypeSkill (職種スキル関連) DDL
-- 生成日時: 2025-06-01 20:40:25

CREATE TABLE MST_JobTypeSkill (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    job_type_id VARCHAR(50),
    skill_item_id VARCHAR(50),
    required_level INTEGER,
    skill_priority ENUM DEFAULT 'MEDIUM',
    skill_category ENUM,
    experience_years DECIMAL(4,1),
    certification_required BOOLEAN DEFAULT False,
    skill_weight DECIMAL(5,2),
    evaluation_criteria TEXT,
    learning_path TEXT,
    skill_status ENUM DEFAULT 'ACTIVE',
    effective_date DATE,
    expiry_date DATE,
    alternative_skills TEXT,
    prerequisite_skills TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE INDEX idx_MST_JobTypeSkill_job_type_id ON MST_JobTypeSkill (job_type_id);
CREATE INDEX idx_MST_JobTypeSkill_skill_item_id ON MST_JobTypeSkill (skill_item_id);
CREATE UNIQUE INDEX idx_MST_JobTypeSkill_job_skill ON MST_JobTypeSkill (job_type_id, skill_item_id);
CREATE INDEX idx_MST_JobTypeSkill_required_level ON MST_JobTypeSkill (required_level);
CREATE INDEX idx_MST_JobTypeSkill_priority ON MST_JobTypeSkill (skill_priority);
CREATE INDEX idx_MST_JobTypeSkill_category ON MST_JobTypeSkill (skill_category);
CREATE INDEX idx_MST_JobTypeSkill_status ON MST_JobTypeSkill (skill_status);
CREATE INDEX idx_MST_JobTypeSkill_effective_date ON MST_JobTypeSkill (effective_date);

-- 外部キー制約
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT fk_MST_JobTypeSkill_job_type FOREIGN KEY (job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT fk_MST_JobTypeSkill_skill_item FOREIGN KEY (skill_item_id) REFERENCES MST_SkillItem(id) ON UPDATE CASCADE ON DELETE CASCADE;
