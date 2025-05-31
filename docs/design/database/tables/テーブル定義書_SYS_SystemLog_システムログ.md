# テーブル定義書：システムログ (SYS_SystemLog)

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-022 |
| **テーブル名** | SYS_SystemLog |
| **論理名** | システムログ |
| **カテゴリ** | システム系 |
| **優先度** | 高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-05-31 |
| **最終更新日** | 2025-05-31 |

## 2. テーブル概要

### 2.1 概要・目的
システムログテーブル（SYS_SystemLog）は、システム全体の動作ログを管理するシステムテーブルです。アプリケーションログ、エラーログ、パフォーマンスログ、セキュリティログなどを統合的に記録し、システム監視、障害対応、セキュリティ監査の基盤となります。ログレベル別の分類や検索機能により、効率的な運用監視と問題解決を支援します。

### 2.2 関連API
- [API-021](../api/specs/API仕様書_API-021.md) - システムログ管理API

### 2.3 関連バッチ
- [BATCH-014](../batch/specs/バッチ定義書_BATCH-014.md) - ログクリーンアップバッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | log_id | ログID | VARCHAR | 50 | × | ○ | - | - | ログを一意に識別するID |
| 2 | log_level | ログレベル | VARCHAR | 20 | × | - | - | - | ログレベル（ERROR/WARN/INFO/DEBUG） |
| 3 | log_category | ログカテゴリ | VARCHAR | 50 | × | - | - | - | ログカテゴリ（APPLICATION/SECURITY/PERFORMANCE等） |
| 4 | occurred_at | 発生日時 | TIMESTAMP | - | × | - | - | - | ログ発生日時 |
| 5 | application_name | アプリケーション名 | VARCHAR | 100 | × | - | - | - | ログを出力したアプリケーション名 |
| 6 | module_name | モジュール名 | VARCHAR | 100 | ○ | - | - | NULL | ログを出力したモジュール名 |
| 7 | function_name | 機能名 | VARCHAR | 100 | ○ | - | - | NULL | ログを出力した機能名 |
| 8 | user_id | ユーザーID | VARCHAR | 50 | ○ | - | - | NULL | 操作を行ったユーザーID |
| 9 | session_id | セッションID | VARCHAR | 100 | ○ | - | - | NULL | セッションID |
| 10 | ip_address | IPアドレス | VARCHAR | 45 | ○ | - | - | NULL | クライアントのIPアドレス |
| 11 | user_agent | ユーザーエージェント | TEXT | - | ○ | - | - | NULL | ブラウザ情報 |
| 12 | request_url | リクエストURL | TEXT | - | ○ | - | - | NULL | リクエストURL |
| 13 | http_method | HTTPメソッド | VARCHAR | 10 | ○ | - | - | NULL | HTTPメソッド（GET/POST/PUT/DELETE等） |
| 14 | response_code | レスポンスコード | INTEGER | - | ○ | - | - | NULL | HTTPレスポンスコード |
| 15 | processing_time | 処理時間 | INTEGER | - | ○ | - | - | NULL | 処理時間（ミリ秒） |
| 16 | message | メッセージ | TEXT | - | × | - | - | - | ログメッセージ |
| 17 | details | 詳細情報 | TEXT | - | ○ | - | - | NULL | 詳細情報（JSON形式） |
| 18 | error_code | エラーコード | VARCHAR | 20 | ○ | - | - | NULL | エラーコード |
| 19 | stack_trace | スタックトレース | TEXT | - | ○ | - | - | NULL | エラー時のスタックトレース |
| 20 | related_log_id | 関連ログID | VARCHAR | 50 | ○ | - | - | NULL | 関連するログのID |
| 21 | tags | タグ | VARCHAR | 500 | ○ | - | - | NULL | 検索用タグ（カンマ区切り） |
| 22 | severity | 重要度 | INTEGER | - | × | - | - | 1 | 重要度（1:低 ～ 5:高） |
| 23 | is_notified | 通知フラグ | BOOLEAN | - | × | - | - | FALSE | 管理者通知済みかどうか |
| 24 | is_archived | アーカイブフラグ | BOOLEAN | - | × | - | - | FALSE | アーカイブ済みかどうか |
| 25 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | log_id | 主キー |
| idx_log_level | INDEX | log_level | ログレベルでの検索用 |
| idx_log_category | INDEX | log_category | ログカテゴリでの検索用 |
| idx_occurred_at | INDEX | occurred_at | 発生日時での検索用 |
| idx_application_name | INDEX | application_name | アプリケーション名での検索用 |
| idx_user_id | INDEX | user_id | ユーザーIDでの検索用 |
| idx_ip_address | INDEX | ip_address | IPアドレスでの検索用 |
| idx_response_code | INDEX | response_code | レスポンスコードでの検索用 |
| idx_severity | INDEX | severity | 重要度での検索用 |
| idx_archived | INDEX | is_archived | アーカイブフラグでの検索用 |
| idx_composite | INDEX | log_level, occurred_at, application_name | 複合検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_system_log | PRIMARY KEY | log_id | 主キー制約 |
| chk_log_level | CHECK | log_level | log_level IN ('ERROR', 'WARN', 'INFO', 'DEBUG') |
| chk_log_category | CHECK | log_category | log_category IN ('APPLICATION', 'SECURITY', 'PERFORMANCE', 'SYSTEM', 'AUDIT') |
| chk_http_method | CHECK | http_method | http_method IN ('GET', 'POST', 'PUT', 'DELETE', 'PATCH') |
| chk_response_code | CHECK | response_code | response_code IS NULL OR (response_code >= 100 AND response_code < 600) |
| chk_processing_time | CHECK | processing_time | processing_time IS NULL OR processing_time >= 0 |
| chk_severity | CHECK | severity | severity >= 1 AND severity <= 5 |

## 4. リレーション

### 4.1 親テーブル
このテーブルには親テーブルはありません（ログの独立性を保つため）。

### 4.2 子テーブル
このテーブルには子テーブルはありません。

## 5. データ仕様

### 5.1 ログレベル定義
| レベル | 説明 | 用途 |
|--------|------|------|
| ERROR | システムエラー、例外発生 | 緊急対応が必要なエラー |
| WARN | 警告、注意が必要な事象 | 監視が必要な警告 |
| INFO | 一般的な情報、正常な処理 | 通常の動作ログ |
| DEBUG | デバッグ情報、詳細な処理内容 | 開発・デバッグ用 |

### 5.2 ログカテゴリ定義
| カテゴリ | 説明 | 用途 |
|----------|------|------|
| APPLICATION | アプリケーション動作ログ | 業務処理の記録 |
| SECURITY | セキュリティ関連ログ | 認証・認可・不正アクセス |
| PERFORMANCE | パフォーマンス関連ログ | 性能監視・最適化 |
| SYSTEM | システム動作ログ | インフラ・システム動作 |
| AUDIT | 監査ログ | コンプライアンス対応 |

### 5.3 重要度定義
| 重要度 | 説明 | 対応 |
|--------|------|------|
| 1 | 低（通常の情報ログ） | 通常監視 |
| 2 | やや低（軽微な警告） | 定期確認 |
| 3 | 中（注意が必要な警告） | 注意深い監視 |
| 4 | 高（重要なエラー） | 管理者通知 |
| 5 | 最高（緊急対応が必要） | 即座に対応 |

### 5.4 データ例
```sql
-- 正常ログイン
INSERT INTO SYS_SystemLog (
    log_id, log_level, log_category, occurred_at,
    application_name, user_id, ip_address, http_method,
    response_code, processing_time, message, severity
) VALUES (
    'LOG_20250531_001',
    'INFO',
    'SECURITY',
    '2025-05-31 10:00:00',
    'skill-report-web',
    'USR_001',
    '192.168.1.100',
    'POST',
    200,
    150,
    'ユーザーログイン成功',
    1
);

-- 不正ログイン試行
INSERT INTO SYS_SystemLog (
    log_id, log_level, log_category, occurred_at,
    application_name, ip_address, http_method,
    response_code, processing_time, message, severity,
    error_code
) VALUES (
    'LOG_20250531_002',
    'ERROR',
    'SECURITY',
    '2025-05-31 10:05:00',
    'skill-report-web',
    '192.168.1.200',
    'POST',
    401,
    50,
    '不正なログイン試行を検知',
    4,
    'AUTH_FAILED'
);

-- パフォーマンス警告
INSERT INTO SYS_SystemLog (
    log_id, log_level, log_category, occurred_at,
    application_name, user_id, ip_address, http_method,
    response_code, processing_time, message, severity
) VALUES (
    'LOG_20250531_003',
    'WARN',
    'PERFORMANCE',
    '2025-05-31 10:10:00',
    'skill-report-web',
    'USR_002',
    '192.168.1.101',
    'GET',
    200,
    5000,
    'レスポンス時間が閾値を超過',
    3
);
```

### 5.5 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 0件 | ログテーブルのため |
| 日次増加件数 | 10,000件 | 通常運用時 |
| 年間想定件数 | 3,650,000件 | 365日分 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：RANGE
- パーティション条件：occurred_at（月単位）

### 6.3 アーカイブ
- ERRORログ：1年間保持後アーカイブ
- WARNログ：6ヶ月間保持後アーカイブ
- INFOログ：3ヶ月間保持後アーカイブ
- DEBUGログ：1ヶ月間保持後アーカイブ

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| INSERT | 極高 | - | ログ出力 |
| SELECT | 高 | log_level, occurred_at | ログ検索 |
| SELECT | 高 | user_id, occurred_at | ユーザー別ログ |
| SELECT | 中 | ip_address | IPアドレス別検索 |
| SELECT | 中 | severity >= 4 | 重要ログ検索 |
| UPDATE | 低 | is_archived | アーカイブ処理 |

### 7.2 パフォーマンス要件
- INSERT：5ms以内
- SELECT：100ms以内（通常検索）
- SELECT：500ms以内（複雑検索）

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| log_admin | ○ | × | ○ | × | ログ管理者 |
| security_admin | ○ | × | × | × | セキュリティ管理者 |
| application | × | ○ | × | × | アプリケーション |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含む可能性（IPアドレス、ユーザーID）
- 機密情報：含む（システム内部情報）
- 暗号化：必要（詳細情報、スタックトレース）

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存ログシステム
- 移行方法：ログファイル解析・変換
- 移行タイミング：システム移行時

### 9.2 移行スクリプト例
```sql
-- 既存ログの移行（例）
INSERT INTO SYS_SystemLog (
    log_id, log_level, log_category, occurred_at,
    application_name, message, severity
)
SELECT 
    CONCAT('LOG_', DATE_FORMAT(log_time, '%Y%m%d'), '_', LPAD(ROW_NUMBER() OVER (ORDER BY log_time), 6, '0')),
    CASE 
        WHEN level = 'ERROR' THEN 'ERROR'
        WHEN level = 'WARN' THEN 'WARN'
        WHEN level = 'INFO' THEN 'INFO'
        ELSE 'DEBUG'
    END,
    'APPLICATION',
    log_time,
    'skill-report-web',
    message,
    CASE 
        WHEN level = 'ERROR' THEN 4
        WHEN level = 'WARN' THEN 3
        ELSE 1
    END
FROM old_application_log
WHERE log_time >= '2025-01-01';
```

### 9.3 DDL
```sql
CREATE TABLE SYS_SystemLog (
    log_id VARCHAR(50) NOT NULL,
    log_level VARCHAR(20) NOT NULL,
    log_category VARCHAR(50) NOT NULL,
    occurred_at TIMESTAMP NOT NULL,
    application_name VARCHAR(100) NOT NULL,
    module_name VARCHAR(100) NULL,
    function_name VARCHAR(100) NULL,
    user_id VARCHAR(50) NULL,
    session_id VARCHAR(100) NULL,
    ip_address VARCHAR(45) NULL,
    user_agent TEXT NULL,
    request_url TEXT NULL,
    http_method VARCHAR(10) NULL,
    response_code INTEGER NULL,
    processing_time INTEGER NULL,
    message TEXT NOT NULL,
    details TEXT NULL,
    error_code VARCHAR(20) NULL,
    stack_trace TEXT NULL,
    related_log_id VARCHAR(50) NULL,
    tags VARCHAR(500) NULL,
    severity INTEGER NOT NULL DEFAULT 1,
    is_notified BOOLEAN NOT NULL DEFAULT FALSE,
    is_archived BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (log_id),
    INDEX idx_log_level (log_level),
    INDEX idx_log_category (log_category),
    INDEX idx_occurred_at (occurred_at),
    INDEX idx_application_name (application_name),
    INDEX idx_user_id (user_id),
    INDEX idx_ip_address (ip_address),
    INDEX idx_response_code (response_code),
    INDEX idx_severity (severity),
    INDEX idx_archived (is_archived),
    INDEX idx_composite (log_level, occurred_at, application_name),
    CONSTRAINT chk_log_level CHECK (log_level IN ('ERROR', 'WARN', 'INFO', 'DEBUG')),
    CONSTRAINT chk_log_category CHECK (log_category IN ('APPLICATION', 'SECURITY', 'PERFORMANCE', 'SYSTEM', 'AUDIT')),
    CONSTRAINT chk_http_method CHECK (http_method IS NULL OR http_method IN ('GET', 'POST', 'PUT', 'DELETE', 'PATCH')),
    CONSTRAINT chk_response_code CHECK (response_code IS NULL OR (response_code >= 100 AND response_code < 600)),
    CONSTRAINT chk_processing_time CHECK (processing_time IS NULL OR processing_time >= 0),
    CONSTRAINT chk_severity CHECK (severity >= 1 AND severity <= 5)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
PARTITION BY RANGE (YEAR(occurred_at) * 100 + MONTH(occurred_at)) (
    PARTITION p202501 VALUES LESS THAN (202502),
    PARTITION p202502 VALUES LESS THAN (202503),
    PARTITION p202503 VALUES LESS THAN (202504),
    PARTITION p202504 VALUES LESS THAN (202505),
    PARTITION p202505 VALUES LESS THAN (202506),
    PARTITION p202506 VALUES LESS THAN (202507),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

## 10. 特記事項

1. **ログ独立性**: 外部キー制約なしでログの独立性を保持
2. **高頻度INSERT**: 大量ログ出力に対応した設計
3. **自動通知**: 重要度4以上で管理者自動通知
4. **パーティション**: 月単位パーティションで性能向上
5. **アーカイブ**: ログレベル別の保持期間設定
6. **検索最適化**: 複合インデックスで高速検索
7. **セキュリティ**: 機密情報の暗号化対応
8. **監視連携**: 外部監視システムとの連携
9. **ログローテーション**: 定期的なログクリーンアップ
10. **障害対応**: ログ基盤での障害分析支援
11. **コンプライアンス**: 監査要件への対応
12. **リアルタイム監視**: 重要ログのリアルタイム検知

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-31 | システムアーキテクト | 初版作成（システムログ管理対応） |
