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

-- 作成日: 2025-06-24 23:05:57
-- ============================================

DROP TABLE IF EXISTS SYS_TokenStore;

CREATE TABLE SYS_TokenStore (
    id VARCHAR(50) COMMENT 'ID',
    tenant_id VARCHAR(50) COMMENT 'テナントID',
    client_ip VARCHAR(45) COMMENT 'クライアントIP',
    device_fingerprint VARCHAR(255) COMMENT 'デバイスフィンガープリント',
    expires_at TIMESTAMP COMMENT '有効期限',
    is_revoked BOOLEAN DEFAULT False COMMENT '無効化フラグ',
    issued_at TIMESTAMP COMMENT '発行日時',
    last_used_at TIMESTAMP COMMENT '最終使用日時',
    revoked_at TIMESTAMP COMMENT '無効化日時',
    revoked_reason ENUM('LOGOUT', 'EXPIRED', 'SECURITY', 'ADMIN') COMMENT '無効化理由',
    scope TEXT COMMENT 'スコープ',
    token_hash VARCHAR(255) COMMENT 'トークンハッシュ',
    token_type ENUM('ACCESS', 'REFRESH', 'SESSION') COMMENT 'トークンタイプ',
    token_value TEXT COMMENT 'トークン値',
    tokenstore_id INT AUTO_INCREMENT NOT NULL COMMENT 'SYS_TokenStoreの主キー',
    user_agent TEXT COMMENT 'ユーザーエージェント',
    user_id VARCHAR(50) COMMENT 'ユーザーID',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_token_store_hash ON SYS_TokenStore (token_hash);
CREATE INDEX idx_token_store_user_type ON SYS_TokenStore (user_id, token_type);
CREATE INDEX idx_token_store_expires ON SYS_TokenStore (expires_at, is_revoked);
CREATE INDEX idx_token_store_tenant_user ON SYS_TokenStore (tenant_id, user_id);
CREATE INDEX idx_token_store_issued ON SYS_TokenStore (issued_at);
CREATE INDEX idx_token_store_last_used ON SYS_TokenStore (last_used_at);

-- 外部キー制約
ALTER TABLE SYS_TokenStore ADD CONSTRAINT fk_token_store_user FOREIGN KEY (user_id) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE CASCADE;

-- その他の制約
-- 制約DDL生成エラー: uk_token_store_hash
ALTER TABLE SYS_TokenStore ADD CONSTRAINT chk_token_store_type CHECK (token_type IN ('ACCESS', 'REFRESH', 'SESSION'));
ALTER TABLE SYS_TokenStore ADD CONSTRAINT chk_token_store_revoked_reason CHECK (revoked_reason IS NULL OR revoked_reason IN ('LOGOUT', 'EXPIRED', 'SECURITY', 'ADMIN'));
ALTER TABLE SYS_TokenStore ADD CONSTRAINT chk_token_store_expires_after_issued CHECK (expires_at > issued_at);
ALTER TABLE SYS_TokenStore ADD CONSTRAINT chk_token_store_revoked_consistency CHECK ((is_revoked = false AND revoked_at IS NULL AND revoked_reason IS NULL) OR (is_revoked = true AND revoked_at IS NOT NULL));
