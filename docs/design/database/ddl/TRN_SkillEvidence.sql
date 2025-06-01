-- TRN_SkillEvidence (スキル証跡) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE TRN_SkillEvidence (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    evidence_id VARCHAR(50),
    employee_id VARCHAR(50),
    skill_id VARCHAR(50),
    evidence_type ENUM,
    evidence_title VARCHAR(200),
    evidence_description TEXT,
    skill_level_demonstrated ENUM,
    evidence_date DATE,
    validity_start_date DATE,
    validity_end_date DATE,
    file_path VARCHAR(500),
    file_type ENUM,
    file_size_kb INTEGER,
    external_url VARCHAR(500),
    issuer_name VARCHAR(100),
    issuer_type ENUM,
    certificate_number VARCHAR(100),
    verification_method ENUM,
    verification_status ENUM DEFAULT 'PENDING',
    verified_by VARCHAR(50),
    verification_date DATE,
    verification_comment TEXT,
    related_project_id VARCHAR(50),
    related_training_id VARCHAR(50),
    related_certification_id VARCHAR(50),
    impact_score DECIMAL(3,1),
    complexity_level ENUM,
    team_size INTEGER,
    role_in_activity VARCHAR(100),
    technologies_used TEXT,
    achievements TEXT,
    lessons_learned TEXT,
    is_public BOOLEAN DEFAULT False,
    is_portfolio_item BOOLEAN DEFAULT False,
    tags TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_evidence_id ON TRN_SkillEvidence (evidence_id);
CREATE INDEX idx_employee_id ON TRN_SkillEvidence (employee_id);
CREATE INDEX idx_skill_id ON TRN_SkillEvidence (skill_id);
CREATE INDEX idx_evidence_type ON TRN_SkillEvidence (evidence_type);
CREATE INDEX idx_skill_level ON TRN_SkillEvidence (skill_level_demonstrated);
CREATE INDEX idx_evidence_date ON TRN_SkillEvidence (evidence_date);
CREATE INDEX idx_verification_status ON TRN_SkillEvidence (verification_status);
CREATE INDEX idx_validity_period ON TRN_SkillEvidence (validity_start_date, validity_end_date);
CREATE INDEX idx_employee_skill ON TRN_SkillEvidence (employee_id, skill_id, verification_status);
CREATE INDEX idx_portfolio ON TRN_SkillEvidence (is_portfolio_item, is_public);

-- 外部キー制約
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_skill FOREIGN KEY (skill_id) REFERENCES MST_SkillItem(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_verifier FOREIGN KEY (verified_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_project FOREIGN KEY (related_project_id) REFERENCES TRN_ProjectRecord(project_record_id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_training FOREIGN KEY (related_training_id) REFERENCES TRN_TrainingHistory(training_history_id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_certification FOREIGN KEY (related_certification_id) REFERENCES MST_Certification(id) ON UPDATE CASCADE ON DELETE SET NULL;
