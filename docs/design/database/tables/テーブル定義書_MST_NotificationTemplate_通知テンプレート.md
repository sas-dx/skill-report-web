# テーブル定義書: MST_NotificationTemplate (通知テンプレート)

## 📋 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_NotificationTemplate |
| 論理名 | 通知テンプレート |
| カテゴリ | マスタ系 |
| 作成日 | 2025-06-01 |

> **注意**: 本テーブル定義書は自動生成されます。手動編集は行わないでください。
> 詳細定義の変更は `table-details/MST_NotificationTemplate_details.yaml` で行ってください。


## 📝 改版履歴

> **注意**: 改版履歴の詳細は以下のYAMLファイルで管理されています：
> `table-details/TABLE_NAME_details.yaml`

| バージョン | 更新日 | 更新者 | 主な変更内容 |
|------------|--------|--------|-------------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 通知テンプレートマスタテーブルの詳細定義 |


## 📝 テーブル概要

MST_NotificationTemplate（通知テンプレート）は、システムで使用する通知メッセージのテンプレートを管理するマスタテーブルです。

主な目的：
- 通知メッセージの定型文管理
- 多言語対応の通知テンプレート管理
- 通知チャネル別のテンプレート管理
- 動的パラメータを含むテンプレート管理
- テナント別カスタマイズ対応

このテーブルは、通知・連携管理機能において一貫性のあるメッセージ配信を実現する重要なマスタデータです。


## 🗂️ カラム定義

| カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト | 説明 |
|----------|--------|----------|------|------|----|----|------------|------|
| id | ID | VARCHAR | 50 | × | ● |  |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × |  |  |  | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  |  |  | マルチテナント識別子 |
| id | ID | VARCHAR | 50 | ○ |  |  |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  |  |  | マルチテナント識別子 |
| template_key | テンプレートキー | VARCHAR | 100 | ○ |  |  |  | テンプレートの識別キー（例：skill_update_email、goal_reminder_slack等） |
| template_name | テンプレート名 | VARCHAR | 200 | ○ |  |  |  | テンプレートの表示名 |
| notification_type | 通知タイプ | ENUM |  | ○ |  |  |  | 対応する通知の種類（EMAIL:メール、SLACK:Slack、TEAMS:Teams、WEBHOOK:Webhook） |
| language_code | 言語コード | VARCHAR | 10 | ○ |  |  | ja | テンプレートの言語（ja:日本語、en:英語等） |
| subject_template | 件名テンプレート | VARCHAR | 500 | ○ |  |  |  | 通知の件名テンプレート（メール等で使用） |
| body_template | 本文テンプレート | TEXT |  | ○ |  |  |  | 通知の本文テンプレート（プレースホルダー含む） |
| format_type | フォーマットタイプ | ENUM |  | ○ |  |  | PLAIN | テンプレートのフォーマット（PLAIN:プレーンテキスト、HTML:HTML、MARKDOWN:Markdown） |
| parameters | パラメータ定義 | TEXT |  | ○ |  |  |  | テンプレートで使用可能なパラメータの定義（JSON形式） |
| sample_data | サンプルデータ | TEXT |  | ○ |  |  |  | テンプレート確認用のサンプルデータ（JSON形式） |
| is_default | デフォルトフラグ | BOOLEAN |  | ○ |  |  |  | 同一キー・タイプでのデフォルトテンプレートかどうか |
| is_active | 有効フラグ | BOOLEAN |  | ○ |  |  | True | テンプレートが有効かどうか |
| version | バージョン | VARCHAR | 20 | ○ |  |  | 1.0.0 | テンプレートのバージョン番号 |
| created_at | 作成日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  |  |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  |  |  | レコード更新者のユーザーID |

## 🔍 インデックス定義

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_notification_template_tenant_key_type | tenant_id, template_key, notification_type, language_code | ○ | テナント別テンプレート検索用（一意） |
| idx_notification_template_type | notification_type | × | 通知タイプ別検索用 |
| idx_notification_template_language | language_code | × | 言語別検索用 |
| idx_notification_template_default | is_default, is_active | × | デフォルト・有効テンプレート検索用 |
| idx_notification_template_key | template_key | × | テンプレートキー別検索用 |

## 🔒 制約定義

| 制約名 | 制約タイプ | 対象カラム | 条件 | 説明 |
|--------|------------|------------|------|------|
| uk_notification_template_tenant_key_type_lang | UNIQUE | tenant_id, template_key, notification_type, language_code |  | テナント内テンプレート一意制約 |
| chk_notification_template_type | CHECK |  | notification_type IN ('EMAIL', 'SLACK', 'TEAMS', 'WEBHOOK') | 通知タイプ値チェック制約 |
| chk_notification_template_format | CHECK |  | format_type IN ('PLAIN', 'HTML', 'MARKDOWN') | フォーマットタイプ値チェック制約 |
| chk_notification_template_language | CHECK |  | language_code IN ('ja', 'en') | 言語コード値チェック制約 |

## 🔗 外部キー関係

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|------------|--------|--------------|------------|--------|--------|------|

## 📊 サンプルデータ

```json
[
  {
    "id": "NT001",
    "tenant_id": "TENANT001",
    "template_key": "skill_update_notification",
    "template_name": "スキル更新通知テンプレート",
    "notification_type": "EMAIL",
    "language_code": "ja",
    "subject_template": "【スキル更新】{{employee_name}}さんのスキル情報が更新されました",
    "body_template": "{{employee_name}}さん\n\n以下のスキル情報が更新されました。\n\nスキル名: {{skill_name}}\n更新日時: {{updated_at}}\n更新者: {{updated_by}}\n\n詳細は以下のリンクからご確認ください。\n{{skill_detail_url}}\n\n※このメールは自動送信されています。\n",
    "format_type": "PLAIN",
    "parameters": "{\"employee_name\": \"社員名\", \"skill_name\": \"スキル名\", \"updated_at\": \"更新日時\", \"updated_by\": \"更新者\", \"skill_detail_url\": \"詳細URL\"}",
    "sample_data": "{\"employee_name\": \"山田太郎\", \"skill_name\": \"Java\", \"updated_at\": \"2025-06-01 10:30:00\", \"updated_by\": \"佐藤花子\", \"skill_detail_url\": \"https://system.company.com/skills/123\"}",
    "is_default": true,
    "is_active": true,
    "version": "1.0.0"
  },
  {
    "id": "NT002",
    "tenant_id": "TENANT001",
    "template_key": "goal_deadline_reminder",
    "template_name": "目標期限リマインダーテンプレート",
    "notification_type": "SLACK",
    "language_code": "ja",
    "subject_template": null,
    "body_template": ":warning: *目標期限のお知らせ* :warning:\n\n{{employee_name}}さんの目標「{{goal_title}}」の期限が近づいています。\n\n• 期限: {{deadline_date}}\n• 残り日数: {{remaining_days}}日\n• 進捗率: {{progress_rate}}%\n\n<{{goal_detail_url}}|詳細を確認する>\n",
    "format_type": "MARKDOWN",
    "parameters": "{\"employee_name\": \"社員名\", \"goal_title\": \"目標タイトル\", \"deadline_date\": \"期限日\", \"remaining_days\": \"残り日数\", \"progress_rate\": \"進捗率\", \"goal_detail_url\": \"詳細URL\"}",
    "sample_data": "{\"employee_name\": \"山田太郎\", \"goal_title\": \"Java認定資格取得\", \"deadline_date\": \"2025-06-30\", \"remaining_days\": \"29\", \"progress_rate\": \"75\", \"goal_detail_url\": \"https://system.company.com/goals/456\"}",
    "is_default": true,
    "is_active": true,
    "version": "1.0.0"
  }
]
```

## 📌 特記事項

- テンプレートはテナント・キー・タイプ・言語の組み合わせで一意
- body_templateにはプレースホルダー（{{parameter_name}}）を使用可能
- parametersフィールドでテンプレートで使用可能なパラメータを定義
- sample_dataフィールドでテンプレートのプレビュー確認が可能
- is_defaultフラグにより同一条件での優先テンプレートを指定
- 多言語対応により国際化に対応
- format_typeによりプレーンテキスト・HTML・Markdownに対応

## 📋 業務ルール

- 同一テナント・キー・タイプ・言語の組み合わせは重複不可
- 無効化されたテンプレートは通知処理から除外される
- デフォルトテンプレートは同一条件で1つのみ設定可能
- プレースホルダーはparametersフィールドで定義されたもののみ使用可能
- subject_templateはメール系通知でのみ使用
- Slack・Teams等ではMarkdown形式の装飾が推奨
- テンプレートバージョンは変更時に更新が必要
