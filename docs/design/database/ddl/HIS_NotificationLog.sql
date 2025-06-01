-- HIS_NotificationLog (通知送信履歴) DDL
-- 生成日時: 2025-06-01 19:42:44

CREATE TABLE HIS_NotificationLog (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    id VARCHAR(50),
    tenant_id VARCHAR(50),
    notification_id VARCHAR(50),
    setting_id VARCHAR(50),
    template_id VARCHAR(50),
    notification_type ENUM,
    recipient_type ENUM,
    recipient_address VARCHAR(500),
    subject VARCHAR(500),
    message_body TEXT,
    message_format ENUM,
    send_status ENUM,
    send_attempts INTEGER DEFAULT 0,
    max_retry_count INTEGER DEFAULT 3,
    scheduled_at TIMESTAMP,
    sent_at TIMESTAMP,
    delivered_at TIMESTAMP,
    opened_at TIMESTAMP,
    response_code VARCHAR(20),
    response_message TEXT,
    error_details TEXT,
    integration_config_id VARCHAR(50),
    priority_level ENUM DEFAULT 'MEDIUM',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE INDEX idx_notification_log_notification ON HIS_NotificationLog (notification_id);
CREATE INDEX idx_notification_log_tenant_status ON HIS_NotificationLog (tenant_id, send_status);
CREATE INDEX idx_notification_log_type ON HIS_NotificationLog (notification_type);
CREATE INDEX idx_notification_log_scheduled ON HIS_NotificationLog (scheduled_at);
CREATE INDEX idx_notification_log_sent ON HIS_NotificationLog (sent_at);
CREATE INDEX idx_notification_log_status_attempts ON HIS_NotificationLog (send_status, send_attempts);
CREATE INDEX idx_notification_log_priority ON HIS_NotificationLog (priority_level, scheduled_at);

-- 外部キー制約
ALTER TABLE HIS_NotificationLog ADD CONSTRAINT fk_notification_log_notification FOREIGN KEY (notification_id) REFERENCES TRN_Notification(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE HIS_NotificationLog ADD CONSTRAINT fk_notification_log_setting FOREIGN KEY (setting_id) REFERENCES MST_NotificationSettings(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE HIS_NotificationLog ADD CONSTRAINT fk_notification_log_template FOREIGN KEY (template_id) REFERENCES MST_NotificationTemplate(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE HIS_NotificationLog ADD CONSTRAINT fk_notification_log_integration FOREIGN KEY (integration_config_id) REFERENCES SYS_IntegrationConfig(id) ON UPDATE CASCADE ON DELETE SET NULL;
