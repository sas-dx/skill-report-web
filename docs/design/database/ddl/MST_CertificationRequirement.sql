-- MST_CertificationRequirement (資格要件マスタ) DDL
-- 生成日時: 2025-06-01 17:02:53

CREATE TABLE MST_CertificationRequirement (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    requirement_id VARCHAR(50) NOT NULL,
    requirement_name VARCHAR(200) NOT NULL,
    requirement_description TEXT,
    requirement_type ENUM('JOB_TYPE', 'POSITION', 'SKILL_GRADE', 'PROJECT', 'PROMOTION') NOT NULL,
    target_job_type_id VARCHAR(50),
    target_position_id VARCHAR(50),
    target_skill_grade_id VARCHAR(50),
    target_department_id VARCHAR(50),
    certification_id VARCHAR(50) NOT NULL,
    requirement_level ENUM('MANDATORY', 'PREFERRED', 'OPTIONAL', 'DISQUALIFYING') NOT NULL,
    priority_order INTEGER NOT NULL DEFAULT 1,
    alternative_certifications TEXT,
    minimum_experience_years INTEGER,
    minimum_skill_level ENUM('BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT'),
    grace_period_months INTEGER,
    renewal_required BOOLEAN NOT NULL DEFAULT false,
    renewal_interval_months INTEGER,
    exemption_conditions TEXT,
    assessment_criteria TEXT,
    business_justification TEXT,
    compliance_requirement BOOLEAN NOT NULL DEFAULT false,
    client_requirement BOOLEAN NOT NULL DEFAULT false,
    internal_policy BOOLEAN NOT NULL DEFAULT false,
    effective_start_date DATE NOT NULL,
    effective_end_date DATE,
    notification_timing INTEGER,
    escalation_timing INTEGER,
    cost_support_available BOOLEAN NOT NULL DEFAULT false,
    cost_support_amount DECIMAL(10,2),
    cost_support_conditions TEXT,
    training_support_available BOOLEAN NOT NULL DEFAULT false,
    recommended_training_programs TEXT,
    study_time_allocation DECIMAL(5,2),
    success_rate DECIMAL(5,2),
    average_study_hours DECIMAL(6,2),
    difficulty_rating ENUM('EASY', 'MEDIUM', 'HARD', 'VERY_HARD'),
    active_flag BOOLEAN NOT NULL DEFAULT true,
    approved_by VARCHAR(50),
    approval_date DATE,
    review_date DATE,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

-- インデックス作成
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

-- 制約追加
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT uk_requirement_id UNIQUE (requirement_id);
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT chk_priority_order_positive CHECK (priority_order > 0);
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT chk_experience_years_positive CHECK (minimum_experience_years IS NULL OR minimum_experience_years >= 0);
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT chk_grace_period_positive CHECK (grace_period_months IS NULL OR grace_period_months > 0);
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT chk_renewal_interval_positive CHECK (renewal_interval_months IS NULL OR renewal_interval_months > 0);
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT chk_effective_period CHECK (effective_end_date IS NULL OR effective_start_date <= effective_end_date);
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT chk_success_rate_range CHECK (success_rate IS NULL OR (success_rate >= 0 AND success_rate <= 100));
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT chk_cost_support_amount_positive CHECK (cost_support_amount IS NULL OR cost_support_amount >= 0);

-- 外部キー制約
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_job_type FOREIGN KEY (target_job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_position FOREIGN KEY (target_position_id) REFERENCES MST_Position(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_skill_grade FOREIGN KEY (target_skill_grade_id) REFERENCES MST_SkillGrade(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_department FOREIGN KEY (target_department_id) REFERENCES MST_Department(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_certification FOREIGN KEY (certification_id) REFERENCES MST_Certification(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_created_by FOREIGN KEY (created_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_approved_by FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
