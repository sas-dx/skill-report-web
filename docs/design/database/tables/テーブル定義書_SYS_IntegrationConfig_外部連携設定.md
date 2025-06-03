# テーブル定義書: SYS_IntegrationConfig

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | SYS_IntegrationConfig |
| 論理名 | 外部連携設定 |
| カテゴリ | システム系 |
| 生成日時 | 2025-06-04 06:57:02 |

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
| id | ID | VARCHAR | 50 | ○ |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  | マルチテナント識別子 |
| integration_key | 連携キー | VARCHAR | 100 | ○ |  | 連携設定の識別キー（例：slack_webhook、teams_connector等） |
| integration_name | 連携名 | VARCHAR | 200 | ○ |  | 連携設定の表示名 |
| integration_type | 連携タイプ | ENUM |  | ○ |  | 連携の種類（WEBHOOK:Webhook、API:REST API、OAUTH:OAuth認証、SMTP:メール送信） |
| endpoint_url | エンドポイントURL | VARCHAR | 500 | ○ |  | 連携先のエンドポイントURL |
| auth_type | 認証タイプ | ENUM |  | ○ |  | 認証方式（NONE:認証なし、BASIC:Basic認証、BEARER:Bearer Token、OAUTH2:OAuth2.0、API_KEY:APIキー） |
| auth_config | 認証設定 | TEXT |  | ○ |  | 認証に必要な設定情報（JSON形式、暗号化必須） |
| connection_config | 接続設定 | TEXT |  | ○ |  | 接続に関する設定情報（JSON形式） |
| request_headers | リクエストヘッダー | TEXT |  | ○ |  | デフォルトリクエストヘッダー（JSON形式） |
| timeout_seconds | タイムアウト秒数 | INTEGER |  | ○ | 30 | 接続タイムアウト時間（秒） |
| retry_count | リトライ回数 | INTEGER |  | ○ | 3 | 失敗時のリトライ回数 |
| retry_interval | リトライ間隔 | INTEGER |  | ○ | 5 | リトライ間隔（秒） |
| rate_limit_per_minute | 分間レート制限 | INTEGER |  | ○ |  | 1分間あたりのリクエスト制限数 |
| is_enabled | 有効フラグ | BOOLEAN |  | ○ | True | 連携設定が有効かどうか |
| health_check_url | ヘルスチェックURL | VARCHAR | 500 | ○ |  | 連携先の死活監視用URL |
| last_health_check | 最終ヘルスチェック | TIMESTAMP |  | ○ |  | 最終ヘルスチェック実行日時 |
| health_status | ヘルス状態 | ENUM |  | ○ |  | 連携先の状態（HEALTHY:正常、UNHEALTHY:異常、UNKNOWN:不明） |
| is_deleted | 削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_integration_config_tenant_key | tenant_id, integration_key | ○ | テナント別連携キー検索用（一意） |
| idx_integration_config_type | integration_type | × | 連携タイプ別検索用 |
| idx_integration_config_enabled | is_enabled | × | 有効設定検索用 |
| idx_integration_config_health | health_status, last_health_check | × | ヘルス状態検索用 |
| idx_integration_config_auth_type | auth_type | × | 認証タイプ別検索用 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_integration_config_tenant_key | UNIQUE |  | テナント内連携キー一意制約 |
| chk_integration_config_type | CHECK | integration_type IN ('WEBHOOK', 'API', 'OAUTH', 'SMTP') | 連携タイプ値チェック制約 |
| chk_integration_config_auth_type | CHECK | auth_type IN ('NONE', 'BASIC', 'BEARER', 'OAUTH2', 'API_KEY') | 認証タイプ値チェック制約 |
| chk_integration_config_health_status | CHECK | health_status IS NULL OR health_status IN ('HEALTHY', 'UNHEALTHY', 'UNKNOWN') | ヘルス状態値チェック制約 |
| chk_integration_config_timeout_positive | CHECK | timeout_seconds > 0 | タイムアウト秒数正数チェック制約 |
| chk_integration_config_retry_positive | CHECK | retry_count >= 0 AND retry_interval >= 0 | リトライ設定正数チェック制約 |

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

## 業務ルール

- 同一テナント内で連携キーは重複不可
- 無効化された設定は連携処理から除外される
- 認証情報は暗号化して保存する
- タイムアウト・リトライ設定は正数である必要がある
- レート制限は外部システムの制約に応じて設定
- ヘルスチェックは定期的に実行し状態を更新
- OAuth2認証の場合はトークン更新処理が必要
- SMTP設定の場合は送信テストを実行して確認

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 外部連携設定システムテーブルの詳細定義 |
