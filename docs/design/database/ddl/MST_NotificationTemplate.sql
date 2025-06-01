-- MST_NotificationTemplate (通知テンプレート) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_NotificationTemplate (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    id VARCHAR(50),
    tenant_id VARCHAR(50),
    template_key VARCHAR(100),
    template_name VARCHAR(200),
    notification_type ENUM,
    language_code VARCHAR(10) DEFAULT 'ja',
    subject_template VARCHAR(500),
    body_template TEXT,
    format_type ENUM DEFAULT 'PLAIN',
    parameters TEXT,
    sample_data TEXT,
    is_default BOOLEAN DEFAULT False,
    is_active BOOLEAN DEFAULT True,
    version VARCHAR(20) DEFAULT '1.0.0',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_notification_template_tenant_key_type ON MST_NotificationTemplate (tenant_id, template_key, notification_type, language_code);
CREATE INDEX idx_notification_template_type ON MST_NotificationTemplate (notification_type);
CREATE INDEX idx_notification_template_language ON MST_NotificationTemplate (language_code);
CREATE INDEX idx_notification_template_default ON MST_NotificationTemplate (is_default, is_active);
CREATE INDEX idx_notification_template_key ON MST_NotificationTemplate (template_key);

-- 外部キー制約
