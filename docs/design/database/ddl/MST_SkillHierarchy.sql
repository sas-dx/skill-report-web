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

-- 作成日: 2025-06-21 22:02:18
-- ============================================

DROP TABLE IF EXISTS MST_SkillHierarchy;

CREATE TABLE MST_SkillHierarchy (
    skillhierarchy_id SERIAL NOT NULL COMMENT 'MST_SkillHierarchyの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (skillhierarchy_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_skillhierarchy_tenant_id ON MST_SkillHierarchy (tenant_id);

-- 外部キー制約
ALTER TABLE MST_SkillHierarchy ADD CONSTRAINT fk_hierarchy_skill FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_SkillHierarchy ADD CONSTRAINT fk_hierarchy_parent FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
