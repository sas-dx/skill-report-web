-- MST_Position (役職マスタ) サンプルデータ
-- 生成日時: 2025-06-04 06:57:02

INSERT INTO MST_Position (
    position_code, position_name, position_name_short, position_level,
    position_rank, position_category, authority_level, approval_limit,
    salary_grade, allowance_amount, is_management, is_executive,
    requires_approval, can_hire, can_evaluate, position_status,
    sort_order, description, code, name
) VALUES
    ('POS001', '代表取締役社長', '社長', 1,
     1, 'EXECUTIVE', 10, 999999999.99,
     'E1', 500000.0, TRUE, TRUE,
     TRUE, TRUE, TRUE, 'ACTIVE',
     1, '会社の最高責任者として経営全般を統括', NULL, NULL),
    ('POS002', '取締役', '取締役', 2,
     1, 'EXECUTIVE', 9, 100000000.0,
     'E2', 300000.0, TRUE, TRUE,
     TRUE, TRUE, TRUE, 'ACTIVE',
     2, '取締役会メンバーとして経営方針決定に参画', NULL, NULL),
    ('POS003', '部長', '部長', 3,
     1, 'MANAGER', 7, 10000000.0,
     'M1', 100000.0, TRUE, FALSE,
     TRUE, TRUE, TRUE, 'ACTIVE',
     3, '部門の責任者として業務全般を管理', NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_Position ORDER BY created_at DESC;
