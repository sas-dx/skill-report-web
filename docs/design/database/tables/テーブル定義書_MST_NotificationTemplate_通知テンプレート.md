# テーブル定義書: MST_NotificationTemplate

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_NotificationTemplate |
| 論理名 | 通知テンプレート |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-24 23:05:57 |

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
| id | ID | VARCHAR | 50 | ○ |  | ID |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  | テナントID |
| body_template | 本文テンプレート | TEXT |  | ○ |  | 本文テンプレート |
| format_type | フォーマットタイプ | ENUM |  | ○ | PLAIN | フォーマットタイプ |
| is_active | 有効フラグ | BOOLEAN |  | ○ | True | 有効フラグ |
| is_default | デフォルトフラグ | BOOLEAN |  | ○ | False | デフォルトフラグ |
| language_code | 言語コード | VARCHAR | 10 | ○ | ja | 言語コード |
| notification_type | 通知タイプ | ENUM |  | ○ |  | 通知タイプ |
| notificationtemplate_id | MST_NotificationTemplateの主キー | SERIAL |  | × |  | MST_NotificationTemplateの主キー |
| parameters | パラメータ定義 | TEXT |  | ○ |  | パラメータ定義 |
| sample_data | サンプルデータ | TEXT |  | ○ |  | サンプルデータ |
| subject_template | 件名テンプレート | VARCHAR | 500 | ○ |  | 件名テンプレート |
| template_key | テンプレートキー | VARCHAR | 100 | ○ |  | テンプレートキー |
| template_name | テンプレート名 | VARCHAR | 200 | ○ |  | テンプレート名 |
| version | バージョン | VARCHAR | 20 | ○ | 1.0.0 | バージョン |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_notification_template_tenant_key_type | tenant_id, template_key, notification_type, language_code | ○ |  |
| idx_notification_template_type | notification_type | × |  |
| idx_notification_template_language | language_code | × |  |
| idx_notification_template_default | is_default, is_active | × |  |
| idx_notification_template_key | template_key | × |  |
| idx_mst_notificationtemplate_tenant_id | tenant_id | × |  |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| chk_format_type | CHECK | format_type IN (...) | format_type値チェック制約 |
| chk_notification_type | CHECK | notification_type IN (...) | notification_type値チェック制約 |

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
- 同一テナント・キー・タイプ・言語の組み合わせは重複不可
- 無効化されたテンプレートは通知処理から除外される
- デフォルトテンプレートは同一条件で1つのみ設定可能
- プレースホルダーはparametersフィールドで定義されたもののみ使用可能
- subject_templateはメール系通知でのみ使用
- Slack・Teams等ではMarkdown形式の装飾が推奨
- テンプレートバージョンは変更時に更新が必要

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 通知テンプレートマスタテーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214907 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_214959 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215053 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223432 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |