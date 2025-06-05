# テーブル定義書: HIS_ReportGeneration

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | HIS_ReportGeneration |
| 論理名 | 帳票生成履歴 |
| カテゴリ | 履歴系 |
| 生成日時 | 2025-06-05 23:01:00 |

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
| id | ID | VARCHAR | 50 | ○ |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  | マルチテナント識別子 |
| template_id | テンプレートID | VARCHAR | 50 | ○ |  | 使用された帳票テンプレートのID（MST_ReportTemplateへの参照） |
| requested_by | 要求者 | VARCHAR | 50 | ○ |  | 帳票生成を要求したユーザーID |
| report_title | 帳票タイトル | VARCHAR | 200 | ○ |  | 生成された帳票のタイトル |
| report_category | 帳票カテゴリ | ENUM |  | ○ |  | 帳票の分類（SKILL:スキル関連、GOAL:目標関連、EVALUATION:評価関連、SUMMARY:サマリー、ANALYTICS:分析） |
| output_format | 出力形式 | ENUM |  | ○ |  | 帳票の出力形式（PDF:PDF、EXCEL:Excel、CSV:CSV、HTML:HTML） |
| generation_status | 生成状態 | ENUM |  | ○ |  | 生成の状態（PENDING:待機中、PROCESSING:処理中、SUCCESS:成功、FAILED:失敗、CANCELLED:キャンセル） |
| parameters | パラメータ | TEXT |  | ○ |  | 帳票生成時のパラメータ（JSON形式） |
| file_path | ファイルパス | VARCHAR | 500 | ○ |  | 生成された帳票ファイルのパス |
| file_size | ファイルサイズ | BIGINT |  | ○ |  | 生成された帳票ファイルのサイズ（バイト） |
| download_count | ダウンロード回数 | INTEGER |  | ○ | 0 | 帳票がダウンロードされた回数 |
| last_downloaded_at | 最終ダウンロード日時 | TIMESTAMP |  | ○ |  | 帳票が最後にダウンロードされた日時 |
| requested_at | 要求日時 | TIMESTAMP |  | ○ |  | 帳票生成が要求された日時 |
| started_at | 開始日時 | TIMESTAMP |  | ○ |  | 帳票生成処理が開始された日時 |
| completed_at | 完了日時 | TIMESTAMP |  | ○ |  | 帳票生成処理が完了した日時 |
| processing_time_ms | 処理時間 | INTEGER |  | ○ |  | 帳票生成にかかった時間（ミリ秒） |
| error_message | エラーメッセージ | TEXT |  | ○ |  | 生成失敗時のエラーメッセージ |
| error_details | エラー詳細 | TEXT |  | ○ |  | 生成失敗時のエラー詳細情報（JSON形式） |
| expires_at | 有効期限 | TIMESTAMP |  | ○ |  | 生成された帳票ファイルの有効期限 |
| is_deleted | 削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_report_generation_template | template_id | × | テンプレートID別検索用 |
| idx_report_generation_requester | requested_by | × | 要求者別検索用 |
| idx_report_generation_tenant_status | tenant_id, generation_status | × | テナント別生成状態検索用 |
| idx_report_generation_category | report_category | × | 帳票カテゴリ別検索用 |
| idx_report_generation_format | output_format | × | 出力形式別検索用 |
| idx_report_generation_requested | requested_at | × | 要求日時検索用 |
| idx_report_generation_completed | completed_at | × | 完了日時検索用 |
| idx_report_generation_expires | expires_at | × | 有効期限検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_report_generation_template | template_id | MST_ReportTemplate | id | CASCADE | RESTRICT | 帳票テンプレートへの外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| chk_report_generation_category | CHECK | report_category IN ('SKILL', 'GOAL', 'EVALUATION', 'SUMMARY', 'ANALYTICS') | 帳票カテゴリ値チェック制約 |
| chk_report_generation_format | CHECK | output_format IN ('PDF', 'EXCEL', 'CSV', 'HTML') | 出力形式値チェック制約 |
| chk_report_generation_status | CHECK | generation_status IN ('PENDING', 'PROCESSING', 'SUCCESS', 'FAILED', 'CANCELLED') | 生成状態値チェック制約 |
| chk_report_generation_file_size_positive | CHECK | file_size IS NULL OR file_size >= 0 | ファイルサイズ正数チェック制約 |
| chk_report_generation_download_count_positive | CHECK | download_count >= 0 | ダウンロード回数正数チェック制約 |
| chk_report_generation_processing_time_positive | CHECK | processing_time_ms IS NULL OR processing_time_ms >= 0 | 処理時間正数チェック制約 |

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

## 業務ルール

- 生成成功時はファイルパス・サイズを必須記録
- 生成失敗時はエラー情報を詳細に記録
- 有効期限切れファイルは自動削除対象
- 同一パラメータでの重複生成は制限
- 処理時間が閾値を超える場合は警告
- ダウンロード時は統計情報を更新
- キャンセルされた生成は中間ファイルを削除
- テンプレート削除時は関連履歴を保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 帳票生成履歴テーブルの詳細定義 |
