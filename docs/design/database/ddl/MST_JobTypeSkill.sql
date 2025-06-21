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

-- 作成日: 2025-06-21 17:20:34
-- ============================================

DROP TABLE IF EXISTS MST_JobTypeSkill;

CREATE TABLE MST_JobTypeSkill (
    job_type_id VARCHAR,
    skill_item_id VARCHAR,
    required_level INTEGER,
    skill_priority ENUM DEFAULT 'MEDIUM',
    skill_category ENUM,
    experience_years DECIMAL,
    certification_required BOOLEAN DEFAULT False,
    skill_weight DECIMAL,
    evaluation_criteria TEXT,
    learning_path TEXT,
    skill_status ENUM DEFAULT 'ACTIVE',
    effective_date DATE,
    expiry_date DATE,
    alternative_skills TEXT,
    prerequisite_skills TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時'
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
