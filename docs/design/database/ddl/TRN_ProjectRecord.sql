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

-- 作成日: 2025-06-21 17:20:34
-- ============================================

DROP TABLE IF EXISTS TRN_ProjectRecord;

CREATE TABLE TRN_ProjectRecord (
    project_record_id VARCHAR,
    employee_id VARCHAR,
    project_name VARCHAR,
    project_code VARCHAR,
    client_name VARCHAR,
    project_type ENUM,
    project_scale ENUM,
    start_date DATE,
    end_date DATE,
    participation_rate DECIMAL,
    role_title VARCHAR,
    responsibilities TEXT,
    technologies_used TEXT,
    skills_applied TEXT,
    achievements TEXT,
    challenges_faced TEXT,
    lessons_learned TEXT,
    team_size INTEGER,
    budget_range ENUM,
    project_status ENUM DEFAULT 'ONGOING',
    evaluation_score DECIMAL,
    evaluation_comment TEXT,
    is_confidential BOOLEAN DEFAULT False,
    is_public_reference BOOLEAN DEFAULT False,
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    created_by VARCHAR(50) NOT NULL COMMENT 'レコード作成者のユーザーID',
    updated_by VARCHAR(50) NOT NULL COMMENT 'レコード更新者のユーザーID',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時',
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
