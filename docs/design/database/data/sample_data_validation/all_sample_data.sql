-- 全テーブル サンプルデータ INSERT文
-- 生成日時: unknown
-- 対象テーブル数: 2
-- 生成テーブル数: 2
-- 総レコード数: 4

-- 実行順序:
--  1. MST_Department
--  2. MST_Employee

BEGIN;

-- MST_Department (2件)
INSERT INTO MST_Department (department_code, department_name, department_name_short, parent_department_id, department_level, department_type, manager_id, deputy_manager_id, cost_center_code, budget_amount, location, phone_number, email_address, establishment_date, abolition_date, department_status, sort_order, description, id, created_at, updated_at, is_deleted) VALUES ('DEPT001', '経営企画本部', '経営企画', NULL, 1, 'HEADQUARTERS', 'EMP000001', NULL, 'CC001', 50000000.0, '本社ビル 10F', '03-1234-5678', 'planning@company.com', '2020-04-01', NULL, 'ACTIVE', 1, '会社全体の経営戦略立案・推進を担当', 'mst_f1962495', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO MST_Department (department_code, department_name, department_name_short, parent_department_id, department_level, department_type, manager_id, deputy_manager_id, cost_center_code, budget_amount, location, phone_number, email_address, establishment_date, abolition_date, department_status, sort_order, description, id, created_at, updated_at, is_deleted) VALUES ('DEPT002', 'システム開発部', 'システム開発', 'DEPT001', 2, 'DEPARTMENT', 'EMP000002', 'EMP000003', 'CC002', 120000000.0, '本社ビル 8F', '03-1234-5679', 'dev@company.com', '2020-04-01', NULL, 'ACTIVE', 2, '社内システムの開発・保守・運用を担当', 'mst_60da828a', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);

-- MST_Employee (2件)
INSERT INTO MST_Employee (id, employee_code, full_name, full_name_kana, email, phone, hire_date, birth_date, gender, department_id, position_id, job_type_id, employment_status, manager_id, employee_status, is_deleted, created_at, updated_at) VALUES ('emp_001', 'EMP000001', '山田太郎', 'ヤマダタロウ', 'yamada.taro@example.com', '090-1234-5678', '2020-04-01', '1990-01-15', 'M', 'dept_001', 'pos_003', 'job_001', 'FULL_TIME', 'emp_002', 'ACTIVE', FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO MST_Employee (id, employee_code, full_name, full_name_kana, email, phone, hire_date, birth_date, gender, department_id, position_id, job_type_id, employment_status, manager_id, employee_status, is_deleted, created_at, updated_at) VALUES ('emp_002', 'EMP000002', '佐藤花子', 'サトウハナコ', 'sato.hanako@example.com', '090-2345-6789', '2018-04-01', '1985-03-20', 'F', 'dept_001', 'pos_002', 'job_001', 'FULL_TIME', NULL, 'ACTIVE', FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

COMMIT;

-- 全テーブル サンプルデータ終了