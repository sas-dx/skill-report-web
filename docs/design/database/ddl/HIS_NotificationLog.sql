-- ============================================
-- テーブル: HIS_NotificationLog
-- 論理名: 通知送信履歴
-- 説明: HIS_NotificationLog（通知送信履歴）は、システムから送信された全ての通知の履歴を管理するテーブルです。

主な目的：
- 通知送信の履歴管理
- 送信成功・失敗の記録
- 通知配信の監査証跡
- 通知システムの分析・改善データ
- 再送処理のための情報管理

このテーブルは、通知・連携管理機能において送信状況の把握と品質向上を支える重要な履歴データです。

-- 作成日: 2025-06-24 23:02:18
-- ============================================

DROP TABLE IF EXISTS HIS_NotificationLog;

CREATE TABLE HIS_NotificationLog (
    id VARCHAR(50) COMMENT 'ID',
    tenant_id VARCHAR(50) COMMENT 'テナントID',
    notification_id VARCHAR(50) COMMENT '通知ID',
    subject VARCHAR(500) COMMENT '件名',
    delivered_at TIMESTAMP COMMENT '配信確認日時',
    error_details TEXT COMMENT 'エラー詳細',
    integration_config_id VARCHAR(50) COMMENT '連携設定ID',
    max_retry_count INTEGER DEFAULT 3 COMMENT '最大リトライ回数',
    message_body TEXT COMMENT 'メッセージ本文',
    message_format ENUM('PLAIN', 'HTML', 'MARKDOWN') COMMENT 'メッセージフォーマット',
    notification_type ENUM('EMAIL', 'SLACK', 'TEAMS', 'WEBHOOK') COMMENT '通知タイプ',
    notificationlog_id INT AUTO_INCREMENT NOT NULL COMMENT 'HIS_NotificationLogの主キー',
    opened_at TIMESTAMP COMMENT '開封日時',
    priority_level ENUM('HIGH', 'MEDIUM', 'LOW') DEFAULT 'MEDIUM' COMMENT '優先度レベル',
    recipient_address VARCHAR(500) COMMENT '受信者アドレス',
    recipient_type ENUM('USER', 'GROUP', 'CHANNEL', 'WEBHOOK') COMMENT '受信者タイプ',
    response_code VARCHAR(20) COMMENT 'レスポンスコード',
    response_message TEXT COMMENT 'レスポンスメッセージ',
    scheduled_at TIMESTAMP COMMENT '送信予定日時',
    send_attempts INTEGER DEFAULT 0 COMMENT '送信試行回数',
    send_status ENUM('PENDING', 'SENDING', 'SUCCESS', 'FAILED', 'RETRY') COMMENT '送信状態',
    sent_at TIMESTAMP COMMENT '送信日時',
    setting_id VARCHAR(50) COMMENT '設定ID',
    template_id VARCHAR(50) COMMENT 'テンプレートID',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_notification_log_notification ON HIS_NotificationLog (notification_id);
CREATE INDEX idx_notification_log_tenant_status ON HIS_NotificationLog (tenant_id, send_status);
CREATE INDEX idx_notification_log_type ON HIS_NotificationLog (notification_type);
CREATE INDEX idx_notification_log_scheduled ON HIS_NotificationLog (scheduled_at);
CREATE INDEX idx_notification_log_sent ON HIS_NotificationLog (sent_at);
CREATE INDEX idx_notification_log_status_attempts ON HIS_NotificationLog (send_status, send_attempts);
CREATE INDEX idx_notification_log_priority ON HIS_NotificationLog (priority_level, scheduled_at);
CREATE INDEX idx_his_notificationlog_tenant_id ON HIS_NotificationLog (tenant_id);

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
