# テーブル定義書：監査ログ (SYS_AuditLog)

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-014 |
| **テーブル名** | SYS_AuditLog |
| **論理名** | 監査ログ |
| **カテゴリ** | システム系 |
| **優先度** | 最高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-05-29 |
| **最終更新日** | 2025-05-31 |

## 2. テーブル概要

### 2.1 概要・目的
監査ログテーブル（SYS_AuditLog）は、システム内で発生した全ての重要な操作を記録します。データの変更履歴、アクセス履歴、セキュリティイベント等を追跡し、コンプライアンス要件への対応とセキュリティ監視を支援します。

### 2.2 関連API
- [API-301](../api/specs/API仕様書_API-301.md) - 監査ログ検索API
- [API-302](../api/specs/API仕様書_API-302.md) - 監査ログ出力API

### 2.3 関連バッチ
- [BATCH-012](../batch/specs/バッチ定義書_BATCH-012.md) - 監査ログアーカイブバッチ
- [BATCH-013](../batch/specs/バッチ定義書_BATCH-013.md) - 監査ログ分析バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | log_id | ログID | VARCHAR | 20 | × | ○ | - | - | 監査ログを一意に識別するID |
| 2 | tenant_id | テナントID | VARCHAR | 50 | ○ | - | ○ | NULL | 操作対象のテナントID |
| 3 | user_id | ユーザーID | VARCHAR | 50 | ○ | - | ○ | NULL | 操作実行者のユーザーID |
| 4 | employee_id | 社員ID | VARCHAR | 20 | ○ | - | ○ | NULL | 操作実行者の社員ID |
| 5 | session_id | セッションID | VARCHAR | 100 | ○ | - | - | NULL | 操作時のセッションID |
| 6 | action_type | アクションタイプ | VARCHAR | 50 | × | - | - | - | 操作の種類（CREATE/UPDATE/DELETE/LOGIN等） |
| 7 | resource_type | リソースタイプ | VARCHAR | 50 | × | - | - | - | 操作対象のリソース種別 |
| 8 | resource_id | リソースID | VARCHAR | 50 | ○ | - | - | NULL | 操作対象のリソースID |
| 9 | table_name | テーブル名 | VARCHAR | 100 | ○ | - | - | NULL | 操作対象のテーブル名 |
| 10 | record_id | レコードID | VARCHAR | 50 | ○ | - | - | NULL | 操作対象のレコードID |
| 11 | operation_result | 操作結果 | VARCHAR | 20 | × | - | - | - | 操作の成功/失敗（SUCCESS/FAILURE/ERROR） |
| 12 | http_method | HTTPメソッド | VARCHAR | 10 | ○ | - | - | NULL | HTTP操作の場合のメソッド |
| 13 | request_url | リクエストURL | VARCHAR | 500 | ○ | - | - | NULL | HTTP操作の場合のURL |
| 14 | request_parameters | リクエストパラメータ | JSON | - | ○ | - | - | NULL | リクエストパラメータ（JSON形式） |
| 15 | old_values | 変更前値 | JSON | - | ○ | - | - | NULL | データ変更前の値（JSON形式） |
| 16 | new_values | 変更後値 | JSON | - | ○ | - | - | NULL | データ変更後の値（JSON形式） |
| 17 | ip_address | IPアドレス | VARCHAR | 45 | ○ | - | - | NULL | 操作元のIPアドレス |
| 18 | user_agent | ユーザーエージェント | VARCHAR | 500 | ○ | - | - | NULL | 操作時のユーザーエージェント |
| 19 | referer | リファラー | VARCHAR | 500 | ○ | - | - | NULL | 操作時のリファラー |
| 20 | response_status | レスポンスステータス | INTEGER | - | ○ | - | - | NULL | HTTPレスポンスステータスコード |
| 21 | response_time | レスポンス時間 | INTEGER | - | ○ | - | - | NULL | 処理時間（ミリ秒） |
| 22 | error_message | エラーメッセージ | TEXT | - | ○ | - | - | NULL | エラー発生時のメッセージ |
| 23 | stack_trace | スタックトレース | TEXT | - | ○ | - | - | NULL | エラー発生時のスタックトレース |
| 24 | severity_level | 重要度レベル | VARCHAR | 10 | × | - | - | 'INFO' | ログの重要度（CRITICAL/ERROR/WARN/INFO/DEBUG） |
| 25 | category | カテゴリ | VARCHAR | 50 | × | - | - | - | ログのカテゴリ（SECURITY/DATA/ACCESS/SYSTEM等） |
| 26 | tags | タグ | VARCHAR | 200 | ○ | - | - | NULL | ログの分類タグ（カンマ区切り） |
| 27 | correlation_id | 相関ID | VARCHAR | 100 | ○ | - | - | NULL | 関連する処理の相関ID |
| 28 | parent_log_id | 親ログID | VARCHAR | 20 | ○ | - | ○ | NULL | 関連する親ログのID |
| 29 | additional_data | 追加データ | JSON | - | ○ | - | - | NULL | その他の追加情報（JSON形式） |
| 30 | retention_period | 保持期間 | INTEGER | - | × | - | - | 2555 | ログの保持期間（日数） |
| 31 | is_sensitive | 機密フラグ | BOOLEAN | - | × | - | - | FALSE | 機密情報を含むかどうか |
| 32 | is_archived | アーカイブフラグ | BOOLEAN | - | × | - | - | FALSE | アーカイブ済みかどうか |
| 33 | archived_at | アーカイブ日時 | TIMESTAMP | - | ○ | - | - | NULL | アーカイブされた日時 |
| 34 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | log_id | 主キー |
| idx_tenant_user | INDEX | tenant_id, user_id | テナント・ユーザー検索用 |
| idx_user | INDEX | user_id | ユーザー検索用 |
| idx_employee | INDEX | employee_id | 社員検索用 |
| idx_action_type | INDEX | action_type | アクションタイプ検索用 |
| idx_resource | INDEX | resource_type, resource_id | リソース検索用 |
| idx_table_record | INDEX | table_name, record_id | テーブル・レコード検索用 |
| idx_result | INDEX | operation_result | 操作結果検索用 |
| idx_severity | INDEX | severity_level | 重要度検索用 |
| idx_category | INDEX | category | カテゴリ検索用 |
| idx_ip | INDEX | ip_address | IPアドレス検索用 |
| idx_created | INDEX | created_at | 作成日時検索用 |
| idx_correlation | INDEX | correlation_id | 相関ID検索用 |
| idx_parent | INDEX | parent_log_id | 親ログ検索用 |
| idx_archived | INDEX | is_archived | アーカイブフラグ検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_audit_log | PRIMARY KEY | log_id | 主キー制約 |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_user | FOREIGN KEY | user_id | MST_UserAuth.user_id |
| fk_employee | FOREIGN KEY | employee_id | MST_Employee.employee_id |
| fk_parent_log | FOREIGN KEY | parent_log_id | SYS_AuditLog.log_id |
| chk_operation_result | CHECK | operation_result | operation_result IN ('SUCCESS', 'FAILURE', 'ERROR') |
| chk_severity_level | CHECK | severity_level | severity_level IN ('CRITICAL', 'ERROR', 'WARN', 'INFO', 'DEBUG') |
| chk_retention_period | CHECK | retention_period | retention_period > 0 |
| chk_response_status | CHECK | response_status | response_status IS NULL OR (response_status >= 100 AND response_status <= 599) |
| chk_response_time | CHECK | response_time | response_time IS NULL OR response_time >= 0 |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Tenant | tenant_id | 1:N | テナント情報 |
| MST_UserAuth | user_id | 1:N | ユーザー情報 |
| MST_Employee | employee_id | 1:N | 社員情報 |
| SYS_AuditLog | parent_log_id | 1:N | 親ログ（自己参照） |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| SYS_AuditLog | parent_log_id | 1:N | 子ログ（自己参照） |

## 5. データ仕様

### 5.1 データ例
```sql
INSERT INTO SYS_AuditLog (
    log_id, tenant_id, user_id, employee_id,
    action_type, resource_type, resource_id,
    table_name, record_id, operation_result,
    http_method, request_url, old_values, new_values,
    ip_address, user_agent, severity_level, category
) VALUES (
    'LOG_001',
    'TENANT_001',
    'user001',
    'EMP_001',
    'UPDATE',
    'SKILL_RECORD',
    'REC_001',
    'TRN_SkillRecord',
    'REC_001',
    'SUCCESS',
    'PUT',
    '/api/v1/skill-records/REC_001',
    '{"self_evaluation": 2, "supervisor_evaluation": null}',
    '{"self_evaluation": 3, "supervisor_evaluation": 3}',
    '192.168.1.100',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'INFO',
    'DATA'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 0件 | 新規システム |
| 日間増加件数 | 100,000件 | 全操作ログ |
| 月間増加件数 | 3,000,000件 | 想定値 |
| 年間増加件数 | 36,000,000件 | 想定値 |
| 5年後想定件数 | 180,000,000件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日1:00実行
- 週次バックアップ：毎週日曜日1:00実行
- 月次バックアップ：毎月1日1:00実行

### 6.2 パーティション
- パーティション種別：RANGE
- パーティション条件：created_at（月単位）

### 6.3 アーカイブ
- アーカイブ条件：作成日から7年経過
- アーカイブ先：長期保存ストレージ

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| INSERT | 最高 | - | 全操作でログ挿入 |
| SELECT | 高 | user_id, created_at | ユーザー別ログ検索 |
| SELECT | 高 | resource_type, resource_id | リソース別ログ検索 |
| SELECT | 中 | action_type, created_at | アクション別ログ検索 |
| SELECT | 中 | severity_level | 重要度別ログ検索 |
| SELECT | 低 | ip_address | IPアドレス別検索 |

### 7.2 パフォーマンス要件
- INSERT：5ms以内
- SELECT：50ms以内
- UPDATE：使用しない
- DELETE：使用しない（論理削除のみ）

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | × | × | システム管理者 |
| security_admin | ○ | × | × | × | セキュリティ管理者 |
| audit_admin | ○ | × | × | × | 監査管理者 |
| system | ○ | ○ | × | × | システム自動処理 |
| readonly | × | × | × | × | 参照不可 |

### 8.2 データ保護
- 個人情報：含む（操作者情報）
- 機密情報：含む（操作内容）
- 暗号化：必要（機密フラグがTRUEの場合）

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存監査ログシステム
- 移行方法：バッチ処理による段階的移行
- 移行タイミング：システム移行後

### 9.2 DDL
```sql
CREATE TABLE SYS_AuditLog (
    log_id VARCHAR(20) NOT NULL,
    tenant_id VARCHAR(50) NULL,
    user_id VARCHAR(50) NULL,
    employee_id VARCHAR(20) NULL,
    session_id VARCHAR(100) NULL,
    action_type VARCHAR(50) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id VARCHAR(50) NULL,
    table_name VARCHAR(100) NULL,
    record_id VARCHAR(50) NULL,
    operation_result VARCHAR(20) NOT NULL,
    http_method VARCHAR(10) NULL,
    request_url VARCHAR(500) NULL,
    request_parameters JSON NULL,
    old_values JSON NULL,
    new_values JSON NULL,
    ip_address VARCHAR(45) NULL,
    user_agent VARCHAR(500) NULL,
    referer VARCHAR(500) NULL,
    response_status INTEGER NULL,
    response_time INTEGER NULL,
    error_message TEXT NULL,
    stack_trace TEXT NULL,
    severity_level VARCHAR(10) NOT NULL DEFAULT 'INFO',
    category VARCHAR(50) NOT NULL,
    tags VARCHAR(200) NULL,
    correlation_id VARCHAR(100) NULL,
    parent_log_id VARCHAR(20) NULL,
    additional_data JSON NULL,
    retention_period INTEGER NOT NULL DEFAULT 2555,
    is_sensitive BOOLEAN NOT NULL DEFAULT FALSE,
    is_archived BOOLEAN NOT NULL DEFAULT FALSE,
    archived_at TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (log_id),
    INDEX idx_tenant_user (tenant_id, user_id),
    INDEX idx_user (user_id),
    INDEX idx_employee (employee_id),
    INDEX idx_action_type (action_type),
    INDEX idx_resource (resource_type, resource_id),
    INDEX idx_table_record (table_name, record_id),
    INDEX idx_result (operation_result),
    INDEX idx_severity (severity_level),
    INDEX idx_category (category),
    INDEX idx_ip (ip_address),
    INDEX idx_created (created_at),
    INDEX idx_correlation (correlation_id),
    INDEX idx_parent (parent_log_id),
    INDEX idx_archived (is_archived),
    CONSTRAINT fk_audit_log_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_audit_log_user FOREIGN KEY (user_id) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_audit_log_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(employee_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_audit_log_parent FOREIGN KEY (parent_log_id) REFERENCES SYS_AuditLog(log_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT chk_audit_log_operation_result CHECK (operation_result IN ('SUCCESS', 'FAILURE', 'ERROR')),
    CONSTRAINT chk_audit_log_severity_level CHECK (severity_level IN ('CRITICAL', 'ERROR', 'WARN', 'INFO', 'DEBUG')),
    CONSTRAINT chk_audit_log_retention_period CHECK (retention_period > 0),
    CONSTRAINT chk_audit_log_response_status CHECK (response_status IS NULL OR (response_status >= 100 AND response_status <= 599)),
    CONSTRAINT chk_audit_log_response_time CHECK (response_time IS NULL OR response_time >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p2026 VALUES LESS THAN (2027),
    PARTITION p2027 VALUES LESS THAN (2028),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

## 10. 特記事項

1. 全ての重要な操作を自動的に記録（INSERT専用テーブル）
2. 機密情報は暗号化して保存し、アクセス制御を厳格化
3. パーティション設計による大量ログデータの効率的管理
4. 相関IDによる関連操作の追跡機能
5. 重要度レベルによるログの優先度管理
6. 法的要件に対応した長期保存（7年間）
7. リアルタイム監視とアラート機能との連携
8. データ変更の前後値を完全記録
9. セキュリティイベントの特別な追跡機能
10. 定期的なアーカイブによる性能維持

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-29 | システムアーキテクト | 初版作成 |
| 1.1 | 2025-05-31 | システムアーキテクト | 新フォーマットに変更、詳細情報追加 |
