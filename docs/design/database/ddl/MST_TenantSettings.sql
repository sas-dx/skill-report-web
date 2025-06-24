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

-- 作成日: 2025-06-24 22:56:14
-- ============================================

DROP TABLE IF EXISTS MST_TenantSettings;

CREATE TABLE MST_TenantSettings (
    id VARCHAR(50) COMMENT 'ID',
    tenant_id VARCHAR(50) COMMENT 'テナントID',
    data_type ENUM('STRING', 'INTEGER', 'BOOLEAN', 'JSON', 'DECIMAL') COMMENT 'データ型',
    default_value TEXT COMMENT 'デフォルト値',
    display_order INTEGER DEFAULT 0 COMMENT '表示順序',
    effective_from TIMESTAMP COMMENT '有効開始日時',
    effective_until TIMESTAMP COMMENT '有効終了日時',
    is_encrypted BOOLEAN DEFAULT False COMMENT '暗号化フラグ',
    is_required BOOLEAN DEFAULT False COMMENT '必須フラグ',
    is_system_managed BOOLEAN DEFAULT False COMMENT 'システム管理フラグ',
    is_user_configurable BOOLEAN DEFAULT True COMMENT 'ユーザー設定可能フラグ',
    last_modified_by VARCHAR(50) COMMENT '最終更新者',
    setting_category ENUM('SYSTEM', 'UI', 'BUSINESS', 'SECURITY', 'INTEGRATION') COMMENT '設定カテゴリ',
    setting_description TEXT COMMENT '設定説明',
    setting_key VARCHAR(100) COMMENT '設定キー',
    setting_name VARCHAR(200) COMMENT '設定名',
    setting_value TEXT COMMENT '設定値',
    tenantsettings_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_TenantSettingsの主キー',
    validation_rules TEXT COMMENT 'バリデーションルール',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_tenant_settings_tenant_key ON MST_TenantSettings (tenant_id, setting_key);
CREATE INDEX idx_tenant_settings_category ON MST_TenantSettings (setting_category);
CREATE INDEX idx_tenant_settings_configurable ON MST_TenantSettings (is_user_configurable);
CREATE INDEX idx_tenant_settings_system_managed ON MST_TenantSettings (is_system_managed);
CREATE INDEX idx_tenant_settings_display_order ON MST_TenantSettings (tenant_id, setting_category, display_order);
CREATE INDEX idx_tenant_settings_effective ON MST_TenantSettings (effective_from, effective_until);
CREATE INDEX idx_mst_tenantsettings_tenant_id ON MST_TenantSettings (tenant_id);

-- 外部キー制約
ALTER TABLE MST_TenantSettings ADD CONSTRAINT fk_tenant_settings_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(id) ON UPDATE CASCADE ON DELETE CASCADE;

-- その他の制約
-- 制約DDL生成エラー: uk_tenant_settings_tenant_key
ALTER TABLE MST_TenantSettings ADD CONSTRAINT chk_tenant_settings_category CHECK (setting_category IN ('SYSTEM', 'UI', 'BUSINESS', 'SECURITY', 'INTEGRATION'));
ALTER TABLE MST_TenantSettings ADD CONSTRAINT chk_tenant_settings_data_type CHECK (data_type IN ('STRING', 'INTEGER', 'BOOLEAN', 'JSON', 'DECIMAL'));
ALTER TABLE MST_TenantSettings ADD CONSTRAINT chk_tenant_settings_effective_period CHECK (effective_until IS NULL OR effective_from IS NULL OR effective_until >= effective_from);
ALTER TABLE MST_TenantSettings ADD CONSTRAINT chk_tenant_settings_display_order_positive CHECK (display_order >= 0);
