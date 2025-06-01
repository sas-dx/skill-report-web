-- MST_NotificationSettings (通知設定) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_NotificationSettings (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    id VARCHAR(50),
    tenant_id VARCHAR(50),
    setting_key VARCHAR(100),
    setting_name VARCHAR(200),
    notification_type ENUM,
    target_audience ENUM,
    trigger_event VARCHAR(100),
    frequency_type ENUM DEFAULT 'IMMEDIATE',
    frequency_value INTEGER,
    template_id VARCHAR(50),
    channel_config TEXT,
    is_enabled BOOLEAN DEFAULT True,
    priority_level ENUM DEFAULT 'MEDIUM',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_notification_settings_tenant_key ON MST_NotificationSettings (tenant_id, setting_key);
CREATE INDEX idx_notification_settings_type ON MST_NotificationSettings (notification_type);
CREATE INDEX idx_notification_settings_event ON MST_NotificationSettings (trigger_event);
CREATE INDEX idx_notification_settings_enabled ON MST_NotificationSettings (is_enabled);
CREATE INDEX idx_notification_settings_template ON MST_NotificationSettings (template_id);

-- 外部キー制約
ALTER TABLE MST_NotificationSettings ADD CONSTRAINT fk_notification_settings_template FOREIGN KEY (template_id) REFERENCES MST_NotificationTemplate(id) ON UPDATE CASCADE ON DELETE SET NULL;
