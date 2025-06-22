-- ============================================
-- テーブル: MST_CareerPlan
-- 論理名: 目標・キャリアプラン
-- 説明: MST_CareerPlan（目標・キャリアプラン）は、社員の中長期的なキャリア目標と成長計画を管理するマスタテーブルです。

主な目的：
- キャリア目標の設定・管理
- 成長計画の策定支援
- スキル開発ロードマップの提供
- 人事評価・昇進判定の基準設定
- 人材育成計画の立案支援

このテーブルにより、個人の成長と組織の人材戦略を連携させ、
効果的なキャリア開発と人材育成を実現できます。

-- 作成日: 2025-06-21 22:02:18
-- ============================================

DROP TABLE IF EXISTS MST_CareerPlan;

CREATE TABLE MST_CareerPlan (
    careerplan_id SERIAL NOT NULL COMMENT 'MST_CareerPlanの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (careerplan_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_careerplan_tenant_id ON MST_CareerPlan (tenant_id);

-- 外部キー制約
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_employee FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_target_position FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_target_job_type FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_target_department FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_mentor FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_supervisor FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
