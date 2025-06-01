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
