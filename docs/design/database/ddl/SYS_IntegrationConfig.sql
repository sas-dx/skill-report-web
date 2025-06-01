-- SYS_IntegrationConfig (外部連携設定) DDL
-- 生成日時: 2025-06-01 19:42:44

CREATE TABLE SYS_IntegrationConfig (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    id VARCHAR(50),
    tenant_id VARCHAR(50),
    integration_key VARCHAR(100),
    integration_name VARCHAR(200),
    integration_type ENUM,
    endpoint_url VARCHAR(500),
    auth_type ENUM,
    auth_config TEXT,
    connection_config TEXT,
    request_headers TEXT,
    timeout_seconds INTEGER DEFAULT 30,
    retry_count INTEGER DEFAULT 3,
    retry_interval INTEGER DEFAULT 5,
    rate_limit_per_minute INTEGER,
    is_enabled BOOLEAN DEFAULT True,
    health_check_url VARCHAR(500),
    last_health_check TIMESTAMP,
    health_status ENUM,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_integration_config_tenant_key ON SYS_IntegrationConfig (tenant_id, integration_key);
CREATE INDEX idx_integration_config_type ON SYS_IntegrationConfig (integration_type);
CREATE INDEX idx_integration_config_enabled ON SYS_IntegrationConfig (is_enabled);
CREATE INDEX idx_integration_config_health ON SYS_IntegrationConfig (health_status, last_health_check);
CREATE INDEX idx_integration_config_auth_type ON SYS_IntegrationConfig (auth_type);

-- 外部キー制約
