/**
 * Prisma Database Seed Script
 * 要求仕様ID: PLT.1-DB.1
 * 対応設計書: docs/design/database/ddl/
 * 実装日: 2025-06-06
 * 実装者: AI Assistant
 */

import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 データベースの初期データ投入を開始します...');

  try {
    console.log("📊 MST_Tenantデータを投入中...");
    await Promise.all([
      prisma.tenant.upsert({
        where: { tenant_id: "TENANT_001" },
        update: {},
        create: {
          tenant_id: "TENANT_001",
          tenant_code: "alpha-corp",
          tenant_name: "アルファコーポレーション株式会社",
          tenant_name_en: "Alpha Corporation Inc.",
          tenant_short_name: "AlphaCorp",
          tenant_type: "ENTERPRISE",
          tenant_level: 1,
          domain_name: "alpha-corp.com",
          subdomain: "alpha-corp",
          logo_url: "https://cdn.example.com/logos/alpha-corp.png",
          primary_color: "#007BFF",
          secondary_color: "#6C757D",
          timezone: "Asia/Tokyo",
          locale: "ja_JP",
          currency_code: "JPY",
          date_format: "YYYY/MM/DD",
          time_format: "HH:mm",
          admin_email: "admin@alpha-corp.com",
          contact_email: "info@alpha-corp.com",
          phone_number: "03-1234-5678",
          address: "東京都千代田区丸の内1-1-1",
          postal_code: "100-0005",
          country_code: "JP",
          subscription_plan: "ENTERPRISE",
          max_users: 500,
          max_storage_gb: 500,
          features_enabled: "[\"advanced_analytics\", \"custom_reports\", \"api_access\", \"sso\", \"audit_logs\"]",
          custom_settings: "{\"theme\": \"corporate\", \"dashboard_layout\": \"advanced\", \"notification_preferences\": {\"email\": true, \"slack\": true}}",
          security_policy: "{\"password_policy\": {\"min_length\": 8, \"require_special_chars\": true, \"require_numbers\": true}, \"session_timeout\": 480, \"mfa_required\": true}",
          data_retention_days: 2555,
          backup_enabled: true,
          backup_frequency: "DAILY",
          contract_start_date: "2024-01-01T00:00:00Z",
          contract_end_date: "2024-12-31T23:59:59Z",
          billing_cycle: "ANNUAL",
          monthly_fee: 50000.00,
          setup_fee: 100000.00,
          status: "ACTIVE",
          activation_date: "2024-01-01T00:00:00Z",
          last_login_date: "2024-06-01T09:00:00Z",
          current_users_count: 250,
          storage_used_gb: 125.50,
          api_rate_limit: 5000,
          sso_enabled: true,
          sso_provider: "Azure AD",
          sso_config: "{\"tenant_id\": \"azure-tenant-123\", \"client_id\": \"client-456\"}",
          created_by: "SYSTEM",
          code: "ALPHA",
          name: "Alpha Corporation",
          description: "大手企業向けエンタープライズプラン"
        }
      }),
      prisma.tenant.upsert({
        where: { tenant_id: "TENANT_002" },
        update: {},
        create: {
          tenant_id: "TENANT_002",
          tenant_code: "beta-tech",
          tenant_name: "ベータテクノロジー株式会社",
          tenant_name_en: "Beta Technology Inc.",
          tenant_short_name: "BetaTech",
          tenant_type: "ENTERPRISE",
          tenant_level: 1,
          subdomain: "beta-tech",
          logo_url: "https://cdn.example.com/logos/beta-tech.png",
          primary_color: "#28A745",
          secondary_color: "#6C757D",
          timezone: "Asia/Tokyo",
          locale: "ja_JP",
          currency_code: "JPY",
          date_format: "YYYY/MM/DD",
          time_format: "HH:mm",
          admin_email: "admin@beta-tech.co.jp",
          contact_email: "info@beta-tech.co.jp",
          phone_number: "06-9876-5432",
          address: "大阪府大阪市北区梅田2-2-2",
          postal_code: "530-0001",
          country_code: "JP",
          subscription_plan: "STANDARD",
          max_users: 200,
          max_storage_gb: 100,
          features_enabled: "[\"basic_analytics\", \"standard_reports\", \"api_access\"]",
          custom_settings: "{\"theme\": \"modern\", \"dashboard_layout\": \"standard\"}",
          security_policy: "{\"password_policy\": {\"min_length\": 6, \"require_special_chars\": false}, \"session_timeout\": 240}",
          data_retention_days: 1825,
          backup_enabled: true,
          backup_frequency: "WEEKLY",
          contract_start_date: "2024-03-01T00:00:00Z",
          contract_end_date: "2025-02-28T23:59:59Z",
          billing_cycle: "MONTHLY",
          monthly_fee: 15000.00,
          setup_fee: 30000.00,
          status: "ACTIVE",
          activation_date: "2024-03-01T00:00:00Z",
          last_login_date: "2024-05-30T14:30:00Z",
          current_users_count: 85,
          storage_used_gb: 23.75,
          api_rate_limit: 2000,
          sso_enabled: false,
          created_by: "SYSTEM",
          code: "BETA",
          name: "Beta Technology",
          description: "中堅企業向けスタンダードプラン"
        }
      })
    ]);

    console.log('✅ 初期データ投入が完了しました！');
  } catch (error) {
    console.error('❌ 初期データ投入中にエラーが発生しました:', error);
    throw error;
  }
}

main()
  .catch((e) => {
    console.error('❌ 初期データ投入中にエラーが発生しました:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
