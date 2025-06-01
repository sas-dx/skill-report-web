-- SYS_MasterData (マスタデータ全般) DDL
-- 生成日時: 2025-06-01 20:40:26

CREATE TABLE SYS_MasterData (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    master_key VARCHAR(100),
    master_category VARCHAR(50),
    master_name VARCHAR(200),
    master_value TEXT,
    data_type ENUM DEFAULT 'STRING',
    default_value TEXT,
    validation_rule TEXT,
    is_system_managed BOOLEAN DEFAULT False,
    is_editable BOOLEAN DEFAULT True,
    display_order INTEGER DEFAULT 0,
    description TEXT,
    effective_from DATE,
    effective_to DATE,
    last_modified_by VARCHAR(100),
    last_modified_at TIMESTAMP,
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_SYS_MasterData_master_key ON SYS_MasterData (master_key);
CREATE INDEX idx_SYS_MasterData_category ON SYS_MasterData (master_category);
CREATE INDEX idx_SYS_MasterData_category_order ON SYS_MasterData (master_category, display_order);
CREATE INDEX idx_SYS_MasterData_effective_period ON SYS_MasterData (effective_from, effective_to);
CREATE INDEX idx_SYS_MasterData_system_managed ON SYS_MasterData (is_system_managed);

-- 外部キー制約
