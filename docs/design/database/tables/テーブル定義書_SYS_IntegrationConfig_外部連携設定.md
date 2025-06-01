# テーブル定義書: SYS_IntegrationConfig (外部連携設定)

## 📋 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | SYS_IntegrationConfig |
| 論理名 | 外部連携設定 |
| カテゴリ | システム系 |
| 作成日 | 2025-06-01 |

> **注意**: 本テーブル定義書は自動生成されます。手動編集は行わないでください。
> 詳細定義の変更は `table-details/SYS_IntegrationConfig_details.yaml` で行ってください。


## 📝 改版履歴

> **注意**: 改版履歴の詳細は以下のYAMLファイルで管理されています：
> `table-details/TABLE_NAME_details.yaml`

| バージョン | 更新日 | 更新者 | 主な変更内容 |
|------------|--------|--------|-------------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 外部連携設定システムテーブルの詳細定義 |


## 📝 テーブル概要

SYS_IntegrationConfig（外部連携設定）は、外部システムとの連携に必要な設定情報を管理するシステムテーブルです。

主な目的：
- 外部API接続設定の管理
- 認証情報・エンドポイント情報の管理
- 連携パラメータ・設定値の管理
- 外部システム別設定の管理
- テナント別連携設定の管理

このテーブルは、通知・連携管理機能において外部システムとの安全で効率的な連携を実現する重要なシステムデータです。


## 🗂️ カラム定義

| カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト | 説明 |
|----------|--------|----------|------|------|----|----|------------|------|
| id | ID | VARCHAR | 50 | × | ● |  |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × |  |  |  | 論理削除フラグ |
| id | ID | VARCHAR | 50 | ○ |  |  |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  |  |  | マルチテナント識別子 |
| integration_key | 連携キー | VARCHAR | 100 | ○ |  |  |  | 連携設定の識別キー（例：slack_webhook、teams_connector等） |
| integration_name | 連携名 | VARCHAR | 200 | ○ |  |  |  | 連携設定の表示名 |
| integration_type | 連携タイプ | ENUM |  | ○ |  |  |  | 連携の種類（WEBHOOK:Webhook、API:REST API、OAUTH:OAuth認証、SMTP:メール送信） |
| endpoint_url | エンドポイントURL | VARCHAR | 500 | ○ |  |  |  | 連携先のエンドポイントURL |
| auth_type | 認証タイプ | ENUM |  | ○ |  |  |  | 認証方式（NONE:認証なし、BASIC:Basic認証、BEARER:Bearer Token、OAUTH2:OAuth2.0、API_KEY:APIキー） |
| auth_config | 認証設定 | TEXT |  | ○ |  |  |  | 認証に必要な設定情報（JSON形式、暗号化必須） |
| connection_config | 接続設定 | TEXT |  | ○ |  |  |  | 接続に関する設定情報（JSON形式） |
| request_headers | リクエストヘッダー | TEXT |  | ○ |  |  |  | デフォルトリクエストヘッダー（JSON形式） |
| timeout_seconds | タイムアウト秒数 | INTEGER |  | ○ |  |  | 30 | 接続タイムアウト時間（秒） |
| retry_count | リトライ回数 | INTEGER |  | ○ |  |  | 3 | 失敗時のリトライ回数 |
| retry_interval | リトライ間隔 | INTEGER |  | ○ |  |  | 5 | リトライ間隔（秒） |
| rate_limit_per_minute | 分間レート制限 | INTEGER |  | ○ |  |  |  | 1分間あたりのリクエスト制限数 |
| is_enabled | 有効フラグ | BOOLEAN |  | ○ |  |  | True | 連携設定が有効かどうか |
| health_check_url | ヘルスチェックURL | VARCHAR | 500 | ○ |  |  |  | 連携先の死活監視用URL |
| last_health_check | 最終ヘルスチェック | TIMESTAMP |  | ○ |  |  |  | 最終ヘルスチェック実行日時 |
| health_status | ヘルス状態 | ENUM |  | ○ |  |  |  | 連携先の状態（HEALTHY:正常、UNHEALTHY:異常、UNKNOWN:不明） |
| created_at | 作成日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  |  |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  |  |  | レコード更新者のユーザーID |

## 🔍 インデックス定義

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_integration_config_tenant_key | tenant_id, integration_key | ○ | テナント別連携キー検索用（一意） |
| idx_integration_config_type | integration_type | × | 連携タイプ別検索用 |
| idx_integration_config_enabled | is_enabled | × | 有効設定検索用 |
| idx_integration_config_health | health_status, last_health_check | × | ヘルス状態検索用 |
| idx_integration_config_auth_type | auth_type | × | 認証タイプ別検索用 |

## 🔒 制約定義

| 制約名 | 制約タイプ | 対象カラム | 条件 | 説明 |
|--------|------------|------------|------|------|
| uk_integration_config_tenant_key | UNIQUE | tenant_id, integration_key |  | テナント内連携キー一意制約 |
| chk_integration_config_type | CHECK |  | integration_type IN ('WEBHOOK', 'API', 'OAUTH', 'SMTP') | 連携タイプ値チェック制約 |
| chk_integration_config_auth_type | CHECK |  | auth_type IN ('NONE', 'BASIC', 'BEARER', 'OAUTH2', 'API_KEY') | 認証タイプ値チェック制約 |
| chk_integration_config_health_status | CHECK |  | health_status IS NULL OR health_status IN ('HEALTHY', 'UNHEALTHY', 'UNKNOWN') | ヘルス状態値チェック制約 |
| chk_integration_config_timeout_positive | CHECK |  | timeout_seconds > 0 | タイムアウト秒数正数チェック制約 |
| chk_integration_config_retry_positive | CHECK |  | retry_count >= 0 AND retry_interval >= 0 | リトライ設定正数チェック制約 |

## 🔗 外部キー関係

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|------------|--------|--------------|------------|--------|--------|------|

## 📊 サンプルデータ

```json
[
  {
    "id": "IC001",
    "tenant_id": "TENANT001",
    "integration_key": "slack_webhook",
    "integration_name": "Slack通知連携",
    "integration_type": "WEBHOOK",
    "endpoint_url": "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX",
    "auth_type": "NONE",
    "auth_config": null,
    "connection_config": "{\"channel\": \"#notifications\", \"username\": \"SkillBot\", \"icon_emoji\": \":robot_face:\"}",
    "request_headers": "{\"Content-Type\": \"application/json\"}",
    "timeout_seconds": 30,
    "retry_count": 3,
    "retry_interval": 5,
    "rate_limit_per_minute": 60,
    "is_enabled": true,
    "health_check_url": null,
    "last_health_check": null,
    "health_status": "UNKNOWN"
  },
  {
    "id": "IC002",
    "tenant_id": "TENANT001",
    "integration_key": "teams_connector",
    "integration_name": "Microsoft Teams連携",
    "integration_type": "WEBHOOK",
    "endpoint_url": "https://outlook.office.com/webhook/xxx/IncomingWebhook/yyy/zzz",
    "auth_type": "NONE",
    "auth_config": null,
    "connection_config": "{\"title\": \"スキル管理システム\", \"theme_color\": \"0078D4\"}",
    "request_headers": "{\"Content-Type\": \"application/json\"}",
    "timeout_seconds": 30,
    "retry_count": 3,
    "retry_interval": 5,
    "rate_limit_per_minute": 30,
    "is_enabled": true,
    "health_check_url": null,
    "last_health_check": null,
    "health_status": "UNKNOWN"
  },
  {
    "id": "IC003",
    "tenant_id": "TENANT001",
    "integration_key": "smtp_server",
    "integration_name": "メール送信サーバー",
    "integration_type": "SMTP",
    "endpoint_url": "smtp.company.com:587",
    "auth_type": "BASIC",
    "auth_config": "{\"username\": \"noreply@company.com\", \"password\": \"encrypted_password\"}",
    "connection_config": "{\"use_tls\": true, \"use_ssl\": false, \"from_address\": \"noreply@company.com\", \"from_name\": \"スキル管理システム\"}",
    "request_headers": null,
    "timeout_seconds": 60,
    "retry_count": 2,
    "retry_interval": 10,
    "rate_limit_per_minute": 100,
    "is_enabled": true,
    "health_check_url": null,
    "last_health_check": "2025-06-01 19:00:00",
    "health_status": "HEALTHY"
  }
]
```

## 📌 特記事項

- 認証設定（auth_config）は暗号化必須
- 接続設定・リクエストヘッダーはJSON形式で柔軟な設定に対応
- レート制限により外部システムへの負荷を制御
- ヘルスチェック機能により連携先の状態を監視
- リトライ機能により一時的な障害に対応
- テナント別設定により個別カスタマイズに対応
- 無効化された設定は連携処理から除外される

## 📋 業務ルール

- 同一テナント内で連携キーは重複不可
- 無効化された設定は連携処理から除外される
- 認証情報は暗号化して保存する
- タイムアウト・リトライ設定は正数である必要がある
- レート制限は外部システムの制約に応じて設定
- ヘルスチェックは定期的に実行し状態を更新
- OAuth2認証の場合はトークン更新処理が必要
- SMTP設定の場合は送信テストを実行して確認
