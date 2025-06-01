-- MST_SystemConfig (システム設定) DDL
-- 生成日時: 2025-06-01 20:40:25

CREATE TABLE MST_SystemConfig (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    config_key VARCHAR(100),
    config_name VARCHAR(200),
    config_value TEXT,
    config_type ENUM,
    config_category ENUM,
    default_value TEXT,
    validation_rule TEXT,
    description TEXT,
    is_encrypted BOOLEAN DEFAULT False,
    is_system_only BOOLEAN DEFAULT False,
    is_user_configurable BOOLEAN DEFAULT True,
    requires_restart BOOLEAN DEFAULT False,
    environment ENUM DEFAULT 'ALL',
    tenant_specific BOOLEAN DEFAULT False,
    last_modified_by VARCHAR(50),
    last_modified_reason TEXT,
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT True,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_config_key ON MST_SystemConfig (config_key);
CREATE INDEX idx_config_category ON MST_SystemConfig (config_category);
CREATE INDEX idx_config_type ON MST_SystemConfig (config_type);
CREATE INDEX idx_user_configurable ON MST_SystemConfig (is_user_configurable, is_active);
CREATE INDEX idx_environment ON MST_SystemConfig (environment, is_active);
CREATE INDEX idx_tenant_specific ON MST_SystemConfig (tenant_specific, is_active);
CREATE INDEX idx_sort_order ON MST_SystemConfig (sort_order);

-- 外部キー制約
