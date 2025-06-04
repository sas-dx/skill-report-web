-- ============================================
-- テーブル: SYS_TokenStore
-- 論理名: トークン管理
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS SYS_TokenStore;

CREATE TABLE SYS_TokenStore (
    id VARCHAR(50) COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) COMMENT 'マルチテナント識別子',
    user_id VARCHAR(50) COMMENT 'トークンの所有者ユーザーID（MST_UserAuthへの参照）',
    token_type ENUM COMMENT 'トークンの種類（ACCESS:アクセストークン、REFRESH:リフレッシュトークン、SESSION:セッション）',
    token_value TEXT COMMENT 'トークンの値（暗号化必須）',
    token_hash VARCHAR(255) COMMENT 'トークン値のハッシュ値（検索用）',
    expires_at TIMESTAMP COMMENT 'トークンの有効期限',
    issued_at TIMESTAMP COMMENT 'トークンの発行日時',
    last_used_at TIMESTAMP COMMENT 'トークンの最終使用日時',
    client_ip VARCHAR(45) COMMENT 'トークン発行時のクライアントIPアドレス（IPv6対応）',
    user_agent TEXT COMMENT 'トークン発行時のユーザーエージェント情報',
    device_fingerprint VARCHAR(255) COMMENT 'デバイス識別用フィンガープリント',
    scope TEXT COMMENT 'トークンのアクセススコープ（JSON形式）',
    is_revoked BOOLEAN DEFAULT False COMMENT 'トークンが無効化されているかどうか',
    revoked_at TIMESTAMP COMMENT 'トークンが無効化された日時',
    revoked_reason ENUM COMMENT '無効化の理由（LOGOUT:ログアウト、EXPIRED:期限切れ、SECURITY:セキュリティ、ADMIN:管理者操作）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_token_store_hash ON SYS_TokenStore (token_hash);
CREATE INDEX idx_token_store_user_type ON SYS_TokenStore (user_id, token_type);
CREATE INDEX idx_token_store_expires ON SYS_TokenStore (expires_at, is_revoked);
CREATE INDEX idx_token_store_tenant_user ON SYS_TokenStore (tenant_id, user_id);
CREATE INDEX idx_token_store_issued ON SYS_TokenStore (issued_at);
CREATE INDEX idx_token_store_last_used ON SYS_TokenStore (last_used_at);

-- 外部キー制約
ALTER TABLE SYS_TokenStore ADD CONSTRAINT fk_token_store_user FOREIGN KEY (user_id) REFERENCES MST_UserAuth(id) ON UPDATE CASCADE ON DELETE CASCADE;

-- その他の制約
ALTER TABLE SYS_TokenStore ADD CONSTRAINT uk_token_store_hash UNIQUE ();
ALTER TABLE SYS_TokenStore ADD CONSTRAINT chk_token_store_type CHECK (token_type IN ('ACCESS', 'REFRESH', 'SESSION'));
ALTER TABLE SYS_TokenStore ADD CONSTRAINT chk_token_store_revoked_reason CHECK (revoked_reason IS NULL OR revoked_reason IN ('LOGOUT', 'EXPIRED', 'SECURITY', 'ADMIN'));
ALTER TABLE SYS_TokenStore ADD CONSTRAINT chk_token_store_expires_after_issued CHECK (expires_at > issued_at);
ALTER TABLE SYS_TokenStore ADD CONSTRAINT chk_token_store_revoked_consistency CHECK ((is_revoked = false AND revoked_at IS NULL AND revoked_reason IS NULL) OR (is_revoked = true AND revoked_at IS NOT NULL));
