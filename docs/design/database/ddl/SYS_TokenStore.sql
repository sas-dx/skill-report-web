-- SYS_TokenStore (トークン管理) DDL
-- 生成日時: 2025-06-01 19:42:44

CREATE TABLE SYS_TokenStore (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    id VARCHAR(50),
    tenant_id VARCHAR(50),
    user_id VARCHAR(50),
    token_type ENUM,
    token_value TEXT,
    token_hash VARCHAR(255),
    expires_at TIMESTAMP,
    issued_at TIMESTAMP,
    last_used_at TIMESTAMP,
    client_ip VARCHAR(45),
    user_agent TEXT,
    device_fingerprint VARCHAR(255),
    scope TEXT,
    is_revoked BOOLEAN DEFAULT False,
    revoked_at TIMESTAMP,
    revoked_reason ENUM,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_token_store_hash ON SYS_TokenStore (token_hash);
CREATE INDEX idx_token_store_user_type ON SYS_TokenStore (user_id, token_type);
CREATE INDEX idx_token_store_expires ON SYS_TokenStore (expires_at, is_revoked);
CREATE INDEX idx_token_store_tenant_user ON SYS_TokenStore (tenant_id, user_id);
CREATE INDEX idx_token_store_issued ON SYS_TokenStore (issued_at);
CREATE INDEX idx_token_store_last_used ON SYS_TokenStore (last_used_at);

-- 外部キー制約
ALTER TABLE SYS_TokenStore ADD CONSTRAINT fk_token_store_user FOREIGN KEY (user_id) REFERENCES MST_UserAuth(id) ON UPDATE CASCADE ON DELETE CASCADE;
