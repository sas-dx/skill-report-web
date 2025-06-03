-- ============================================
-- テーブル: TRN_ProjectRecord
-- 論理名: 案件実績
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS TRN_ProjectRecord;

CREATE TABLE TRN_ProjectRecord (
    project_record_id VARCHAR(50) COMMENT '案件実績を一意に識別するID',
    employee_id VARCHAR(50) COMMENT '参加した社員のID（MST_Employeeへの外部キー）',
    project_name VARCHAR(200) COMMENT 'プロジェクト・案件の名称',
    project_code VARCHAR(50) COMMENT '社内プロジェクト管理コード',
    client_name VARCHAR(100) COMMENT '顧客・クライアント名（機密情報のため暗号化）',
    project_type ENUM COMMENT 'プロジェクトの種別（DEVELOPMENT:開発、MAINTENANCE:保守、CONSULTING:コンサル、RESEARCH:研究、OTHER:その他）',
    project_scale ENUM COMMENT 'プロジェクトの規模（SMALL:小規模、MEDIUM:中規模、LARGE:大規模、ENTERPRISE:エンタープライズ）',
    start_date DATE COMMENT 'プロジェクト参加開始日',
    end_date DATE COMMENT 'プロジェクト参加終了日（進行中の場合はNULL）',
    participation_rate DECIMAL(5,2) COMMENT 'プロジェクトへの参画率（%）',
    role_title VARCHAR(100) COMMENT 'プロジェクト内での役職・ポジション',
    responsibilities TEXT COMMENT '具体的な担当業務・責任範囲',
    technologies_used TEXT COMMENT 'プロジェクトで使用した技術・ツール（JSON形式）',
    skills_applied TEXT COMMENT 'プロジェクトで活用したスキル（JSON形式）',
    achievements TEXT COMMENT 'プロジェクトでの具体的な成果・実績',
    challenges_faced TEXT COMMENT '直面した課題や困難とその対応',
    lessons_learned TEXT COMMENT 'プロジェクトから学んだ知識・経験',
    team_size INTEGER COMMENT 'プロジェクトチームの人数',
    budget_range ENUM COMMENT 'プロジェクトの予算規模（UNDER_1M:100万円未満、UNDER_10M:1000万円未満、UNDER_100M:1億円未満、OVER_100M:1億円以上）',
    project_status ENUM DEFAULT 'ONGOING' COMMENT 'プロジェクトの状況（ONGOING:進行中、COMPLETED:完了、SUSPENDED:中断、CANCELLED:中止）',
    evaluation_score DECIMAL(3,1) COMMENT 'プロジェクトでの評価点数（1.0-5.0）',
    evaluation_comment TEXT COMMENT '上司・PMからの評価コメント',
    is_confidential BOOLEAN DEFAULT False COMMENT '機密プロジェクトかどうか',
    is_public_reference BOOLEAN DEFAULT False COMMENT '社外への参照情報として公開可能か',
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
CREATE UNIQUE INDEX idx_project_record_id ON TRN_ProjectRecord (project_record_id);
CREATE INDEX idx_employee_id ON TRN_ProjectRecord (employee_id);
CREATE INDEX idx_project_name ON TRN_ProjectRecord (project_name);
CREATE INDEX idx_project_code ON TRN_ProjectRecord (project_code);
CREATE INDEX idx_project_type ON TRN_ProjectRecord (project_type);
CREATE INDEX idx_date_range ON TRN_ProjectRecord (start_date, end_date);
CREATE INDEX idx_project_status ON TRN_ProjectRecord (project_status);
CREATE INDEX idx_employee_period ON TRN_ProjectRecord (employee_id, start_date, end_date);

-- 外部キー制約
ALTER TABLE TRN_ProjectRecord ADD CONSTRAINT fk_project_record_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;

-- その他の制約
ALTER TABLE TRN_ProjectRecord ADD CONSTRAINT uk_project_record_id UNIQUE ();
ALTER TABLE TRN_ProjectRecord ADD CONSTRAINT chk_project_type CHECK (project_type IN ('DEVELOPMENT', 'MAINTENANCE', 'CONSULTING', 'RESEARCH', 'OTHER'));
ALTER TABLE TRN_ProjectRecord ADD CONSTRAINT chk_project_scale CHECK (project_scale IN ('SMALL', 'MEDIUM', 'LARGE', 'ENTERPRISE'));
ALTER TABLE TRN_ProjectRecord ADD CONSTRAINT chk_budget_range CHECK (budget_range IN ('UNDER_1M', 'UNDER_10M', 'UNDER_100M', 'OVER_100M'));
ALTER TABLE TRN_ProjectRecord ADD CONSTRAINT chk_project_status CHECK (project_status IN ('ONGOING', 'COMPLETED', 'SUSPENDED', 'CANCELLED'));
ALTER TABLE TRN_ProjectRecord ADD CONSTRAINT chk_date_range CHECK (end_date IS NULL OR start_date <= end_date);
ALTER TABLE TRN_ProjectRecord ADD CONSTRAINT chk_participation_rate CHECK (participation_rate IS NULL OR (participation_rate >= 0 AND participation_rate <= 100));
ALTER TABLE TRN_ProjectRecord ADD CONSTRAINT chk_evaluation_score CHECK (evaluation_score IS NULL OR (evaluation_score >= 1.0 AND evaluation_score <= 5.0));
ALTER TABLE TRN_ProjectRecord ADD CONSTRAINT chk_team_size CHECK (team_size IS NULL OR team_size > 0);
