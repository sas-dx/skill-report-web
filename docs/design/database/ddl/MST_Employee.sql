-- MST_Employee (社員基本情報) DDL
-- 生成日時: 2025-06-01 15:57:34

CREATE TABLE MST_Employee (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    employee_code VARCHAR(30),
    full_name VARCHAR(100),
    full_name_kana VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(20),
    hire_date DATE,
    birth_date DATE,
    gender ENUM,
    department_id VARCHAR(50),
    position_id VARCHAR(50),
    job_type_id VARCHAR(50),
    employment_status ENUM DEFAULT 'FULL_TIME',
    manager_id VARCHAR(50),
    employee_status ENUM DEFAULT 'ACTIVE',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_employee_code ON MST_Employee (employee_code);
CREATE UNIQUE INDEX idx_email ON MST_Employee (email);
CREATE INDEX idx_department ON MST_Employee (department_id);
CREATE INDEX idx_manager ON MST_Employee (manager_id);
CREATE INDEX idx_status ON MST_Employee (employee_status);
CREATE INDEX idx_hire_date ON MST_Employee (hire_date);

-- 外部キー制約
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_department FOREIGN KEY (department_id) REFERENCES MST_Department(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_position FOREIGN KEY (position_id) REFERENCES MST_Position(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_job_type FOREIGN KEY (job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_manager FOREIGN KEY (manager_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
