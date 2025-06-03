-- ============================================
-- テーブル: MST_SkillItem
-- 論理名: スキル項目マスタ
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_SkillItem;

CREATE TABLE MST_SkillItem (
    skill_code VARCHAR(20) COMMENT 'スキル項目を一意に識別するコード（例：SKILL001）',
    skill_name VARCHAR(100) COMMENT 'スキル項目の正式名称',
    skill_category_id VARCHAR(50) COMMENT 'スキルカテゴリのID',
    skill_type ENUM COMMENT 'スキルの種別（TECHNICAL:技術、BUSINESS:ビジネス、CERTIFICATION:資格）',
    difficulty_level INT COMMENT 'スキル習得の難易度（1-5段階）',
    importance_level INT COMMENT '組織における重要度（1-5段階）',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称',
    description TEXT COMMENT 'マスタ説明'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_skill_code ON MST_SkillItem (skill_code);
CREATE INDEX idx_skill_category ON MST_SkillItem (skill_category_id);

-- その他の制約
ALTER TABLE MST_SkillItem ADD CONSTRAINT uk_skill_code UNIQUE ();
