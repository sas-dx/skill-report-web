-- TRN_EmployeeSkillGrade (社員スキルグレード) サンプルデータ
-- 生成日時: 2025-06-24 23:05:57

INSERT INTO TRN_EmployeeSkillGrade (
    id, tenant_id, certification_flag, effective_date,
    employee_id, employeeskillgrade_id, evaluation_comment, evaluation_date,
    evaluator_id, expiry_date, job_type_id, next_evaluation_date,
    skill_grade, skill_level, is_deleted, created_at,
    created_by, updated_by, updated_at
) VALUES
    (NULL, NULL, TRUE, '2024-04-01',
     'EMP000001', NULL, '優秀な技術力と指導力を発揮している', '2024-03-15',
     'EMP000010', NULL, 'JOB001', '2025-04-01',
     'A', 4, NULL, NULL,
     NULL, NULL, NULL),
    (NULL, NULL, TRUE, '2024-04-01',
     'EMP000002', NULL, '着実にスキルアップしており、次のレベルが期待される', '2024-03-20',
     'EMP000001', NULL, 'JOB002', '2025-04-01',
     'B', 3, NULL, NULL,
     NULL, NULL, NULL),
    (NULL, NULL, TRUE, '2023-04-01',
     'EMP000001', NULL, '前年度からの成長が顕著', '2023-03-15',
     'EMP000010', '2024-03-31', 'JOB001', '2024-04-01',
     'B', 3, NULL, NULL,
     NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM TRN_EmployeeSkillGrade ORDER BY created_at DESC;
