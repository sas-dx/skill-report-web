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

-- 作成日: 2025-06-21 22:02:17
-- ============================================

DROP TABLE IF EXISTS SYS_TokenStore;

CREATE TABLE SYS_TokenStore (
    tokenstore_id SERIAL NOT NULL COMMENT 'SYS_TokenStoreの主キー',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    PRIMARY KEY (tokenstore_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 外部キー制約
ALTER TABLE SYS_TokenStore ADD CONSTRAINT fk_token_store_user FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
