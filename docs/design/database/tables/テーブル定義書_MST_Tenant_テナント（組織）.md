# テーブル定義書: MST_Tenant

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_Tenant |
| 論理名 | テナント（組織） |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-04 06:57:02 |

## 概要

MST_Tenant（テナント）は、マルチテナント対応システムにおける組織・会社情報を管理するマスタテーブルです。

主な目的：
- マルチテナント環境での組織分離
- 組織固有の設定・ポリシー管理
- データアクセス制御の基盤
- 組織階層・関連の管理
- 課金・契約管理の基盤

このテーブルにより、複数の組織が同一システムを安全に利用でき、
組織ごとの独立性とカスタマイズを実現できます。



## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| tenant_id | テナントID | VARCHAR | 50 | ○ |  | テナントを一意に識別するID |
| tenant_code | テナントコード | VARCHAR | 20 | ○ |  | テナントの識別コード（URL等で使用） |
| tenant_name | テナント名 | VARCHAR | 200 | ○ |  | テナント（組織・会社）の正式名称 |
| tenant_name_en | テナント名（英語） | VARCHAR | 200 | ○ |  | テナントの英語名称 |
| tenant_short_name | テナント略称 | VARCHAR | 50 | ○ |  | テナントの略称・短縮名 |
| tenant_type | テナント種別 | ENUM |  | ○ |  | テナントの種別（ENTERPRISE:企業、DEPARTMENT:部門、SUBSIDIARY:子会社、PARTNER:パートナー、TRIAL:試用） |
| parent_tenant_id | 親テナントID | VARCHAR | 50 | ○ |  | 親テナントのID（階層構造の場合） |
| tenant_level | テナントレベル | INTEGER |  | ○ | 1 | テナント階層のレベル（1が最上位） |
| domain_name | ドメイン名 | VARCHAR | 100 | ○ |  | テナント専用ドメイン名 |
| subdomain | サブドメイン | VARCHAR | 50 | ○ |  | サブドメイン名（xxx.system.com） |
| logo_url | ロゴURL | VARCHAR | 500 | ○ |  | テナントロゴ画像のURL |
| primary_color | プライマリカラー | VARCHAR | 7 | ○ |  | テナントのプライマリカラー（#RRGGBB） |
| secondary_color | セカンダリカラー | VARCHAR | 7 | ○ |  | テナントのセカンダリカラー（#RRGGBB） |
| timezone | タイムゾーン | VARCHAR | 50 | ○ | Asia/Tokyo | テナントのデフォルトタイムゾーン |
| locale | ロケール | VARCHAR | 10 | ○ | ja_JP | テナントのデフォルトロケール |
| currency_code | 通貨コード | VARCHAR | 3 | ○ | JPY | テナントで使用する通貨コード（ISO 4217） |
| date_format | 日付フォーマット | VARCHAR | 20 | ○ | YYYY-MM-DD | テナントで使用する日付フォーマット |
| time_format | 時刻フォーマット | VARCHAR | 20 | ○ | HH:mm:ss | テナントで使用する時刻フォーマット |
| admin_email | 管理者メール | VARCHAR | 255 | ○ |  | テナント管理者のメールアドレス |
| contact_email | 連絡先メール | VARCHAR | 255 | ○ |  | テナントの一般連絡先メールアドレス |
| phone_number | 電話番号 | VARCHAR | 20 | ○ |  | テナントの電話番号 |
| address | 住所 | TEXT |  | ○ |  | テナントの住所 |
| postal_code | 郵便番号 | VARCHAR | 10 | ○ |  | 郵便番号 |
| country_code | 国コード | VARCHAR | 2 | ○ | JP | 国コード（ISO 3166-1 alpha-2） |
| subscription_plan | サブスクリプションプラン | ENUM |  | ○ | BASIC | 契約プラン（FREE:無料、BASIC:基本、STANDARD:標準、PREMIUM:プレミアム、ENTERPRISE:エンタープライズ） |
| max_users | 最大ユーザー数 | INTEGER |  | ○ | 100 | 契約上の最大ユーザー数 |
| max_storage_gb | 最大ストレージ容量 | INTEGER |  | ○ | 10 | 契約上の最大ストレージ容量（GB） |
| features_enabled | 有効機能 | TEXT |  | ○ |  | 有効化されている機能一覧（JSON形式） |
| custom_settings | カスタム設定 | TEXT |  | ○ |  | テナント固有のカスタム設定（JSON形式） |
| security_policy | セキュリティポリシー | TEXT |  | ○ |  | テナントのセキュリティポリシー設定（JSON形式） |
| data_retention_days | データ保持期間 | INTEGER |  | ○ | 2555 | データの保持期間（日数） |
| backup_enabled | バックアップ有効 | BOOLEAN |  | ○ | True | 自動バックアップが有効かどうか |
| backup_frequency | バックアップ頻度 | ENUM |  | ○ | DAILY | バックアップの実行頻度（DAILY:日次、WEEKLY:週次、MONTHLY:月次） |
| contract_start_date | 契約開始日 | DATE |  | ○ |  | テナント契約の開始日 |
| contract_end_date | 契約終了日 | DATE |  | ○ |  | テナント契約の終了日 |
| trial_end_date | 試用期間終了日 | DATE |  | ○ |  | 試用期間の終了日 |
| billing_cycle | 請求サイクル | ENUM |  | ○ | MONTHLY | 請求の周期（MONTHLY:月次、QUARTERLY:四半期、ANNUAL:年次） |
| monthly_fee | 月額料金 | DECIMAL | 10,2 | ○ |  | 月額利用料金 |
| setup_fee | 初期費用 | DECIMAL | 10,2 | ○ |  | 初期セットアップ費用 |
| status | ステータス | ENUM |  | ○ | TRIAL | テナントの状態（ACTIVE:有効、INACTIVE:無効、SUSPENDED:停止、TRIAL:試用中、EXPIRED:期限切れ） |
| activation_date | 有効化日 | DATE |  | ○ |  | テナントが有効化された日 |
| suspension_date | 停止日 | DATE |  | ○ |  | テナントが停止された日 |
| suspension_reason | 停止理由 | TEXT |  | ○ |  | テナント停止の理由 |
| last_login_date | 最終ログイン日 | DATE |  | ○ |  | テナント内での最終ログイン日 |
| current_users_count | 現在ユーザー数 | INTEGER |  | ○ | 0 | 現在のアクティブユーザー数 |
| storage_used_gb | 使用ストレージ容量 | DECIMAL | 10,3 | ○ | 0.0 | 現在使用中のストレージ容量（GB） |
| api_rate_limit | API制限数 | INTEGER |  | ○ | 1000 | 1時間あたりのAPI呼び出し制限数 |
| sso_enabled | SSO有効 | BOOLEAN |  | ○ | False | シングルサインオンが有効かどうか |
| sso_provider | SSOプロバイダー | VARCHAR | 50 | ○ |  | SSOプロバイダー名（SAML、OAuth等） |
| sso_config | SSO設定 | TEXT |  | ○ |  | SSO設定情報（JSON形式） |
| webhook_url | Webhook URL | VARCHAR | 500 | ○ |  | イベント通知用のWebhook URL |
| webhook_secret | Webhook秘密鍵 | VARCHAR | 100 | ○ |  | Webhook認証用の秘密鍵 |
| created_by | 作成者 | VARCHAR | 50 | ○ |  | テナントを作成したユーザーID |
| notes | 備考 | TEXT |  | ○ |  | テナントに関する備考・メモ |
| code | コード | VARCHAR | 20 | × |  | マスタコード |
| name | 名称 | VARCHAR | 100 | × |  | マスタ名称 |
| description | 説明 | TEXT |  | ○ |  | マスタ説明 |

## インデックス

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

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_tenant_parent | parent_tenant_id | MST_Tenant | tenant_id | CASCADE | SET NULL | 親テナントへの外部キー（自己参照） |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_tenant_id | UNIQUE |  | テナントID一意制約 |
| uk_tenant_code | UNIQUE |  | テナントコード一意制約 |
| uk_domain_name | UNIQUE |  | ドメイン名一意制約 |
| uk_subdomain | UNIQUE |  | サブドメイン一意制約 |
| chk_tenant_type | CHECK | tenant_type IN ('ENTERPRISE', 'DEPARTMENT', 'SUBSIDIARY', 'PARTNER', 'TRIAL') | テナント種別値チェック制約 |
| chk_subscription_plan | CHECK | subscription_plan IN ('FREE', 'BASIC', 'STANDARD', 'PREMIUM', 'ENTERPRISE') | サブスクリプションプラン値チェック制約 |
| chk_backup_frequency | CHECK | backup_frequency IN ('DAILY', 'WEEKLY', 'MONTHLY') | バックアップ頻度値チェック制約 |
| chk_billing_cycle | CHECK | billing_cycle IN ('MONTHLY', 'QUARTERLY', 'ANNUAL') | 請求サイクル値チェック制約 |
| chk_status | CHECK | status IN ('ACTIVE', 'INACTIVE', 'SUSPENDED', 'TRIAL', 'EXPIRED') | ステータス値チェック制約 |
| chk_tenant_level_positive | CHECK | tenant_level > 0 | テナントレベル正数チェック制約 |
| chk_max_users_positive | CHECK | max_users > 0 | 最大ユーザー数正数チェック制約 |
| chk_max_storage_positive | CHECK | max_storage_gb > 0 | 最大ストレージ容量正数チェック制約 |
| chk_data_retention_positive | CHECK | data_retention_days > 0 | データ保持期間正数チェック制約 |
| chk_contract_period | CHECK | contract_end_date IS NULL OR contract_start_date <= contract_end_date | 契約期間整合性チェック制約 |
| chk_current_users_range | CHECK | current_users_count >= 0 AND current_users_count <= max_users | 現在ユーザー数範囲チェック制約 |
| chk_storage_used_positive | CHECK | storage_used_gb >= 0 | 使用ストレージ容量非負数チェック制約 |
| chk_api_rate_limit_positive | CHECK | api_rate_limit > 0 | API制限数正数チェック制約 |

## サンプルデータ

| tenant_id | tenant_code | tenant_name | tenant_name_en | tenant_short_name | tenant_type | parent_tenant_id | tenant_level | domain_name | subdomain | logo_url | primary_color | secondary_color | timezone | locale | currency_code | date_format | time_format | admin_email | contact_email | phone_number | address | postal_code | country_code | subscription_plan | max_users | max_storage_gb | features_enabled | custom_settings | security_policy | data_retention_days | backup_enabled | backup_frequency | contract_start_date | contract_end_date | trial_end_date | billing_cycle | monthly_fee | setup_fee | status | activation_date | suspension_date | suspension_reason | last_login_date | current_users_count | storage_used_gb | api_rate_limit | sso_enabled | sso_provider | sso_config | webhook_url | webhook_secret | created_by | notes |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| TENANT_001 | acme-corp | 株式会社ACME | ACME Corporation | ACME | ENTERPRISE | None | 1 | acme-corp.com | acme | https://cdn.example.com/logos/acme-corp.png | #0066CC | #FF6600 | Asia/Tokyo | ja_JP | JPY | YYYY-MM-DD | HH:mm:ss | admin@acme-corp.com | contact@acme-corp.com | 03-1234-5678 | 東京都千代田区丸の内1-1-1 | 100-0005 | JP | ENTERPRISE | 1000 | 1000 | ["advanced_analytics", "custom_reports", "api_access", "sso", "audit_logs"] | {"theme": "corporate", "dashboard_layout": "advanced", "notification_preferences": {"email": true, "slack": true}} | {"password_policy": {"min_length": 8, "require_special_chars": true}, "session_timeout": 480, "ip_whitelist": ["192.168.1.0/24"]} | 2555 | True | DAILY | 2024-01-01 | 2024-12-31 | None | ANNUAL | 50000.0 | 100000.0 | ACTIVE | 2024-01-01 | None | None | 2024-06-01 | 250 | 125.5 | 10000 | True | SAML | {"entity_id": "acme-corp", "sso_url": "https://sso.acme-corp.com/saml", "certificate": "..."} | https://api.acme-corp.com/webhooks/skill-system | webhook_secret_key_123 | SYSTEM | 大手企業向けエンタープライズプラン |
| TENANT_002 | beta-tech | ベータテクノロジー株式会社 | Beta Technology Inc. | BetaTech | ENTERPRISE | None | 1 | None | beta-tech | https://cdn.example.com/logos/beta-tech.png | #28A745 | #6C757D | Asia/Tokyo | ja_JP | JPY | YYYY/MM/DD | HH:mm | admin@beta-tech.co.jp | info@beta-tech.co.jp | 06-9876-5432 | 大阪府大阪市北区梅田2-2-2 | 530-0001 | JP | STANDARD | 200 | 100 | ["basic_analytics", "standard_reports", "api_access"] | {"theme": "modern", "dashboard_layout": "standard"} | {"password_policy": {"min_length": 6, "require_special_chars": false}, "session_timeout": 240} | 1825 | True | WEEKLY | 2024-03-01 | 2025-02-28 | None | MONTHLY | 15000.0 | 30000.0 | ACTIVE | 2024-03-01 | None | None | 2024-05-30 | 85 | 23.75 | 2000 | False | None | None | None | None | SYSTEM | 中堅企業向けスタンダードプラン |

## 特記事項

- マルチテナント環境でのデータ分離の基盤テーブル
- 階層構造により親子関係のある組織に対応
- カスタム設定により組織固有の要件に対応
- セキュリティポリシーで組織ごとのセキュリティ要件を管理
- 使用量監視により契約制限の遵守を確保
- SSO連携により既存認証システムとの統合が可能

## 業務ルール

- テナントID、テナントコード、ドメイン名、サブドメインは一意である必要がある
- テナントレベルは正数である必要がある
- 現在ユーザー数は最大ユーザー数以下である必要がある
- 契約開始日は契約終了日以前である必要がある
- 使用ストレージ容量は最大ストレージ容量以下である必要がある
- 親テナントのレベルは子テナントより小さい必要がある
- 試用期間中のテナントは機能制限がある
- 停止中のテナントはログイン不可

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - テナント（組織）マスタの詳細定義 |
