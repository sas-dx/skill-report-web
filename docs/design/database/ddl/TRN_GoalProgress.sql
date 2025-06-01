-- TRN_GoalProgress (目標進捗) DDL
-- 生成日時: 2025-06-01 13:28:12

CREATE TABLE TRN_GoalProgress (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    employee_id VARCHAR(50),
    goal_title VARCHAR(200),
    goal_category ENUM,
    target_date DATE,
    progress_rate DECIMAL(5,2) DEFAULT 0.0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE INDEX idx_employee ON TRN_GoalProgress (employee_id);
