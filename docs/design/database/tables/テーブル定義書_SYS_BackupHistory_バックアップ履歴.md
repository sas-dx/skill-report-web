# テーブル定義書: SYS_BackupHistory

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | SYS_BackupHistory |
| 論理名 | バックアップ履歴 |
| カテゴリ | システム系 |
| 生成日時 | 2025-06-24 22:56:15 |

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
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| backup_end_time | バックアップ終了時刻 | TIMESTAMP |  | ○ |  | バックアップ終了時刻 |
| backup_file_path | バックアップファイルパス | VARCHAR | 1000 | ○ |  | バックアップファイルパス |
| backup_file_size | バックアップファイルサイズ | BIGINT |  | ○ |  | バックアップファイルサイズ |
| backup_id | バックアップID | VARCHAR | 50 | ○ |  | バックアップID |
| backup_scope | バックアップ範囲 | ENUM |  | ○ | DATABASE | バックアップ範囲 |
| backup_start_time | バックアップ開始時刻 | TIMESTAMP |  | ○ |  | バックアップ開始時刻 |
| backup_status | バックアップ状況 | ENUM |  | ○ | RUNNING | バックアップ状況 |
| backup_trigger | バックアップ契機 | ENUM |  | ○ | SCHEDULED | バックアップ契機 |
| backup_type | バックアップ種別 | ENUM |  | ○ | FULL | バックアップ種別 |
| backuphistory_id | SYS_BackupHistoryの主キー | SERIAL |  | × |  | SYS_BackupHistoryの主キー |
| checksum | チェックサム | VARCHAR | 128 | ○ |  | チェックサム |
| compression_type | 圧縮形式 | ENUM |  | ○ |  | 圧縮形式 |
| encryption_enabled | 暗号化有無 | BOOLEAN |  | ○ | False | 暗号化有無 |
| error_message | エラーメッセージ | TEXT |  | ○ |  | エラーメッセージ |
| executed_by | 実行者 | VARCHAR | 100 | ○ |  | 実行者 |
| expiry_date | 有効期限 | DATE |  | ○ |  | 有効期限 |
| recovery_test_date | 復旧テスト日 | DATE |  | ○ |  | 復旧テスト日 |
| recovery_tested | 復旧テスト済み | BOOLEAN |  | ○ | False | 復旧テスト済み |
| retention_period_days | 保持期間日数 | INTEGER |  | ○ | 30 | 保持期間日数 |
| target_objects | 対象オブジェクト | TEXT |  | ○ |  | 対象オブジェクト |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_SYS_BackupHistory_backup_id | backup_id | ○ |  |
| idx_SYS_BackupHistory_start_time | backup_start_time | × |  |
| idx_SYS_BackupHistory_status | backup_status | × |  |
| idx_SYS_BackupHistory_type_scope | backup_type, backup_scope | × |  |
| idx_SYS_BackupHistory_expiry_date | expiry_date | × |  |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| uk_backup_id | UNIQUE |  | backup_id一意制約 |
| chk_backup_status | CHECK | backup_status IN (...) | backup_status値チェック制約 |
| chk_backup_type | CHECK | backup_type IN (...) | backup_type値チェック制約 |
| chk_compression_type | CHECK | compression_type IN (...) | compression_type値チェック制約 |

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
- バックアップIDは「BKP_YYYYMMDD_NNN」形式で生成する
- フルバックアップは毎週日曜日2:00に実行する
- 増分バックアップは毎日14:00に実行する（日曜日を除く）
- バックアップファイルは必ず暗号化して保存する
- フルバックアップの保持期間は90日、増分バックアップは30日
- バックアップ失敗時は管理者にアラート通知を送信する
- 月次で復旧テストを実施し、結果を記録する
- 緊急時のマニュアルバックアップも履歴として記録する

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | システム | 初版作成 - SYS_BackupHistoryの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214007 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214907 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215000 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215054 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223433 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |