-- HIS_TenantBilling (テナント課金履歴) サンプルデータ
-- 生成日時: 2025-06-24 22:56:15

INSERT INTO HIS_TenantBilling (
    id, tenant_id, plan_name, additional_amount,
    base_amount, billing_period_end, billing_period_start, billing_status,
    billing_type, currency_code, discount_amount, due_date,
    invoice_date, invoice_number, notes, paid_date,
    payment_method, plan_id, subtotal_amount, tax_amount,
    tax_rate, tenantbilling_id, total_amount, usage_amount,
    usage_details, is_deleted, created_at, updated_at
) VALUES
    ('TB001', 'TENANT001', 'スタンダードプラン', 5000.0,
     50000.0, '2025-05-31', '2025-05-01', 'PAID',
     'MONTHLY', 'JPY', 3000.0, '2025-06-30',
     '2025-06-01', 'INV-2025-05-001', '5月分月額利用料金', '2025-06-15',
     'CREDIT_CARD', 'PLAN_STANDARD', 67000.0, 6700.0,
     0.1, NULL, 73700.0, 15000.0,
     '{"users": 25, "storage_gb": 150, "api_calls": 50000}', NULL, NULL, NULL),
    ('TB002', 'TENANT002', 'エンタープライズプラン', 0.0,
     100000.0, '2025-05-31', '2025-05-01', 'INVOICED',
     'USAGE', 'JPY', 10000.0, '2025-06-30',
     '2025-06-01', 'INV-2025-05-002', '5月分従量課金（大容量利用）', NULL,
     'BANK_TRANSFER', 'PLAN_ENTERPRISE', 135000.0, 13500.0,
     0.1, NULL, 148500.0, 45000.0,
     '{"users": 100, "storage_gb": 500, "api_calls": 200000, "premium_features": true}', NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM HIS_TenantBilling ORDER BY created_at DESC;
