-- MST_UserAuth (ユーザー認証情報) DDL
-- 生成日時: 2025-06-01 19:42:42

CREATE TABLE MST_UserAuth (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    user_id VARCHAR(50),
    login_id VARCHAR(100),
    password_hash VARCHAR(255),
    password_salt VARCHAR(100),
    employee_id VARCHAR(50),
    account_status ENUM DEFAULT 'ACTIVE',
    last_login_at TIMESTAMP,
    last_login_ip VARCHAR(45),
    failed_login_count INT DEFAULT 0,
    last_failed_login_at TIMESTAMP,
    password_changed_at TIMESTAMP,
    password_expires_at TIMESTAMP,
    mfa_enabled BOOLEAN DEFAULT False,
    mfa_secret VARCHAR(255),
    recovery_token VARCHAR(255),
    recovery_token_expires_at TIMESTAMP,
    session_timeout INT,
    external_auth_provider VARCHAR(50),
    external_auth_id VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_user_id ON MST_UserAuth (user_id);
CREATE UNIQUE INDEX idx_login_id ON MST_UserAuth (login_id);
CREATE UNIQUE INDEX idx_employee_id ON MST_UserAuth (employee_id);
CREATE INDEX idx_account_status ON MST_UserAuth (account_status);
CREATE INDEX idx_last_login ON MST_UserAuth (last_login_at);
CREATE INDEX idx_password_expires ON MST_UserAuth (password_expires_at);
CREATE INDEX idx_external_auth ON MST_UserAuth (external_auth_provider, external_auth_id);

-- 外部キー制約
ALTER TABLE MST_UserAuth ADD CONSTRAINT fk_userauth_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
