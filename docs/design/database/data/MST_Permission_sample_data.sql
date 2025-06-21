-- MST_Permission (権限情報) サンプルデータ
-- 生成日時: 2025-06-21 17:21:58

INSERT INTO MST_Permission (
    permission_code, permission_name, permission_name_short, permission_category,
    resource_type, action_type, scope_level, parent_permission_id,
    is_system_permission, requires_conditions, condition_expression, risk_level,
    requires_approval, audit_required, permission_status, effective_from,
    effective_to, sort_order, description, created_at,
    updated_at
) VALUES
    ('PERM_USER_READ', 'ユーザー情報参照', 'ユーザー参照', 'DATA',
     'USER', 'READ', 'TENANT', NULL,
     TRUE, FALSE, NULL, 1,
     FALSE, TRUE, 'ACTIVE', '2025-01-01',
     NULL, 1, 'ユーザー情報の参照権限', NULL,
     NULL),
    ('PERM_USER_UPDATE', 'ユーザー情報更新', 'ユーザー更新', 'DATA',
     'USER', 'UPDATE', 'DEPARTMENT', NULL,
     TRUE, TRUE, 'department_id = :user_department_id', 2,
     FALSE, TRUE, 'ACTIVE', '2025-01-01',
     NULL, 2, 'ユーザー情報の更新権限（同一部署のみ）', NULL,
     NULL),
    ('PERM_SYSTEM_ADMIN', 'システム管理', 'システム管理', 'SYSTEM',
     'SYSTEM', 'EXECUTE', 'GLOBAL', NULL,
     TRUE, FALSE, NULL, 4,
     TRUE, TRUE, 'ACTIVE', '2025-01-01',
     NULL, 100, 'システム全体の管理権限', NULL,
     NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_Permission ORDER BY created_at DESC;
