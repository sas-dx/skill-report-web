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

-- 作成日: 2025-06-21 17:20:35
-- ============================================

DROP TABLE IF EXISTS MST_CareerPlan;

CREATE TABLE MST_CareerPlan (
    career_plan_id VARCHAR,
    employee_id VARCHAR,
    plan_name VARCHAR,
    plan_description TEXT,
    plan_type ENUM,
    target_position_id VARCHAR,
    target_job_type_id VARCHAR,
    target_department_id VARCHAR,
    current_level ENUM,
    target_level ENUM,
    plan_start_date DATE,
    plan_end_date DATE,
    milestone_1_date DATE,
    milestone_1_description VARCHAR,
    milestone_2_date DATE,
    milestone_2_description VARCHAR,
    milestone_3_date DATE,
    milestone_3_description VARCHAR,
    required_skills TEXT,
    required_certifications TEXT,
    required_experiences TEXT,
    development_actions TEXT,
    training_plan TEXT,
    mentor_id VARCHAR,
    supervisor_id VARCHAR,
    plan_status ENUM DEFAULT 'DRAFT',
    progress_percentage DECIMAL DEFAULT 0.0,
    last_review_date DATE,
    next_review_date DATE,
    review_frequency ENUM DEFAULT 'QUARTERLY',
    success_criteria TEXT,
    risk_factors TEXT,
    support_resources TEXT,
    budget_allocated DECIMAL,
    budget_used DECIMAL DEFAULT 0.0,
    priority_level ENUM DEFAULT 'NORMAL',
    visibility_level ENUM DEFAULT 'MANAGER',
    template_id VARCHAR,
    custom_fields TEXT,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_career_plan_id ON MST_CareerPlan (career_plan_id);
CREATE INDEX idx_employee_id ON MST_CareerPlan (employee_id);
CREATE INDEX idx_plan_type ON MST_CareerPlan (plan_type);
CREATE INDEX idx_target_position ON MST_CareerPlan (target_position_id);
CREATE INDEX idx_target_job_type ON MST_CareerPlan (target_job_type_id);
CREATE INDEX idx_plan_status ON MST_CareerPlan (plan_status);
CREATE INDEX idx_plan_period ON MST_CareerPlan (plan_start_date, plan_end_date);
CREATE INDEX idx_review_date ON MST_CareerPlan (next_review_date);
CREATE INDEX idx_mentor_id ON MST_CareerPlan (mentor_id);
CREATE INDEX idx_supervisor_id ON MST_CareerPlan (supervisor_id);
CREATE INDEX idx_priority_level ON MST_CareerPlan (priority_level);
