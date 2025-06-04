-- ============================================
-- テーブル: MST_TenantSettings
-- 論理名: テナント設定
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_TenantSettings;

CREATE TABLE MST_TenantSettings (
    id VARCHAR(50) COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) COMMENT '設定対象のテナントID（MST_Tenantへの参照）',
    setting_category ENUM COMMENT '設定の分類（SYSTEM:システム、UI:ユーザーインターフェース、BUSINESS:業務、SECURITY:セキュリティ、INTEGRATION:連携）',
    setting_key VARCHAR(100) COMMENT '設定項目の識別キー（例：max_users、theme_color、skill_approval_required等）',
    setting_name VARCHAR(200) COMMENT '設定項目の表示名',
    setting_description TEXT COMMENT '設定項目の詳細説明',
    data_type ENUM COMMENT '設定値のデータ型（STRING:文字列、INTEGER:整数、BOOLEAN:真偽値、JSON:JSON、DECIMAL:小数）',
    setting_value TEXT COMMENT '実際の設定値（文字列として格納、data_typeに応じて解釈）',
    default_value TEXT COMMENT '設定のデフォルト値',
    validation_rules TEXT COMMENT '設定値のバリデーションルール（JSON形式）',
    is_required BOOLEAN DEFAULT False COMMENT '設定が必須かどうか',
    is_encrypted BOOLEAN DEFAULT False COMMENT '設定値を暗号化するかどうか',
    is_system_managed BOOLEAN DEFAULT False COMMENT 'システムが自動管理する設定かどうか',
    is_user_configurable BOOLEAN DEFAULT True COMMENT 'テナント管理者が変更可能かどうか',
    display_order INTEGER DEFAULT 0 COMMENT '管理画面での表示順序',
    effective_from TIMESTAMP COMMENT '設定が有効になる日時',
    effective_until TIMESTAMP COMMENT '設定が無効になる日時',
    last_modified_by VARCHAR(50) COMMENT '設定を最後に更新したユーザーID',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称',
    description TEXT COMMENT 'マスタ説明'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_tenant_settings_tenant_key ON MST_TenantSettings (tenant_id, setting_key);
CREATE INDEX idx_tenant_settings_category ON MST_TenantSettings (setting_category);
CREATE INDEX idx_tenant_settings_configurable ON MST_TenantSettings (is_user_configurable);
CREATE INDEX idx_tenant_settings_system_managed ON MST_TenantSettings (is_system_managed);
CREATE INDEX idx_tenant_settings_display_order ON MST_TenantSettings (tenant_id, setting_category, display_order);
CREATE INDEX idx_tenant_settings_effective ON MST_TenantSettings (effective_from, effective_until);

-- 外部キー制約
ALTER TABLE MST_TenantSettings ADD CONSTRAINT fk_tenant_settings_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(id) ON UPDATE CASCADE ON DELETE CASCADE;

-- その他の制約
ALTER TABLE MST_TenantSettings ADD CONSTRAINT uk_tenant_settings_tenant_key UNIQUE ();
ALTER TABLE MST_TenantSettings ADD CONSTRAINT chk_tenant_settings_category CHECK (setting_category IN ('SYSTEM', 'UI', 'BUSINESS', 'SECURITY', 'INTEGRATION'));
ALTER TABLE MST_TenantSettings ADD CONSTRAINT chk_tenant_settings_data_type CHECK (data_type IN ('STRING', 'INTEGER', 'BOOLEAN', 'JSON', 'DECIMAL'));
ALTER TABLE MST_TenantSettings ADD CONSTRAINT chk_tenant_settings_effective_period CHECK (effective_until IS NULL OR effective_from IS NULL OR effective_until >= effective_from);
ALTER TABLE MST_TenantSettings ADD CONSTRAINT chk_tenant_settings_display_order_positive CHECK (display_order >= 0);
