-- MST_UserAuth (ユーザー認証情報) サンプルデータ
-- 生成日時: 2025-06-21 17:20:35

INSERT INTO MST_UserAuth (
    user_id, login_id, password_hash, password_salt,
    employee_id, account_status, last_login_at, last_login_ip,
    failed_login_count, last_failed_login_at, password_changed_at, password_expires_at,
    mfa_enabled, mfa_secret, recovery_token, recovery_token_expires_at,
    session_timeout, external_auth_provider, external_auth_id, created_at,
    updated_at
) VALUES
    ('USER000001', 'yamada.taro@company.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uIoS', 'randomsalt123',
     'EMP000001', 'ACTIVE', '2025-06-01 09:00:00', '192.168.1.100',
     0, NULL, '2025-01-01 00:00:00', '2025-12-31 23:59:59',
     TRUE, 'JBSWY3DPEHPK3PXP', NULL, NULL,
     480, NULL, NULL, NULL,
     NULL),
    ('USER000002', 'sato.hanako@company.com', '$2b$12$XQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uIoX', 'randomsalt456',
     'EMP000002', 'ACTIVE', '2025-05-31 17:30:00', '192.168.1.101',
     0, NULL, '2025-02-01 00:00:00', '2026-01-31 23:59:59',
     FALSE, NULL, NULL, NULL,
     240, NULL, NULL, NULL,
     NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_UserAuth ORDER BY created_at DESC;
