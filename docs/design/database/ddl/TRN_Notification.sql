-- ============================================
-- テーブル: TRN_Notification
-- 論理名: 通知履歴
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS TRN_Notification;

CREATE TABLE TRN_Notification (
    notification_id VARCHAR(50) COMMENT '通知を一意に識別するID',
    recipient_id VARCHAR(50) COMMENT '通知受信者の社員ID（MST_Employeeへの外部キー）',
    sender_id VARCHAR(50) COMMENT '通知送信者の社員ID（システム送信の場合はNULL）',
    notification_type ENUM COMMENT '通知の種別（SYSTEM:システム、REMINDER:リマインダー、APPROVAL:承認、ALERT:アラート、INFO:情報、URGENT:緊急）',
    notification_category ENUM COMMENT '通知の分類（SKILL:スキル関連、TRAINING:研修関連、PROJECT:プロジェクト関連、CERTIFICATION:資格関連、SYSTEM:システム関連、HR:人事関連）',
    priority_level ENUM DEFAULT 'NORMAL' COMMENT '通知の優先度（LOW:低、NORMAL:通常、HIGH:高、CRITICAL:緊急）',
    title VARCHAR(200) COMMENT '通知のタイトル・件名',
    message TEXT COMMENT '通知の本文メッセージ',
    message_format ENUM DEFAULT 'PLAIN' COMMENT 'メッセージの形式（PLAIN:プレーンテキスト、HTML:HTML、MARKDOWN:Markdown）',
    action_url VARCHAR(500) COMMENT '通知に関連するアクションのURL',
    action_label VARCHAR(50) COMMENT 'アクションボタンのラベル',
    delivery_method ENUM COMMENT '通知の配信方法（IN_APP:アプリ内、EMAIL:メール、SLACK:Slack、TEAMS:Teams、LINE_WORKS:LINE WORKS、SMS:SMS）',
    delivery_status ENUM DEFAULT 'PENDING' COMMENT '配信状況（PENDING:配信待ち、SENT:送信済み、DELIVERED:配信完了、FAILED:配信失敗、BOUNCED:バウンス）',
    sent_at TIMESTAMP COMMENT '通知が送信された日時',
    delivered_at TIMESTAMP COMMENT '通知が配信された日時',
    read_status ENUM DEFAULT 'UNREAD' COMMENT '既読状況（UNREAD:未読、READ:既読、ARCHIVED:アーカイブ済み）',
    read_at TIMESTAMP COMMENT '通知が既読になった日時',
    archived_at TIMESTAMP COMMENT '通知がアーカイブされた日時',
    expiry_date DATE COMMENT '通知の有効期限',
    retry_count INTEGER DEFAULT 0 COMMENT '配信失敗時の再送回数',
    max_retry_count INTEGER DEFAULT 3 COMMENT '最大再送回数',
    last_retry_at TIMESTAMP COMMENT '最後に再送を試行した日時',
    error_message TEXT COMMENT '配信失敗時のエラーメッセージ',
    external_message_id VARCHAR(100) COMMENT '外部サービス（メール、Slack等）のメッセージID',
    template_id VARCHAR(50) COMMENT '使用した通知テンプレートのID',
    template_variables TEXT COMMENT 'テンプレートに渡した変数（JSON形式）',
    related_entity_type ENUM COMMENT '関連するエンティティの種別（PROJECT:プロジェクト、TRAINING:研修、CERTIFICATION:資格、SKILL:スキル、EMPLOYEE:社員）',
    related_entity_id VARCHAR(50) COMMENT '関連するエンティティのID',
    batch_id VARCHAR(50) COMMENT '一括送信時のバッチID',
    user_agent VARCHAR(500) COMMENT '既読時のユーザーエージェント情報',
    ip_address VARCHAR(45) COMMENT '既読時のIPアドレス',
    device_type ENUM COMMENT '既読時のデバイス種別（PC:PC、MOBILE:モバイル、TABLET:タブレット）',
    is_bulk_notification BOOLEAN DEFAULT False COMMENT '一括送信された通知かどうか',
    personalization_data TEXT COMMENT '個人向けカスタマイズデータ（JSON形式）',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'マルチテナント識別子',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT 'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP' COMMENT 'レコード更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT 'レコード作成者のユーザーID',
    updated_by VARCHAR(50) NOT NULL COMMENT 'レコード更新者のユーザーID',
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

-- 外部キー制約
ALTER TABLE TRN_Notification ADD CONSTRAINT fk_notification_recipient FOREIGN KEY (recipient_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_Notification ADD CONSTRAINT fk_notification_sender FOREIGN KEY (sender_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
ALTER TABLE TRN_Notification ADD CONSTRAINT uk_notification_id UNIQUE ();
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
