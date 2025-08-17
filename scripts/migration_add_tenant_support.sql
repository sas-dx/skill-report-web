-- マルチテナント対応マイグレーション
-- 要求仕様ID: TNT.1-MGMT.1, TNT.2-ISOL.1

-- 1. デフォルトテナントを作成（既存データ用）
INSERT INTO "MST_Tenant" (
  tenant_id,
  tenant_code,
  tenant_name,
  tenant_name_kana,
  tenant_type,
  domain,
  subdomain,
  contact_email,
  contract_start_date,
  user_limit,
  storage_limit_gb,
  tenant_status,
  activation_date,
  total_users,
  total_storage_used_gb,
  timezone,
  locale,
  created_at,
  updated_at,
  is_deleted
) VALUES (
  'default-tenant',
  'DEFAULT',
  'デフォルトテナント',
  'デフォルトテナント',
  'STANDARD',
  'localhost',
  'default',
  'admin@localhost',
  CURRENT_TIMESTAMP,
  100,
  10,
  'ACTIVE',
  CURRENT_TIMESTAMP,
  0,
  0,
  'Asia/Tokyo',
  'ja',
  CURRENT_TIMESTAMP,
  CURRENT_TIMESTAMP,
  false
) ON CONFLICT (tenant_code) DO NOTHING;

-- 2. 既存のMST_Tenantテーブルのカラムを更新
ALTER TABLE "MST_Tenant" 
  ADD COLUMN IF NOT EXISTS company_info JSONB,
  ADD COLUMN IF NOT EXISTS contact_person VARCHAR(255),
  ADD COLUMN IF NOT EXISTS contact_phone VARCHAR(255),
  ADD COLUMN IF NOT EXISTS billing_plan_id VARCHAR(255),
  ADD COLUMN IF NOT EXISTS user_limit INTEGER DEFAULT 100,
  ADD COLUMN IF NOT EXISTS storage_limit_gb INTEGER DEFAULT 10,
  ADD COLUMN IF NOT EXISTS monthly_fee DECIMAL(10,2),
  ADD COLUMN IF NOT EXISTS payment_method VARCHAR(255),
  ADD COLUMN IF NOT EXISTS payment_status VARCHAR(255) DEFAULT 'ACTIVE',
  ADD COLUMN IF NOT EXISTS features_enabled JSONB,
  ADD COLUMN IF NOT EXISTS api_key VARCHAR(255),
  ADD COLUMN IF NOT EXISTS webhook_url VARCHAR(255),
  ADD COLUMN IF NOT EXISTS custom_logo_url VARCHAR(255),
  ADD COLUMN IF NOT EXISTS theme_color VARCHAR(255),
  ADD COLUMN IF NOT EXISTS timezone VARCHAR(255) DEFAULT 'Asia/Tokyo',
  ADD COLUMN IF NOT EXISTS locale VARCHAR(255) DEFAULT 'ja',
  ADD COLUMN IF NOT EXISTS security_settings JSONB,
  ADD COLUMN IF NOT EXISTS notification_settings JSONB,
  ADD COLUMN IF NOT EXISTS tenant_status VARCHAR(255) DEFAULT 'ACTIVE',
  ADD COLUMN IF NOT EXISTS activation_date TIMESTAMP,
  ADD COLUMN IF NOT EXISTS suspension_date TIMESTAMP,
  ADD COLUMN IF NOT EXISTS suspension_reason TEXT,
  ADD COLUMN IF NOT EXISTS last_login_at TIMESTAMP,
  ADD COLUMN IF NOT EXISTS total_users INTEGER DEFAULT 0,
  ADD COLUMN IF NOT EXISTS total_storage_used_gb DECIMAL(10,2) DEFAULT 0,
  ADD COLUMN IF NOT EXISTS metadata JSONB,
  ADD COLUMN IF NOT EXISTS domain VARCHAR(255),
  ADD COLUMN IF NOT EXISTS subdomain VARCHAR(255),
  ADD COLUMN IF NOT EXISTS tenant_type VARCHAR(255) DEFAULT 'STANDARD';

-- 3. MST_TenantSettingsテーブルに必要なカラムを追加
ALTER TABLE "MST_TenantSettings" 
  ADD COLUMN IF NOT EXISTS setting_type VARCHAR(255),
  ADD COLUMN IF NOT EXISTS is_encrypted BOOLEAN DEFAULT false,
  ADD COLUMN IF NOT EXISTS description TEXT,
  ADD COLUMN IF NOT EXISTS default_value TEXT,
  ADD COLUMN IF NOT EXISTS allowed_values TEXT[],
  ADD COLUMN IF NOT EXISTS validation_rule TEXT,
  ADD COLUMN IF NOT EXISTS requires_restart BOOLEAN DEFAULT false,
  ADD COLUMN IF NOT EXISTS is_system_setting BOOLEAN DEFAULT false,
  ADD COLUMN IF NOT EXISTS is_user_configurable BOOLEAN DEFAULT true,
  ADD COLUMN IF NOT EXISTS display_order INTEGER,
  ADD COLUMN IF NOT EXISTS effective_from TIMESTAMP,
  ADD COLUMN IF NOT EXISTS effective_until TIMESTAMP,
  ADD COLUMN IF NOT EXISTS last_modified_by VARCHAR(255);

-- 4. 既存テーブルにtenant_idカラムを追加（デフォルト値付き）
ALTER TABLE "MST_Employee" 
  ADD COLUMN IF NOT EXISTS tenant_id VARCHAR(255) DEFAULT 'default-tenant';

ALTER TABLE "MST_Department" 
  ADD COLUMN IF NOT EXISTS tenant_id VARCHAR(255) DEFAULT 'default-tenant';

ALTER TABLE "MST_CareerPlan" 
  ADD COLUMN IF NOT EXISTS tenant_id VARCHAR(255) DEFAULT 'default-tenant';

ALTER TABLE "TRN_SkillRecord" 
  ADD COLUMN IF NOT EXISTS tenant_id VARCHAR(255) DEFAULT 'default-tenant';

ALTER TABLE "TRN_ProjectRecord" 
  ADD COLUMN IF NOT EXISTS tenant_id VARCHAR(255) DEFAULT 'default-tenant';

ALTER TABLE "TRN_TrainingHistory" 
  ADD COLUMN IF NOT EXISTS tenant_id VARCHAR(255) DEFAULT 'default-tenant';

ALTER TABLE "TRN_GoalProgress" 
  ADD COLUMN IF NOT EXISTS tenant_id VARCHAR(255) DEFAULT 'default-tenant';

ALTER TABLE "TRN_Notification" 
  ADD COLUMN IF NOT EXISTS tenant_id VARCHAR(255) DEFAULT 'default-tenant';

ALTER TABLE "MST_UserAuth" 
  ADD COLUMN IF NOT EXISTS tenant_id VARCHAR(255) DEFAULT 'default-tenant';

ALTER TABLE "MST_UserRole" 
  ADD COLUMN IF NOT EXISTS tenant_id VARCHAR(255) DEFAULT 'default-tenant';

ALTER TABLE "MST_RolePermission" 
  ADD COLUMN IF NOT EXISTS tenant_id VARCHAR(255) DEFAULT 'default-tenant';

-- 5. 既存データのtenant_idを更新
UPDATE "MST_Employee" SET tenant_id = 'default-tenant' WHERE tenant_id IS NULL;
UPDATE "MST_Department" SET tenant_id = 'default-tenant' WHERE tenant_id IS NULL;
UPDATE "MST_CareerPlan" SET tenant_id = 'default-tenant' WHERE tenant_id IS NULL;
UPDATE "TRN_SkillRecord" SET tenant_id = 'default-tenant' WHERE tenant_id IS NULL;
UPDATE "TRN_ProjectRecord" SET tenant_id = 'default-tenant' WHERE tenant_id IS NULL;
UPDATE "TRN_TrainingHistory" SET tenant_id = 'default-tenant' WHERE tenant_id IS NULL;
UPDATE "TRN_GoalProgress" SET tenant_id = 'default-tenant' WHERE tenant_id IS NULL;
UPDATE "TRN_Notification" SET tenant_id = 'default-tenant' WHERE tenant_id IS NULL;
UPDATE "MST_UserAuth" SET tenant_id = 'default-tenant' WHERE tenant_id IS NULL;
UPDATE "MST_UserRole" SET tenant_id = 'default-tenant' WHERE tenant_id IS NULL;
UPDATE "MST_RolePermission" SET tenant_id = 'default-tenant' WHERE tenant_id IS NULL;

-- 6. デフォルト値を削除してNOT NULL制約を追加
ALTER TABLE "MST_Employee" 
  ALTER COLUMN tenant_id DROP DEFAULT,
  ALTER COLUMN tenant_id SET NOT NULL;

ALTER TABLE "MST_Department" 
  ALTER COLUMN tenant_id DROP DEFAULT,
  ALTER COLUMN tenant_id SET NOT NULL;

ALTER TABLE "MST_CareerPlan" 
  ALTER COLUMN tenant_id DROP DEFAULT,
  ALTER COLUMN tenant_id SET NOT NULL;

-- 7. ユニーク制約を追加
ALTER TABLE "MST_Employee" 
  DROP CONSTRAINT IF EXISTS "MST_Employee_employee_code_key",
  DROP CONSTRAINT IF EXISTS "MST_Employee_email_key";

ALTER TABLE "MST_Employee" 
  ADD CONSTRAINT "MST_Employee_tenant_id_employee_code_key" UNIQUE (tenant_id, employee_code),
  ADD CONSTRAINT "MST_Employee_tenant_id_email_key" UNIQUE (tenant_id, email);

ALTER TABLE "MST_Department" 
  ADD CONSTRAINT "MST_Department_tenant_id_department_code_key" UNIQUE (tenant_id, department_code);

ALTER TABLE "MST_Tenant" 
  ADD CONSTRAINT "MST_Tenant_domain_key" UNIQUE (domain),
  ADD CONSTRAINT "MST_Tenant_api_key_key" UNIQUE (api_key);

ALTER TABLE "MST_TenantSettings" 
  ADD CONSTRAINT "MST_TenantSettings_tenant_id_setting_category_setting_key_key" 
  UNIQUE (tenant_id, setting_category, setting_key);

-- 8. インデックスを追加
CREATE INDEX IF NOT EXISTS "MST_Employee_tenant_id_idx" ON "MST_Employee" (tenant_id);
CREATE INDEX IF NOT EXISTS "MST_Department_tenant_id_idx" ON "MST_Department" (tenant_id);
CREATE INDEX IF NOT EXISTS "MST_CareerPlan_tenant_id_idx" ON "MST_CareerPlan" (tenant_id);
CREATE INDEX IF NOT EXISTS "TRN_SkillRecord_tenant_id_idx" ON "TRN_SkillRecord" (tenant_id);
CREATE INDEX IF NOT EXISTS "TRN_ProjectRecord_tenant_id_idx" ON "TRN_ProjectRecord" (tenant_id);
CREATE INDEX IF NOT EXISTS "TRN_TrainingHistory_tenant_id_idx" ON "TRN_TrainingHistory" (tenant_id);
CREATE INDEX IF NOT EXISTS "TRN_GoalProgress_tenant_id_idx" ON "TRN_GoalProgress" (tenant_id);
CREATE INDEX IF NOT EXISTS "TRN_Notification_tenant_id_idx" ON "TRN_Notification" (tenant_id);

-- 9. デフォルトテナントの設定を追加
INSERT INTO "MST_TenantSettings" (
  id,
  tenant_id,
  setting_category,
  setting_key,
  setting_value,
  setting_type,
  description,
  default_value,
  is_system_setting,
  created_at,
  updated_at,
  is_deleted
) VALUES 
  (gen_random_uuid(), 'default-tenant', 'AUTH', 'SESSION_TIMEOUT', '86400', 'NUMBER', 'セッションタイムアウト（秒）', '86400', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, false),
  (gen_random_uuid(), 'default-tenant', 'AUTH', 'PASSWORD_MIN_LENGTH', '8', 'NUMBER', 'パスワード最小文字数', '8', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, false),
  (gen_random_uuid(), 'default-tenant', 'NOTIFICATION', 'EMAIL_ENABLED', 'false', 'BOOLEAN', 'メール通知有効化', 'false', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, false),
  (gen_random_uuid(), 'default-tenant', 'UI', 'THEME', 'light', 'STRING', 'UIテーマ', 'light', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, false)
ON CONFLICT (tenant_id, setting_category, setting_key) DO NOTHING;

-- 10. 既存のUserAuthにパスワードを設定（開発用）
UPDATE "MST_UserAuth" 
SET password_hash = '$2a$10$YourHashedPasswordHere' -- 実際には bcrypt でハッシュ化したパスワード
WHERE password_hash IS NULL OR password_hash = '';

-- マイグレーション完了
SELECT 'Migration completed successfully' AS status;