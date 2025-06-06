-- MST_Employee (社員基本情報) サンプルデータ
-- 生成日時: 2025-06-04 06:57:02

INSERT INTO MST_Employee (
    employee_code, full_name, full_name_kana, email,
    phone, hire_date, birth_date, gender,
    department_id, position_id, job_type_id, employment_status,
    manager_id, employee_status, code, name,
    description
) VALUES
    ('EMP000001', '山田太郎', 'ヤマダタロウ', 'yamada.taro@company.com',
     '090-1234-5678', '2020-04-01', '1990-01-15', 'M',
     'DEPT001', 'POS001', 'JOB001', 'FULL_TIME',
     NULL, 'ACTIVE', NULL, NULL,
     NULL),
    ('EMP000002', '佐藤花子', 'サトウハナコ', 'sato.hanako@company.com',
     '090-2345-6789', '2021-04-01', '1992-03-20', 'F',
     'DEPT002', 'POS002', 'JOB002', 'FULL_TIME',
     'EMP000001', 'ACTIVE', NULL, NULL,
     NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_Employee ORDER BY created_at DESC;
