-- ============================================
-- テーブル: MST_Skill
-- 論理名: スキルマスタ
-- 説明: スキルマスタテーブルは、システムで管理するスキル項目の基本情報を管理するマスタテーブルです。

主な目的：
- スキル項目の一元管理
- スキルカテゴリとレベル定義の管理
- スキル評価基準の標準化
- スキル検索とフィルタリングの支援

このテーブルは、スキル管理システムの基盤となるマスタテーブルで、
統一されたスキル評価基準と効率的なスキル管理を実現します。

-- 作成日: 2025-06-21 17:21:58
-- ============================================

DROP TABLE IF EXISTS MST_Skill;

CREATE TABLE MST_Skill (
    id VARCHAR,
    tenant_id VARCHAR,
    skill_name VARCHAR,
    skill_name_en VARCHAR,
    category_id VARCHAR,
    skill_type ENUM DEFAULT 'TECHNICAL',
    difficulty_level INTEGER DEFAULT 3,
    description TEXT,
    evaluation_criteria TEXT,
    required_experience_months INTEGER,
    related_skills TEXT,
    prerequisite_skills TEXT,
    certification_info TEXT,
    learning_resources TEXT,
    market_demand ENUM DEFAULT 'MEDIUM',
    technology_trend ENUM DEFAULT 'STABLE',
    is_core_skill BOOLEAN DEFAULT False,
    display_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT True,
    effective_from DATE,
    effective_to DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT False
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_MST_Skill_id ON MST_Skill (id);
CREATE INDEX idx_MST_Skill_skill_name ON MST_Skill (skill_name);
CREATE INDEX idx_MST_Skill_category_id ON MST_Skill (category_id);
CREATE INDEX idx_MST_Skill_skill_type ON MST_Skill (skill_type);
CREATE INDEX idx_MST_Skill_category_order ON MST_Skill (category_id, display_order);
CREATE INDEX idx_MST_Skill_market_demand ON MST_Skill (market_demand);
CREATE INDEX idx_MST_Skill_is_active ON MST_Skill (is_active);
