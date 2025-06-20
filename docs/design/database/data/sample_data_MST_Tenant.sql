-- サンプルデータ INSERT文: MST_Tenant
-- 生成日時: 2025-06-21 07:31:30
-- レコード数: 2

BEGIN;

INSERT INTO MST_Tenant (tenant_id, tenant_code, tenant_name, tenant_name_en, tenant_short_name, tenant_type, parent_tenant_id, tenant_level, domain_name, subdomain, logo_url, primary_color, secondary_color, timezone, locale, currency_code, admin_email, contact_email, phone_number, address, postal_code, country_code, subscription_plan, max_users, max_storage_gb, status, contract_start_date, contract_end_date, is_deleted, id, created_at, updated_at) VALUES ('tenant_001', 'main-corp', 'メイン株式会社', 'Main Corporation', 'メイン', 'ENTERPRISE', NULL, 1, 'main-corp.com', 'main', 'https://cdn.example.com/logos/main-corp.png', '#0066CC', '#FF6600', 'Asia/Tokyo', 'ja_JP', 'JPY', 'admin@main-corp.com', 'contact@main-corp.com', '03-1234-5678', '東京都千代田区丸の内1-1-1', '100-0005', 'JP', 'ENTERPRISE', 1000, 100, 'ACTIVE', '2025-04-01', NULL, FALSE, 'mst_76320e27', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO MST_Tenant (tenant_id, tenant_code, tenant_name, tenant_name_en, tenant_short_name, tenant_type, parent_tenant_id, tenant_level, domain_name, subdomain, logo_url, primary_color, secondary_color, timezone, locale, currency_code, admin_email, contact_email, phone_number, address, postal_code, country_code, subscription_plan, max_users, max_storage_gb, status, contract_start_date, contract_end_date, is_deleted, id, created_at, updated_at) VALUES ('tenant_002', 'sub-division', 'サブ事業部', 'Sub Division', 'サブ', 'DEPARTMENT', 'tenant_001', 2, NULL, 'sub', NULL, '#0066CC', '#FF6600', 'Asia/Tokyo', 'ja_JP', 'JPY', 'admin@sub.main-corp.com', NULL, NULL, NULL, NULL, 'JP', 'STANDARD', 100, 20, 'ACTIVE', '2025-04-01', NULL, FALSE, 'mst_e6e60057', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

COMMIT;

-- MST_Tenant サンプルデータ終了
