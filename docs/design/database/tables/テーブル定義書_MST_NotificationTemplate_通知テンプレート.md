# テーブル定義書: MST_NotificationTemplate

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_NotificationTemplate |
| 論理名 | 通知テンプレート |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-04 06:57:02 |

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
| id | ID | VARCHAR | 50 | ○ |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  | マルチテナント識別子 |
| template_key | テンプレートキー | VARCHAR | 100 | ○ |  | テンプレートの識別キー（例：skill_update_email、goal_reminder_slack等） |
| template_name | テンプレート名 | VARCHAR | 200 | ○ |  | テンプレートの表示名 |
| notification_type | 通知タイプ | ENUM |  | ○ |  | 対応する通知の種類（EMAIL:メール、SLACK:Slack、TEAMS:Teams、WEBHOOK:Webhook） |
| language_code | 言語コード | VARCHAR | 10 | ○ | ja | テンプレートの言語（ja:日本語、en:英語等） |
| subject_template | 件名テンプレート | VARCHAR | 500 | ○ |  | 通知の件名テンプレート（メール等で使用） |
| body_template | 本文テンプレート | TEXT |  | ○ |  | 通知の本文テンプレート（プレースホルダー含む） |
| format_type | フォーマットタイプ | ENUM |  | ○ | PLAIN | テンプレートのフォーマット（PLAIN:プレーンテキスト、HTML:HTML、MARKDOWN:Markdown） |
| parameters | パラメータ定義 | TEXT |  | ○ |  | テンプレートで使用可能なパラメータの定義（JSON形式） |
| sample_data | サンプルデータ | TEXT |  | ○ |  | テンプレート確認用のサンプルデータ（JSON形式） |
| is_default | デフォルトフラグ | BOOLEAN |  | ○ | False | 同一キー・タイプでのデフォルトテンプレートかどうか |
| is_active | 有効フラグ | BOOLEAN |  | ○ | True | テンプレートが有効かどうか |
| version | バージョン | VARCHAR | 20 | ○ | 1.0.0 | テンプレートのバージョン番号 |
| code | コード | VARCHAR | 20 | × |  | マスタコード |
| name | 名称 | VARCHAR | 100 | × |  | マスタ名称 |
| description | 説明 | TEXT |  | ○ |  | マスタ説明 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_notification_template_tenant_key_type | tenant_id, template_key, notification_type, language_code | ○ | テナント別テンプレート検索用（一意） |
| idx_notification_template_type | notification_type | × | 通知タイプ別検索用 |
| idx_notification_template_language | language_code | × | 言語別検索用 |
| idx_notification_template_default | is_default, is_active | × | デフォルト・有効テンプレート検索用 |
| idx_notification_template_key | template_key | × | テンプレートキー別検索用 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_notification_template_tenant_key_type_lang | UNIQUE |  | テナント内テンプレート一意制約 |
| chk_notification_template_type | CHECK | notification_type IN ('EMAIL', 'SLACK', 'TEAMS', 'WEBHOOK') | 通知タイプ値チェック制約 |
| chk_notification_template_format | CHECK | format_type IN ('PLAIN', 'HTML', 'MARKDOWN') | フォーマットタイプ値チェック制約 |
| chk_notification_template_language | CHECK | language_code IN ('ja', 'en') | 言語コード値チェック制約 |

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
