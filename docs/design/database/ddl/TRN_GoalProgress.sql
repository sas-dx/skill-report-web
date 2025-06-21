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

-- 作成日: 2025-06-21 17:20:34
-- ============================================

DROP TABLE IF EXISTS TRN_GoalProgress;

CREATE TABLE TRN_GoalProgress (
    goal_id VARCHAR,
    employee_id VARCHAR,
    goal_title VARCHAR,
    goal_description TEXT,
    goal_category ENUM,
    goal_type ENUM,
    priority_level ENUM DEFAULT 'MEDIUM',
    target_value DECIMAL,
    current_value DECIMAL,
    unit VARCHAR,
    start_date DATE,
    target_date DATE,
    progress_rate DECIMAL DEFAULT 0.0,
    achievement_status ENUM DEFAULT 'NOT_STARTED',
    supervisor_id VARCHAR,
    approval_status ENUM DEFAULT 'DRAFT',
    approved_at TIMESTAMP,
    approved_by VARCHAR,
    completion_date DATE,
    achievement_rate DECIMAL,
    self_evaluation INTEGER,
    supervisor_evaluation INTEGER,
    evaluation_comments TEXT,
    related_career_plan_id VARCHAR,
    related_skill_items TEXT,
    milestones TEXT,
    obstacles TEXT,
    support_needed TEXT,
    last_updated_at TIMESTAMP,
    next_review_date DATE,
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    created_by VARCHAR(50) NOT NULL COMMENT 'レコード作成者のユーザーID',
    updated_by VARCHAR(50) NOT NULL COMMENT 'レコード更新者のユーザーID',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時',
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
