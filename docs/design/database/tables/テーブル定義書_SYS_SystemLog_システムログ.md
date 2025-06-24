# テーブル定義書: SYS_SystemLog

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | SYS_SystemLog |
| 論理名 | システムログ |
| カテゴリ | システム系 |
| 生成日時 | 2025-06-24 23:02:19 |

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
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  | テナントID |
| log_level | ログレベル | ENUM |  | ○ |  | ログレベル |
| message | ログメッセージ | TEXT |  | ○ |  | ログメッセージ |
| component_name | コンポーネント名 | VARCHAR | 100 | ○ |  | コンポーネント名 |
| user_id | 実行ユーザーID | VARCHAR | 50 | ○ |  | 実行ユーザーID |
| session_id | セッションID | VARCHAR | 100 | ○ |  | セッションID |
| correlation_id | 相関ID | VARCHAR | 100 | ○ |  | 相関ID |
| error_code | エラーコード | VARCHAR | 20 | ○ |  | エラーコード |
| stack_trace | スタックトレース | TEXT |  | ○ |  | スタックトレース |
| request_url | リクエストURL | TEXT |  | ○ |  | リクエストURL |
| request_method | HTTPメソッド | VARCHAR | 10 | ○ |  | HTTPメソッド |
| request_body | リクエストボディ | TEXT |  | ○ |  | リクエストボディ |
| response_status | レスポンスステータス | INT |  | ○ |  | レスポンスステータス |
| response_body | レスポンスボディ | TEXT |  | ○ |  | レスポンスボディ |
| user_agent | ユーザーエージェント | TEXT |  | ○ |  | ユーザーエージェント |
| ip_address | IPアドレス | VARCHAR | 45 | ○ |  | IPアドレス |
| log_category | ログカテゴリ | VARCHAR | 50 | ○ |  | ログカテゴリ |
| response_time | レスポンス時間 | INT |  | ○ |  | レスポンス時間 |
| server_name | サーバー名 | VARCHAR | 100 | ○ |  | サーバー名 |
| thread_name | スレッド名 | VARCHAR | 100 | ○ |  | スレッド名 |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

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

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_log_user | user_id | MST_UserAuth | id | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
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
- ERRORレベルのログは即座にアラート通知
- WARNレベルのログは日次で監視・分析
- レスポンス時間が5秒を超える場合は自動的にWARNログ出力
- 個人情報を含むログは暗号化して保存
- ログ保持期間は6ヶ月（法的要件に応じて調整）
- システム障害時の調査のため詳細ログを保持
- 相関IDによりリクエストの全体フローを追跡可能

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - システムログテーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214007 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214907 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215001 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215054 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223433 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |
| SPECIAL.20250624_223559 | 2025-06-24 | 特殊ケース修正ツール | tenant_idカラム追加とカラム順序の最終調整 |
| FINAL.20250624_223648 | 2025-06-24 | SYS_SystemLog最終修正ツール | 重複主キーカラム除去とカラム順序の最終修正 |