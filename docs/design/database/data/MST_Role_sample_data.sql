-- MST_Role (ロール情報) サンプルデータ
-- 生成日時: 2025-06-24 22:56:16

INSERT INTO MST_Role (
    id, tenant_id, auto_assign_conditions, description,
    effective_from, effective_to, is_system_role, is_tenant_specific,
    max_users, parent_role_id, role_category, role_code,
    role_id, role_level, role_name, role_name_short,
    role_priority, role_status, sort_order, is_deleted,
    created_at, updated_at
) VALUES
    (NULL, NULL, NULL, 'システム全体の管理権限を持つ最上位ロール',
     '2025-01-01', NULL, TRUE, FALSE,
     5, NULL, 'SYSTEM', 'ROLE001',
     NULL, 1, 'システム管理者', 'システム管理者',
     1, 'ACTIVE', 1, NULL,
     NULL, NULL),
    (NULL, NULL, NULL, 'テナント内の管理権限を持つロール',
     '2025-01-01', NULL, TRUE, TRUE,
     10, NULL, 'TENANT', 'ROLE002',
     NULL, 2, 'テナント管理者', 'テナント管理者',
     2, 'ACTIVE', 2, NULL,
     NULL, NULL),
    (NULL, NULL, '{"default": true}', '基本的な業務機能を利用できるロール',
     '2025-01-01', NULL, TRUE, FALSE,
     NULL, NULL, 'BUSINESS', 'ROLE003',
     NULL, 3, '一般ユーザー', '一般ユーザー',
     10, 'ACTIVE', 10, NULL,
     NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_Role ORDER BY created_at DESC;
