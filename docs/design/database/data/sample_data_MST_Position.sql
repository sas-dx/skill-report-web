-- サンプルデータ INSERT文: MST_Position
-- 生成日時: 2025-06-21 07:22:21
-- レコード数: 3

BEGIN;

INSERT INTO MST_Position (position_code, position_name, position_name_short, position_level, position_rank, position_category, authority_level, approval_limit, salary_grade, allowance_amount, is_management, is_executive, requires_approval, can_hire, can_evaluate, position_status, sort_order, description, id, created_at, updated_at, is_deleted) VALUES ('POS001', '代表取締役社長', '社長', 1, 1, 'EXECUTIVE', 10, 999999999.99, 'E1', 500000.0, TRUE, TRUE, TRUE, TRUE, TRUE, 'ACTIVE', 1, '会社の最高責任者として経営全般を統括', 'mst_f40051d0', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO MST_Position (position_code, position_name, position_name_short, position_level, position_rank, position_category, authority_level, approval_limit, salary_grade, allowance_amount, is_management, is_executive, requires_approval, can_hire, can_evaluate, position_status, sort_order, description, id, created_at, updated_at, is_deleted) VALUES ('POS002', '取締役', '取締役', 2, 1, 'EXECUTIVE', 9, 100000000.0, 'E2', 300000.0, TRUE, TRUE, TRUE, TRUE, TRUE, 'ACTIVE', 2, '取締役会メンバーとして経営方針決定に参画', 'mst_eebc081f', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO MST_Position (position_code, position_name, position_name_short, position_level, position_rank, position_category, authority_level, approval_limit, salary_grade, allowance_amount, is_management, is_executive, requires_approval, can_hire, can_evaluate, position_status, sort_order, description, id, created_at, updated_at, is_deleted) VALUES ('POS003', '部長', '部長', 3, 1, 'MANAGER', 7, 10000000.0, 'M1', 100000.0, TRUE, FALSE, TRUE, TRUE, TRUE, 'ACTIVE', 3, '部門の責任者として業務全般を管理', 'mst_a1c54dba', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);

COMMIT;

-- MST_Position サンプルデータ終了
