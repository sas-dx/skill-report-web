# テーブル定義書: MST_Tenant

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_Tenant |
| 論理名 | テナント（組織） |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 17:20:33 |

## 概要

マルチテナント対応システムにおける組織・会社情報を管理するマスタテーブル。
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


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| tenant_id | テナントを一意に識別するID | VARCHAR | 50 | × |  | テナントを一意に識別するID |
| tenant_code | テナントの識別コード | VARCHAR | 20 | × |  | テナントの識別コード（URL等で使用） |
| tenant_name | テナント | VARCHAR | 200 | × |  | テナント（組織・会社）の正式名称 |
| tenant_name_en | テナントの英語名称 | VARCHAR | 200 | ○ |  | テナントの英語名称 |
| tenant_short_name | テナントの略称・短縮名 | VARCHAR | 50 | ○ |  | テナントの略称・短縮名 |
| tenant_type | テナントの種別 | VARCHAR | 20 | × | ENTERPRISE | テナントの種別（ENTERPRISE:企業、DEPARTMENT:部門、SUBSIDIARY:子会社、PARTNER:パートナー、TRIAL:試用） |
| parent_tenant_id | 親テナントのID | VARCHAR | 50 | ○ |  | 親テナントのID（階層構造の場合） |
| tenant_level | テナント階層のレベル | INTEGER |  | × | 1 | テナント階層のレベル（1が最上位） |
| domain_name | テナント専用ドメイン名 | VARCHAR | 100 | ○ |  | テナント専用ドメイン名 |
| subdomain | サブドメイン名 | VARCHAR | 50 | ○ |  | サブドメイン名（xxx.system.com） |
| logo_url | テナントロゴ画像のURL | VARCHAR | 500 | ○ |  | テナントロゴ画像のURL |
| primary_color | テナントのプライマリカラー | VARCHAR | 7 | ○ |  | テナントのプライマリカラー（#RRGGBB） |
| secondary_color | テナントのセカンダリカラー | VARCHAR | 7 | ○ |  | テナントのセカンダリカラー（#RRGGBB） |
| timezone | テナントのデフォルトタイムゾーン | VARCHAR | 50 | × | Asia/Tokyo | テナントのデフォルトタイムゾーン |
| locale | テナントのデフォルトロケール | VARCHAR | 10 | × | ja_JP | テナントのデフォルトロケール |
| currency_code | テナントで使用する通貨コード | VARCHAR | 3 | × | JPY | テナントで使用する通貨コード（ISO 4217） |
| admin_email | テナント管理者のメールアドレス | VARCHAR | 255 | × |  | テナント管理者のメールアドレス |
| contact_email | テナントの一般連絡先メールアドレス | VARCHAR | 255 | ○ |  | テナントの一般連絡先メールアドレス |
| phone_number | テナントの電話番号 | VARCHAR | 20 | ○ |  | テナントの電話番号 |
| address | テナントの住所 | TEXT |  | ○ |  | テナントの住所 |
| postal_code | 郵便番号 | VARCHAR | 10 | ○ |  | 郵便番号 |
| country_code | 国コード | VARCHAR | 2 | × | JP | 国コード（ISO 3166-1 alpha-2） |
| subscription_plan | 契約プラン | VARCHAR | 20 | × | BASIC | 契約プラン（FREE:無料、BASIC:基本、STANDARD:標準、PREMIUM:プレミアム、ENTERPRISE:エンタープライズ） |
| max_users | 契約上の最大ユーザー数 | INTEGER |  | × | 100 | 契約上の最大ユーザー数 |
| max_storage_gb | 契約上の最大ストレージ容量 | INTEGER |  | × | 10 | 契約上の最大ストレージ容量（GB） |
| status | テナントの状態 | VARCHAR | 20 | × | TRIAL | テナントの状態（ACTIVE:有効、INACTIVE:無効、SUSPENDED:停止、TRIAL:試用中、EXPIRED:期限切れ） |
| contract_start_date | テナント契約の開始日 | DATE |  | × |  | テナント契約の開始日 |
| contract_end_date | テナント契約の終了日 | DATE |  | ○ |  | テナント契約の終了日 |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |

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
| idx_admin_email | admin_email | × | 管理者メール検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_tenant_parent | None | None | None | CASCADE | SET NULL |  |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_mst_tenant | PRIMARY KEY | tenant_id | 主キー制約 |
| uk_tenant_id | UNIQUE |  | tenant_id一意制約 |
| uk_tenant_code | UNIQUE |  | tenant_code一意制約 |
| uk_domain_name | UNIQUE |  | domain_name一意制約 |
| uk_subdomain | UNIQUE |  | subdomain一意制約 |
| chk_tenant_type | CHECK | tenant_type IN (...) | tenant_type値チェック制約 |
| chk_tenant_level | CHECK | tenant_level > 0 | tenant_level正値チェック制約 |
| chk_status | CHECK | status IN (...) | status値チェック制約 |

## サンプルデータ

| tenant_id | tenant_code | tenant_name | tenant_name_en | tenant_short_name | tenant_type | parent_tenant_id | tenant_level | domain_name | subdomain | logo_url | primary_color | secondary_color | timezone | locale | currency_code | admin_email | contact_email | phone_number | address | postal_code | country_code | subscription_plan | max_users | max_storage_gb | status | contract_start_date | contract_end_date | is_deleted |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| tenant_001 | main-corp | メイン株式会社 | Main Corporation | メイン | ENTERPRISE | None | 1 | main-corp.com | main | https://cdn.example.com/logos/main-corp.png | #0066CC | #FF6600 | Asia/Tokyo | ja_JP | JPY | admin@main-corp.com | contact@main-corp.com | 03-1234-5678 | 東京都千代田区丸の内1-1-1 | 100-0005 | JP | ENTERPRISE | 1000 | 100 | ACTIVE | 2025-04-01 | None | False |
| tenant_002 | sub-division | サブ事業部 | Sub Division | サブ | DEPARTMENT | tenant_001 | 2 | None | sub | None | #0066CC | #FF6600 | Asia/Tokyo | ja_JP | JPY | admin@sub.main-corp.com | None | None | None | None | JP | STANDARD | 100 | 20 | ACTIVE | 2025-04-01 | None | False |

## 特記事項

- 現在はシングルテナント実装のため、1レコードのみ存在
- 将来のマルチテナント化に備えた完全な設計を実装
- parent_tenant_idによる自己参照で組織階層を表現
- domain_name、subdomainは一意制約でテナント分離を保証
- カラーコードは#RRGGBB形式で統一（UI表示用）
- 契約情報（プラン、制限値）は課金システムとの連携を想定
- 論理削除は is_deleted フラグで管理
- タイムゾーン・ロケール設定でグローバル対応

## 業務ルール

- テナントID（tenant_id）は一意で変更不可
- テナントコード（tenant_code）はURL等で使用するため英数字のみ
- ドメイン名・サブドメインは重複不可（テナント分離保証）
- 親テナント（parent_tenant_id）は同一テナント種別内のみ設定可能
- 契約開始日（contract_start_date）は必須、終了日は無期限契約の場合NULL
- 最大ユーザー数・ストレージ容量は契約プランに応じて設定
- ステータスがINACTIVE/SUSPENDEDの場合、ログイン不可
- 管理者メール（admin_email）は必須、システム通知の送信先
- 論理削除時は関連する全データも論理削除対象
- 階層レベル（tenant_level）は親子関係の整合性を保証

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - MST_Tenantテーブルの詳細定義 |
| 1.1.0 | 2025-06-12 | 開発チーム | 必須セクション追加 - revision_history, overview, notes, business_rules |