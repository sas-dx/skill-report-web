-- ============================================
-- テーブル: TRN_ProjectRecord
-- 論理名: 案件実績
-- 説明: TRN_ProjectRecord（案件実績）は、社員が参加したプロジェクト・案件の実績情報を管理するトランザクションテーブルです。

主な目的：
- プロジェクト参加履歴の記録・管理
- 担当役割・責任範囲の記録
- 使用技術・スキルの実績記録
- 成果・評価の記録
- キャリア形成・スキル証明の基盤

このテーブルにより、社員の実務経験を体系的に記録し、
スキル評価やキャリア開発の判断材料として活用できます。

-- 作成日: 2025-06-24 22:56:15
-- ============================================

DROP TABLE IF EXISTS TRN_ProjectRecord;

CREATE TABLE TRN_ProjectRecord (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    project_code VARCHAR(50) COMMENT 'プロジェクトコード',
    project_name VARCHAR(200) COMMENT 'プロジェクト名',
    achievements TEXT COMMENT '成果・実績',
    budget_range ENUM('UNDER_1M', 'UNDER_10M', 'UNDER_100M', 'OVER_100M') COMMENT '予算規模',
    challenges_faced TEXT COMMENT '課題・困難',
    client_name VARCHAR(100) COMMENT '顧客名',
    employee_id VARCHAR(50) COMMENT '社員ID',
    end_date DATE COMMENT '終了日',
    evaluation_comment TEXT COMMENT '評価コメント',
    evaluation_score DECIMAL(3,1) COMMENT '評価点数',
    is_confidential BOOLEAN DEFAULT False COMMENT '機密フラグ',
    is_public_reference BOOLEAN DEFAULT False COMMENT '公開参照可能フラグ',
    lessons_learned TEXT COMMENT '学んだこと',
    participation_rate DECIMAL(5,2) COMMENT '参画率',
    project_record_id VARCHAR(50) COMMENT '案件実績ID',
    project_scale ENUM('SMALL', 'MEDIUM', 'LARGE', 'ENTERPRISE') COMMENT 'プロジェクト規模',
    project_status ENUM('ONGOING', 'COMPLETED', 'SUSPENDED', 'CANCELLED') DEFAULT 'ONGOING' COMMENT 'プロジェクト状況',
    project_type ENUM('DEVELOPMENT', 'MAINTENANCE', 'CONSULTING', 'RESEARCH', 'OTHER') COMMENT 'プロジェクト種別',
    projectrecord_id INT AUTO_INCREMENT NOT NULL COMMENT 'TRN_ProjectRecordの主キー',
    responsibilities TEXT COMMENT '担当業務',
    role_title VARCHAR(100) COMMENT '担当役職',
    skills_applied TEXT COMMENT '適用スキル',
    start_date DATE COMMENT '開始日',
    team_size INTEGER COMMENT 'チーム規模',
    technologies_used TEXT COMMENT '使用技術',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    created_by VARCHAR(50) COMMENT '作成者ID',
    updated_by VARCHAR(50) COMMENT '更新者ID',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
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
CREATE INDEX idx_trn_projectrecord_tenant_id ON TRN_ProjectRecord (tenant_id);

-- 外部キー制約
ALTER TABLE TRN_ProjectRecord ADD CONSTRAINT fk_project_record_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;

-- その他の制約
-- 制約DDL生成エラー: uk_project_record_id
ALTER TABLE TRN_ProjectRecord ADD CONSTRAINT chk_project_type CHECK (project_type IN ('DEVELOPMENT', 'MAINTENANCE', 'CONSULTING', 'RESEARCH', 'OTHER'));
ALTER TABLE TRN_ProjectRecord ADD CONSTRAINT chk_project_scale CHECK (project_scale IN ('SMALL', 'MEDIUM', 'LARGE', 'ENTERPRISE'));
ALTER TABLE TRN_ProjectRecord ADD CONSTRAINT chk_budget_range CHECK (budget_range IN ('UNDER_1M', 'UNDER_10M', 'UNDER_100M', 'OVER_100M'));
ALTER TABLE TRN_ProjectRecord ADD CONSTRAINT chk_project_status CHECK (project_status IN ('ONGOING', 'COMPLETED', 'SUSPENDED', 'CANCELLED'));
ALTER TABLE TRN_ProjectRecord ADD CONSTRAINT chk_date_range CHECK (end_date IS NULL OR start_date <= end_date);
ALTER TABLE TRN_ProjectRecord ADD CONSTRAINT chk_participation_rate CHECK (participation_rate IS NULL OR (participation_rate >= 0 AND participation_rate <= 100));
ALTER TABLE TRN_ProjectRecord ADD CONSTRAINT chk_evaluation_score CHECK (evaluation_score IS NULL OR (evaluation_score >= 1.0 AND evaluation_score <= 5.0));
ALTER TABLE TRN_ProjectRecord ADD CONSTRAINT chk_team_size CHECK (team_size IS NULL OR team_size > 0);
