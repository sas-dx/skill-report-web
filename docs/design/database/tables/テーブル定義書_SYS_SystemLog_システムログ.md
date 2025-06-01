# テーブル定義書: SYS_SystemLog

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | SYS_SystemLog |
| 論理名 | システムログ |
| カテゴリ | システム系 |
| 生成日時 | 2025-06-01 20:40:26 |

## 概要

SYS_SystemLog（システムログ）は、アプリケーション全体で発生するあらゆるシステムイベントを記録・管理するログテーブルです。

主な目的：
- システム運用監視（エラー、警告、情報ログの記録）
- セキュリティ監査（認証、アクセス、操作履歴の追跡）
- パフォーマンス分析（レスポンス時間、処理時間の測定）
- 障害調査・デバッグ（詳細なエラー情報、スタックトレースの保存）
- 分散システムトレーシング（相関IDによるリクエスト追跡）
- コンプライアンス対応（法的要件に基づくログ保持）

このテーブルは、システムの安定運用、セキュリティ確保、問題解決の基盤となる重要なログ管理システムです。
大量データの効率的な管理のため、月次パーティション分割と自動アーカイブ機能を実装しています。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | ID | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| log_level | ログレベル | ENUM |  | ○ |  | ログレベル（ERROR:エラー、WARN:警告、INFO:情報、DEBUG:デバッグ） |
| log_category | ログカテゴリ | VARCHAR | 50 | ○ |  | ログのカテゴリ（AUTH:認証、API:API、BATCH:バッチ、SYSTEM:システム） |
| message | ログメッセージ | TEXT |  | ○ |  | ログメッセージの内容 |
| user_id | 実行ユーザーID | VARCHAR | 50 | ○ |  | ログを発生させたユーザーのID（MST_UserAuthへの外部キー） |
| session_id | セッションID | VARCHAR | 100 | ○ |  | セッションID（ユーザーセッションの識別） |
| ip_address | IPアドレス | VARCHAR | 45 | ○ |  | クライアントのIPアドレス（IPv4/IPv6対応） |
| user_agent | ユーザーエージェント | TEXT |  | ○ |  | クライアントのユーザーエージェント情報 |
| request_url | リクエストURL | TEXT |  | ○ |  | リクエストされたURL |
| request_method | HTTPメソッド | VARCHAR | 10 | ○ |  | HTTPメソッド（GET、POST、PUT、DELETE等） |
| response_status | レスポンスステータス | INT |  | ○ |  | HTTPレスポンスステータスコード |
| response_time | レスポンス時間 | INT |  | ○ |  | レスポンス時間（ミリ秒） |
| error_code | エラーコード | VARCHAR | 20 | ○ |  | アプリケーション固有のエラーコード |
| stack_trace | スタックトレース | TEXT |  | ○ |  | エラー発生時のスタックトレース |
| request_body | リクエストボディ | TEXT |  | ○ |  | リクエストボディ（個人情報含む可能性があるため暗号化） |
| response_body | レスポンスボディ | TEXT |  | ○ |  | レスポンスボディ（個人情報含む可能性があるため暗号化） |
| correlation_id | 相関ID | VARCHAR | 100 | ○ |  | 分散システムでのトレーシング用相関ID |
| component_name | コンポーネント名 | VARCHAR | 100 | ○ |  | ログを出力したコンポーネント名 |
| thread_name | スレッド名 | VARCHAR | 100 | ○ |  | ログを出力したスレッド名 |
| server_name | サーバー名 | VARCHAR | 100 | ○ |  | ログを出力したサーバー名 |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  | レコード更新者のユーザーID |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_log_level | log_level | × | ログレベル別検索用 |
| idx_log_category | log_category | × | ログカテゴリ別検索用 |
| idx_user_id | user_id | × | ユーザー別検索用 |
| idx_session_id | session_id | × | セッション別検索用 |
| idx_ip_address | ip_address | × | IPアドレス別検索用 |
| idx_error_code | error_code | × | エラーコード別検索用 |
| idx_correlation_id | correlation_id | × | 相関ID別検索用 |
| idx_component | component_name | × | コンポーネント別検索用 |
| idx_server | server_name | × | サーバー別検索用 |
| idx_response_time | response_time | × | レスポンス時間検索用（パフォーマンス分析） |
| idx_created_at_level | created_at, log_level | × | 日時・レベル複合検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_log_user | user_id | MST_UserAuth | user_id | CASCADE | SET NULL | ユーザーへの外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| chk_log_level | CHECK | log_level IN ('ERROR', 'WARN', 'INFO', 'DEBUG') | ログレベル値チェック制約 |
| chk_response_status | CHECK | response_status IS NULL OR (response_status >= 100 AND response_status <= 599) | HTTPステータスコード値チェック制約 |
| chk_response_time | CHECK | response_time IS NULL OR response_time >= 0 | レスポンス時間非負値チェック制約 |

## サンプルデータ

| log_level | log_category | message | user_id | session_id | ip_address | user_agent | request_url | request_method | response_status | response_time | error_code | stack_trace | correlation_id | component_name | thread_name | server_name |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| INFO | AUTH | ユーザーログイン成功 | user001 | sess_abc123 | 192.168.1.100 | Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 | /api/auth/login | POST | 200 | 150 | None | None | corr_xyz789 | AuthService | http-nio-8080-exec-1 | app-server-01 |
| ERROR | API | データベース接続エラー | user002 | sess_def456 | 192.168.1.101 | Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 | /api/employees | GET | 500 | 5000 | DB_CONNECTION_ERROR | java.sql.SQLException: Connection timeout... | corr_abc456 | EmployeeService | http-nio-8080-exec-2 | app-server-02 |

## 特記事項

- 大量のログデータが蓄積されるため、定期的なアーカイブが必要
- 個人情報を含む可能性があるリクエスト・レスポンスボディは暗号化
- パフォーマンス分析のためレスポンス時間を記録
- 分散システムでのトレーシングのため相関IDを使用
- ログレベルによる検索頻度が高いためインデックス最適化
- 古いログは自動的にアーカイブ（6ヶ月経過後）

## 業務ルール

- ERRORレベルのログは即座にアラート通知
- WARNレベルのログは日次で監視・分析
- レスポンス時間が5秒を超える場合は自動的にWARNログ出力
- 個人情報を含むログは暗号化して保存
- ログ保持期間は6ヶ月（法的要件に応じて調整）
- システム障害時の調査のため詳細ログを保持
- 相関IDによりリクエストの全体フローを追跡可能

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - システムログテーブルの詳細定義 |
