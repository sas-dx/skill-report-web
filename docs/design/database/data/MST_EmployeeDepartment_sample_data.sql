-- MST_EmployeeDepartment (社員部署関連) サンプルデータ
-- 生成日時: 2025-06-24 23:05:58

INSERT INTO MST_EmployeeDepartment (
    id, tenant_id, approval_status, approved_at,
    approved_by, assignment_ratio, assignment_reason, assignment_status,
    assignment_type, department_id, employee_id, employeedepartment_id,
    end_date, reporting_manager_id, role_in_department, start_date,
    is_deleted, created_at, updated_at
) VALUES
    (NULL, NULL, 'APPROVED', '2020-03-25 10:00:00',
     'EMP000010', 100.0, '新卒入社時配属', 'ACTIVE',
     'PRIMARY', 'DEPT001', 'EMP000001', NULL,
     NULL, 'EMP000010', 'チームリーダー', '2020-04-01',
     NULL, NULL, NULL),
    (NULL, NULL, 'APPROVED', '2021-03-25 10:00:00',
     'EMP000011', 80.0, '新卒入社時配属', 'ACTIVE',
     'PRIMARY', 'DEPT002', 'EMP000002', NULL,
     NULL, 'EMP000011', '開発担当', '2021-04-01',
     NULL, NULL, NULL),
    (NULL, NULL, 'APPROVED', '2022-12-20 14:00:00',
     'EMP000012', 20.0, 'プロジェクト支援のため兼務', 'ACTIVE',
     'SECONDARY', 'DEPT003', 'EMP000002', NULL,
     NULL, 'EMP000012', 'プロジェクト支援', '2023-01-01',
     NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_EmployeeDepartment ORDER BY created_at DESC;
