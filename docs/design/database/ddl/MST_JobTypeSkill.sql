-- ============================================
-- テーブル: MST_JobTypeSkill
-- 論理名: 職種スキル関連
-- 説明: MST_JobTypeSkill（職種スキル関連）は、職種と必要スキルの関連付けを管理するマスタテーブルです。

主な目的：
- 職種ごとの必要スキルの定義
- スキル要求レベルの管理
- 職種別スキル要件の標準化
- 人材配置時のスキルマッチング
- 教育計画立案の基礎データ
- 採用要件定義の支援

このテーブルにより、各職種に求められるスキルセットを明確に定義し、
人材育成や配置転換の判断基準として活用できます。

-- 作成日: 2025-06-24 23:05:57
-- ============================================

DROP TABLE IF EXISTS MST_JobTypeSkill;

CREATE TABLE MST_JobTypeSkill (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    alternative_skills TEXT COMMENT '代替スキル',
    certification_required BOOLEAN DEFAULT False COMMENT '資格必須',
    effective_date DATE COMMENT '有効開始日',
    evaluation_criteria TEXT COMMENT '評価基準',
    experience_years DECIMAL(4,1) COMMENT '必要経験年数',
    expiry_date DATE COMMENT '有効終了日',
    job_type_id VARCHAR(50) COMMENT '職種ID',
    jobtypeskill_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_JobTypeSkillの主キー',
    learning_path TEXT COMMENT '学習パス',
    prerequisite_skills TEXT COMMENT '前提スキル',
    required_level INTEGER COMMENT '必要レベル',
    skill_category ENUM('TECHNICAL', 'BUSINESS', 'MANAGEMENT', 'COMMUNICATION') COMMENT 'スキル分類',
    skill_item_id VARCHAR(50) COMMENT 'スキル項目ID',
    skill_priority ENUM('CRITICAL', 'HIGH', 'MEDIUM', 'LOW') DEFAULT 'MEDIUM' COMMENT 'スキル優先度',
    skill_status ENUM('ACTIVE', 'DEPRECATED', 'OBSOLETE') DEFAULT 'ACTIVE' COMMENT 'スキル状況',
    skill_weight DECIMAL(5,2) COMMENT 'スキル重み',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
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
CREATE INDEX idx_mst_jobtypeskill_tenant_id ON MST_JobTypeSkill (tenant_id);

-- 外部キー制約
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT fk_MST_JobTypeSkill_job_type FOREIGN KEY (job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT fk_MST_JobTypeSkill_skill_item FOREIGN KEY (skill_item_id) REFERENCES MST_SkillItem(id) ON UPDATE CASCADE ON DELETE CASCADE;

-- その他の制約
-- 制約DDL生成エラー: uk_MST_JobTypeSkill_job_skill
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT chk_MST_JobTypeSkill_required_level CHECK (required_level >= 1 AND required_level <= 5);
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT chk_MST_JobTypeSkill_priority CHECK (skill_priority IN ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW'));
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT chk_MST_JobTypeSkill_category CHECK (skill_category IN ('TECHNICAL', 'BUSINESS', 'MANAGEMENT', 'COMMUNICATION'));
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT chk_MST_JobTypeSkill_status CHECK (skill_status IN ('ACTIVE', 'DEPRECATED', 'OBSOLETE'));
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT chk_MST_JobTypeSkill_experience_years CHECK (experience_years IS NULL OR experience_years >= 0);
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT chk_MST_JobTypeSkill_skill_weight CHECK (skill_weight IS NULL OR (skill_weight >= 0 AND skill_weight <= 100));
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT chk_MST_JobTypeSkill_date_range CHECK (expiry_date IS NULL OR effective_date <= expiry_date);
