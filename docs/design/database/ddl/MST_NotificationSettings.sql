-- ============================================
-- テーブル: MST_NotificationSettings
-- 論理名: 通知設定
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_NotificationSettings;

CREATE TABLE MST_NotificationSettings (
    id VARCHAR(50) COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) COMMENT 'マルチテナント識別子',
    setting_key VARCHAR(100) COMMENT '通知設定の識別キー（例：skill_update_notification、goal_reminder等）',
    setting_name VARCHAR(200) COMMENT '通知設定の表示名',
    notification_type ENUM COMMENT '通知の種類（EMAIL:メール、SLACK:Slack、TEAMS:Teams、WEBHOOK:Webhook）',
    target_audience ENUM COMMENT '通知対象（ALL:全員、MANAGER:管理者、EMPLOYEE:一般社員、CUSTOM:カスタム）',
    trigger_event VARCHAR(100) COMMENT '通知を発生させるイベント（例：skill_registered、goal_deadline_approaching等）',
    frequency_type ENUM DEFAULT 'IMMEDIATE' COMMENT '通知頻度（IMMEDIATE:即座、DAILY:日次、WEEKLY:週次、MONTHLY:月次）',
    frequency_value INTEGER COMMENT '頻度の具体的な値（日次の場合は時間、週次の場合は曜日等）',
    template_id VARCHAR(50) COMMENT '使用する通知テンプレートのID（MST_NotificationTemplateへの参照）',
    channel_config TEXT COMMENT '通知チャネル固有の設定情報（JSON形式）',
    is_enabled BOOLEAN DEFAULT True COMMENT '通知設定が有効かどうか',
    priority_level ENUM DEFAULT 'MEDIUM' COMMENT '通知の優先度（HIGH:高、MEDIUM:中、LOW:低）',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称',
    description TEXT COMMENT 'マスタ説明'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_notification_settings_tenant_key ON MST_NotificationSettings (tenant_id, setting_key);
CREATE INDEX idx_notification_settings_type ON MST_NotificationSettings (notification_type);
CREATE INDEX idx_notification_settings_event ON MST_NotificationSettings (trigger_event);
CREATE INDEX idx_notification_settings_enabled ON MST_NotificationSettings (is_enabled);
CREATE INDEX idx_notification_settings_template ON MST_NotificationSettings (template_id);

-- 外部キー制約
ALTER TABLE MST_NotificationSettings ADD CONSTRAINT fk_notification_settings_template FOREIGN KEY (template_id) REFERENCES MST_NotificationTemplate(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
ALTER TABLE MST_NotificationSettings ADD CONSTRAINT uk_notification_settings_tenant_key UNIQUE ();
ALTER TABLE MST_NotificationSettings ADD CONSTRAINT chk_notification_settings_type CHECK (notification_type IN ('EMAIL', 'SLACK', 'TEAMS', 'WEBHOOK'));
ALTER TABLE MST_NotificationSettings ADD CONSTRAINT chk_notification_settings_audience CHECK (target_audience IN ('ALL', 'MANAGER', 'EMPLOYEE', 'CUSTOM'));
ALTER TABLE MST_NotificationSettings ADD CONSTRAINT chk_notification_settings_frequency CHECK (frequency_type IN ('IMMEDIATE', 'DAILY', 'WEEKLY', 'MONTHLY'));
ALTER TABLE MST_NotificationSettings ADD CONSTRAINT chk_notification_settings_priority CHECK (priority_level IN ('HIGH', 'MEDIUM', 'LOW'));
