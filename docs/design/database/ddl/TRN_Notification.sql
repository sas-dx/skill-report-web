-- ============================================
-- テーブル: TRN_Notification
-- 論理名: 通知履歴
-- 説明: TRN_Notification（通知履歴）は、システムから送信された各種通知の履歴を管理するトランザクションテーブルです。

主な目的：
- 通知送信履歴の記録・管理
- 通知配信状況の追跡
- 通知効果の分析
- 未読通知の管理
- 通知設定の最適化支援

このテーブルにより、効果的な情報伝達を実現し、
重要な情報の確実な配信と適切なコミュニケーションを支援できます。

-- 作成日: 2025-06-21 17:20:34
-- ============================================

DROP TABLE IF EXISTS TRN_Notification;

CREATE TABLE TRN_Notification (
    notification_id VARCHAR,
    recipient_id VARCHAR,
    sender_id VARCHAR,
    notification_type ENUM,
    notification_category ENUM,
    priority_level ENUM DEFAULT 'NORMAL',
    title VARCHAR,
    message TEXT,
    message_format ENUM DEFAULT 'PLAIN',
    action_url VARCHAR,
    action_label VARCHAR,
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
    external_message_id VARCHAR,
    template_id VARCHAR,
    template_variables TEXT,
    related_entity_type ENUM,
    related_entity_id VARCHAR,
    batch_id VARCHAR,
    user_agent VARCHAR,
    ip_address VARCHAR,
    device_type ENUM,
    is_bulk_notification BOOLEAN DEFAULT False,
    personalization_data TEXT,
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    created_by VARCHAR(50) NOT NULL COMMENT 'レコード作成者のユーザーID',
    updated_by VARCHAR(50) NOT NULL COMMENT 'レコード更新者のユーザーID',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時',
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
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
