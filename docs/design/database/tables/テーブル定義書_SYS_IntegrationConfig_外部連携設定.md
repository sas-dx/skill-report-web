# テーブル定義書_SYS_IntegrationConfig_外部連携設定

## 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | SYS_IntegrationConfig |
| 論理名 | 外部連携設定 |
| 用途 | 外部システムとの連携設定を管理 |
| カテゴリ | システム系 |
| 作成日 | 2025-05-31 |
| 最終更新日 | 2025-05-31 |

## 概要

Slack、Teams、LINE WORKS等の外部システムとの連携に必要な設定情報（API キー、エンドポイント、認証情報等）を安全に管理するテーブル。

## カラム定義

| No | カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト値 | 主キー | 外部キー | 説明 |
|----|----------|--------|----------|------|------|-------------|--------|----------|------|
| 1 | config_id | 設定ID | BIGINT | - | NOT NULL | AUTO_INCREMENT | ○ | - | 連携設定の一意識別子 |
| 2 | tenant_id | テナントID | VARCHAR | 50 | NOT NULL | - | - | MST_Tenant.tenant_id | 対象テナントID |
| 3 | integration_type | 連携タイプ | VARCHAR | 50 | NOT NULL | - | - | - | 連携システム種別 |
| 4 | integration_name | 連携名 | VARCHAR | 100 | NOT NULL | - | - | - | 連携設定の表示名 |
| 5 | service_provider | サービスプロバイダー | VARCHAR | 50 | NOT NULL | - | - | - | サービス提供者名 |
| 6 | api_endpoint | APIエンドポイント | VARCHAR | 500 | NULL | NULL | - | - | API接続先URL |
| 7 | api_version | APIバージョン | VARCHAR | 20 | NULL | NULL | - | - | 使用するAPIバージョン |
| 8 | auth_type | 認証タイプ | VARCHAR | 30 | NOT NULL | - | - | - | 認証方式 |
| 9 | api_key_encrypted | APIキー（暗号化） | TEXT | - | NULL | NULL | - | - | 暗号化されたAPIキー |
| 10 | client_id | クライアントID | VARCHAR | 200 | NULL | NULL | - | - | OAuth用クライアントID |
| 11 | client_secret_encrypted | クライアントシークレット（暗号化） | TEXT | - | NULL | NULL | - | - | 暗号化されたクライアントシークレット |
| 12 | access_token_encrypted | アクセストークン（暗号化） | TEXT | - | NULL | NULL | - | - | 暗号化されたアクセストークン |
| 13 | refresh_token_encrypted | リフレッシュトークン（暗号化） | TEXT | - | NULL | NULL | - | - | 暗号化されたリフレッシュトークン |
| 14 | token_expires_at | トークン有効期限 | TIMESTAMP | - | NULL | NULL | - | - | アクセストークンの有効期限 |
| 15 | webhook_url | Webhook URL | VARCHAR | 500 | NULL | NULL | - | - | Webhook受信用URL |
| 16 | webhook_secret_encrypted | Webhookシークレット（暗号化） | TEXT | - | NULL | NULL | - | - | 暗号化されたWebhookシークレット |
| 17 | connection_timeout | 接続タイムアウト(秒) | INT | - | NULL | 30 | - | - | 接続タイムアウト時間 |
| 18 | read_timeout | 読み取りタイムアウト(秒) | INT | - | NULL | 60 | - | - | 読み取りタイムアウト時間 |
| 19 | retry_count | リトライ回数 | INT | - | NULL | 3 | - | - | 失敗時のリトライ回数 |
| 20 | retry_interval | リトライ間隔(秒) | INT | - | NULL | 5 | - | - | リトライ間隔 |
| 21 | rate_limit_per_minute | 分間レート制限 | INT | - | NULL | NULL | - | - | 1分間あたりのAPI呼び出し制限 |
| 22 | rate_limit_per_hour | 時間レート制限 | INT | - | NULL | NULL | - | - | 1時間あたりのAPI呼び出し制限 |
| 23 | custom_headers_json | カスタムヘッダー | JSON | - | NULL | NULL | - | - | 追加HTTPヘッダー（JSON形式） |
| 24 | config_json | 設定詳細 | JSON | - | NULL | NULL | - | - | サービス固有の設定（JSON形式） |
| 25 | is_active | 有効フラグ | BOOLEAN | - | NOT NULL | TRUE | - | - | 設定の有効/無効 |
| 26 | is_test_mode | テストモード | BOOLEAN | - | NOT NULL | FALSE | - | - | テストモードフラグ |
| 27 | last_connection_test | 最終接続テスト日時 | TIMESTAMP | - | NULL | NULL | - | - | 最後に接続テストを実行した日時 |
| 28 | last_connection_status | 最終接続ステータス | VARCHAR | 20 | NULL | NULL | - | - | 最後の接続テスト結果 |
| 29 | error_count | エラー回数 | INT | - | NULL | 0 | - | - | 連続エラー回数 |
| 30 | last_error_message | 最終エラーメッセージ | TEXT | - | NULL | NULL | - | - | 最後に発生したエラーメッセージ |
| 31 | last_error_at | 最終エラー日時 | TIMESTAMP | - | NULL | NULL | - | - | 最後にエラーが発生した日時 |
| 32 | encryption_key_id | 暗号化キーID | VARCHAR | 50 | NULL | NULL | - | - | 暗号化に使用したキーID |
| 33 | notes | 備考 | TEXT | - | NULL | NULL | - | - | 設定に関する備考 |
| 34 | created_at | 作成日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP | - | - | レコード作成日時 |
| 35 | updated_at | 更新日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | レコード更新日時 |
| 36 | created_by | 作成者 | VARCHAR | 50 | NOT NULL | - | - | - | レコード作成者 |
| 37 | updated_by | 更新者 | VARCHAR | 50 | NOT NULL | - | - | - | レコード更新者 |

## 制約

### 主キー制約
- PRIMARY KEY (config_id)

### 外部キー制約
- FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id)

### ユニーク制約
- UNIQUE KEY uk_tenant_integration (tenant_id, integration_type, integration_name)

### チェック制約
- CHECK (integration_type IN ('SLACK', 'TEAMS', 'LINE_WORKS', 'EMAIL', 'WEBHOOK', 'API', 'SSO', 'LDAP'))
- CHECK (auth_type IN ('API_KEY', 'OAUTH2', 'BEARER_TOKEN', 'BASIC_AUTH', 'CUSTOM'))
- CHECK (last_connection_status IN ('SUCCESS', 'FAILED', 'TIMEOUT', 'UNAUTHORIZED', 'NOT_TESTED'))
- CHECK (connection_timeout > 0)
- CHECK (read_timeout > 0)
- CHECK (retry_count >= 0)
- CHECK (retry_interval >= 0)
- CHECK (error_count >= 0)

## インデックス

| インデックス名 | 種別 | 対象カラム | 説明 |
|---------------|------|------------|------|
| idx_tenant_integration | BTREE | tenant_id, integration_type | テナント・連携タイプでの検索用 |
| idx_integration_type | BTREE | integration_type | 連携タイプでの検索用 |
| idx_is_active | BTREE | is_active | 有効フラグでの検索用 |
| idx_last_connection_test | BTREE | last_connection_test | 接続テスト日時での検索用 |
| idx_token_expires | BTREE | token_expires_at | トークン有効期限での検索用 |
| idx_created_at | BTREE | created_at | 作成日時での検索用 |

## DDL

```sql
CREATE TABLE SYS_IntegrationConfig (
    config_id BIGINT NOT NULL AUTO_INCREMENT COMMENT '設定ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    integration_type VARCHAR(50) NOT NULL COMMENT '連携タイプ',
    integration_name VARCHAR(100) NOT NULL COMMENT '連携名',
    service_provider VARCHAR(50) NOT NULL COMMENT 'サービスプロバイダー',
    api_endpoint VARCHAR(500) COMMENT 'APIエンドポイント',
    api_version VARCHAR(20) COMMENT 'APIバージョン',
    auth_type VARCHAR(30) NOT NULL COMMENT '認証タイプ',
    api_key_encrypted TEXT COMMENT 'APIキー（暗号化）',
    client_id VARCHAR(200) COMMENT 'クライアントID',
    client_secret_encrypted TEXT COMMENT 'クライアントシークレット（暗号化）',
    access_token_encrypted TEXT COMMENT 'アクセストークン（暗号化）',
    refresh_token_encrypted TEXT COMMENT 'リフレッシュトークン（暗号化）',
    token_expires_at TIMESTAMP COMMENT 'トークン有効期限',
    webhook_url VARCHAR(500) COMMENT 'Webhook URL',
    webhook_secret_encrypted TEXT COMMENT 'Webhookシークレット（暗号化）',
    connection_timeout INT DEFAULT 30 COMMENT '接続タイムアウト(秒)',
    read_timeout INT DEFAULT 60 COMMENT '読み取りタイムアウト(秒)',
    retry_count INT DEFAULT 3 COMMENT 'リトライ回数',
    retry_interval INT DEFAULT 5 COMMENT 'リトライ間隔(秒)',
    rate_limit_per_minute INT COMMENT '分間レート制限',
    rate_limit_per_hour INT COMMENT '時間レート制限',
    custom_headers_json JSON COMMENT 'カスタムヘッダー',
    config_json JSON COMMENT '設定詳細',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '有効フラグ',
    is_test_mode BOOLEAN NOT NULL DEFAULT FALSE COMMENT 'テストモード',
    last_connection_test TIMESTAMP COMMENT '最終接続テスト日時',
    last_connection_status VARCHAR(20) COMMENT '最終接続ステータス',
    error_count INT DEFAULT 0 COMMENT 'エラー回数',
    last_error_message TEXT COMMENT '最終エラーメッセージ',
    last_error_at TIMESTAMP COMMENT '最終エラー日時',
    encryption_key_id VARCHAR(50) COMMENT '暗号化キーID',
    notes TEXT COMMENT '備考',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT '作成者',
    updated_by VARCHAR(50) NOT NULL COMMENT '更新者',
    
    PRIMARY KEY (config_id),
    UNIQUE KEY uk_tenant_integration (tenant_id, integration_type, integration_name),
    
    CONSTRAINT fk_integration_config_tenant 
        FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id),
    
    CONSTRAINT chk_integration_type 
        CHECK (integration_type IN ('SLACK', 'TEAMS', 'LINE_WORKS', 'EMAIL', 'WEBHOOK', 'API', 'SSO', 'LDAP')),
    CONSTRAINT chk_auth_type 
        CHECK (auth_type IN ('API_KEY', 'OAUTH2', 'BEARER_TOKEN', 'BASIC_AUTH', 'CUSTOM')),
    CONSTRAINT chk_connection_status 
        CHECK (last_connection_status IN ('SUCCESS', 'FAILED', 'TIMEOUT', 'UNAUTHORIZED', 'NOT_TESTED')),
    CONSTRAINT chk_connection_timeout 
        CHECK (connection_timeout > 0),
    CONSTRAINT chk_read_timeout 
        CHECK (read_timeout > 0),
    CONSTRAINT chk_retry_count 
        CHECK (retry_count >= 0),
    CONSTRAINT chk_retry_interval 
        CHECK (retry_interval >= 0),
    CONSTRAINT chk_error_count 
        CHECK (error_count >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='外部連携設定管理テーブル';

-- インデックス作成
CREATE INDEX idx_tenant_integration ON SYS_IntegrationConfig(tenant_id, integration_type);
CREATE INDEX idx_integration_type ON SYS_IntegrationConfig(integration_type);
CREATE INDEX idx_is_active ON SYS_IntegrationConfig(is_active);
CREATE INDEX idx_last_connection_test ON SYS_IntegrationConfig(last_connection_test);
CREATE INDEX idx_token_expires ON SYS_IntegrationConfig(token_expires_at);
CREATE INDEX idx_created_at ON SYS_IntegrationConfig(created_at);
```

## 関連テーブル

| テーブル名 | 関係 | 説明 |
|------------|------|------|
| MST_Tenant | 親 | テナント基本情報 |
| SYS_NotificationSettings | 関連 | 通知設定 |
| TRN_Notification | 関連 | 通知履歴 |
| SYS_SystemLog | 関連 | システムログ |
| SYS_AuditLog | 関連 | 監査ログ |

## 利用API

| API ID | API名 | 説明 |
|--------|-------|------|
| API-028 | 通知設定API | 外部連携設定管理 |
| API-029 | 通知送信API | 外部システム連携 |

## 利用バッチ

| バッチ ID | バッチ名 | 説明 |
|-----------|----------|------|
| BATCH-019-03 | 外部システム連携バッチ | 外部システムとの連携処理 |
| BATCH-019-05 | 通知設定検証バッチ | 連携設定の検証 |
| BATCH-407 | Slack連携同期バッチ | Slack連携処理 |
| BATCH-408 | Teams連携同期バッチ | Teams連携処理 |
| BATCH-409 | LINE WORKS連携同期バッチ | LINE WORKS連携処理 |

## 運用考慮事項

### セキュリティ
- 機密情報（APIキー、トークン等）は必ず暗号化して保存
- 暗号化キーの適切な管理とローテーション
- アクセス権限の厳格な制御
- 監査ログの記録

### パフォーマンス
- 接続プールの適切な設定
- レート制限の遵守
- タイムアウト設定の最適化
- 失敗時のリトライ戦略

### 可用性
- 接続状態の定期監視
- 自動復旧機能の実装
- フェイルオーバー機能
- 障害時の通知機能

### 運用
- 定期的な接続テストの実施
- トークンの自動更新機能
- 設定変更の履歴管理
- 障害時の迅速な対応

## データサンプル

```sql
-- Slack連携設定例
INSERT INTO SYS_IntegrationConfig (
    tenant_id, integration_type, integration_name, service_provider,
    api_endpoint, auth_type, api_key_encrypted,
    webhook_url, is_active, created_by, updated_by
) VALUES (
    'tenant001', 'SLACK', 'メイン通知チャンネル', 'Slack Technologies',
    'https://hooks.slack.com/services/', 'API_KEY', 'encrypted_api_key_here',
    'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX',
    TRUE, 'admin', 'admin'
);

-- Teams連携設定例
INSERT INTO SYS_IntegrationConfig (
    tenant_id, integration_type, integration_name, service_provider,
    api_endpoint, auth_type, client_id, client_secret_encrypted,
    is_active, created_by, updated_by
) VALUES (
    'tenant001', 'TEAMS', 'Teams通知', 'Microsoft Corporation',
    'https://graph.microsoft.com/v1.0/', 'OAUTH2', 'client_id_here', 'encrypted_secret_here',
    TRUE, 'admin', 'admin'
);

-- LINE WORKS連携設定例
INSERT INTO SYS_IntegrationConfig (
    tenant_id, integration_type, integration_name, service_provider,
    api_endpoint, auth_type, api_key_encrypted,
    is_active, created_by, updated_by
) VALUES (
    'tenant001', 'LINE_WORKS', 'LINE WORKS通知', 'LINE Corporation',
    'https://www.worksapis.com/v1.0/', 'API_KEY', 'encrypted_line_api_key',
    TRUE, 'admin', 'admin'
);
```

## 変更履歴

| 版数 | 変更日 | 変更者 | 変更内容 |
|------|--------|--------|----------|
| 1.0 | 2025-05-31 | システム管理者 | 初版作成 |
