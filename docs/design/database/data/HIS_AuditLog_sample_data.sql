-- HIS_AuditLog (監査ログ) サンプルデータ
-- 生成日時: 2025-06-21 22:02:17

INSERT INTO HIS_AuditLog (
    auditlog_id, tenant_id, created_at, updated_at,
    id, is_deleted
) VALUES
    (NULL, 'tenant_001', NULL, NULL,
     'audit_001', FALSE),
    (NULL, 'tenant_001', NULL, NULL,
     'audit_002', FALSE)
;

-- 実行確認用クエリ
-- SELECT * FROM HIS_AuditLog ORDER BY created_at DESC;
