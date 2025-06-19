-- MST_Tenant (テナント（組織）)
-- 生成日時: 2025-06-11 01:52:36
-- カテゴリ: マスタ系
-- 要求仕様ID: TNT.1-MGMT.1

CREATE TABLE MST_Tenant (
    tenant_id VARCHAR(50) NOT NULL,
    tenant_code VARCHAR(20) NOT NULL,
    tenant_name VARCHAR(200) NOT NULL,
    tenant_name_en VARCHAR(200),
    tenant_short_name VARCHAR(50),
    tenant_type VARCHAR(20) NOT NULL DEFAULT 'ENTERPRISE',
    parent_tenant_id VARCHAR(50),
    tenant_level INTEGER NOT NULL DEFAULT 1,
    domain_name VARCHAR(100),
    subdomain VARCHAR(50),
    logo_url VARCHAR(500),
    primary_color VARCHAR(7),
    secondary_color VARCHAR(7),
    timezone VARCHAR(50) NOT NULL DEFAULT 'Asia/Tokyo',
    locale VARCHAR(10) NOT NULL DEFAULT 'ja_JP',
    currency_code VARCHAR(3) NOT NULL DEFAULT 'JPY',
    admin_email VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255),
    phone_number VARCHAR(20),
    address TEXT,
    postal_code VARCHAR(10),
    country_code VARCHAR(2) NOT NULL DEFAULT 'JP',
    subscription_plan VARCHAR(20) NOT NULL DEFAULT 'BASIC',
    max_users INTEGER NOT NULL DEFAULT 100,
    max_storage_gb INTEGER NOT NULL DEFAULT 10,
    status VARCHAR(20) NOT NULL DEFAULT 'TRIAL',
    contract_start_date DATE NOT NULL,
    contract_end_date DATE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (tenant_id)
);

-- インデックス作成
CREATE UNIQUE INDEX idx_tenant_id ON MST_Tenant (tenant_id); -- テナントID検索用（一意）
CREATE UNIQUE INDEX idx_tenant_code ON MST_Tenant (tenant_code); -- テナントコード検索用（一意）
CREATE UNIQUE INDEX idx_domain_name ON MST_Tenant (domain_name); -- ドメイン名検索用（一意）
CREATE UNIQUE INDEX idx_subdomain ON MST_Tenant (subdomain); -- サブドメイン検索用（一意）
CREATE INDEX idx_tenant_type ON MST_Tenant (tenant_type); -- テナント種別検索用
CREATE INDEX idx_parent_tenant_id ON MST_Tenant (parent_tenant_id); -- 親テナント検索用
CREATE INDEX idx_subscription_plan ON MST_Tenant (subscription_plan); -- サブスクリプションプラン検索用
CREATE INDEX idx_status ON MST_Tenant (status); -- ステータス検索用
CREATE INDEX idx_admin_email ON MST_Tenant (admin_email); -- 管理者メール検索用

-- 外部キー制約
ALTER TABLE MST_Tenant ADD CONSTRAINT fk_tenant_parent FOREIGN KEY (parent_tenant_id) REFERENCES MST_Tenant (tenant_id) ON UPDATE CASCADE ON DELETE SET NULL;

COMMENT ON TABLE MST_Tenant IS 'テナント（組織）';

COMMENT ON COLUMN MST_Tenant.tenant_id IS 'テナントを一意に識別するID';
COMMENT ON COLUMN MST_Tenant.tenant_code IS 'テナントの識別コード（URL等で使用）';
COMMENT ON COLUMN MST_Tenant.tenant_name IS 'テナント（組織・会社）の正式名称';
COMMENT ON COLUMN MST_Tenant.tenant_name_en IS 'テナントの英語名称';
COMMENT ON COLUMN MST_Tenant.tenant_short_name IS 'テナントの略称・短縮名';
COMMENT ON COLUMN MST_Tenant.tenant_type IS 'テナントの種別（ENTERPRISE:企業、DEPARTMENT:部門、SUBSIDIARY:子会社、PARTNER:パートナー、TRIAL:試用）';
COMMENT ON COLUMN MST_Tenant.parent_tenant_id IS '親テナントのID（階層構造の場合）';
COMMENT ON COLUMN MST_Tenant.tenant_level IS 'テナント階層のレベル（1が最上位）';
COMMENT ON COLUMN MST_Tenant.domain_name IS 'テナント専用ドメイン名';
COMMENT ON COLUMN MST_Tenant.subdomain IS 'サブドメイン名（xxx.system.com）';
COMMENT ON COLUMN MST_Tenant.logo_url IS 'テナントロゴ画像のURL';
COMMENT ON COLUMN MST_Tenant.primary_color IS 'テナントのプライマリカラー（#RRGGBB）';
COMMENT ON COLUMN MST_Tenant.secondary_color IS 'テナントのセカンダリカラー（#RRGGBB）';
COMMENT ON COLUMN MST_Tenant.timezone IS 'テナントのデフォルトタイムゾーン';
COMMENT ON COLUMN MST_Tenant.locale IS 'テナントのデフォルトロケール';
COMMENT ON COLUMN MST_Tenant.currency_code IS 'テナントで使用する通貨コード（ISO 4217）';
COMMENT ON COLUMN MST_Tenant.admin_email IS 'テナント管理者のメールアドレス';
COMMENT ON COLUMN MST_Tenant.contact_email IS 'テナントの一般連絡先メールアドレス';
COMMENT ON COLUMN MST_Tenant.phone_number IS 'テナントの電話番号';
COMMENT ON COLUMN MST_Tenant.address IS 'テナントの住所';
COMMENT ON COLUMN MST_Tenant.postal_code IS '郵便番号';
COMMENT ON COLUMN MST_Tenant.country_code IS '国コード（ISO 3166-1 alpha-2）';
COMMENT ON COLUMN MST_Tenant.subscription_plan IS '契約プラン（FREE:無料、BASIC:基本、STANDARD:標準、PREMIUM:プレミアム、ENTERPRISE:エンタープライズ）';
COMMENT ON COLUMN MST_Tenant.max_users IS '契約上の最大ユーザー数';
COMMENT ON COLUMN MST_Tenant.max_storage_gb IS '契約上の最大ストレージ容量（GB）';
COMMENT ON COLUMN MST_Tenant.status IS 'テナントの状態（ACTIVE:有効、INACTIVE:無効、SUSPENDED:停止、TRIAL:試用中、EXPIRED:期限切れ）';
COMMENT ON COLUMN MST_Tenant.contract_start_date IS 'テナント契約の開始日';
COMMENT ON COLUMN MST_Tenant.contract_end_date IS 'テナント契約の終了日';
COMMENT ON COLUMN MST_Tenant.created_at IS '作成日時';
COMMENT ON COLUMN MST_Tenant.updated_at IS '更新日時';
COMMENT ON COLUMN MST_Tenant.is_deleted IS '論理削除フラグ';
