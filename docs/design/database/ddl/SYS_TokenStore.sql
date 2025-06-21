-- ============================================
-- テーブル: SYS_TokenStore
-- 論理名: トークン管理
-- 説明: SYS_TokenStore（トークン管理）は、認証・認可システムで使用するトークン情報を管理するシステムテーブルです。

主な目的：
- JWTアクセストークンの管理
- リフレッシュトークンの管理
- セッション管理
- トークンの有効期限管理
- セキュリティ監査のためのトークン履歴管理

このテーブルは、認証・認可システムの基盤となる重要なシステムデータです。

-- 作成日: 2025-06-21 17:20:34
-- ============================================

DROP TABLE IF EXISTS SYS_TokenStore;

CREATE TABLE SYS_TokenStore (
    id VARCHAR,
    tenant_id VARCHAR,
    user_id VARCHAR,
    token_type ENUM,
    token_value TEXT,
    token_hash VARCHAR,
    expires_at TIMESTAMP,
    issued_at TIMESTAMP,
    last_used_at TIMESTAMP,
    client_ip VARCHAR,
    user_agent TEXT,
    device_fingerprint VARCHAR,
    scope TEXT,
    is_revoked BOOLEAN DEFAULT False,
    revoked_at TIMESTAMP,
    revoked_reason ENUM,
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_token_store_hash ON SYS_TokenStore (token_hash);
CREATE INDEX idx_token_store_user_type ON SYS_TokenStore (user_id, token_type);
CREATE INDEX idx_token_store_expires ON SYS_TokenStore (expires_at, is_revoked);
CREATE INDEX idx_token_store_tenant_user ON SYS_TokenStore (tenant_id, user_id);
CREATE INDEX idx_token_store_issued ON SYS_TokenStore (issued_at);
CREATE INDEX idx_token_store_last_used ON SYS_TokenStore (last_used_at);
