-- サンプルデータ INSERT文: TRN_EmployeeSkillGrade
-- 生成日時: 2025-06-21 17:21:42
-- レコード数: 3

INSERT INTO TRN_EmployeeSkillGrade (employee_id, job_type_id, skill_grade, skill_level, effective_date, expiry_date, evaluation_date, evaluator_id, evaluation_comment, certification_flag, next_evaluation_date, id, created_at, updated_at, is_deleted) VALUES ('EMP000001', 'JOB001', 'A', 4, '2024-04-01', NULL, '2024-03-15', 'EMP000010', '優秀な技術力と指導力を発揮している', TRUE, '2025-04-01', 'trn_35276cec', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO TRN_EmployeeSkillGrade (employee_id, job_type_id, skill_grade, skill_level, effective_date, expiry_date, evaluation_date, evaluator_id, evaluation_comment, certification_flag, next_evaluation_date, id, created_at, updated_at, is_deleted) VALUES ('EMP000002', 'JOB002', 'B', 3, '2024-04-01', NULL, '2024-03-20', 'EMP000001', '着実にスキルアップしており、次のレベルが期待される', TRUE, '2025-04-01', 'trn_36abd328', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO TRN_EmployeeSkillGrade (employee_id, job_type_id, skill_grade, skill_level, effective_date, expiry_date, evaluation_date, evaluator_id, evaluation_comment, certification_flag, next_evaluation_date, id, created_at, updated_at, is_deleted) VALUES ('EMP000001', 'JOB001', 'B', 3, '2023-04-01', '2024-03-31', '2023-03-15', 'EMP000010', '前年度からの成長が顕著', TRUE, '2024-04-01', 'trn_82179674', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);

-- TRN_EmployeeSkillGrade サンプルデータ終了
