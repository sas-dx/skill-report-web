-- MST_UserAuth (ユーザー認証情報) サンプルデータ
-- 生成日時: 2025-06-24 23:02:18

INSERT INTO MST_UserAuth (
    id, tenant_id, account_status, employee_id,
    external_auth_id, external_auth_provider, failed_login_count, last_failed_login_at,
    last_login_at, last_login_ip, login_id, mfa_enabled,
    mfa_secret, password_changed_at, password_expires_at, password_hash,
    password_salt, recovery_token, recovery_token_expires_at, session_timeout,
    user_id, userauth_id, is_deleted, created_at,
    updated_at
) VALUES
    (NULL, NULL, 'ACTIVE', 'EMP000001',
     NULL, NULL, 0, NULL,
     '2025-06-01 09:00:00', '192.168.1.100', 'yamada.taro@company.com', TRUE,
     'JBSWY3DPEHPK3PXP', '2025-01-01 00:00:00', '2025-12-31 23:59:59', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uIoS',
     'randomsalt123', NULL, NULL, 480,
     'USER000001', NULL, NULL, NULL,
     NULL),
    (NULL, NULL, 'ACTIVE', 'EMP000002',
     NULL, NULL, 0, NULL,
     '2025-05-31 17:30:00', '192.168.1.101', 'sato.hanako@company.com', FALSE,
     NULL, '2025-02-01 00:00:00', '2026-01-31 23:59:59', '$2b$12$XQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uIoX',
     'randomsalt456', NULL, NULL, 240,
     'USER000002', NULL, NULL, NULL,
     NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_UserAuth ORDER BY created_at DESC;
