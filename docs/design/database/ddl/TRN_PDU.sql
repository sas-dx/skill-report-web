-- ============================================
-- テーブル: TRN_PDU
-- 論理名: 継続教育ポイント
-- 説明: TRN_PDU（継続教育ポイント）は、社員が取得した継続教育ポイント（Professional Development Units）を管理するトランザクションテーブルです。

主な目的：
- PDU取得履歴の記録・管理
- 資格維持要件の追跡
- 学習活動の定量化
- 継続教育計画の進捗管理
- 資格更新の支援

このテーブルにより、社員の継続的な学習活動を体系的に記録し、
資格維持や専門性向上の支援を効率的に行うことができます。

-- 作成日: 2025-06-21 17:20:35
-- ============================================

DROP TABLE IF EXISTS TRN_PDU;

CREATE TABLE TRN_PDU (
    pdu_id VARCHAR,
    employee_id VARCHAR,
    certification_id VARCHAR,
    activity_type ENUM,
    activity_name VARCHAR,
    activity_description TEXT,
    provider_name VARCHAR,
    activity_date DATE,
    start_time TIME,
    end_time TIME,
    duration_hours DECIMAL,
    pdu_points DECIMAL,
    pdu_category ENUM,
    pdu_subcategory VARCHAR,
    location VARCHAR,
    cost DECIMAL,
    cost_covered_by ENUM,
    evidence_type ENUM,
    evidence_file_path VARCHAR,
    certificate_number VARCHAR,
    instructor_name VARCHAR,
    learning_objectives TEXT,
    learning_outcomes TEXT,
    skills_developed TEXT,
    approval_status ENUM DEFAULT 'PENDING',
    approved_by VARCHAR,
    approval_date DATE,
    approval_comment TEXT,
    expiry_date DATE,
    is_recurring BOOLEAN DEFAULT False,
    recurrence_pattern VARCHAR,
    related_training_id VARCHAR,
    related_project_id VARCHAR,
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    created_by VARCHAR(50) NOT NULL COMMENT 'レコード作成者のユーザーID',
    updated_by VARCHAR(50) NOT NULL COMMENT 'レコード更新者のユーザーID',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時',
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_pdu_id ON TRN_PDU (pdu_id);
CREATE INDEX idx_employee_id ON TRN_PDU (employee_id);
CREATE INDEX idx_certification_id ON TRN_PDU (certification_id);
CREATE INDEX idx_activity_type ON TRN_PDU (activity_type);
CREATE INDEX idx_activity_date ON TRN_PDU (activity_date);
CREATE INDEX idx_pdu_category ON TRN_PDU (pdu_category);
CREATE INDEX idx_approval_status ON TRN_PDU (approval_status);
CREATE INDEX idx_employee_period ON TRN_PDU (employee_id, activity_date);
CREATE INDEX idx_expiry_date ON TRN_PDU (expiry_date);
CREATE INDEX idx_certification_employee ON TRN_PDU (certification_id, employee_id, approval_status);
