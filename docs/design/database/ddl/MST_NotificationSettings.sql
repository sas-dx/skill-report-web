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

-- 作成日: 2025-06-21 17:20:34
-- ============================================

DROP TABLE IF EXISTS MST_NotificationSettings;

CREATE TABLE MST_NotificationSettings (
    id VARCHAR,
    tenant_id VARCHAR,
    setting_key VARCHAR,
    setting_name VARCHAR,
    notification_type ENUM,
    target_audience ENUM,
    trigger_event VARCHAR,
    frequency_type ENUM DEFAULT 'IMMEDIATE',
    frequency_value INTEGER,
    template_id VARCHAR,
    channel_config TEXT,
    is_enabled BOOLEAN DEFAULT True,
    priority_level ENUM DEFAULT 'MEDIUM',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_notification_settings_tenant_key ON MST_NotificationSettings (tenant_id, setting_key);
CREATE INDEX idx_notification_settings_type ON MST_NotificationSettings (notification_type);
CREATE INDEX idx_notification_settings_event ON MST_NotificationSettings (trigger_event);
CREATE INDEX idx_notification_settings_enabled ON MST_NotificationSettings (is_enabled);
CREATE INDEX idx_notification_settings_template ON MST_NotificationSettings (template_id);
