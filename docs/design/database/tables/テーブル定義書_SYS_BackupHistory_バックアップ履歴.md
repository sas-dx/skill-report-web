# テーブル定義書: SYS_BackupHistory

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | SYS_BackupHistory |
| 論理名 | バックアップ履歴 |
| カテゴリ | システム系 |
| 生成日時 | 2025-06-04 06:57:02 |

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
| backup_id | バックアップID | VARCHAR | 50 | ○ |  | バックアップの一意識別子 |
| backup_type | バックアップ種別 | ENUM |  | ○ | FULL | バックアップの種別（FULL:フルバックアップ、INCREMENTAL:増分バックアップ、DIFFERENTIAL:差分バックアップ） |
| backup_scope | バックアップ範囲 | ENUM |  | ○ | DATABASE | バックアップ対象範囲（DATABASE:データベース全体、TABLE:特定テーブル、SCHEMA:特定スキーマ） |
| target_objects | 対象オブジェクト | TEXT |  | ○ |  | バックアップ対象のテーブル名やスキーマ名（JSON配列形式） |
| backup_start_time | バックアップ開始時刻 | TIMESTAMP |  | ○ |  | バックアップ処理の開始日時 |
| backup_end_time | バックアップ終了時刻 | TIMESTAMP |  | ○ |  | バックアップ処理の終了日時 |
| backup_status | バックアップ状況 | ENUM |  | ○ | RUNNING | バックアップの実行状況（RUNNING:実行中、SUCCESS:成功、FAILED:失敗、CANCELLED:キャンセル） |
| backup_file_path | バックアップファイルパス | VARCHAR | 1000 | ○ |  | バックアップファイルの保存先パス |
| backup_file_size | バックアップファイルサイズ | BIGINT |  | ○ |  | バックアップファイルのサイズ（バイト） |
| compression_type | 圧縮形式 | ENUM |  | ○ |  | バックアップファイルの圧縮形式（NONE:無圧縮、GZIP:gzip圧縮、ZIP:zip圧縮） |
| encryption_enabled | 暗号化有無 | BOOLEAN |  | ○ | False | バックアップファイルの暗号化有無 |
| checksum | チェックサム | VARCHAR | 128 | ○ |  | バックアップファイルの整合性チェック用ハッシュ値 |
| retention_period_days | 保持期間日数 | INTEGER |  | ○ | 30 | バックアップファイルの保持期間（日数） |
| expiry_date | 有効期限 | DATE |  | ○ |  | バックアップファイルの有効期限日 |
| backup_trigger | バックアップ契機 | ENUM |  | ○ | SCHEDULED | バックアップ実行の契機（SCHEDULED:スケジュール、MANUAL:手動、EMERGENCY:緊急） |
| executed_by | 実行者 | VARCHAR | 100 | ○ |  | バックアップを実行したユーザーまたはシステム |
| error_message | エラーメッセージ | TEXT |  | ○ |  | バックアップ失敗時のエラーメッセージ |
| recovery_tested | 復旧テスト済み | BOOLEAN |  | ○ | False | このバックアップからの復旧テストが実施済みかどうか |
| recovery_test_date | 復旧テスト日 | DATE |  | ○ |  | 復旧テストを実施した日付 |
| id | ID | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_SYS_BackupHistory_backup_id | backup_id | ○ | バックアップID検索用（一意） |
| idx_SYS_BackupHistory_start_time | backup_start_time | × | バックアップ開始時刻検索用 |
| idx_SYS_BackupHistory_status | backup_status | × | バックアップ状況検索用 |
| idx_SYS_BackupHistory_type_scope | backup_type, backup_scope | × | バックアップ種別と範囲の複合検索用 |
| idx_SYS_BackupHistory_expiry_date | expiry_date | × | 有効期限検索用（期限切れバックアップの削除処理用） |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_SYS_BackupHistory_backup_id | UNIQUE |  | バックアップID一意制約 |
| chk_SYS_BackupHistory_backup_type | CHECK | backup_type IN ('FULL', 'INCREMENTAL', 'DIFFERENTIAL') | バックアップ種別値チェック制約 |
| chk_SYS_BackupHistory_backup_scope | CHECK | backup_scope IN ('DATABASE', 'TABLE', 'SCHEMA') | バックアップ範囲値チェック制約 |
| chk_SYS_BackupHistory_backup_status | CHECK | backup_status IN ('RUNNING', 'SUCCESS', 'FAILED', 'CANCELLED') | バックアップ状況値チェック制約 |
| chk_SYS_BackupHistory_compression_type | CHECK | compression_type IS NULL OR compression_type IN ('NONE', 'GZIP', 'ZIP') | 圧縮形式値チェック制約 |
| chk_SYS_BackupHistory_backup_trigger | CHECK | backup_trigger IN ('SCHEDULED', 'MANUAL', 'EMERGENCY') | バックアップ契機値チェック制約 |
| chk_SYS_BackupHistory_retention_period | CHECK | retention_period_days > 0 | 保持期間正数チェック制約 |
| chk_SYS_BackupHistory_file_size | CHECK | backup_file_size IS NULL OR backup_file_size >= 0 | ファイルサイズ非負数チェック制約 |
| chk_SYS_BackupHistory_end_time | CHECK | backup_end_time IS NULL OR backup_end_time >= backup_start_time | 終了時刻は開始時刻以降チェック制約 |

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
