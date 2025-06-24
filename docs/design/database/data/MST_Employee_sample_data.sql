-- MST_Employee (社員基本情報) サンプルデータ
-- 生成日時: 2025-06-24 22:56:15

INSERT INTO MST_Employee (
    id, tenant_id, employee_code, full_name,
    full_name_kana, email, phone, birth_date,
    gender, hire_date, department_id, position_id,
    job_type_id, manager_id, employment_status, employee_status,
    is_deleted, created_at, updated_at
) VALUES
    ('emp_001', NULL, 'EMP000001', '山田太郎',
     'ヤマダタロウ', 'yamada.taro@example.com', '090-1234-5678', '1990-01-15',
     'M', '2020-04-01', 'dept_001', 'pos_003',
     'job_001', 'emp_002', 'FULL_TIME', 'ACTIVE',
     FALSE, NULL, NULL),
    ('emp_002', NULL, 'EMP000002', '佐藤花子',
     'サトウハナコ', 'sato.hanako@example.com', '090-2345-6789', '1985-03-20',
     'F', '2018-04-01', 'dept_001', 'pos_002',
     'job_001', NULL, 'FULL_TIME', 'ACTIVE',
     FALSE, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_Employee ORDER BY created_at DESC;
