-- TRN_SkillRecord (スキル情報) DDL
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE TRN_SkillRecord (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    employee_id VARCHAR(50),
    skill_item_id VARCHAR(50),
    skill_level INT,
    self_assessment INT,
    manager_assessment INT,
    evidence_description TEXT,
    acquisition_date DATE,
    last_used_date DATE,
    expiry_date DATE,
    certification_id VARCHAR(50),
    skill_category_id VARCHAR(50),
    assessment_date DATE,
    assessor_id VARCHAR(50),
    skill_status ENUM DEFAULT 'ACTIVE',
    learning_hours INT,
    project_experience_count INT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_employee_skill ON TRN_SkillRecord (employee_id, skill_item_id);
CREATE INDEX idx_employee ON TRN_SkillRecord (employee_id);
CREATE INDEX idx_skill_item ON TRN_SkillRecord (skill_item_id);
CREATE INDEX idx_skill_level ON TRN_SkillRecord (skill_level);
CREATE INDEX idx_skill_category ON TRN_SkillRecord (skill_category_id);
CREATE INDEX idx_certification ON TRN_SkillRecord (certification_id);
CREATE INDEX idx_status ON TRN_SkillRecord (skill_status);
CREATE INDEX idx_expiry_date ON TRN_SkillRecord (expiry_date);
CREATE INDEX idx_assessment_date ON TRN_SkillRecord (assessment_date);

-- 外部キー制約
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_item FOREIGN KEY (skill_item_id) REFERENCES MST_SkillItem(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_certification FOREIGN KEY (certification_id) REFERENCES MST_Certification(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_category FOREIGN KEY (skill_category_id) REFERENCES MST_SkillCategory(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_assessor FOREIGN KEY (assessor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
