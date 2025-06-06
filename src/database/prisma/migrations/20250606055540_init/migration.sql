-- CreateTable
CREATE TABLE "HIS_AuditLog" (
    "id" TEXT NOT NULL,
    "user_id" TEXT,
    "session_id" TEXT,
    "action_type" TEXT,
    "target_table" TEXT,
    "target_id" TEXT,
    "old_values" TEXT,
    "new_values" TEXT,
    "ip_address" TEXT,
    "user_agent" TEXT,
    "result_status" TEXT,
    "error_message" TEXT,
    "execution_time_ms" INTEGER,
    "is_deleted" BOOLEAN,
    "tenant_id" TEXT,
    "created_at" TIMESTAMP(3),
    "updated_at" TIMESTAMP(3),
    "created_by" TEXT,
    "updated_by" TEXT,

    CONSTRAINT "HIS_AuditLog_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "HIS_NotificationLog" (
    "id" TEXT NOT NULL,
    "tenant_id" TEXT,
    "notification_id" TEXT,
    "setting_id" TEXT,
    "template_id" TEXT,
    "notification_type" TEXT,
    "recipient_type" TEXT,
    "recipient_address" TEXT,
    "subject" TEXT,
    "message_body" TEXT,
    "message_format" TEXT,
    "send_status" TEXT,
    "send_attempts" INTEGER,
    "max_retry_count" INTEGER,
    "scheduled_at" TIMESTAMP(3),
    "sent_at" TIMESTAMP(3),
    "delivered_at" TIMESTAMP(3),
    "opened_at" TIMESTAMP(3),
    "response_code" TEXT,
    "response_message" TEXT,
    "error_details" TEXT,
    "integration_config_id" TEXT,
    "priority_level" TEXT,
    "is_deleted" BOOLEAN NOT NULL,

    CONSTRAINT "HIS_NotificationLog_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "HIS_TenantBilling" (
    "id" TEXT,
    "tenant_id" TEXT,
    "billing_period_start" TIMESTAMP(3),
    "billing_period_end" TIMESTAMP(3),
    "billing_type" TEXT,
    "plan_id" TEXT,
    "plan_name" TEXT,
    "base_amount" DECIMAL(65,30),
    "usage_amount" DECIMAL(65,30),
    "additional_amount" DECIMAL(65,30),
    "discount_amount" DECIMAL(65,30),
    "subtotal_amount" DECIMAL(65,30),
    "tax_rate" DECIMAL(65,30),
    "tax_amount" DECIMAL(65,30),
    "total_amount" DECIMAL(65,30),
    "currency_code" TEXT,
    "usage_details" TEXT,
    "billing_status" TEXT,
    "invoice_number" TEXT NOT NULL,
    "invoice_date" TIMESTAMP(3),
    "due_date" TIMESTAMP(3),
    "paid_date" TIMESTAMP(3),
    "payment_method" TEXT,
    "notes" TEXT,
    "is_deleted" BOOLEAN NOT NULL,

    CONSTRAINT "HIS_TenantBilling_pkey" PRIMARY KEY ("invoice_number")
);

-- CreateTable
CREATE TABLE "MST_CareerPlan" (
    "career_plan_id" TEXT NOT NULL,
    "employee_id" TEXT,
    "plan_name" TEXT,
    "plan_description" TEXT,
    "plan_type" TEXT,
    "target_position_id" TEXT,
    "target_job_type_id" TEXT,
    "target_department_id" TEXT,
    "current_level" TEXT,
    "target_level" TEXT,
    "plan_start_date" TIMESTAMP(3),
    "plan_end_date" TIMESTAMP(3),
    "milestone_1_date" TIMESTAMP(3),
    "milestone_1_description" TEXT,
    "milestone_2_date" TIMESTAMP(3),
    "milestone_2_description" TEXT,
    "milestone_3_date" TIMESTAMP(3),
    "milestone_3_description" TEXT,
    "required_skills" TEXT,
    "required_certifications" TEXT,
    "required_experiences" TEXT,
    "development_actions" TEXT,
    "training_plan" TEXT,
    "mentor_id" TEXT,
    "supervisor_id" TEXT,
    "plan_status" TEXT,
    "progress_percentage" DECIMAL(65,30),
    "last_review_date" TIMESTAMP(3),
    "next_review_date" TIMESTAMP(3),
    "review_frequency" TEXT,
    "success_criteria" TEXT,
    "risk_factors" TEXT,
    "support_resources" TEXT,
    "budget_allocated" DECIMAL(65,30),
    "budget_used" DECIMAL(65,30),
    "priority_level" TEXT,
    "visibility_level" TEXT,
    "template_id" TEXT,
    "custom_fields" TEXT,
    "notes" TEXT,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,

    CONSTRAINT "MST_CareerPlan_pkey" PRIMARY KEY ("career_plan_id")
);

-- CreateTable
CREATE TABLE "MST_Certification" (
    "certification_code" TEXT NOT NULL,
    "certification_name" TEXT,
    "certification_name_en" TEXT,
    "issuer" TEXT,
    "issuer_country" TEXT,
    "certification_category" TEXT,
    "certification_level" TEXT,
    "validity_period_months" INTEGER,
    "renewal_required" BOOLEAN,
    "renewal_requirements" TEXT,
    "exam_fee" DECIMAL(65,30),
    "exam_language" TEXT,
    "exam_format" TEXT,
    "official_url" TEXT,
    "description" TEXT,
    "skill_category_id" TEXT,
    "is_recommended" BOOLEAN,
    "is_active" BOOLEAN,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,

    CONSTRAINT "MST_Certification_pkey" PRIMARY KEY ("certification_code")
);

-- CreateTable
CREATE TABLE "MST_CertificationRequirement" (
    "requirement_id" TEXT NOT NULL,
    "requirement_name" TEXT,
    "requirement_description" TEXT,
    "requirement_type" TEXT,
    "target_job_type_id" TEXT,
    "target_position_id" TEXT,
    "target_skill_grade_id" TEXT,
    "target_department_id" TEXT,
    "certification_id" TEXT,
    "requirement_level" TEXT,
    "priority_order" INTEGER,
    "alternative_certifications" TEXT,
    "minimum_experience_years" INTEGER,
    "minimum_skill_level" TEXT,
    "grace_period_months" INTEGER,
    "renewal_required" BOOLEAN,
    "renewal_interval_months" INTEGER,
    "exemption_conditions" TEXT,
    "assessment_criteria" TEXT,
    "business_justification" TEXT,
    "compliance_requirement" BOOLEAN,
    "client_requirement" BOOLEAN,
    "internal_policy" BOOLEAN,
    "effective_start_date" TIMESTAMP(3),
    "effective_end_date" TIMESTAMP(3),
    "notification_timing" INTEGER,
    "escalation_timing" INTEGER,
    "cost_support_available" BOOLEAN,
    "cost_support_amount" DECIMAL(65,30),
    "cost_support_conditions" TEXT,
    "training_support_available" BOOLEAN,
    "recommended_training_programs" TEXT,
    "study_time_allocation" DECIMAL(65,30),
    "success_rate" DECIMAL(65,30),
    "average_study_hours" DECIMAL(65,30),
    "difficulty_rating" TEXT,
    "active_flag" BOOLEAN,
    "created_by" TEXT,
    "approved_by" TEXT,
    "approval_date" TIMESTAMP(3),
    "review_date" TIMESTAMP(3),
    "notes" TEXT,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,

    CONSTRAINT "MST_CertificationRequirement_pkey" PRIMARY KEY ("requirement_id")
);

-- CreateTable
CREATE TABLE "MST_Department" (
    "department_code" TEXT NOT NULL,
    "department_name" TEXT,
    "department_name_short" TEXT,
    "parent_department_id" TEXT,
    "department_level" INTEGER,
    "department_type" TEXT,
    "manager_id" TEXT,
    "deputy_manager_id" TEXT,
    "cost_center_code" TEXT,
    "budget_amount" DECIMAL(65,30),
    "location" TEXT,
    "phone_number" TEXT,
    "email_address" TEXT,
    "establishment_date" TIMESTAMP(3),
    "abolition_date" TIMESTAMP(3),
    "department_status" TEXT,
    "sort_order" INTEGER,
    "description" TEXT,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,

    CONSTRAINT "MST_Department_pkey" PRIMARY KEY ("department_code")
);

-- CreateTable
CREATE TABLE "MST_Employee" (
    "employee_code" TEXT NOT NULL,
    "full_name" TEXT,
    "full_name_kana" TEXT,
    "email" TEXT,
    "phone" TEXT,
    "hire_date" TIMESTAMP(3),
    "birth_date" TIMESTAMP(3),
    "gender" TEXT,
    "department_id" TEXT,
    "position_id" TEXT,
    "job_type_id" TEXT,
    "employment_status" TEXT,
    "manager_id" TEXT,
    "employee_status" TEXT,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,

    CONSTRAINT "MST_Employee_pkey" PRIMARY KEY ("employee_code")
);

-- CreateTable
CREATE TABLE "MST_EmployeeDepartment" (
    "employee_id" TEXT NOT NULL,
    "department_id" TEXT,
    "assignment_type" TEXT,
    "start_date" TIMESTAMP(3),
    "end_date" TIMESTAMP(3),
    "assignment_ratio" DECIMAL(65,30),
    "role_in_department" TEXT,
    "reporting_manager_id" TEXT,
    "assignment_reason" TEXT,
    "assignment_status" TEXT,
    "approval_status" TEXT,
    "approved_by" TEXT,
    "approved_at" TIMESTAMP(3),
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,

    CONSTRAINT "MST_EmployeeDepartment_pkey" PRIMARY KEY ("employee_id")
);

-- CreateTable
CREATE TABLE "MST_EmployeeJobType" (
    "employee_job_type_id" TEXT NOT NULL,
    "employee_id" TEXT,
    "job_type_id" TEXT,
    "assignment_type" TEXT,
    "assignment_ratio" DECIMAL(65,30),
    "effective_start_date" TIMESTAMP(3),
    "effective_end_date" TIMESTAMP(3),
    "assignment_reason" TEXT,
    "assignment_status" TEXT,
    "proficiency_level" TEXT,
    "target_proficiency_level" TEXT,
    "target_achievement_date" TIMESTAMP(3),
    "certification_requirements" TEXT,
    "skill_requirements" TEXT,
    "experience_requirements" TEXT,
    "development_plan" TEXT,
    "training_plan" TEXT,
    "mentor_id" TEXT,
    "supervisor_id" TEXT,
    "performance_rating" TEXT,
    "last_evaluation_date" TIMESTAMP(3),
    "next_evaluation_date" TIMESTAMP(3),
    "evaluation_frequency" TEXT,
    "career_path" TEXT,
    "strengths" TEXT,
    "improvement_areas" TEXT,
    "achievements" TEXT,
    "goals" TEXT,
    "workload_percentage" DECIMAL(65,30),
    "billable_flag" BOOLEAN,
    "cost_center" TEXT,
    "budget_allocation" DECIMAL(65,30),
    "hourly_rate" DECIMAL(65,30),
    "overtime_eligible" BOOLEAN,
    "remote_work_eligible" BOOLEAN,
    "travel_required" BOOLEAN,
    "security_clearance_required" BOOLEAN,
    "created_by" TEXT,
    "approved_by" TEXT,
    "approval_date" TIMESTAMP(3),
    "notes" TEXT,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,

    CONSTRAINT "MST_EmployeeJobType_pkey" PRIMARY KEY ("employee_job_type_id")
);

-- CreateTable
CREATE TABLE "MST_EmployeePosition" (
    "employee_id" TEXT NOT NULL,
    "position_id" TEXT,
    "appointment_type" TEXT,
    "start_date" TIMESTAMP(3),
    "end_date" TIMESTAMP(3),
    "appointment_reason" TEXT,
    "responsibility_scope" TEXT,
    "authority_level" INTEGER,
    "salary_grade" TEXT,
    "appointment_status" TEXT,
    "approval_status" TEXT,
    "approved_by" TEXT,
    "approved_at" TIMESTAMP(3),
    "performance_target" TEXT,
    "delegation_authority" TEXT,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,

    CONSTRAINT "MST_EmployeePosition_pkey" PRIMARY KEY ("employee_id")
);

-- CreateTable
CREATE TABLE "MST_JobType" (
    "job_type_code" TEXT NOT NULL,
    "job_type_name" TEXT,
    "job_type_name_en" TEXT,
    "job_category" TEXT,
    "job_level" TEXT,
    "description" TEXT,
    "required_experience_years" INTEGER,
    "salary_grade_min" INTEGER,
    "salary_grade_max" INTEGER,
    "career_path" TEXT,
    "required_certifications" TEXT,
    "required_skills" TEXT,
    "department_affinity" TEXT,
    "remote_work_eligible" BOOLEAN,
    "travel_frequency" TEXT,
    "sort_order" INTEGER,
    "is_active" BOOLEAN,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,

    CONSTRAINT "MST_JobType_pkey" PRIMARY KEY ("job_type_code")
);

-- CreateTable
CREATE TABLE "MST_JobTypeSkill" (
    "job_type_id" TEXT NOT NULL,
    "skill_item_id" TEXT NOT NULL,
    "required_level" INTEGER,
    "skill_priority" TEXT,
    "skill_category" TEXT,
    "experience_years" DECIMAL(65,30),
    "certification_required" BOOLEAN,
    "skill_weight" DECIMAL(65,30),
    "evaluation_criteria" TEXT,
    "learning_path" TEXT,
    "skill_status" TEXT,
    "effective_date" TIMESTAMP(3),
    "expiry_date" TIMESTAMP(3),
    "alternative_skills" TEXT,
    "prerequisite_skills" TEXT,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,

    CONSTRAINT "MST_JobTypeSkill_pkey" PRIMARY KEY ("job_type_id","skill_item_id")
);

-- CreateTable
CREATE TABLE "MST_JobTypeSkillGrade" (
    "job_type_id" TEXT NOT NULL,
    "skill_grade_id" TEXT NOT NULL,
    "grade_requirement_type" TEXT,
    "required_experience_years" DECIMAL(65,30),
    "promotion_criteria" TEXT,
    "salary_range_min" DECIMAL(65,30),
    "salary_range_max" DECIMAL(65,30),
    "performance_expectations" TEXT,
    "leadership_requirements" TEXT,
    "technical_depth" INTEGER,
    "business_impact" INTEGER,
    "team_size_expectation" INTEGER,
    "certification_requirements" TEXT,
    "grade_status" TEXT,
    "effective_date" TIMESTAMP(3),
    "expiry_date" TIMESTAMP(3),
    "next_grade_path" TEXT,
    "evaluation_frequency" TEXT,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,

    CONSTRAINT "MST_JobTypeSkillGrade_pkey" PRIMARY KEY ("job_type_id","skill_grade_id")
);

-- CreateTable
CREATE TABLE "MST_NotificationSettings" (
    "id" TEXT,
    "tenant_id" TEXT NOT NULL,
    "setting_key" TEXT NOT NULL,
    "setting_name" TEXT,
    "notification_type" TEXT,
    "target_audience" TEXT,
    "trigger_event" TEXT,
    "frequency_type" TEXT,
    "frequency_value" INTEGER,
    "template_id" TEXT,
    "channel_config" TEXT,
    "is_enabled" BOOLEAN,
    "priority_level" TEXT,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,

    CONSTRAINT "MST_NotificationSettings_pkey" PRIMARY KEY ("tenant_id","setting_key")
);

-- CreateTable
CREATE TABLE "MST_NotificationTemplate" (
    "id" TEXT,
    "tenant_id" TEXT NOT NULL,
    "template_key" TEXT NOT NULL,
    "template_name" TEXT,
    "notification_type" TEXT NOT NULL,
    "language_code" TEXT NOT NULL,
    "subject_template" TEXT,
    "body_template" TEXT,
    "format_type" TEXT,
    "parameters" TEXT,
    "sample_data" TEXT,
    "is_default" BOOLEAN,
    "is_active" BOOLEAN,
    "version" TEXT,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,

    CONSTRAINT "MST_NotificationTemplate_pkey" PRIMARY KEY ("tenant_id","template_key","notification_type","language_code")
);

-- CreateTable
CREATE TABLE "MST_Permission" (
    "permission_code" TEXT NOT NULL,
    "permission_name" TEXT,
    "permission_name_short" TEXT,
    "permission_category" TEXT,
    "resource_type" TEXT,
    "action_type" TEXT,
    "scope_level" TEXT,
    "parent_permission_id" TEXT,
    "is_system_permission" BOOLEAN,
    "requires_conditions" BOOLEAN,
    "condition_expression" TEXT,
    "risk_level" INTEGER,
    "requires_approval" BOOLEAN,
    "audit_required" BOOLEAN,
    "permission_status" TEXT,
    "effective_from" TIMESTAMP(3),
    "effective_to" TIMESTAMP(3),
    "sort_order" INTEGER,
    "description" TEXT,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,

    CONSTRAINT "MST_Permission_pkey" PRIMARY KEY ("permission_code")
);

-- CreateTable
CREATE TABLE "MST_Position" (
    "position_code" TEXT NOT NULL,
    "position_name" TEXT,
    "position_name_short" TEXT,
    "position_level" INTEGER,
    "position_rank" INTEGER,
    "position_category" TEXT,
    "authority_level" INTEGER,
    "approval_limit" DECIMAL(65,30),
    "salary_grade" TEXT,
    "allowance_amount" DECIMAL(65,30),
    "is_management" BOOLEAN,
    "is_executive" BOOLEAN,
    "requires_approval" BOOLEAN,
    "can_hire" BOOLEAN,
    "can_evaluate" BOOLEAN,
    "position_status" TEXT,
    "sort_order" INTEGER,
    "description" TEXT,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,

    CONSTRAINT "MST_Position_pkey" PRIMARY KEY ("position_code")
);

-- CreateTable
CREATE TABLE "MST_ReportTemplate" (
    "id" TEXT,
    "tenant_id" TEXT NOT NULL,
    "template_key" TEXT NOT NULL,
    "template_name" TEXT,
    "report_category" TEXT,
    "output_format" TEXT,
    "language_code" TEXT NOT NULL,
    "template_content" TEXT,
    "style_sheet" TEXT,
    "parameters_schema" TEXT,
    "data_source_config" TEXT,
    "page_settings" TEXT,
    "header_template" TEXT,
    "footer_template" TEXT,
    "is_default" BOOLEAN,
    "is_active" BOOLEAN,
    "version" TEXT,
    "preview_image_url" TEXT,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,

    CONSTRAINT "MST_ReportTemplate_pkey" PRIMARY KEY ("tenant_id","template_key","language_code")
);

-- CreateTable
CREATE TABLE "MST_Role" (
    "role_code" TEXT NOT NULL,
    "role_name" TEXT,
    "role_name_short" TEXT,
    "role_category" TEXT,
    "role_level" INTEGER,
    "parent_role_id" TEXT,
    "is_system_role" BOOLEAN,
    "is_tenant_specific" BOOLEAN,
    "max_users" INTEGER,
    "role_priority" INTEGER,
    "auto_assign_conditions" TEXT,
    "role_status" TEXT,
    "effective_from" TIMESTAMP(3),
    "effective_to" TIMESTAMP(3),
    "sort_order" INTEGER,
    "description" TEXT,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,

    CONSTRAINT "MST_Role_pkey" PRIMARY KEY ("role_code")
);

-- CreateTable
CREATE TABLE "MST_SkillCategory" (
    "category_code" TEXT NOT NULL,
    "category_name" TEXT,
    "category_name_short" TEXT,
    "category_name_en" TEXT,
    "category_type" TEXT,
    "parent_category_id" TEXT,
    "category_level" INTEGER,
    "category_path" TEXT,
    "is_system_category" BOOLEAN,
    "is_leaf_category" BOOLEAN,
    "skill_count" INTEGER,
    "evaluation_method" TEXT,
    "max_level" INTEGER,
    "icon_url" TEXT,
    "color_code" TEXT,
    "display_order" INTEGER,
    "is_popular" BOOLEAN,
    "category_status" TEXT,
    "effective_from" TIMESTAMP(3),
    "effective_to" TIMESTAMP(3),
    "description" TEXT,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,

    CONSTRAINT "MST_SkillCategory_pkey" PRIMARY KEY ("category_code")
);

-- CreateTable
CREATE TABLE "MST_SkillGrade" (
    "grade_code" TEXT NOT NULL,
    "grade_name" TEXT,
    "grade_name_short" TEXT,
    "grade_level" INTEGER,
    "description" TEXT,
    "evaluation_criteria" TEXT,
    "required_experience_months" INTEGER,
    "skill_indicators" TEXT,
    "competency_requirements" TEXT,
    "certification_requirements" TEXT,
    "project_complexity" TEXT,
    "mentoring_capability" BOOLEAN,
    "leadership_level" TEXT,
    "salary_impact_factor" DECIMAL(65,30),
    "promotion_eligibility" BOOLEAN,
    "color_code" TEXT,
    "sort_order" INTEGER,
    "is_active" BOOLEAN,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,

    CONSTRAINT "MST_SkillGrade_pkey" PRIMARY KEY ("grade_code")
);

-- CreateTable
CREATE TABLE "MST_SkillGradeRequirement" (
    "skill_grade_id" TEXT NOT NULL,
    "requirement_category" TEXT,
    "requirement_name" TEXT,
    "requirement_description" TEXT,
    "evaluation_criteria" TEXT,
    "proficiency_level" INTEGER,
    "weight_percentage" DECIMAL(65,30),
    "minimum_score" DECIMAL(65,30),
    "evidence_requirements" TEXT,
    "learning_resources" TEXT,
    "prerequisite_requirements" TEXT,
    "assessment_method" TEXT,
    "assessment_frequency" TEXT,
    "validity_period" INTEGER,
    "certification_mapping" TEXT,
    "requirement_status" TEXT,
    "effective_date" TIMESTAMP(3),
    "expiry_date" TIMESTAMP(3),
    "revision_notes" TEXT,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,

    CONSTRAINT "MST_SkillGradeRequirement_pkey" PRIMARY KEY ("skill_grade_id")
);

-- CreateTable
CREATE TABLE "MST_SkillHierarchy" (
    "skill_id" TEXT NOT NULL,
    "parent_skill_id" TEXT,
    "hierarchy_level" INTEGER,
    "skill_path" TEXT,
    "sort_order" INTEGER,
    "is_leaf" BOOLEAN,
    "skill_category" TEXT,
    "description" TEXT,
    "is_active" BOOLEAN,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,

    CONSTRAINT "MST_SkillHierarchy_pkey" PRIMARY KEY ("skill_id")
);

-- CreateTable
CREATE TABLE "MST_SkillItem" (
    "skill_code" TEXT NOT NULL,
    "skill_name" TEXT,
    "skill_category_id" TEXT,
    "skill_type" TEXT,
    "difficulty_level" INTEGER,
    "importance_level" INTEGER,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,

    CONSTRAINT "MST_SkillItem_pkey" PRIMARY KEY ("skill_code")
);

-- CreateTable
CREATE TABLE "MST_SystemConfig" (
    "config_key" TEXT NOT NULL,
    "config_name" TEXT,
    "config_value" TEXT,
    "config_type" TEXT,
    "config_category" TEXT,
    "default_value" TEXT,
    "validation_rule" TEXT,
    "description" TEXT,
    "is_encrypted" BOOLEAN,
    "is_system_only" BOOLEAN,
    "is_user_configurable" BOOLEAN,
    "requires_restart" BOOLEAN,
    "environment" TEXT,
    "tenant_specific" BOOLEAN,
    "last_modified_by" TEXT,
    "last_modified_reason" TEXT,
    "sort_order" INTEGER,
    "is_active" BOOLEAN,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,

    CONSTRAINT "MST_SystemConfig_pkey" PRIMARY KEY ("config_key")
);

-- CreateTable
CREATE TABLE "MST_Tenant" (
    "tenant_id" TEXT NOT NULL,
    "tenant_code" TEXT,
    "tenant_name" TEXT,
    "tenant_name_en" TEXT,
    "tenant_short_name" TEXT,
    "tenant_type" TEXT,
    "parent_tenant_id" TEXT,
    "tenant_level" INTEGER,
    "domain_name" TEXT,
    "subdomain" TEXT,
    "logo_url" TEXT,
    "primary_color" TEXT,
    "secondary_color" TEXT,
    "timezone" TEXT,
    "locale" TEXT,
    "currency_code" TEXT,
    "date_format" TEXT,
    "time_format" TEXT,
    "admin_email" TEXT,
    "contact_email" TEXT,
    "phone_number" TEXT,
    "address" TEXT,
    "postal_code" TEXT,
    "country_code" TEXT,
    "subscription_plan" TEXT,
    "max_users" INTEGER,
    "max_storage_gb" INTEGER,
    "features_enabled" TEXT,
    "custom_settings" TEXT,
    "security_policy" TEXT,
    "data_retention_days" INTEGER,
    "backup_enabled" BOOLEAN,
    "backup_frequency" TEXT,
    "contract_start_date" TIMESTAMP(3),
    "contract_end_date" TIMESTAMP(3),
    "trial_end_date" TIMESTAMP(3),
    "billing_cycle" TEXT,
    "monthly_fee" DECIMAL(65,30),
    "setup_fee" DECIMAL(65,30),
    "status" TEXT,
    "activation_date" TIMESTAMP(3),
    "suspension_date" TIMESTAMP(3),
    "suspension_reason" TEXT,
    "last_login_date" TIMESTAMP(3),
    "current_users_count" INTEGER,
    "storage_used_gb" DECIMAL(65,30),
    "api_rate_limit" INTEGER,
    "sso_enabled" BOOLEAN,
    "sso_provider" TEXT,
    "sso_config" TEXT,
    "webhook_url" TEXT,
    "webhook_secret" TEXT,
    "created_by" TEXT,
    "notes" TEXT,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,

    CONSTRAINT "MST_Tenant_pkey" PRIMARY KEY ("tenant_id")
);

-- CreateTable
CREATE TABLE "MST_TenantSettings" (
    "id" TEXT,
    "tenant_id" TEXT NOT NULL,
    "setting_category" TEXT,
    "setting_key" TEXT NOT NULL,
    "setting_name" TEXT,
    "setting_description" TEXT,
    "data_type" TEXT,
    "setting_value" TEXT,
    "default_value" TEXT,
    "validation_rules" TEXT,
    "is_required" BOOLEAN,
    "is_encrypted" BOOLEAN,
    "is_system_managed" BOOLEAN,
    "is_user_configurable" BOOLEAN,
    "display_order" INTEGER,
    "effective_from" TIMESTAMP(3),
    "effective_until" TIMESTAMP(3),
    "last_modified_by" TEXT,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,

    CONSTRAINT "MST_TenantSettings_pkey" PRIMARY KEY ("tenant_id","setting_key")
);

-- CreateTable
CREATE TABLE "MST_TrainingProgram" (
    "training_program_id" TEXT NOT NULL,
    "program_code" TEXT,
    "program_name" TEXT,
    "program_name_en" TEXT,
    "program_description" TEXT,
    "program_category" TEXT,
    "program_type" TEXT,
    "target_audience" TEXT,
    "difficulty_level" TEXT,
    "duration_hours" DECIMAL(65,30),
    "duration_days" INTEGER,
    "max_participants" INTEGER,
    "min_participants" INTEGER,
    "prerequisites" TEXT,
    "learning_objectives" TEXT,
    "curriculum_outline" TEXT,
    "curriculum_details" TEXT,
    "materials_required" TEXT,
    "equipment_required" TEXT,
    "instructor_requirements" TEXT,
    "assessment_method" TEXT,
    "passing_score" DECIMAL(65,30),
    "certification_provided" BOOLEAN,
    "pdu_credits" DECIMAL(65,30),
    "related_skills" TEXT,
    "related_certifications" TEXT,
    "cost_per_participant" DECIMAL(65,30),
    "external_provider" TEXT,
    "external_url" TEXT,
    "venue_type" TEXT,
    "venue_requirements" TEXT,
    "language" TEXT,
    "repeat_interval" INTEGER,
    "mandatory_flag" BOOLEAN,
    "active_flag" BOOLEAN,
    "effective_start_date" TIMESTAMP(3),
    "effective_end_date" TIMESTAMP(3),
    "created_by" TEXT,
    "approved_by" TEXT,
    "approval_date" TIMESTAMP(3),
    "version_number" TEXT,
    "revision_notes" TEXT,
    "tags" TEXT,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,

    CONSTRAINT "MST_TrainingProgram_pkey" PRIMARY KEY ("training_program_id")
);

-- CreateTable
CREATE TABLE "MST_UserAuth" (
    "user_id" TEXT NOT NULL,
    "login_id" TEXT,
    "password_hash" TEXT,
    "password_salt" TEXT,
    "employee_id" TEXT,
    "account_status" TEXT,
    "last_login_at" TIMESTAMP(3),
    "last_login_ip" TEXT,
    "failed_login_count" INTEGER,
    "last_failed_login_at" TIMESTAMP(3),
    "password_changed_at" TIMESTAMP(3),
    "password_expires_at" TIMESTAMP(3),
    "mfa_enabled" BOOLEAN,
    "mfa_secret" TEXT,
    "recovery_token" TEXT,
    "recovery_token_expires_at" TIMESTAMP(3),
    "session_timeout" INTEGER,
    "external_auth_provider" TEXT,
    "external_auth_id" TEXT,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,

    CONSTRAINT "MST_UserAuth_pkey" PRIMARY KEY ("user_id")
);

-- CreateTable
CREATE TABLE "MST_UserRole" (
    "user_id" TEXT NOT NULL,
    "role_id" TEXT NOT NULL,
    "assignment_type" TEXT,
    "assigned_by" TEXT,
    "assignment_reason" TEXT,
    "effective_from" TIMESTAMP(3),
    "effective_to" TIMESTAMP(3),
    "is_primary_role" BOOLEAN,
    "priority_order" INTEGER,
    "conditions" TEXT,
    "delegation_source_user_id" TEXT,
    "delegation_expires_at" TIMESTAMP(3),
    "auto_assigned" BOOLEAN,
    "requires_approval" BOOLEAN,
    "approval_status" TEXT,
    "approved_by" TEXT,
    "approved_at" TIMESTAMP(3),
    "assignment_status" TEXT,
    "last_used_at" TIMESTAMP(3),
    "usage_count" INTEGER,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,

    CONSTRAINT "MST_UserRole_pkey" PRIMARY KEY ("user_id","role_id")
);

-- CreateTable
CREATE TABLE "SYS_BackupHistory" (
    "backup_id" TEXT,
    "backup_type" TEXT,
    "backup_scope" TEXT,
    "target_objects" TEXT,
    "backup_start_time" TIMESTAMP(3),
    "backup_end_time" TIMESTAMP(3),
    "backup_status" TEXT,
    "backup_file_path" TEXT,
    "backup_file_size" BIGINT,
    "compression_type" TEXT,
    "encryption_enabled" BOOLEAN,
    "checksum" TEXT,
    "retention_period_days" INTEGER,
    "expiry_date" TIMESTAMP(3),
    "backup_trigger" TEXT,
    "executed_by" TEXT,
    "error_message" TEXT,
    "recovery_tested" BOOLEAN,
    "recovery_test_date" TIMESTAMP(3),
    "id" TEXT NOT NULL,
    "is_deleted" BOOLEAN NOT NULL,

    CONSTRAINT "SYS_BackupHistory_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "SYS_IntegrationConfig" (
    "id" TEXT,
    "tenant_id" TEXT NOT NULL,
    "integration_key" TEXT NOT NULL,
    "integration_name" TEXT,
    "integration_type" TEXT,
    "endpoint_url" TEXT,
    "auth_type" TEXT,
    "auth_config" TEXT,
    "connection_config" TEXT,
    "request_headers" TEXT,
    "timeout_seconds" INTEGER,
    "retry_count" INTEGER,
    "retry_interval" INTEGER,
    "rate_limit_per_minute" INTEGER,
    "is_enabled" BOOLEAN,
    "health_check_url" TEXT,
    "last_health_check" TIMESTAMP(3),
    "health_status" TEXT,
    "is_deleted" BOOLEAN NOT NULL,

    CONSTRAINT "SYS_IntegrationConfig_pkey" PRIMARY KEY ("tenant_id","integration_key")
);

-- CreateTable
CREATE TABLE "SYS_MasterData" (
    "master_key" TEXT,
    "master_category" TEXT,
    "master_name" TEXT,
    "master_value" TEXT,
    "data_type" TEXT,
    "default_value" TEXT,
    "validation_rule" TEXT,
    "is_system_managed" BOOLEAN,
    "is_editable" BOOLEAN,
    "display_order" INTEGER,
    "description" TEXT,
    "effective_from" TIMESTAMP(3),
    "effective_to" TIMESTAMP(3),
    "last_modified_by" TEXT,
    "last_modified_at" TIMESTAMP(3),
    "version" INTEGER,
    "id" TEXT NOT NULL,
    "is_deleted" BOOLEAN NOT NULL,

    CONSTRAINT "SYS_MasterData_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "SYS_SkillIndex" (
    "id" TEXT NOT NULL,
    "tenant_id" TEXT,
    "skill_id" TEXT,
    "index_type" TEXT,
    "search_term" TEXT,
    "normalized_term" TEXT,
    "relevance_score" DECIMAL(65,30),
    "frequency_weight" DECIMAL(65,30),
    "position_weight" DECIMAL(65,30),
    "language_code" TEXT,
    "source_field" TEXT,
    "is_active" BOOLEAN,
    "search_count" INTEGER,
    "last_searched_at" TIMESTAMP(3),
    "index_updated_at" TIMESTAMP(3),
    "is_deleted" BOOLEAN NOT NULL,

    CONSTRAINT "SYS_SkillIndex_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "SYS_SkillMatrix" (
    "employee_id" TEXT,
    "skill_id" TEXT,
    "skill_level" INTEGER,
    "self_assessment" INTEGER,
    "manager_assessment" INTEGER,
    "peer_assessment" INTEGER,
    "assessment_date" TIMESTAMP(3),
    "evidence_url" TEXT,
    "notes" TEXT,
    "next_target_level" INTEGER,
    "target_date" TIMESTAMP(3),
    "id" TEXT NOT NULL,
    "is_deleted" BOOLEAN NOT NULL,

    CONSTRAINT "SYS_SkillMatrix_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "SYS_SystemLog" (
    "log_level" TEXT,
    "log_category" TEXT,
    "message" TEXT,
    "user_id" TEXT,
    "session_id" TEXT,
    "ip_address" TEXT,
    "user_agent" TEXT,
    "request_url" TEXT,
    "request_method" TEXT,
    "response_status" INTEGER,
    "response_time" INTEGER,
    "error_code" TEXT,
    "stack_trace" TEXT,
    "request_body" TEXT,
    "response_body" TEXT,
    "correlation_id" TEXT,
    "component_name" TEXT,
    "thread_name" TEXT,
    "server_name" TEXT,
    "id" TEXT NOT NULL,
    "is_deleted" BOOLEAN NOT NULL,

    CONSTRAINT "SYS_SystemLog_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "SYS_TenantUsage" (
    "usage_date" TIMESTAMP(3),
    "tenant_id" TEXT,
    "active_users" INTEGER,
    "total_logins" INTEGER,
    "api_requests" BIGINT,
    "data_storage_mb" DECIMAL(65,30),
    "file_storage_mb" DECIMAL(65,30),
    "backup_storage_mb" DECIMAL(65,30),
    "cpu_usage_minutes" DECIMAL(65,30),
    "memory_usage_mb_hours" DECIMAL(65,30),
    "network_transfer_mb" DECIMAL(65,30),
    "report_generations" INTEGER,
    "skill_assessments" INTEGER,
    "notification_sent" INTEGER,
    "peak_concurrent_users" INTEGER,
    "peak_time" TIMESTAMP(3),
    "error_count" INTEGER,
    "response_time_avg_ms" DECIMAL(65,30),
    "uptime_percentage" DECIMAL(65,30),
    "billing_amount" DECIMAL(65,30),
    "collection_timestamp" TIMESTAMP(3),
    "id" TEXT NOT NULL,
    "is_deleted" BOOLEAN NOT NULL,

    CONSTRAINT "SYS_TenantUsage_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "SYS_TokenStore" (
    "id" TEXT,
    "tenant_id" TEXT,
    "user_id" TEXT,
    "token_type" TEXT,
    "token_value" TEXT,
    "token_hash" TEXT NOT NULL,
    "expires_at" TIMESTAMP(3),
    "issued_at" TIMESTAMP(3),
    "last_used_at" TIMESTAMP(3),
    "client_ip" TEXT,
    "user_agent" TEXT,
    "device_fingerprint" TEXT,
    "scope" TEXT,
    "is_revoked" BOOLEAN,
    "revoked_at" TIMESTAMP(3),
    "revoked_reason" TEXT,
    "is_deleted" BOOLEAN NOT NULL,

    CONSTRAINT "SYS_TokenStore_pkey" PRIMARY KEY ("token_hash")
);

-- CreateTable
CREATE TABLE "TRN_EmployeeSkillGrade" (
    "employee_id" TEXT,
    "job_type_id" TEXT,
    "skill_grade" TEXT,
    "skill_level" INTEGER,
    "effective_date" TIMESTAMP(3),
    "expiry_date" TIMESTAMP(3),
    "evaluation_date" TIMESTAMP(3),
    "evaluator_id" TEXT,
    "evaluation_comment" TEXT,
    "certification_flag" BOOLEAN,
    "next_evaluation_date" TIMESTAMP(3),
    "id" TEXT NOT NULL,
    "is_deleted" BOOLEAN NOT NULL,
    "tenant_id" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "created_by" TEXT NOT NULL,
    "updated_by" TEXT NOT NULL,

    CONSTRAINT "TRN_EmployeeSkillGrade_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "TRN_GoalProgress" (
    "goal_id" TEXT,
    "employee_id" TEXT,
    "goal_title" TEXT,
    "goal_description" TEXT,
    "goal_category" TEXT,
    "goal_type" TEXT,
    "priority_level" TEXT,
    "target_value" DECIMAL(65,30),
    "current_value" DECIMAL(65,30),
    "unit" TEXT,
    "start_date" TIMESTAMP(3),
    "target_date" TIMESTAMP(3),
    "progress_rate" DECIMAL(65,30),
    "achievement_status" TEXT,
    "supervisor_id" TEXT,
    "approval_status" TEXT,
    "approved_at" TIMESTAMP(3),
    "approved_by" TEXT,
    "completion_date" TIMESTAMP(3),
    "achievement_rate" DECIMAL(65,30),
    "self_evaluation" INTEGER,
    "supervisor_evaluation" INTEGER,
    "evaluation_comments" TEXT,
    "related_career_plan_id" TEXT,
    "related_skill_items" TEXT,
    "milestones" TEXT,
    "obstacles" TEXT,
    "support_needed" TEXT,
    "last_updated_at" TIMESTAMP(3),
    "next_review_date" TIMESTAMP(3),
    "id" TEXT NOT NULL,
    "is_deleted" BOOLEAN NOT NULL,
    "tenant_id" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "created_by" TEXT NOT NULL,
    "updated_by" TEXT NOT NULL,

    CONSTRAINT "TRN_GoalProgress_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "TRN_Notification" (
    "notification_id" TEXT,
    "recipient_id" TEXT,
    "sender_id" TEXT,
    "notification_type" TEXT,
    "notification_category" TEXT,
    "priority_level" TEXT,
    "title" TEXT,
    "message" TEXT,
    "message_format" TEXT,
    "action_url" TEXT,
    "action_label" TEXT,
    "delivery_method" TEXT,
    "delivery_status" TEXT,
    "sent_at" TIMESTAMP(3),
    "delivered_at" TIMESTAMP(3),
    "read_status" TEXT,
    "read_at" TIMESTAMP(3),
    "archived_at" TIMESTAMP(3),
    "expiry_date" TIMESTAMP(3),
    "retry_count" INTEGER,
    "max_retry_count" INTEGER,
    "last_retry_at" TIMESTAMP(3),
    "error_message" TEXT,
    "external_message_id" TEXT,
    "template_id" TEXT,
    "template_variables" TEXT,
    "related_entity_type" TEXT,
    "related_entity_id" TEXT,
    "batch_id" TEXT,
    "user_agent" TEXT,
    "ip_address" TEXT,
    "device_type" TEXT,
    "is_bulk_notification" BOOLEAN,
    "personalization_data" TEXT,
    "id" TEXT NOT NULL,
    "is_deleted" BOOLEAN NOT NULL,
    "tenant_id" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "created_by" TEXT NOT NULL,
    "updated_by" TEXT NOT NULL,

    CONSTRAINT "TRN_Notification_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "TRN_PDU" (
    "pdu_id" TEXT,
    "employee_id" TEXT,
    "certification_id" TEXT,
    "activity_type" TEXT,
    "activity_name" TEXT,
    "activity_description" TEXT,
    "provider_name" TEXT,
    "activity_date" TIMESTAMP(3),
    "start_time" TIMESTAMP(3),
    "end_time" TIMESTAMP(3),
    "duration_hours" DECIMAL(65,30),
    "pdu_points" DECIMAL(65,30),
    "pdu_category" TEXT,
    "pdu_subcategory" TEXT,
    "location" TEXT,
    "cost" DECIMAL(65,30),
    "cost_covered_by" TEXT,
    "evidence_type" TEXT,
    "evidence_file_path" TEXT,
    "certificate_number" TEXT,
    "instructor_name" TEXT,
    "learning_objectives" TEXT,
    "learning_outcomes" TEXT,
    "skills_developed" TEXT,
    "approval_status" TEXT,
    "approved_by" TEXT,
    "approval_date" TIMESTAMP(3),
    "approval_comment" TEXT,
    "expiry_date" TIMESTAMP(3),
    "is_recurring" BOOLEAN,
    "recurrence_pattern" TEXT,
    "related_training_id" TEXT,
    "related_project_id" TEXT,
    "id" TEXT NOT NULL,
    "is_deleted" BOOLEAN NOT NULL,
    "tenant_id" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "created_by" TEXT NOT NULL,
    "updated_by" TEXT NOT NULL,

    CONSTRAINT "TRN_PDU_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "TRN_ProjectRecord" (
    "project_record_id" TEXT,
    "employee_id" TEXT,
    "project_name" TEXT,
    "project_code" TEXT,
    "client_name" TEXT,
    "project_type" TEXT,
    "project_scale" TEXT,
    "start_date" TIMESTAMP(3),
    "end_date" TIMESTAMP(3),
    "participation_rate" DECIMAL(65,30),
    "role_title" TEXT,
    "responsibilities" TEXT,
    "technologies_used" TEXT,
    "skills_applied" TEXT,
    "achievements" TEXT,
    "challenges_faced" TEXT,
    "lessons_learned" TEXT,
    "team_size" INTEGER,
    "budget_range" TEXT,
    "project_status" TEXT,
    "evaluation_score" DECIMAL(65,30),
    "evaluation_comment" TEXT,
    "is_confidential" BOOLEAN,
    "is_public_reference" BOOLEAN,
    "id" TEXT NOT NULL,
    "is_deleted" BOOLEAN NOT NULL,
    "tenant_id" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "created_by" TEXT NOT NULL,
    "updated_by" TEXT NOT NULL,

    CONSTRAINT "TRN_ProjectRecord_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "TRN_SkillEvidence" (
    "evidence_id" TEXT,
    "employee_id" TEXT,
    "skill_id" TEXT,
    "evidence_type" TEXT,
    "evidence_title" TEXT,
    "evidence_description" TEXT,
    "skill_level_demonstrated" TEXT,
    "evidence_date" TIMESTAMP(3),
    "validity_start_date" TIMESTAMP(3),
    "validity_end_date" TIMESTAMP(3),
    "file_path" TEXT,
    "file_type" TEXT,
    "file_size_kb" INTEGER,
    "external_url" TEXT,
    "issuer_name" TEXT,
    "issuer_type" TEXT,
    "certificate_number" TEXT,
    "verification_method" TEXT,
    "verification_status" TEXT,
    "verified_by" TEXT,
    "verification_date" TIMESTAMP(3),
    "verification_comment" TEXT,
    "related_project_id" TEXT,
    "related_training_id" TEXT,
    "related_certification_id" TEXT,
    "impact_score" DECIMAL(65,30),
    "complexity_level" TEXT,
    "team_size" INTEGER,
    "role_in_activity" TEXT,
    "technologies_used" TEXT,
    "achievements" TEXT,
    "lessons_learned" TEXT,
    "is_public" BOOLEAN,
    "is_portfolio_item" BOOLEAN,
    "tags" TEXT,
    "id" TEXT NOT NULL,
    "is_deleted" BOOLEAN NOT NULL,
    "tenant_id" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "created_by" TEXT NOT NULL,
    "updated_by" TEXT NOT NULL,

    CONSTRAINT "TRN_SkillEvidence_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "TRN_SkillRecord" (
    "employee_id" TEXT,
    "skill_item_id" TEXT,
    "skill_level" INTEGER,
    "self_assessment" INTEGER,
    "manager_assessment" INTEGER,
    "evidence_description" TEXT,
    "acquisition_date" TIMESTAMP(3),
    "last_used_date" TIMESTAMP(3),
    "expiry_date" TIMESTAMP(3),
    "certification_id" TEXT,
    "skill_category_id" TEXT,
    "assessment_date" TIMESTAMP(3),
    "assessor_id" TEXT,
    "skill_status" TEXT,
    "learning_hours" INTEGER,
    "project_experience_count" INTEGER,
    "id" TEXT NOT NULL,
    "is_deleted" BOOLEAN NOT NULL,
    "tenant_id" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "created_by" TEXT NOT NULL,
    "updated_by" TEXT NOT NULL,

    CONSTRAINT "TRN_SkillRecord_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "TRN_TrainingHistory" (
    "training_history_id" TEXT,
    "employee_id" TEXT,
    "training_program_id" TEXT,
    "training_name" TEXT,
    "training_type" TEXT,
    "training_category" TEXT,
    "provider_name" TEXT,
    "instructor_name" TEXT,
    "start_date" TIMESTAMP(3),
    "end_date" TIMESTAMP(3),
    "duration_hours" DECIMAL(65,30),
    "location" TEXT,
    "cost" DECIMAL(65,30),
    "cost_covered_by" TEXT,
    "attendance_status" TEXT,
    "completion_rate" DECIMAL(65,30),
    "test_score" DECIMAL(65,30),
    "grade" TEXT,
    "certificate_obtained" BOOLEAN,
    "certificate_number" TEXT,
    "pdu_earned" DECIMAL(65,30),
    "skills_acquired" TEXT,
    "learning_objectives" TEXT,
    "learning_outcomes" TEXT,
    "feedback" TEXT,
    "satisfaction_score" DECIMAL(65,30),
    "recommendation_score" DECIMAL(65,30),
    "follow_up_required" BOOLEAN,
    "follow_up_date" TIMESTAMP(3),
    "manager_approval" BOOLEAN,
    "approved_by" TEXT,
    "id" TEXT NOT NULL,
    "is_deleted" BOOLEAN NOT NULL,
    "tenant_id" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "created_by" TEXT NOT NULL,
    "updated_by" TEXT NOT NULL,

    CONSTRAINT "TRN_TrainingHistory_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "WRK_BatchJobLog" (
    "job_id" TEXT,
    "job_name" TEXT,
    "job_type" TEXT,
    "status" TEXT,
    "start_time" TIMESTAMP(3),
    "end_time" TIMESTAMP(3),
    "total_records" INTEGER,
    "processed_records" INTEGER,
    "success_records" INTEGER,
    "error_records" INTEGER,
    "error_details" TEXT,
    "input_file_path" TEXT,
    "output_file_path" TEXT,
    "executed_by" TEXT,
    "progress_percentage" DECIMAL(65,30),
    "execution_environment" TEXT,
    "job_parameters" TEXT,
    "id" TEXT NOT NULL,
    "is_deleted" BOOLEAN NOT NULL,

    CONSTRAINT "WRK_BatchJobLog_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "MST_Employee_email_key" ON "MST_Employee"("email");

-- CreateIndex
CREATE UNIQUE INDEX "MST_SkillGrade_grade_level_key" ON "MST_SkillGrade"("grade_level");

-- CreateIndex
CREATE UNIQUE INDEX "MST_Tenant_tenant_code_key" ON "MST_Tenant"("tenant_code");

-- CreateIndex
CREATE UNIQUE INDEX "MST_Tenant_domain_name_key" ON "MST_Tenant"("domain_name");

-- CreateIndex
CREATE UNIQUE INDEX "MST_Tenant_subdomain_key" ON "MST_Tenant"("subdomain");

-- CreateIndex
CREATE UNIQUE INDEX "MST_TrainingProgram_program_code_key" ON "MST_TrainingProgram"("program_code");

-- CreateIndex
CREATE UNIQUE INDEX "MST_UserAuth_login_id_key" ON "MST_UserAuth"("login_id");

-- CreateIndex
CREATE UNIQUE INDEX "MST_UserAuth_employee_id_key" ON "MST_UserAuth"("employee_id");

-- CreateIndex
CREATE UNIQUE INDEX "SYS_BackupHistory_backup_id_key" ON "SYS_BackupHistory"("backup_id");

-- CreateIndex
CREATE UNIQUE INDEX "SYS_MasterData_master_key_key" ON "SYS_MasterData"("master_key");

-- CreateIndex
CREATE UNIQUE INDEX "SYS_SkillMatrix_employee_id_skill_id_key" ON "SYS_SkillMatrix"("employee_id", "skill_id");

-- CreateIndex
CREATE UNIQUE INDEX "SYS_TenantUsage_usage_date_tenant_id_key" ON "SYS_TenantUsage"("usage_date", "tenant_id");

-- CreateIndex
CREATE UNIQUE INDEX "TRN_GoalProgress_goal_id_key" ON "TRN_GoalProgress"("goal_id");

-- CreateIndex
CREATE UNIQUE INDEX "TRN_Notification_notification_id_key" ON "TRN_Notification"("notification_id");

-- CreateIndex
CREATE UNIQUE INDEX "TRN_PDU_pdu_id_key" ON "TRN_PDU"("pdu_id");

-- CreateIndex
CREATE UNIQUE INDEX "TRN_ProjectRecord_project_record_id_key" ON "TRN_ProjectRecord"("project_record_id");

-- CreateIndex
CREATE UNIQUE INDEX "TRN_SkillEvidence_evidence_id_key" ON "TRN_SkillEvidence"("evidence_id");

-- CreateIndex
CREATE UNIQUE INDEX "TRN_SkillRecord_employee_id_skill_item_id_key" ON "TRN_SkillRecord"("employee_id", "skill_item_id");

-- CreateIndex
CREATE UNIQUE INDEX "TRN_TrainingHistory_training_history_id_key" ON "TRN_TrainingHistory"("training_history_id");

-- CreateIndex
CREATE UNIQUE INDEX "WRK_BatchJobLog_job_id_key" ON "WRK_BatchJobLog"("job_id");
