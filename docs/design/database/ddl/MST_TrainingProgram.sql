-- ============================================
-- テーブル: MST_TrainingProgram
-- 論理名: 研修プログラム
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_TrainingProgram;

CREATE TABLE MST_TrainingProgram (
    training_program_id VARCHAR(50) COMMENT '研修プログラムを一意に識別するID',
    program_code VARCHAR(20) COMMENT '研修プログラムの識別コード',
    program_name VARCHAR(200) COMMENT '研修プログラムの名称',
    program_name_en VARCHAR(200) COMMENT '研修プログラムの英語名称',
    program_description TEXT COMMENT '研修プログラムの詳細説明',
    program_category ENUM COMMENT '研修の分類（TECHNICAL:技術、BUSINESS:ビジネス、MANAGEMENT:管理、COMPLIANCE:コンプライアンス、SOFT_SKILL:ソフトスキル、CERTIFICATION:資格、ORIENTATION:新人研修）',
    program_type ENUM COMMENT '研修の実施形態（CLASSROOM:集合研修、ONLINE:オンライン、BLENDED:ブレンド、OJT:OJT、SELF_STUDY:自習、EXTERNAL:外部研修）',
    target_audience ENUM COMMENT '研修の対象者（ALL:全社員、NEW_HIRE:新入社員、JUNIOR:若手、MIDDLE:中堅、SENIOR:シニア、MANAGER:管理職、EXECUTIVE:役員、SPECIALIST:専門職）',
    difficulty_level ENUM COMMENT '研修の難易度（BEGINNER:初級、INTERMEDIATE:中級、ADVANCED:上級、EXPERT:エキスパート）',
    duration_hours DECIMAL(5,2) COMMENT '研修の総時間数',
    duration_days INTEGER COMMENT '研修の実施日数',
    max_participants INTEGER COMMENT '1回の研修での最大参加者数',
    min_participants INTEGER COMMENT '開催に必要な最小参加者数',
    prerequisites TEXT COMMENT '受講に必要な前提知識・条件',
    learning_objectives TEXT COMMENT '研修の学習目標・到達目標',
    curriculum_outline TEXT COMMENT '研修のカリキュラム・内容概要',
    curriculum_details TEXT COMMENT '詳細なカリキュラム内容（JSON形式）',
    materials_required TEXT COMMENT '研修に必要な教材・資料（JSON形式）',
    equipment_required TEXT COMMENT '研修に必要な機材・設備（JSON形式）',
    instructor_requirements TEXT COMMENT '講師に求められる要件・資格',
    assessment_method ENUM COMMENT '研修の評価方法（NONE:なし、TEST:テスト、ASSIGNMENT:課題、PRESENTATION:発表、PRACTICAL:実技、COMPREHENSIVE:総合評価）',
    passing_score DECIMAL(5,2) COMMENT '研修合格に必要な点数',
    certification_provided BOOLEAN DEFAULT False COMMENT '修了時に認定証を発行するかどうか',
    pdu_credits DECIMAL(5,2) COMMENT '取得可能なPDUクレジット数',
    related_skills TEXT COMMENT '研修で習得・向上するスキル（JSON形式）',
    related_certifications TEXT COMMENT '研修に関連する資格（JSON形式）',
    cost_per_participant DECIMAL(10,2) COMMENT '参加者1人あたりの研修費用',
    external_provider VARCHAR(200) COMMENT '外部研修の場合の提供会社・機関名',
    external_url VARCHAR(500) COMMENT '外部研修の詳細情報URL',
    venue_type ENUM COMMENT '研修会場の種別（INTERNAL:社内、EXTERNAL:社外、ONLINE:オンライン、HYBRID:ハイブリッド）',
    venue_requirements TEXT COMMENT '研修会場に必要な設備・条件',
    language ENUM DEFAULT 'JA' COMMENT '研修の実施言語（JA:日本語、EN:英語、BILINGUAL:バイリンガル）',
    repeat_interval INTEGER COMMENT '再受講可能な間隔（月数）',
    mandatory_flag BOOLEAN DEFAULT False COMMENT '必須研修かどうか',
    active_flag BOOLEAN DEFAULT True COMMENT '現在提供中の研修かどうか',
    effective_start_date DATE COMMENT '研修プログラムの提供開始日',
    effective_end_date DATE COMMENT '研修プログラムの提供終了日',
    created_by VARCHAR(50) COMMENT 'プログラムを作成した担当者ID',
    approved_by VARCHAR(50) COMMENT 'プログラムを承認した責任者ID',
    approval_date DATE COMMENT 'プログラムが承認された日付',
    version_number VARCHAR(10) DEFAULT '1.0' COMMENT 'プログラムのバージョン番号',
    revision_notes TEXT COMMENT 'バージョン改訂時のメモ・変更内容',
    tags TEXT COMMENT '検索・分類用のタグ（JSON形式）',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称',
    description TEXT COMMENT 'マスタ説明'
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

-- 外部キー制約
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT fk_training_program_created_by FOREIGN KEY (created_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT fk_training_program_approved_by FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT uk_training_program_id UNIQUE ();
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT uk_program_code UNIQUE ();
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
