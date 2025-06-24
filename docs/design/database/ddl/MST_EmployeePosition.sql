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

-- 作成日: 2025-06-24 22:56:14
-- ============================================

DROP TABLE IF EXISTS MST_EmployeePosition;

CREATE TABLE MST_EmployeePosition (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    appointment_reason VARCHAR(500) COMMENT '任命理由',
    appointment_status ENUM('ACTIVE', 'INACTIVE', 'SUSPENDED') DEFAULT 'ACTIVE' COMMENT '任命状況',
    appointment_type ENUM('PRIMARY', 'ACTING', 'CONCURRENT') DEFAULT 'PRIMARY' COMMENT '任命区分',
    approval_status ENUM('APPROVED', 'PENDING', 'REJECTED') DEFAULT 'PENDING' COMMENT '承認状況',
    approved_at TIMESTAMP COMMENT '承認日時',
    approved_by VARCHAR(50) COMMENT '承認者ID',
    authority_level INTEGER COMMENT '権限レベル',
    delegation_authority TEXT COMMENT '委譲権限',
    employee_id VARCHAR(50) COMMENT '社員ID',
    employeeposition_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_EmployeePositionの主キー',
    end_date DATE COMMENT '任命終了日',
    performance_target TEXT COMMENT '成果目標',
    position_id VARCHAR(50) COMMENT '役職ID',
    responsibility_scope VARCHAR(500) COMMENT '責任範囲',
    salary_grade VARCHAR(20) COMMENT '給与等級',
    start_date DATE COMMENT '任命開始日',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
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
CREATE INDEX idx_mst_employeeposition_tenant_id ON MST_EmployeePosition (tenant_id);

-- 外部キー制約
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT fk_MST_EmployeePosition_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT fk_MST_EmployeePosition_position FOREIGN KEY (position_id) REFERENCES MST_Position(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT fk_MST_EmployeePosition_approved_by FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
-- 制約DDL生成エラー: uk_MST_EmployeePosition_employee_pos_primary
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT chk_MST_EmployeePosition_appointment_type CHECK (appointment_type IN ('PRIMARY', 'ACTING', 'CONCURRENT'));
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT chk_MST_EmployeePosition_appointment_status CHECK (appointment_status IN ('ACTIVE', 'INACTIVE', 'SUSPENDED'));
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT chk_MST_EmployeePosition_approval_status CHECK (approval_status IN ('APPROVED', 'PENDING', 'REJECTED'));
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT chk_MST_EmployeePosition_date_range CHECK (end_date IS NULL OR start_date <= end_date);
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT chk_MST_EmployeePosition_authority_level CHECK (authority_level IS NULL OR (authority_level >= 1 AND authority_level <= 10));
