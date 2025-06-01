-- 全テーブル統合DDL
-- 生成日時: 2025-06-01 19:42:44

-- MST_UserAuth (ユーザー認証情報) DDL
-- 生成日時: 2025-06-01 19:42:42

CREATE TABLE MST_UserAuth (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    user_id VARCHAR(50),
    login_id VARCHAR(100),
    password_hash VARCHAR(255),
    password_salt VARCHAR(100),
    employee_id VARCHAR(50),
    account_status ENUM DEFAULT 'ACTIVE',
    last_login_at TIMESTAMP,
    last_login_ip VARCHAR(45),
    failed_login_count INT DEFAULT 0,
    last_failed_login_at TIMESTAMP,
    password_changed_at TIMESTAMP,
    password_expires_at TIMESTAMP,
    mfa_enabled BOOLEAN DEFAULT False,
    mfa_secret VARCHAR(255),
    recovery_token VARCHAR(255),
    recovery_token_expires_at TIMESTAMP,
    session_timeout INT,
    external_auth_provider VARCHAR(50),
    external_auth_id VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_user_id ON MST_UserAuth (user_id);
CREATE UNIQUE INDEX idx_login_id ON MST_UserAuth (login_id);
CREATE UNIQUE INDEX idx_employee_id ON MST_UserAuth (employee_id);
CREATE INDEX idx_account_status ON MST_UserAuth (account_status);
CREATE INDEX idx_last_login ON MST_UserAuth (last_login_at);
CREATE INDEX idx_password_expires ON MST_UserAuth (password_expires_at);
CREATE INDEX idx_external_auth ON MST_UserAuth (external_auth_provider, external_auth_id);

-- 外部キー制約
ALTER TABLE MST_UserAuth ADD CONSTRAINT fk_userauth_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;


-- MST_Role (ロール情報) DDL
-- 生成日時: 2025-06-01 19:42:42

CREATE TABLE MST_Role (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    role_code VARCHAR(20),
    role_name VARCHAR(100),
    role_name_short VARCHAR(50),
    role_category ENUM,
    role_level INT,
    parent_role_id VARCHAR(50),
    is_system_role BOOLEAN DEFAULT False,
    is_tenant_specific BOOLEAN DEFAULT False,
    max_users INT,
    role_priority INT DEFAULT 999,
    auto_assign_conditions JSON,
    role_status ENUM DEFAULT 'ACTIVE',
    effective_from DATE,
    effective_to DATE,
    sort_order INT,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_role_code ON MST_Role (role_code);
CREATE INDEX idx_role_category ON MST_Role (role_category);
CREATE INDEX idx_role_level ON MST_Role (role_level);
CREATE INDEX idx_parent_role ON MST_Role (parent_role_id);
CREATE INDEX idx_system_role ON MST_Role (is_system_role);
CREATE INDEX idx_tenant_specific ON MST_Role (is_tenant_specific);
CREATE INDEX idx_role_status ON MST_Role (role_status);
CREATE INDEX idx_effective_period ON MST_Role (effective_from, effective_to);
CREATE INDEX idx_sort_order ON MST_Role (sort_order);

-- 外部キー制約
ALTER TABLE MST_Role ADD CONSTRAINT fk_role_parent FOREIGN KEY (parent_role_id) REFERENCES MST_Role(id) ON UPDATE CASCADE ON DELETE SET NULL;


-- MST_Permission (権限情報) DDL
-- 生成日時: 2025-06-01 19:42:42

CREATE TABLE MST_Permission (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    permission_code VARCHAR(50),
    permission_name VARCHAR(100),
    permission_name_short VARCHAR(50),
    permission_category ENUM,
    resource_type VARCHAR(50),
    action_type ENUM,
    scope_level ENUM,
    parent_permission_id VARCHAR(50),
    is_system_permission BOOLEAN DEFAULT False,
    requires_conditions BOOLEAN DEFAULT False,
    condition_expression TEXT,
    risk_level INT DEFAULT 1,
    requires_approval BOOLEAN DEFAULT False,
    audit_required BOOLEAN DEFAULT False,
    permission_status ENUM DEFAULT 'ACTIVE',
    effective_from DATE,
    effective_to DATE,
    sort_order INT,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_permission_code ON MST_Permission (permission_code);
CREATE INDEX idx_permission_category ON MST_Permission (permission_category);
CREATE INDEX idx_resource_action ON MST_Permission (resource_type, action_type);
CREATE INDEX idx_scope_level ON MST_Permission (scope_level);
CREATE INDEX idx_parent_permission ON MST_Permission (parent_permission_id);
CREATE INDEX idx_system_permission ON MST_Permission (is_system_permission);
CREATE INDEX idx_risk_level ON MST_Permission (risk_level);
CREATE INDEX idx_permission_status ON MST_Permission (permission_status);
CREATE INDEX idx_effective_period ON MST_Permission (effective_from, effective_to);

-- 外部キー制約
ALTER TABLE MST_Permission ADD CONSTRAINT fk_permission_parent FOREIGN KEY (parent_permission_id) REFERENCES MST_Permission(id) ON UPDATE CASCADE ON DELETE SET NULL;


-- MST_UserRole (ユーザーロール紐付け) DDL
-- 生成日時: 2025-06-01 19:42:42

CREATE TABLE MST_UserRole (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    user_id VARCHAR(50),
    role_id VARCHAR(50),
    assignment_type ENUM DEFAULT 'DIRECT',
    assigned_by VARCHAR(50),
    assignment_reason TEXT,
    effective_from TIMESTAMP DEFAULT 'CURRENT_TIMESTAMP',
    effective_to TIMESTAMP,
    is_primary_role BOOLEAN DEFAULT False,
    priority_order INT DEFAULT 999,
    conditions JSON,
    delegation_source_user_id VARCHAR(50),
    delegation_expires_at TIMESTAMP,
    auto_assigned BOOLEAN DEFAULT False,
    requires_approval BOOLEAN DEFAULT False,
    approval_status ENUM,
    approved_by VARCHAR(50),
    approved_at TIMESTAMP,
    assignment_status ENUM DEFAULT 'ACTIVE',
    last_used_at TIMESTAMP,
    usage_count INT DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_user_role ON MST_UserRole (user_id, role_id);
CREATE INDEX idx_user_id ON MST_UserRole (user_id);
CREATE INDEX idx_role_id ON MST_UserRole (role_id);
CREATE INDEX idx_assignment_type ON MST_UserRole (assignment_type);
CREATE INDEX idx_assigned_by ON MST_UserRole (assigned_by);
CREATE INDEX idx_effective_period ON MST_UserRole (effective_from, effective_to);
CREATE INDEX idx_primary_role ON MST_UserRole (user_id, is_primary_role);
CREATE INDEX idx_assignment_status ON MST_UserRole (assignment_status);
CREATE INDEX idx_approval_status ON MST_UserRole (approval_status);
CREATE INDEX idx_delegation_source ON MST_UserRole (delegation_source_user_id);

-- 外部キー制約
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_user FOREIGN KEY (user_id) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_role FOREIGN KEY (role_id) REFERENCES MST_Role(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_assigned_by FOREIGN KEY (assigned_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_delegation_source FOREIGN KEY (delegation_source_user_id) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_approved_by FOREIGN KEY (approved_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE SET NULL;


-- MST_Employee (社員基本情報) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_Employee (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    employee_code VARCHAR(30),
    full_name VARCHAR(100),
    full_name_kana VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(20),
    hire_date DATE,
    birth_date DATE,
    gender ENUM,
    department_id VARCHAR(50),
    position_id VARCHAR(50),
    job_type_id VARCHAR(50),
    employment_status ENUM DEFAULT 'FULL_TIME',
    manager_id VARCHAR(50),
    employee_status ENUM DEFAULT 'ACTIVE',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_employee_code ON MST_Employee (employee_code);
CREATE UNIQUE INDEX idx_email ON MST_Employee (email);
CREATE INDEX idx_department ON MST_Employee (department_id);
CREATE INDEX idx_manager ON MST_Employee (manager_id);
CREATE INDEX idx_status ON MST_Employee (employee_status);
CREATE INDEX idx_hire_date ON MST_Employee (hire_date);

-- 外部キー制約
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_department FOREIGN KEY (department_id) REFERENCES MST_Department(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_position FOREIGN KEY (position_id) REFERENCES MST_Position(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_job_type FOREIGN KEY (job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_manager FOREIGN KEY (manager_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;


-- MST_Department (部署マスタ) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_Department (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    department_code VARCHAR(20),
    department_name VARCHAR(100),
    department_name_short VARCHAR(50),
    parent_department_id VARCHAR(50),
    department_level INT,
    department_type ENUM,
    manager_id VARCHAR(50),
    deputy_manager_id VARCHAR(50),
    cost_center_code VARCHAR(20),
    budget_amount DECIMAL(15,2),
    location VARCHAR(200),
    phone_number VARCHAR(20),
    email_address VARCHAR(255),
    establishment_date DATE,
    abolition_date DATE,
    department_status ENUM DEFAULT 'ACTIVE',
    sort_order INT,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_department_code ON MST_Department (department_code);
CREATE INDEX idx_parent_department ON MST_Department (parent_department_id);
CREATE INDEX idx_department_level ON MST_Department (department_level);
CREATE INDEX idx_department_type ON MST_Department (department_type);
CREATE INDEX idx_manager ON MST_Department (manager_id);
CREATE INDEX idx_status ON MST_Department (department_status);
CREATE INDEX idx_cost_center ON MST_Department (cost_center_code);
CREATE INDEX idx_sort_order ON MST_Department (sort_order);

-- 外部キー制約
ALTER TABLE MST_Department ADD CONSTRAINT fk_department_parent FOREIGN KEY (parent_department_id) REFERENCES MST_Department(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_Department ADD CONSTRAINT fk_department_manager FOREIGN KEY (manager_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_Department ADD CONSTRAINT fk_department_deputy FOREIGN KEY (deputy_manager_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;


-- MST_Position (役職マスタ) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_Position (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    position_code VARCHAR(20),
    position_name VARCHAR(100),
    position_name_short VARCHAR(50),
    position_level INT,
    position_rank INT,
    position_category ENUM,
    authority_level INT,
    approval_limit DECIMAL(15,2),
    salary_grade VARCHAR(10),
    allowance_amount DECIMAL(10,2),
    is_management BOOLEAN DEFAULT False,
    is_executive BOOLEAN DEFAULT False,
    requires_approval BOOLEAN DEFAULT False,
    can_hire BOOLEAN DEFAULT False,
    can_evaluate BOOLEAN DEFAULT False,
    position_status ENUM DEFAULT 'ACTIVE',
    sort_order INT,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_position_code ON MST_Position (position_code);
CREATE INDEX idx_position_level ON MST_Position (position_level);
CREATE INDEX idx_position_rank ON MST_Position (position_rank);
CREATE INDEX idx_position_category ON MST_Position (position_category);
CREATE INDEX idx_authority_level ON MST_Position (authority_level);
CREATE INDEX idx_salary_grade ON MST_Position (salary_grade);
CREATE INDEX idx_status ON MST_Position (position_status);
CREATE INDEX idx_management_flags ON MST_Position (is_management, is_executive);
CREATE INDEX idx_sort_order ON MST_Position (sort_order);


-- MST_SkillHierarchy (スキル階層マスタ) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_SkillHierarchy (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    skill_id VARCHAR(50),
    parent_skill_id VARCHAR(50),
    hierarchy_level INTEGER,
    skill_path VARCHAR(500),
    sort_order INTEGER DEFAULT 0,
    is_leaf BOOLEAN DEFAULT True,
    skill_category ENUM,
    description TEXT,
    is_active BOOLEAN DEFAULT True,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE INDEX idx_skill_id ON MST_SkillHierarchy (skill_id);
CREATE INDEX idx_parent_skill ON MST_SkillHierarchy (parent_skill_id);
CREATE INDEX idx_hierarchy_level ON MST_SkillHierarchy (hierarchy_level);
CREATE INDEX idx_skill_path ON MST_SkillHierarchy (skill_path);
CREATE INDEX idx_category_level ON MST_SkillHierarchy (skill_category, hierarchy_level);
CREATE INDEX idx_parent_sort ON MST_SkillHierarchy (parent_skill_id, sort_order);

-- 外部キー制約
ALTER TABLE MST_SkillHierarchy ADD CONSTRAINT fk_hierarchy_skill FOREIGN KEY (skill_id) REFERENCES MST_SkillItem(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_SkillHierarchy ADD CONSTRAINT fk_hierarchy_parent FOREIGN KEY (parent_skill_id) REFERENCES MST_SkillHierarchy(skill_id) ON UPDATE CASCADE ON DELETE CASCADE;


-- MST_Certification (資格情報) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_Certification (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    certification_code VARCHAR(50),
    certification_name VARCHAR(200),
    certification_name_en VARCHAR(200),
    issuer VARCHAR(100),
    issuer_country VARCHAR(10),
    certification_category ENUM,
    certification_level ENUM,
    validity_period_months INTEGER,
    renewal_required BOOLEAN DEFAULT False,
    renewal_requirements TEXT,
    exam_fee DECIMAL(10,2),
    exam_language VARCHAR(50),
    exam_format ENUM,
    official_url VARCHAR(500),
    description TEXT,
    skill_category_id VARCHAR(50),
    is_recommended BOOLEAN DEFAULT False,
    is_active BOOLEAN DEFAULT True,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_certification_code ON MST_Certification (certification_code);
CREATE INDEX idx_certification_name ON MST_Certification (certification_name);
CREATE INDEX idx_issuer ON MST_Certification (issuer);
CREATE INDEX idx_category_level ON MST_Certification (certification_category, certification_level);
CREATE INDEX idx_recommended ON MST_Certification (is_recommended, is_active);
CREATE INDEX idx_skill_category ON MST_Certification (skill_category_id);

-- 外部キー制約
ALTER TABLE MST_Certification ADD CONSTRAINT fk_certification_skill_category FOREIGN KEY (skill_category_id) REFERENCES MST_SkillCategory(id) ON UPDATE CASCADE ON DELETE SET NULL;


-- MST_CareerPlan (目標・キャリアプラン) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_CareerPlan (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    career_plan_id VARCHAR(50),
    employee_id VARCHAR(50),
    plan_name VARCHAR(200),
    plan_description TEXT,
    plan_type ENUM,
    target_position_id VARCHAR(50),
    target_job_type_id VARCHAR(50),
    target_department_id VARCHAR(50),
    current_level ENUM,
    target_level ENUM,
    plan_start_date DATE,
    plan_end_date DATE,
    milestone_1_date DATE,
    milestone_1_description VARCHAR(500),
    milestone_2_date DATE,
    milestone_2_description VARCHAR(500),
    milestone_3_date DATE,
    milestone_3_description VARCHAR(500),
    required_skills TEXT,
    required_certifications TEXT,
    required_experiences TEXT,
    development_actions TEXT,
    training_plan TEXT,
    mentor_id VARCHAR(50),
    supervisor_id VARCHAR(50),
    plan_status ENUM DEFAULT 'DRAFT',
    progress_percentage DECIMAL(5,2) DEFAULT 0.0,
    last_review_date DATE,
    next_review_date DATE,
    review_frequency ENUM DEFAULT 'QUARTERLY',
    success_criteria TEXT,
    risk_factors TEXT,
    support_resources TEXT,
    budget_allocated DECIMAL(10,2),
    budget_used DECIMAL(10,2) DEFAULT 0.0,
    priority_level ENUM DEFAULT 'NORMAL',
    visibility_level ENUM DEFAULT 'MANAGER',
    template_id VARCHAR(50),
    custom_fields TEXT,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_career_plan_id ON MST_CareerPlan (career_plan_id);
CREATE INDEX idx_employee_id ON MST_CareerPlan (employee_id);
CREATE INDEX idx_plan_type ON MST_CareerPlan (plan_type);
CREATE INDEX idx_target_position ON MST_CareerPlan (target_position_id);
CREATE INDEX idx_target_job_type ON MST_CareerPlan (target_job_type_id);
CREATE INDEX idx_plan_status ON MST_CareerPlan (plan_status);
CREATE INDEX idx_plan_period ON MST_CareerPlan (plan_start_date, plan_end_date);
CREATE INDEX idx_review_date ON MST_CareerPlan (next_review_date);
CREATE INDEX idx_mentor_id ON MST_CareerPlan (mentor_id);
CREATE INDEX idx_supervisor_id ON MST_CareerPlan (supervisor_id);
CREATE INDEX idx_priority_level ON MST_CareerPlan (priority_level);

-- 外部キー制約
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_target_position FOREIGN KEY (target_position_id) REFERENCES MST_Position(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_target_job_type FOREIGN KEY (target_job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_target_department FOREIGN KEY (target_department_id) REFERENCES MST_Department(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_mentor FOREIGN KEY (mentor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_supervisor FOREIGN KEY (supervisor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;


-- MST_ReportTemplate (帳票テンプレート) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_ReportTemplate (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    id VARCHAR(50),
    tenant_id VARCHAR(50),
    template_key VARCHAR(100),
    template_name VARCHAR(200),
    report_category ENUM,
    output_format ENUM,
    language_code VARCHAR(10) DEFAULT 'ja',
    template_content TEXT,
    style_sheet TEXT,
    parameters_schema TEXT,
    data_source_config TEXT,
    page_settings TEXT,
    header_template TEXT,
    footer_template TEXT,
    is_default BOOLEAN DEFAULT False,
    is_active BOOLEAN DEFAULT True,
    version VARCHAR(20) DEFAULT '1.0.0',
    preview_image_url VARCHAR(500),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_report_template_tenant_key ON MST_ReportTemplate (tenant_id, template_key, language_code);
CREATE INDEX idx_report_template_category ON MST_ReportTemplate (report_category);
CREATE INDEX idx_report_template_format ON MST_ReportTemplate (output_format);
CREATE INDEX idx_report_template_language ON MST_ReportTemplate (language_code);
CREATE INDEX idx_report_template_default ON MST_ReportTemplate (is_default, is_active);

-- 外部キー制約


-- MST_SystemConfig (システム設定) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_SystemConfig (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    config_key VARCHAR(100),
    config_name VARCHAR(200),
    config_value TEXT,
    config_type ENUM,
    config_category ENUM,
    default_value TEXT,
    validation_rule TEXT,
    description TEXT,
    is_encrypted BOOLEAN DEFAULT False,
    is_system_only BOOLEAN DEFAULT False,
    is_user_configurable BOOLEAN DEFAULT True,
    requires_restart BOOLEAN DEFAULT False,
    environment ENUM DEFAULT 'ALL',
    tenant_specific BOOLEAN DEFAULT False,
    last_modified_by VARCHAR(50),
    last_modified_reason TEXT,
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT True,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_config_key ON MST_SystemConfig (config_key);
CREATE INDEX idx_config_category ON MST_SystemConfig (config_category);
CREATE INDEX idx_config_type ON MST_SystemConfig (config_type);
CREATE INDEX idx_user_configurable ON MST_SystemConfig (is_user_configurable, is_active);
CREATE INDEX idx_environment ON MST_SystemConfig (environment, is_active);
CREATE INDEX idx_tenant_specific ON MST_SystemConfig (tenant_specific, is_active);
CREATE INDEX idx_sort_order ON MST_SystemConfig (sort_order);

-- 外部キー制約


-- MST_Tenant (テナント管理) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_Tenant (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    tenant_id VARCHAR(50),
    tenant_code VARCHAR(20),
    tenant_name VARCHAR(200),
    tenant_name_en VARCHAR(200),
    tenant_short_name VARCHAR(50),
    tenant_type ENUM,
    parent_tenant_id VARCHAR(50),
    tenant_level INTEGER DEFAULT 1,
    domain_name VARCHAR(100),
    subdomain VARCHAR(50),
    logo_url VARCHAR(500),
    primary_color VARCHAR(7),
    secondary_color VARCHAR(7),
    timezone VARCHAR(50) DEFAULT 'Asia/Tokyo',
    locale VARCHAR(10) DEFAULT 'ja_JP',
    currency_code VARCHAR(3) DEFAULT 'JPY',
    date_format VARCHAR(20) DEFAULT 'YYYY-MM-DD',
    time_format VARCHAR(20) DEFAULT 'HH:mm:ss',
    admin_email VARCHAR(255),
    contact_email VARCHAR(255),
    phone_number VARCHAR(20),
    address TEXT,
    postal_code VARCHAR(10),
    country_code VARCHAR(2) DEFAULT 'JP',
    subscription_plan ENUM DEFAULT 'BASIC',
    max_users INTEGER DEFAULT 100,
    max_storage_gb INTEGER DEFAULT 10,
    features_enabled TEXT,
    custom_settings TEXT,
    security_policy TEXT,
    data_retention_days INTEGER DEFAULT 2555,
    backup_enabled BOOLEAN DEFAULT True,
    backup_frequency ENUM DEFAULT 'DAILY',
    contract_start_date DATE,
    contract_end_date DATE,
    trial_end_date DATE,
    billing_cycle ENUM DEFAULT 'MONTHLY',
    monthly_fee DECIMAL(10,2),
    setup_fee DECIMAL(10,2),
    status ENUM DEFAULT 'TRIAL',
    activation_date DATE,
    suspension_date DATE,
    suspension_reason TEXT,
    last_login_date DATE,
    current_users_count INTEGER DEFAULT 0,
    storage_used_gb DECIMAL(10,3) DEFAULT 0.0,
    api_rate_limit INTEGER DEFAULT 1000,
    sso_enabled BOOLEAN DEFAULT False,
    sso_provider VARCHAR(50),
    sso_config TEXT,
    webhook_url VARCHAR(500),
    webhook_secret VARCHAR(100),
    created_by VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_tenant_id ON MST_Tenant (tenant_id);
CREATE UNIQUE INDEX idx_tenant_code ON MST_Tenant (tenant_code);
CREATE UNIQUE INDEX idx_domain_name ON MST_Tenant (domain_name);
CREATE UNIQUE INDEX idx_subdomain ON MST_Tenant (subdomain);
CREATE INDEX idx_tenant_type ON MST_Tenant (tenant_type);
CREATE INDEX idx_parent_tenant_id ON MST_Tenant (parent_tenant_id);
CREATE INDEX idx_subscription_plan ON MST_Tenant (subscription_plan);
CREATE INDEX idx_status ON MST_Tenant (status);
CREATE INDEX idx_contract_period ON MST_Tenant (contract_start_date, contract_end_date);
CREATE INDEX idx_admin_email ON MST_Tenant (admin_email);

-- 外部キー制約
ALTER TABLE MST_Tenant ADD CONSTRAINT fk_tenant_parent FOREIGN KEY (parent_tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE SET NULL;


-- MST_TenantSettings (テナント設定) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_TenantSettings (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    id VARCHAR(50),
    tenant_id VARCHAR(50),
    setting_category ENUM,
    setting_key VARCHAR(100),
    setting_name VARCHAR(200),
    setting_description TEXT,
    data_type ENUM,
    setting_value TEXT,
    default_value TEXT,
    validation_rules TEXT,
    is_required BOOLEAN DEFAULT False,
    is_encrypted BOOLEAN DEFAULT False,
    is_system_managed BOOLEAN DEFAULT False,
    is_user_configurable BOOLEAN DEFAULT True,
    display_order INTEGER DEFAULT 0,
    effective_from TIMESTAMP,
    effective_until TIMESTAMP,
    last_modified_by VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_tenant_settings_tenant_key ON MST_TenantSettings (tenant_id, setting_key);
CREATE INDEX idx_tenant_settings_category ON MST_TenantSettings (setting_category);
CREATE INDEX idx_tenant_settings_configurable ON MST_TenantSettings (is_user_configurable);
CREATE INDEX idx_tenant_settings_system_managed ON MST_TenantSettings (is_system_managed);
CREATE INDEX idx_tenant_settings_display_order ON MST_TenantSettings (tenant_id, setting_category, display_order);
CREATE INDEX idx_tenant_settings_effective ON MST_TenantSettings (effective_from, effective_until);

-- 外部キー制約
ALTER TABLE MST_TenantSettings ADD CONSTRAINT fk_tenant_settings_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(id) ON UPDATE CASCADE ON DELETE CASCADE;


-- MST_NotificationSettings (通知設定) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_NotificationSettings (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    id VARCHAR(50),
    tenant_id VARCHAR(50),
    setting_key VARCHAR(100),
    setting_name VARCHAR(200),
    notification_type ENUM,
    target_audience ENUM,
    trigger_event VARCHAR(100),
    frequency_type ENUM DEFAULT 'IMMEDIATE',
    frequency_value INTEGER,
    template_id VARCHAR(50),
    channel_config TEXT,
    is_enabled BOOLEAN DEFAULT True,
    priority_level ENUM DEFAULT 'MEDIUM',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_notification_settings_tenant_key ON MST_NotificationSettings (tenant_id, setting_key);
CREATE INDEX idx_notification_settings_type ON MST_NotificationSettings (notification_type);
CREATE INDEX idx_notification_settings_event ON MST_NotificationSettings (trigger_event);
CREATE INDEX idx_notification_settings_enabled ON MST_NotificationSettings (is_enabled);
CREATE INDEX idx_notification_settings_template ON MST_NotificationSettings (template_id);

-- 外部キー制約
ALTER TABLE MST_NotificationSettings ADD CONSTRAINT fk_notification_settings_template FOREIGN KEY (template_id) REFERENCES MST_NotificationTemplate(id) ON UPDATE CASCADE ON DELETE SET NULL;


-- MST_NotificationTemplate (通知テンプレート) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_NotificationTemplate (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    id VARCHAR(50),
    tenant_id VARCHAR(50),
    template_key VARCHAR(100),
    template_name VARCHAR(200),
    notification_type ENUM,
    language_code VARCHAR(10) DEFAULT 'ja',
    subject_template VARCHAR(500),
    body_template TEXT,
    format_type ENUM DEFAULT 'PLAIN',
    parameters TEXT,
    sample_data TEXT,
    is_default BOOLEAN DEFAULT False,
    is_active BOOLEAN DEFAULT True,
    version VARCHAR(20) DEFAULT '1.0.0',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_notification_template_tenant_key_type ON MST_NotificationTemplate (tenant_id, template_key, notification_type, language_code);
CREATE INDEX idx_notification_template_type ON MST_NotificationTemplate (notification_type);
CREATE INDEX idx_notification_template_language ON MST_NotificationTemplate (language_code);
CREATE INDEX idx_notification_template_default ON MST_NotificationTemplate (is_default, is_active);
CREATE INDEX idx_notification_template_key ON MST_NotificationTemplate (template_key);

-- 外部キー制約


-- MST_SkillCategory (スキルカテゴリマスタ) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_SkillCategory (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    category_code VARCHAR(20),
    category_name VARCHAR(100),
    category_name_short VARCHAR(50),
    category_name_en VARCHAR(100),
    category_type ENUM,
    parent_category_id VARCHAR(50),
    category_level INT DEFAULT 1,
    category_path VARCHAR(500),
    is_system_category BOOLEAN DEFAULT False,
    is_leaf_category BOOLEAN DEFAULT True,
    skill_count INT DEFAULT 0,
    evaluation_method ENUM,
    max_level INT,
    icon_url VARCHAR(255),
    color_code VARCHAR(7),
    display_order INT DEFAULT 999,
    is_popular BOOLEAN DEFAULT False,
    category_status ENUM DEFAULT 'ACTIVE',
    effective_from DATE,
    effective_to DATE,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_category_code ON MST_SkillCategory (category_code);
CREATE INDEX idx_category_type ON MST_SkillCategory (category_type);
CREATE INDEX idx_parent_category ON MST_SkillCategory (parent_category_id);
CREATE INDEX idx_category_level ON MST_SkillCategory (category_level);
CREATE INDEX idx_category_path ON MST_SkillCategory (category_path);
CREATE INDEX idx_system_category ON MST_SkillCategory (is_system_category);
CREATE INDEX idx_leaf_category ON MST_SkillCategory (is_leaf_category);
CREATE INDEX idx_category_status ON MST_SkillCategory (category_status);
CREATE INDEX idx_display_order ON MST_SkillCategory (parent_category_id, display_order);
CREATE INDEX idx_popular_category ON MST_SkillCategory (is_popular);

-- 外部キー制約
ALTER TABLE MST_SkillCategory ADD CONSTRAINT fk_skillcategory_parent FOREIGN KEY (parent_category_id) REFERENCES MST_SkillCategory(id) ON UPDATE CASCADE ON DELETE SET NULL;


-- MST_JobType (職種マスタ) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_JobType (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    job_type_code VARCHAR(20),
    job_type_name VARCHAR(100),
    job_type_name_en VARCHAR(100),
    job_category ENUM,
    job_level ENUM,
    description TEXT,
    required_experience_years INTEGER,
    salary_grade_min INTEGER,
    salary_grade_max INTEGER,
    career_path TEXT,
    required_certifications TEXT,
    required_skills TEXT,
    department_affinity TEXT,
    remote_work_eligible BOOLEAN DEFAULT False,
    travel_frequency ENUM,
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT True,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_job_type_code ON MST_JobType (job_type_code);
CREATE INDEX idx_job_type_name ON MST_JobType (job_type_name);
CREATE INDEX idx_job_category ON MST_JobType (job_category);
CREATE INDEX idx_job_level ON MST_JobType (job_level);
CREATE INDEX idx_category_level ON MST_JobType (job_category, job_level);
CREATE INDEX idx_remote_eligible ON MST_JobType (remote_work_eligible, is_active);
CREATE INDEX idx_sort_order ON MST_JobType (sort_order);

-- 外部キー制約


-- MST_SkillGrade (スキルグレードマスタ) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_SkillGrade (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    grade_code VARCHAR(20),
    grade_name VARCHAR(50),
    grade_name_short VARCHAR(10),
    grade_level INTEGER,
    description TEXT,
    evaluation_criteria TEXT,
    required_experience_months INTEGER,
    skill_indicators TEXT,
    competency_requirements TEXT,
    certification_requirements TEXT,
    project_complexity ENUM,
    mentoring_capability BOOLEAN DEFAULT False,
    leadership_level ENUM,
    salary_impact_factor DECIMAL(3,2),
    promotion_eligibility BOOLEAN DEFAULT False,
    color_code VARCHAR(7),
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT True,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_grade_code ON MST_SkillGrade (grade_code);
CREATE UNIQUE INDEX idx_grade_level ON MST_SkillGrade (grade_level);
CREATE INDEX idx_grade_name ON MST_SkillGrade (grade_name);
CREATE INDEX idx_mentoring ON MST_SkillGrade (mentoring_capability, is_active);
CREATE INDEX idx_promotion ON MST_SkillGrade (promotion_eligibility, is_active);
CREATE INDEX idx_sort_order ON MST_SkillGrade (sort_order);

-- 外部キー制約


-- MST_CertificationRequirement (資格要件マスタ) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_CertificationRequirement (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    requirement_id VARCHAR(50),
    requirement_name VARCHAR(200),
    requirement_description TEXT,
    requirement_type ENUM,
    target_job_type_id VARCHAR(50),
    target_position_id VARCHAR(50),
    target_skill_grade_id VARCHAR(50),
    target_department_id VARCHAR(50),
    certification_id VARCHAR(50),
    requirement_level ENUM,
    priority_order INTEGER DEFAULT 1,
    alternative_certifications TEXT,
    minimum_experience_years INTEGER,
    minimum_skill_level ENUM,
    grace_period_months INTEGER,
    renewal_required BOOLEAN DEFAULT False,
    renewal_interval_months INTEGER,
    exemption_conditions TEXT,
    assessment_criteria TEXT,
    business_justification TEXT,
    compliance_requirement BOOLEAN DEFAULT False,
    client_requirement BOOLEAN DEFAULT False,
    internal_policy BOOLEAN DEFAULT False,
    effective_start_date DATE,
    effective_end_date DATE,
    notification_timing INTEGER,
    escalation_timing INTEGER,
    cost_support_available BOOLEAN DEFAULT False,
    cost_support_amount DECIMAL(10,2),
    cost_support_conditions TEXT,
    training_support_available BOOLEAN DEFAULT False,
    recommended_training_programs TEXT,
    study_time_allocation DECIMAL(5,2),
    success_rate DECIMAL(5,2),
    average_study_hours DECIMAL(6,2),
    difficulty_rating ENUM,
    active_flag BOOLEAN DEFAULT True,
    created_by VARCHAR(50),
    approved_by VARCHAR(50),
    approval_date DATE,
    review_date DATE,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_requirement_id ON MST_CertificationRequirement (requirement_id);
CREATE INDEX idx_requirement_type ON MST_CertificationRequirement (requirement_type);
CREATE INDEX idx_target_job_type ON MST_CertificationRequirement (target_job_type_id);
CREATE INDEX idx_target_position ON MST_CertificationRequirement (target_position_id);
CREATE INDEX idx_target_skill_grade ON MST_CertificationRequirement (target_skill_grade_id);
CREATE INDEX idx_certification_id ON MST_CertificationRequirement (certification_id);
CREATE INDEX idx_requirement_level ON MST_CertificationRequirement (requirement_level);
CREATE INDEX idx_active_flag ON MST_CertificationRequirement (active_flag);
CREATE INDEX idx_effective_period ON MST_CertificationRequirement (effective_start_date, effective_end_date);
CREATE INDEX idx_compliance_requirement ON MST_CertificationRequirement (compliance_requirement);
CREATE INDEX idx_priority_order ON MST_CertificationRequirement (priority_order);

-- 外部キー制約
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_job_type FOREIGN KEY (target_job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_position FOREIGN KEY (target_position_id) REFERENCES MST_Position(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_skill_grade FOREIGN KEY (target_skill_grade_id) REFERENCES MST_SkillGrade(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_department FOREIGN KEY (target_department_id) REFERENCES MST_Department(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_certification FOREIGN KEY (certification_id) REFERENCES MST_Certification(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_created_by FOREIGN KEY (created_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_approved_by FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;


-- MST_EmployeeJobType (社員職種関連) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_EmployeeJobType (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    employee_job_type_id VARCHAR(50),
    employee_id VARCHAR(50),
    job_type_id VARCHAR(50),
    assignment_type ENUM,
    assignment_ratio DECIMAL(5,2) DEFAULT 100.0,
    effective_start_date DATE,
    effective_end_date DATE,
    assignment_reason ENUM,
    assignment_status ENUM DEFAULT 'ACTIVE',
    proficiency_level ENUM DEFAULT 'NOVICE',
    target_proficiency_level ENUM,
    target_achievement_date DATE,
    certification_requirements TEXT,
    skill_requirements TEXT,
    experience_requirements TEXT,
    development_plan TEXT,
    training_plan TEXT,
    mentor_id VARCHAR(50),
    supervisor_id VARCHAR(50),
    performance_rating ENUM,
    last_evaluation_date DATE,
    next_evaluation_date DATE,
    evaluation_frequency ENUM DEFAULT 'QUARTERLY',
    career_path TEXT,
    strengths TEXT,
    improvement_areas TEXT,
    achievements TEXT,
    goals TEXT,
    workload_percentage DECIMAL(5,2) DEFAULT 100.0,
    billable_flag BOOLEAN DEFAULT True,
    cost_center VARCHAR(20),
    budget_allocation DECIMAL(10,2),
    hourly_rate DECIMAL(8,2),
    overtime_eligible BOOLEAN DEFAULT True,
    remote_work_eligible BOOLEAN DEFAULT False,
    travel_required BOOLEAN DEFAULT False,
    security_clearance_required BOOLEAN DEFAULT False,
    created_by VARCHAR(50),
    approved_by VARCHAR(50),
    approval_date DATE,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_employee_job_type_id ON MST_EmployeeJobType (employee_job_type_id);
CREATE INDEX idx_employee_id ON MST_EmployeeJobType (employee_id);
CREATE INDEX idx_job_type_id ON MST_EmployeeJobType (job_type_id);
CREATE INDEX idx_employee_job_type ON MST_EmployeeJobType (employee_id, job_type_id);
CREATE INDEX idx_assignment_type ON MST_EmployeeJobType (assignment_type);
CREATE INDEX idx_assignment_status ON MST_EmployeeJobType (assignment_status);
CREATE INDEX idx_proficiency_level ON MST_EmployeeJobType (proficiency_level);
CREATE INDEX idx_effective_period ON MST_EmployeeJobType (effective_start_date, effective_end_date);
CREATE INDEX idx_mentor_id ON MST_EmployeeJobType (mentor_id);
CREATE INDEX idx_supervisor_id ON MST_EmployeeJobType (supervisor_id);
CREATE INDEX idx_performance_rating ON MST_EmployeeJobType (performance_rating);

-- 外部キー制約
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_job_type FOREIGN KEY (job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_mentor FOREIGN KEY (mentor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_supervisor FOREIGN KEY (supervisor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_created_by FOREIGN KEY (created_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_approved_by FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;


-- MST_JobTypeSkillGrade (職種スキルグレード関連) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_JobTypeSkillGrade (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    job_type_id VARCHAR(50),
    skill_grade_id VARCHAR(50),
    grade_requirement_type ENUM DEFAULT 'STANDARD',
    required_experience_years DECIMAL(4,1),
    promotion_criteria TEXT,
    salary_range_min DECIMAL(10,0),
    salary_range_max DECIMAL(10,0),
    performance_expectations TEXT,
    leadership_requirements TEXT,
    technical_depth INTEGER,
    business_impact INTEGER,
    team_size_expectation INTEGER,
    certification_requirements TEXT,
    grade_status ENUM DEFAULT 'ACTIVE',
    effective_date DATE,
    expiry_date DATE,
    next_grade_path TEXT,
    evaluation_frequency ENUM DEFAULT 'ANNUAL',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE INDEX idx_MST_JobTypeSkillGrade_job_type_id ON MST_JobTypeSkillGrade (job_type_id);
CREATE INDEX idx_MST_JobTypeSkillGrade_skill_grade_id ON MST_JobTypeSkillGrade (skill_grade_id);
CREATE UNIQUE INDEX idx_MST_JobTypeSkillGrade_job_grade ON MST_JobTypeSkillGrade (job_type_id, skill_grade_id);
CREATE INDEX idx_MST_JobTypeSkillGrade_requirement_type ON MST_JobTypeSkillGrade (grade_requirement_type);
CREATE INDEX idx_MST_JobTypeSkillGrade_experience_years ON MST_JobTypeSkillGrade (required_experience_years);
CREATE INDEX idx_MST_JobTypeSkillGrade_status ON MST_JobTypeSkillGrade (grade_status);
CREATE INDEX idx_MST_JobTypeSkillGrade_effective_date ON MST_JobTypeSkillGrade (effective_date);
CREATE INDEX idx_MST_JobTypeSkillGrade_technical_depth ON MST_JobTypeSkillGrade (technical_depth);

-- 外部キー制約
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT fk_MST_JobTypeSkillGrade_job_type FOREIGN KEY (job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT fk_MST_JobTypeSkillGrade_skill_grade FOREIGN KEY (skill_grade_id) REFERENCES MST_SkillGrade(id) ON UPDATE CASCADE ON DELETE CASCADE;


-- MST_SkillGradeRequirement (スキルグレード要件) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_SkillGradeRequirement (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    skill_grade_id VARCHAR(50),
    requirement_category ENUM,
    requirement_name VARCHAR(200),
    requirement_description TEXT,
    evaluation_criteria TEXT,
    proficiency_level INTEGER,
    weight_percentage DECIMAL(5,2),
    minimum_score DECIMAL(5,2),
    evidence_requirements TEXT,
    learning_resources TEXT,
    prerequisite_requirements TEXT,
    assessment_method ENUM,
    assessment_frequency ENUM DEFAULT 'ANNUAL',
    validity_period INTEGER,
    certification_mapping TEXT,
    requirement_status ENUM DEFAULT 'ACTIVE',
    effective_date DATE,
    expiry_date DATE,
    revision_notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE INDEX idx_MST_SkillGradeRequirement_skill_grade_id ON MST_SkillGradeRequirement (skill_grade_id);
CREATE INDEX idx_MST_SkillGradeRequirement_category ON MST_SkillGradeRequirement (requirement_category);
CREATE INDEX idx_MST_SkillGradeRequirement_grade_category ON MST_SkillGradeRequirement (skill_grade_id, requirement_category);
CREATE INDEX idx_MST_SkillGradeRequirement_proficiency_level ON MST_SkillGradeRequirement (proficiency_level);
CREATE INDEX idx_MST_SkillGradeRequirement_assessment_method ON MST_SkillGradeRequirement (assessment_method);
CREATE INDEX idx_MST_SkillGradeRequirement_status ON MST_SkillGradeRequirement (requirement_status);
CREATE INDEX idx_MST_SkillGradeRequirement_effective_date ON MST_SkillGradeRequirement (effective_date);
CREATE INDEX idx_MST_SkillGradeRequirement_weight ON MST_SkillGradeRequirement (weight_percentage);

-- 外部キー制約
ALTER TABLE MST_SkillGradeRequirement ADD CONSTRAINT fk_MST_SkillGradeRequirement_skill_grade FOREIGN KEY (skill_grade_id) REFERENCES MST_SkillGrade(id) ON UPDATE CASCADE ON DELETE CASCADE;


-- MST_JobTypeSkill (職種スキル関連) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_JobTypeSkill (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    job_type_id VARCHAR(50),
    skill_item_id VARCHAR(50),
    required_level INTEGER,
    skill_priority ENUM DEFAULT 'MEDIUM',
    skill_category ENUM,
    experience_years DECIMAL(4,1),
    certification_required BOOLEAN DEFAULT False,
    skill_weight DECIMAL(5,2),
    evaluation_criteria TEXT,
    learning_path TEXT,
    skill_status ENUM DEFAULT 'ACTIVE',
    effective_date DATE,
    expiry_date DATE,
    alternative_skills TEXT,
    prerequisite_skills TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE INDEX idx_MST_JobTypeSkill_job_type_id ON MST_JobTypeSkill (job_type_id);
CREATE INDEX idx_MST_JobTypeSkill_skill_item_id ON MST_JobTypeSkill (skill_item_id);
CREATE UNIQUE INDEX idx_MST_JobTypeSkill_job_skill ON MST_JobTypeSkill (job_type_id, skill_item_id);
CREATE INDEX idx_MST_JobTypeSkill_required_level ON MST_JobTypeSkill (required_level);
CREATE INDEX idx_MST_JobTypeSkill_priority ON MST_JobTypeSkill (skill_priority);
CREATE INDEX idx_MST_JobTypeSkill_category ON MST_JobTypeSkill (skill_category);
CREATE INDEX idx_MST_JobTypeSkill_status ON MST_JobTypeSkill (skill_status);
CREATE INDEX idx_MST_JobTypeSkill_effective_date ON MST_JobTypeSkill (effective_date);

-- 外部キー制約
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT fk_MST_JobTypeSkill_job_type FOREIGN KEY (job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT fk_MST_JobTypeSkill_skill_item FOREIGN KEY (skill_item_id) REFERENCES MST_SkillItem(id) ON UPDATE CASCADE ON DELETE CASCADE;


-- MST_EmployeeDepartment (社員部署関連) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_EmployeeDepartment (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    employee_id VARCHAR(50),
    department_id VARCHAR(50),
    assignment_type ENUM DEFAULT 'PRIMARY',
    start_date DATE,
    end_date DATE,
    assignment_ratio DECIMAL(5,2),
    role_in_department VARCHAR(100),
    reporting_manager_id VARCHAR(50),
    assignment_reason VARCHAR(500),
    assignment_status ENUM DEFAULT 'ACTIVE',
    approval_status ENUM DEFAULT 'PENDING',
    approved_by VARCHAR(50),
    approved_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE INDEX idx_MST_EmployeeDepartment_employee_id ON MST_EmployeeDepartment (employee_id);
CREATE INDEX idx_MST_EmployeeDepartment_department_id ON MST_EmployeeDepartment (department_id);
CREATE INDEX idx_MST_EmployeeDepartment_employee_department ON MST_EmployeeDepartment (employee_id, department_id);
CREATE INDEX idx_MST_EmployeeDepartment_assignment_type ON MST_EmployeeDepartment (assignment_type);
CREATE INDEX idx_MST_EmployeeDepartment_start_date ON MST_EmployeeDepartment (start_date);
CREATE INDEX idx_MST_EmployeeDepartment_end_date ON MST_EmployeeDepartment (end_date);
CREATE INDEX idx_MST_EmployeeDepartment_status ON MST_EmployeeDepartment (assignment_status);

-- 外部キー制約
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT fk_MST_EmployeeDepartment_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT fk_MST_EmployeeDepartment_department FOREIGN KEY (department_id) REFERENCES MST_Department(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT fk_MST_EmployeeDepartment_reporting_manager FOREIGN KEY (reporting_manager_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT fk_MST_EmployeeDepartment_approved_by FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;


-- MST_EmployeePosition (社員役職関連) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_EmployeePosition (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    employee_id VARCHAR(50),
    position_id VARCHAR(50),
    appointment_type ENUM DEFAULT 'PRIMARY',
    start_date DATE,
    end_date DATE,
    appointment_reason VARCHAR(500),
    responsibility_scope VARCHAR(500),
    authority_level INTEGER,
    salary_grade VARCHAR(20),
    appointment_status ENUM DEFAULT 'ACTIVE',
    approval_status ENUM DEFAULT 'PENDING',
    approved_by VARCHAR(50),
    approved_at TIMESTAMP,
    performance_target TEXT,
    delegation_authority TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE INDEX idx_MST_EmployeePosition_employee_id ON MST_EmployeePosition (employee_id);
CREATE INDEX idx_MST_EmployeePosition_position_id ON MST_EmployeePosition (position_id);
CREATE INDEX idx_MST_EmployeePosition_employee_position ON MST_EmployeePosition (employee_id, position_id);
CREATE INDEX idx_MST_EmployeePosition_appointment_type ON MST_EmployeePosition (appointment_type);
CREATE INDEX idx_MST_EmployeePosition_start_date ON MST_EmployeePosition (start_date);
CREATE INDEX idx_MST_EmployeePosition_end_date ON MST_EmployeePosition (end_date);
CREATE INDEX idx_MST_EmployeePosition_status ON MST_EmployeePosition (appointment_status);
CREATE INDEX idx_MST_EmployeePosition_authority_level ON MST_EmployeePosition (authority_level);

-- 外部キー制約
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT fk_MST_EmployeePosition_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT fk_MST_EmployeePosition_position FOREIGN KEY (position_id) REFERENCES MST_Position(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT fk_MST_EmployeePosition_approved_by FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;


-- MST_SkillItem (スキル項目マスタ) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_SkillItem (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    skill_code VARCHAR(20),
    skill_name VARCHAR(100),
    skill_category_id VARCHAR(50),
    skill_type ENUM,
    difficulty_level INT,
    importance_level INT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_skill_code ON MST_SkillItem (skill_code);
CREATE INDEX idx_skill_category ON MST_SkillItem (skill_category_id);


-- MST_TrainingProgram (研修プログラム) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE MST_TrainingProgram (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    training_program_id VARCHAR(50),
    program_code VARCHAR(20),
    program_name VARCHAR(200),
    program_name_en VARCHAR(200),
    program_description TEXT,
    program_category ENUM,
    program_type ENUM,
    target_audience ENUM,
    difficulty_level ENUM,
    duration_hours DECIMAL(5,2),
    duration_days INTEGER,
    max_participants INTEGER,
    min_participants INTEGER,
    prerequisites TEXT,
    learning_objectives TEXT,
    curriculum_outline TEXT,
    curriculum_details TEXT,
    materials_required TEXT,
    equipment_required TEXT,
    instructor_requirements TEXT,
    assessment_method ENUM,
    passing_score DECIMAL(5,2),
    certification_provided BOOLEAN DEFAULT False,
    pdu_credits DECIMAL(5,2),
    related_skills TEXT,
    related_certifications TEXT,
    cost_per_participant DECIMAL(10,2),
    external_provider VARCHAR(200),
    external_url VARCHAR(500),
    venue_type ENUM,
    venue_requirements TEXT,
    language ENUM DEFAULT 'JA',
    repeat_interval INTEGER,
    mandatory_flag BOOLEAN DEFAULT False,
    active_flag BOOLEAN DEFAULT True,
    effective_start_date DATE,
    effective_end_date DATE,
    created_by VARCHAR(50),
    approved_by VARCHAR(50),
    approval_date DATE,
    version_number VARCHAR(10) DEFAULT '1.0',
    revision_notes TEXT,
    tags TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_training_program_id ON MST_TrainingProgram (training_program_id);
CREATE UNIQUE INDEX idx_program_code ON MST_TrainingProgram (program_code);
CREATE INDEX idx_program_category ON MST_TrainingProgram (program_category);
CREATE INDEX idx_program_type ON MST_TrainingProgram (program_type);
CREATE INDEX idx_target_audience ON MST_TrainingProgram (target_audience);
CREATE INDEX idx_difficulty_level ON MST_TrainingProgram (difficulty_level);
CREATE INDEX idx_active_flag ON MST_TrainingProgram (active_flag);
CREATE INDEX idx_mandatory_flag ON MST_TrainingProgram (mandatory_flag);
CREATE INDEX idx_effective_period ON MST_TrainingProgram (effective_start_date, effective_end_date);
CREATE INDEX idx_external_provider ON MST_TrainingProgram (external_provider);
CREATE INDEX idx_language ON MST_TrainingProgram (language);

-- 外部キー制約
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT fk_training_program_created_by FOREIGN KEY (created_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT fk_training_program_approved_by FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;


-- TRN_SkillRecord (スキル情報) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE TRN_SkillRecord (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    employee_id VARCHAR(50),
    skill_item_id VARCHAR(50),
    skill_level INT,
    self_assessment INT,
    manager_assessment INT,
    evidence_description TEXT,
    acquisition_date DATE,
    last_used_date DATE,
    expiry_date DATE,
    certification_id VARCHAR(50),
    skill_category_id VARCHAR(50),
    assessment_date DATE,
    assessor_id VARCHAR(50),
    skill_status ENUM DEFAULT 'ACTIVE',
    learning_hours INT,
    project_experience_count INT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_employee_skill ON TRN_SkillRecord (employee_id, skill_item_id);
CREATE INDEX idx_employee ON TRN_SkillRecord (employee_id);
CREATE INDEX idx_skill_item ON TRN_SkillRecord (skill_item_id);
CREATE INDEX idx_skill_level ON TRN_SkillRecord (skill_level);
CREATE INDEX idx_skill_category ON TRN_SkillRecord (skill_category_id);
CREATE INDEX idx_certification ON TRN_SkillRecord (certification_id);
CREATE INDEX idx_status ON TRN_SkillRecord (skill_status);
CREATE INDEX idx_expiry_date ON TRN_SkillRecord (expiry_date);
CREATE INDEX idx_assessment_date ON TRN_SkillRecord (assessment_date);

-- 外部キー制約
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_item FOREIGN KEY (skill_item_id) REFERENCES MST_SkillItem(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_certification FOREIGN KEY (certification_id) REFERENCES MST_Certification(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_category FOREIGN KEY (skill_category_id) REFERENCES MST_SkillCategory(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_assessor FOREIGN KEY (assessor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;


-- TRN_GoalProgress (目標進捗) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE TRN_GoalProgress (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    goal_id VARCHAR(50),
    employee_id VARCHAR(50),
    goal_title VARCHAR(200),
    goal_description TEXT,
    goal_category ENUM,
    goal_type ENUM,
    priority_level ENUM DEFAULT 'MEDIUM',
    target_value DECIMAL(15,2),
    current_value DECIMAL(15,2),
    unit VARCHAR(50),
    start_date DATE,
    target_date DATE,
    progress_rate DECIMAL(5,2) DEFAULT 0.0,
    achievement_status ENUM DEFAULT 'NOT_STARTED',
    supervisor_id VARCHAR(50),
    approval_status ENUM DEFAULT 'DRAFT',
    approved_at TIMESTAMP,
    approved_by VARCHAR(50),
    completion_date DATE,
    achievement_rate DECIMAL(5,2),
    self_evaluation INTEGER,
    supervisor_evaluation INTEGER,
    evaluation_comments TEXT,
    related_career_plan_id VARCHAR(50),
    related_skill_items TEXT,
    milestones TEXT,
    obstacles TEXT,
    support_needed TEXT,
    last_updated_at TIMESTAMP,
    next_review_date DATE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_TRN_GoalProgress_goal_id ON TRN_GoalProgress (goal_id);
CREATE INDEX idx_TRN_GoalProgress_employee_id ON TRN_GoalProgress (employee_id);
CREATE INDEX idx_TRN_GoalProgress_supervisor_id ON TRN_GoalProgress (supervisor_id);
CREATE INDEX idx_TRN_GoalProgress_category ON TRN_GoalProgress (goal_category);
CREATE INDEX idx_TRN_GoalProgress_status ON TRN_GoalProgress (achievement_status);
CREATE INDEX idx_TRN_GoalProgress_approval_status ON TRN_GoalProgress (approval_status);
CREATE INDEX idx_TRN_GoalProgress_target_date ON TRN_GoalProgress (target_date);
CREATE INDEX idx_TRN_GoalProgress_priority ON TRN_GoalProgress (priority_level);
CREATE INDEX idx_TRN_GoalProgress_employee_period ON TRN_GoalProgress (employee_id, start_date, target_date);
CREATE INDEX idx_TRN_GoalProgress_next_review ON TRN_GoalProgress (next_review_date);

-- 外部キー制約
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_supervisor FOREIGN KEY (supervisor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_approved_by FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_career_plan FOREIGN KEY (related_career_plan_id) REFERENCES MST_CareerPlan(id) ON UPDATE CASCADE ON DELETE SET NULL;


-- TRN_ProjectRecord (案件実績) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE TRN_ProjectRecord (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    project_record_id VARCHAR(50),
    employee_id VARCHAR(50),
    project_name VARCHAR(200),
    project_code VARCHAR(50),
    client_name VARCHAR(100),
    project_type ENUM,
    project_scale ENUM,
    start_date DATE,
    end_date DATE,
    participation_rate DECIMAL(5,2),
    role_title VARCHAR(100),
    responsibilities TEXT,
    technologies_used TEXT,
    skills_applied TEXT,
    achievements TEXT,
    challenges_faced TEXT,
    lessons_learned TEXT,
    team_size INTEGER,
    budget_range ENUM,
    project_status ENUM DEFAULT 'ONGOING',
    evaluation_score DECIMAL(3,1),
    evaluation_comment TEXT,
    is_confidential BOOLEAN DEFAULT False,
    is_public_reference BOOLEAN DEFAULT False,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_project_record_id ON TRN_ProjectRecord (project_record_id);
CREATE INDEX idx_employee_id ON TRN_ProjectRecord (employee_id);
CREATE INDEX idx_project_name ON TRN_ProjectRecord (project_name);
CREATE INDEX idx_project_code ON TRN_ProjectRecord (project_code);
CREATE INDEX idx_project_type ON TRN_ProjectRecord (project_type);
CREATE INDEX idx_date_range ON TRN_ProjectRecord (start_date, end_date);
CREATE INDEX idx_project_status ON TRN_ProjectRecord (project_status);
CREATE INDEX idx_employee_period ON TRN_ProjectRecord (employee_id, start_date, end_date);

-- 外部キー制約
ALTER TABLE TRN_ProjectRecord ADD CONSTRAINT fk_project_record_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;


-- TRN_TrainingHistory (研修参加履歴) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE TRN_TrainingHistory (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    training_history_id VARCHAR(50),
    employee_id VARCHAR(50),
    training_program_id VARCHAR(50),
    training_name VARCHAR(200),
    training_type ENUM,
    training_category ENUM,
    provider_name VARCHAR(100),
    instructor_name VARCHAR(100),
    start_date DATE,
    end_date DATE,
    duration_hours DECIMAL(5,1),
    location VARCHAR(200),
    cost DECIMAL(10,2),
    cost_covered_by ENUM,
    attendance_status ENUM DEFAULT 'COMPLETED',
    completion_rate DECIMAL(5,2),
    test_score DECIMAL(5,2),
    grade VARCHAR(10),
    certificate_obtained BOOLEAN DEFAULT False,
    certificate_number VARCHAR(100),
    pdu_earned DECIMAL(5,1),
    skills_acquired TEXT,
    learning_objectives TEXT,
    learning_outcomes TEXT,
    feedback TEXT,
    satisfaction_score DECIMAL(3,1),
    recommendation_score DECIMAL(3,1),
    follow_up_required BOOLEAN DEFAULT False,
    follow_up_date DATE,
    manager_approval BOOLEAN DEFAULT False,
    approved_by VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_training_history_id ON TRN_TrainingHistory (training_history_id);
CREATE INDEX idx_employee_id ON TRN_TrainingHistory (employee_id);
CREATE INDEX idx_training_program_id ON TRN_TrainingHistory (training_program_id);
CREATE INDEX idx_training_type ON TRN_TrainingHistory (training_type);
CREATE INDEX idx_training_category ON TRN_TrainingHistory (training_category);
CREATE INDEX idx_date_range ON TRN_TrainingHistory (start_date, end_date);
CREATE INDEX idx_attendance_status ON TRN_TrainingHistory (attendance_status);
CREATE INDEX idx_employee_period ON TRN_TrainingHistory (employee_id, start_date, end_date);
CREATE INDEX idx_certificate ON TRN_TrainingHistory (certificate_obtained, certificate_number);

-- 外部キー制約
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT fk_training_history_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT fk_training_history_program FOREIGN KEY (training_program_id) REFERENCES MST_TrainingProgram(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT fk_training_history_approver FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;


-- TRN_PDU (継続教育ポイント) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE TRN_PDU (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    pdu_id VARCHAR(50),
    employee_id VARCHAR(50),
    certification_id VARCHAR(50),
    activity_type ENUM,
    activity_name VARCHAR(200),
    activity_description TEXT,
    provider_name VARCHAR(100),
    activity_date DATE,
    start_time TIME,
    end_time TIME,
    duration_hours DECIMAL(5,1),
    pdu_points DECIMAL(5,1),
    pdu_category ENUM,
    pdu_subcategory VARCHAR(50),
    location VARCHAR(200),
    cost DECIMAL(10,2),
    cost_covered_by ENUM,
    evidence_type ENUM,
    evidence_file_path VARCHAR(500),
    certificate_number VARCHAR(100),
    instructor_name VARCHAR(100),
    learning_objectives TEXT,
    learning_outcomes TEXT,
    skills_developed TEXT,
    approval_status ENUM DEFAULT 'PENDING',
    approved_by VARCHAR(50),
    approval_date DATE,
    approval_comment TEXT,
    expiry_date DATE,
    is_recurring BOOLEAN DEFAULT False,
    recurrence_pattern VARCHAR(50),
    related_training_id VARCHAR(50),
    related_project_id VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_pdu_id ON TRN_PDU (pdu_id);
CREATE INDEX idx_employee_id ON TRN_PDU (employee_id);
CREATE INDEX idx_certification_id ON TRN_PDU (certification_id);
CREATE INDEX idx_activity_type ON TRN_PDU (activity_type);
CREATE INDEX idx_activity_date ON TRN_PDU (activity_date);
CREATE INDEX idx_pdu_category ON TRN_PDU (pdu_category);
CREATE INDEX idx_approval_status ON TRN_PDU (approval_status);
CREATE INDEX idx_employee_period ON TRN_PDU (employee_id, activity_date);
CREATE INDEX idx_expiry_date ON TRN_PDU (expiry_date);
CREATE INDEX idx_certification_employee ON TRN_PDU (certification_id, employee_id, approval_status);

-- 外部キー制約
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_certification FOREIGN KEY (certification_id) REFERENCES MST_Certification(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_approver FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_training FOREIGN KEY (related_training_id) REFERENCES TRN_TrainingHistory(training_history_id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_project FOREIGN KEY (related_project_id) REFERENCES TRN_ProjectRecord(project_record_id) ON UPDATE CASCADE ON DELETE SET NULL;


-- TRN_SkillEvidence (スキル証跡) DDL
-- 生成日時: 2025-06-01 19:42:43

CREATE TABLE TRN_SkillEvidence (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    evidence_id VARCHAR(50),
    employee_id VARCHAR(50),
    skill_id VARCHAR(50),
    evidence_type ENUM,
    evidence_title VARCHAR(200),
    evidence_description TEXT,
    skill_level_demonstrated ENUM,
    evidence_date DATE,
    validity_start_date DATE,
    validity_end_date DATE,
    file_path VARCHAR(500),
    file_type ENUM,
    file_size_kb INTEGER,
    external_url VARCHAR(500),
    issuer_name VARCHAR(100),
    issuer_type ENUM,
    certificate_number VARCHAR(100),
    verification_method ENUM,
    verification_status ENUM DEFAULT 'PENDING',
    verified_by VARCHAR(50),
    verification_date DATE,
    verification_comment TEXT,
    related_project_id VARCHAR(50),
    related_training_id VARCHAR(50),
    related_certification_id VARCHAR(50),
    impact_score DECIMAL(3,1),
    complexity_level ENUM,
    team_size INTEGER,
    role_in_activity VARCHAR(100),
    technologies_used TEXT,
    achievements TEXT,
    lessons_learned TEXT,
    is_public BOOLEAN DEFAULT False,
    is_portfolio_item BOOLEAN DEFAULT False,
    tags TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_evidence_id ON TRN_SkillEvidence (evidence_id);
CREATE INDEX idx_employee_id ON TRN_SkillEvidence (employee_id);
CREATE INDEX idx_skill_id ON TRN_SkillEvidence (skill_id);
CREATE INDEX idx_evidence_type ON TRN_SkillEvidence (evidence_type);
CREATE INDEX idx_skill_level ON TRN_SkillEvidence (skill_level_demonstrated);
CREATE INDEX idx_evidence_date ON TRN_SkillEvidence (evidence_date);
CREATE INDEX idx_verification_status ON TRN_SkillEvidence (verification_status);
CREATE INDEX idx_validity_period ON TRN_SkillEvidence (validity_start_date, validity_end_date);
CREATE INDEX idx_employee_skill ON TRN_SkillEvidence (employee_id, skill_id, verification_status);
CREATE INDEX idx_portfolio ON TRN_SkillEvidence (is_portfolio_item, is_public);

-- 外部キー制約
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_skill FOREIGN KEY (skill_id) REFERENCES MST_SkillItem(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_verifier FOREIGN KEY (verified_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_project FOREIGN KEY (related_project_id) REFERENCES TRN_ProjectRecord(project_record_id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_training FOREIGN KEY (related_training_id) REFERENCES TRN_TrainingHistory(training_history_id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_certification FOREIGN KEY (related_certification_id) REFERENCES MST_Certification(id) ON UPDATE CASCADE ON DELETE SET NULL;


-- TRN_Notification (通知履歴) DDL
-- 生成日時: 2025-06-01 19:42:44

CREATE TABLE TRN_Notification (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    notification_id VARCHAR(50),
    recipient_id VARCHAR(50),
    sender_id VARCHAR(50),
    notification_type ENUM,
    notification_category ENUM,
    priority_level ENUM DEFAULT 'NORMAL',
    title VARCHAR(200),
    message TEXT,
    message_format ENUM DEFAULT 'PLAIN',
    action_url VARCHAR(500),
    action_label VARCHAR(50),
    delivery_method ENUM,
    delivery_status ENUM DEFAULT 'PENDING',
    sent_at TIMESTAMP,
    delivered_at TIMESTAMP,
    read_status ENUM DEFAULT 'UNREAD',
    read_at TIMESTAMP,
    archived_at TIMESTAMP,
    expiry_date DATE,
    retry_count INTEGER DEFAULT 0,
    max_retry_count INTEGER DEFAULT 3,
    last_retry_at TIMESTAMP,
    error_message TEXT,
    external_message_id VARCHAR(100),
    template_id VARCHAR(50),
    template_variables TEXT,
    related_entity_type ENUM,
    related_entity_id VARCHAR(50),
    batch_id VARCHAR(50),
    user_agent VARCHAR(500),
    ip_address VARCHAR(45),
    device_type ENUM,
    is_bulk_notification BOOLEAN DEFAULT False,
    personalization_data TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_notification_id ON TRN_Notification (notification_id);
CREATE INDEX idx_recipient_id ON TRN_Notification (recipient_id);
CREATE INDEX idx_sender_id ON TRN_Notification (sender_id);
CREATE INDEX idx_notification_type ON TRN_Notification (notification_type);
CREATE INDEX idx_notification_category ON TRN_Notification (notification_category);
CREATE INDEX idx_priority_level ON TRN_Notification (priority_level);
CREATE INDEX idx_delivery_method ON TRN_Notification (delivery_method);
CREATE INDEX idx_delivery_status ON TRN_Notification (delivery_status);
CREATE INDEX idx_read_status ON TRN_Notification (read_status);
CREATE INDEX idx_sent_at ON TRN_Notification (sent_at);
CREATE INDEX idx_recipient_unread ON TRN_Notification (recipient_id, read_status, expiry_date);
CREATE INDEX idx_batch_id ON TRN_Notification (batch_id);
CREATE INDEX idx_related_entity ON TRN_Notification (related_entity_type, related_entity_id);

-- 外部キー制約
ALTER TABLE TRN_Notification ADD CONSTRAINT fk_notification_recipient FOREIGN KEY (recipient_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_Notification ADD CONSTRAINT fk_notification_sender FOREIGN KEY (sender_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;


-- SYS_SkillIndex (スキル検索インデックス) DDL
-- 生成日時: 2025-06-01 19:42:44

CREATE TABLE SYS_SkillIndex (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    id VARCHAR(50),
    tenant_id VARCHAR(50),
    skill_id VARCHAR(50),
    index_type ENUM,
    search_term VARCHAR(200),
    normalized_term VARCHAR(200),
    relevance_score DECIMAL(5,3) DEFAULT 1.0,
    frequency_weight DECIMAL(5,3) DEFAULT 1.0,
    position_weight DECIMAL(5,3) DEFAULT 1.0,
    language_code VARCHAR(10) DEFAULT 'ja',
    source_field ENUM,
    is_active BOOLEAN DEFAULT True,
    search_count INTEGER DEFAULT 0,
    last_searched_at TIMESTAMP,
    index_updated_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE INDEX idx_skill_index_skill ON SYS_SkillIndex (skill_id);
CREATE INDEX idx_skill_index_search_term ON SYS_SkillIndex (normalized_term, language_code);
CREATE INDEX idx_skill_index_type ON SYS_SkillIndex (index_type);
CREATE INDEX idx_skill_index_tenant_term ON SYS_SkillIndex (tenant_id, normalized_term);
CREATE INDEX idx_skill_index_relevance ON SYS_SkillIndex (relevance_score);
CREATE INDEX idx_skill_index_active ON SYS_SkillIndex (is_active);
CREATE INDEX idx_skill_index_search_stats ON SYS_SkillIndex (search_count, last_searched_at);

-- 外部キー制約
ALTER TABLE SYS_SkillIndex ADD CONSTRAINT fk_skill_index_skill FOREIGN KEY (skill_id) REFERENCES MST_Skill(id) ON UPDATE CASCADE ON DELETE CASCADE;


-- SYS_SkillMatrix (スキルマップ) DDL
-- 生成日時: 2025-06-01 19:42:44

CREATE TABLE SYS_SkillMatrix (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- SYS_BackupHistory (バックアップ履歴) DDL
-- 生成日時: 2025-06-01 19:42:44

CREATE TABLE SYS_BackupHistory (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- SYS_SystemLog (システムログ) DDL
-- 生成日時: 2025-06-01 19:42:44

CREATE TABLE SYS_SystemLog (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    log_level ENUM,
    log_category VARCHAR(50),
    message TEXT,
    user_id VARCHAR(50),
    session_id VARCHAR(100),
    ip_address VARCHAR(45),
    user_agent TEXT,
    request_url TEXT,
    request_method VARCHAR(10),
    response_status INT,
    response_time INT,
    error_code VARCHAR(20),
    stack_trace TEXT,
    request_body TEXT,
    response_body TEXT,
    correlation_id VARCHAR(100),
    component_name VARCHAR(100),
    thread_name VARCHAR(100),
    server_name VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE INDEX idx_log_level ON SYS_SystemLog (log_level);
CREATE INDEX idx_log_category ON SYS_SystemLog (log_category);
CREATE INDEX idx_user_id ON SYS_SystemLog (user_id);
CREATE INDEX idx_session_id ON SYS_SystemLog (session_id);
CREATE INDEX idx_ip_address ON SYS_SystemLog (ip_address);
CREATE INDEX idx_error_code ON SYS_SystemLog (error_code);
CREATE INDEX idx_correlation_id ON SYS_SystemLog (correlation_id);
CREATE INDEX idx_component ON SYS_SystemLog (component_name);
CREATE INDEX idx_server ON SYS_SystemLog (server_name);
CREATE INDEX idx_response_time ON SYS_SystemLog (response_time);
CREATE INDEX idx_created_at_level ON SYS_SystemLog (created_at, log_level);

-- 外部キー制約
ALTER TABLE SYS_SystemLog ADD CONSTRAINT fk_log_user FOREIGN KEY (user_id) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE SET NULL;


-- SYS_TokenStore (トークン管理) DDL
-- 生成日時: 2025-06-01 19:42:44

CREATE TABLE SYS_TokenStore (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    id VARCHAR(50),
    tenant_id VARCHAR(50),
    user_id VARCHAR(50),
    token_type ENUM,
    token_value TEXT,
    token_hash VARCHAR(255),
    expires_at TIMESTAMP,
    issued_at TIMESTAMP,
    last_used_at TIMESTAMP,
    client_ip VARCHAR(45),
    user_agent TEXT,
    device_fingerprint VARCHAR(255),
    scope TEXT,
    is_revoked BOOLEAN DEFAULT False,
    revoked_at TIMESTAMP,
    revoked_reason ENUM,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_token_store_hash ON SYS_TokenStore (token_hash);
CREATE INDEX idx_token_store_user_type ON SYS_TokenStore (user_id, token_type);
CREATE INDEX idx_token_store_expires ON SYS_TokenStore (expires_at, is_revoked);
CREATE INDEX idx_token_store_tenant_user ON SYS_TokenStore (tenant_id, user_id);
CREATE INDEX idx_token_store_issued ON SYS_TokenStore (issued_at);
CREATE INDEX idx_token_store_last_used ON SYS_TokenStore (last_used_at);

-- 外部キー制約
ALTER TABLE SYS_TokenStore ADD CONSTRAINT fk_token_store_user FOREIGN KEY (user_id) REFERENCES MST_UserAuth(id) ON UPDATE CASCADE ON DELETE CASCADE;


-- SYS_MasterData (マスタデータ全般) DDL
-- 生成日時: 2025-06-01 19:42:44

CREATE TABLE SYS_MasterData (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- SYS_TenantUsage (テナント使用量) DDL
-- 生成日時: 2025-06-01 19:42:44

CREATE TABLE SYS_TenantUsage (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- SYS_IntegrationConfig (外部連携設定) DDL
-- 生成日時: 2025-06-01 19:42:44

CREATE TABLE SYS_IntegrationConfig (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    id VARCHAR(50),
    tenant_id VARCHAR(50),
    integration_key VARCHAR(100),
    integration_name VARCHAR(200),
    integration_type ENUM,
    endpoint_url VARCHAR(500),
    auth_type ENUM,
    auth_config TEXT,
    connection_config TEXT,
    request_headers TEXT,
    timeout_seconds INTEGER DEFAULT 30,
    retry_count INTEGER DEFAULT 3,
    retry_interval INTEGER DEFAULT 5,
    rate_limit_per_minute INTEGER,
    is_enabled BOOLEAN DEFAULT True,
    health_check_url VARCHAR(500),
    last_health_check TIMESTAMP,
    health_status ENUM,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_integration_config_tenant_key ON SYS_IntegrationConfig (tenant_id, integration_key);
CREATE INDEX idx_integration_config_type ON SYS_IntegrationConfig (integration_type);
CREATE INDEX idx_integration_config_enabled ON SYS_IntegrationConfig (is_enabled);
CREATE INDEX idx_integration_config_health ON SYS_IntegrationConfig (health_status, last_health_check);
CREATE INDEX idx_integration_config_auth_type ON SYS_IntegrationConfig (auth_type);

-- 外部キー制約


-- HIS_AuditLog (監査ログ) DDL
-- 生成日時: 2025-06-01 19:42:44

CREATE TABLE HIS_AuditLog (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    id VARCHAR(50),
    user_id VARCHAR(50),
    session_id VARCHAR(100),
    action_type ENUM,
    target_table VARCHAR(100),
    target_id VARCHAR(50),
    old_values TEXT,
    new_values TEXT,
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    result_status ENUM DEFAULT 'SUCCESS',
    error_message TEXT,
    execution_time_ms INTEGER,
    is_deleted BOOLEAN DEFAULT False,
    tenant_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT 'CURRENT_TIMESTAMP',
    updated_at TIMESTAMP DEFAULT 'CURRENT_TIMESTAMP',
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_his_auditlog_id ON HIS_AuditLog (id);
CREATE INDEX idx_his_auditlog_user_id ON HIS_AuditLog (user_id);
CREATE INDEX idx_his_auditlog_tenant_id ON HIS_AuditLog (tenant_id);
CREATE INDEX idx_his_auditlog_action_type ON HIS_AuditLog (action_type);
CREATE INDEX idx_his_auditlog_target_table ON HIS_AuditLog (target_table);
CREATE INDEX idx_his_auditlog_created_at ON HIS_AuditLog (created_at);
CREATE INDEX idx_his_auditlog_user_created ON HIS_AuditLog (user_id, created_at);
CREATE INDEX idx_his_auditlog_tenant_created ON HIS_AuditLog (tenant_id, created_at);

-- 外部キー制約
ALTER TABLE HIS_AuditLog ADD CONSTRAINT fk_his_auditlog_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE HIS_AuditLog ADD CONSTRAINT fk_his_auditlog_user FOREIGN KEY (user_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;


-- HIS_NotificationLog (通知送信履歴) DDL
-- 生成日時: 2025-06-01 19:42:44

CREATE TABLE HIS_NotificationLog (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    id VARCHAR(50),
    tenant_id VARCHAR(50),
    notification_id VARCHAR(50),
    setting_id VARCHAR(50),
    template_id VARCHAR(50),
    notification_type ENUM,
    recipient_type ENUM,
    recipient_address VARCHAR(500),
    subject VARCHAR(500),
    message_body TEXT,
    message_format ENUM,
    send_status ENUM,
    send_attempts INTEGER DEFAULT 0,
    max_retry_count INTEGER DEFAULT 3,
    scheduled_at TIMESTAMP,
    sent_at TIMESTAMP,
    delivered_at TIMESTAMP,
    opened_at TIMESTAMP,
    response_code VARCHAR(20),
    response_message TEXT,
    error_details TEXT,
    integration_config_id VARCHAR(50),
    priority_level ENUM DEFAULT 'MEDIUM',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE INDEX idx_notification_log_notification ON HIS_NotificationLog (notification_id);
CREATE INDEX idx_notification_log_tenant_status ON HIS_NotificationLog (tenant_id, send_status);
CREATE INDEX idx_notification_log_type ON HIS_NotificationLog (notification_type);
CREATE INDEX idx_notification_log_scheduled ON HIS_NotificationLog (scheduled_at);
CREATE INDEX idx_notification_log_sent ON HIS_NotificationLog (sent_at);
CREATE INDEX idx_notification_log_status_attempts ON HIS_NotificationLog (send_status, send_attempts);
CREATE INDEX idx_notification_log_priority ON HIS_NotificationLog (priority_level, scheduled_at);

-- 外部キー制約
ALTER TABLE HIS_NotificationLog ADD CONSTRAINT fk_notification_log_notification FOREIGN KEY (notification_id) REFERENCES TRN_Notification(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE HIS_NotificationLog ADD CONSTRAINT fk_notification_log_setting FOREIGN KEY (setting_id) REFERENCES MST_NotificationSettings(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE HIS_NotificationLog ADD CONSTRAINT fk_notification_log_template FOREIGN KEY (template_id) REFERENCES MST_NotificationTemplate(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE HIS_NotificationLog ADD CONSTRAINT fk_notification_log_integration FOREIGN KEY (integration_config_id) REFERENCES SYS_IntegrationConfig(id) ON UPDATE CASCADE ON DELETE SET NULL;


-- HIS_TenantBilling (テナント課金履歴) DDL
-- 生成日時: 2025-06-01 19:42:44

CREATE TABLE HIS_TenantBilling (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    id VARCHAR(50),
    tenant_id VARCHAR(50),
    billing_period_start DATE,
    billing_period_end DATE,
    billing_type ENUM,
    plan_id VARCHAR(50),
    plan_name VARCHAR(200),
    base_amount DECIMAL(12,2) DEFAULT 0.0,
    usage_amount DECIMAL(12,2) DEFAULT 0.0,
    additional_amount DECIMAL(12,2) DEFAULT 0.0,
    discount_amount DECIMAL(12,2) DEFAULT 0.0,
    subtotal_amount DECIMAL(12,2),
    tax_rate DECIMAL(5,3),
    tax_amount DECIMAL(12,2),
    total_amount DECIMAL(12,2),
    currency_code VARCHAR(3) DEFAULT 'JPY',
    usage_details TEXT,
    billing_status ENUM DEFAULT 'CALCULATED',
    invoice_number VARCHAR(50),
    invoice_date DATE,
    due_date DATE,
    paid_date DATE,
    payment_method ENUM,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE INDEX idx_tenant_billing_tenant_period ON HIS_TenantBilling (tenant_id, billing_period_start, billing_period_end);
CREATE INDEX idx_tenant_billing_status ON HIS_TenantBilling (billing_status);
CREATE UNIQUE INDEX idx_tenant_billing_invoice ON HIS_TenantBilling (invoice_number);
CREATE INDEX idx_tenant_billing_dates ON HIS_TenantBilling (invoice_date, due_date, paid_date);
CREATE INDEX idx_tenant_billing_type ON HIS_TenantBilling (billing_type);
CREATE INDEX idx_tenant_billing_amount ON HIS_TenantBilling (total_amount);

-- 外部キー制約
ALTER TABLE HIS_TenantBilling ADD CONSTRAINT fk_tenant_billing_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;


-- WRK_BatchJobLog (一括登録ジョブログ) DDL
-- 生成日時: 2025-06-01 19:42:44

CREATE TABLE WRK_BatchJobLog (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

