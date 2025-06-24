-- ============================================
-- テーブル: MST_SkillHierarchy
-- 論理名: スキル階層マスタ
-- 説明: MST_SkillHierarchy（スキル階層マスタ）は、スキル項目間の階層関係を管理するマスタテーブルです。

主な目的：
- スキルの親子関係・階層構造の管理
- スキル分類の体系化（大分類→中分類→小分類）
- スキル検索・フィルタリングの基盤提供
- スキルマップ・スキルツリーの表示支援
- 関連スキルの推薦機能の基盤

このテーブルにより、技術スキル、ビジネススキル、資格等を体系的に分類し、
社員のスキル管理を効率的に行うことができます。

-- 作成日: 2025-06-24 22:56:14
-- ============================================

DROP TABLE IF EXISTS MST_SkillHierarchy;

CREATE TABLE MST_SkillHierarchy (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    description TEXT COMMENT '説明',
    hierarchy_level INTEGER COMMENT '階層レベル',
    is_active BOOLEAN DEFAULT True COMMENT '有効フラグ',
    is_leaf BOOLEAN DEFAULT True COMMENT '末端フラグ',
    parent_skill_id VARCHAR(50) COMMENT '親スキルID',
    skill_category ENUM('TECHNICAL', 'BUSINESS', 'CERTIFICATION', 'SOFT') COMMENT 'スキルカテゴリ',
    skill_id VARCHAR(50) COMMENT 'スキルID',
    skill_path VARCHAR(500) COMMENT 'スキルパス',
    skillhierarchy_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_SkillHierarchyの主キー',
    sort_order INTEGER DEFAULT 0 COMMENT '表示順序',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_skill_id ON MST_SkillHierarchy (skill_id);
CREATE INDEX idx_parent_skill ON MST_SkillHierarchy (parent_skill_id);
CREATE INDEX idx_hierarchy_level ON MST_SkillHierarchy (hierarchy_level);
CREATE INDEX idx_skill_path ON MST_SkillHierarchy (skill_path);
CREATE INDEX idx_category_level ON MST_SkillHierarchy (skill_category, hierarchy_level);
CREATE INDEX idx_parent_sort ON MST_SkillHierarchy (parent_skill_id, sort_order);
CREATE INDEX idx_mst_skillhierarchy_tenant_id ON MST_SkillHierarchy (tenant_id);

-- 外部キー制約
ALTER TABLE MST_SkillHierarchy ADD CONSTRAINT fk_hierarchy_skill FOREIGN KEY (skill_id) REFERENCES MST_SkillItem(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_SkillHierarchy ADD CONSTRAINT fk_hierarchy_parent FOREIGN KEY (parent_skill_id) REFERENCES MST_SkillHierarchy(id) ON UPDATE CASCADE ON DELETE CASCADE;

-- その他の制約
-- 制約DDL生成エラー: uk_skill_hierarchy
ALTER TABLE MST_SkillHierarchy ADD CONSTRAINT chk_hierarchy_level CHECK (hierarchy_level >= 1 AND hierarchy_level <= 5);
ALTER TABLE MST_SkillHierarchy ADD CONSTRAINT chk_skill_category CHECK (skill_category IN ('TECHNICAL', 'BUSINESS', 'CERTIFICATION', 'SOFT'));
ALTER TABLE MST_SkillHierarchy ADD CONSTRAINT chk_no_self_reference CHECK (skill_id != parent_skill_id);
