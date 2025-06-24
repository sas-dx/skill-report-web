-- MST_EmployeePosition (社員役職関連) サンプルデータ
-- 生成日時: 2025-06-24 22:56:14

INSERT INTO MST_EmployeePosition (
    id, tenant_id, appointment_reason, appointment_status,
    appointment_type, approval_status, approved_at, approved_by,
    authority_level, delegation_authority, employee_id, employeeposition_id,
    end_date, performance_target, position_id, responsibility_scope,
    salary_grade, start_date, is_deleted, created_at,
    updated_at
) VALUES
    (NULL, NULL, '新卒入社時任命', 'ACTIVE',
     'PRIMARY', 'APPROVED', '2020-03-25 10:00:00', 'EMP000010',
     5, '{"budget_approval": 1000000, "hiring_authority": true, "performance_evaluation": true}', 'EMP000001', NULL,
     NULL, 'チーム生産性20%向上、メンバー育成2名', 'POS001', 'チーム運営、メンバー指導、プロジェクト管理',
     'G5', '2020-04-01', NULL, NULL,
     NULL),
    (NULL, NULL, '新卒入社時任命', 'INACTIVE',
     'PRIMARY', 'APPROVED', '2021-03-25 10:00:00', 'EMP000011',
     3, '{"code_review": true, "technical_decision": false}', 'EMP000002', NULL,
     '2023-03-31', '開発効率向上、技術スキル習得', 'POS002', 'システム開発、技術調査',
     'G3', '2021-04-01', NULL, NULL,
     NULL),
    (NULL, NULL, '昇進による任命', 'ACTIVE',
     'PRIMARY', 'APPROVED', '2023-03-20 14:00:00', 'EMP000011',
     4, '{"technical_decision": true, "architecture_review": true}', 'EMP000002', NULL,
     NULL, '技術品質向上、後輩指導3名', 'POS003', 'シニア開発者、技術指導、アーキテクチャ設計',
     'G4', '2023-04-01', NULL, NULL,
     NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_EmployeePosition ORDER BY created_at DESC;
