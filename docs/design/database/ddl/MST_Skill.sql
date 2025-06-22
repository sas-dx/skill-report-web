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

-- 作成日: 2025-06-21 23:19:39
-- ============================================

DROP TABLE IF EXISTS MST_Skill;

CREATE TABLE MST_Skill (
    skill_id SERIAL NOT NULL COMMENT 'MST_Skillの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT 'False' COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (skill_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_skill_tenant_id ON MST_Skill (tenant_id);

-- 外部キー制約
ALTER TABLE MST_Skill ADD CONSTRAINT fk_MST_Skill_tenant FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_Skill ADD CONSTRAINT fk_MST_Skill_category FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE RESTRICT;
