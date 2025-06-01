-- MST_TenantSettings (テナント設定) DDL
-- 生成日時: 2025-06-01 20:40:25

CREATE TABLE MST_TenantSettings (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    id VARCHAR(50),
    tenant_id VARCHAR(50),
    setting_category ENUM,
    setting_key VARCHAR(100),
    setting_name VARCHAR(200),
    setting_description TEXT,
    data_type ENUM,
    setting_value TEXT,
    default_value TEXT,
    validation_rules TEXT,
    is_required BOOLEAN DEFAULT False,
    is_encrypted BOOLEAN DEFAULT False,
    is_system_managed BOOLEAN DEFAULT False,
    is_user_configurable BOOLEAN DEFAULT True,
    display_order INTEGER DEFAULT 0,
    effective_from TIMESTAMP,
    effective_until TIMESTAMP,
    last_modified_by VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_tenant_settings_tenant_key ON MST_TenantSettings (tenant_id, setting_key);
CREATE INDEX idx_tenant_settings_category ON MST_TenantSettings (setting_category);
CREATE INDEX idx_tenant_settings_configurable ON MST_TenantSettings (is_user_configurable);
CREATE INDEX idx_tenant_settings_system_managed ON MST_TenantSettings (is_system_managed);
CREATE INDEX idx_tenant_settings_display_order ON MST_TenantSettings (tenant_id, setting_category, display_order);
CREATE INDEX idx_tenant_settings_effective ON MST_TenantSettings (effective_from, effective_until);

-- 外部キー制約
ALTER TABLE MST_TenantSettings ADD CONSTRAINT fk_tenant_settings_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(id) ON UPDATE CASCADE ON DELETE CASCADE;
