-- ============================================
-- テーブル: MST_JobTypeSkill
-- 論理名: 職種スキル関連
-- 説明: MST_JobTypeSkill（職種スキル関連）は、職種と必要スキルの関連付けを管理するマスタテーブルです。

主な目的：
- 職種ごとの必要スキルの定義
- スキル要求レベルの管理
- 職種別スキル要件の標準化
- 人材配置時のスキルマッチング
- 教育計画立案の基礎データ
- 採用要件定義の支援

このテーブルにより、各職種に求められるスキルセットを明確に定義し、
人材育成や配置転換の判断基準として活用できます。

-- 作成日: 2025-06-21 22:02:18
-- ============================================

DROP TABLE IF EXISTS MST_JobTypeSkill;

CREATE TABLE MST_JobTypeSkill (
    jobtypeskill_id SERIAL NOT NULL COMMENT 'MST_JobTypeSkillの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (jobtypeskill_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_jobtypeskill_tenant_id ON MST_JobTypeSkill (tenant_id);

-- 外部キー制約
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT fk_MST_JobTypeSkill_job_type FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT fk_MST_JobTypeSkill_skill_item FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
