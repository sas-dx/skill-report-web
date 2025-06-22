-- ============================================
-- テーブル: MST_SkillGradeRequirement
-- 論理名: スキルグレード要件
-- 説明: MST_SkillGradeRequirement（スキルグレード要件）は、スキルグレードごとの詳細要件を管理するマスタテーブルです。

主な目的：
- スキルグレード別の詳細要件定義
- 昇格基準の明確化
- 評価項目の標準化
- 学習目標の設定
- 能力開発計画の基礎データ
- 人材評価の客観化

このテーブルにより、各スキルグレードに求められる具体的な要件を明確に定義し、
公正で透明性の高い人材評価・育成システムを構築できます。

-- 作成日: 2025-06-21 22:02:18
-- ============================================

DROP TABLE IF EXISTS MST_SkillGradeRequirement;

CREATE TABLE MST_SkillGradeRequirement (
    skillgraderequirement_id SERIAL NOT NULL COMMENT 'MST_SkillGradeRequirementの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (skillgraderequirement_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_skillgraderequirement_tenant_id ON MST_SkillGradeRequirement (tenant_id);

-- 外部キー制約
ALTER TABLE MST_SkillGradeRequirement ADD CONSTRAINT fk_MST_SkillGradeRequirement_skill_grade FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
