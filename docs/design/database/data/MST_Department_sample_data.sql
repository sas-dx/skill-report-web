-- MST_Department (部署マスタ) サンプルデータ
-- 生成日時: 2025-06-24 23:05:57

INSERT INTO MST_Department (
    id, tenant_id, abolition_date, budget_amount,
    cost_center_code, department_code, department_id, department_level,
    department_name, department_name_short, department_status, department_type,
    deputy_manager_id, description, email_address, establishment_date,
    location, manager_id, parent_department_id, phone_number,
    sort_order, is_deleted, created_at, updated_at
) VALUES
    (NULL, NULL, NULL, 50000000.0,
     'CC001', 'DEPT001', NULL, 1,
     '経営企画本部', '経営企画', 'ACTIVE', 'HEADQUARTERS',
     NULL, '会社全体の経営戦略立案・推進を担当', 'planning@company.com', '2020-04-01',
     '本社ビル 10F', 'EMP000001', NULL, '03-1234-5678',
     1, NULL, NULL, NULL),
    (NULL, NULL, NULL, 120000000.0,
     'CC002', 'DEPT002', NULL, 2,
     'システム開発部', 'システム開発', 'ACTIVE', 'DEPARTMENT',
     'EMP000003', '社内システムの開発・保守・運用を担当', 'dev@company.com', '2020-04-01',
     '本社ビル 8F', 'EMP000002', 'DEPT001', '03-1234-5679',
     2, NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_Department ORDER BY created_at DESC;
