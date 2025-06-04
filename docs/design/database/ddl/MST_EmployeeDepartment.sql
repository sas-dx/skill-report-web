-- ============================================
-- テーブル: MST_EmployeeDepartment
-- 論理名: 社員部署関連
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_EmployeeDepartment;

CREATE TABLE MST_EmployeeDepartment (
    employee_id VARCHAR(50) COMMENT '社員のID（MST_Employeeへの外部キー）',
    department_id VARCHAR(50) COMMENT '部署のID（MST_Departmentへの外部キー）',
    assignment_type ENUM DEFAULT 'PRIMARY' COMMENT '配属区分（PRIMARY:主配属、SECONDARY:兼務、TEMPORARY:一時配属）',
    start_date DATE COMMENT '部署への配属開始日',
    end_date DATE COMMENT '部署からの配属終了日（NULL:現在も配属中）',
    assignment_ratio DECIMAL(5,2) COMMENT '配属比率（%）兼務時の工数配分用',
    role_in_department VARCHAR(100) COMMENT '部署内での役割・職責',
    reporting_manager_id VARCHAR(50) COMMENT '当該部署での報告先上司ID（MST_Employeeへの外部キー）',
    assignment_reason VARCHAR(500) COMMENT '配属・異動の理由',
    assignment_status ENUM DEFAULT 'ACTIVE' COMMENT '配属状況（ACTIVE:有効、INACTIVE:無効、PENDING:保留）',
    approval_status ENUM DEFAULT 'PENDING' COMMENT '承認状況（APPROVED:承認済、PENDING:承認待ち、REJECTED:却下）',
    approved_by VARCHAR(50) COMMENT '配属を承認した管理者のID',
    approved_at TIMESTAMP COMMENT '配属が承認された日時',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称',
    description TEXT COMMENT 'マスタ説明'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
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

-- その他の制約
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT uk_MST_EmployeeDepartment_employee_dept_primary UNIQUE ();
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT chk_MST_EmployeeDepartment_assignment_type CHECK (assignment_type IN ('PRIMARY', 'SECONDARY', 'TEMPORARY'));
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT chk_MST_EmployeeDepartment_assignment_status CHECK (assignment_status IN ('ACTIVE', 'INACTIVE', 'PENDING'));
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT chk_MST_EmployeeDepartment_approval_status CHECK (approval_status IN ('APPROVED', 'PENDING', 'REJECTED'));
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT chk_MST_EmployeeDepartment_date_range CHECK (end_date IS NULL OR start_date <= end_date);
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT chk_MST_EmployeeDepartment_assignment_ratio CHECK (assignment_ratio IS NULL OR (assignment_ratio >= 0 AND assignment_ratio <= 100));
