-- MST_EmployeePosition (社員役職関連) DDL
-- 生成日時: 2025-06-01 20:40:25

CREATE TABLE MST_EmployeePosition (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    employee_id VARCHAR(50),
    position_id VARCHAR(50),
    appointment_type ENUM DEFAULT 'PRIMARY',
    start_date DATE,
    end_date DATE,
    appointment_reason VARCHAR(500),
    responsibility_scope VARCHAR(500),
    authority_level INTEGER,
    salary_grade VARCHAR(20),
    appointment_status ENUM DEFAULT 'ACTIVE',
    approval_status ENUM DEFAULT 'PENDING',
    approved_by VARCHAR(50),
    approved_at TIMESTAMP,
    performance_target TEXT,
    delegation_authority TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

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
