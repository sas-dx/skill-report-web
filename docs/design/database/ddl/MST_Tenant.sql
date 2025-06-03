-- ============================================
-- テーブル: MST_Tenant
-- 論理名: テナント（組織）
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_Tenant;

CREATE TABLE MST_Tenant (
    tenant_id VARCHAR(50) COMMENT 'テナントを一意に識別するID',
    tenant_code VARCHAR(20) COMMENT 'テナントの識別コード（URL等で使用）',
    tenant_name VARCHAR(200) COMMENT 'テナント（組織・会社）の正式名称',
    tenant_name_en VARCHAR(200) COMMENT 'テナントの英語名称',
    tenant_short_name VARCHAR(50) COMMENT 'テナントの略称・短縮名',
    tenant_type ENUM COMMENT 'テナントの種別（ENTERPRISE:企業、DEPARTMENT:部門、SUBSIDIARY:子会社、PARTNER:パートナー、TRIAL:試用）',
    parent_tenant_id VARCHAR(50) COMMENT '親テナントのID（階層構造の場合）',
    tenant_level INTEGER DEFAULT 1 COMMENT 'テナント階層のレベル（1が最上位）',
    domain_name VARCHAR(100) COMMENT 'テナント専用ドメイン名',
    subdomain VARCHAR(50) COMMENT 'サブドメイン名（xxx.system.com）',
    logo_url VARCHAR(500) COMMENT 'テナントロゴ画像のURL',
    primary_color VARCHAR(7) COMMENT 'テナントのプライマリカラー（#RRGGBB）',
    secondary_color VARCHAR(7) COMMENT 'テナントのセカンダリカラー（#RRGGBB）',
    timezone VARCHAR(50) DEFAULT 'Asia/Tokyo' COMMENT 'テナントのデフォルトタイムゾーン',
    locale VARCHAR(10) DEFAULT 'ja_JP' COMMENT 'テナントのデフォルトロケール',
    currency_code VARCHAR(3) DEFAULT 'JPY' COMMENT 'テナントで使用する通貨コード（ISO 4217）',
    date_format VARCHAR(20) DEFAULT 'YYYY-MM-DD' COMMENT 'テナントで使用する日付フォーマット',
    time_format VARCHAR(20) DEFAULT 'HH:mm:ss' COMMENT 'テナントで使用する時刻フォーマット',
    admin_email VARCHAR(255) COMMENT 'テナント管理者のメールアドレス',
    contact_email VARCHAR(255) COMMENT 'テナントの一般連絡先メールアドレス',
    phone_number VARCHAR(20) COMMENT 'テナントの電話番号',
    address TEXT COMMENT 'テナントの住所',
    postal_code VARCHAR(10) COMMENT '郵便番号',
    country_code VARCHAR(2) DEFAULT 'JP' COMMENT '国コード（ISO 3166-1 alpha-2）',
    subscription_plan ENUM DEFAULT 'BASIC' COMMENT '契約プラン（FREE:無料、BASIC:基本、STANDARD:標準、PREMIUM:プレミアム、ENTERPRISE:エンタープライズ）',
    max_users INTEGER DEFAULT 100 COMMENT '契約上の最大ユーザー数',
    max_storage_gb INTEGER DEFAULT 10 COMMENT '契約上の最大ストレージ容量（GB）',
    features_enabled TEXT COMMENT '有効化されている機能一覧（JSON形式）',
    custom_settings TEXT COMMENT 'テナント固有のカスタム設定（JSON形式）',
    security_policy TEXT COMMENT 'テナントのセキュリティポリシー設定（JSON形式）',
    data_retention_days INTEGER DEFAULT 2555 COMMENT 'データの保持期間（日数）',
    backup_enabled BOOLEAN DEFAULT True COMMENT '自動バックアップが有効かどうか',
    backup_frequency ENUM DEFAULT 'DAILY' COMMENT 'バックアップの実行頻度（DAILY:日次、WEEKLY:週次、MONTHLY:月次）',
    contract_start_date DATE COMMENT 'テナント契約の開始日',
    contract_end_date DATE COMMENT 'テナント契約の終了日',
    trial_end_date DATE COMMENT '試用期間の終了日',
    billing_cycle ENUM DEFAULT 'MONTHLY' COMMENT '請求の周期（MONTHLY:月次、QUARTERLY:四半期、ANNUAL:年次）',
    monthly_fee DECIMAL(10,2) COMMENT '月額利用料金',
    setup_fee DECIMAL(10,2) COMMENT '初期セットアップ費用',
    status ENUM DEFAULT 'TRIAL' COMMENT 'テナントの状態（ACTIVE:有効、INACTIVE:無効、SUSPENDED:停止、TRIAL:試用中、EXPIRED:期限切れ）',
    activation_date DATE COMMENT 'テナントが有効化された日',
    suspension_date DATE COMMENT 'テナントが停止された日',
    suspension_reason TEXT COMMENT 'テナント停止の理由',
    last_login_date DATE COMMENT 'テナント内での最終ログイン日',
    current_users_count INTEGER DEFAULT 0 COMMENT '現在のアクティブユーザー数',
    storage_used_gb DECIMAL(10,3) DEFAULT 0.0 COMMENT '現在使用中のストレージ容量（GB）',
    api_rate_limit INTEGER DEFAULT 1000 COMMENT '1時間あたりのAPI呼び出し制限数',
    sso_enabled BOOLEAN DEFAULT False COMMENT 'シングルサインオンが有効かどうか',
    sso_provider VARCHAR(50) COMMENT 'SSOプロバイダー名（SAML、OAuth等）',
    sso_config TEXT COMMENT 'SSO設定情報（JSON形式）',
    webhook_url VARCHAR(500) COMMENT 'イベント通知用のWebhook URL',
    webhook_secret VARCHAR(100) COMMENT 'Webhook認証用の秘密鍵',
    created_by VARCHAR(50) COMMENT 'テナントを作成したユーザーID',
    notes TEXT COMMENT 'テナントに関する備考・メモ',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称',
    description TEXT COMMENT 'マスタ説明'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_tenant_id ON MST_Tenant (tenant_id);
CREATE UNIQUE INDEX idx_tenant_code ON MST_Tenant (tenant_code);
CREATE UNIQUE INDEX idx_domain_name ON MST_Tenant (domain_name);
CREATE UNIQUE INDEX idx_subdomain ON MST_Tenant (subdomain);
CREATE INDEX idx_tenant_type ON MST_Tenant (tenant_type);
CREATE INDEX idx_parent_tenant_id ON MST_Tenant (parent_tenant_id);
CREATE INDEX idx_subscription_plan ON MST_Tenant (subscription_plan);
CREATE INDEX idx_status ON MST_Tenant (status);
CREATE INDEX idx_contract_period ON MST_Tenant (contract_start_date, contract_end_date);
CREATE INDEX idx_admin_email ON MST_Tenant (admin_email);

-- 外部キー制約
ALTER TABLE MST_Tenant ADD CONSTRAINT fk_tenant_parent FOREIGN KEY (parent_tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
ALTER TABLE MST_Tenant ADD CONSTRAINT uk_tenant_id UNIQUE ();
ALTER TABLE MST_Tenant ADD CONSTRAINT uk_tenant_code UNIQUE ();
ALTER TABLE MST_Tenant ADD CONSTRAINT uk_domain_name UNIQUE ();
ALTER TABLE MST_Tenant ADD CONSTRAINT uk_subdomain UNIQUE ();
ALTER TABLE MST_Tenant ADD CONSTRAINT chk_tenant_type CHECK (tenant_type IN ('ENTERPRISE', 'DEPARTMENT', 'SUBSIDIARY', 'PARTNER', 'TRIAL'));
ALTER TABLE MST_Tenant ADD CONSTRAINT chk_subscription_plan CHECK (subscription_plan IN ('FREE', 'BASIC', 'STANDARD', 'PREMIUM', 'ENTERPRISE'));
ALTER TABLE MST_Tenant ADD CONSTRAINT chk_backup_frequency CHECK (backup_frequency IN ('DAILY', 'WEEKLY', 'MONTHLY'));
ALTER TABLE MST_Tenant ADD CONSTRAINT chk_billing_cycle CHECK (billing_cycle IN ('MONTHLY', 'QUARTERLY', 'ANNUAL'));
ALTER TABLE MST_Tenant ADD CONSTRAINT chk_status CHECK (status IN ('ACTIVE', 'INACTIVE', 'SUSPENDED', 'TRIAL', 'EXPIRED'));
ALTER TABLE MST_Tenant ADD CONSTRAINT chk_tenant_level_positive CHECK (tenant_level > 0);
ALTER TABLE MST_Tenant ADD CONSTRAINT chk_max_users_positive CHECK (max_users > 0);
ALTER TABLE MST_Tenant ADD CONSTRAINT chk_max_storage_positive CHECK (max_storage_gb > 0);
ALTER TABLE MST_Tenant ADD CONSTRAINT chk_data_retention_positive CHECK (data_retention_days > 0);
ALTER TABLE MST_Tenant ADD CONSTRAINT chk_contract_period CHECK (contract_end_date IS NULL OR contract_start_date <= contract_end_date);
ALTER TABLE MST_Tenant ADD CONSTRAINT chk_current_users_range CHECK (current_users_count >= 0 AND current_users_count <= max_users);
ALTER TABLE MST_Tenant ADD CONSTRAINT chk_storage_used_positive CHECK (storage_used_gb >= 0);
ALTER TABLE MST_Tenant ADD CONSTRAINT chk_api_rate_limit_positive CHECK (api_rate_limit > 0);
