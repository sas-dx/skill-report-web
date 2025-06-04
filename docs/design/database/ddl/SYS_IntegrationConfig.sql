-- ============================================
-- テーブル: SYS_IntegrationConfig
-- 論理名: 外部連携設定
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS SYS_IntegrationConfig;

CREATE TABLE SYS_IntegrationConfig (
    id VARCHAR(50) COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) COMMENT 'マルチテナント識別子',
    integration_key VARCHAR(100) COMMENT '連携設定の識別キー（例：slack_webhook、teams_connector等）',
    integration_name VARCHAR(200) COMMENT '連携設定の表示名',
    integration_type ENUM COMMENT '連携の種類（WEBHOOK:Webhook、API:REST API、OAUTH:OAuth認証、SMTP:メール送信）',
    endpoint_url VARCHAR(500) COMMENT '連携先のエンドポイントURL',
    auth_type ENUM COMMENT '認証方式（NONE:認証なし、BASIC:Basic認証、BEARER:Bearer Token、OAUTH2:OAuth2.0、API_KEY:APIキー）',
    auth_config TEXT COMMENT '認証に必要な設定情報（JSON形式、暗号化必須）',
    connection_config TEXT COMMENT '接続に関する設定情報（JSON形式）',
    request_headers TEXT COMMENT 'デフォルトリクエストヘッダー（JSON形式）',
    timeout_seconds INTEGER DEFAULT 30 COMMENT '接続タイムアウト時間（秒）',
    retry_count INTEGER DEFAULT 3 COMMENT '失敗時のリトライ回数',
    retry_interval INTEGER DEFAULT 5 COMMENT 'リトライ間隔（秒）',
    rate_limit_per_minute INTEGER COMMENT '1分間あたりのリクエスト制限数',
    is_enabled BOOLEAN DEFAULT True COMMENT '連携設定が有効かどうか',
    health_check_url VARCHAR(500) COMMENT '連携先の死活監視用URL',
    last_health_check TIMESTAMP COMMENT '最終ヘルスチェック実行日時',
    health_status ENUM COMMENT '連携先の状態（HEALTHY:正常、UNHEALTHY:異常、UNKNOWN:不明）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_integration_config_tenant_key ON SYS_IntegrationConfig (tenant_id, integration_key);
CREATE INDEX idx_integration_config_type ON SYS_IntegrationConfig (integration_type);
CREATE INDEX idx_integration_config_enabled ON SYS_IntegrationConfig (is_enabled);
CREATE INDEX idx_integration_config_health ON SYS_IntegrationConfig (health_status, last_health_check);
CREATE INDEX idx_integration_config_auth_type ON SYS_IntegrationConfig (auth_type);

-- その他の制約
ALTER TABLE SYS_IntegrationConfig ADD CONSTRAINT uk_integration_config_tenant_key UNIQUE ();
ALTER TABLE SYS_IntegrationConfig ADD CONSTRAINT chk_integration_config_type CHECK (integration_type IN ('WEBHOOK', 'API', 'OAUTH', 'SMTP'));
ALTER TABLE SYS_IntegrationConfig ADD CONSTRAINT chk_integration_config_auth_type CHECK (auth_type IN ('NONE', 'BASIC', 'BEARER', 'OAUTH2', 'API_KEY'));
ALTER TABLE SYS_IntegrationConfig ADD CONSTRAINT chk_integration_config_health_status CHECK (health_status IS NULL OR health_status IN ('HEALTHY', 'UNHEALTHY', 'UNKNOWN'));
ALTER TABLE SYS_IntegrationConfig ADD CONSTRAINT chk_integration_config_timeout_positive CHECK (timeout_seconds > 0);
ALTER TABLE SYS_IntegrationConfig ADD CONSTRAINT chk_integration_config_retry_positive CHECK (retry_count >= 0 AND retry_interval >= 0);
