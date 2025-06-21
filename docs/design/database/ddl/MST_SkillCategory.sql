-- ============================================
-- テーブル: MST_SkillCategory
-- 論理名: スキルカテゴリマスタ
-- 説明: MST_SkillCategory（スキルカテゴリマスタ）は、スキルの分類・カテゴリを管理するマスタテーブルです。

主な目的：
- スキルの体系的分類・階層管理
- スキル検索・絞り込みの基盤
- スキルマップ・スキル評価の構造化
- 業界標準・企業独自のスキル分類対応
- スキル統計・分析の軸設定
- キャリアパス・研修計画の基盤
- スキル可視化・レポート生成の支援

このテーブルは、スキル管理システムの基盤となり、
効率的なスキル管理と戦略的人材育成を支援します。

-- 作成日: 2025-06-21 17:21:58
-- ============================================

DROP TABLE IF EXISTS MST_SkillCategory;

CREATE TABLE MST_SkillCategory (
    category_code VARCHAR,
    category_name VARCHAR,
    category_name_short VARCHAR,
    category_name_en VARCHAR,
    category_type ENUM,
    parent_category_id VARCHAR,
    category_level INT DEFAULT 1,
    category_path VARCHAR,
    is_system_category BOOLEAN DEFAULT False,
    is_leaf_category BOOLEAN DEFAULT True,
    skill_count INT DEFAULT 0,
    evaluation_method ENUM,
    max_level INT,
    icon_url VARCHAR,
    color_code VARCHAR,
    display_order INT DEFAULT 999,
    is_popular BOOLEAN DEFAULT False,
    category_status ENUM DEFAULT 'ACTIVE',
    effective_from DATE,
    effective_to DATE,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_category_code ON MST_SkillCategory (category_code);
CREATE INDEX idx_category_type ON MST_SkillCategory (category_type);
CREATE INDEX idx_parent_category ON MST_SkillCategory (parent_category_id);
CREATE INDEX idx_category_level ON MST_SkillCategory (category_level);
CREATE INDEX idx_category_path ON MST_SkillCategory (category_path);
CREATE INDEX idx_system_category ON MST_SkillCategory (is_system_category);
CREATE INDEX idx_leaf_category ON MST_SkillCategory (is_leaf_category);
CREATE INDEX idx_category_status ON MST_SkillCategory (category_status);
CREATE INDEX idx_display_order ON MST_SkillCategory (parent_category_id, display_order);
CREATE INDEX idx_popular_category ON MST_SkillCategory (is_popular);
