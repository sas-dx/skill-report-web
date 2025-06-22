# テーブル定義書: HIS_ReportGeneration

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | HIS_ReportGeneration |
| 論理名 | 帳票生成履歴 |
| カテゴリ | 履歴系 |
| 生成日時 | 2025-06-21 22:02:17 |

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
| reportgeneration_id | HIS_ReportGenerationの主キー | SERIAL |  | × |  | HIS_ReportGenerationの主キー |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_his_reportgeneration_tenant_id | tenant_id | × | テナントID検索用インデックス |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_report_generation_template | None | None | None | CASCADE | RESTRICT | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_his_reportgeneration | PRIMARY KEY | reportgeneration_id, id | 主キー制約 |

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