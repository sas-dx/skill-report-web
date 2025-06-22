-- ============================================
-- テーブル: MST_UserAuth
-- 論理名: ユーザー認証情報
-- 説明: MST_UserAuth（ユーザー認証情報）は、システムにアクセスする全ユーザーの認証・認可情報を管理するマスタテーブルです。

主な目的：
- ユーザーアカウントの一元管理（ログインID、パスワード等）
- 認証情報のセキュアな保存（パスワードハッシュ化、多要素認証対応）
- アカウント状態管理（有効/無効、ロック状態等）
- セッション管理・トークン管理
- パスワードポリシーの適用・管理
- ログイン履歴・セキュリティ監査
- 外部認証システム連携（SSO、LDAP等）

このテーブルは、システム全体のセキュリティの基盤となり、不正アクセス防止、
個人情報保護、コンプライアンス対応において重要な役割を果たします。

-- 作成日: 2025-06-21 22:02:18
-- ============================================

DROP TABLE IF EXISTS MST_UserAuth;

CREATE TABLE MST_UserAuth (
    userauth_id SERIAL NOT NULL COMMENT 'MST_UserAuthの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (userauth_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_userauth_tenant_id ON MST_UserAuth (tenant_id);

-- 外部キー制約
ALTER TABLE MST_UserAuth ADD CONSTRAINT fk_userauth_employee FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
