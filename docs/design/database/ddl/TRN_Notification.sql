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

-- 作成日: 2025-06-24 23:05:56
-- ============================================

DROP TABLE IF EXISTS TRN_Notification;

CREATE TABLE TRN_Notification (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    batch_id VARCHAR(50) COMMENT 'バッチID',
    notification_id VARCHAR(50) COMMENT '通知ID',
    title VARCHAR(200) COMMENT 'タイトル',
    message TEXT COMMENT 'メッセージ',
    action_label VARCHAR(50) COMMENT 'アクションラベル',
    action_url VARCHAR(500) COMMENT 'アクションURL',
    archived_at TIMESTAMP COMMENT 'アーカイブ日時',
    delivered_at TIMESTAMP COMMENT '配信日時',
    delivery_method ENUM('IN_APP', 'EMAIL', 'SLACK', 'TEAMS', 'LINE_WORKS', 'SMS') COMMENT '配信方法',
    delivery_status ENUM('PENDING', 'SENT', 'DELIVERED', 'FAILED', 'BOUNCED') DEFAULT 'PENDING' COMMENT '配信状況',
    device_type ENUM('PC', 'MOBILE', 'TABLET') COMMENT 'デバイス種別',
    error_message TEXT COMMENT 'エラーメッセージ',
    expiry_date DATE COMMENT '有効期限',
    external_message_id VARCHAR(100) COMMENT '外部メッセージID',
    ip_address VARCHAR(45) COMMENT 'IPアドレス',
    is_bulk_notification BOOLEAN DEFAULT False COMMENT '一括通知フラグ',
    last_retry_at TIMESTAMP COMMENT '最終再送日時',
    max_retry_count INTEGER DEFAULT 3 COMMENT '最大再送回数',
    message_format ENUM('PLAIN', 'HTML', 'MARKDOWN') DEFAULT 'PLAIN' COMMENT 'メッセージ形式',
    notification_category ENUM('SKILL', 'TRAINING', 'PROJECT', 'CERTIFICATION', 'SYSTEM', 'HR') COMMENT '通知カテゴリ',
    notification_type ENUM('SYSTEM', 'REMINDER', 'APPROVAL', 'ALERT', 'INFO', 'URGENT') COMMENT '通知種別',
    personalization_data TEXT COMMENT 'パーソナライゼーションデータ',
    priority_level ENUM('LOW', 'NORMAL', 'HIGH', 'CRITICAL') DEFAULT 'NORMAL' COMMENT '優先度',
    read_at TIMESTAMP COMMENT '既読日時',
    read_status ENUM('UNREAD', 'READ', 'ARCHIVED') DEFAULT 'UNREAD' COMMENT '既読状況',
    recipient_id VARCHAR(50) COMMENT '受信者ID',
    related_entity_id VARCHAR(50) COMMENT '関連エンティティID',
    related_entity_type ENUM('PROJECT', 'TRAINING', 'CERTIFICATION', 'SKILL', 'EMPLOYEE') COMMENT '関連エンティティ種別',
    retry_count INTEGER DEFAULT 0 COMMENT '再送回数',
    sender_id VARCHAR(50) COMMENT '送信者ID',
    sent_at TIMESTAMP COMMENT '送信日時',
    template_id VARCHAR(50) COMMENT 'テンプレートID',
    template_variables TEXT COMMENT 'テンプレート変数',
    user_agent VARCHAR(500) COMMENT 'ユーザーエージェント',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    created_by VARCHAR(50) COMMENT '作成者ID',
    updated_by VARCHAR(50) COMMENT '更新者ID',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
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
CREATE INDEX idx_trn_notification_tenant_id ON TRN_Notification (tenant_id);

-- 外部キー制約
ALTER TABLE TRN_Notification ADD CONSTRAINT fk_notification_recipient FOREIGN KEY (recipient_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_Notification ADD CONSTRAINT fk_notification_sender FOREIGN KEY (sender_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
-- 制約DDL生成エラー: uk_notification_id
ALTER TABLE TRN_Notification ADD CONSTRAINT chk_notification_type CHECK (notification_type IN ('SYSTEM', 'REMINDER', 'APPROVAL', 'ALERT', 'INFO', 'URGENT'));
ALTER TABLE TRN_Notification ADD CONSTRAINT chk_notification_category CHECK (notification_category IN ('SKILL', 'TRAINING', 'PROJECT', 'CERTIFICATION', 'SYSTEM', 'HR'));
ALTER TABLE TRN_Notification ADD CONSTRAINT chk_priority_level CHECK (priority_level IN ('LOW', 'NORMAL', 'HIGH', 'CRITICAL'));
ALTER TABLE TRN_Notification ADD CONSTRAINT chk_message_format CHECK (message_format IN ('PLAIN', 'HTML', 'MARKDOWN'));
ALTER TABLE TRN_Notification ADD CONSTRAINT chk_delivery_method CHECK (delivery_method IN ('IN_APP', 'EMAIL', 'SLACK', 'TEAMS', 'LINE_WORKS', 'SMS'));
ALTER TABLE TRN_Notification ADD CONSTRAINT chk_delivery_status CHECK (delivery_status IN ('PENDING', 'SENT', 'DELIVERED', 'FAILED', 'BOUNCED'));
ALTER TABLE TRN_Notification ADD CONSTRAINT chk_read_status CHECK (read_status IN ('UNREAD', 'READ', 'ARCHIVED'));
ALTER TABLE TRN_Notification ADD CONSTRAINT chk_related_entity_type CHECK (related_entity_type IN ('PROJECT', 'TRAINING', 'CERTIFICATION', 'SKILL', 'EMPLOYEE'));
ALTER TABLE TRN_Notification ADD CONSTRAINT chk_device_type CHECK (device_type IN ('PC', 'MOBILE', 'TABLET'));
ALTER TABLE TRN_Notification ADD CONSTRAINT chk_retry_count CHECK (retry_count >= 0 AND retry_count <= max_retry_count);
ALTER TABLE TRN_Notification ADD CONSTRAINT chk_max_retry_count CHECK (max_retry_count >= 0);
