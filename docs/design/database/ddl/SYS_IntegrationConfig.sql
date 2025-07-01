-- ============================================
-- テーブル: SYS_IntegrationConfig
-- 論理名: 外部連携設定
-- 説明: SYS_IntegrationConfig（外部連携設定）は、外部システムとの連携に必要な設定情報を管理するシステムテーブルです。

主な目的：
- 外部API接続設定の管理
- 認証情報・エンドポイント情報の管理
- 連携パラメータ・設定値の管理
- 外部システム別設定の管理
- テナント別連携設定の管理

このテーブルは、通知・連携管理機能において外部システムとの安全で効率的な連携を実現する重要なシステムデータです。

-- 作成日: 2025-06-24 23:05:57
-- ============================================

DROP TABLE IF EXISTS SYS_IntegrationConfig;

CREATE TABLE SYS_IntegrationConfig (
    id VARCHAR(50) COMMENT 'ID',
    tenant_id VARCHAR(50) COMMENT 'テナントID',
    auth_config TEXT COMMENT '認証設定',
    auth_type ENUM('NONE', 'BASIC', 'BEARER', 'OAUTH2', 'API_KEY') COMMENT '認証タイプ',
    connection_config TEXT COMMENT '接続設定',
    endpoint_url VARCHAR(500) COMMENT 'エンドポイントURL',
    health_check_url VARCHAR(500) COMMENT 'ヘルスチェックURL',
    health_status ENUM('HEALTHY', 'UNHEALTHY', 'UNKNOWN') COMMENT 'ヘルス状態',
    integration_key VARCHAR(100) COMMENT '連携キー',
    integration_name VARCHAR(200) COMMENT '連携名',
    integration_type ENUM('WEBHOOK', 'API', 'OAUTH', 'SMTP') COMMENT '連携タイプ',
    integrationconfig_id INT AUTO_INCREMENT NOT NULL COMMENT 'SYS_IntegrationConfigの主キー',
    is_enabled BOOLEAN DEFAULT True COMMENT '有効フラグ',
    last_health_check TIMESTAMP COMMENT '最終ヘルスチェック',
    rate_limit_per_minute INTEGER COMMENT '分間レート制限',
    request_headers TEXT COMMENT 'リクエストヘッダー',
    retry_count INTEGER DEFAULT 3 COMMENT 'リトライ回数',
    retry_interval INTEGER DEFAULT 5 COMMENT 'リトライ間隔',
    timeout_seconds INTEGER DEFAULT 30 COMMENT 'タイムアウト秒数',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_integration_config_tenant_key ON SYS_IntegrationConfig (tenant_id, integration_key);
CREATE INDEX idx_integration_config_type ON SYS_IntegrationConfig (integration_type);
CREATE INDEX idx_integration_config_enabled ON SYS_IntegrationConfig (is_enabled);
CREATE INDEX idx_integration_config_health ON SYS_IntegrationConfig (health_status, last_health_check);
CREATE INDEX idx_integration_config_auth_type ON SYS_IntegrationConfig (auth_type);

-- その他の制約
-- 制約DDL生成エラー: uk_integration_config_tenant_key
ALTER TABLE SYS_IntegrationConfig ADD CONSTRAINT chk_integration_config_type CHECK (integration_type IN ('WEBHOOK', 'API', 'OAUTH', 'SMTP'));
ALTER TABLE SYS_IntegrationConfig ADD CONSTRAINT chk_integration_config_auth_type CHECK (auth_type IN ('NONE', 'BASIC', 'BEARER', 'OAUTH2', 'API_KEY'));
ALTER TABLE SYS_IntegrationConfig ADD CONSTRAINT chk_integration_config_health_status CHECK (health_status IS NULL OR health_status IN ('HEALTHY', 'UNHEALTHY', 'UNKNOWN'));
ALTER TABLE SYS_IntegrationConfig ADD CONSTRAINT chk_integration_config_timeout_positive CHECK (timeout_seconds > 0);
ALTER TABLE SYS_IntegrationConfig ADD CONSTRAINT chk_integration_config_retry_positive CHECK (retry_count >= 0 AND retry_interval >= 0);
