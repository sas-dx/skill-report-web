-- ============================================
-- テーブル: MST_CareerPlan
-- 論理名: 目標・キャリアプラン
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_CareerPlan;

CREATE TABLE MST_CareerPlan (
    career_plan_id VARCHAR(50) COMMENT 'キャリアプランを一意に識別するID',
    employee_id VARCHAR(50) COMMENT '対象社員のID（MST_Employeeへの外部キー）',
    plan_name VARCHAR(200) COMMENT 'キャリアプランの名称',
    plan_description TEXT COMMENT 'キャリアプランの詳細説明',
    plan_type ENUM COMMENT 'プランの種別（SHORT_TERM:短期、MEDIUM_TERM:中期、LONG_TERM:長期、SPECIALIZED:専門特化、MANAGEMENT:管理職、TECHNICAL:技術職）',
    target_position_id VARCHAR(50) COMMENT '目標とする役職のID（MST_Positionへの外部キー）',
    target_job_type_id VARCHAR(50) COMMENT '目標とする職種のID（MST_JobTypeへの外部キー）',
    target_department_id VARCHAR(50) COMMENT '目標とする部署のID（MST_Departmentへの外部キー）',
    current_level ENUM COMMENT '現在のキャリアレベル（ENTRY:新人、JUNIOR:初級、INTERMEDIATE:中級、SENIOR:上級、EXPERT:エキスパート、MANAGER:管理職、EXECUTIVE:役員）',
    target_level ENUM COMMENT '目標とするキャリアレベル（ENTRY:新人、JUNIOR:初級、INTERMEDIATE:中級、SENIOR:上級、EXPERT:エキスパート、MANAGER:管理職、EXECUTIVE:役員）',
    plan_start_date DATE COMMENT 'キャリアプランの開始日',
    plan_end_date DATE COMMENT 'キャリアプランの目標達成予定日',
    milestone_1_date DATE COMMENT '第1マイルストーンの目標日',
    milestone_1_description VARCHAR(500) COMMENT '第1マイルストーンの内容説明',
    milestone_2_date DATE COMMENT '第2マイルストーンの目標日',
    milestone_2_description VARCHAR(500) COMMENT '第2マイルストーンの内容説明',
    milestone_3_date DATE COMMENT '第3マイルストーンの目標日',
    milestone_3_description VARCHAR(500) COMMENT '第3マイルストーンの内容説明',
    required_skills TEXT COMMENT '目標達成に必要なスキル一覧（JSON形式）',
    required_certifications TEXT COMMENT '目標達成に必要な資格一覧（JSON形式）',
    required_experiences TEXT COMMENT '目標達成に必要な経験・実績（JSON形式）',
    development_actions TEXT COMMENT '具体的な育成・開発アクション（JSON形式）',
    training_plan TEXT COMMENT '推奨研修・教育プログラム（JSON形式）',
    mentor_id VARCHAR(50) COMMENT '指導担当者のID（MST_Employeeへの外部キー）',
    supervisor_id VARCHAR(50) COMMENT '直属上司のID（MST_Employeeへの外部キー）',
    plan_status ENUM DEFAULT 'DRAFT' COMMENT 'プランの進捗状況（DRAFT:下書き、ACTIVE:実行中、ON_HOLD:保留、COMPLETED:完了、CANCELLED:中止、REVISED:改訂）',
    progress_percentage DECIMAL(5,2) DEFAULT 0.0 COMMENT 'プランの進捗率（0.00-100.00）',
    last_review_date DATE COMMENT '最後にレビューを実施した日付',
    next_review_date DATE COMMENT '次回レビュー予定日',
    review_frequency ENUM DEFAULT 'QUARTERLY' COMMENT 'レビューの実施頻度（MONTHLY:月次、QUARTERLY:四半期、SEMI_ANNUAL:半年、ANNUAL:年次）',
    success_criteria TEXT COMMENT 'プラン成功の判定基準',
    risk_factors TEXT COMMENT '目標達成のリスク要因・課題',
    support_resources TEXT COMMENT '利用可能な支援・リソース情報',
    budget_allocated DECIMAL(10,2) COMMENT 'プラン実行のための割当予算',
    budget_used DECIMAL(10,2) DEFAULT 0.0 COMMENT '実際に使用した予算',
    priority_level ENUM DEFAULT 'NORMAL' COMMENT 'プランの優先度（LOW:低、NORMAL:通常、HIGH:高、CRITICAL:最重要）',
    visibility_level ENUM DEFAULT 'MANAGER' COMMENT 'プランの公開範囲（PRIVATE:本人のみ、MANAGER:上司まで、DEPARTMENT:部署内、COMPANY:全社）',
    template_id VARCHAR(50) COMMENT '使用したプランテンプレートのID',
    custom_fields TEXT COMMENT '組織固有の追加項目（JSON形式）',
    notes TEXT COMMENT 'その他の備考・メモ',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称',
    description TEXT COMMENT 'マスタ説明'
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

-- 外部キー制約
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_target_position FOREIGN KEY (target_position_id) REFERENCES MST_Position(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_target_job_type FOREIGN KEY (target_job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_target_department FOREIGN KEY (target_department_id) REFERENCES MST_Department(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_mentor FOREIGN KEY (mentor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_supervisor FOREIGN KEY (supervisor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
ALTER TABLE MST_CareerPlan ADD CONSTRAINT uk_career_plan_id UNIQUE ();
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
