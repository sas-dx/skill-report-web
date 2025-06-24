-- ============================================
-- テーブル: TRN_GoalProgress
-- 論理名: 目標進捗
-- 説明: TRN_GoalProgress（目標進捗）は、社員個人の目標設定と進捗状況を管理するトランザクションテーブルです。

主な目的：
- 個人目標の設定・管理（業務目標、スキル向上目標等）
- 目標達成度の定期的な進捗管理
- 上司・部下間での目標共有・フィードバック
- 人事評価・査定の基礎データ
- 組織目標と個人目標の連携管理
- 目標設定から達成までのプロセス管理
- 成果測定・KPI管理
- 人材育成計画の基礎データ

このテーブルは、人事評価制度、目標管理制度（MBO）、人材育成など、
組織の成果管理と人材開発の基盤となる重要なデータを提供します。

-- 作成日: 2025-06-24 23:02:19
-- ============================================

DROP TABLE IF EXISTS TRN_GoalProgress;

CREATE TABLE TRN_GoalProgress (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    achievement_rate DECIMAL(5,2) COMMENT '達成率',
    achievement_status ENUM('NOT_STARTED', 'IN_PROGRESS', 'COMPLETED', 'OVERDUE', 'CANCELLED') DEFAULT 'NOT_STARTED' COMMENT '達成状況',
    approval_status ENUM('DRAFT', 'PENDING', 'APPROVED', 'REJECTED') DEFAULT 'DRAFT' COMMENT '承認状況',
    approved_at TIMESTAMP COMMENT '承認日時',
    approved_by VARCHAR(50) COMMENT '承認者ID',
    completion_date DATE COMMENT '完了日',
    current_value DECIMAL(15,2) COMMENT '現在値',
    employee_id VARCHAR(50) COMMENT '社員ID',
    evaluation_comments TEXT COMMENT '評価コメント',
    goal_category ENUM('BUSINESS', 'SKILL', 'CAREER', 'PERSONAL') COMMENT '目標カテゴリ',
    goal_description TEXT COMMENT '目標詳細',
    goal_id VARCHAR(50) COMMENT '目標ID',
    goal_title VARCHAR(200) COMMENT '目標タイトル',
    goal_type ENUM('QUANTITATIVE', 'QUALITATIVE', 'MILESTONE') COMMENT '目標種別',
    goalprogress_id INT AUTO_INCREMENT NOT NULL COMMENT 'TRN_GoalProgressの主キー',
    last_updated_at TIMESTAMP COMMENT '最終更新日時',
    milestones TEXT COMMENT 'マイルストーン',
    next_review_date DATE COMMENT '次回レビュー日',
    obstacles TEXT COMMENT '障害・課題',
    priority_level ENUM('HIGH', 'MEDIUM', 'LOW') DEFAULT 'MEDIUM' COMMENT '優先度',
    progress_rate DECIMAL(5,2) DEFAULT 0.0 COMMENT '進捗率',
    related_career_plan_id VARCHAR(50) COMMENT '関連キャリアプランID',
    related_skill_items TEXT COMMENT '関連スキル項目',
    self_evaluation INTEGER COMMENT '自己評価',
    start_date DATE COMMENT '開始日',
    supervisor_evaluation INTEGER COMMENT '上司評価',
    supervisor_id VARCHAR(50) COMMENT '上司ID',
    support_needed TEXT COMMENT '必要サポート',
    target_date DATE COMMENT '目標期限',
    target_value DECIMAL(15,2) COMMENT '目標値',
    unit VARCHAR(50) COMMENT '単位',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    created_by VARCHAR(50) COMMENT '作成者ID',
    updated_by VARCHAR(50) COMMENT '更新者ID',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
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
CREATE INDEX idx_trn_goalprogress_tenant_id ON TRN_GoalProgress (tenant_id);

-- 外部キー制約
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_supervisor FOREIGN KEY (supervisor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_approved_by FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_career_plan FOREIGN KEY (related_career_plan_id) REFERENCES MST_CareerPlan(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
-- 制約DDL生成エラー: uk_TRN_GoalProgress_goal_id
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
