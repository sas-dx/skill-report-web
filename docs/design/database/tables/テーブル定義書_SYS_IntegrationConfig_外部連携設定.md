# テーブル定義書: SYS_IntegrationConfig

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | SYS_IntegrationConfig |
| 論理名 | 外部連携設定 |
| カテゴリ | システム系 |
| 生成日時 | 2025-06-24 22:56:15 |

## 概要

SYS_IntegrationConfig（外部連携設定）は、外部システムとの連携に必要な設定情報を管理するシステムテーブルです。
主な目的：
- 外部API接続設定の管理
- 認証情報・エンドポイント情報の管理
- 連携パラメータ・設定値の管理
- 外部システム別設定の管理
- テナント別連携設定の管理
このテーブルは、通知・連携管理機能において外部システムとの安全で効率的な連携を実現する重要なシステムデータです。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | ID | VARCHAR | 50 | ○ |  | ID |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  | テナントID |
| auth_config | 認証設定 | TEXT |  | ○ |  | 認証設定 |
| auth_type | 認証タイプ | ENUM |  | ○ |  | 認証タイプ |
| connection_config | 接続設定 | TEXT |  | ○ |  | 接続設定 |
| endpoint_url | エンドポイントURL | VARCHAR | 500 | ○ |  | エンドポイントURL |
| health_check_url | ヘルスチェックURL | VARCHAR | 500 | ○ |  | ヘルスチェックURL |
| health_status | ヘルス状態 | ENUM |  | ○ |  | ヘルス状態 |
| integration_key | 連携キー | VARCHAR | 100 | ○ |  | 連携キー |
| integration_name | 連携名 | VARCHAR | 200 | ○ |  | 連携名 |
| integration_type | 連携タイプ | ENUM |  | ○ |  | 連携タイプ |
| integrationconfig_id | SYS_IntegrationConfigの主キー | SERIAL |  | × |  | SYS_IntegrationConfigの主キー |
| is_enabled | 有効フラグ | BOOLEAN |  | ○ | True | 有効フラグ |
| last_health_check | 最終ヘルスチェック | TIMESTAMP |  | ○ |  | 最終ヘルスチェック |
| rate_limit_per_minute | 分間レート制限 | INTEGER |  | ○ |  | 分間レート制限 |
| request_headers | リクエストヘッダー | TEXT |  | ○ |  | リクエストヘッダー |
| retry_count | リトライ回数 | INTEGER |  | ○ | 3 | リトライ回数 |
| retry_interval | リトライ間隔 | INTEGER |  | ○ | 5 | リトライ間隔 |
| timeout_seconds | タイムアウト秒数 | INTEGER |  | ○ | 30 | タイムアウト秒数 |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_integration_config_tenant_key | tenant_id, integration_key | ○ |  |
| idx_integration_config_type | integration_type | × |  |
| idx_integration_config_enabled | is_enabled | × |  |
| idx_integration_config_health | health_status, last_health_check | × |  |
| idx_integration_config_auth_type | auth_type | × |  |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| chk_auth_type | CHECK | auth_type IN (...) | auth_type値チェック制約 |
| chk_health_status | CHECK | health_status IN (...) | health_status値チェック制約 |
| chk_integration_type | CHECK | integration_type IN (...) | integration_type値チェック制約 |

## サンプルデータ

| id | tenant_id | integration_key | integration_name | integration_type | endpoint_url | auth_type | auth_config | connection_config | request_headers | timeout_seconds | retry_count | retry_interval | rate_limit_per_minute | is_enabled | health_check_url | last_health_check | health_status |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| IC001 | TENANT001 | slack_webhook | Slack通知連携 | WEBHOOK | https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX | NONE | None | {"channel": "#notifications", "username": "SkillBot", "icon_emoji": ":robot_face:"} | {"Content-Type": "application/json"} | 30 | 3 | 5 | 60 | True | None | None | UNKNOWN |
| IC002 | TENANT001 | teams_connector | Microsoft Teams連携 | WEBHOOK | https://outlook.office.com/webhook/xxx/IncomingWebhook/yyy/zzz | NONE | None | {"title": "スキル管理システム", "theme_color": "0078D4"} | {"Content-Type": "application/json"} | 30 | 3 | 5 | 30 | True | None | None | UNKNOWN |
| IC003 | TENANT001 | smtp_server | メール送信サーバー | SMTP | smtp.company.com:587 | BASIC | {"username": "noreply@company.com", "password": "encrypted_password"} | {"use_tls": true, "use_ssl": false, "from_address": "noreply@company.com", "from_name": "スキル管理システム"} | None | 60 | 2 | 10 | 100 | True | None | 2025-06-01 19:00:00 | HEALTHY |

## 特記事項

- 認証設定（auth_config）は暗号化必須
- 接続設定・リクエストヘッダーはJSON形式で柔軟な設定に対応
- レート制限により外部システムへの負荷を制御
- ヘルスチェック機能により連携先の状態を監視
- リトライ機能により一時的な障害に対応
- テナント別設定により個別カスタマイズに対応
- 無効化された設定は連携処理から除外される
- 同一テナント内で連携キーは重複不可
- 無効化された設定は連携処理から除外される
- 認証情報は暗号化して保存する
- タイムアウト・リトライ設定は正数である必要がある
- レート制限は外部システムの制約に応じて設定
- ヘルスチェックは定期的に実行し状態を更新
- OAuth2認証の場合はトークン更新処理が必要
- SMTP設定の場合は送信テストを実行して確認

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 外部連携設定システムテーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214007 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214907 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215000 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215054 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223433 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |