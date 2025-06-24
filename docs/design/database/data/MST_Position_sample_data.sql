-- MST_Position (役職マスタ) サンプルデータ
-- 生成日時: 2025-06-24 23:02:18

INSERT INTO MST_Position (
    id, tenant_id, position_code, position_name,
    allowance_amount, approval_limit, authority_level, can_evaluate,
    can_hire, description, is_executive, is_management,
    position_category, position_id, position_level, position_name_short,
    position_rank, position_status, requires_approval, salary_grade,
    sort_order, is_deleted, created_at, updated_at
) VALUES
    (NULL, NULL, 'POS001', '代表取締役社長',
     500000.0, 999999999.99, 10, TRUE,
     TRUE, '会社の最高責任者として経営全般を統括', TRUE, TRUE,
     'EXECUTIVE', NULL, 1, '社長',
     1, 'ACTIVE', TRUE, 'E1',
     1, NULL, NULL, NULL),
    (NULL, NULL, 'POS002', '取締役',
     300000.0, 100000000.0, 9, TRUE,
     TRUE, '取締役会メンバーとして経営方針決定に参画', TRUE, TRUE,
     'EXECUTIVE', NULL, 2, '取締役',
     1, 'ACTIVE', TRUE, 'E2',
     2, NULL, NULL, NULL),
    (NULL, NULL, 'POS003', '部長',
     100000.0, 10000000.0, 7, TRUE,
     TRUE, '部門の責任者として業務全般を管理', FALSE, TRUE,
     'MANAGER', NULL, 3, '部長',
     1, 'ACTIVE', TRUE, 'M1',
     3, NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_Position ORDER BY created_at DESC;
