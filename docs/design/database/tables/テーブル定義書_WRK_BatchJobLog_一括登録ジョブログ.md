# テーブル定義書: WRK_BatchJobLog

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | WRK_BatchJobLog |
| 論理名 | 一括登録ジョブログ |
| カテゴリ | ワーク系 |
| 生成日時 | 2025-06-24 23:02:17 |

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
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| job_id | ジョブID | VARCHAR | 50 | ○ |  | ジョブID |
| batchjoblog_id | WRK_BatchJobLogの主キー | SERIAL |  | × |  | WRK_BatchJobLogの主キー |
| end_time | 終了時刻 | TIMESTAMP |  | ○ |  | 終了時刻 |
| error_details | エラー詳細 | TEXT |  | ○ |  | エラー詳細 |
| error_records | エラーレコード数 | INTEGER |  | ○ | 0 | エラーレコード数 |
| executed_by | 実行者 | VARCHAR | 50 | ○ |  | 実行者 |
| execution_environment | 実行環境 | VARCHAR | 100 | ○ |  | 実行環境 |
| input_file_path | 入力ファイルパス | VARCHAR | 500 | ○ |  | 入力ファイルパス |
| job_name | ジョブ名 | VARCHAR | 200 | ○ |  | ジョブ名 |
| job_parameters | ジョブパラメータ | TEXT |  | ○ |  | ジョブパラメータ |
| job_type | ジョブ種別 | ENUM |  | ○ | SKILL_IMPORT | ジョブ種別 |
| output_file_path | 出力ファイルパス | VARCHAR | 500 | ○ |  | 出力ファイルパス |
| processed_records | 処理済みレコード数 | INTEGER |  | ○ | 0 | 処理済みレコード数 |
| progress_percentage | 進捗率 | DECIMAL | 5,2 | ○ | 0.0 | 進捗率 |
| start_time | 開始時刻 | TIMESTAMP |  | ○ |  | 開始時刻 |
| status | 実行ステータス | ENUM |  | ○ | PENDING | 実行ステータス |
| success_records | 成功レコード数 | INTEGER |  | ○ | 0 | 成功レコード数 |
| total_records | 総レコード数 | INTEGER |  | ○ | 0 | 総レコード数 |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_WRK_BatchJobLog_job_id | job_id | ○ |  |
| idx_WRK_BatchJobLog_status | status | × |  |
| idx_WRK_BatchJobLog_start_time | start_time | × |  |
| idx_WRK_BatchJobLog_executed_by | executed_by | × |  |
| idx_WRK_BatchJobLog_job_type | job_type | × |  |
| idx_WRK_BatchJobLog_status_start_time | status, start_time | × |  |
| idx_wrk_batchjoblog_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_WRK_BatchJobLog_executed_by | executed_by | MST_UserAuth | id | CASCADE | RESTRICT | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| uk_job_id | UNIQUE |  | job_id一意制約 |
| chk_job_type | CHECK | job_type IN (...) | job_type値チェック制約 |
| chk_status | CHECK | status IN (...) | status値チェック制約 |

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

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - WRK_BatchJobLogの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214007 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214908 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215001 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215054 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222632 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223433 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |