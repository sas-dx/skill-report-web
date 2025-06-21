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

-- 作成日: 2025-06-21 17:20:35
-- ============================================

DROP TABLE IF EXISTS MST_SystemConfig;

CREATE TABLE MST_SystemConfig (
    config_key VARCHAR,
    config_name VARCHAR,
    config_value TEXT,
    config_type ENUM,
    config_category ENUM,
    default_value TEXT,
    validation_rule TEXT,
    description TEXT,
    is_encrypted BOOLEAN DEFAULT False,
    is_system_only BOOLEAN DEFAULT False,
    is_user_configurable BOOLEAN DEFAULT True,
    requires_restart BOOLEAN DEFAULT False,
    environment ENUM DEFAULT 'ALL',
    tenant_specific BOOLEAN DEFAULT False,
    last_modified_by VARCHAR,
    last_modified_reason TEXT,
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT True,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_config_key ON MST_SystemConfig (config_key);
CREATE INDEX idx_config_category ON MST_SystemConfig (config_category);
CREATE INDEX idx_config_type ON MST_SystemConfig (config_type);
CREATE INDEX idx_user_configurable ON MST_SystemConfig (is_user_configurable, is_active);
CREATE INDEX idx_environment ON MST_SystemConfig (environment, is_active);
CREATE INDEX idx_tenant_specific ON MST_SystemConfig (tenant_specific, is_active);
CREATE INDEX idx_sort_order ON MST_SystemConfig (sort_order);
