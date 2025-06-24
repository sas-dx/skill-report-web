-- ============================================
-- テーブル: MST_NotificationSettings
-- 論理名: 通知設定
-- 説明: MST_NotificationSettings（通知設定）は、システム全体の通知機能に関する設定情報を管理するマスタテーブルです。

主な目的：
- 通知チャネル（メール、Slack、Teams等）の設定管理
- 通知タイミング・頻度の制御設定
- 通知対象者・グループの設定管理
- 通知テンプレートとの紐付け設定
- テナント別通知設定の管理

このテーブルは、通知・連携管理機能の基盤となる重要なマスタデータです。

-- 作成日: 2025-06-24 23:02:17
-- ============================================

DROP TABLE IF EXISTS MST_NotificationSettings;

CREATE TABLE MST_NotificationSettings (
    id VARCHAR(50) COMMENT 'ID',
    tenant_id VARCHAR(50) COMMENT 'テナントID',
    channel_config TEXT COMMENT 'チャネル設定',
    frequency_type ENUM('IMMEDIATE', 'DAILY', 'WEEKLY', 'MONTHLY') DEFAULT 'IMMEDIATE' COMMENT '頻度タイプ',
    frequency_value INTEGER COMMENT '頻度値',
    is_enabled BOOLEAN DEFAULT True COMMENT '有効フラグ',
    notification_type ENUM('EMAIL', 'SLACK', 'TEAMS', 'WEBHOOK') COMMENT '通知タイプ',
    notificationsettings_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_NotificationSettingsの主キー',
    priority_level ENUM('HIGH', 'MEDIUM', 'LOW') DEFAULT 'MEDIUM' COMMENT '優先度レベル',
    setting_key VARCHAR(100) COMMENT '設定キー',
    setting_name VARCHAR(200) COMMENT '設定名',
    target_audience ENUM('ALL', 'MANAGER', 'EMPLOYEE', 'CUSTOM') COMMENT '対象者',
    template_id VARCHAR(50) COMMENT 'テンプレートID',
    trigger_event VARCHAR(100) COMMENT 'トリガーイベント',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_notification_settings_tenant_key ON MST_NotificationSettings (tenant_id, setting_key);
CREATE INDEX idx_notification_settings_type ON MST_NotificationSettings (notification_type);
CREATE INDEX idx_notification_settings_event ON MST_NotificationSettings (trigger_event);
CREATE INDEX idx_notification_settings_enabled ON MST_NotificationSettings (is_enabled);
CREATE INDEX idx_notification_settings_template ON MST_NotificationSettings (template_id);
CREATE INDEX idx_mst_notificationsettings_tenant_id ON MST_NotificationSettings (tenant_id);

-- 外部キー制約
ALTER TABLE MST_NotificationSettings ADD CONSTRAINT fk_notification_settings_template FOREIGN KEY (template_id) REFERENCES MST_NotificationTemplate(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
-- 制約DDL生成エラー: uk_notification_settings_tenant_key
ALTER TABLE MST_NotificationSettings ADD CONSTRAINT chk_notification_settings_type CHECK (notification_type IN ('EMAIL', 'SLACK', 'TEAMS', 'WEBHOOK'));
ALTER TABLE MST_NotificationSettings ADD CONSTRAINT chk_notification_settings_audience CHECK (target_audience IN ('ALL', 'MANAGER', 'EMPLOYEE', 'CUSTOM'));
ALTER TABLE MST_NotificationSettings ADD CONSTRAINT chk_notification_settings_frequency CHECK (frequency_type IN ('IMMEDIATE', 'DAILY', 'WEEKLY', 'MONTHLY'));
ALTER TABLE MST_NotificationSettings ADD CONSTRAINT chk_notification_settings_priority CHECK (priority_level IN ('HIGH', 'MEDIUM', 'LOW'));
