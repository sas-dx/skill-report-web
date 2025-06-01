# テーブル定義書: MST_Tenant (テナント管理)

## 📋 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_Tenant |
| 論理名 | テナント管理 |
| カテゴリ | マスタ系 |
| 作成日 | 2025-06-01 |

> **注意**: 本テーブル定義書は自動生成されます。手動編集は行わないでください。
> 詳細定義の変更は `table-details/MST_Tenant_details.yaml` で行ってください。


## 📝 改版履歴

> **注意**: 改版履歴の詳細は以下のYAMLファイルで管理されています：
> `table-details/TABLE_NAME_details.yaml`

| バージョン | 更新日 | 更新者 | 主な変更内容 |
|------------|--------|--------|-------------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - テナント（組織）マスタの詳細定義 |


## 📝 テーブル概要

MST_Tenant（テナント）は、マルチテナント対応システムにおける組織・会社情報を管理するマスタテーブルです。

主な目的：
- マルチテナント環境での組織分離
- 組織固有の設定・ポリシー管理
- データアクセス制御の基盤
- 組織階層・関連の管理
- 課金・契約管理の基盤

このテーブルにより、複数の組織が同一システムを安全に利用でき、
組織ごとの独立性とカスタマイズを実現できます。


## 🗂️ カラム定義

| カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト | 説明 |
|----------|--------|----------|------|------|----|----|------------|------|
| id | ID | VARCHAR | 50 | × | ● |  |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × |  |  |  | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  |  |  | マルチテナント識別子 |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  |  |  | テナントを一意に識別するID |
| tenant_code | テナントコード | VARCHAR | 20 | ○ |  |  |  | テナントの識別コード（URL等で使用） |
| tenant_name | テナント名 | VARCHAR | 200 | ○ |  |  |  | テナント（組織・会社）の正式名称 |
| tenant_name_en | テナント名（英語） | VARCHAR | 200 | ○ |  |  |  | テナントの英語名称 |
| tenant_short_name | テナント略称 | VARCHAR | 50 | ○ |  |  |  | テナントの略称・短縮名 |
| tenant_type | テナント種別 | ENUM |  | ○ |  |  |  | テナントの種別（ENTERPRISE:企業、DEPARTMENT:部門、SUBSIDIARY:子会社、PARTNER:パートナー、TRIAL:試用） |
| parent_tenant_id | 親テナントID | VARCHAR | 50 | ○ |  | ● |  | 親テナントのID（階層構造の場合） |
| tenant_level | テナントレベル | INTEGER |  | ○ |  |  | 1 | テナント階層のレベル（1が最上位） |
| domain_name | ドメイン名 | VARCHAR | 100 | ○ |  |  |  | テナント専用ドメイン名 |
| subdomain | サブドメイン | VARCHAR | 50 | ○ |  |  |  | サブドメイン名（xxx.system.com） |
| logo_url | ロゴURL | VARCHAR | 500 | ○ |  |  |  | テナントロゴ画像のURL |
| primary_color | プライマリカラー | VARCHAR | 7 | ○ |  |  |  | テナントのプライマリカラー（#RRGGBB） |
| secondary_color | セカンダリカラー | VARCHAR | 7 | ○ |  |  |  | テナントのセカンダリカラー（#RRGGBB） |
| timezone | タイムゾーン | VARCHAR | 50 | ○ |  |  | Asia/Tokyo | テナントのデフォルトタイムゾーン |
| locale | ロケール | VARCHAR | 10 | ○ |  |  | ja_JP | テナントのデフォルトロケール |
| currency_code | 通貨コード | VARCHAR | 3 | ○ |  |  | JPY | テナントで使用する通貨コード（ISO 4217） |
| date_format | 日付フォーマット | VARCHAR | 20 | ○ |  |  | YYYY-MM-DD | テナントで使用する日付フォーマット |
| time_format | 時刻フォーマット | VARCHAR | 20 | ○ |  |  | HH:mm:ss | テナントで使用する時刻フォーマット |
| admin_email | 管理者メール | VARCHAR | 255 | ○ |  |  |  | テナント管理者のメールアドレス |
| contact_email | 連絡先メール | VARCHAR | 255 | ○ |  |  |  | テナントの一般連絡先メールアドレス |
| phone_number | 電話番号 | VARCHAR | 20 | ○ |  |  |  | テナントの電話番号 |
| address | 住所 | TEXT |  | ○ |  |  |  | テナントの住所 |
| postal_code | 郵便番号 | VARCHAR | 10 | ○ |  |  |  | 郵便番号 |
| country_code | 国コード | VARCHAR | 2 | ○ |  |  | JP | 国コード（ISO 3166-1 alpha-2） |
| subscription_plan | サブスクリプションプラン | ENUM |  | ○ |  |  | BASIC | 契約プラン（FREE:無料、BASIC:基本、STANDARD:標準、PREMIUM:プレミアム、ENTERPRISE:エンタープライズ） |
| max_users | 最大ユーザー数 | INTEGER |  | ○ |  |  | 100 | 契約上の最大ユーザー数 |
| max_storage_gb | 最大ストレージ容量 | INTEGER |  | ○ |  |  | 10 | 契約上の最大ストレージ容量（GB） |
| features_enabled | 有効機能 | TEXT |  | ○ |  |  |  | 有効化されている機能一覧（JSON形式） |
| custom_settings | カスタム設定 | TEXT |  | ○ |  |  |  | テナント固有のカスタム設定（JSON形式） |
| security_policy | セキュリティポリシー | TEXT |  | ○ |  |  |  | テナントのセキュリティポリシー設定（JSON形式） |
| data_retention_days | データ保持期間 | INTEGER |  | ○ |  |  | 2555 | データの保持期間（日数） |
| backup_enabled | バックアップ有効 | BOOLEAN |  | ○ |  |  | True | 自動バックアップが有効かどうか |
| backup_frequency | バックアップ頻度 | ENUM |  | ○ |  |  | DAILY | バックアップの実行頻度（DAILY:日次、WEEKLY:週次、MONTHLY:月次） |
| contract_start_date | 契約開始日 | DATE |  | ○ |  |  |  | テナント契約の開始日 |
| contract_end_date | 契約終了日 | DATE |  | ○ |  |  |  | テナント契約の終了日 |
| trial_end_date | 試用期間終了日 | DATE |  | ○ |  |  |  | 試用期間の終了日 |
| billing_cycle | 請求サイクル | ENUM |  | ○ |  |  | MONTHLY | 請求の周期（MONTHLY:月次、QUARTERLY:四半期、ANNUAL:年次） |
| monthly_fee | 月額料金 | DECIMAL | 10,2 | ○ |  |  |  | 月額利用料金 |
| setup_fee | 初期費用 | DECIMAL | 10,2 | ○ |  |  |  | 初期セットアップ費用 |
| status | ステータス | ENUM |  | ○ |  |  | TRIAL | テナントの状態（ACTIVE:有効、INACTIVE:無効、SUSPENDED:停止、TRIAL:試用中、EXPIRED:期限切れ） |
| activation_date | 有効化日 | DATE |  | ○ |  |  |  | テナントが有効化された日 |
| suspension_date | 停止日 | DATE |  | ○ |  |  |  | テナントが停止された日 |
| suspension_reason | 停止理由 | TEXT |  | ○ |  |  |  | テナント停止の理由 |
| last_login_date | 最終ログイン日 | DATE |  | ○ |  |  |  | テナント内での最終ログイン日 |
| current_users_count | 現在ユーザー数 | INTEGER |  | ○ |  |  |  | 現在のアクティブユーザー数 |
| storage_used_gb | 使用ストレージ容量 | DECIMAL | 10,3 | ○ |  |  |  | 現在使用中のストレージ容量（GB） |
| api_rate_limit | API制限数 | INTEGER |  | ○ |  |  | 1000 | 1時間あたりのAPI呼び出し制限数 |
| sso_enabled | SSO有効 | BOOLEAN |  | ○ |  |  |  | シングルサインオンが有効かどうか |
| sso_provider | SSOプロバイダー | VARCHAR | 50 | ○ |  |  |  | SSOプロバイダー名（SAML、OAuth等） |
| sso_config | SSO設定 | TEXT |  | ○ |  |  |  | SSO設定情報（JSON形式） |
| webhook_url | Webhook URL | VARCHAR | 500 | ○ |  |  |  | イベント通知用のWebhook URL |
| webhook_secret | Webhook秘密鍵 | VARCHAR | 100 | ○ |  |  |  | Webhook認証用の秘密鍵 |
| created_by | 作成者 | VARCHAR | 50 | ○ |  |  |  | テナントを作成したユーザーID |
| notes | 備考 | TEXT |  | ○ |  |  |  | テナントに関する備考・メモ |
| created_at | 作成日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  |  |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  |  |  | レコード更新者のユーザーID |

## 🔍 インデックス定義

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_tenant_id | tenant_id | ○ | テナントID検索用（一意） |
| idx_tenant_code | tenant_code | ○ | テナントコード検索用（一意） |
| idx_domain_name | domain_name | ○ | ドメイン名検索用（一意） |
| idx_subdomain | subdomain | ○ | サブドメイン検索用（一意） |
| idx_tenant_type | tenant_type | × | テナント種別検索用 |
| idx_parent_tenant_id | parent_tenant_id | × | 親テナント検索用 |
| idx_subscription_plan | subscription_plan | × | サブスクリプションプラン検索用 |
| idx_status | status | × | ステータス検索用 |
| idx_contract_period | contract_start_date, contract_end_date | × | 契約期間検索用 |
| idx_admin_email | admin_email | × | 管理者メール検索用 |

## 🔒 制約定義

| 制約名 | 制約タイプ | 対象カラム | 条件 | 説明 |
|--------|------------|------------|------|------|
| uk_tenant_id | UNIQUE | tenant_id |  | テナントID一意制約 |
| uk_tenant_code | UNIQUE | tenant_code |  | テナントコード一意制約 |
| uk_domain_name | UNIQUE | domain_name |  | ドメイン名一意制約 |
| uk_subdomain | UNIQUE | subdomain |  | サブドメイン一意制約 |
| chk_tenant_type | CHECK |  | tenant_type IN ('ENTERPRISE', 'DEPARTMENT', 'SUBSIDIARY', 'PARTNER', 'TRIAL') | テナント種別値チェック制約 |
| chk_subscription_plan | CHECK |  | subscription_plan IN ('FREE', 'BASIC', 'STANDARD', 'PREMIUM', 'ENTERPRISE') | サブスクリプションプラン値チェック制約 |
| chk_backup_frequency | CHECK |  | backup_frequency IN ('DAILY', 'WEEKLY', 'MONTHLY') | バックアップ頻度値チェック制約 |
| chk_billing_cycle | CHECK |  | billing_cycle IN ('MONTHLY', 'QUARTERLY', 'ANNUAL') | 請求サイクル値チェック制約 |
| chk_status | CHECK |  | status IN ('ACTIVE', 'INACTIVE', 'SUSPENDED', 'TRIAL', 'EXPIRED') | ステータス値チェック制約 |
| chk_tenant_level_positive | CHECK |  | tenant_level > 0 | テナントレベル正数チェック制約 |
| chk_max_users_positive | CHECK |  | max_users > 0 | 最大ユーザー数正数チェック制約 |
| chk_max_storage_positive | CHECK |  | max_storage_gb > 0 | 最大ストレージ容量正数チェック制約 |
| chk_data_retention_positive | CHECK |  | data_retention_days > 0 | データ保持期間正数チェック制約 |
| chk_contract_period | CHECK |  | contract_end_date IS NULL OR contract_start_date <= contract_end_date | 契約期間整合性チェック制約 |
| chk_current_users_range | CHECK |  | current_users_count >= 0 AND current_users_count <= max_users | 現在ユーザー数範囲チェック制約 |
| chk_storage_used_positive | CHECK |  | storage_used_gb >= 0 | 使用ストレージ容量非負数チェック制約 |
| chk_api_rate_limit_positive | CHECK |  | api_rate_limit > 0 | API制限数正数チェック制約 |

## 🔗 外部キー関係

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|------------|--------|--------------|------------|--------|--------|------|
| fk_tenant_parent | parent_tenant_id | MST_Tenant | tenant_id | CASCADE | SET NULL | 親テナントへの外部キー（自己参照） |

## 📊 サンプルデータ

```json
[
  {
    "tenant_id": "TENANT_001",
    "tenant_code": "acme-corp",
    "tenant_name": "株式会社ACME",
    "tenant_name_en": "ACME Corporation",
    "tenant_short_name": "ACME",
    "tenant_type": "ENTERPRISE",
    "parent_tenant_id": null,
    "tenant_level": 1,
    "domain_name": "acme-corp.com",
    "subdomain": "acme",
    "logo_url": "https://cdn.example.com/logos/acme-corp.png",
    "primary_color": "#0066CC",
    "secondary_color": "#FF6600",
    "timezone": "Asia/Tokyo",
    "locale": "ja_JP",
    "currency_code": "JPY",
    "date_format": "YYYY-MM-DD",
    "time_format": "HH:mm:ss",
    "admin_email": "admin@acme-corp.com",
    "contact_email": "contact@acme-corp.com",
    "phone_number": "03-1234-5678",
    "address": "東京都千代田区丸の内1-1-1",
    "postal_code": "100-0005",
    "country_code": "JP",
    "subscription_plan": "ENTERPRISE",
    "max_users": 1000,
    "max_storage_gb": 1000,
    "features_enabled": "[\"advanced_analytics\", \"custom_reports\", \"api_access\", \"sso\", \"audit_logs\"]",
    "custom_settings": "{\"theme\": \"corporate\", \"dashboard_layout\": \"advanced\", \"notification_preferences\": {\"email\": true, \"slack\": true}}",
    "security_policy": "{\"password_policy\": {\"min_length\": 8, \"require_special_chars\": true}, \"session_timeout\": 480, \"ip_whitelist\": [\"192.168.1.0/24\"]}",
    "data_retention_days": 2555,
    "backup_enabled": true,
    "backup_frequency": "DAILY",
    "contract_start_date": "2024-01-01",
    "contract_end_date": "2024-12-31",
    "trial_end_date": null,
    "billing_cycle": "ANNUAL",
    "monthly_fee": 50000.0,
    "setup_fee": 100000.0,
    "status": "ACTIVE",
    "activation_date": "2024-01-01",
    "suspension_date": null,
    "suspension_reason": null,
    "last_login_date": "2024-06-01",
    "current_users_count": 250,
    "storage_used_gb": 125.5,
    "api_rate_limit": 10000,
    "sso_enabled": true,
    "sso_provider": "SAML",
    "sso_config": "{\"entity_id\": \"acme-corp\", \"sso_url\": \"https://sso.acme-corp.com/saml\", \"certificate\": \"...\"}",
    "webhook_url": "https://api.acme-corp.com/webhooks/skill-system",
    "webhook_secret": "webhook_secret_key_123",
    "created_by": "SYSTEM",
    "notes": "大手企業向けエンタープライズプラン"
  },
  {
    "tenant_id": "TENANT_002",
    "tenant_code": "beta-tech",
    "tenant_name": "ベータテクノロジー株式会社",
    "tenant_name_en": "Beta Technology Inc.",
    "tenant_short_name": "BetaTech",
    "tenant_type": "ENTERPRISE",
    "parent_tenant_id": null,
    "tenant_level": 1,
    "domain_name": null,
    "subdomain": "beta-tech",
    "logo_url": "https://cdn.example.com/logos/beta-tech.png",
    "primary_color": "#28A745",
    "secondary_color": "#6C757D",
    "timezone": "Asia/Tokyo",
    "locale": "ja_JP",
    "currency_code": "JPY",
    "date_format": "YYYY/MM/DD",
    "time_format": "HH:mm",
    "admin_email": "admin@beta-tech.co.jp",
    "contact_email": "info@beta-tech.co.jp",
    "phone_number": "06-9876-5432",
    "address": "大阪府大阪市北区梅田2-2-2",
    "postal_code": "530-0001",
    "country_code": "JP",
    "subscription_plan": "STANDARD",
    "max_users": 200,
    "max_storage_gb": 100,
    "features_enabled": "[\"basic_analytics\", \"standard_reports\", \"api_access\"]",
    "custom_settings": "{\"theme\": \"modern\", \"dashboard_layout\": \"standard\"}",
    "security_policy": "{\"password_policy\": {\"min_length\": 6, \"require_special_chars\": false}, \"session_timeout\": 240}",
    "data_retention_days": 1825,
    "backup_enabled": true,
    "backup_frequency": "WEEKLY",
    "contract_start_date": "2024-03-01",
    "contract_end_date": "2025-02-28",
    "trial_end_date": null,
    "billing_cycle": "MONTHLY",
    "monthly_fee": 15000.0,
    "setup_fee": 30000.0,
    "status": "ACTIVE",
    "activation_date": "2024-03-01",
    "suspension_date": null,
    "suspension_reason": null,
    "last_login_date": "2024-05-30",
    "current_users_count": 85,
    "storage_used_gb": 23.75,
    "api_rate_limit": 2000,
    "sso_enabled": false,
    "sso_provider": null,
    "sso_config": null,
    "webhook_url": null,
    "webhook_secret": null,
    "created_by": "SYSTEM",
    "notes": "中堅企業向けスタンダードプラン"
  }
]
```

## 📌 特記事項

- マルチテナント環境でのデータ分離の基盤テーブル
- 階層構造により親子関係のある組織に対応
- カスタム設定により組織固有の要件に対応
- セキュリティポリシーで組織ごとのセキュリティ要件を管理
- 使用量監視により契約制限の遵守を確保
- SSO連携により既存認証システムとの統合が可能

## 📋 業務ルール

- テナントID、テナントコード、ドメイン名、サブドメインは一意である必要がある
- テナントレベルは正数である必要がある
- 現在ユーザー数は最大ユーザー数以下である必要がある
- 契約開始日は契約終了日以前である必要がある
- 使用ストレージ容量は最大ストレージ容量以下である必要がある
- 親テナントのレベルは子テナントより小さい必要がある
- 試用期間中のテナントは機能制限がある
- 停止中のテナントはログイン不可
