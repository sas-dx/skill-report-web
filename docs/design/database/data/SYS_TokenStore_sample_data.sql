-- SYS_TokenStore (トークン管理) サンプルデータ
-- 生成日時: 2025-06-24 23:02:18

INSERT INTO SYS_TokenStore (
    id, tenant_id, client_ip, device_fingerprint,
    expires_at, is_revoked, issued_at, last_used_at,
    revoked_at, revoked_reason, scope, token_hash,
    token_type, token_value, tokenstore_id, user_agent,
    user_id, is_deleted, created_at, updated_at
) VALUES
    ('TS001', 'TENANT001', '192.168.1.100', 'fp_abc123def456',
     '2025-06-01 20:00:00', FALSE, '2025-06-01 19:00:00', '2025-06-01 19:30:00',
     NULL, NULL, '["read:profile", "write:skills", "read:goals"]', 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0',
     'ACCESS', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...', NULL, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
     'USER001', NULL, NULL, NULL),
    ('TS002', 'TENANT001', '192.168.1.100', 'fp_abc123def456',
     '2025-06-08 19:00:00', FALSE, '2025-06-01 19:00:00', NULL,
     NULL, NULL, '["refresh"]', 'b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1',
     'REFRESH', 'rt_xyz789abc123def456ghi789jkl012mno345', NULL, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
     'USER001', NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM SYS_TokenStore ORDER BY created_at DESC;
