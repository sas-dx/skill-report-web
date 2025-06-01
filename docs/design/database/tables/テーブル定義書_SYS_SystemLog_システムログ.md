# テーブル定義書：SYS_SystemLog（システムログ）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-022 |
| **テーブル名** | SYS_SystemLog |
| **論理名** | システムログ |
| **カテゴリ** | システム系 |
| **機能カテゴリ** | システム管理 |
| **優先度** | 高 |
| **個人情報含有** | なし |
| **機密情報レベル** | 中 |
| **暗号化要否** | 不要 |
| **ステータス** | 運用中 |
| **作成日** | 2025-06-01 |
| **最終更新日** | 2025-06-01 |

## 2. テーブル概要

### 2.1 概要・目的
SCR-ADMIN

### 2.2 特記事項
- 大量のログデータが蓄積されるため、定期的なアーカイブが必要
- 個人情報を含む可能性があるリクエスト・レスポンスボディは暗号化
- パフォーマンス分析のためレスポンス時間を記録
- 分散システムでのトレーシングのため相関IDを使用
- ログレベルによる検索頻度が高いためインデックス最適化
- 古いログは自動的にアーカイブ（6ヶ月経過後）

### 2.3 関連API
API-021

### 2.4 関連バッチ
BATCH-014

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | id | ID | VARCHAR | 50 | × | ○ | - | - | 主キー |
| 2 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | テナントID |
| 3 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | レコードが有効かどうか |
| 4 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 5 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 6 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 7 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |
| 8 | log_level | ログレベル | ENUM | None | ○ | - | - | - | ログレベル（ERROR:エラー、WARN:警告、INFO:情報、DEBUG:デバッグ） |
| 9 | log_category | ログカテゴリ | VARCHAR | 50 | ○ | - | - | - | ログのカテゴリ（AUTH:認証、API:API、BATCH:バッチ、SYSTEM:システム） |
| 10 | message | ログメッセージ | TEXT | None | ○ | - | - | - | ログメッセージの内容 |
| 11 | user_id | 実行ユーザーID | VARCHAR | 50 | ○ | - | ○ | - | ログを発生させたユーザーのID（MST_UserAuthへの外部キー） |
| 12 | session_id | セッションID | VARCHAR | 100 | ○ | - | ○ | - | セッションID（ユーザーセッションの識別） |
| 13 | ip_address | IPアドレス | VARCHAR | 45 | ○ | - | - | - | クライアントのIPアドレス（IPv4/IPv6対応） |
| 14 | user_agent | ユーザーエージェント | TEXT | None | ○ | - | - | - | クライアントのユーザーエージェント情報 |
| 15 | request_url | リクエストURL | TEXT | None | ○ | - | - | - | リクエストされたURL |
| 16 | request_method | HTTPメソッド | VARCHAR | 10 | ○ | - | - | - | HTTPメソッド（GET、POST、PUT、DELETE等） |
| 17 | response_status | レスポンスステータス | INT | None | ○ | - | - | - | HTTPレスポンスステータスコード |
| 18 | response_time | レスポンス時間 | INT | None | ○ | - | - | - | レスポンス時間（ミリ秒） |
| 19 | error_code | エラーコード | VARCHAR | 20 | ○ | - | - | - | アプリケーション固有のエラーコード |
| 20 | stack_trace | スタックトレース | TEXT | None | ○ | - | - | - | エラー発生時のスタックトレース |
| 21 | request_body | リクエストボディ | TEXT | None | ○ | - | - | - | リクエストボディ（個人情報含む可能性があるため暗号化） |
| 22 | response_body | レスポンスボディ | TEXT | None | ○ | - | - | - | レスポンスボディ（個人情報含む可能性があるため暗号化） |
| 23 | correlation_id | 相関ID | VARCHAR | 100 | ○ | - | ○ | - | 分散システムでのトレーシング用相関ID |
| 24 | component_name | コンポーネント名 | VARCHAR | 100 | ○ | - | - | - | ログを出力したコンポーネント名 |
| 25 | thread_name | スレッド名 | VARCHAR | 100 | ○ | - | - | - | ログを出力したスレッド名 |
| 26 | server_name | サーバー名 | VARCHAR | 100 | ○ | - | - | - | ログを出力したサーバー名 |


### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | id | 主キー |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |
| idx_created_at | INDEX | created_at | 作成日時検索用 |
| idx_log_level | INDEX | log_level | ログレベル別検索用 |
| idx_log_category | INDEX | log_category | ログカテゴリ別検索用 |
| idx_user_id | INDEX | user_id | ユーザー別検索用 |
| idx_session_id | INDEX | session_id | セッション別検索用 |
| idx_ip_address | INDEX | ip_address | IPアドレス別検索用 |
| idx_error_code | INDEX | error_code | エラーコード別検索用 |
| idx_correlation_id | INDEX | correlation_id | 相関ID別検索用 |
| idx_component | INDEX | component_name | コンポーネント別検索用 |
| idx_server | INDEX | server_name | サーバー別検索用 |
| idx_response_time | INDEX | response_time | レスポンス時間検索用（パフォーマンス分析） |
| idx_created_at_level | INDEX | created_at, log_level | 日時・レベル複合検索用 |


### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_sys_systemlog | PRIMARY KEY | id | 主キー制約 |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_log_level | CHECK |  | log_level IN ('ERROR', 'WARN', 'INFO', 'DEBUG') |
| chk_response_status | CHECK |  | response_status IS NULL OR (response_status >= 100 AND response_status <= 599) |
| chk_response_time | CHECK |  | response_time IS NULL OR response_time >= 0 |


## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_UserAuth | created_by, updated_by | 1:N | ユーザー情報 |
| MST_UserAuth | user_id | 1:N | ユーザーへの外部キー |


### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| - | - | - | 必要に応じて追加 |

## 5. データ仕様

### 5.1 データ例
```sql
-- サンプルデータ
INSERT INTO SYS_SystemLog (
    id, tenant_id, log_level, log_category, message, user_id, session_id, ip_address, user_agent, request_url, request_method, response_status, response_time, error_code, stack_trace, correlation_id, component_name, thread_name, server_name, created_by, updated_by
) VALUES (
    'sample_001', 'tenant_001', 'INFO', 'AUTH', 'ユーザーログイン成功', 'user001', 'sess_abc123', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '/api/auth/login', 'POST', '200', '150', NULL, NULL, 'corr_xyz789', 'AuthService', 'http-nio-8080-exec-1', 'app-server-01', 'user_admin', 'user_admin'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 500件 | 初期設定データ |
| 月間増加件数 | 100件 | 想定値 |
| 年間増加件数 | 1,200件 | 想定値 |
| 5年後想定件数 | 6,500件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：なし
- パーティション条件：-

### 6.3 アーカイブ
- アーカイブ条件：作成から3年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | id, tenant_id | 基本検索 |
| INSERT | 中 | - | 新規登録 |
| UPDATE | 中 | id | 更新処理 |
| DELETE | 低 | id | 削除処理 |

### 7.2 パフォーマンス要件
- SELECT：15ms以内
- INSERT：50ms以内
- UPDATE：50ms以内
- DELETE：100ms以内

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| tenant_admin | ○ | ○ | ○ | × | テナント管理者（自テナントのみ） |
| user | ○ | × | × | × | 一般ユーザー（参照のみ） |

### 8.2 データ保護
- 個人情報：なし
- 機密情報：中レベル
- 暗号化：不要

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存システム
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
-- システムログテーブル作成DDL
CREATE TABLE SYS_SystemLog (
    id VARCHAR(50) NOT NULL COMMENT 'ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '有効フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT '作成者ID',
    updated_by VARCHAR(50) NOT NULL COMMENT '更新者ID',
    log_level ENUM COMMENT 'ログレベル',
    log_category VARCHAR(50) COMMENT 'ログカテゴリ',
    message TEXT COMMENT 'ログメッセージ',
    user_id VARCHAR(50) COMMENT '実行ユーザーID',
    session_id VARCHAR(100) COMMENT 'セッションID',
    ip_address VARCHAR(45) COMMENT 'IPアドレス',
    user_agent TEXT COMMENT 'ユーザーエージェント',
    request_url TEXT COMMENT 'リクエストURL',
    request_method VARCHAR(10) COMMENT 'HTTPメソッド',
    response_status INT COMMENT 'レスポンスステータス',
    response_time INT COMMENT 'レスポンス時間',
    error_code VARCHAR(20) COMMENT 'エラーコード',
    stack_trace TEXT COMMENT 'スタックトレース',
    request_body TEXT COMMENT 'リクエストボディ',
    response_body TEXT COMMENT 'レスポンスボディ',
    correlation_id VARCHAR(100) COMMENT '相関ID',
    component_name VARCHAR(100) COMMENT 'コンポーネント名',
    thread_name VARCHAR(100) COMMENT 'スレッド名',
    server_name VARCHAR(100) COMMENT 'サーバー名',
    PRIMARY KEY (id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_active (is_active),
    INDEX idx_created_at (created_at),
    INDEX idx_log_level (log_level),
    INDEX idx_log_category (log_category),
    INDEX idx_user_id (user_id),
    INDEX idx_session_id (session_id),
    INDEX idx_ip_address (ip_address),
    INDEX idx_error_code (error_code),
    INDEX idx_correlation_id (correlation_id),
    INDEX idx_component (component_name),
    INDEX idx_server (server_name),
    INDEX idx_response_time (response_time),
    INDEX idx_created_at_level (created_at, log_level),
    CONSTRAINT fk_log_user FOREIGN KEY (user_id) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='システムログ';

```

## 10. 特記事項

1. **設計方針**
   - システム系として設計
   - マルチテナント対応
   - 監査証跡の保持

2. **運用上の注意点**
   - 定期的なデータクリーンアップが必要
   - パフォーマンス監視を実施
   - データ量見積もりの定期見直し

3. **今後の拡張予定**
   - 必要に応じて機能拡張を検討

4. **関連画面**
   - 関連画面情報

5. **データ量・パフォーマンス監視**
   - データ量が想定の150%を超えた場合はアラート
   - 応答時間が設定値の120%を超えた場合は調査


## 11. 業務ルール

- ERRORレベルのログは即座にアラート通知
- WARNレベルのログは日次で監視・分析
- レスポンス時間が5秒を超える場合は自動的にWARNログ出力
- 個人情報を含むログは暗号化して保存
- ログ保持期間は6ヶ月（法的要件に応じて調整）
- システム障害時の調査のため詳細ログを保持
- 相関IDによりリクエストの全体フローを追跡可能
