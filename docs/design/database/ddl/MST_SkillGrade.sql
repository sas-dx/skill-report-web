-- ============================================
-- テーブル: MST_SkillGrade
-- 論理名: スキルグレードマスタ
-- 説明: MST_SkillGrade（スキルグレードマスタ）は、スキルの習熟度レベルを定義・管理するマスタテーブルです。

主な目的：
- スキル習熟度の標準化・統一
- スキル評価基準の明確化
- 職種別スキル要件の定義基盤
- スキル成長パスの可視化
- 人材育成計画の策定支援

このテーブルにより、組織全体で統一されたスキル評価基準を確立し、
社員のスキル開発と適切な人材配置を効率的に行うことができます。

-- 作成日: 2025-06-21 23:19:39
-- ============================================

DROP TABLE IF EXISTS MST_SkillGrade;

CREATE TABLE MST_SkillGrade (
    skillgrade_id SERIAL NOT NULL COMMENT 'MST_SkillGradeの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT 'False' COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (skillgrade_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_skillgrade_tenant_id ON MST_SkillGrade (tenant_id);
