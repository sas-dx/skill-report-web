# テーブル定義書: SYS_SystemLog (システムログ)

## 📋 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | SYS_SystemLog |
| 論理名 | システムログ |
| カテゴリ | システム系 |
| 作成日 | 2025-06-01 |

> **注意**: 本テーブル定義書は自動生成されます。手動編集は行わないでください。
> 詳細定義の変更は `table-details/SYS_SystemLog_details.yaml` で行ってください。



## 📝 テーブル概要

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


## 🗂️ カラム定義

| カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト | 説明 |
|----------|--------|----------|------|------|----|----|------------|------|
| id | ID | VARCHAR | 50 | × | ● |  |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × |  |  |  | 論理削除フラグ |
| log_level | ログレベル | ENUM |  | ○ |  |  |  | ログレベル（ERROR:エラー、WARN:警告、INFO:情報、DEBUG:デバッグ） |
| log_category | ログカテゴリ | VARCHAR | 50 | ○ |  |  |  | ログのカテゴリ（AUTH:認証、API:API、BATCH:バッチ、SYSTEM:システム） |
| message | ログメッセージ | TEXT |  | ○ |  |  |  | ログメッセージの内容 |
| user_id | 実行ユーザーID | VARCHAR | 50 | ○ |  | ● |  | ログを発生させたユーザーのID（MST_UserAuthへの外部キー） |
| session_id | セッションID | VARCHAR | 100 | ○ |  |  |  | セッションID（ユーザーセッションの識別） |
| ip_address | IPアドレス | VARCHAR | 45 | ○ |  |  |  | クライアントのIPアドレス（IPv4/IPv6対応） |
| user_agent | ユーザーエージェント | TEXT |  | ○ |  |  |  | クライアントのユーザーエージェント情報 |
| request_url | リクエストURL | TEXT |  | ○ |  |  |  | リクエストされたURL |
| request_method | HTTPメソッド | VARCHAR | 10 | ○ |  |  |  | HTTPメソッド（GET、POST、PUT、DELETE等） |
| response_status | レスポンスステータス | INT |  | ○ |  |  |  | HTTPレスポンスステータスコード |
| response_time | レスポンス時間 | INT |  | ○ |  |  |  | レスポンス時間（ミリ秒） |
| error_code | エラーコード | VARCHAR | 20 | ○ |  |  |  | アプリケーション固有のエラーコード |
| stack_trace | スタックトレース | TEXT |  | ○ |  |  |  | エラー発生時のスタックトレース |
| request_body | リクエストボディ | TEXT |  | ○ |  |  |  | リクエストボディ（個人情報含む可能性があるため暗号化） |
| response_body | レスポンスボディ | TEXT |  | ○ |  |  |  | レスポンスボディ（個人情報含む可能性があるため暗号化） |
| correlation_id | 相関ID | VARCHAR | 100 | ○ |  |  |  | 分散システムでのトレーシング用相関ID |
| component_name | コンポーネント名 | VARCHAR | 100 | ○ |  |  |  | ログを出力したコンポーネント名 |
| thread_name | スレッド名 | VARCHAR | 100 | ○ |  |  |  | ログを出力したスレッド名 |
| server_name | サーバー名 | VARCHAR | 100 | ○ |  |  |  | ログを出力したサーバー名 |
| created_at | 作成日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  |  |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  |  |  | レコード更新者のユーザーID |

## 🔍 インデックス定義

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

## 🔒 制約定義

| 制約名 | 制約タイプ | 対象カラム | 条件 | 説明 |
|--------|------------|------------|------|------|
| chk_log_level | CHECK |  | log_level IN ('ERROR', 'WARN', 'INFO', 'DEBUG') | ログレベル値チェック制約 |
| chk_response_status | CHECK |  | response_status IS NULL OR (response_status >= 100 AND response_status <= 599) | HTTPステータスコード値チェック制約 |
| chk_response_time | CHECK |  | response_time IS NULL OR response_time >= 0 | レスポンス時間非負値チェック制約 |

## 🔗 外部キー関係

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|------------|--------|--------------|------------|--------|--------|------|
| fk_log_user | user_id | MST_UserAuth | user_id | CASCADE | SET NULL | ユーザーへの外部キー |

## 📊 サンプルデータ

```json
[
  {
    "log_level": "INFO",
    "log_category": "AUTH",
    "message": "ユーザーログイン成功",
    "user_id": "user001",
    "session_id": "sess_abc123",
    "ip_address": "192.168.1.100",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "request_url": "/api/auth/login",
    "request_method": "POST",
    "response_status": 200,
    "response_time": 150,
    "error_code": null,
    "stack_trace": null,
    "correlation_id": "corr_xyz789",
    "component_name": "AuthService",
    "thread_name": "http-nio-8080-exec-1",
    "server_name": "app-server-01"
  },
  {
    "log_level": "ERROR",
    "log_category": "API",
    "message": "データベース接続エラー",
    "user_id": "user002",
    "session_id": "sess_def456",
    "ip_address": "192.168.1.101",
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "request_url": "/api/employees",
    "request_method": "GET",
    "response_status": 500,
    "response_time": 5000,
    "error_code": "DB_CONNECTION_ERROR",
    "stack_trace": "java.sql.SQLException: Connection timeout...",
    "correlation_id": "corr_abc456",
    "component_name": "EmployeeService",
    "thread_name": "http-nio-8080-exec-2",
    "server_name": "app-server-02"
  }
]
```

## 📌 特記事項

- 大量のログデータが蓄積されるため、定期的なアーカイブが必要
- 個人情報を含む可能性があるリクエスト・レスポンスボディは暗号化
- パフォーマンス分析のためレスポンス時間を記録
- 分散システムでのトレーシングのため相関IDを使用
- ログレベルによる検索頻度が高いためインデックス最適化
- 古いログは自動的にアーカイブ（6ヶ月経過後）

## 📋 業務ルール

- ERRORレベルのログは即座にアラート通知
- WARNレベルのログは日次で監視・分析
- レスポンス時間が5秒を超える場合は自動的にWARNログ出力
- 個人情報を含むログは暗号化して保存
- ログ保持期間は6ヶ月（法的要件に応じて調整）
- システム障害時の調査のため詳細ログを保持
- 相関IDによりリクエストの全体フローを追跡可能
