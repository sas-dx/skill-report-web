# テーブル定義書_MST_Tenant_テナント（組織）

## テーブル情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_Tenant |
| 論理名 | テナント（組織） |
| カテゴリ | マスタ系 |
| 優先度 | 最高 |
| 要求仕様ID | TNT.1-MGMT.1 |

## カラム定義

| カラム名 | データ型 | NULL許可 | 主キー | デフォルト値 | 説明 | 要求仕様ID |
|----------|----------|----------|--------|--------------|------|-------------|
| tenant_id | VARCHAR(50) | NO | YES | - | テナントを一意に識別するID | TNT.1-MGMT.1 |
| tenant_code | VARCHAR(20) | NO | NO | - | テナントの識別コード（URL等で使用） | TNT.1-MGMT.1 |
| tenant_name | VARCHAR(200) | NO | NO | - | テナント（組織・会社）の正式名称 | TNT.1-MGMT.1 |
| tenant_name_en | VARCHAR(200) | YES | NO | - | テナントの英語名称 | TNT.1-MGMT.1 |
| tenant_short_name | VARCHAR(50) | YES | NO | - | テナントの略称・短縮名 | TNT.1-MGMT.1 |
| tenant_type | VARCHAR(20) | NO | NO | ENTERPRISE | テナントの種別（ENTERPRISE:企業、DEPARTMENT:部門、SUBSIDIARY:子会社、PARTNER:パートナー、TRIAL:試用） | TNT.1-MGMT.1 |
| parent_tenant_id | VARCHAR(50) | YES | NO | - | 親テナントのID（階層構造の場合） | TNT.1-MGMT.1 |
| tenant_level | INTEGER | NO | NO | 1 | テナント階層のレベル（1が最上位） | TNT.1-MGMT.1 |
| domain_name | VARCHAR(100) | YES | NO | - | テナント専用ドメイン名 | TNT.1-MGMT.1 |
| subdomain | VARCHAR(50) | YES | NO | - | サブドメイン名（xxx.system.com） | TNT.1-MGMT.1 |
| logo_url | VARCHAR(500) | YES | NO | - | テナントロゴ画像のURL | TNT.1-MGMT.1 |
| primary_color | VARCHAR(7) | YES | NO | - | テナントのプライマリカラー（#RRGGBB） | TNT.1-MGMT.1 |
| secondary_color | VARCHAR(7) | YES | NO | - | テナントのセカンダリカラー（#RRGGBB） | TNT.1-MGMT.1 |
| timezone | VARCHAR(50) | NO | NO | Asia/Tokyo | テナントのデフォルトタイムゾーン | TNT.1-MGMT.1 |
| locale | VARCHAR(10) | NO | NO | ja_JP | テナントのデフォルトロケール | TNT.1-MGMT.1 |
| currency_code | VARCHAR(3) | NO | NO | JPY | テナントで使用する通貨コード（ISO 4217） | TNT.1-MGMT.1 |
| admin_email | VARCHAR(255) | NO | NO | - | テナント管理者のメールアドレス | TNT.1-MGMT.1 |
| contact_email | VARCHAR(255) | YES | NO | - | テナントの一般連絡先メールアドレス | TNT.1-MGMT.1 |
| phone_number | VARCHAR(20) | YES | NO | - | テナントの電話番号 | TNT.1-MGMT.1 |
| address | TEXT | YES | NO | - | テナントの住所 | TNT.1-MGMT.1 |
| postal_code | VARCHAR(10) | YES | NO | - | 郵便番号 | TNT.1-MGMT.1 |
| country_code | VARCHAR(2) | NO | NO | JP | 国コード（ISO 3166-1 alpha-2） | TNT.1-MGMT.1 |
| subscription_plan | VARCHAR(20) | NO | NO | BASIC | 契約プラン（FREE:無料、BASIC:基本、STANDARD:標準、PREMIUM:プレミアム、ENTERPRISE:エンタープライズ） | TNT.1-MGMT.1 |
| max_users | INTEGER | NO | NO | 100 | 契約上の最大ユーザー数 | TNT.1-MGMT.1 |
| max_storage_gb | INTEGER | NO | NO | 10 | 契約上の最大ストレージ容量（GB） | TNT.1-MGMT.1 |
| status | VARCHAR(20) | NO | NO | TRIAL | テナントの状態（ACTIVE:有効、INACTIVE:無効、SUSPENDED:停止、TRIAL:試用中、EXPIRED:期限切れ） | TNT.1-MGMT.1 |
| contract_start_date | DATE | NO | NO | - | テナント契約の開始日 | TNT.1-MGMT.1 |
| contract_end_date | DATE | YES | NO | - | テナント契約の終了日 | TNT.1-MGMT.1 |
| created_at | TIMESTAMP | NO | NO | CURRENT_TIMESTAMP | 作成日時 | PLT.1-WEB.1 |
| updated_at | TIMESTAMP | NO | NO | CURRENT_TIMESTAMP | 更新日時 | PLT.1-WEB.1 |
| is_deleted | BOOLEAN | NO | NO | - | 論理削除フラグ | PLT.1-WEB.1 |

## インデックス定義

| インデックス名 | 対象カラム | ユニーク | 説明 |
|----------------|------------|----------|------|
| idx_tenant_id | tenant_id | YES | テナントID検索用（一意） |
| idx_tenant_code | tenant_code | YES | テナントコード検索用（一意） |
| idx_domain_name | domain_name | YES | ドメイン名検索用（一意） |
| idx_subdomain | subdomain | YES | サブドメイン検索用（一意） |
| idx_tenant_type | tenant_type | NO | テナント種別検索用 |
| idx_parent_tenant_id | parent_tenant_id | NO | 親テナント検索用 |
| idx_subscription_plan | subscription_plan | NO | サブスクリプションプラン検索用 |
| idx_status | status | NO | ステータス検索用 |
| idx_admin_email | admin_email | NO | 管理者メール検索用 |

## 外部キー定義

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 |
|------------|--------|--------------|------------|--------|--------|
| fk_tenant_parent | parent_tenant_id | MST_Tenant | tenant_id | CASCADE | SET NULL |

---
生成日時: 2025-06-11 01:52:36
