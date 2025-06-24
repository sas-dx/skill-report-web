-- MST_UserRole (ユーザーロール紐付け) サンプルデータ
-- 生成日時: 2025-06-24 22:56:14

INSERT INTO MST_UserRole (
    id, tenant_id, approval_status, approved_at,
    approved_by, assigned_by, assignment_reason, assignment_status,
    assignment_type, auto_assigned, conditions, delegation_expires_at,
    delegation_source_user_id, effective_from, effective_to, is_primary_role,
    last_used_at, priority_order, requires_approval, role_id,
    usage_count, user_id, userrole_id, is_deleted,
    created_at, updated_at
) VALUES
    (NULL, NULL, NULL, NULL,
     NULL, 'USER000000', '新規ユーザー登録時の標準ロール割り当て', 'ACTIVE',
     'DIRECT', TRUE, NULL, NULL,
     NULL, '2025-01-01 00:00:00', NULL, TRUE,
     '2025-06-01 09:00:00', 1, FALSE, 'ROLE003',
     150, 'USER000001', NULL, NULL,
     NULL, NULL),
    (NULL, NULL, 'APPROVED', '2025-01-31 15:30:00',
     'USER000001', 'USER000001', 'テナント管理者権限付与', 'ACTIVE',
     'DIRECT', FALSE, '{"tenant_id": "TENANT001"}', NULL,
     NULL, '2025-02-01 00:00:00', NULL, TRUE,
     '2025-06-01 10:30:00', 1, TRUE, 'ROLE002',
     75, 'USER000002', NULL, NULL,
     NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_UserRole ORDER BY created_at DESC;
