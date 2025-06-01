-- 全テーブル統合DDL
-- 生成日時: 2025-06-01 13:03:58

-- MST_Department (部署マスタ) DDL
-- 生成日時: 2025-06-01 13:03:58

CREATE TABLE MST_Department (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    department_code VARCHAR(20),
    department_name VARCHAR(100),
    department_name_short VARCHAR(50),
    parent_department_id VARCHAR(50),
    department_level INT,
    department_type ENUM,
    manager_id VARCHAR(50),
    deputy_manager_id VARCHAR(50),
    cost_center_code VARCHAR(20),
    budget_amount DECIMAL(15,2),
    location VARCHAR(200),
    phone_number VARCHAR(20),
    email_address VARCHAR(255),
    establishment_date DATE,
    abolition_date DATE,
    department_status ENUM DEFAULT 'ACTIVE',
    sort_order INT,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_department_code ON MST_Department (department_code);
CREATE INDEX idx_parent_department ON MST_Department (parent_department_id);
CREATE INDEX idx_department_level ON MST_Department (department_level);
CREATE INDEX idx_department_type ON MST_Department (department_type);
CREATE INDEX idx_manager ON MST_Department (manager_id);
CREATE INDEX idx_status ON MST_Department (department_status);
CREATE INDEX idx_cost_center ON MST_Department (cost_center_code);
CREATE INDEX idx_sort_order ON MST_Department (sort_order);

-- 外部キー制約
ALTER TABLE MST_Department ADD CONSTRAINT fk_department_parent FOREIGN KEY (parent_department_id) REFERENCES MST_Department(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_Department ADD CONSTRAINT fk_department_manager FOREIGN KEY (manager_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_Department ADD CONSTRAINT fk_department_deputy FOREIGN KEY (deputy_manager_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;


-- MST_Position (役職マスタ) DDL
-- 生成日時: 2025-06-01 13:03:58

CREATE TABLE MST_Position (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    position_code VARCHAR(20),
    position_name VARCHAR(100),
    position_name_short VARCHAR(50),
    position_level INT,
    position_rank INT,
    position_category ENUM,
    authority_level INT,
    approval_limit DECIMAL(15,2),
    salary_grade VARCHAR(10),
    allowance_amount DECIMAL(10,2),
    is_management BOOLEAN DEFAULT False,
    is_executive BOOLEAN DEFAULT False,
    requires_approval BOOLEAN DEFAULT False,
    can_hire BOOLEAN DEFAULT False,
    can_evaluate BOOLEAN DEFAULT False,
    position_status ENUM DEFAULT 'ACTIVE',
    sort_order INT,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_position_code ON MST_Position (position_code);
CREATE INDEX idx_position_level ON MST_Position (position_level);
CREATE INDEX idx_position_rank ON MST_Position (position_rank);
CREATE INDEX idx_position_category ON MST_Position (position_category);
CREATE INDEX idx_authority_level ON MST_Position (authority_level);
CREATE INDEX idx_salary_grade ON MST_Position (salary_grade);
CREATE INDEX idx_status ON MST_Position (position_status);
CREATE INDEX idx_management_flags ON MST_Position (is_management, is_executive);
CREATE INDEX idx_sort_order ON MST_Position (sort_order);
