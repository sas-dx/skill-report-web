-- HIS_TenantBilling (テナント課金履歴) サンプルデータ
-- 生成日時: 2025-06-04 06:57:02

INSERT INTO HIS_TenantBilling (
    id, tenant_id, billing_period_start, billing_period_end,
    billing_type, plan_id, plan_name, base_amount,
    usage_amount, additional_amount, discount_amount, subtotal_amount,
    tax_rate, tax_amount, total_amount, currency_code,
    usage_details, billing_status, invoice_number, invoice_date,
    due_date, paid_date, payment_method, notes,
    is_deleted
) VALUES
    ('TB001', 'TENANT001', '2025-05-01', '2025-05-31',
     'MONTHLY', 'PLAN_STANDARD', 'スタンダードプラン', 50000.0,
     15000.0, 5000.0, 3000.0, 67000.0,
     0.1, 6700.0, 73700.0, 'JPY',
     '{"users": 25, "storage_gb": 150, "api_calls": 50000}', 'PAID', 'INV-2025-05-001', '2025-06-01',
     '2025-06-30', '2025-06-15', 'CREDIT_CARD', '5月分月額利用料金',
     NULL),
    ('TB002', 'TENANT002', '2025-05-01', '2025-05-31',
     'USAGE', 'PLAN_ENTERPRISE', 'エンタープライズプラン', 100000.0,
     45000.0, 0.0, 10000.0, 135000.0,
     0.1, 13500.0, 148500.0, 'JPY',
     '{"users": 100, "storage_gb": 500, "api_calls": 200000, "premium_features": true}', 'INVOICED', 'INV-2025-05-002', '2025-06-01',
     '2025-06-30', NULL, 'BANK_TRANSFER', '5月分従量課金（大容量利用）',
     NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM HIS_TenantBilling ORDER BY created_at DESC;
