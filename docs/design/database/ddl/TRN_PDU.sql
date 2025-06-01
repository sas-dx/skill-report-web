-- TRN_PDU (継続教育ポイント) DDL
-- 生成日時: 2025-06-01 20:40:26

CREATE TABLE TRN_PDU (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    pdu_id VARCHAR(50),
    employee_id VARCHAR(50),
    certification_id VARCHAR(50),
    activity_type ENUM,
    activity_name VARCHAR(200),
    activity_description TEXT,
    provider_name VARCHAR(100),
    activity_date DATE,
    start_time TIME,
    end_time TIME,
    duration_hours DECIMAL(5,1),
    pdu_points DECIMAL(5,1),
    pdu_category ENUM,
    pdu_subcategory VARCHAR(50),
    location VARCHAR(200),
    cost DECIMAL(10,2),
    cost_covered_by ENUM,
    evidence_type ENUM,
    evidence_file_path VARCHAR(500),
    certificate_number VARCHAR(100),
    instructor_name VARCHAR(100),
    learning_objectives TEXT,
    learning_outcomes TEXT,
    skills_developed TEXT,
    approval_status ENUM DEFAULT 'PENDING',
    approved_by VARCHAR(50),
    approval_date DATE,
    approval_comment TEXT,
    expiry_date DATE,
    is_recurring BOOLEAN DEFAULT False,
    recurrence_pattern VARCHAR(50),
    related_training_id VARCHAR(50),
    related_project_id VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_pdu_id ON TRN_PDU (pdu_id);
CREATE INDEX idx_employee_id ON TRN_PDU (employee_id);
CREATE INDEX idx_certification_id ON TRN_PDU (certification_id);
CREATE INDEX idx_activity_type ON TRN_PDU (activity_type);
CREATE INDEX idx_activity_date ON TRN_PDU (activity_date);
CREATE INDEX idx_pdu_category ON TRN_PDU (pdu_category);
CREATE INDEX idx_approval_status ON TRN_PDU (approval_status);
CREATE INDEX idx_employee_period ON TRN_PDU (employee_id, activity_date);
CREATE INDEX idx_expiry_date ON TRN_PDU (expiry_date);
CREATE INDEX idx_certification_employee ON TRN_PDU (certification_id, employee_id, approval_status);

-- 外部キー制約
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_certification FOREIGN KEY (certification_id) REFERENCES MST_Certification(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_approver FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_training FOREIGN KEY (related_training_id) REFERENCES TRN_TrainingHistory(training_history_id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_project FOREIGN KEY (related_project_id) REFERENCES TRN_ProjectRecord(project_record_id) ON UPDATE CASCADE ON DELETE SET NULL;
