-- TRN_Notification (通知履歴) DDL
-- 生成日時: 2025-06-01 20:40:26

CREATE TABLE TRN_Notification (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    notification_id VARCHAR(50),
    recipient_id VARCHAR(50),
    sender_id VARCHAR(50),
    notification_type ENUM,
    notification_category ENUM,
    priority_level ENUM DEFAULT 'NORMAL',
    title VARCHAR(200),
    message TEXT,
    message_format ENUM DEFAULT 'PLAIN',
    action_url VARCHAR(500),
    action_label VARCHAR(50),
    delivery_method ENUM,
    delivery_status ENUM DEFAULT 'PENDING',
    sent_at TIMESTAMP,
    delivered_at TIMESTAMP,
    read_status ENUM DEFAULT 'UNREAD',
    read_at TIMESTAMP,
    archived_at TIMESTAMP,
    expiry_date DATE,
    retry_count INTEGER DEFAULT 0,
    max_retry_count INTEGER DEFAULT 3,
    last_retry_at TIMESTAMP,
    error_message TEXT,
    external_message_id VARCHAR(100),
    template_id VARCHAR(50),
    template_variables TEXT,
    related_entity_type ENUM,
    related_entity_id VARCHAR(50),
    batch_id VARCHAR(50),
    user_agent VARCHAR(500),
    ip_address VARCHAR(45),
    device_type ENUM,
    is_bulk_notification BOOLEAN DEFAULT False,
    personalization_data TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_notification_id ON TRN_Notification (notification_id);
CREATE INDEX idx_recipient_id ON TRN_Notification (recipient_id);
CREATE INDEX idx_sender_id ON TRN_Notification (sender_id);
CREATE INDEX idx_notification_type ON TRN_Notification (notification_type);
CREATE INDEX idx_notification_category ON TRN_Notification (notification_category);
CREATE INDEX idx_priority_level ON TRN_Notification (priority_level);
CREATE INDEX idx_delivery_method ON TRN_Notification (delivery_method);
CREATE INDEX idx_delivery_status ON TRN_Notification (delivery_status);
CREATE INDEX idx_read_status ON TRN_Notification (read_status);
CREATE INDEX idx_sent_at ON TRN_Notification (sent_at);
CREATE INDEX idx_recipient_unread ON TRN_Notification (recipient_id, read_status, expiry_date);
CREATE INDEX idx_batch_id ON TRN_Notification (batch_id);
CREATE INDEX idx_related_entity ON TRN_Notification (related_entity_type, related_entity_id);

-- 外部キー制約
ALTER TABLE TRN_Notification ADD CONSTRAINT fk_notification_recipient FOREIGN KEY (recipient_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_Notification ADD CONSTRAINT fk_notification_sender FOREIGN KEY (sender_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
