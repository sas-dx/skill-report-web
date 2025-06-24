# テーブル定義書: HIS_ReportGeneration

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | HIS_ReportGeneration |
| 論理名 | 帳票生成履歴 |
| カテゴリ | 履歴系 |
| 生成日時 | 2025-06-24 23:02:18 |

## 概要

HIS_ReportGeneration（帳票生成履歴）は、システムで生成された帳票・レポートの履歴を管理するテーブルです。
主な目的：
- 帳票生成の履歴管理
- 生成成功・失敗の記録
- 帳票ファイルの管理
- 生成パフォーマンスの監視
- 帳票利用状況の分析
このテーブルは、帳票・レポート機能において生成状況の把握と品質向上を支える重要な履歴データです。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | ID | VARCHAR | 50 | ○ |  | ID |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  | テナントID |
| completed_at | 完了日時 | TIMESTAMP |  | ○ |  | 完了日時 |
| download_count | ダウンロード回数 | INTEGER |  | ○ | 0 | ダウンロード回数 |
| error_details | エラー詳細 | TEXT |  | ○ |  | エラー詳細 |
| error_message | エラーメッセージ | TEXT |  | ○ |  | エラーメッセージ |
| expires_at | 有効期限 | TIMESTAMP |  | ○ |  | 有効期限 |
| file_path | ファイルパス | VARCHAR | 500 | ○ |  | ファイルパス |
| file_size | ファイルサイズ | BIGINT |  | ○ |  | ファイルサイズ |
| generation_status | 生成状態 | ENUM |  | ○ |  | 生成状態 |
| last_downloaded_at | 最終ダウンロード日時 | TIMESTAMP |  | ○ |  | 最終ダウンロード日時 |
| output_format | 出力形式 | ENUM |  | ○ |  | 出力形式 |
| parameters | パラメータ | TEXT |  | ○ |  | パラメータ |
| processing_time_ms | 処理時間 | INTEGER |  | ○ |  | 処理時間 |
| report_category | 帳票カテゴリ | ENUM |  | ○ |  | 帳票カテゴリ |
| report_title | 帳票タイトル | VARCHAR | 200 | ○ |  | 帳票タイトル |
| reportgeneration_id | HIS_ReportGenerationの主キー | SERIAL |  | × |  | HIS_ReportGenerationの主キー |
| requested_at | 要求日時 | TIMESTAMP |  | ○ |  | 要求日時 |
| requested_by | 要求者 | VARCHAR | 50 | ○ |  | 要求者 |
| started_at | 開始日時 | TIMESTAMP |  | ○ |  | 開始日時 |
| template_id | テンプレートID | VARCHAR | 50 | ○ |  | テンプレートID |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_report_generation_template | template_id | × |  |
| idx_report_generation_requester | requested_by | × |  |
| idx_report_generation_tenant_status | tenant_id, generation_status | × |  |
| idx_report_generation_category | report_category | × |  |
| idx_report_generation_format | output_format | × |  |
| idx_report_generation_requested | requested_at | × |  |
| idx_report_generation_completed | completed_at | × |  |
| idx_report_generation_expires | expires_at | × |  |
| idx_his_reportgeneration_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_report_generation_template | template_id | MST_ReportTemplate | id | CASCADE | RESTRICT | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| chk_generation_status | CHECK | generation_status IN (...) | generation_status値チェック制約 |

## サンプルデータ

| id | tenant_id | template_id | requested_by | report_title | report_category | output_format | generation_status | parameters | file_path | file_size | download_count | last_downloaded_at | requested_at | started_at | completed_at | processing_time_ms | error_message | error_details | expires_at |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| RG001 | TENANT001 | RT001 | USER001 | 山田太郎さんのスキルサマリーレポート | SKILL | PDF | SUCCESS | {"employee_id": "EMP001", "report_date": "2025-06-01"} | /reports/2025/06/01/skill_summary_EMP001_20250601.pdf | 1048576 | 3 | 2025-06-01 18:45:00 | 2025-06-01 15:30:00 | 2025-06-01 15:30:05 | 2025-06-01 15:30:25 | 20000 | None | None | 2025-06-08 15:30:00 |
| RG002 | TENANT001 | RT002 | USER002 | 開発部目標進捗レポート | GOAL | EXCEL | FAILED | {"department_id": "DEPT001", "period_start": "2025-05-01", "period_end": "2025-05-31"} | None | None | 0 | None | 2025-06-01 16:00:00 | 2025-06-01 16:00:10 | 2025-06-01 16:00:15 | 5000 | データ取得エラー: 指定された期間のデータが見つかりません | {"error_code": "DATA_NOT_FOUND", "sql_error": "No rows found for the specified period"} | None |

## 特記事項

- 帳票生成履歴は1年間保持される
- 生成されたファイルは有効期限後に自動削除
- 処理時間はパフォーマンス監視に活用
- エラー詳細はJSON形式で構造化された情報を格納
- ダウンロード統計は利用状況分析に活用
- 大容量ファイルは外部ストレージに保存
- パラメータ情報は再生成時の参考に使用
- 生成成功時はファイルパス・サイズを必須記録
- 生成失敗時はエラー情報を詳細に記録
- 有効期限切れファイルは自動削除対象
- 同一パラメータでの重複生成は制限
- 処理時間が閾値を超える場合は警告
- ダウンロード時は統計情報を更新
- キャンセルされた生成は中間ファイルを削除
- テンプレート削除時は関連履歴を保持

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 帳票生成履歴テーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214905 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_214959 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215052 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222630 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223431 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |