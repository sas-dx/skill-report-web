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

-- 作成日: 2025-06-21 17:20:35
-- ============================================

DROP TABLE IF EXISTS HIS_NotificationLog;

CREATE TABLE HIS_NotificationLog (
    id VARCHAR,
    tenant_id VARCHAR,
    notification_id VARCHAR,
    setting_id VARCHAR,
    template_id VARCHAR,
    notification_type ENUM,
    recipient_type ENUM,
    recipient_address VARCHAR,
    subject VARCHAR,
    message_body TEXT,
    message_format ENUM,
    send_status ENUM,
    send_attempts INTEGER DEFAULT 0,
    max_retry_count INTEGER DEFAULT 3,
    scheduled_at TIMESTAMP,
    sent_at TIMESTAMP,
    delivered_at TIMESTAMP,
    opened_at TIMESTAMP,
    response_code VARCHAR,
    response_message TEXT,
    error_details TEXT,
    integration_config_id VARCHAR,
    priority_level ENUM DEFAULT 'MEDIUM',
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
