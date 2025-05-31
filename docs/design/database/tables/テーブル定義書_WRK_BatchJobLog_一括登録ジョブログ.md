# テーブル定義書_WRK_BatchJobLog_一括登録ジョブログ

## テーブル概要

| 項目 | 内容 |
|------|------|
| テーブル名（物理） | WRK_BatchJobLog |
| テーブル名（論理） | 一括登録ジョブログ |
| 用途 | 一括データ登録処理のジョブ実行ログを管理するワークテーブル |
| カテゴリ | ワーク系 |
| 主な利用機能 | 作業実績管理 |
| 主な利用API | API-015 |
| 主な利用バッチ | BATCH-010 |
| 優先度 | 低 |

## カラム定義

| No | カラム名（物理） | カラム名（論理） | データ型 | 桁数 | NULL許可 | デフォルト値 | 主キー | 外部キー | 説明 |
|----|------------------|------------------|----------|------|----------|--------------|--------|----------|------|
| 1 | job_log_id | ジョブログID | VARCHAR | 20 | × | - | ○ | - | ジョブログの一意識別子 |
| 2 | tenant_id | テナントID | VARCHAR | 20 | × | - | - | MST_Tenant.tenant_id | テナント識別子 |
| 3 | job_type | ジョブ種別 | VARCHAR | 50 | × | - | - | - | 一括処理の種別（SKILL_BULK, PROJECT_BULK等） |
| 4 | job_name | ジョブ名 | VARCHAR | 100 | × | - | - | - | ジョブの名称 |
| 5 | file_name | ファイル名 | VARCHAR | 255 | ○ | NULL | - | - | 処理対象ファイル名 |
| 6 | file_path | ファイルパス | VARCHAR | 500 | ○ | NULL | - | - | 処理対象ファイルのパス |
| 7 | file_size | ファイルサイズ | BIGINT | - | ○ | NULL | - | - | 処理対象ファイルのサイズ（バイト） |
| 8 | total_records | 総レコード数 | INT | - | ○ | NULL | - | - | 処理対象の総レコード数 |
| 9 | processed_records | 処理済レコード数 | INT | - | × | 0 | - | - | 処理完了したレコード数 |
| 10 | success_records | 成功レコード数 | INT | - | × | 0 | - | - | 正常に処理されたレコード数 |
| 11 | error_records | エラーレコード数 | INT | - | × | 0 | - | - | エラーが発生したレコード数 |
| 12 | skip_records | スキップレコード数 | INT | - | × | 0 | - | - | スキップされたレコード数 |
| 13 | job_status | ジョブステータス | VARCHAR | 20 | × | 'PENDING' | - | - | ジョブの実行状態（PENDING/RUNNING/COMPLETED/FAILED/CANCELLED） |
| 14 | start_time | 開始時刻 | TIMESTAMP | - | ○ | NULL | - | - | ジョブ開始時刻 |
| 15 | end_time | 終了時刻 | TIMESTAMP | - | ○ | NULL | - | - | ジョブ終了時刻 |
| 16 | execution_time | 実行時間 | INT | - | ○ | NULL | - | - | 実行時間（秒） |
| 17 | error_message | エラーメッセージ | TEXT | - | ○ | NULL | - | - | エラー発生時のメッセージ |
| 18 | error_details | エラー詳細 | TEXT | - | ○ | NULL | - | - | エラーの詳細情報 |
| 19 | progress_percentage | 進捗率 | DECIMAL | 5,2 | × | 0.00 | - | - | 処理進捗率（0.00-100.00） |
| 20 | result_file_path | 結果ファイルパス | VARCHAR | 500 | ○ | NULL | - | - | 処理結果ファイルのパス |
| 21 | log_file_path | ログファイルパス | VARCHAR | 500 | ○ | NULL | - | - | 処理ログファイルのパス |
| 22 | created_at | 作成日時 | TIMESTAMP | - | × | CURRENT_TIMESTAMP | - | - | レコード作成日時 |
| 23 | created_by | 作成者ID | VARCHAR | 20 | × | - | - | MST_UserAuth.user_id | レコード作成者 |
| 24 | updated_at | 更新日時 | TIMESTAMP | - | × | CURRENT_TIMESTAMP | - | - | レコード更新日時 |
| 25 | updated_by | 更新者ID | VARCHAR | 20 | × | - | - | MST_UserAuth.user_id | レコード更新者 |

## インデックス定義

| インデックス名 | 種別 | 対象カラム | 説明 |
|----------------|------|------------|------|
| PK_WRK_BatchJobLog | PRIMARY KEY | job_log_id | 主キー |
| IDX_WRK_BatchJobLog_tenant | INDEX | tenant_id | テナント検索用 |
| IDX_WRK_BatchJobLog_type | INDEX | job_type | ジョブ種別検索用 |
| IDX_WRK_BatchJobLog_status | INDEX | job_status | ステータス検索用 |
| IDX_WRK_BatchJobLog_created | INDEX | created_at | 作成日時検索用 |
| IDX_WRK_BatchJobLog_user | INDEX | created_by | 作成者検索用 |

## 制約定義

| 制約名 | 種別 | 対象カラム | 説明 |
|--------|------|------------|------|
| PK_WRK_BatchJobLog | PRIMARY KEY | job_log_id | 主キー制約 |
| FK_WRK_BatchJobLog_tenant | FOREIGN KEY | tenant_id | テナントマスタ参照制約 |
| FK_WRK_BatchJobLog_created_by | FOREIGN KEY | created_by | 作成者参照制約 |
| FK_WRK_BatchJobLog_updated_by | FOREIGN KEY | updated_by | 更新者参照制約 |
| CHK_WRK_BatchJobLog_status | CHECK | job_status | job_status IN ('PENDING','RUNNING','COMPLETED','FAILED','CANCELLED') |
| CHK_WRK_BatchJobLog_records | CHECK | processed_records, success_records, error_records, skip_records | processed_records >= 0 AND success_records >= 0 AND error_records >= 0 AND skip_records >= 0 |
| CHK_WRK_BatchJobLog_progress | CHECK | progress_percentage | progress_percentage >= 0.00 AND progress_percentage <= 100.00 |
| CHK_WRK_BatchJobLog_time | CHECK | start_time, end_time | end_time IS NULL OR start_time IS NULL OR end_time >= start_time |

## 関連テーブル

### 参照先テーブル
- MST_Tenant（テナント管理）
- MST_UserAuth（ユーザー認証情報）

### 参照元テーブル
- なし（ワークテーブルのため）

## 備考・注意事項

### 業務ルール
1. ジョブステータスは以下の順序で遷移する：PENDING → RUNNING → COMPLETED/FAILED/CANCELLED
2. 進捗率は処理済レコード数/総レコード数で計算される
3. 実行時間は終了時刻-開始時刻で自動計算される
4. エラー発生時はエラーメッセージとエラー詳細を必須で記録する
5. 処理完了後は結果ファイルとログファイルのパスを記録する

### 運用上の注意
- 大量データ処理のため、適切なタイムアウト設定を行う
- 処理中断時の再開機能を考慮した設計とする
- ログファイルは定期的にアーカイブまたは削除する
- 同時実行数の制限を設ける

### パフォーマンス考慮事項
- テナントIDでの検索が頻繁に行われるためインデックスを設定
- ジョブ種別、ステータスでの絞り込みが多いためインデックスを設定
- 作成日時での範囲検索が多いためインデックスを設定

### セキュリティ考慮事項
- テナント分離を確実に行い、他テナントのジョブログにアクセスできないようにする
- ファイルパスの情報漏洩を防ぐため、適切なアクセス制御を行う
- エラー詳細に機密情報が含まれないよう注意する

### データ保持ポリシー
- 完了したジョブログは一定期間（例：3ヶ月）後にアーカイブする
- 失敗したジョブログは調査のため長期間保持する
- ファイルサイズが大きい場合は外部ストレージに保存する
