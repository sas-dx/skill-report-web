# テーブル定義書: MST_ReportTemplate

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_ReportTemplate |
| 論理名 | 帳票テンプレート |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-01 20:40:25 |

## 概要

MST_ReportTemplate（帳票テンプレート）は、システムで生成する各種帳票のテンプレート情報を管理するマスタテーブルです。

主な目的：
- 帳票レイアウト・フォーマットの管理
- 帳票生成パラメータの管理
- 多言語対応の帳票テンプレート管理
- テナント別カスタマイズ対応
- 帳票出力形式の管理

このテーブルは、帳票・レポート機能において一貫性のある帳票出力を実現する重要なマスタデータです。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | ID | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  | マルチテナント識別子 |
| id | ID | VARCHAR | 50 | ○ |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  | マルチテナント識別子 |
| template_key | テンプレートキー | VARCHAR | 100 | ○ |  | テンプレートの識別キー（例：skill_report、goal_summary等） |
| template_name | テンプレート名 | VARCHAR | 200 | ○ |  | テンプレートの表示名 |
| report_category | 帳票カテゴリ | ENUM |  | ○ |  | 帳票の分類（SKILL:スキル関連、GOAL:目標関連、EVALUATION:評価関連、SUMMARY:サマリー、ANALYTICS:分析） |
| output_format | 出力形式 | ENUM |  | ○ |  | 帳票の出力形式（PDF:PDF、EXCEL:Excel、CSV:CSV、HTML:HTML） |
| language_code | 言語コード | VARCHAR | 10 | ○ | ja | テンプレートの言語（ja:日本語、en:英語等） |
| template_content | テンプレート内容 | TEXT |  | ○ |  | 帳票テンプレートの内容（HTML、XML等の形式） |
| style_sheet | スタイルシート | TEXT |  | ○ |  | 帳票のスタイル定義（CSS等） |
| parameters_schema | パラメータスキーマ | TEXT |  | ○ |  | 帳票生成に必要なパラメータの定義（JSON Schema形式） |
| data_source_config | データソース設定 | TEXT |  | ○ |  | データ取得に関する設定（JSON形式） |
| page_settings | ページ設定 | TEXT |  | ○ |  | ページサイズ・余白等の設定（JSON形式） |
| header_template | ヘッダーテンプレート | TEXT |  | ○ |  | 帳票ヘッダー部分のテンプレート |
| footer_template | フッターテンプレート | TEXT |  | ○ |  | 帳票フッター部分のテンプレート |
| is_default | デフォルトフラグ | BOOLEAN |  | ○ | False | 同一キー・カテゴリでのデフォルトテンプレートかどうか |
| is_active | 有効フラグ | BOOLEAN |  | ○ | True | テンプレートが有効かどうか |
| version | バージョン | VARCHAR | 20 | ○ | 1.0.0 | テンプレートのバージョン番号 |
| preview_image_url | プレビュー画像URL | VARCHAR | 500 | ○ |  | テンプレートのプレビュー画像URL |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  | レコード更新者のユーザーID |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_report_template_tenant_key | tenant_id, template_key, language_code | ○ | テナント別テンプレートキー検索用（一意） |
| idx_report_template_category | report_category | × | 帳票カテゴリ別検索用 |
| idx_report_template_format | output_format | × | 出力形式別検索用 |
| idx_report_template_language | language_code | × | 言語別検索用 |
| idx_report_template_default | is_default, is_active | × | デフォルト・有効テンプレート検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_report_template_tenant_key_lang | UNIQUE |  | テナント内テンプレート一意制約 |
| chk_report_template_category | CHECK | report_category IN ('SKILL', 'GOAL', 'EVALUATION', 'SUMMARY', 'ANALYTICS') | 帳票カテゴリ値チェック制約 |
| chk_report_template_format | CHECK | output_format IN ('PDF', 'EXCEL', 'CSV', 'HTML') | 出力形式値チェック制約 |
| chk_report_template_language | CHECK | language_code IN ('ja', 'en') | 言語コード値チェック制約 |

## サンプルデータ

| id | tenant_id | template_key | template_name | report_category | output_format | language_code | template_content | style_sheet | parameters_schema | data_source_config | page_settings | header_template | footer_template | is_default | is_active | version | preview_image_url |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| RT001 | TENANT001 | skill_summary_report | スキルサマリーレポート | SKILL | PDF | ja | <!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{report_title}}</title>
</head>
<body>
    <h1>{{employee_name}}さんのスキルサマリー</h1>
    <div class="summary-section">
        <h2>保有スキル一覧</h2>
        {{#skills}}
        <div class="skill-item">
            <span class="skill-name">{{skill_name}}</span>
            <span class="skill-level">レベル: {{skill_level}}</span>
        </div>
        {{/skills}}
    </div>
</body>
</html>
 | body { font-family: 'Noto Sans JP', sans-serif; }
.skill-item { margin: 10px 0; padding: 5px; border-bottom: 1px solid #ccc; }
.skill-name { font-weight: bold; }
.skill-level { color: #666; }
 | {"type": "object", "properties": {"employee_id": {"type": "string"}, "report_date": {"type": "string", "format": "date"}}} | {"tables": ["MST_Employee", "TRN_EmployeeSkill", "MST_Skill"], "joins": ["employee_skills", "skill_details"]} | {"size": "A4", "orientation": "portrait", "margin": {"top": "20mm", "bottom": "20mm", "left": "15mm", "right": "15mm"}} | <div style="text-align: center; font-size: 12px;">{{company_name}} - スキル管理システム</div> | <div style="text-align: center; font-size: 10px;">出力日時: {{generated_at}} - ページ {{page_number}}</div> | True | True | 1.0.0 | /assets/templates/skill_summary_preview.png |
| RT002 | TENANT001 | goal_progress_report | 目標進捗レポート | GOAL | EXCEL | ja | <workbook>
    <worksheet name="目標進捗">
        <row>
            <cell>社員名</cell>
            <cell>目標タイトル</cell>
            <cell>進捗率</cell>
            <cell>期限</cell>
            <cell>状態</cell>
        </row>
        {{#goals}}
        <row>
            <cell>{{employee_name}}</cell>
            <cell>{{goal_title}}</cell>
            <cell>{{progress_rate}}%</cell>
            <cell>{{deadline}}</cell>
            <cell>{{status}}</cell>
        </row>
        {{/goals}}
    </worksheet>
</workbook>
 | None | {"type": "object", "properties": {"department_id": {"type": "string"}, "period_start": {"type": "string", "format": "date"}, "period_end": {"type": "string", "format": "date"}}} | {"tables": ["MST_Employee", "TRN_Goal"], "joins": ["employee_goals"]} | {"orientation": "landscape"} | None | None | True | True | 1.0.0 | /assets/templates/goal_progress_preview.png |

## 特記事項

- テンプレートはテナント・キー・言語の組み合わせで一意
- template_contentにはMustache等のテンプレートエンジン記法を使用
- parameters_schemaでテンプレートで使用可能なパラメータを定義
- data_source_configで必要なデータの取得方法を定義
- 多言語対応により国際化に対応
- 出力形式により異なるテンプレート記法に対応
- プレビュー画像によりテンプレート選択時の視認性を向上

## 業務ルール

- 同一テナント・キー・言語の組み合わせは重複不可
- 無効化されたテンプレートは帳票生成から除外される
- デフォルトテンプレートは同一条件で1つのみ設定可能
- パラメータはparameters_schemaで定義されたもののみ使用可能
- データソース設定は実際のテーブル構造と整合性が必要
- 出力形式に応じたテンプレート記法を使用
- テンプレートバージョンは変更時に更新が必要
- プレビュー画像は管理画面での選択性向上のため推奨

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 帳票テンプレートマスタテーブルの詳細定義 |
