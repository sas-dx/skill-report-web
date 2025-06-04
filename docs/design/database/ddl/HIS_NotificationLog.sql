-- ============================================
-- テーブル: HIS_NotificationLog
-- 論理名: 通知送信履歴
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS HIS_NotificationLog;

CREATE TABLE HIS_NotificationLog (
    id VARCHAR(50) COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) COMMENT 'マルチテナント識別子',
    notification_id VARCHAR(50) COMMENT '送信された通知のID（TRN_Notificationへの参照）',
    setting_id VARCHAR(50) COMMENT '使用された通知設定のID（MST_NotificationSettingsへの参照）',
    template_id VARCHAR(50) COMMENT '使用された通知テンプレートのID（MST_NotificationTemplateへの参照）',
    notification_type ENUM COMMENT '送信された通知の種類（EMAIL:メール、SLACK:Slack、TEAMS:Teams、WEBHOOK:Webhook）',
    recipient_type ENUM COMMENT '受信者の種類（USER:個人、GROUP:グループ、CHANNEL:チャネル、WEBHOOK:Webhook）',
    recipient_address VARCHAR(500) COMMENT '送信先アドレス（メールアドレス、Slack チャネル等、暗号化必須）',
    subject VARCHAR(500) COMMENT '送信された通知の件名',
    message_body TEXT COMMENT '送信された通知の本文',
    message_format ENUM COMMENT 'メッセージのフォーマット（PLAIN:プレーンテキスト、HTML:HTML、MARKDOWN:Markdown）',
    send_status ENUM COMMENT '送信の状態（PENDING:送信待ち、SENDING:送信中、SUCCESS:成功、FAILED:失敗、RETRY:リトライ中）',
    send_attempts INTEGER DEFAULT 0 COMMENT '送信を試行した回数',
    max_retry_count INTEGER DEFAULT 3 COMMENT '設定された最大リトライ回数',
    scheduled_at TIMESTAMP COMMENT '送信が予定された日時',
    sent_at TIMESTAMP COMMENT '実際に送信された日時',
    delivered_at TIMESTAMP COMMENT '配信が確認された日時（対応している場合）',
    opened_at TIMESTAMP COMMENT '開封が確認された日時（メール等で対応している場合）',
    response_code VARCHAR(20) COMMENT '送信先システムからのレスポンスコード',
    response_message TEXT COMMENT '送信先システムからのレスポンスメッセージ',
    error_details TEXT COMMENT '送信失敗時のエラー詳細情報（JSON形式）',
    integration_config_id VARCHAR(50) COMMENT '使用された外部連携設定のID（SYS_IntegrationConfigへの参照）',
    priority_level ENUM DEFAULT 'MEDIUM' COMMENT '通知の優先度（HIGH:高、MEDIUM:中、LOW:低）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
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

-- その他の制約
ALTER TABLE HIS_NotificationLog ADD CONSTRAINT chk_notification_log_type CHECK (notification_type IN ('EMAIL', 'SLACK', 'TEAMS', 'WEBHOOK'));
ALTER TABLE HIS_NotificationLog ADD CONSTRAINT chk_notification_log_recipient_type CHECK (recipient_type IN ('USER', 'GROUP', 'CHANNEL', 'WEBHOOK'));
ALTER TABLE HIS_NotificationLog ADD CONSTRAINT chk_notification_log_format CHECK (message_format IN ('PLAIN', 'HTML', 'MARKDOWN'));
ALTER TABLE HIS_NotificationLog ADD CONSTRAINT chk_notification_log_status CHECK (send_status IN ('PENDING', 'SENDING', 'SUCCESS', 'FAILED', 'RETRY'));
ALTER TABLE HIS_NotificationLog ADD CONSTRAINT chk_notification_log_priority CHECK (priority_level IN ('HIGH', 'MEDIUM', 'LOW'));
ALTER TABLE HIS_NotificationLog ADD CONSTRAINT chk_notification_log_attempts_positive CHECK (send_attempts >= 0 AND max_retry_count >= 0);
ALTER TABLE HIS_NotificationLog ADD CONSTRAINT chk_notification_log_attempts_limit CHECK (send_attempts <= max_retry_count + 1);
