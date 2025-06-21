-- HIS_AuditLog (監査ログ) サンプルデータ
-- 生成日時: 2025-06-21 17:20:34

INSERT INTO HIS_AuditLog (
    id, user_id, session_id, action_type,
    target_table, target_id, old_values, new_values,
    ip_address, user_agent, result_status, error_message,
    execution_time_ms, is_deleted, tenant_id, created_at,
    updated_at, created_by, updated_by
) VALUES
    ('audit_001', 'emp_001', 'sess_abc123', 'LOGIN',
     NULL, NULL, NULL, NULL,
     '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'SUCCESS', NULL,
     150, FALSE, 'tenant_001', NULL,
     NULL, 'system', 'system'),
    ('audit_002', 'emp_001', 'sess_abc123', 'UPDATE',
     'MST_Employee', 'emp_001', '{"name": "田中太郎", "email": "tanaka@example.com"}', '{"name": "田中太郎", "email": "tanaka.new@example.com"}',
     '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'SUCCESS', NULL,
     250, FALSE, 'tenant_001', NULL,
     NULL, 'emp_001', 'emp_001')
;

-- 実行確認用クエリ
-- SELECT * FROM HIS_AuditLog ORDER BY created_at DESC;
