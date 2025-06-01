# テーブル定義書: HIS_NotificationLog (通知送信履歴)

## 📋 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | HIS_NotificationLog |
| 論理名 | 通知送信履歴 |
| カテゴリ | 履歴系 |
| 作成日 | 2025-06-01 |

> **注意**: 本テーブル定義書は自動生成されます。手動編集は行わないでください。
> 詳細定義の変更は `table-details/HIS_NotificationLog_details.yaml` で行ってください。


## 📝 改版履歴

> **注意**: 改版履歴の詳細は以下のYAMLファイルで管理されています：
> `table-details/TABLE_NAME_details.yaml`

| バージョン | 更新日 | 更新者 | 主な変更内容 |
|------------|--------|--------|-------------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 通知送信履歴テーブルの詳細定義 |


## 📝 テーブル概要

HIS_NotificationLog（通知送信履歴）は、システムから送信された全ての通知の履歴を管理するテーブルです。

主な目的：
- 通知送信の履歴管理
- 送信成功・失敗の記録
- 通知配信の監査証跡
- 通知システムの分析・改善データ
- 再送処理のための情報管理

このテーブルは、通知・連携管理機能において送信状況の把握と品質向上を支える重要な履歴データです。


## 🗂️ カラム定義

| カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト | 説明 |
|----------|--------|----------|------|------|----|----|------------|------|
| id | ID | VARCHAR | 50 | × | ● |  |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × |  |  |  | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  |  |  | マルチテナント識別子 |
| id | ID | VARCHAR | 50 | ○ |  |  |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  |  |  | マルチテナント識別子 |
| notification_id | 通知ID | VARCHAR | 50 | ○ |  | ● |  | 送信された通知のID（TRN_Notificationへの参照） |
| setting_id | 設定ID | VARCHAR | 50 | ○ |  | ● |  | 使用された通知設定のID（MST_NotificationSettingsへの参照） |
| template_id | テンプレートID | VARCHAR | 50 | ○ |  | ● |  | 使用された通知テンプレートのID（MST_NotificationTemplateへの参照） |
| notification_type | 通知タイプ | ENUM |  | ○ |  |  |  | 送信された通知の種類（EMAIL:メール、SLACK:Slack、TEAMS:Teams、WEBHOOK:Webhook） |
| recipient_type | 受信者タイプ | ENUM |  | ○ |  |  |  | 受信者の種類（USER:個人、GROUP:グループ、CHANNEL:チャネル、WEBHOOK:Webhook） |
| recipient_address | 受信者アドレス | VARCHAR | 500 | ○ |  |  |  | 送信先アドレス（メールアドレス、Slack チャネル等、暗号化必須） |
| subject | 件名 | VARCHAR | 500 | ○ |  |  |  | 送信された通知の件名 |
| message_body | メッセージ本文 | TEXT |  | ○ |  |  |  | 送信された通知の本文 |
| message_format | メッセージフォーマット | ENUM |  | ○ |  |  |  | メッセージのフォーマット（PLAIN:プレーンテキスト、HTML:HTML、MARKDOWN:Markdown） |
| send_status | 送信状態 | ENUM |  | ○ |  |  |  | 送信の状態（PENDING:送信待ち、SENDING:送信中、SUCCESS:成功、FAILED:失敗、RETRY:リトライ中） |
| send_attempts | 送信試行回数 | INTEGER |  | ○ |  |  |  | 送信を試行した回数 |
| max_retry_count | 最大リトライ回数 | INTEGER |  | ○ |  |  | 3 | 設定された最大リトライ回数 |
| scheduled_at | 送信予定日時 | TIMESTAMP |  | ○ |  |  |  | 送信が予定された日時 |
| sent_at | 送信日時 | TIMESTAMP |  | ○ |  |  |  | 実際に送信された日時 |
| delivered_at | 配信確認日時 | TIMESTAMP |  | ○ |  |  |  | 配信が確認された日時（対応している場合） |
| opened_at | 開封日時 | TIMESTAMP |  | ○ |  |  |  | 開封が確認された日時（メール等で対応している場合） |
| response_code | レスポンスコード | VARCHAR | 20 | ○ |  |  |  | 送信先システムからのレスポンスコード |
| response_message | レスポンスメッセージ | TEXT |  | ○ |  |  |  | 送信先システムからのレスポンスメッセージ |
| error_details | エラー詳細 | TEXT |  | ○ |  |  |  | 送信失敗時のエラー詳細情報（JSON形式） |
| integration_config_id | 連携設定ID | VARCHAR | 50 | ○ |  | ● |  | 使用された外部連携設定のID（SYS_IntegrationConfigへの参照） |
| priority_level | 優先度レベル | ENUM |  | ○ |  |  | MEDIUM | 通知の優先度（HIGH:高、MEDIUM:中、LOW:低） |
| created_at | 作成日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  |  |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  |  |  | レコード更新者のユーザーID |

## 🔍 インデックス定義

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_notification_log_notification | notification_id | × | 通知ID別検索用 |
| idx_notification_log_tenant_status | tenant_id, send_status | × | テナント別送信状態検索用 |
| idx_notification_log_type | notification_type | × | 通知タイプ別検索用 |
| idx_notification_log_scheduled | scheduled_at | × | 送信予定日時検索用 |
| idx_notification_log_sent | sent_at | × | 送信日時検索用 |
| idx_notification_log_status_attempts | send_status, send_attempts | × | 送信状態・試行回数検索用 |
| idx_notification_log_priority | priority_level, scheduled_at | × | 優先度別送信予定検索用 |

## 🔒 制約定義

| 制約名 | 制約タイプ | 対象カラム | 条件 | 説明 |
|--------|------------|------------|------|------|
| chk_notification_log_type | CHECK |  | notification_type IN ('EMAIL', 'SLACK', 'TEAMS', 'WEBHOOK') | 通知タイプ値チェック制約 |
| chk_notification_log_recipient_type | CHECK |  | recipient_type IN ('USER', 'GROUP', 'CHANNEL', 'WEBHOOK') | 受信者タイプ値チェック制約 |
| chk_notification_log_format | CHECK |  | message_format IN ('PLAIN', 'HTML', 'MARKDOWN') | メッセージフォーマット値チェック制約 |
| chk_notification_log_status | CHECK |  | send_status IN ('PENDING', 'SENDING', 'SUCCESS', 'FAILED', 'RETRY') | 送信状態値チェック制約 |
| chk_notification_log_priority | CHECK |  | priority_level IN ('HIGH', 'MEDIUM', 'LOW') | 優先度レベル値チェック制約 |
| chk_notification_log_attempts_positive | CHECK |  | send_attempts >= 0 AND max_retry_count >= 0 | 試行回数正数チェック制約 |
| chk_notification_log_attempts_limit | CHECK |  | send_attempts <= max_retry_count + 1 | 試行回数上限チェック制約 |

## 🔗 外部キー関係

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|------------|--------|--------------|------------|--------|--------|------|
| fk_notification_log_notification | notification_id | TRN_Notification | id | CASCADE | CASCADE | 通知履歴への外部キー |
| fk_notification_log_setting | setting_id | MST_NotificationSettings | id | CASCADE | SET NULL | 通知設定への外部キー |
| fk_notification_log_template | template_id | MST_NotificationTemplate | id | CASCADE | SET NULL | 通知テンプレートへの外部キー |
| fk_notification_log_integration | integration_config_id | SYS_IntegrationConfig | id | CASCADE | SET NULL | 外部連携設定への外部キー |

## 📊 サンプルデータ

```json
[
  {
    "id": "NL001",
    "tenant_id": "TENANT001",
    "notification_id": "NOTIF001",
    "setting_id": "NS001",
    "template_id": "NT001",
    "notification_type": "EMAIL",
    "recipient_type": "USER",
    "recipient_address": "yamada.taro@company.com",
    "subject": "【スキル更新】山田太郎さんのスキル情報が更新されました",
    "message_body": "山田太郎さん\n\n以下のスキル情報が更新されました。\n\nスキル名: Java\n更新日時: 2025-06-01 10:30:00\n更新者: 佐藤花子\n\n詳細は以下のリンクからご確認ください。\nhttps://system.company.com/skills/123\n\n※このメールは自動送信されています。",
    "message_format": "PLAIN",
    "send_status": "SUCCESS",
    "send_attempts": 1,
    "max_retry_count": 3,
    "scheduled_at": "2025-06-01 10:30:00",
    "sent_at": "2025-06-01 10:30:15",
    "delivered_at": "2025-06-01 10:30:45",
    "opened_at": "2025-06-01 11:15:30",
    "response_code": "250",
    "response_message": "Message accepted for delivery",
    "error_details": null,
    "integration_config_id": "IC003",
    "priority_level": "MEDIUM"
  },
  {
    "id": "NL002",
    "tenant_id": "TENANT001",
    "notification_id": "NOTIF002",
    "setting_id": "NS002",
    "template_id": "NT002",
    "notification_type": "SLACK",
    "recipient_type": "CHANNEL",
    "recipient_address": "#notifications",
    "subject": null,
    "message_body": ":warning: *目標期限のお知らせ* :warning:\n\n山田太郎さんの目標「Java認定資格取得」の期限が近づいています。\n\n• 期限: 2025-06-30\n• 残り日数: 29日\n• 進捗率: 75%\n\n<https://system.company.com/goals/456|詳細を確認する>",
    "message_format": "MARKDOWN",
    "send_status": "FAILED",
    "send_attempts": 3,
    "max_retry_count": 3,
    "scheduled_at": "2025-06-01 09:00:00",
    "sent_at": null,
    "delivered_at": null,
    "opened_at": null,
    "response_code": "404",
    "response_message": "channel_not_found",
    "error_details": "{\"error\": \"channel_not_found\", \"details\": \"The specified channel does not exist or the bot is not a member\"}",
    "integration_config_id": "IC001",
    "priority_level": "HIGH"
  }
]
```

## 📌 特記事項

- 通知送信履歴は2年間保持される
- 受信者アドレスは個人情報のため暗号化必須
- エラー詳細はJSON形式で構造化された情報を格納
- 配信確認・開封確認は対応している通知チャネルでのみ記録
- リトライ処理は最大試行回数まで自動実行
- 送信状態により後続処理を制御
- 優先度により送信順序を制御

## 📋 業務ルール

- 送信試行回数は最大リトライ回数+1を超えない
- 成功した通知は再送不可
- 失敗した通知は設定された回数までリトライ
- 高優先度の通知は優先的に送信処理
- 送信予定日時を過ぎた通知は期限切れとして処理
- 受信者アドレスは送信時に暗号化して保存
- エラー詳細は障害分析のため詳細に記録
- 配信確認機能は通知チャネルの対応状況に依存
