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

-- 作成日: 2025-06-24 23:02:18
-- ============================================

DROP TABLE IF EXISTS MST_NotificationTemplate;

CREATE TABLE MST_NotificationTemplate (
    id VARCHAR(50) COMMENT 'ID',
    tenant_id VARCHAR(50) COMMENT 'テナントID',
    body_template TEXT COMMENT '本文テンプレート',
    format_type ENUM('PLAIN', 'HTML', 'MARKDOWN') DEFAULT 'PLAIN' COMMENT 'フォーマットタイプ',
    is_active BOOLEAN DEFAULT True COMMENT '有効フラグ',
    is_default BOOLEAN DEFAULT False COMMENT 'デフォルトフラグ',
    language_code VARCHAR(10) DEFAULT 'ja' COMMENT '言語コード',
    notification_type ENUM('EMAIL', 'SLACK', 'TEAMS', 'WEBHOOK') COMMENT '通知タイプ',
    notificationtemplate_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_NotificationTemplateの主キー',
    parameters TEXT COMMENT 'パラメータ定義',
    sample_data TEXT COMMENT 'サンプルデータ',
    subject_template VARCHAR(500) COMMENT '件名テンプレート',
    template_key VARCHAR(100) COMMENT 'テンプレートキー',
    template_name VARCHAR(200) COMMENT 'テンプレート名',
    version VARCHAR(20) DEFAULT '1.0.0' COMMENT 'バージョン',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_notification_template_tenant_key_type ON MST_NotificationTemplate (tenant_id, template_key, notification_type, language_code);
CREATE INDEX idx_notification_template_type ON MST_NotificationTemplate (notification_type);
CREATE INDEX idx_notification_template_language ON MST_NotificationTemplate (language_code);
CREATE INDEX idx_notification_template_default ON MST_NotificationTemplate (is_default, is_active);
CREATE INDEX idx_notification_template_key ON MST_NotificationTemplate (template_key);
CREATE INDEX idx_mst_notificationtemplate_tenant_id ON MST_NotificationTemplate (tenant_id);

-- その他の制約
-- 制約DDL生成エラー: uk_notification_template_tenant_key_type_lang
ALTER TABLE MST_NotificationTemplate ADD CONSTRAINT chk_notification_template_type CHECK (notification_type IN ('EMAIL', 'SLACK', 'TEAMS', 'WEBHOOK'));
ALTER TABLE MST_NotificationTemplate ADD CONSTRAINT chk_notification_template_format CHECK (format_type IN ('PLAIN', 'HTML', 'MARKDOWN'));
ALTER TABLE MST_NotificationTemplate ADD CONSTRAINT chk_notification_template_language CHECK (language_code IN ('ja', 'en'));
