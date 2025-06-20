-- サンプルデータ INSERT文: MST_Employee
-- 生成日時: 2025-06-20 00:12:02
-- レコード数: 2

INSERT INTO MST_Employee (id, employee_code, full_name, full_name_kana, email, phone, hire_date, birth_date, gender, department_id, position_id, job_type_id, employment_status, manager_id, employee_status, is_deleted) VALUES ('emp_001', 'EMP000001', '山田太郎', 'ヤマダタロウ', 'yamada.taro@example.com', '090-1234-5678', '2020-04-01', '1990-01-15', 'M', 'dept_001', 'pos_003', 'job_001', 'FULL_TIME', 'emp_002', 'ACTIVE', FALSE);
INSERT INTO MST_Employee (id, employee_code, full_name, full_name_kana, email, phone, hire_date, birth_date, gender, department_id, position_id, job_type_id, employment_status, manager_id, employee_status, is_deleted) VALUES ('emp_002', 'EMP000002', '佐藤花子', 'サトウハナコ', 'sato.hanako@example.com', '090-2345-6789', '2018-04-01', '1985-03-20', 'F', 'dept_001', 'pos_002', 'job_001', 'FULL_TIME', NULL, 'ACTIVE', FALSE);

-- MST_Employee サンプルデータ終了
