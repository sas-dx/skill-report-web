/*
  Warnings:

  - The primary key for the `HIS_TenantBilling` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `code` on the `MST_CareerPlan` table. All the data in the column will be lost.
  - You are about to drop the column `description` on the `MST_CareerPlan` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_CareerPlan` table. All the data in the column will be lost.
  - You are about to drop the column `code` on the `MST_Certification` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_Certification` table. All the data in the column will be lost.
  - You are about to drop the column `code` on the `MST_CertificationRequirement` table. All the data in the column will be lost.
  - You are about to drop the column `description` on the `MST_CertificationRequirement` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_CertificationRequirement` table. All the data in the column will be lost.
  - You are about to drop the column `code` on the `MST_Department` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_Department` table. All the data in the column will be lost.
  - The primary key for the `MST_Employee` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `code` on the `MST_Employee` table. All the data in the column will be lost.
  - You are about to drop the column `description` on the `MST_Employee` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_Employee` table. All the data in the column will be lost.
  - The primary key for the `MST_EmployeeDepartment` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `code` on the `MST_EmployeeDepartment` table. All the data in the column will be lost.
  - You are about to drop the column `description` on the `MST_EmployeeDepartment` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_EmployeeDepartment` table. All the data in the column will be lost.
  - The primary key for the `MST_EmployeeJobType` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `code` on the `MST_EmployeeJobType` table. All the data in the column will be lost.
  - You are about to drop the column `description` on the `MST_EmployeeJobType` table. All the data in the column will be lost.
  - You are about to drop the column `employee_job_type_id` on the `MST_EmployeeJobType` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_EmployeeJobType` table. All the data in the column will be lost.
  - The primary key for the `MST_EmployeePosition` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `code` on the `MST_EmployeePosition` table. All the data in the column will be lost.
  - You are about to drop the column `description` on the `MST_EmployeePosition` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_EmployeePosition` table. All the data in the column will be lost.
  - You are about to drop the column `code` on the `MST_JobType` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_JobType` table. All the data in the column will be lost.
  - The primary key for the `MST_JobTypeSkill` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `code` on the `MST_JobTypeSkill` table. All the data in the column will be lost.
  - You are about to drop the column `description` on the `MST_JobTypeSkill` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_JobTypeSkill` table. All the data in the column will be lost.
  - The primary key for the `MST_JobTypeSkillGrade` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `code` on the `MST_JobTypeSkillGrade` table. All the data in the column will be lost.
  - You are about to drop the column `description` on the `MST_JobTypeSkillGrade` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_JobTypeSkillGrade` table. All the data in the column will be lost.
  - The primary key for the `MST_NotificationSettings` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `code` on the `MST_NotificationSettings` table. All the data in the column will be lost.
  - You are about to drop the column `description` on the `MST_NotificationSettings` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_NotificationSettings` table. All the data in the column will be lost.
  - The primary key for the `MST_NotificationTemplate` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `code` on the `MST_NotificationTemplate` table. All the data in the column will be lost.
  - You are about to drop the column `description` on the `MST_NotificationTemplate` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_NotificationTemplate` table. All the data in the column will be lost.
  - You are about to drop the column `code` on the `MST_Permission` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_Permission` table. All the data in the column will be lost.
  - You are about to drop the column `code` on the `MST_Position` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_Position` table. All the data in the column will be lost.
  - The primary key for the `MST_ReportTemplate` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `code` on the `MST_ReportTemplate` table. All the data in the column will be lost.
  - You are about to drop the column `description` on the `MST_ReportTemplate` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_ReportTemplate` table. All the data in the column will be lost.
  - You are about to drop the column `code` on the `MST_Role` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_Role` table. All the data in the column will be lost.
  - You are about to drop the column `code` on the `MST_SkillCategory` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_SkillCategory` table. All the data in the column will be lost.
  - You are about to drop the column `code` on the `MST_SkillGrade` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_SkillGrade` table. All the data in the column will be lost.
  - The primary key for the `MST_SkillGradeRequirement` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `code` on the `MST_SkillGradeRequirement` table. All the data in the column will be lost.
  - You are about to drop the column `description` on the `MST_SkillGradeRequirement` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_SkillGradeRequirement` table. All the data in the column will be lost.
  - You are about to drop the column `code` on the `MST_SkillHierarchy` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_SkillHierarchy` table. All the data in the column will be lost.
  - You are about to drop the column `code` on the `MST_SkillItem` table. All the data in the column will be lost.
  - You are about to drop the column `description` on the `MST_SkillItem` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_SkillItem` table. All the data in the column will be lost.
  - You are about to drop the column `code` on the `MST_SystemConfig` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_SystemConfig` table. All the data in the column will be lost.
  - You are about to drop the column `activation_date` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `api_rate_limit` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `backup_enabled` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `backup_frequency` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `billing_cycle` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `code` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `created_by` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `current_users_count` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `custom_settings` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `data_retention_days` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `date_format` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `description` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `features_enabled` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `last_login_date` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `monthly_fee` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `notes` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `security_policy` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `setup_fee` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `sso_config` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `sso_enabled` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `sso_provider` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `storage_used_gb` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `suspension_date` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `suspension_reason` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `time_format` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `trial_end_date` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `webhook_secret` on the `MST_Tenant` table. All the data in the column will be lost.
  - You are about to drop the column `webhook_url` on the `MST_Tenant` table. All the data in the column will be lost.
  - The primary key for the `MST_TenantSettings` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `code` on the `MST_TenantSettings` table. All the data in the column will be lost.
  - You are about to drop the column `description` on the `MST_TenantSettings` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_TenantSettings` table. All the data in the column will be lost.
  - You are about to drop the column `code` on the `MST_TrainingProgram` table. All the data in the column will be lost.
  - You are about to drop the column `description` on the `MST_TrainingProgram` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_TrainingProgram` table. All the data in the column will be lost.
  - You are about to drop the column `code` on the `MST_UserAuth` table. All the data in the column will be lost.
  - You are about to drop the column `description` on the `MST_UserAuth` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_UserAuth` table. All the data in the column will be lost.
  - The primary key for the `MST_UserRole` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `code` on the `MST_UserRole` table. All the data in the column will be lost.
  - You are about to drop the column `description` on the `MST_UserRole` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `MST_UserRole` table. All the data in the column will be lost.
  - The primary key for the `SYS_IntegrationConfig` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `request_body` on the `SYS_SystemLog` table. All the data in the column will be lost.
  - You are about to drop the column `response_body` on the `SYS_SystemLog` table. All the data in the column will be lost.
  - The primary key for the `SYS_TokenStore` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - A unique constraint covering the columns `[employee_code]` on the table `MST_Employee` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[job_type_id,skill_item_id]` on the table `MST_JobTypeSkill` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[job_type_id,skill_grade_id]` on the table `MST_JobTypeSkillGrade` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[tenant_id,setting_key]` on the table `MST_NotificationSettings` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[tenant_id,template_key,notification_type,language_code]` on the table `MST_NotificationTemplate` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[tenant_id,template_key,language_code]` on the table `MST_ReportTemplate` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[tenant_id,setting_key]` on the table `MST_TenantSettings` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[user_id,role_id]` on the table `MST_UserRole` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[tenant_id,integration_key]` on the table `SYS_IntegrationConfig` will be added. If there are existing duplicate values, this will fail.
  - Added the required column `updated_at` to the `HIS_NotificationLog` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `HIS_TenantBilling` table without a default value. This is not possible if the table is not empty.
  - Made the column `id` on table `HIS_TenantBilling` required. This step will fail if there are existing NULL values in that column.
  - Added the required column `updated_at` to the `MST_CareerPlan` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `MST_Certification` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `MST_CertificationRequirement` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `MST_Department` table without a default value. This is not possible if the table is not empty.
  - Added the required column `id` to the `MST_Employee` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `MST_Employee` table without a default value. This is not possible if the table is not empty.
  - Added the required column `id` to the `MST_EmployeeDepartment` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `MST_EmployeeDepartment` table without a default value. This is not possible if the table is not empty.
  - Added the required column `id` to the `MST_EmployeeJobType` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `MST_EmployeeJobType` table without a default value. This is not possible if the table is not empty.
  - Added the required column `id` to the `MST_EmployeePosition` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `MST_EmployeePosition` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `MST_JobType` table without a default value. This is not possible if the table is not empty.
  - Added the required column `id` to the `MST_JobTypeSkill` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `MST_JobTypeSkill` table without a default value. This is not possible if the table is not empty.
  - Added the required column `id` to the `MST_JobTypeSkillGrade` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `MST_JobTypeSkillGrade` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `MST_NotificationSettings` table without a default value. This is not possible if the table is not empty.
  - Made the column `id` on table `MST_NotificationSettings` required. This step will fail if there are existing NULL values in that column.
  - Added the required column `updated_at` to the `MST_NotificationTemplate` table without a default value. This is not possible if the table is not empty.
  - Made the column `id` on table `MST_NotificationTemplate` required. This step will fail if there are existing NULL values in that column.
  - Added the required column `updated_at` to the `MST_Permission` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `MST_Position` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `MST_ReportTemplate` table without a default value. This is not possible if the table is not empty.
  - Made the column `id` on table `MST_ReportTemplate` required. This step will fail if there are existing NULL values in that column.
  - Added the required column `updated_at` to the `MST_Role` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `MST_SkillCategory` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `MST_SkillGrade` table without a default value. This is not possible if the table is not empty.
  - Added the required column `id` to the `MST_SkillGradeRequirement` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `MST_SkillGradeRequirement` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `MST_SkillHierarchy` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `MST_SkillItem` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `MST_SystemConfig` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `MST_Tenant` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `MST_TenantSettings` table without a default value. This is not possible if the table is not empty.
  - Made the column `id` on table `MST_TenantSettings` required. This step will fail if there are existing NULL values in that column.
  - Added the required column `updated_at` to the `MST_TrainingProgram` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `MST_UserAuth` table without a default value. This is not possible if the table is not empty.
  - Added the required column `id` to the `MST_UserRole` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `MST_UserRole` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `SYS_BackupHistory` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `SYS_IntegrationConfig` table without a default value. This is not possible if the table is not empty.
  - Made the column `id` on table `SYS_IntegrationConfig` required. This step will fail if there are existing NULL values in that column.
  - Added the required column `updated_at` to the `SYS_MasterData` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `SYS_SkillIndex` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `SYS_SkillMatrix` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `SYS_SystemLog` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `SYS_TenantUsage` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `SYS_TokenStore` table without a default value. This is not possible if the table is not empty.
  - Made the column `id` on table `SYS_TokenStore` required. This step will fail if there are existing NULL values in that column.
  - Added the required column `updated_at` to the `WRK_BatchJobLog` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "HIS_NotificationLog" ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL,
ALTER COLUMN "is_deleted" SET DEFAULT false;

-- AlterTable
ALTER TABLE "HIS_TenantBilling" DROP CONSTRAINT "HIS_TenantBilling_pkey",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL,
ALTER COLUMN "id" SET NOT NULL,
ALTER COLUMN "invoice_number" DROP NOT NULL,
ALTER COLUMN "is_deleted" SET DEFAULT false,
ADD CONSTRAINT "HIS_TenantBilling_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "MST_CareerPlan" DROP COLUMN "code",
DROP COLUMN "description",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL;

-- AlterTable
ALTER TABLE "MST_Certification" DROP COLUMN "code",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL;

-- AlterTable
ALTER TABLE "MST_CertificationRequirement" DROP COLUMN "code",
DROP COLUMN "description",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL;

-- AlterTable
ALTER TABLE "MST_Department" DROP COLUMN "code",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL;

-- AlterTable
ALTER TABLE "MST_Employee" DROP CONSTRAINT "MST_Employee_pkey",
DROP COLUMN "code",
DROP COLUMN "description",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "id" TEXT NOT NULL,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL,
ADD CONSTRAINT "MST_Employee_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "MST_EmployeeDepartment" DROP CONSTRAINT "MST_EmployeeDepartment_pkey",
DROP COLUMN "code",
DROP COLUMN "description",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "id" TEXT NOT NULL,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL,
ADD CONSTRAINT "MST_EmployeeDepartment_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "MST_EmployeeJobType" DROP CONSTRAINT "MST_EmployeeJobType_pkey",
DROP COLUMN "code",
DROP COLUMN "description",
DROP COLUMN "employee_job_type_id",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "id" TEXT NOT NULL,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL,
ADD CONSTRAINT "MST_EmployeeJobType_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "MST_EmployeePosition" DROP CONSTRAINT "MST_EmployeePosition_pkey",
DROP COLUMN "code",
DROP COLUMN "description",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "id" TEXT NOT NULL,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL,
ADD CONSTRAINT "MST_EmployeePosition_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "MST_JobType" DROP COLUMN "code",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL;

-- AlterTable
ALTER TABLE "MST_JobTypeSkill" DROP CONSTRAINT "MST_JobTypeSkill_pkey",
DROP COLUMN "code",
DROP COLUMN "description",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "id" TEXT NOT NULL,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL,
ADD CONSTRAINT "MST_JobTypeSkill_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "MST_JobTypeSkillGrade" DROP CONSTRAINT "MST_JobTypeSkillGrade_pkey",
DROP COLUMN "code",
DROP COLUMN "description",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "id" TEXT NOT NULL,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL,
ADD CONSTRAINT "MST_JobTypeSkillGrade_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "MST_NotificationSettings" DROP CONSTRAINT "MST_NotificationSettings_pkey",
DROP COLUMN "code",
DROP COLUMN "description",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL,
ALTER COLUMN "id" SET NOT NULL,
ADD CONSTRAINT "MST_NotificationSettings_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "MST_NotificationTemplate" DROP CONSTRAINT "MST_NotificationTemplate_pkey",
DROP COLUMN "code",
DROP COLUMN "description",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL,
ALTER COLUMN "id" SET NOT NULL,
ADD CONSTRAINT "MST_NotificationTemplate_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "MST_Permission" DROP COLUMN "code",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL;

-- AlterTable
ALTER TABLE "MST_Position" DROP COLUMN "code",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL;

-- AlterTable
ALTER TABLE "MST_ReportTemplate" DROP CONSTRAINT "MST_ReportTemplate_pkey",
DROP COLUMN "code",
DROP COLUMN "description",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL,
ALTER COLUMN "id" SET NOT NULL,
ADD CONSTRAINT "MST_ReportTemplate_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "MST_Role" DROP COLUMN "code",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL;

-- AlterTable
ALTER TABLE "MST_SkillCategory" DROP COLUMN "code",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL;

-- AlterTable
ALTER TABLE "MST_SkillGrade" DROP COLUMN "code",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL;

-- AlterTable
ALTER TABLE "MST_SkillGradeRequirement" DROP CONSTRAINT "MST_SkillGradeRequirement_pkey",
DROP COLUMN "code",
DROP COLUMN "description",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "id" TEXT NOT NULL,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL,
ADD CONSTRAINT "MST_SkillGradeRequirement_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "MST_SkillHierarchy" DROP COLUMN "code",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL;

-- AlterTable
ALTER TABLE "MST_SkillItem" DROP COLUMN "code",
DROP COLUMN "description",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL;

-- AlterTable
ALTER TABLE "MST_SystemConfig" DROP COLUMN "code",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL;

-- AlterTable
ALTER TABLE "MST_Tenant" DROP COLUMN "activation_date",
DROP COLUMN "api_rate_limit",
DROP COLUMN "backup_enabled",
DROP COLUMN "backup_frequency",
DROP COLUMN "billing_cycle",
DROP COLUMN "code",
DROP COLUMN "created_by",
DROP COLUMN "current_users_count",
DROP COLUMN "custom_settings",
DROP COLUMN "data_retention_days",
DROP COLUMN "date_format",
DROP COLUMN "description",
DROP COLUMN "features_enabled",
DROP COLUMN "last_login_date",
DROP COLUMN "monthly_fee",
DROP COLUMN "name",
DROP COLUMN "notes",
DROP COLUMN "security_policy",
DROP COLUMN "setup_fee",
DROP COLUMN "sso_config",
DROP COLUMN "sso_enabled",
DROP COLUMN "sso_provider",
DROP COLUMN "storage_used_gb",
DROP COLUMN "suspension_date",
DROP COLUMN "suspension_reason",
DROP COLUMN "time_format",
DROP COLUMN "trial_end_date",
DROP COLUMN "webhook_secret",
DROP COLUMN "webhook_url",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL;

-- AlterTable
ALTER TABLE "MST_TenantSettings" DROP CONSTRAINT "MST_TenantSettings_pkey",
DROP COLUMN "code",
DROP COLUMN "description",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL,
ALTER COLUMN "id" SET NOT NULL,
ADD CONSTRAINT "MST_TenantSettings_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "MST_TrainingProgram" DROP COLUMN "code",
DROP COLUMN "description",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL;

-- AlterTable
ALTER TABLE "MST_UserAuth" DROP COLUMN "code",
DROP COLUMN "description",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL;

-- AlterTable
ALTER TABLE "MST_UserRole" DROP CONSTRAINT "MST_UserRole_pkey",
DROP COLUMN "code",
DROP COLUMN "description",
DROP COLUMN "name",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "id" TEXT NOT NULL,
ADD COLUMN     "is_deleted" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL,
ADD CONSTRAINT "MST_UserRole_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "SYS_BackupHistory" ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL,
ALTER COLUMN "is_deleted" SET DEFAULT false;

-- AlterTable
ALTER TABLE "SYS_IntegrationConfig" DROP CONSTRAINT "SYS_IntegrationConfig_pkey",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL,
ALTER COLUMN "id" SET NOT NULL,
ALTER COLUMN "is_deleted" SET DEFAULT false,
ADD CONSTRAINT "SYS_IntegrationConfig_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "SYS_MasterData" ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL,
ALTER COLUMN "is_deleted" SET DEFAULT false;

-- AlterTable
ALTER TABLE "SYS_SkillIndex" ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL,
ALTER COLUMN "is_deleted" SET DEFAULT false;

-- AlterTable
ALTER TABLE "SYS_SkillMatrix" ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL,
ALTER COLUMN "is_deleted" SET DEFAULT false;

-- AlterTable
ALTER TABLE "SYS_SystemLog" DROP COLUMN "request_body",
DROP COLUMN "response_body",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL,
ALTER COLUMN "is_deleted" SET DEFAULT false;

-- AlterTable
ALTER TABLE "SYS_TenantUsage" ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL,
ALTER COLUMN "is_deleted" SET DEFAULT false;

-- AlterTable
ALTER TABLE "SYS_TokenStore" DROP CONSTRAINT "SYS_TokenStore_pkey",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL,
ALTER COLUMN "id" SET NOT NULL,
ALTER COLUMN "token_hash" DROP NOT NULL,
ALTER COLUMN "is_deleted" SET DEFAULT false,
ADD CONSTRAINT "SYS_TokenStore_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "TRN_EmployeeSkillGrade" ALTER COLUMN "is_deleted" SET DEFAULT false,
ALTER COLUMN "created_at" SET DEFAULT CURRENT_TIMESTAMP;

-- AlterTable
ALTER TABLE "TRN_GoalProgress" ALTER COLUMN "is_deleted" SET DEFAULT false,
ALTER COLUMN "created_at" SET DEFAULT CURRENT_TIMESTAMP;

-- AlterTable
ALTER TABLE "TRN_Notification" ALTER COLUMN "is_deleted" SET DEFAULT false,
ALTER COLUMN "created_at" SET DEFAULT CURRENT_TIMESTAMP;

-- AlterTable
ALTER TABLE "TRN_PDU" ALTER COLUMN "is_deleted" SET DEFAULT false,
ALTER COLUMN "created_at" SET DEFAULT CURRENT_TIMESTAMP;

-- AlterTable
ALTER TABLE "TRN_ProjectRecord" ALTER COLUMN "is_deleted" SET DEFAULT false,
ALTER COLUMN "created_at" SET DEFAULT CURRENT_TIMESTAMP;

-- AlterTable
ALTER TABLE "TRN_SkillEvidence" ALTER COLUMN "is_deleted" SET DEFAULT false,
ALTER COLUMN "created_at" SET DEFAULT CURRENT_TIMESTAMP;

-- AlterTable
ALTER TABLE "TRN_SkillRecord" ALTER COLUMN "is_deleted" SET DEFAULT false,
ALTER COLUMN "created_at" SET DEFAULT CURRENT_TIMESTAMP;

-- AlterTable
ALTER TABLE "TRN_TrainingHistory" ALTER COLUMN "is_deleted" SET DEFAULT false,
ALTER COLUMN "created_at" SET DEFAULT CURRENT_TIMESTAMP;

-- AlterTable
ALTER TABLE "WRK_BatchJobLog" ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL,
ALTER COLUMN "is_deleted" SET DEFAULT false;

-- CreateTable
CREATE TABLE "HIS_ReportGeneration" (
    "id" TEXT NOT NULL,
    "tenant_id" TEXT,
    "template_id" TEXT,
    "requested_by" TEXT,
    "report_title" TEXT,
    "report_category" TEXT,
    "output_format" TEXT,
    "generation_status" TEXT,
    "parameters" TEXT,
    "file_path" TEXT,
    "file_size" INTEGER,
    "download_count" INTEGER,
    "last_downloaded_at" TIMESTAMP(3),
    "requested_at" TIMESTAMP(3),
    "started_at" TIMESTAMP(3),
    "completed_at" TIMESTAMP(3),
    "processing_time_ms" INTEGER,
    "error_message" TEXT,
    "error_details" TEXT,
    "expires_at" TIMESTAMP(3),
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "is_deleted" BOOLEAN NOT NULL DEFAULT false,

    CONSTRAINT "HIS_ReportGeneration_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "MST_RolePermission" (
    "id" TEXT NOT NULL,
    "role_permission_id" TEXT,
    "role_id" TEXT,
    "permission_id" TEXT,
    "is_active" BOOLEAN,
    "granted_at" TIMESTAMP(3),
    "granted_by" TEXT,
    "revoked_at" TIMESTAMP(3),
    "revoked_by" TEXT,
    "notes" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "is_deleted" BOOLEAN NOT NULL DEFAULT false,

    CONSTRAINT "MST_RolePermission_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "MST_Skill" (
    "id" TEXT NOT NULL,
    "skill_name" TEXT,
    "skill_name_en" TEXT,
    "category_id" TEXT,
    "skill_type" TEXT,
    "difficulty_level" INTEGER,
    "description" TEXT,
    "evaluation_criteria" TEXT,
    "required_experience_months" INTEGER,
    "related_skills" TEXT,
    "prerequisite_skills" TEXT,
    "certification_info" TEXT,
    "learning_resources" TEXT,
    "market_demand" TEXT,
    "technology_trend" TEXT,
    "is_core_skill" BOOLEAN,
    "display_order" INTEGER,
    "is_active" BOOLEAN,
    "effective_from" TIMESTAMP(3),
    "effective_to" TIMESTAMP(3),
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "is_deleted" BOOLEAN NOT NULL DEFAULT false,

    CONSTRAINT "MST_Skill_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "MST_Employee_employee_code_key" ON "MST_Employee"("employee_code");

-- CreateIndex
CREATE UNIQUE INDEX "MST_JobTypeSkill_job_type_id_skill_item_id_key" ON "MST_JobTypeSkill"("job_type_id", "skill_item_id");

-- CreateIndex
CREATE UNIQUE INDEX "MST_JobTypeSkillGrade_job_type_id_skill_grade_id_key" ON "MST_JobTypeSkillGrade"("job_type_id", "skill_grade_id");

-- CreateIndex
CREATE UNIQUE INDEX "MST_NotificationSettings_tenant_id_setting_key_key" ON "MST_NotificationSettings"("tenant_id", "setting_key");

-- CreateIndex
CREATE UNIQUE INDEX "MST_NotificationTemplate_tenant_id_template_key_notificatio_key" ON "MST_NotificationTemplate"("tenant_id", "template_key", "notification_type", "language_code");

-- CreateIndex
CREATE UNIQUE INDEX "MST_ReportTemplate_tenant_id_template_key_language_code_key" ON "MST_ReportTemplate"("tenant_id", "template_key", "language_code");

-- CreateIndex
CREATE UNIQUE INDEX "MST_TenantSettings_tenant_id_setting_key_key" ON "MST_TenantSettings"("tenant_id", "setting_key");

-- CreateIndex
CREATE UNIQUE INDEX "MST_UserRole_user_id_role_id_key" ON "MST_UserRole"("user_id", "role_id");

-- CreateIndex
CREATE UNIQUE INDEX "SYS_IntegrationConfig_tenant_id_integration_key_key" ON "SYS_IntegrationConfig"("tenant_id", "integration_key");
