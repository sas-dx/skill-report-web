-- ============================================
-- テーブル: MST_TenantSettings
-- 論理名: テナント設定
-- 説明: MST_TenantSettings（テナント設定）は、マルチテナントシステムにおける各テナント固有の設定情報を管理するマスタテーブルです。

主な目的：
- テナント別システム設定の管理
- 機能有効/無効の制御設定
- UI・表示設定のカスタマイズ
- 業務ルール・制限値の設定
- 外部連携設定の管理

このテーブルは、マルチテナント管理機能において各テナントの個別要件に対応する重要なマスタデータです。

-- 作成日: 2025-06-21 17:20:34
-- ============================================

DROP TABLE IF EXISTS MST_TenantSettings;

CREATE TABLE MST_TenantSettings (
    id VARCHAR,
    tenant_id VARCHAR,
    setting_category ENUM,
    setting_key VARCHAR,
    setting_name VARCHAR,
    setting_description TEXT,
    data_type ENUM,
    setting_value TEXT,
    default_value TEXT,
    validation_rules TEXT,
    is_required BOOLEAN DEFAULT False,
    is_encrypted BOOLEAN DEFAULT False,
    is_system_managed BOOLEAN DEFAULT False,
    is_user_configurable BOOLEAN DEFAULT True,
    display_order INTEGER DEFAULT 0,
    effective_from TIMESTAMP,
    effective_until TIMESTAMP,
    last_modified_by VARCHAR,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_tenant_settings_tenant_key ON MST_TenantSettings (tenant_id, setting_key);
CREATE INDEX idx_tenant_settings_category ON MST_TenantSettings (setting_category);
CREATE INDEX idx_tenant_settings_configurable ON MST_TenantSettings (is_user_configurable);
CREATE INDEX idx_tenant_settings_system_managed ON MST_TenantSettings (is_system_managed);
CREATE INDEX idx_tenant_settings_display_order ON MST_TenantSettings (tenant_id, setting_category, display_order);
CREATE INDEX idx_tenant_settings_effective ON MST_TenantSettings (effective_from, effective_until);
