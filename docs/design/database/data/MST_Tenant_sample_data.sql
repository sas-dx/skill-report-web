-- MST_Tenant (テナント（組織）) サンプルデータ
-- 生成日時: 2025-06-24 23:02:18

INSERT INTO MST_Tenant (
    id, tenant_id, address, admin_email,
    contact_email, contract_end_date, contract_start_date, country_code,
    currency_code, domain_name, locale, logo_url,
    max_storage_gb, max_users, parent_tenant_id, phone_number,
    postal_code, primary_color, secondary_color, status,
    subdomain, subscription_plan, tenant_code, tenant_level,
    tenant_name, tenant_name_en, tenant_short_name, tenant_type,
    timezone, is_deleted, created_at, updated_at
) VALUES
    (NULL, 'tenant_001', '東京都千代田区丸の内1-1-1', 'admin@main-corp.com',
     'contact@main-corp.com', NULL, '2025-04-01', 'JP',
     'JPY', 'main-corp.com', 'ja_JP', 'https://cdn.example.com/logos/main-corp.png',
     100, 1000, NULL, '03-1234-5678',
     '100-0005', '#0066CC', '#FF6600', 'ACTIVE',
     'main', 'ENTERPRISE', 'main-corp', 1,
     'メイン株式会社', 'Main Corporation', 'メイン', 'ENTERPRISE',
     'Asia/Tokyo', FALSE, NULL, NULL),
    (NULL, 'tenant_002', NULL, 'admin@sub.main-corp.com',
     NULL, NULL, '2025-04-01', 'JP',
     'JPY', NULL, 'ja_JP', NULL,
     20, 100, 'tenant_001', NULL,
     NULL, '#0066CC', '#FF6600', 'ACTIVE',
     'sub', 'STANDARD', 'sub-division', 2,
     'サブ事業部', 'Sub Division', 'サブ', 'DEPARTMENT',
     'Asia/Tokyo', FALSE, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_Tenant ORDER BY created_at DESC;
