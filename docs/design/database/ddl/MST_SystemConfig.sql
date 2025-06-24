-- ============================================
-- テーブル: MST_SystemConfig
-- 論理名: システム設定
-- 説明: MST_SystemConfig（システム設定）は、システム全体の設定値・パラメータを管理するマスタテーブルです。

主な目的：
- システム運用パラメータの一元管理
- 機能ON/OFF設定の管理
- 業務ルール・閾値の設定管理
- 外部連携設定の管理
- セキュリティ設定の管理

このテーブルにより、システムの動作を柔軟に制御し、
運用環境に応じた設定変更を効率的に行うことができます。

-- 作成日: 2025-06-24 23:05:57
-- ============================================

DROP TABLE IF EXISTS MST_SystemConfig;

CREATE TABLE MST_SystemConfig (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    config_key VARCHAR(100) COMMENT '設定キー',
    config_category ENUM('SECURITY', 'SYSTEM', 'BUSINESS', 'UI', 'INTEGRATION') COMMENT '設定カテゴリ',
    config_name VARCHAR(200) COMMENT '設定名',
    config_type ENUM('STRING', 'INTEGER', 'DECIMAL', 'BOOLEAN', 'JSON', 'ENCRYPTED') COMMENT '設定タイプ',
    config_value TEXT COMMENT '設定値',
    default_value TEXT COMMENT 'デフォルト値',
    description TEXT COMMENT '説明',
    environment ENUM('DEV', 'TEST', 'PROD', 'ALL') DEFAULT 'ALL' COMMENT '環境',
    is_active BOOLEAN DEFAULT True COMMENT '有効フラグ',
    is_encrypted BOOLEAN DEFAULT False COMMENT '暗号化フラグ',
    is_system_only BOOLEAN DEFAULT False COMMENT 'システム専用フラグ',
    is_user_configurable BOOLEAN DEFAULT True COMMENT 'ユーザー設定可能フラグ',
    last_modified_by VARCHAR(50) COMMENT '最終更新者',
    last_modified_reason TEXT COMMENT '更新理由',
    requires_restart BOOLEAN DEFAULT False COMMENT '再起動要否',
    sort_order INTEGER DEFAULT 0 COMMENT '表示順序',
    systemconfig_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_SystemConfigの主キー',
    tenant_specific BOOLEAN DEFAULT False COMMENT 'テナント固有フラグ',
    validation_rule TEXT COMMENT '検証ルール',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_config_key ON MST_SystemConfig (config_key);
CREATE INDEX idx_config_category ON MST_SystemConfig (config_category);
CREATE INDEX idx_config_type ON MST_SystemConfig (config_type);
CREATE INDEX idx_user_configurable ON MST_SystemConfig (is_user_configurable, is_active);
CREATE INDEX idx_environment ON MST_SystemConfig (environment, is_active);
CREATE INDEX idx_tenant_specific ON MST_SystemConfig (tenant_specific, is_active);
CREATE INDEX idx_sort_order ON MST_SystemConfig (sort_order);
CREATE INDEX idx_mst_systemconfig_tenant_id ON MST_SystemConfig (tenant_id);

-- その他の制約
-- 制約DDL生成エラー: uk_config_key
ALTER TABLE MST_SystemConfig ADD CONSTRAINT chk_config_type CHECK (config_type IN ('STRING', 'INTEGER', 'DECIMAL', 'BOOLEAN', 'JSON', 'ENCRYPTED'));
ALTER TABLE MST_SystemConfig ADD CONSTRAINT chk_config_category CHECK (config_category IN ('SECURITY', 'SYSTEM', 'BUSINESS', 'UI', 'INTEGRATION'));
ALTER TABLE MST_SystemConfig ADD CONSTRAINT chk_environment CHECK (environment IN ('DEV', 'TEST', 'PROD', 'ALL'));
