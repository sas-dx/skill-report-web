-- ============================================
-- テーブル: MST_JobTypeSkill
-- 論理名: 職種スキル関連
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_JobTypeSkill;

CREATE TABLE MST_JobTypeSkill (
    job_type_id VARCHAR(50) COMMENT '職種のID（MST_JobTypeへの外部キー）',
    skill_item_id VARCHAR(50) COMMENT 'スキル項目のID（MST_SkillItemへの外部キー）',
    required_level INTEGER COMMENT '当該職種で必要なスキルレベル（1-5、5が最高レベル）',
    skill_priority ENUM DEFAULT 'MEDIUM' COMMENT 'スキル優先度（CRITICAL:必須、HIGH:重要、MEDIUM:推奨、LOW:あれば良い）',
    skill_category ENUM COMMENT 'スキル分類（TECHNICAL:技術、BUSINESS:業務、MANAGEMENT:管理、COMMUNICATION:コミュニケーション）',
    experience_years DECIMAL(4,1) COMMENT '当該スキルの必要経験年数',
    certification_required BOOLEAN DEFAULT False COMMENT '関連資格の取得が必須かどうか',
    skill_weight DECIMAL(5,2) COMMENT '職種内でのスキル重み（%、合計100%）',
    evaluation_criteria TEXT COMMENT 'スキルレベルの評価基準・判定方法',
    learning_path TEXT COMMENT 'スキル習得のための推奨学習パス',
    skill_status ENUM DEFAULT 'ACTIVE' COMMENT 'スキル状況（ACTIVE:有効、DEPRECATED:非推奨、OBSOLETE:廃止）',
    effective_date DATE COMMENT 'スキル要件の有効開始日',
    expiry_date DATE COMMENT 'スキル要件の有効終了日（NULL:無期限）',
    alternative_skills TEXT COMMENT '代替可能なスキルのリスト（JSON形式）',
    prerequisite_skills TEXT COMMENT '前提となるスキルのリスト（JSON形式）',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称',
    description TEXT COMMENT 'マスタ説明'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_MST_JobTypeSkill_job_type_id ON MST_JobTypeSkill (job_type_id);
CREATE INDEX idx_MST_JobTypeSkill_skill_item_id ON MST_JobTypeSkill (skill_item_id);
CREATE UNIQUE INDEX idx_MST_JobTypeSkill_job_skill ON MST_JobTypeSkill (job_type_id, skill_item_id);
CREATE INDEX idx_MST_JobTypeSkill_required_level ON MST_JobTypeSkill (required_level);
CREATE INDEX idx_MST_JobTypeSkill_priority ON MST_JobTypeSkill (skill_priority);
CREATE INDEX idx_MST_JobTypeSkill_category ON MST_JobTypeSkill (skill_category);
CREATE INDEX idx_MST_JobTypeSkill_status ON MST_JobTypeSkill (skill_status);
CREATE INDEX idx_MST_JobTypeSkill_effective_date ON MST_JobTypeSkill (effective_date);

-- 外部キー制約
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT fk_MST_JobTypeSkill_job_type FOREIGN KEY (job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT fk_MST_JobTypeSkill_skill_item FOREIGN KEY (skill_item_id) REFERENCES MST_SkillItem(id) ON UPDATE CASCADE ON DELETE CASCADE;

-- その他の制約
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT uk_MST_JobTypeSkill_job_skill UNIQUE ();
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT chk_MST_JobTypeSkill_required_level CHECK (required_level >= 1 AND required_level <= 5);
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT chk_MST_JobTypeSkill_priority CHECK (skill_priority IN ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW'));
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT chk_MST_JobTypeSkill_category CHECK (skill_category IN ('TECHNICAL', 'BUSINESS', 'MANAGEMENT', 'COMMUNICATION'));
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT chk_MST_JobTypeSkill_status CHECK (skill_status IN ('ACTIVE', 'DEPRECATED', 'OBSOLETE'));
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT chk_MST_JobTypeSkill_experience_years CHECK (experience_years IS NULL OR experience_years >= 0);
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT chk_MST_JobTypeSkill_skill_weight CHECK (skill_weight IS NULL OR (skill_weight >= 0 AND skill_weight <= 100));
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT chk_MST_JobTypeSkill_date_range CHECK (expiry_date IS NULL OR effective_date <= expiry_date);
