-- サンプルデータ INSERT文: MST_EmployeeDepartment
-- 生成日時: 2025-06-20 00:15:12
-- レコード数: 3

INSERT INTO MST_EmployeeDepartment (employee_id, department_id, assignment_type, start_date, end_date, assignment_ratio, role_in_department, reporting_manager_id, assignment_reason, assignment_status, approval_status, approved_by, approved_at, id, created_at, updated_at, is_deleted) VALUES ('EMP000001', 'DEPT001', 'PRIMARY', '2020-04-01', NULL, 100.0, 'チームリーダー', 'EMP000010', '新卒入社時配属', 'ACTIVE', 'APPROVED', 'EMP000010', '2020-03-25 10:00:00', 'mst_6c899c3b', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO MST_EmployeeDepartment (employee_id, department_id, assignment_type, start_date, end_date, assignment_ratio, role_in_department, reporting_manager_id, assignment_reason, assignment_status, approval_status, approved_by, approved_at, id, created_at, updated_at, is_deleted) VALUES ('EMP000002', 'DEPT002', 'PRIMARY', '2021-04-01', NULL, 80.0, '開発担当', 'EMP000011', '新卒入社時配属', 'ACTIVE', 'APPROVED', 'EMP000011', '2021-03-25 10:00:00', 'mst_78852830', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO MST_EmployeeDepartment (employee_id, department_id, assignment_type, start_date, end_date, assignment_ratio, role_in_department, reporting_manager_id, assignment_reason, assignment_status, approval_status, approved_by, approved_at, id, created_at, updated_at, is_deleted) VALUES ('EMP000002', 'DEPT003', 'SECONDARY', '2023-01-01', NULL, 20.0, 'プロジェクト支援', 'EMP000012', 'プロジェクト支援のため兼務', 'ACTIVE', 'APPROVED', 'EMP000012', '2022-12-20 14:00:00', 'mst_6bcc465a', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);

-- MST_EmployeeDepartment サンプルデータ終了
