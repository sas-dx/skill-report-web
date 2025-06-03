-- ============================================
-- テーブル: MST_SystemConfig
-- 論理名: システム設定
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_SystemConfig;

CREATE TABLE MST_SystemConfig (
    config_key VARCHAR(100) COMMENT '設定項目を一意に識別するキー（例：MAX_LOGIN_ATTEMPTS、SESSION_TIMEOUT）',
    config_name VARCHAR(200) COMMENT '設定項目の表示名・説明',
    config_value TEXT COMMENT '設定の値（文字列、数値、JSON等）',
    config_type ENUM COMMENT '設定値のデータタイプ（STRING:文字列、INTEGER:整数、DECIMAL:小数、BOOLEAN:真偽値、JSON:JSON、ENCRYPTED:暗号化）',
    config_category ENUM COMMENT '設定の分類（SECURITY:セキュリティ、SYSTEM:システム、BUSINESS:業務、UI:ユーザーインターフェース、INTEGRATION:連携）',
    default_value TEXT COMMENT '設定のデフォルト値',
    validation_rule TEXT COMMENT '設定値の検証ルール（正規表現、範囲等）',
    description TEXT COMMENT '設定項目の詳細説明・用途',
    is_encrypted BOOLEAN DEFAULT False COMMENT '設定値が暗号化されているかどうか',
    is_system_only BOOLEAN DEFAULT False COMMENT 'システム内部でのみ使用される設定かどうか',
    is_user_configurable BOOLEAN DEFAULT True COMMENT '管理者がUI経由で変更可能かどうか',
    requires_restart BOOLEAN DEFAULT False COMMENT '設定変更時にシステム再起動が必要かどうか',
    environment ENUM DEFAULT 'ALL' COMMENT '設定が適用される環境（DEV:開発、TEST:テスト、PROD:本番、ALL:全環境）',
    tenant_specific BOOLEAN DEFAULT False COMMENT 'テナントごとに異なる値を持つ設定かどうか',
    last_modified_by VARCHAR(50) COMMENT '設定を最後に更新したユーザーID',
    last_modified_reason TEXT COMMENT '設定変更の理由・目的',
    sort_order INTEGER DEFAULT 0 COMMENT '設定一覧での表示順序',
    is_active BOOLEAN DEFAULT True COMMENT '設定が有効かどうか',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_config_key ON MST_SystemConfig (config_key);
CREATE INDEX idx_config_category ON MST_SystemConfig (config_category);
CREATE INDEX idx_config_type ON MST_SystemConfig (config_type);
CREATE INDEX idx_user_configurable ON MST_SystemConfig (is_user_configurable, is_active);
CREATE INDEX idx_environment ON MST_SystemConfig (environment, is_active);
CREATE INDEX idx_tenant_specific ON MST_SystemConfig (tenant_specific, is_active);
CREATE INDEX idx_sort_order ON MST_SystemConfig (sort_order);

-- その他の制約
ALTER TABLE MST_SystemConfig ADD CONSTRAINT uk_config_key UNIQUE ();
ALTER TABLE MST_SystemConfig ADD CONSTRAINT chk_config_type CHECK (config_type IN ('STRING', 'INTEGER', 'DECIMAL', 'BOOLEAN', 'JSON', 'ENCRYPTED'));
ALTER TABLE MST_SystemConfig ADD CONSTRAINT chk_config_category CHECK (config_category IN ('SECURITY', 'SYSTEM', 'BUSINESS', 'UI', 'INTEGRATION'));
ALTER TABLE MST_SystemConfig ADD CONSTRAINT chk_environment CHECK (environment IN ('DEV', 'TEST', 'PROD', 'ALL'));
