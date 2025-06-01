-- MST_TrainingProgram (研修プログラム) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_TrainingProgram (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    training_program_id VARCHAR(50),
    program_code VARCHAR(20),
    program_name VARCHAR(200),
    program_name_en VARCHAR(200),
    program_description TEXT,
    program_category ENUM,
    program_type ENUM,
    target_audience ENUM,
    difficulty_level ENUM,
    duration_hours DECIMAL(5,2),
    duration_days INTEGER,
    max_participants INTEGER,
    min_participants INTEGER,
    prerequisites TEXT,
    learning_objectives TEXT,
    curriculum_outline TEXT,
    curriculum_details TEXT,
    materials_required TEXT,
    equipment_required TEXT,
    instructor_requirements TEXT,
    assessment_method ENUM,
    passing_score DECIMAL(5,2),
    certification_provided BOOLEAN DEFAULT False,
    pdu_credits DECIMAL(5,2),
    related_skills TEXT,
    related_certifications TEXT,
    cost_per_participant DECIMAL(10,2),
    external_provider VARCHAR(200),
    external_url VARCHAR(500),
    venue_type ENUM,
    venue_requirements TEXT,
    language ENUM DEFAULT 'JA',
    repeat_interval INTEGER,
    mandatory_flag BOOLEAN DEFAULT False,
    active_flag BOOLEAN DEFAULT True,
    effective_start_date DATE,
    effective_end_date DATE,
    created_by VARCHAR(50),
    approved_by VARCHAR(50),
    approval_date DATE,
    version_number VARCHAR(10) DEFAULT '1.0',
    revision_notes TEXT,
    tags TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_training_program_id ON MST_TrainingProgram (training_program_id);
CREATE UNIQUE INDEX idx_program_code ON MST_TrainingProgram (program_code);
CREATE INDEX idx_program_category ON MST_TrainingProgram (program_category);
CREATE INDEX idx_program_type ON MST_TrainingProgram (program_type);
CREATE INDEX idx_target_audience ON MST_TrainingProgram (target_audience);
CREATE INDEX idx_difficulty_level ON MST_TrainingProgram (difficulty_level);
CREATE INDEX idx_active_flag ON MST_TrainingProgram (active_flag);
CREATE INDEX idx_mandatory_flag ON MST_TrainingProgram (mandatory_flag);
CREATE INDEX idx_effective_period ON MST_TrainingProgram (effective_start_date, effective_end_date);
CREATE INDEX idx_external_provider ON MST_TrainingProgram (external_provider);
CREATE INDEX idx_language ON MST_TrainingProgram (language);

-- 外部キー制約
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT fk_training_program_created_by FOREIGN KEY (created_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT fk_training_program_approved_by FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
