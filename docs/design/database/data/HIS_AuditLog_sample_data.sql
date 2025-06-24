-- HIS_AuditLog (監査ログ) サンプルデータ
-- 生成日時: 2025-06-24 22:56:14

INSERT INTO HIS_AuditLog (
    id, tenant_id, action_type, auditlog_id,
    created_by, error_message, execution_time_ms, ip_address,
    new_values, old_values, result_status, session_id,
    target_id, target_table, updated_by, user_agent,
    user_id, is_deleted, created_at, updated_at
) VALUES
    ('audit_001', 'tenant_001', 'LOGIN', NULL,
     'system', NULL, 150, '192.168.1.100',
     NULL, NULL, 'SUCCESS', 'sess_abc123',
     NULL, NULL, 'system', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
     'emp_001', FALSE, NULL, NULL),
    ('audit_002', 'tenant_001', 'UPDATE', NULL,
     'emp_001', NULL, 250, '192.168.1.100',
     '{"name": "田中太郎", "email": "tanaka.new@example.com"}', '{"name": "田中太郎", "email": "tanaka@example.com"}', 'SUCCESS', 'sess_abc123',
     'emp_001', 'MST_Employee', 'emp_001', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
     'emp_001', FALSE, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM HIS_AuditLog ORDER BY created_at DESC;
