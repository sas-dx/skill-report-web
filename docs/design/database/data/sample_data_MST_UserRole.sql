-- サンプルデータ INSERT文: MST_UserRole
-- 生成日時: 2025-06-20 00:15:12
-- レコード数: 2

INSERT INTO MST_UserRole (user_id, role_id, assignment_type, assigned_by, assignment_reason, effective_from, effective_to, is_primary_role, priority_order, conditions, delegation_source_user_id, delegation_expires_at, auto_assigned, requires_approval, approval_status, approved_by, approved_at, assignment_status, last_used_at, usage_count, id, created_at, updated_at, is_deleted) VALUES ('USER000001', 'ROLE003', 'DIRECT', 'USER000000', '新規ユーザー登録時の標準ロール割り当て', '2025-01-01 00:00:00', NULL, TRUE, 1, NULL, NULL, NULL, TRUE, FALSE, NULL, NULL, NULL, 'ACTIVE', '2025-06-01 09:00:00', 150, 'mst_9690a482', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO MST_UserRole (user_id, role_id, assignment_type, assigned_by, assignment_reason, effective_from, effective_to, is_primary_role, priority_order, conditions, delegation_source_user_id, delegation_expires_at, auto_assigned, requires_approval, approval_status, approved_by, approved_at, assignment_status, last_used_at, usage_count, id, created_at, updated_at, is_deleted) VALUES ('USER000002', 'ROLE002', 'DIRECT', 'USER000001', 'テナント管理者権限付与', '2025-02-01 00:00:00', NULL, TRUE, 1, '{"tenant_id": "TENANT001"}', NULL, NULL, FALSE, TRUE, 'APPROVED', 'USER000001', '2025-01-31 15:30:00', 'ACTIVE', '2025-06-01 10:30:00', 75, 'mst_a8197766', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);

-- MST_UserRole サンプルデータ終了
