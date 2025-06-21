-- ============================================
-- テーブル: MST_NotificationTemplate
-- 論理名: 通知テンプレート
-- 説明: MST_NotificationTemplate（通知テンプレート）は、システムで使用する通知メッセージのテンプレートを管理するマスタテーブルです。

主な目的：
- 通知メッセージの定型文管理
- 多言語対応の通知テンプレート管理
- 通知チャネル別のテンプレート管理
- 動的パラメータを含むテンプレート管理
- テナント別カスタマイズ対応

このテーブルは、通知・連携管理機能において一貫性のあるメッセージ配信を実現する重要なマスタデータです。

-- 作成日: 2025-06-21 17:20:33
-- ============================================

DROP TABLE IF EXISTS MST_NotificationTemplate;

CREATE TABLE MST_NotificationTemplate (
    id VARCHAR,
    tenant_id VARCHAR,
    template_key VARCHAR,
    template_name VARCHAR,
    notification_type ENUM,
    language_code VARCHAR DEFAULT 'ja',
    subject_template VARCHAR,
    body_template TEXT,
    format_type ENUM DEFAULT 'PLAIN',
    parameters TEXT,
    sample_data TEXT,
    is_default BOOLEAN DEFAULT False,
    is_active BOOLEAN DEFAULT True,
    version VARCHAR DEFAULT '1.0.0',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_notification_template_tenant_key_type ON MST_NotificationTemplate (tenant_id, template_key, notification_type, language_code);
CREATE INDEX idx_notification_template_type ON MST_NotificationTemplate (notification_type);
CREATE INDEX idx_notification_template_language ON MST_NotificationTemplate (language_code);
CREATE INDEX idx_notification_template_default ON MST_NotificationTemplate (is_default, is_active);
CREATE INDEX idx_notification_template_key ON MST_NotificationTemplate (template_key);
