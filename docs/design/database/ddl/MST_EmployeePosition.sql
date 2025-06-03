-- ============================================
-- テーブル: MST_EmployeePosition
-- 論理名: 社員役職関連
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_EmployeePosition;

CREATE TABLE MST_EmployeePosition (
    employee_id VARCHAR(50) COMMENT '社員のID（MST_Employeeへの外部キー）',
    position_id VARCHAR(50) COMMENT '役職のID（MST_Positionへの外部キー）',
    appointment_type ENUM DEFAULT 'PRIMARY' COMMENT '任命区分（PRIMARY:主役職、ACTING:代理、CONCURRENT:兼任）',
    start_date DATE COMMENT '役職への任命開始日',
    end_date DATE COMMENT '役職からの任命終了日（NULL:現在も任命中）',
    appointment_reason VARCHAR(500) COMMENT '任命・昇進・降格の理由',
    responsibility_scope VARCHAR(500) COMMENT '当該役職での責任範囲・職務内容',
    authority_level INTEGER COMMENT '権限レベル（1-10、数値が大きいほど高権限）',
    salary_grade VARCHAR(20) COMMENT '役職に対応する給与等級',
    appointment_status ENUM DEFAULT 'ACTIVE' COMMENT '任命状況（ACTIVE:有効、INACTIVE:無効、SUSPENDED:停止）',
    approval_status ENUM DEFAULT 'PENDING' COMMENT '承認状況（APPROVED:承認済、PENDING:承認待ち、REJECTED:却下）',
    approved_by VARCHAR(50) COMMENT '任命を承認した管理者のID',
    approved_at TIMESTAMP COMMENT '任命が承認された日時',
    performance_target TEXT COMMENT '当該役職での成果目標・KPI',
    delegation_authority TEXT COMMENT '委譲された権限の詳細（JSON形式）',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称',
    description TEXT COMMENT 'マスタ説明'
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

-- 外部キー制約
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT fk_MST_EmployeePosition_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT fk_MST_EmployeePosition_position FOREIGN KEY (position_id) REFERENCES MST_Position(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT fk_MST_EmployeePosition_approved_by FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT uk_MST_EmployeePosition_employee_pos_primary UNIQUE ();
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT chk_MST_EmployeePosition_appointment_type CHECK (appointment_type IN ('PRIMARY', 'ACTING', 'CONCURRENT'));
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT chk_MST_EmployeePosition_appointment_status CHECK (appointment_status IN ('ACTIVE', 'INACTIVE', 'SUSPENDED'));
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT chk_MST_EmployeePosition_approval_status CHECK (approval_status IN ('APPROVED', 'PENDING', 'REJECTED'));
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT chk_MST_EmployeePosition_date_range CHECK (end_date IS NULL OR start_date <= end_date);
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT chk_MST_EmployeePosition_authority_level CHECK (authority_level IS NULL OR (authority_level >= 1 AND authority_level <= 10));
