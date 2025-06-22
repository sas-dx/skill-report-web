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

-- 作成日: 2025-06-21 23:19:39
-- ============================================

DROP TABLE IF EXISTS MST_SkillCategory;

CREATE TABLE MST_SkillCategory (
    skillcategory_id SERIAL NOT NULL COMMENT 'MST_SkillCategoryの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT 'False' COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (skillcategory_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_skillcategory_tenant_id ON MST_SkillCategory (tenant_id);

-- 外部キー制約
ALTER TABLE MST_SkillCategory ADD CONSTRAINT fk_skillcategory_parent FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
