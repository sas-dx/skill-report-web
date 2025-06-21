-- ============================================
-- テーブル: MST_EmployeePosition
-- 論理名: 社員役職関連
-- 説明: MST_EmployeePosition（社員役職関連）は、社員と役職の関連付けを管理するマスタテーブルです。

主な目的：
- 社員の役職任命履歴の管理
- 複数役職兼任の管理
- 昇進・降格履歴の追跡
- 役職変更時の影響範囲把握
- 役職別権限管理
- 組織階層における権限委譲の管理

このテーブルにより、社員の役職変遷を詳細に管理し、
人事評価や昇進管理の履歴を正確に追跡できます。

-- 作成日: 2025-06-21 17:20:34
-- ============================================

DROP TABLE IF EXISTS MST_EmployeePosition;

CREATE TABLE MST_EmployeePosition (
    employee_id VARCHAR,
    position_id VARCHAR,
    appointment_type ENUM DEFAULT 'PRIMARY',
    start_date DATE,
    end_date DATE,
    appointment_reason VARCHAR,
    responsibility_scope VARCHAR,
    authority_level INTEGER,
    salary_grade VARCHAR,
    appointment_status ENUM DEFAULT 'ACTIVE',
    approval_status ENUM DEFAULT 'PENDING',
    approved_by VARCHAR,
    approved_at TIMESTAMP,
    performance_target TEXT,
    delegation_authority TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_MST_EmployeePosition_employee_id ON MST_EmployeePosition (employee_id);
CREATE INDEX idx_MST_EmployeePosition_position_id ON MST_EmployeePosition (position_id);
CREATE INDEX idx_MST_EmployeePosition_employee_position ON MST_EmployeePosition (employee_id, position_id);
CREATE INDEX idx_MST_EmployeePosition_appointment_type ON MST_EmployeePosition (appointment_type);
CREATE INDEX idx_MST_EmployeePosition_start_date ON MST_EmployeePosition (start_date);
CREATE INDEX idx_MST_EmployeePosition_end_date ON MST_EmployeePosition (end_date);
CREATE INDEX idx_MST_EmployeePosition_status ON MST_EmployeePosition (appointment_status);
CREATE INDEX idx_MST_EmployeePosition_authority_level ON MST_EmployeePosition (authority_level);
