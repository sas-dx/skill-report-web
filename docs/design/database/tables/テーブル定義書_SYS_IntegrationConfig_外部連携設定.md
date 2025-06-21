# テーブル定義書: SYS_IntegrationConfig

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | SYS_IntegrationConfig |
| 論理名 | 外部連携設定 |
| カテゴリ | システム系 |
| 生成日時 | 2025-06-21 17:20:35 |

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
| id |  | VARCHAR |  | ○ |  |  |
| tenant_id |  | VARCHAR |  | ○ |  |  |
| integration_key |  | VARCHAR |  | ○ |  |  |
| integration_name |  | VARCHAR |  | ○ |  |  |
| integration_type |  | ENUM |  | ○ |  |  |
| endpoint_url |  | VARCHAR |  | ○ |  |  |
| auth_type |  | ENUM |  | ○ |  |  |
| auth_config |  | TEXT |  | ○ |  |  |
| connection_config |  | TEXT |  | ○ |  |  |
| request_headers |  | TEXT |  | ○ |  |  |
| timeout_seconds |  | INTEGER |  | ○ | 30 |  |
| retry_count |  | INTEGER |  | ○ | 3 |  |
| retry_interval |  | INTEGER |  | ○ | 5 |  |
| rate_limit_per_minute |  | INTEGER |  | ○ |  |  |
| is_enabled |  | BOOLEAN |  | ○ | True |  |
| health_check_url |  | VARCHAR |  | ○ |  |  |
| last_health_check |  | TIMESTAMP |  | ○ |  |  |
| health_status |  | ENUM |  | ○ |  |  |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |

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
| chk_integration_type | CHECK | integration_type IN (...) | integration_type値チェック制約 |
| chk_auth_type | CHECK | auth_type IN (...) | auth_type値チェック制約 |
| chk_health_status | CHECK | health_status IN (...) | health_status値チェック制約 |

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