-- TRN_TrainingHistory (研修参加履歴) DDL
-- 生成日時: 2025-06-01 20:40:26

CREATE TABLE TRN_TrainingHistory (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    training_history_id VARCHAR(50),
    employee_id VARCHAR(50),
    training_program_id VARCHAR(50),
    training_name VARCHAR(200),
    training_type ENUM,
    training_category ENUM,
    provider_name VARCHAR(100),
    instructor_name VARCHAR(100),
    start_date DATE,
    end_date DATE,
    duration_hours DECIMAL(5,1),
    location VARCHAR(200),
    cost DECIMAL(10,2),
    cost_covered_by ENUM,
    attendance_status ENUM DEFAULT 'COMPLETED',
    completion_rate DECIMAL(5,2),
    test_score DECIMAL(5,2),
    grade VARCHAR(10),
    certificate_obtained BOOLEAN DEFAULT False,
    certificate_number VARCHAR(100),
    pdu_earned DECIMAL(5,1),
    skills_acquired TEXT,
    learning_objectives TEXT,
    learning_outcomes TEXT,
    feedback TEXT,
    satisfaction_score DECIMAL(3,1),
    recommendation_score DECIMAL(3,1),
    follow_up_required BOOLEAN DEFAULT False,
    follow_up_date DATE,
    manager_approval BOOLEAN DEFAULT False,
    approved_by VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_training_history_id ON TRN_TrainingHistory (training_history_id);
CREATE INDEX idx_employee_id ON TRN_TrainingHistory (employee_id);
CREATE INDEX idx_training_program_id ON TRN_TrainingHistory (training_program_id);
CREATE INDEX idx_training_type ON TRN_TrainingHistory (training_type);
CREATE INDEX idx_training_category ON TRN_TrainingHistory (training_category);
CREATE INDEX idx_date_range ON TRN_TrainingHistory (start_date, end_date);
CREATE INDEX idx_attendance_status ON TRN_TrainingHistory (attendance_status);
CREATE INDEX idx_employee_period ON TRN_TrainingHistory (employee_id, start_date, end_date);
CREATE INDEX idx_certificate ON TRN_TrainingHistory (certificate_obtained, certificate_number);

-- 外部キー制約
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT fk_training_history_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT fk_training_history_program FOREIGN KEY (training_program_id) REFERENCES MST_TrainingProgram(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT fk_training_history_approver FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
