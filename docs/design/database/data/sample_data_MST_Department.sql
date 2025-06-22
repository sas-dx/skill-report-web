-- サンプルデータ INSERT文: MST_Department
-- 生成日時: 2025-06-21 22:54:41
-- レコード数: 2

INSERT INTO MST_Department (department_code, department_name, department_name_short, parent_department_id, department_level, department_type, manager_id, deputy_manager_id, cost_center_code, budget_amount, location, phone_number, email_address, establishment_date, abolition_date, department_status, sort_order, description, id, created_at, updated_at, is_deleted) VALUES ('DEPT001', '経営企画本部', '経営企画', NULL, 1, 'HEADQUARTERS', 'EMP000001', NULL, 'CC001', 50000000.0, '本社ビル 10F', '03-1234-5678', 'planning@company.com', '2020-04-01', NULL, 'ACTIVE', 1, '会社全体の経営戦略立案・推進を担当', 'mst_6735a783', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO MST_Department (department_code, department_name, department_name_short, parent_department_id, department_level, department_type, manager_id, deputy_manager_id, cost_center_code, budget_amount, location, phone_number, email_address, establishment_date, abolition_date, department_status, sort_order, description, id, created_at, updated_at, is_deleted) VALUES ('DEPT002', 'システム開発部', 'システム開発', 'DEPT001', 2, 'DEPARTMENT', 'EMP000002', 'EMP000003', 'CC002', 120000000.0, '本社ビル 8F', '03-1234-5679', 'dev@company.com', '2020-04-01', NULL, 'ACTIVE', 2, '社内システムの開発・保守・運用を担当', 'mst_f0c90b9f', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);

-- MST_Department サンプルデータ終了
