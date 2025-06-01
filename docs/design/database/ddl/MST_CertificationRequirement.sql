-- MST_CertificationRequirement (資格要件マスタ) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_CertificationRequirement (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    requirement_id VARCHAR(50),
    requirement_name VARCHAR(200),
    requirement_description TEXT,
    requirement_type ENUM,
    target_job_type_id VARCHAR(50),
    target_position_id VARCHAR(50),
    target_skill_grade_id VARCHAR(50),
    target_department_id VARCHAR(50),
    certification_id VARCHAR(50),
    requirement_level ENUM,
    priority_order INTEGER DEFAULT 1,
    alternative_certifications TEXT,
    minimum_experience_years INTEGER,
    minimum_skill_level ENUM,
    grace_period_months INTEGER,
    renewal_required BOOLEAN DEFAULT False,
    renewal_interval_months INTEGER,
    exemption_conditions TEXT,
    assessment_criteria TEXT,
    business_justification TEXT,
    compliance_requirement BOOLEAN DEFAULT False,
    client_requirement BOOLEAN DEFAULT False,
    internal_policy BOOLEAN DEFAULT False,
    effective_start_date DATE,
    effective_end_date DATE,
    notification_timing INTEGER,
    escalation_timing INTEGER,
    cost_support_available BOOLEAN DEFAULT False,
    cost_support_amount DECIMAL(10,2),
    cost_support_conditions TEXT,
    training_support_available BOOLEAN DEFAULT False,
    recommended_training_programs TEXT,
    study_time_allocation DECIMAL(5,2),
    success_rate DECIMAL(5,2),
    average_study_hours DECIMAL(6,2),
    difficulty_rating ENUM,
    active_flag BOOLEAN DEFAULT True,
    created_by VARCHAR(50),
    approved_by VARCHAR(50),
    approval_date DATE,
    review_date DATE,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_requirement_id ON MST_CertificationRequirement (requirement_id);
CREATE INDEX idx_requirement_type ON MST_CertificationRequirement (requirement_type);
CREATE INDEX idx_target_job_type ON MST_CertificationRequirement (target_job_type_id);
CREATE INDEX idx_target_position ON MST_CertificationRequirement (target_position_id);
CREATE INDEX idx_target_skill_grade ON MST_CertificationRequirement (target_skill_grade_id);
CREATE INDEX idx_certification_id ON MST_CertificationRequirement (certification_id);
CREATE INDEX idx_requirement_level ON MST_CertificationRequirement (requirement_level);
CREATE INDEX idx_active_flag ON MST_CertificationRequirement (active_flag);
CREATE INDEX idx_effective_period ON MST_CertificationRequirement (effective_start_date, effective_end_date);
CREATE INDEX idx_compliance_requirement ON MST_CertificationRequirement (compliance_requirement);
CREATE INDEX idx_priority_order ON MST_CertificationRequirement (priority_order);

-- 外部キー制約
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_job_type FOREIGN KEY (target_job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_position FOREIGN KEY (target_position_id) REFERENCES MST_Position(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_skill_grade FOREIGN KEY (target_skill_grade_id) REFERENCES MST_SkillGrade(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_department FOREIGN KEY (target_department_id) REFERENCES MST_Department(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_certification FOREIGN KEY (certification_id) REFERENCES MST_Certification(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_created_by FOREIGN KEY (created_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_approved_by FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
