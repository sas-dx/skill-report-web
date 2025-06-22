# テーブル定義書: SYS_BackupHistory

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | SYS_BackupHistory |
| 論理名 | バックアップ履歴 |
| カテゴリ | システム系 |
| 生成日時 | 2025-06-21 22:02:18 |

## 概要

バックアップ履歴テーブルは、システムのデータバックアップ実行履歴を管理するシステムテーブルです。
主な目的：
- データベースバックアップの実行履歴管理
- バックアップの成功・失敗状況の記録
- バックアップファイルの保存場所管理
- 復旧時のバックアップ選択支援
このテーブルは、システムの可用性とデータ保護を支える重要なテーブルで、
障害時の迅速な復旧とデータ整合性の確保に貢献します。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| backuphistory_id | SYS_BackupHistoryの主キー | SERIAL |  | × |  | SYS_BackupHistoryの主キー |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_sys_backuphistory | PRIMARY KEY | backuphistory_id, id | 主キー制約 |

## サンプルデータ

| backup_id | backup_type | backup_scope | target_objects | backup_start_time | backup_end_time | backup_status | backup_file_path | backup_file_size | compression_type | encryption_enabled | checksum | retention_period_days | expiry_date | backup_trigger | executed_by | error_message | recovery_tested | recovery_test_date |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| BKP_20240101_001 | FULL | DATABASE | None | 2024-01-01 02:00:00 | 2024-01-01 02:45:00 | SUCCESS | /backup/full/skill_report_20240101_020000.sql.gz | 1073741824 | GZIP | True | a1b2c3d4e5f6789012345678901234567890abcd | 90 | 2024-04-01 | SCHEDULED | system_backup_job | None | True | 2024-01-15 |
| BKP_20240101_002 | INCREMENTAL | DATABASE | None | 2024-01-01 14:00:00 | 2024-01-01 14:05:00 | SUCCESS | /backup/incremental/skill_report_20240101_140000.sql.gz | 52428800 | GZIP | True | b2c3d4e5f6789012345678901234567890abcde1 | 30 | 2024-01-31 | SCHEDULED | system_backup_job | None | False | None |

## 特記事項

- バックアップIDは一意である必要がある
- バックアップ実行中はSTATUSがRUNNINGとなり、終了時に結果に応じて更新される
- フルバックアップは週次、増分バックアップは日次で実行される
- バックアップファイルは暗号化して保存される
- 有効期限を過ぎたバックアップファイルは自動削除される
- 復旧テストは定期的に実施し、結果を記録する
- 論理削除は is_deleted フラグで管理

## 業務ルール

- バックアップIDは「BKP_YYYYMMDD_NNN」形式で生成する
- フルバックアップは毎週日曜日2:00に実行する
- 増分バックアップは毎日14:00に実行する（日曜日を除く）
- バックアップファイルは必ず暗号化して保存する
- フルバックアップの保持期間は90日、増分バックアップは30日
- バックアップ失敗時は管理者にアラート通知を送信する
- 月次で復旧テストを実施し、結果を記録する
- 緊急時のマニュアルバックアップも履歴として記録する

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | システム | 初版作成 - SYS_BackupHistoryの詳細定義 |