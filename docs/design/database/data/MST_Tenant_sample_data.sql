-- MST_Tenant (テナント（組織）) サンプルデータ
-- 生成日時: 2025-06-04 06:57:02

INSERT INTO MST_Tenant (
    tenant_id, tenant_code, tenant_name, tenant_name_en,
    tenant_short_name, tenant_type, parent_tenant_id, tenant_level,
    domain_name, subdomain, logo_url, primary_color,
    secondary_color, timezone, locale, currency_code,
    date_format, time_format, admin_email, contact_email,
    phone_number, address, postal_code, country_code,
    subscription_plan, max_users, max_storage_gb, features_enabled,
    custom_settings, security_policy, data_retention_days, backup_enabled,
    backup_frequency, contract_start_date, contract_end_date, trial_end_date,
    billing_cycle, monthly_fee, setup_fee, status,
    activation_date, suspension_date, suspension_reason, last_login_date,
    current_users_count, storage_used_gb, api_rate_limit, sso_enabled,
    sso_provider, sso_config, webhook_url, webhook_secret,
    created_by, notes, code, name,
    description
) VALUES
    ('TENANT_001', 'acme-corp', '株式会社ACME', 'ACME Corporation',
     'ACME', 'ENTERPRISE', NULL, 1,
     'acme-corp.com', 'acme', 'https://cdn.example.com/logos/acme-corp.png', '#0066CC',
     '#FF6600', 'Asia/Tokyo', 'ja_JP', 'JPY',
     'YYYY-MM-DD', 'HH:mm:ss', 'admin@acme-corp.com', 'contact@acme-corp.com',
     '03-1234-5678', '東京都千代田区丸の内1-1-1', '100-0005', 'JP',
     'ENTERPRISE', 1000, 1000, '["advanced_analytics", "custom_reports", "api_access", "sso", "audit_logs"]',
     '{"theme": "corporate", "dashboard_layout": "advanced", "notification_preferences": {"email": true, "slack": true}}', '{"password_policy": {"min_length": 8, "require_special_chars": true}, "session_timeout": 480, "ip_whitelist": ["192.168.1.0/24"]}', 2555, TRUE,
     'DAILY', '2024-01-01', '2024-12-31', NULL,
     'ANNUAL', 50000.0, 100000.0, 'ACTIVE',
     '2024-01-01', NULL, NULL, '2024-06-01',
     250, 125.5, 10000, TRUE,
     'SAML', '{"entity_id": "acme-corp", "sso_url": "https://sso.acme-corp.com/saml", "certificate": "..."}', 'https://api.acme-corp.com/webhooks/skill-system', 'webhook_secret_key_123',
     'SYSTEM', '大手企業向けエンタープライズプラン', NULL, NULL,
     NULL),
    ('TENANT_002', 'beta-tech', 'ベータテクノロジー株式会社', 'Beta Technology Inc.',
     'BetaTech', 'ENTERPRISE', NULL, 1,
     NULL, 'beta-tech', 'https://cdn.example.com/logos/beta-tech.png', '#28A745',
     '#6C757D', 'Asia/Tokyo', 'ja_JP', 'JPY',
     'YYYY/MM/DD', 'HH:mm', 'admin@beta-tech.co.jp', 'info@beta-tech.co.jp',
     '06-9876-5432', '大阪府大阪市北区梅田2-2-2', '530-0001', 'JP',
     'STANDARD', 200, 100, '["basic_analytics", "standard_reports", "api_access"]',
     '{"theme": "modern", "dashboard_layout": "standard"}', '{"password_policy": {"min_length": 6, "require_special_chars": false}, "session_timeout": 240}', 1825, TRUE,
     'WEEKLY', '2024-03-01', '2025-02-28', NULL,
     'MONTHLY', 15000.0, 30000.0, 'ACTIVE',
     '2024-03-01', NULL, NULL, '2024-05-30',
     85, 23.75, 2000, FALSE,
     NULL, NULL, NULL, NULL,
     'SYSTEM', '中堅企業向けスタンダードプラン', NULL, NULL,
     NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_Tenant ORDER BY created_at DESC;
