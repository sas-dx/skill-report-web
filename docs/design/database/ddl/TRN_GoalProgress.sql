-- ============================================
-- テーブル: TRN_GoalProgress
-- 論理名: 目標進捗
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS TRN_GoalProgress;

CREATE TABLE TRN_GoalProgress (
    goal_id VARCHAR(50) COMMENT '目標を一意に識別するID（例：GOAL000001）',
    employee_id VARCHAR(50) COMMENT '目標を設定した社員のID（MST_Employeeへの外部キー）',
    goal_title VARCHAR(200) COMMENT '目標の簡潔なタイトル',
    goal_description TEXT COMMENT '目標の詳細説明・背景・期待効果',
    goal_category ENUM COMMENT '目標のカテゴリ（BUSINESS:業務、SKILL:スキル、CAREER:キャリア、PERSONAL:個人）',
    goal_type ENUM COMMENT '目標種別（QUANTITATIVE:定量、QUALITATIVE:定性、MILESTONE:マイルストーン）',
    priority_level ENUM DEFAULT 'MEDIUM' COMMENT '目標の優先度（HIGH:高、MEDIUM:中、LOW:低）',
    target_value DECIMAL(15,2) COMMENT '定量目標の目標値',
    current_value DECIMAL(15,2) COMMENT '定量目標の現在値',
    unit VARCHAR(50) COMMENT '目標値・現在値の単位（件、円、%等）',
    start_date DATE COMMENT '目標の開始日',
    target_date DATE COMMENT '目標達成の期限日',
    progress_rate DECIMAL(5,2) DEFAULT 0.0 COMMENT '目標の進捗率（0.00-100.00%）',
    achievement_status ENUM DEFAULT 'NOT_STARTED' COMMENT '達成状況（NOT_STARTED:未着手、IN_PROGRESS:進行中、COMPLETED:完了、OVERDUE:期限超過、CANCELLED:中止）',
    supervisor_id VARCHAR(50) COMMENT '目標を承認・管理する上司のID（MST_Employeeへの外部キー）',
    approval_status ENUM DEFAULT 'DRAFT' COMMENT '承認状況（DRAFT:下書き、PENDING:承認待ち、APPROVED:承認済み、REJECTED:却下）',
    approved_at TIMESTAMP COMMENT '目標が承認された日時',
    approved_by VARCHAR(50) COMMENT '目標を承認した人のID（MST_Employeeへの外部キー）',
    completion_date DATE COMMENT '目標が完了した日',
    achievement_rate DECIMAL(5,2) COMMENT '最終的な達成率（0.00-100.00%）',
    self_evaluation INTEGER COMMENT '本人による自己評価（1-5段階）',
    supervisor_evaluation INTEGER COMMENT '上司による評価（1-5段階）',
    evaluation_comments TEXT COMMENT '評価に関するコメント・フィードバック',
    related_career_plan_id VARCHAR(50) COMMENT '関連するキャリアプランのID（MST_CareerPlanへの外部キー）',
    related_skill_items TEXT COMMENT '関連するスキル項目のリスト（JSON形式）',
    milestones TEXT COMMENT '目標達成のマイルストーン（JSON形式）',
    obstacles TEXT COMMENT '目標達成の障害・課題（JSON形式）',
    support_needed TEXT COMMENT '目標達成に必要なサポート・リソース',
    last_updated_at TIMESTAMP COMMENT '進捗が最後に更新された日時',
    next_review_date DATE COMMENT '次回の進捗レビュー予定日',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'マルチテナント識別子',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT 'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP' COMMENT 'レコード更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT 'レコード作成者のユーザーID',
    updated_by VARCHAR(50) NOT NULL COMMENT 'レコード更新者のユーザーID',
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_TRN_GoalProgress_goal_id ON TRN_GoalProgress (goal_id);
CREATE INDEX idx_TRN_GoalProgress_employee_id ON TRN_GoalProgress (employee_id);
CREATE INDEX idx_TRN_GoalProgress_supervisor_id ON TRN_GoalProgress (supervisor_id);
CREATE INDEX idx_TRN_GoalProgress_category ON TRN_GoalProgress (goal_category);
CREATE INDEX idx_TRN_GoalProgress_status ON TRN_GoalProgress (achievement_status);
CREATE INDEX idx_TRN_GoalProgress_approval_status ON TRN_GoalProgress (approval_status);
CREATE INDEX idx_TRN_GoalProgress_target_date ON TRN_GoalProgress (target_date);
CREATE INDEX idx_TRN_GoalProgress_priority ON TRN_GoalProgress (priority_level);
CREATE INDEX idx_TRN_GoalProgress_employee_period ON TRN_GoalProgress (employee_id, start_date, target_date);
CREATE INDEX idx_TRN_GoalProgress_next_review ON TRN_GoalProgress (next_review_date);

-- 外部キー制約
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_supervisor FOREIGN KEY (supervisor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_approved_by FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_career_plan FOREIGN KEY (related_career_plan_id) REFERENCES MST_CareerPlan(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT uk_TRN_GoalProgress_goal_id UNIQUE ();
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT chk_TRN_GoalProgress_category CHECK (goal_category IN ('BUSINESS', 'SKILL', 'CAREER', 'PERSONAL'));
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT chk_TRN_GoalProgress_type CHECK (goal_type IN ('QUANTITATIVE', 'QUALITATIVE', 'MILESTONE'));
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT chk_TRN_GoalProgress_priority CHECK (priority_level IN ('HIGH', 'MEDIUM', 'LOW'));
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT chk_TRN_GoalProgress_progress_rate CHECK (progress_rate >= 0 AND progress_rate <= 100);
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT chk_TRN_GoalProgress_achievement_status CHECK (achievement_status IN ('NOT_STARTED', 'IN_PROGRESS', 'COMPLETED', 'OVERDUE', 'CANCELLED'));
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT chk_TRN_GoalProgress_approval_status CHECK (approval_status IN ('DRAFT', 'PENDING', 'APPROVED', 'REJECTED'));
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT chk_TRN_GoalProgress_achievement_rate CHECK (achievement_rate IS NULL OR (achievement_rate >= 0 AND achievement_rate <= 100));
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT chk_TRN_GoalProgress_self_evaluation CHECK (self_evaluation IS NULL OR (self_evaluation >= 1 AND self_evaluation <= 5));
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT chk_TRN_GoalProgress_supervisor_evaluation CHECK (supervisor_evaluation IS NULL OR (supervisor_evaluation >= 1 AND supervisor_evaluation <= 5));
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT chk_TRN_GoalProgress_date_range CHECK (start_date <= target_date);
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT chk_TRN_GoalProgress_target_value CHECK (target_value IS NULL OR target_value >= 0);
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT chk_TRN_GoalProgress_current_value CHECK (current_value IS NULL OR current_value >= 0);
