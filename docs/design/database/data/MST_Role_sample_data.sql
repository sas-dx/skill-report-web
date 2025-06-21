-- MST_Role (ロール情報) サンプルデータ
-- 生成日時: 2025-06-21 17:21:58

INSERT INTO MST_Role (
    role_code, role_name, role_name_short, role_category,
    role_level, parent_role_id, is_system_role, is_tenant_specific,
    max_users, role_priority, auto_assign_conditions, role_status,
    effective_from, effective_to, sort_order, description,
    created_at, updated_at
) VALUES
    ('ROLE001', 'システム管理者', 'システム管理者', 'SYSTEM',
     1, NULL, TRUE, FALSE,
     5, 1, NULL, 'ACTIVE',
     '2025-01-01', NULL, 1, 'システム全体の管理権限を持つ最上位ロール',
     NULL, NULL),
    ('ROLE002', 'テナント管理者', 'テナント管理者', 'TENANT',
     2, NULL, TRUE, TRUE,
     10, 2, NULL, 'ACTIVE',
     '2025-01-01', NULL, 2, 'テナント内の管理権限を持つロール',
     NULL, NULL),
    ('ROLE003', '一般ユーザー', '一般ユーザー', 'BUSINESS',
     3, NULL, TRUE, FALSE,
     NULL, 10, '{"default": true}', 'ACTIVE',
     '2025-01-01', NULL, 10, '基本的な業務機能を利用できるロール',
     NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_Role ORDER BY created_at DESC;
