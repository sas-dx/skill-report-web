-- MST_EmployeePosition (社員役職関連) サンプルデータ
-- 生成日時: 2025-06-21 17:20:34

INSERT INTO MST_EmployeePosition (
    employee_id, position_id, appointment_type, start_date,
    end_date, appointment_reason, responsibility_scope, authority_level,
    salary_grade, appointment_status, approval_status, approved_by,
    approved_at, performance_target, delegation_authority, created_at,
    updated_at
) VALUES
    ('EMP000001', 'POS001', 'PRIMARY', '2020-04-01',
     NULL, '新卒入社時任命', 'チーム運営、メンバー指導、プロジェクト管理', 5,
     'G5', 'ACTIVE', 'APPROVED', 'EMP000010',
     '2020-03-25 10:00:00', 'チーム生産性20%向上、メンバー育成2名', '{"budget_approval": 1000000, "hiring_authority": true, "performance_evaluation": true}', NULL,
     NULL),
    ('EMP000002', 'POS002', 'PRIMARY', '2021-04-01',
     '2023-03-31', '新卒入社時任命', 'システム開発、技術調査', 3,
     'G3', 'INACTIVE', 'APPROVED', 'EMP000011',
     '2021-03-25 10:00:00', '開発効率向上、技術スキル習得', '{"code_review": true, "technical_decision": false}', NULL,
     NULL),
    ('EMP000002', 'POS003', 'PRIMARY', '2023-04-01',
     NULL, '昇進による任命', 'シニア開発者、技術指導、アーキテクチャ設計', 4,
     'G4', 'ACTIVE', 'APPROVED', 'EMP000011',
     '2023-03-20 14:00:00', '技術品質向上、後輩指導3名', '{"technical_decision": true, "architecture_review": true}', NULL,
     NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_EmployeePosition ORDER BY created_at DESC;
