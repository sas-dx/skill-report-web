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

-- 作成日: 2025-06-24 23:02:18
-- ============================================

DROP TABLE IF EXISTS MST_CareerPlan;

CREATE TABLE MST_CareerPlan (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    plan_name VARCHAR(200) COMMENT 'プラン名',
    budget_allocated DECIMAL(10,2) COMMENT '割当予算',
    budget_used DECIMAL(10,2) DEFAULT 0.0 COMMENT '使用予算',
    career_plan_id VARCHAR(50) COMMENT 'キャリアプランID',
    careerplan_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_CareerPlanの主キー',
    current_level ENUM('ENTRY', 'JUNIOR', 'INTERMEDIATE', 'SENIOR', 'EXPERT', 'MANAGER', 'EXECUTIVE') COMMENT '現在レベル',
    custom_fields TEXT COMMENT 'カスタムフィールド',
    development_actions TEXT COMMENT '育成アクション',
    employee_id VARCHAR(50) COMMENT '社員ID',
    last_review_date DATE COMMENT '最終レビュー日',
    mentor_id VARCHAR(50) COMMENT 'メンターID',
    milestone_1_date DATE COMMENT 'マイルストーン1日付',
    milestone_1_description VARCHAR(500) COMMENT 'マイルストーン1説明',
    milestone_2_date DATE COMMENT 'マイルストーン2日付',
    milestone_2_description VARCHAR(500) COMMENT 'マイルストーン2説明',
    milestone_3_date DATE COMMENT 'マイルストーン3日付',
    milestone_3_description VARCHAR(500) COMMENT 'マイルストーン3説明',
    next_review_date DATE COMMENT '次回レビュー日',
    notes TEXT COMMENT '備考',
    plan_description TEXT COMMENT 'プラン説明',
    plan_end_date DATE COMMENT 'プラン終了日',
    plan_start_date DATE COMMENT 'プラン開始日',
    plan_status ENUM('DRAFT', 'ACTIVE', 'ON_HOLD', 'COMPLETED', 'CANCELLED', 'REVISED') DEFAULT 'DRAFT' COMMENT 'プラン状況',
    plan_type ENUM('SHORT_TERM', 'MEDIUM_TERM', 'LONG_TERM', 'SPECIALIZED', 'MANAGEMENT', 'TECHNICAL') COMMENT 'プラン種別',
    priority_level ENUM('LOW', 'NORMAL', 'HIGH', 'CRITICAL') DEFAULT 'NORMAL' COMMENT '優先度',
    progress_percentage DECIMAL(5,2) DEFAULT 0.0 COMMENT '進捗率',
    required_certifications TEXT COMMENT '必要資格',
    required_experiences TEXT COMMENT '必要経験',
    required_skills TEXT COMMENT '必要スキル',
    review_frequency ENUM('MONTHLY', 'QUARTERLY', 'SEMI_ANNUAL', 'ANNUAL') DEFAULT 'QUARTERLY' COMMENT 'レビュー頻度',
    risk_factors TEXT COMMENT 'リスク要因',
    success_criteria TEXT COMMENT '成功基準',
    supervisor_id VARCHAR(50) COMMENT '上司ID',
    support_resources TEXT COMMENT '支援リソース',
    target_department_id VARCHAR(50) COMMENT '目標部署ID',
    target_job_type_id VARCHAR(50) COMMENT '目標職種ID',
    target_level ENUM('ENTRY', 'JUNIOR', 'INTERMEDIATE', 'SENIOR', 'EXPERT', 'MANAGER', 'EXECUTIVE') COMMENT '目標レベル',
    target_position_id VARCHAR(50) COMMENT '目標役職ID',
    template_id VARCHAR(50) COMMENT 'テンプレートID',
    training_plan TEXT COMMENT '研修計画',
    visibility_level ENUM('PRIVATE', 'MANAGER', 'DEPARTMENT', 'COMPANY') DEFAULT 'MANAGER' COMMENT '公開レベル',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
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
CREATE INDEX idx_mst_careerplan_tenant_id ON MST_CareerPlan (tenant_id);

-- 外部キー制約
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_target_position FOREIGN KEY (target_position_id) REFERENCES MST_Position(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_target_job_type FOREIGN KEY (target_job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_target_department FOREIGN KEY (target_department_id) REFERENCES MST_Department(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_mentor FOREIGN KEY (mentor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_supervisor FOREIGN KEY (supervisor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
-- 制約DDL生成エラー: uk_career_plan_id
ALTER TABLE MST_CareerPlan ADD CONSTRAINT chk_plan_type CHECK (plan_type IN ('SHORT_TERM', 'MEDIUM_TERM', 'LONG_TERM', 'SPECIALIZED', 'MANAGEMENT', 'TECHNICAL'));
ALTER TABLE MST_CareerPlan ADD CONSTRAINT chk_current_level CHECK (current_level IN ('ENTRY', 'JUNIOR', 'INTERMEDIATE', 'SENIOR', 'EXPERT', 'MANAGER', 'EXECUTIVE'));
ALTER TABLE MST_CareerPlan ADD CONSTRAINT chk_target_level CHECK (target_level IN ('ENTRY', 'JUNIOR', 'INTERMEDIATE', 'SENIOR', 'EXPERT', 'MANAGER', 'EXECUTIVE'));
ALTER TABLE MST_CareerPlan ADD CONSTRAINT chk_plan_status CHECK (plan_status IN ('DRAFT', 'ACTIVE', 'ON_HOLD', 'COMPLETED', 'CANCELLED', 'REVISED'));
ALTER TABLE MST_CareerPlan ADD CONSTRAINT chk_review_frequency CHECK (review_frequency IN ('MONTHLY', 'QUARTERLY', 'SEMI_ANNUAL', 'ANNUAL'));
ALTER TABLE MST_CareerPlan ADD CONSTRAINT chk_priority_level CHECK (priority_level IN ('LOW', 'NORMAL', 'HIGH', 'CRITICAL'));
ALTER TABLE MST_CareerPlan ADD CONSTRAINT chk_visibility_level CHECK (visibility_level IN ('PRIVATE', 'MANAGER', 'DEPARTMENT', 'COMPANY'));
ALTER TABLE MST_CareerPlan ADD CONSTRAINT chk_plan_period CHECK (plan_start_date <= plan_end_date);
ALTER TABLE MST_CareerPlan ADD CONSTRAINT chk_progress_percentage CHECK (progress_percentage >= 0.00 AND progress_percentage <= 100.00);
ALTER TABLE MST_CareerPlan ADD CONSTRAINT chk_budget_positive CHECK (budget_allocated IS NULL OR budget_allocated >= 0);
ALTER TABLE MST_CareerPlan ADD CONSTRAINT chk_budget_used_positive CHECK (budget_used >= 0);
