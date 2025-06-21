# テーブル定義書: MST_NotificationTemplate

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_NotificationTemplate |
| 論理名 | 通知テンプレート |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 17:20:33 |

## 概要

MST_NotificationTemplate（通知テンプレート）は、システムで使用する通知メッセージのテンプレートを管理するマスタテーブルです。
主な目的：
- 通知メッセージの定型文管理
- 多言語対応の通知テンプレート管理
- 通知チャネル別のテンプレート管理
- 動的パラメータを含むテンプレート管理
- テナント別カスタマイズ対応
このテーブルは、通知・連携管理機能において一貫性のあるメッセージ配信を実現する重要なマスタデータです。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id |  | VARCHAR |  | ○ |  |  |
| tenant_id |  | VARCHAR |  | ○ |  |  |
| template_key |  | VARCHAR |  | ○ |  |  |
| template_name |  | VARCHAR |  | ○ |  |  |
| notification_type |  | ENUM |  | ○ |  |  |
| language_code |  | VARCHAR |  | ○ | ja |  |
| subject_template |  | VARCHAR |  | ○ |  |  |
| body_template |  | TEXT |  | ○ |  |  |
| format_type |  | ENUM |  | ○ | PLAIN |  |
| parameters |  | TEXT |  | ○ |  |  |
| sample_data |  | TEXT |  | ○ |  |  |
| is_default |  | BOOLEAN |  | ○ | False |  |
| is_active |  | BOOLEAN |  | ○ | True |  |
| version |  | VARCHAR |  | ○ | 1.0.0 |  |
| created_at | レコード作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | レコード更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_notification_template_tenant_key_type | tenant_id, template_key, notification_type, language_code | ○ |  |
| idx_notification_template_type | notification_type | × |  |
| idx_notification_template_language | language_code | × |  |
| idx_notification_template_default | is_default, is_active | × |  |
| idx_notification_template_key | template_key | × |  |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| chk_notification_type | CHECK | notification_type IN (...) | notification_type値チェック制約 |
| chk_format_type | CHECK | format_type IN (...) | format_type値チェック制約 |

## サンプルデータ

| id | tenant_id | template_key | template_name | notification_type | language_code | subject_template | body_template | format_type | parameters | sample_data | is_default | is_active | version |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| NT001 | TENANT001 | skill_update_notification | スキル更新通知テンプレート | EMAIL | ja | 【スキル更新】{{employee_name}}さんのスキル情報が更新されました | {{employee_name}}さん

以下のスキル情報が更新されました。

スキル名: {{skill_name}}
更新日時: {{updated_at}}
更新者: {{updated_by}}

詳細は以下のリンクからご確認ください。
{{skill_detail_url}}

※このメールは自動送信されています。
 | PLAIN | {"employee_name": "社員名", "skill_name": "スキル名", "updated_at": "更新日時", "updated_by": "更新者", "skill_detail_url": "詳細URL"} | {"employee_name": "山田太郎", "skill_name": "Java", "updated_at": "2025-06-01 10:30:00", "updated_by": "佐藤花子", "skill_detail_url": "https://system.company.com/skills/123"} | True | True | 1.0.0 |
| NT002 | TENANT001 | goal_deadline_reminder | 目標期限リマインダーテンプレート | SLACK | ja | None | :warning: *目標期限のお知らせ* :warning:

{{employee_name}}さんの目標「{{goal_title}}」の期限が近づいています。

• 期限: {{deadline_date}}
• 残り日数: {{remaining_days}}日
• 進捗率: {{progress_rate}}%

<{{goal_detail_url}}|詳細を確認する>
 | MARKDOWN | {"employee_name": "社員名", "goal_title": "目標タイトル", "deadline_date": "期限日", "remaining_days": "残り日数", "progress_rate": "進捗率", "goal_detail_url": "詳細URL"} | {"employee_name": "山田太郎", "goal_title": "Java認定資格取得", "deadline_date": "2025-06-30", "remaining_days": "29", "progress_rate": "75", "goal_detail_url": "https://system.company.com/goals/456"} | True | True | 1.0.0 |

## 特記事項

- テンプレートはテナント・キー・タイプ・言語の組み合わせで一意
- body_templateにはプレースホルダー（{{parameter_name}}）を使用可能
- parametersフィールドでテンプレートで使用可能なパラメータを定義
- sample_dataフィールドでテンプレートのプレビュー確認が可能
- is_defaultフラグにより同一条件での優先テンプレートを指定
- 多言語対応により国際化に対応
- format_typeによりプレーンテキスト・HTML・Markdownに対応

## 業務ルール

- 同一テナント・キー・タイプ・言語の組み合わせは重複不可
- 無効化されたテンプレートは通知処理から除外される
- デフォルトテンプレートは同一条件で1つのみ設定可能
- プレースホルダーはparametersフィールドで定義されたもののみ使用可能
- subject_templateはメール系通知でのみ使用
- Slack・Teams等ではMarkdown形式の装飾が推奨
- テンプレートバージョンは変更時に更新が必要

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 通知テンプレートマスタテーブルの詳細定義 |