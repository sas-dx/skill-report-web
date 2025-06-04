-- ============================================
-- テーブル: MST_UserAuth
-- 論理名: ユーザー認証情報
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_UserAuth;

CREATE TABLE MST_UserAuth (
    user_id VARCHAR(50) COMMENT 'ユーザーを一意に識別するID（例：USER000001）',
    login_id VARCHAR(100) COMMENT 'ログイン時に使用するID（通常はメールアドレス）',
    password_hash VARCHAR(255) COMMENT 'ハッシュ化されたパスワード（bcrypt等）',
    password_salt VARCHAR(100) COMMENT 'パスワードハッシュ化用のソルト値',
    employee_id VARCHAR(50) COMMENT '関連する社員のID（MST_Employeeへの外部キー）',
    account_status ENUM DEFAULT 'ACTIVE' COMMENT 'アカウントの状態（ACTIVE:有効、INACTIVE:無効、LOCKED:ロック、SUSPENDED:停止）',
    last_login_at TIMESTAMP COMMENT '最後にログインした日時',
    last_login_ip VARCHAR(45) COMMENT '最後にログインしたIPアドレス（IPv4/IPv6対応）',
    failed_login_count INT DEFAULT 0 COMMENT '連続ログイン失敗回数（アカウントロック判定用）',
    last_failed_login_at TIMESTAMP COMMENT '最後にログインに失敗した日時',
    password_changed_at TIMESTAMP COMMENT 'パスワードを最後に変更した日時',
    password_expires_at TIMESTAMP COMMENT 'パスワードの有効期限',
    mfa_enabled BOOLEAN DEFAULT False COMMENT '多要素認証が有効かどうか',
    mfa_secret VARCHAR(255) COMMENT 'TOTP等の多要素認証用シークレットキー',
    recovery_token VARCHAR(255) COMMENT 'パスワードリセット等の復旧用トークン',
    recovery_token_expires_at TIMESTAMP COMMENT '復旧トークンの有効期限',
    session_timeout INT COMMENT 'セッションタイムアウト時間（分）',
    external_auth_provider VARCHAR(50) COMMENT '外部認証プロバイダ（LDAP、SAML、OAuth等）',
    external_auth_id VARCHAR(255) COMMENT '外部認証システムでのユーザーID',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称',
    description TEXT COMMENT 'マスタ説明'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_user_id ON MST_UserAuth (user_id);
CREATE UNIQUE INDEX idx_login_id ON MST_UserAuth (login_id);
CREATE UNIQUE INDEX idx_employee_id ON MST_UserAuth (employee_id);
CREATE INDEX idx_account_status ON MST_UserAuth (account_status);
CREATE INDEX idx_last_login ON MST_UserAuth (last_login_at);
CREATE INDEX idx_password_expires ON MST_UserAuth (password_expires_at);
CREATE INDEX idx_external_auth ON MST_UserAuth (external_auth_provider, external_auth_id);

-- 外部キー制約
ALTER TABLE MST_UserAuth ADD CONSTRAINT fk_userauth_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
ALTER TABLE MST_UserAuth ADD CONSTRAINT uk_user_id UNIQUE ();
ALTER TABLE MST_UserAuth ADD CONSTRAINT uk_login_id UNIQUE ();
ALTER TABLE MST_UserAuth ADD CONSTRAINT uk_employee_id UNIQUE ();
ALTER TABLE MST_UserAuth ADD CONSTRAINT chk_account_status CHECK (account_status IN ('ACTIVE', 'INACTIVE', 'LOCKED', 'SUSPENDED'));
ALTER TABLE MST_UserAuth ADD CONSTRAINT chk_failed_login_count CHECK (failed_login_count >= 0);
ALTER TABLE MST_UserAuth ADD CONSTRAINT chk_session_timeout CHECK (session_timeout IS NULL OR session_timeout > 0);
