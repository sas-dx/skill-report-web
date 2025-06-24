-- ============================================
-- テーブル: MST_Tenant
-- 論理名: テナント（組織）
-- 説明: マルチテナント対応システムにおける組織・会社情報を管理するマスタテーブル。

主な目的：
- 複数の組織・会社（テナント）の基本情報管理
- テナント別のシステム設定・カスタマイズ情報の管理
- 階層構造による組織関係の表現（親子関係）
- テナント別のブランディング設定（ロゴ、カラー）
- 契約・課金情報の管理（プラン、ユーザー数制限）
- マルチテナント認証・認可の基盤データ提供

このテーブルはマルチテナントシステムの中核となるマスタデータであり、
全ての業務データがテナント単位で分離される基盤を提供する。
現在はシングルテナント実装だが、将来のマルチテナント化に備えた設計。

-- 作成日: 2025-06-24 22:56:15
-- ============================================

DROP TABLE IF EXISTS MST_Tenant;

CREATE TABLE MST_Tenant (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントを一意に識別するID',
    address TEXT COMMENT 'テナントの住所',
    admin_email VARCHAR(255) NOT NULL COMMENT 'テナント管理者のメールアドレス',
    contact_email VARCHAR(255) COMMENT 'テナントの一般連絡先メールアドレス',
    contract_end_date DATE COMMENT 'テナント契約の終了日',
    contract_start_date DATE NOT NULL COMMENT 'テナント契約の開始日',
    country_code VARCHAR(2) NOT NULL DEFAULT 'JP' COMMENT '国コード（ISO 3166-1 alpha-2）',
    currency_code VARCHAR(3) NOT NULL DEFAULT 'JPY' COMMENT 'テナントで使用する通貨コード（ISO 4217）',
    domain_name VARCHAR(100) COMMENT 'テナント専用ドメイン名',
    locale VARCHAR(10) NOT NULL DEFAULT 'ja_JP' COMMENT 'テナントのデフォルトロケール',
    logo_url VARCHAR(500) COMMENT 'テナントロゴ画像のURL',
    max_storage_gb INTEGER NOT NULL DEFAULT 10 COMMENT '契約上の最大ストレージ容量（GB）',
    max_users INTEGER NOT NULL DEFAULT 100 COMMENT '契約上の最大ユーザー数',
    parent_tenant_id VARCHAR(50) COMMENT '親テナントのID（階層構造の場合）',
    phone_number VARCHAR(20) COMMENT 'テナントの電話番号',
    postal_code VARCHAR(10) COMMENT '郵便番号',
    primary_color VARCHAR(7) COMMENT 'テナントのプライマリカラー（#RRGGBB）',
    secondary_color VARCHAR(7) COMMENT 'テナントのセカンダリカラー（#RRGGBB）',
    status VARCHAR(20) NOT NULL DEFAULT 'TRIAL' COMMENT 'テナントの状態（ACTIVE:有効、INACTIVE:無効、SUSPENDED:停止、TRIAL:試用中、EXPIRED:期限切れ）',
    subdomain VARCHAR(50) COMMENT 'サブドメイン名（xxx.system.com）',
    subscription_plan VARCHAR(20) NOT NULL DEFAULT 'BASIC' COMMENT '契約プラン（FREE:無料、BASIC:基本、STANDARD:標準、PREMIUM:プレミアム、ENTERPRISE:エンタープライズ）',
    tenant_code VARCHAR(20) NOT NULL COMMENT 'テナントの識別コード（URL等で使用）',
    tenant_level INTEGER NOT NULL DEFAULT 1 COMMENT 'テナント階層のレベル（1が最上位）',
    tenant_name VARCHAR(200) NOT NULL COMMENT 'テナント（組織・会社）の正式名称',
    tenant_name_en VARCHAR(200) COMMENT 'テナントの英語名称',
    tenant_short_name VARCHAR(50) COMMENT 'テナントの略称・短縮名',
    tenant_type VARCHAR(20) NOT NULL DEFAULT 'ENTERPRISE' COMMENT 'テナントの種別（ENTERPRISE:企業、DEPARTMENT:部門、SUBSIDIARY:子会社、PARTNER:パートナー、TRIAL:試用）',
    timezone VARCHAR(50) NOT NULL DEFAULT 'Asia/Tokyo' COMMENT 'テナントのデフォルトタイムゾーン',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
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
CREATE INDEX idx_admin_email ON MST_Tenant (admin_email);

-- 外部キー制約
ALTER TABLE MST_Tenant ADD CONSTRAINT fk_tenant_parent FOREIGN KEY (parent_tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE SET NULL;
