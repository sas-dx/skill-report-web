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

-- 作成日: 2025-06-24 22:56:15
-- ============================================

DROP TABLE IF EXISTS MST_TrainingProgram;

CREATE TABLE MST_TrainingProgram (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    active_flag BOOLEAN DEFAULT True COMMENT '有効フラグ',
    approval_date DATE COMMENT '承認日',
    approved_by VARCHAR(50) COMMENT '承認者',
    assessment_method ENUM('NONE', 'TEST', 'ASSIGNMENT', 'PRESENTATION', 'PRACTICAL', 'COMPREHENSIVE') COMMENT '評価方法',
    certification_provided BOOLEAN DEFAULT False COMMENT '認定証発行',
    cost_per_participant DECIMAL(10,2) COMMENT '参加者単価',
    created_by VARCHAR(50) COMMENT '作成者',
    curriculum_details TEXT COMMENT 'カリキュラム詳細',
    curriculum_outline TEXT COMMENT 'カリキュラム概要',
    difficulty_level ENUM('BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT') COMMENT '難易度',
    duration_days INTEGER COMMENT '研修日数',
    duration_hours DECIMAL(5,2) COMMENT '研修時間',
    effective_end_date DATE COMMENT '有効終了日',
    effective_start_date DATE COMMENT '有効開始日',
    equipment_required TEXT COMMENT '必要機材',
    external_provider VARCHAR(200) COMMENT '外部提供者',
    external_url VARCHAR(500) COMMENT '外部URL',
    instructor_requirements TEXT COMMENT '講師要件',
    language ENUM('JA', 'EN', 'BILINGUAL') DEFAULT 'JA' COMMENT '実施言語',
    learning_objectives TEXT COMMENT '学習目標',
    mandatory_flag BOOLEAN DEFAULT False COMMENT '必須研修フラグ',
    materials_required TEXT COMMENT '必要教材',
    max_participants INTEGER COMMENT '最大参加者数',
    min_participants INTEGER COMMENT '最小参加者数',
    passing_score DECIMAL(5,2) COMMENT '合格点',
    pdu_credits DECIMAL(5,2) COMMENT 'PDUクレジット',
    prerequisites TEXT COMMENT '前提条件',
    program_category ENUM('TECHNICAL', 'BUSINESS', 'MANAGEMENT', 'COMPLIANCE', 'SOFT_SKILL', 'CERTIFICATION', 'ORIENTATION') COMMENT 'プログラムカテゴリ',
    program_code VARCHAR(20) COMMENT 'プログラムコード',
    program_description TEXT COMMENT 'プログラム説明',
    program_name VARCHAR(200) COMMENT 'プログラム名',
    program_name_en VARCHAR(200) COMMENT 'プログラム名（英語）',
    program_type ENUM('CLASSROOM', 'ONLINE', 'BLENDED', 'OJT', 'SELF_STUDY', 'EXTERNAL') COMMENT 'プログラム種別',
    related_certifications TEXT COMMENT '関連資格',
    related_skills TEXT COMMENT '関連スキル',
    repeat_interval INTEGER COMMENT '再受講間隔',
    revision_notes TEXT COMMENT '改訂メモ',
    tags TEXT COMMENT 'タグ',
    target_audience ENUM('ALL', 'NEW_HIRE', 'JUNIOR', 'MIDDLE', 'SENIOR', 'MANAGER', 'EXECUTIVE', 'SPECIALIST') COMMENT '対象者',
    training_program_id VARCHAR(50) COMMENT '研修プログラムID',
    trainingprogram_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_TrainingProgramの主キー',
    venue_requirements TEXT COMMENT '会場要件',
    venue_type ENUM('INTERNAL', 'EXTERNAL', 'ONLINE', 'HYBRID') COMMENT '会場種別',
    version_number VARCHAR(10) DEFAULT '1.0' COMMENT 'バージョン番号',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
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
CREATE INDEX idx_mst_trainingprogram_tenant_id ON MST_TrainingProgram (tenant_id);

-- 外部キー制約
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT fk_training_program_created_by FOREIGN KEY (created_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT fk_training_program_approved_by FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
-- 制約DDL生成エラー: uk_training_program_id
-- 制約DDL生成エラー: uk_program_code
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT chk_program_category CHECK (program_category IN ('TECHNICAL', 'BUSINESS', 'MANAGEMENT', 'COMPLIANCE', 'SOFT_SKILL', 'CERTIFICATION', 'ORIENTATION'));
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT chk_program_type CHECK (program_type IN ('CLASSROOM', 'ONLINE', 'BLENDED', 'OJT', 'SELF_STUDY', 'EXTERNAL'));
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT chk_target_audience CHECK (target_audience IN ('ALL', 'NEW_HIRE', 'JUNIOR', 'MIDDLE', 'SENIOR', 'MANAGER', 'EXECUTIVE', 'SPECIALIST'));
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT chk_difficulty_level CHECK (difficulty_level IN ('BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT'));
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT chk_assessment_method CHECK (assessment_method IN ('NONE', 'TEST', 'ASSIGNMENT', 'PRESENTATION', 'PRACTICAL', 'COMPREHENSIVE'));
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT chk_venue_type CHECK (venue_type IN ('INTERNAL', 'EXTERNAL', 'ONLINE', 'HYBRID'));
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT chk_language CHECK (language IN ('JA', 'EN', 'BILINGUAL'));
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT chk_duration_positive CHECK (duration_hours > 0 AND duration_days > 0);
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT chk_participants_range CHECK (min_participants IS NULL OR max_participants IS NULL OR min_participants <= max_participants);
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT chk_effective_period CHECK (effective_end_date IS NULL OR effective_start_date <= effective_end_date);
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT chk_passing_score_range CHECK (passing_score IS NULL OR (passing_score >= 0 AND passing_score <= 100));
