# テーブル定義書: WRK_BatchJobLog

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | WRK_BatchJobLog |
| 論理名 | 一括登録ジョブログ |
| カテゴリ | ワーク系 |
| 生成日時 | 2025-06-01 20:40:26 |

## 概要

一括登録・更新処理のジョブ実行ログを管理するワーク系テーブル。

主な目的：
- バッチ処理の実行状況監視
- エラー発生時の原因調査・トラブルシューティング
- 処理結果の統計情報管理
- 一括処理の進捗追跡

このテーブルは一時的なワークテーブルとして機能し、
処理完了後は定期的にアーカイブ・削除される。
主に管理者画面での監視とAPI経由での状況確認に使用される。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | ID | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  | マルチテナント識別子 |
| job_id | ジョブID | VARCHAR | 50 | ○ |  | 一括処理ジョブの一意識別子（UUID形式） |
| job_name | ジョブ名 | VARCHAR | 200 | ○ |  | 実行されたジョブの名称（画面表示用） |
| job_type | ジョブ種別 | ENUM |  | ○ | SKILL_IMPORT | ジョブの種別（SKILL_IMPORT:スキル情報一括登録、EMPLOYEE_IMPORT:社員情報一括登録、BULK_UPDATE:一括更新、BULK_DELETE:一括削除、DATA_EXPORT:データエクスポート） |
| status | 実行ステータス | ENUM |  | ○ | PENDING | ジョブの実行状況（PENDING:待機中、RUNNING:実行中、COMPLETED:完了、FAILED:失敗、CANCELLED:キャンセル） |
| start_time | 開始時刻 | TIMESTAMP |  | ○ |  | ジョブ実行開始日時 |
| end_time | 終了時刻 | TIMESTAMP |  | ○ |  | ジョブ実行終了日時 |
| total_records | 総レコード数 | INTEGER |  | ○ | 0 | 処理対象の総レコード数 |
| processed_records | 処理済みレコード数 | INTEGER |  | ○ | 0 | 実際に処理されたレコード数 |
| success_records | 成功レコード数 | INTEGER |  | ○ | 0 | 正常に処理されたレコード数 |
| error_records | エラーレコード数 | INTEGER |  | ○ | 0 | エラーが発生したレコード数 |
| error_details | エラー詳細 | TEXT |  | ○ |  | エラー内容の詳細情報（JSON形式でエラーメッセージ、行番号、カラム名等を格納） |
| input_file_path | 入力ファイルパス | VARCHAR | 500 | ○ |  | 処理対象の入力ファイルパス（CSVファイル等） |
| output_file_path | 出力ファイルパス | VARCHAR | 500 | ○ |  | 処理結果の出力ファイルパス（エラーレポート等） |
| executed_by | 実行者 | VARCHAR | 50 | ○ |  | ジョブを実行したユーザーのID |
| progress_percentage | 進捗率 | DECIMAL | 5,2 | ○ | 0.0 | ジョブの進捗率（0.00-100.00） |
| execution_environment | 実行環境 | VARCHAR | 100 | ○ |  | ジョブが実行された環境情報（サーバー名、プロセスID等） |
| job_parameters | ジョブパラメータ | TEXT |  | ○ |  | ジョブ実行時のパラメータ情報（JSON形式） |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  | レコード更新者のユーザーID |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_WRK_BatchJobLog_job_id | job_id | ○ | ジョブID検索用（一意） |
| idx_WRK_BatchJobLog_status | status | × | ステータス検索用（実行中ジョブの監視等） |
| idx_WRK_BatchJobLog_start_time | start_time | × | 開始時刻検索用（日時範囲での絞り込み） |
| idx_WRK_BatchJobLog_executed_by | executed_by | × | 実行者検索用（ユーザー別ジョブ履歴） |
| idx_WRK_BatchJobLog_job_type | job_type | × | ジョブ種別検索用（種別別の統計等） |
| idx_WRK_BatchJobLog_status_start_time | status, start_time | × | ステータスと開始時刻の複合検索用（監視画面での絞り込み） |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_WRK_BatchJobLog_executed_by | executed_by | MST_UserAuth | user_id | CASCADE | RESTRICT | 実行者（ユーザー認証情報）への外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| chk_WRK_BatchJobLog_status | CHECK | status IN ('PENDING', 'RUNNING', 'COMPLETED', 'FAILED', 'CANCELLED') | ステータス値チェック制約 |
| chk_WRK_BatchJobLog_job_type | CHECK | job_type IN ('SKILL_IMPORT', 'EMPLOYEE_IMPORT', 'BULK_UPDATE', 'BULK_DELETE', 'DATA_EXPORT') | ジョブ種別値チェック制約 |
| chk_WRK_BatchJobLog_records_positive | CHECK | total_records >= 0 AND processed_records >= 0 AND success_records >= 0 AND error_records >= 0 | レコード数正数チェック制約 |
| chk_WRK_BatchJobLog_progress_range | CHECK | progress_percentage >= 0.00 AND progress_percentage <= 100.00 | 進捗率範囲チェック制約（0-100%） |
| chk_WRK_BatchJobLog_time_consistency | CHECK | end_time IS NULL OR start_time IS NULL OR start_time <= end_time | 開始時刻と終了時刻の整合性チェック制約 |
| chk_WRK_BatchJobLog_record_consistency | CHECK | processed_records <= total_records AND (success_records + error_records) <= processed_records | 処理件数の整合性チェック制約 |

## サンプルデータ

| job_id | job_name | job_type | status | start_time | end_time | total_records | processed_records | success_records | error_records | error_details | input_file_path | output_file_path | executed_by | progress_percentage | execution_environment | job_parameters |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| JOB-001-20250601-001 | スキル情報一括登録（2025年6月分） | SKILL_IMPORT | COMPLETED | 2025-06-01 09:00:00 | 2025-06-01 09:15:30 | 500 | 500 | 485 | 15 | {"errors": [{"row": 23, "column": "skill_level", "message": "無効なスキルレベル値"}, {"row": 45, "column": "employee_id", "message": "存在しない社員ID"}]} | /uploads/skill_import_20250601.csv | /reports/skill_import_error_20250601.csv | admin001 | 100.0 | batch-server-01:12345 | {"delimiter": ",", "encoding": "UTF-8", "skip_header": true} |
| JOB-002-20250601-002 | 社員部署情報一括更新 | BULK_UPDATE | RUNNING | 2025-06-01 14:30:00 | None | 1000 | 650 | 640 | 10 | {"errors": [{"row": 15, "column": "department_id", "message": "存在しない部署ID"}]} | /uploads/employee_update_20250601.csv | None | hr_manager001 | 65.0 | batch-server-02:23456 | {"update_mode": "partial", "validate_only": false} |
| JOB-003-20250601-003 | 全社員スキルデータエクスポート | DATA_EXPORT | FAILED | 2025-06-01 16:00:00 | 2025-06-01 16:05:15 | 0 | 0 | 0 | 0 | {"system_error": "データベース接続エラー", "error_code": "DB_CONNECTION_TIMEOUT"} | None | /exports/skill_data_20250601.csv | system_admin001 | 0.0 | batch-server-01:34567 | {"format": "CSV", "include_deleted": false} |

## 特記事項

- ワーク系テーブルのため、処理完了から3ヶ月経過後に自動アーカイブ
- 大量データ処理時はprogress_percentageで進捗監視可能
- error_detailsとjob_parametersはJSON形式で柔軟な情報格納
- 実行環境情報により分散処理時の追跡が可能
- 外部ファイルパスは相対パスまたは論理パスで管理
- 長時間実行ジョブは定期的にprogress_percentage更新
- システム障害時の復旧用にexecution_environment情報を活用

## 業務ルール

- ジョブ開始時にPENDINGステータスでレコード作成
- 実行開始時にRUNNINGステータスに更新、start_time設定
- 処理完了時にCOMPLETED/FAILEDステータスに更新、end_time設定
- エラー発生時は即座にerror_detailsに詳細情報記録
- 進捗率は処理済みレコード数/総レコード数で自動計算
- 同一ユーザーの同時実行ジョブ数は最大3個まで制限
- RUNNING状態で24時間経過したジョブは自動的にFAILEDに変更
- ファイルパスは実際のファイル存在確認後に設定
- 処理完了後のファイルは7日間保持後に自動削除
- エラーレコード数が総レコード数の50%を超えた場合は処理中断

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - WRK_BatchJobLogの詳細定義 |
