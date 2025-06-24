-- MST_Permission (権限情報) サンプルデータ
-- 生成日時: 2025-06-24 23:02:18

INSERT INTO MST_Permission (
    id, tenant_id, action_type, audit_required,
    condition_expression, description, effective_from, effective_to,
    is_system_permission, parent_permission_id, permission_category, permission_code,
    permission_id, permission_name, permission_name_short, permission_status,
    requires_approval, requires_conditions, resource_type, risk_level,
    scope_level, sort_order, is_deleted, created_at,
    updated_at
) VALUES
    (NULL, NULL, 'READ', TRUE,
     NULL, 'ユーザー情報の参照権限', '2025-01-01', NULL,
     TRUE, NULL, 'DATA', 'PERM_USER_READ',
     NULL, 'ユーザー情報参照', 'ユーザー参照', 'ACTIVE',
     FALSE, FALSE, 'USER', 1,
     'TENANT', 1, NULL, NULL,
     NULL),
    (NULL, NULL, 'UPDATE', TRUE,
     'department_id = :user_department_id', 'ユーザー情報の更新権限（同一部署のみ）', '2025-01-01', NULL,
     TRUE, NULL, 'DATA', 'PERM_USER_UPDATE',
     NULL, 'ユーザー情報更新', 'ユーザー更新', 'ACTIVE',
     FALSE, TRUE, 'USER', 2,
     'DEPARTMENT', 2, NULL, NULL,
     NULL),
    (NULL, NULL, 'EXECUTE', TRUE,
     NULL, 'システム全体の管理権限', '2025-01-01', NULL,
     TRUE, NULL, 'SYSTEM', 'PERM_SYSTEM_ADMIN',
     NULL, 'システム管理', 'システム管理', 'ACTIVE',
     TRUE, FALSE, 'SYSTEM', 4,
     'GLOBAL', 100, NULL, NULL,
     NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_Permission ORDER BY created_at DESC;
