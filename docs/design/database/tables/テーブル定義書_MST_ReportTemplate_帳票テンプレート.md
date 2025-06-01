# テーブル定義書: MST_ReportTemplate (帳票テンプレート)

## 📋 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_ReportTemplate |
| 論理名 | 帳票テンプレート |
| カテゴリ | マスタ系 |
| 作成日 | 2025-06-01 |

> **注意**: 本テーブル定義書は自動生成されます。手動編集は行わないでください。
> 詳細定義の変更は `table-details/MST_ReportTemplate_details.yaml` で行ってください。


## 📝 改版履歴

> **注意**: 改版履歴の詳細は以下のYAMLファイルで管理されています：
> `table-details/TABLE_NAME_details.yaml`

| バージョン | 更新日 | 更新者 | 主な変更内容 |
|------------|--------|--------|-------------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 帳票テンプレートマスタテーブルの詳細定義 |


## 📝 テーブル概要

MST_ReportTemplate（帳票テンプレート）は、システムで生成する各種帳票のテンプレート情報を管理するマスタテーブルです。

主な目的：
- 帳票レイアウト・フォーマットの管理
- 帳票生成パラメータの管理
- 多言語対応の帳票テンプレート管理
- テナント別カスタマイズ対応
- 帳票出力形式の管理

このテーブルは、帳票・レポート機能において一貫性のある帳票出力を実現する重要なマスタデータです。


## 🗂️ カラム定義

| カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト | 説明 |
|----------|--------|----------|------|------|----|----|------------|------|
| id | ID | VARCHAR | 50 | × | ● |  |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × |  |  |  | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  |  |  | マルチテナント識別子 |
| id | ID | VARCHAR | 50 | ○ |  |  |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  |  |  | マルチテナント識別子 |
| template_key | テンプレートキー | VARCHAR | 100 | ○ |  |  |  | テンプレートの識別キー（例：skill_report、goal_summary等） |
| template_name | テンプレート名 | VARCHAR | 200 | ○ |  |  |  | テンプレートの表示名 |
| report_category | 帳票カテゴリ | ENUM |  | ○ |  |  |  | 帳票の分類（SKILL:スキル関連、GOAL:目標関連、EVALUATION:評価関連、SUMMARY:サマリー、ANALYTICS:分析） |
| output_format | 出力形式 | ENUM |  | ○ |  |  |  | 帳票の出力形式（PDF:PDF、EXCEL:Excel、CSV:CSV、HTML:HTML） |
| language_code | 言語コード | VARCHAR | 10 | ○ |  |  | ja | テンプレートの言語（ja:日本語、en:英語等） |
| template_content | テンプレート内容 | TEXT |  | ○ |  |  |  | 帳票テンプレートの内容（HTML、XML等の形式） |
| style_sheet | スタイルシート | TEXT |  | ○ |  |  |  | 帳票のスタイル定義（CSS等） |
| parameters_schema | パラメータスキーマ | TEXT |  | ○ |  |  |  | 帳票生成に必要なパラメータの定義（JSON Schema形式） |
| data_source_config | データソース設定 | TEXT |  | ○ |  |  |  | データ取得に関する設定（JSON形式） |
| page_settings | ページ設定 | TEXT |  | ○ |  |  |  | ページサイズ・余白等の設定（JSON形式） |
| header_template | ヘッダーテンプレート | TEXT |  | ○ |  |  |  | 帳票ヘッダー部分のテンプレート |
| footer_template | フッターテンプレート | TEXT |  | ○ |  |  |  | 帳票フッター部分のテンプレート |
| is_default | デフォルトフラグ | BOOLEAN |  | ○ |  |  |  | 同一キー・カテゴリでのデフォルトテンプレートかどうか |
| is_active | 有効フラグ | BOOLEAN |  | ○ |  |  | True | テンプレートが有効かどうか |
| version | バージョン | VARCHAR | 20 | ○ |  |  | 1.0.0 | テンプレートのバージョン番号 |
| preview_image_url | プレビュー画像URL | VARCHAR | 500 | ○ |  |  |  | テンプレートのプレビュー画像URL |
| created_at | 作成日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  |  |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  |  |  | レコード更新者のユーザーID |

## 🔍 インデックス定義

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_report_template_tenant_key | tenant_id, template_key, language_code | ○ | テナント別テンプレートキー検索用（一意） |
| idx_report_template_category | report_category | × | 帳票カテゴリ別検索用 |
| idx_report_template_format | output_format | × | 出力形式別検索用 |
| idx_report_template_language | language_code | × | 言語別検索用 |
| idx_report_template_default | is_default, is_active | × | デフォルト・有効テンプレート検索用 |

## 🔒 制約定義

| 制約名 | 制約タイプ | 対象カラム | 条件 | 説明 |
|--------|------------|------------|------|------|
| uk_report_template_tenant_key_lang | UNIQUE | tenant_id, template_key, language_code |  | テナント内テンプレート一意制約 |
| chk_report_template_category | CHECK |  | report_category IN ('SKILL', 'GOAL', 'EVALUATION', 'SUMMARY', 'ANALYTICS') | 帳票カテゴリ値チェック制約 |
| chk_report_template_format | CHECK |  | output_format IN ('PDF', 'EXCEL', 'CSV', 'HTML') | 出力形式値チェック制約 |
| chk_report_template_language | CHECK |  | language_code IN ('ja', 'en') | 言語コード値チェック制約 |

## 🔗 外部キー関係

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|------------|--------|--------------|------------|--------|--------|------|

## 📊 サンプルデータ

```json
[
  {
    "id": "RT001",
    "tenant_id": "TENANT001",
    "template_key": "skill_summary_report",
    "template_name": "スキルサマリーレポート",
    "report_category": "SKILL",
    "output_format": "PDF",
    "language_code": "ja",
    "template_content": "<!DOCTYPE html>\n<html>\n<head>\n    <meta charset=\"UTF-8\">\n    <title>{{report_title}}</title>\n</head>\n<body>\n    <h1>{{employee_name}}さんのスキルサマリー</h1>\n    <div class=\"summary-section\">\n        <h2>保有スキル一覧</h2>\n        {{#skills}}\n        <div class=\"skill-item\">\n            <span class=\"skill-name\">{{skill_name}}</span>\n            <span class=\"skill-level\">レベル: {{skill_level}}</span>\n        </div>\n        {{/skills}}\n    </div>\n</body>\n</html>\n",
    "style_sheet": "body { font-family: 'Noto Sans JP', sans-serif; }\n.skill-item { margin: 10px 0; padding: 5px; border-bottom: 1px solid #ccc; }\n.skill-name { font-weight: bold; }\n.skill-level { color: #666; }\n",
    "parameters_schema": "{\"type\": \"object\", \"properties\": {\"employee_id\": {\"type\": \"string\"}, \"report_date\": {\"type\": \"string\", \"format\": \"date\"}}}",
    "data_source_config": "{\"tables\": [\"MST_Employee\", \"TRN_EmployeeSkill\", \"MST_Skill\"], \"joins\": [\"employee_skills\", \"skill_details\"]}",
    "page_settings": "{\"size\": \"A4\", \"orientation\": \"portrait\", \"margin\": {\"top\": \"20mm\", \"bottom\": \"20mm\", \"left\": \"15mm\", \"right\": \"15mm\"}}",
    "header_template": "<div style=\"text-align: center; font-size: 12px;\">{{company_name}} - スキル管理システム</div>",
    "footer_template": "<div style=\"text-align: center; font-size: 10px;\">出力日時: {{generated_at}} - ページ {{page_number}}</div>",
    "is_default": true,
    "is_active": true,
    "version": "1.0.0",
    "preview_image_url": "/assets/templates/skill_summary_preview.png"
  },
  {
    "id": "RT002",
    "tenant_id": "TENANT001",
    "template_key": "goal_progress_report",
    "template_name": "目標進捗レポート",
    "report_category": "GOAL",
    "output_format": "EXCEL",
    "language_code": "ja",
    "template_content": "<workbook>\n    <worksheet name=\"目標進捗\">\n        <row>\n            <cell>社員名</cell>\n            <cell>目標タイトル</cell>\n            <cell>進捗率</cell>\n            <cell>期限</cell>\n            <cell>状態</cell>\n        </row>\n        {{#goals}}\n        <row>\n            <cell>{{employee_name}}</cell>\n            <cell>{{goal_title}}</cell>\n            <cell>{{progress_rate}}%</cell>\n            <cell>{{deadline}}</cell>\n            <cell>{{status}}</cell>\n        </row>\n        {{/goals}}\n    </worksheet>\n</workbook>\n",
    "style_sheet": null,
    "parameters_schema": "{\"type\": \"object\", \"properties\": {\"department_id\": {\"type\": \"string\"}, \"period_start\": {\"type\": \"string\", \"format\": \"date\"}, \"period_end\": {\"type\": \"string\", \"format\": \"date\"}}}",
    "data_source_config": "{\"tables\": [\"MST_Employee\", \"TRN_Goal\"], \"joins\": [\"employee_goals\"]}",
    "page_settings": "{\"orientation\": \"landscape\"}",
    "header_template": null,
    "footer_template": null,
    "is_default": true,
    "is_active": true,
    "version": "1.0.0",
    "preview_image_url": "/assets/templates/goal_progress_preview.png"
  }
]
```

## 📌 特記事項

- テンプレートはテナント・キー・言語の組み合わせで一意
- template_contentにはMustache等のテンプレートエンジン記法を使用
- parameters_schemaでテンプレートで使用可能なパラメータを定義
- data_source_configで必要なデータの取得方法を定義
- 多言語対応により国際化に対応
- 出力形式により異なるテンプレート記法に対応
- プレビュー画像によりテンプレート選択時の視認性を向上

## 📋 業務ルール

- 同一テナント・キー・言語の組み合わせは重複不可
- 無効化されたテンプレートは帳票生成から除外される
- デフォルトテンプレートは同一条件で1つのみ設定可能
- パラメータはparameters_schemaで定義されたもののみ使用可能
- データソース設定は実際のテーブル構造と整合性が必要
- 出力形式に応じたテンプレート記法を使用
- テンプレートバージョンは変更時に更新が必要
- プレビュー画像は管理画面での選択性向上のため推奨
