-- MST_EmployeeDepartment (社員部署関連) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_EmployeeDepartment (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    employee_id VARCHAR(50),
    department_id VARCHAR(50),
    assignment_type ENUM DEFAULT 'PRIMARY',
    start_date DATE,
    end_date DATE,
    assignment_ratio DECIMAL(5,2),
    role_in_department VARCHAR(100),
    reporting_manager_id VARCHAR(50),
    assignment_reason VARCHAR(500),
    assignment_status ENUM DEFAULT 'ACTIVE',
    approval_status ENUM DEFAULT 'PENDING',
    approved_by VARCHAR(50),
    approved_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE INDEX idx_MST_EmployeeDepartment_employee_id ON MST_EmployeeDepartment (employee_id);
CREATE INDEX idx_MST_EmployeeDepartment_department_id ON MST_EmployeeDepartment (department_id);
CREATE INDEX idx_MST_EmployeeDepartment_employee_department ON MST_EmployeeDepartment (employee_id, department_id);
CREATE INDEX idx_MST_EmployeeDepartment_assignment_type ON MST_EmployeeDepartment (assignment_type);
CREATE INDEX idx_MST_EmployeeDepartment_start_date ON MST_EmployeeDepartment (start_date);
CREATE INDEX idx_MST_EmployeeDepartment_end_date ON MST_EmployeeDepartment (end_date);
CREATE INDEX idx_MST_EmployeeDepartment_status ON MST_EmployeeDepartment (assignment_status);

-- 外部キー制約
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT fk_MST_EmployeeDepartment_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT fk_MST_EmployeeDepartment_department FOREIGN KEY (department_id) REFERENCES MST_Department(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT fk_MST_EmployeeDepartment_reporting_manager FOREIGN KEY (reporting_manager_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT fk_MST_EmployeeDepartment_approved_by FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
