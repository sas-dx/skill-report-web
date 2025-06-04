-- ============================================
-- テーブル: MST_SkillHierarchy
-- 論理名: スキル階層マスタ
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_SkillHierarchy;

CREATE TABLE MST_SkillHierarchy (
    skill_id VARCHAR(50) COMMENT 'スキル項目のID（MST_SkillItemへの外部キー）',
    parent_skill_id VARCHAR(50) COMMENT '親スキルのID（MST_SkillHierarchyへの自己参照外部キー、NULLの場合はルートスキル）',
    hierarchy_level INTEGER COMMENT '階層の深さ（1:大分類、2:中分類、3:小分類、最大5階層まで）',
    skill_path VARCHAR(500) COMMENT 'ルートからのスキルパス（例：/技術スキル/プログラミング/Java）',
    sort_order INTEGER DEFAULT 0 COMMENT '同一階層内での表示順序',
    is_leaf BOOLEAN DEFAULT True COMMENT '末端ノード（子を持たない）かどうか',
    skill_category ENUM COMMENT 'スキルの大分類（TECHNICAL:技術、BUSINESS:ビジネス、CERTIFICATION:資格、SOFT:ソフトスキル）',
    description TEXT COMMENT 'スキル階層の詳細説明',
    is_active BOOLEAN DEFAULT True COMMENT '階層が有効かどうか',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_skill_id ON MST_SkillHierarchy (skill_id);
CREATE INDEX idx_parent_skill ON MST_SkillHierarchy (parent_skill_id);
CREATE INDEX idx_hierarchy_level ON MST_SkillHierarchy (hierarchy_level);
CREATE INDEX idx_skill_path ON MST_SkillHierarchy (skill_path);
CREATE INDEX idx_category_level ON MST_SkillHierarchy (skill_category, hierarchy_level);
CREATE INDEX idx_parent_sort ON MST_SkillHierarchy (parent_skill_id, sort_order);

-- 外部キー制約
ALTER TABLE MST_SkillHierarchy ADD CONSTRAINT fk_hierarchy_skill FOREIGN KEY (skill_id) REFERENCES MST_SkillItem(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_SkillHierarchy ADD CONSTRAINT fk_hierarchy_parent FOREIGN KEY (parent_skill_id) REFERENCES MST_SkillHierarchy(skill_id) ON UPDATE CASCADE ON DELETE CASCADE;

-- その他の制約
ALTER TABLE MST_SkillHierarchy ADD CONSTRAINT uk_skill_hierarchy UNIQUE ();
ALTER TABLE MST_SkillHierarchy ADD CONSTRAINT chk_hierarchy_level CHECK (hierarchy_level >= 1 AND hierarchy_level <= 5);
ALTER TABLE MST_SkillHierarchy ADD CONSTRAINT chk_skill_category CHECK (skill_category IN ('TECHNICAL', 'BUSINESS', 'CERTIFICATION', 'SOFT'));
ALTER TABLE MST_SkillHierarchy ADD CONSTRAINT chk_no_self_reference CHECK (skill_id != parent_skill_id);
