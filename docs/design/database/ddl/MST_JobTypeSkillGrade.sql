-- ============================================
-- テーブル: MST_JobTypeSkillGrade
-- 論理名: 職種スキルグレード関連
-- 説明: MST_JobTypeSkillGrade（職種スキルグレード関連）は、職種とスキルグレードの関連付けを管理するマスタテーブルです。

主な目的：
- 職種ごとの必要スキルグレードの定義
- 昇進・昇格要件の明確化
- キャリアパス設計の基礎データ
- 人材評価基準の標準化
- 給与体系との連動管理
- 教育計画の目標設定

このテーブルにより、各職種に求められるスキルグレードを明確に定義し、
人材育成や昇進管理の判断基準として活用できます。

-- 作成日: 2025-06-21 22:02:17
-- ============================================

DROP TABLE IF EXISTS MST_JobTypeSkillGrade;

CREATE TABLE MST_JobTypeSkillGrade (
    jobtypeskillgrade_id SERIAL NOT NULL COMMENT 'MST_JobTypeSkillGradeの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (jobtypeskillgrade_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_jobtypeskillgrade_tenant_id ON MST_JobTypeSkillGrade (tenant_id);

-- 外部キー制約
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT fk_MST_JobTypeSkillGrade_job_type FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT fk_MST_JobTypeSkillGrade_skill_grade FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
