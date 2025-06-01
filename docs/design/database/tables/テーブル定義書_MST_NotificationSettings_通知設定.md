# テーブル定義書: MST_NotificationSettings (通知設定)

## 📋 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_NotificationSettings |
| 論理名 | 通知設定 |
| カテゴリ | マスタ系 |
| 作成日 | 2025-06-01 |

> **注意**: 本テーブル定義書は自動生成されます。手動編集は行わないでください。
> 詳細定義の変更は `table-details/MST_NotificationSettings_details.yaml` で行ってください。


## 📝 改版履歴

> **注意**: 改版履歴の詳細は以下のYAMLファイルで管理されています：
> `table-details/TABLE_NAME_details.yaml`

| バージョン | 更新日 | 更新者 | 主な変更内容 |
|------------|--------|--------|-------------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 通知設定マスタテーブルの詳細定義 |


## 📝 テーブル概要

MST_NotificationSettings（通知設定）は、システム全体の通知機能に関する設定情報を管理するマスタテーブルです。

主な目的：
- 通知チャネル（メール、Slack、Teams等）の設定管理
- 通知タイミング・頻度の制御設定
- 通知対象者・グループの設定管理
- 通知テンプレートとの紐付け設定
- テナント別通知設定の管理

このテーブルは、通知・連携管理機能の基盤となる重要なマスタデータです。


## 🗂️ カラム定義

| カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト | 説明 |
|----------|--------|----------|------|------|----|----|------------|------|
| id | ID | VARCHAR | 50 | × | ● |  |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × |  |  |  | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  |  |  | マルチテナント識別子 |
| id | ID | VARCHAR | 50 | ○ |  |  |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  |  |  | マルチテナント識別子 |
| setting_key | 設定キー | VARCHAR | 100 | ○ |  |  |  | 通知設定の識別キー（例：skill_update_notification、goal_reminder等） |
| setting_name | 設定名 | VARCHAR | 200 | ○ |  |  |  | 通知設定の表示名 |
| notification_type | 通知タイプ | ENUM |  | ○ |  |  |  | 通知の種類（EMAIL:メール、SLACK:Slack、TEAMS:Teams、WEBHOOK:Webhook） |
| target_audience | 対象者 | ENUM |  | ○ |  |  |  | 通知対象（ALL:全員、MANAGER:管理者、EMPLOYEE:一般社員、CUSTOM:カスタム） |
| trigger_event | トリガーイベント | VARCHAR | 100 | ○ |  |  |  | 通知を発生させるイベント（例：skill_registered、goal_deadline_approaching等） |
| frequency_type | 頻度タイプ | ENUM |  | ○ |  |  | IMMEDIATE | 通知頻度（IMMEDIATE:即座、DAILY:日次、WEEKLY:週次、MONTHLY:月次） |
| frequency_value | 頻度値 | INTEGER |  | ○ |  |  |  | 頻度の具体的な値（日次の場合は時間、週次の場合は曜日等） |
| template_id | テンプレートID | VARCHAR | 50 | ○ |  | ● |  | 使用する通知テンプレートのID（MST_NotificationTemplateへの参照） |
| channel_config | チャネル設定 | TEXT |  | ○ |  |  |  | 通知チャネル固有の設定情報（JSON形式） |
| is_enabled | 有効フラグ | BOOLEAN |  | ○ |  |  | True | 通知設定が有効かどうか |
| priority_level | 優先度レベル | ENUM |  | ○ |  |  | MEDIUM | 通知の優先度（HIGH:高、MEDIUM:中、LOW:低） |
| created_at | 作成日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  |  |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  |  |  | レコード更新者のユーザーID |

## 🔍 インデックス定義

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_notification_settings_tenant_key | tenant_id, setting_key | ○ | テナント別設定キー検索用（一意） |
| idx_notification_settings_type | notification_type | × | 通知タイプ別検索用 |
| idx_notification_settings_event | trigger_event | × | トリガーイベント別検索用 |
| idx_notification_settings_enabled | is_enabled | × | 有効設定検索用 |
| idx_notification_settings_template | template_id | × | テンプレート別検索用 |

## 🔒 制約定義

| 制約名 | 制約タイプ | 対象カラム | 条件 | 説明 |
|--------|------------|------------|------|------|
| uk_notification_settings_tenant_key | UNIQUE | tenant_id, setting_key |  | テナント内設定キー一意制約 |
| chk_notification_settings_type | CHECK |  | notification_type IN ('EMAIL', 'SLACK', 'TEAMS', 'WEBHOOK') | 通知タイプ値チェック制約 |
| chk_notification_settings_audience | CHECK |  | target_audience IN ('ALL', 'MANAGER', 'EMPLOYEE', 'CUSTOM') | 対象者値チェック制約 |
| chk_notification_settings_frequency | CHECK |  | frequency_type IN ('IMMEDIATE', 'DAILY', 'WEEKLY', 'MONTHLY') | 頻度タイプ値チェック制約 |
| chk_notification_settings_priority | CHECK |  | priority_level IN ('HIGH', 'MEDIUM', 'LOW') | 優先度レベル値チェック制約 |

## 🔗 外部キー関係

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|------------|--------|--------------|------------|--------|--------|------|
| fk_notification_settings_template | template_id | MST_NotificationTemplate | id | CASCADE | SET NULL | 通知テンプレートへの外部キー |

## 📊 サンプルデータ

```json
[
  {
    "id": "NS001",
    "tenant_id": "TENANT001",
    "setting_key": "skill_update_notification",
    "setting_name": "スキル更新通知",
    "notification_type": "EMAIL",
    "target_audience": "MANAGER",
    "trigger_event": "skill_registered",
    "frequency_type": "IMMEDIATE",
    "frequency_value": null,
    "template_id": "NT001",
    "channel_config": "{\"smtp_server\": \"smtp.company.com\", \"from_address\": \"noreply@company.com\"}",
    "is_enabled": true,
    "priority_level": "MEDIUM"
  },
  {
    "id": "NS002",
    "tenant_id": "TENANT001",
    "setting_key": "goal_deadline_reminder",
    "setting_name": "目標期限リマインダー",
    "notification_type": "SLACK",
    "target_audience": "EMPLOYEE",
    "trigger_event": "goal_deadline_approaching",
    "frequency_type": "DAILY",
    "frequency_value": 9,
    "template_id": "NT002",
    "channel_config": "{\"webhook_url\": \"https://hooks.slack.com/services/xxx\", \"channel\": \"#notifications\"}",
    "is_enabled": true,
    "priority_level": "HIGH"
  }
]
```

## 📌 特記事項

- 通知設定はテナント別に管理され、同一テナント内で設定キーは一意
- channel_configはJSON形式で通知チャネル固有の設定を格納
- frequency_valueは頻度タイプに応じて異なる意味を持つ（時間、曜日等）
- 論理削除は is_enabled フラグで管理
- 通知テンプレートとの連携により柔軟な通知内容設定が可能
- 優先度レベルにより通知の重要度を制御

## 📋 業務ルール

- 同一テナント内で設定キーは重複不可
- 無効化された設定は通知処理から除外される
- テンプレートIDが指定されていない場合はデフォルトテンプレートを使用
- CUSTOM対象者の場合は別途対象者マスタで詳細設定が必要
- 頻度タイプがIMMEDIATEの場合、frequency_valueは不要
- 通知チャネル設定はJSON形式で各チャネルの仕様に準拠
