-- ============================================
-- テーブル: MST_NotificationTemplate
-- 論理名: 通知テンプレート
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_NotificationTemplate;

CREATE TABLE MST_NotificationTemplate (
    id VARCHAR(50) COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) COMMENT 'マルチテナント識別子',
    template_key VARCHAR(100) COMMENT 'テンプレートの識別キー（例：skill_update_email、goal_reminder_slack等）',
    template_name VARCHAR(200) COMMENT 'テンプレートの表示名',
    notification_type ENUM COMMENT '対応する通知の種類（EMAIL:メール、SLACK:Slack、TEAMS:Teams、WEBHOOK:Webhook）',
    language_code VARCHAR(10) DEFAULT 'ja' COMMENT 'テンプレートの言語（ja:日本語、en:英語等）',
    subject_template VARCHAR(500) COMMENT '通知の件名テンプレート（メール等で使用）',
    body_template TEXT COMMENT '通知の本文テンプレート（プレースホルダー含む）',
    format_type ENUM DEFAULT 'PLAIN' COMMENT 'テンプレートのフォーマット（PLAIN:プレーンテキスト、HTML:HTML、MARKDOWN:Markdown）',
    parameters TEXT COMMENT 'テンプレートで使用可能なパラメータの定義（JSON形式）',
    sample_data TEXT COMMENT 'テンプレート確認用のサンプルデータ（JSON形式）',
    is_default BOOLEAN DEFAULT False COMMENT '同一キー・タイプでのデフォルトテンプレートかどうか',
    is_active BOOLEAN DEFAULT True COMMENT 'テンプレートが有効かどうか',
    version VARCHAR(20) DEFAULT '1.0.0' COMMENT 'テンプレートのバージョン番号',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称',
    description TEXT COMMENT 'マスタ説明'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_notification_template_tenant_key_type ON MST_NotificationTemplate (tenant_id, template_key, notification_type, language_code);
CREATE INDEX idx_notification_template_type ON MST_NotificationTemplate (notification_type);
CREATE INDEX idx_notification_template_language ON MST_NotificationTemplate (language_code);
CREATE INDEX idx_notification_template_default ON MST_NotificationTemplate (is_default, is_active);
CREATE INDEX idx_notification_template_key ON MST_NotificationTemplate (template_key);

-- その他の制約
ALTER TABLE MST_NotificationTemplate ADD CONSTRAINT uk_notification_template_tenant_key_type_lang UNIQUE ();
ALTER TABLE MST_NotificationTemplate ADD CONSTRAINT chk_notification_template_type CHECK (notification_type IN ('EMAIL', 'SLACK', 'TEAMS', 'WEBHOOK'));
ALTER TABLE MST_NotificationTemplate ADD CONSTRAINT chk_notification_template_format CHECK (format_type IN ('PLAIN', 'HTML', 'MARKDOWN'));
ALTER TABLE MST_NotificationTemplate ADD CONSTRAINT chk_notification_template_language CHECK (language_code IN ('ja', 'en'));
