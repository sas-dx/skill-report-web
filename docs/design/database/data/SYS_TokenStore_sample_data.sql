-- SYS_TokenStore (トークン管理) サンプルデータ
-- 生成日時: 2025-06-21 17:20:34

INSERT INTO SYS_TokenStore (
    id, tenant_id, user_id, token_type,
    token_value, token_hash, expires_at, issued_at,
    last_used_at, client_ip, user_agent, device_fingerprint,
    scope, is_revoked, revoked_at, revoked_reason,
    is_deleted
) VALUES
    ('TS001', 'TENANT001', 'USER001', 'ACCESS',
     'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...', 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0', '2025-06-01 20:00:00', '2025-06-01 19:00:00',
     '2025-06-01 19:30:00', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'fp_abc123def456',
     '["read:profile", "write:skills", "read:goals"]', FALSE, NULL, NULL,
     NULL),
    ('TS002', 'TENANT001', 'USER001', 'REFRESH',
     'rt_xyz789abc123def456ghi789jkl012mno345', 'b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1', '2025-06-08 19:00:00', '2025-06-01 19:00:00',
     NULL, '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'fp_abc123def456',
     '["refresh"]', FALSE, NULL, NULL,
     NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM SYS_TokenStore ORDER BY created_at DESC;
