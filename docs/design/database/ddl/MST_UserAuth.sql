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

-- 作成日: 2025-06-24 23:05:56
-- ============================================

DROP TABLE IF EXISTS MST_UserAuth;

CREATE TABLE MST_UserAuth (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    account_status ENUM('ACTIVE', 'INACTIVE', 'LOCKED', 'SUSPENDED') DEFAULT 'ACTIVE' COMMENT 'アカウント状態',
    employee_id VARCHAR(50) COMMENT '社員ID',
    external_auth_id VARCHAR(255) COMMENT '外部認証ID',
    external_auth_provider VARCHAR(50) COMMENT '外部認証プロバイダ',
    failed_login_count INT DEFAULT 0 COMMENT 'ログイン失敗回数',
    last_failed_login_at TIMESTAMP COMMENT '最終ログイン失敗日時',
    last_login_at TIMESTAMP COMMENT '最終ログイン日時',
    last_login_ip VARCHAR(45) COMMENT '最終ログインIP',
    login_id VARCHAR(100) COMMENT 'ログインID',
    mfa_enabled BOOLEAN DEFAULT False COMMENT '多要素認証有効',
    mfa_secret VARCHAR(255) COMMENT '多要素認証シークレット',
    password_changed_at TIMESTAMP COMMENT 'パスワード変更日時',
    password_expires_at TIMESTAMP COMMENT 'パスワード有効期限',
    password_hash VARCHAR(255) COMMENT 'パスワードハッシュ',
    password_salt VARCHAR(100) COMMENT 'パスワードソルト',
    recovery_token VARCHAR(255) COMMENT '復旧トークン',
    recovery_token_expires_at TIMESTAMP COMMENT '復旧トークン有効期限',
    session_timeout INT COMMENT 'セッションタイムアウト',
    user_id VARCHAR(50) COMMENT 'ユーザーID',
    userauth_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_UserAuthの主キー',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_user_id ON MST_UserAuth (user_id);
CREATE UNIQUE INDEX idx_login_id ON MST_UserAuth (login_id);
CREATE UNIQUE INDEX idx_employee_id ON MST_UserAuth (employee_id);
CREATE INDEX idx_account_status ON MST_UserAuth (account_status);
CREATE INDEX idx_last_login ON MST_UserAuth (last_login_at);
CREATE INDEX idx_password_expires ON MST_UserAuth (password_expires_at);
CREATE INDEX idx_external_auth ON MST_UserAuth (external_auth_provider, external_auth_id);
CREATE INDEX idx_mst_userauth_tenant_id ON MST_UserAuth (tenant_id);

-- 外部キー制約
ALTER TABLE MST_UserAuth ADD CONSTRAINT fk_userauth_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
-- 制約DDL生成エラー: uk_user_id
-- 制約DDL生成エラー: uk_login_id
-- 制約DDL生成エラー: uk_employee_id
ALTER TABLE MST_UserAuth ADD CONSTRAINT chk_account_status CHECK (account_status IN ('ACTIVE', 'INACTIVE', 'LOCKED', 'SUSPENDED'));
ALTER TABLE MST_UserAuth ADD CONSTRAINT chk_failed_login_count CHECK (failed_login_count >= 0);
ALTER TABLE MST_UserAuth ADD CONSTRAINT chk_session_timeout CHECK (session_timeout IS NULL OR session_timeout > 0);
