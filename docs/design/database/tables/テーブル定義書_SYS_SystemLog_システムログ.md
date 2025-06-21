# テーブル定義書: SYS_SystemLog

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | SYS_SystemLog |
| 論理名 | システムログ |
| カテゴリ | システム系 |
| 生成日時 | 2025-06-21 17:20:33 |

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
| log_level |  | ENUM |  | ○ |  |  |
| log_category |  | VARCHAR |  | ○ |  |  |
| message |  | TEXT |  | ○ |  |  |
| user_id |  | VARCHAR |  | ○ |  |  |
| session_id |  | VARCHAR |  | ○ |  |  |
| ip_address |  | VARCHAR |  | ○ |  |  |
| user_agent |  | TEXT |  | ○ |  |  |
| request_url |  | TEXT |  | ○ |  |  |
| request_method |  | VARCHAR |  | ○ |  |  |
| response_status |  | INT |  | ○ |  |  |
| response_time |  | INT |  | ○ |  |  |
| error_code |  | VARCHAR |  | ○ |  |  |
| stack_trace |  | TEXT |  | ○ |  |  |
| request_body |  | TEXT |  | ○ |  |  |
| response_body |  | TEXT |  | ○ |  |  |
| correlation_id |  | VARCHAR |  | ○ |  |  |
| component_name |  | VARCHAR |  | ○ |  |  |
| thread_name |  | VARCHAR |  | ○ |  |  |
| server_name |  | VARCHAR |  | ○ |  |  |
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_log_level | log_level | × |  |
| idx_log_category | log_category | × |  |
| idx_user_id | user_id | × |  |
| idx_session_id | session_id | × |  |
| idx_ip_address | ip_address | × |  |
| idx_error_code | error_code | × |  |
| idx_correlation_id | correlation_id | × |  |
| idx_component | component_name | × |  |
| idx_server | server_name | × |  |
| idx_response_time | response_time | × |  |
| idx_created_at_level | created_at, log_level | × |  |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_sys_systemlog | PRIMARY KEY | id | 主キー制約 |
| chk_response_status | CHECK | response_status IN (...) | response_status値チェック制約 |

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