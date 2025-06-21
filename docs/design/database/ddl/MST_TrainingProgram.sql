-- ============================================
-- テーブル: MST_TrainingProgram
-- 論理名: 研修プログラム
-- 説明: MST_TrainingProgram（研修プログラム）は、組織で提供される研修・教育プログラムの詳細情報を管理するマスタテーブルです。

主な目的：
- 研修プログラムの体系的管理
- 研修内容・カリキュラムの標準化
- スキル開発との連携
- 研修効果の測定・評価
- 人材育成計画の支援

このテーブルにより、効果的な研修体系を構築し、
組織全体のスキル向上と人材育成を促進できます。

-- 作成日: 2025-06-21 17:20:35
-- ============================================

DROP TABLE IF EXISTS MST_TrainingProgram;

CREATE TABLE MST_TrainingProgram (
    training_program_id VARCHAR,
    program_code VARCHAR,
    program_name VARCHAR,
    program_name_en VARCHAR,
    program_description TEXT,
    program_category ENUM,
    program_type ENUM,
    target_audience ENUM,
    difficulty_level ENUM,
    duration_hours DECIMAL,
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
    passing_score DECIMAL,
    certification_provided BOOLEAN DEFAULT False,
    pdu_credits DECIMAL,
    related_skills TEXT,
    related_certifications TEXT,
    cost_per_participant DECIMAL,
    external_provider VARCHAR,
    external_url VARCHAR,
    venue_type ENUM,
    venue_requirements TEXT,
    language ENUM DEFAULT 'JA',
    repeat_interval INTEGER,
    mandatory_flag BOOLEAN DEFAULT False,
    active_flag BOOLEAN DEFAULT True,
    effective_start_date DATE,
    effective_end_date DATE,
    created_by VARCHAR,
    approved_by VARCHAR,
    approval_date DATE,
    version_number VARCHAR DEFAULT '1.0',
    revision_notes TEXT,
    tags TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
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
