-- MST_Tenant (テナント管理) DDL
-- 生成日時: 2025-06-01 20:40:25

CREATE TABLE MST_Tenant (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    tenant_id VARCHAR(50),
    tenant_code VARCHAR(20),
    tenant_name VARCHAR(200),
    tenant_name_en VARCHAR(200),
    tenant_short_name VARCHAR(50),
    tenant_type ENUM,
    parent_tenant_id VARCHAR(50),
    tenant_level INTEGER DEFAULT 1,
    domain_name VARCHAR(100),
    subdomain VARCHAR(50),
    logo_url VARCHAR(500),
    primary_color VARCHAR(7),
    secondary_color VARCHAR(7),
    timezone VARCHAR(50) DEFAULT 'Asia/Tokyo',
    locale VARCHAR(10) DEFAULT 'ja_JP',
    currency_code VARCHAR(3) DEFAULT 'JPY',
    date_format VARCHAR(20) DEFAULT 'YYYY-MM-DD',
    time_format VARCHAR(20) DEFAULT 'HH:mm:ss',
    admin_email VARCHAR(255),
    contact_email VARCHAR(255),
    phone_number VARCHAR(20),
    address TEXT,
    postal_code VARCHAR(10),
    country_code VARCHAR(2) DEFAULT 'JP',
    subscription_plan ENUM DEFAULT 'BASIC',
    max_users INTEGER DEFAULT 100,
    max_storage_gb INTEGER DEFAULT 10,
    features_enabled TEXT,
    custom_settings TEXT,
    security_policy TEXT,
    data_retention_days INTEGER DEFAULT 2555,
    backup_enabled BOOLEAN DEFAULT True,
    backup_frequency ENUM DEFAULT 'DAILY',
    contract_start_date DATE,
    contract_end_date DATE,
    trial_end_date DATE,
    billing_cycle ENUM DEFAULT 'MONTHLY',
    monthly_fee DECIMAL(10,2),
    setup_fee DECIMAL(10,2),
    status ENUM DEFAULT 'TRIAL',
    activation_date DATE,
    suspension_date DATE,
    suspension_reason TEXT,
    last_login_date DATE,
    current_users_count INTEGER DEFAULT 0,
    storage_used_gb DECIMAL(10,3) DEFAULT 0.0,
    api_rate_limit INTEGER DEFAULT 1000,
    sso_enabled BOOLEAN DEFAULT False,
    sso_provider VARCHAR(50),
    sso_config TEXT,
    webhook_url VARCHAR(500),
    webhook_secret VARCHAR(100),
    created_by VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_tenant_id ON MST_Tenant (tenant_id);
CREATE UNIQUE INDEX idx_tenant_code ON MST_Tenant (tenant_code);
CREATE UNIQUE INDEX idx_domain_name ON MST_Tenant (domain_name);
CREATE UNIQUE INDEX idx_subdomain ON MST_Tenant (subdomain);
CREATE INDEX idx_tenant_type ON MST_Tenant (tenant_type);
CREATE INDEX idx_parent_tenant_id ON MST_Tenant (parent_tenant_id);
CREATE INDEX idx_subscription_plan ON MST_Tenant (subscription_plan);
CREATE INDEX idx_status ON MST_Tenant (status);
CREATE INDEX idx_contract_period ON MST_Tenant (contract_start_date, contract_end_date);
CREATE INDEX idx_admin_email ON MST_Tenant (admin_email);

-- 外部キー制約
ALTER TABLE MST_Tenant ADD CONSTRAINT fk_tenant_parent FOREIGN KEY (parent_tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE SET NULL;
