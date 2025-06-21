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

-- 作成日: 2025-06-21 17:20:35
-- ============================================

DROP TABLE IF EXISTS SYS_IntegrationConfig;

CREATE TABLE SYS_IntegrationConfig (
    id VARCHAR,
    tenant_id VARCHAR,
    integration_key VARCHAR,
    integration_name VARCHAR,
    integration_type ENUM,
    endpoint_url VARCHAR,
    auth_type ENUM,
    auth_config TEXT,
    connection_config TEXT,
    request_headers TEXT,
    timeout_seconds INTEGER DEFAULT 30,
    retry_count INTEGER DEFAULT 3,
    retry_interval INTEGER DEFAULT 5,
    rate_limit_per_minute INTEGER,
    is_enabled BOOLEAN DEFAULT True,
    health_check_url VARCHAR,
    last_health_check TIMESTAMP,
    health_status ENUM,
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_integration_config_tenant_key ON SYS_IntegrationConfig (tenant_id, integration_key);
CREATE INDEX idx_integration_config_type ON SYS_IntegrationConfig (integration_type);
CREATE INDEX idx_integration_config_enabled ON SYS_IntegrationConfig (is_enabled);
CREATE INDEX idx_integration_config_health ON SYS_IntegrationConfig (health_status, last_health_check);
CREATE INDEX idx_integration_config_auth_type ON SYS_IntegrationConfig (auth_type);
