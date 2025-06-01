-- 全テーブル統合DDL
-- 生成日時: 2025-06-01 16:12:38

-- MST_UserAuth (ユーザー認証情報) DDL
-- 生成日時: 2025-06-01 16:12:37

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
-- 生成日時: 2025-06-01 16:12:37

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
-- 生成日時: 2025-06-01 16:12:37

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
-- 生成日時: 2025-06-01 16:12:37

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
-- 生成日時: 2025-06-01 16:12:37

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
-- 生成日時: 2025-06-01 16:12:37

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
-- 生成日時: 2025-06-01 16:12:38

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
-- 生成日時: 2025-06-01 16:12:38

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
-- 生成日時: 2025-06-01 16:12:38

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
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE MST_CareerPlan (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- MST_ReportTemplate (帳票テンプレート) DDL
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE MST_ReportTemplate (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- MST_SystemConfig (システム設定) DDL
-- 生成日時: 2025-06-01 16:12:38

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
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE MST_Tenant (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- MST_TenantSettings (テナント設定) DDL
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE MST_TenantSettings (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- MST_NotificationSettings (通知設定) DDL
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE MST_NotificationSettings (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- MST_NotificationTemplate (通知テンプレート) DDL
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE MST_NotificationTemplate (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- MST_SkillCategory (スキルカテゴリマスタ) DDL
-- 生成日時: 2025-06-01 16:12:38

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
-- 生成日時: 2025-06-01 16:12:38

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
-- 生成日時: 2025-06-01 16:12:38

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
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE MST_CertificationRequirement (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- MST_EmployeeJobType (社員職種関連) DDL
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE MST_EmployeeJobType (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- MST_JobTypeSkillGrade (職種スキルグレード関連) DDL
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE MST_JobTypeSkillGrade (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- MST_SkillGradeRequirement (スキルグレード要件) DDL
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE MST_SkillGradeRequirement (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- MST_JobTypeSkill (職種スキル関連) DDL
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE MST_JobTypeSkill (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- MST_EmployeeDepartment (社員部署関連) DDL
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE MST_EmployeeDepartment (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- MST_EmployeePosition (社員役職関連) DDL
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE MST_EmployeePosition (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- MST_SkillItem (スキル項目マスタ) DDL
-- 生成日時: 2025-06-01 16:12:38

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
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE MST_TrainingProgram (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- TRN_SkillRecord (スキル情報) DDL
-- 生成日時: 2025-06-01 16:12:38

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
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE TRN_GoalProgress (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    employee_id VARCHAR(50),
    goal_title VARCHAR(200),
    goal_category ENUM,
    target_date DATE,
    progress_rate DECIMAL(5,2) DEFAULT 0.0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE INDEX idx_employee ON TRN_GoalProgress (employee_id);


-- TRN_ProjectRecord (案件実績) DDL
-- 生成日時: 2025-06-01 16:12:38

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
-- 生成日時: 2025-06-01 16:12:38

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
-- 生成日時: 2025-06-01 16:12:38

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
-- 生成日時: 2025-06-01 16:12:38

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
-- 生成日時: 2025-06-01 16:12:38

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


-- TRN_EmployeeSkillGrade (社員スキルグレード) DDL
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE TRN_EmployeeSkillGrade (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    employee_id VARCHAR(50),
    job_type_id VARCHAR(50),
    skill_grade VARCHAR(10),
    skill_level INT,
    effective_date DATE,
    expiry_date DATE,
    evaluation_date DATE,
    evaluator_id VARCHAR(50),
    evaluation_comment TEXT,
    certification_flag BOOLEAN DEFAULT False,
    next_evaluation_date DATE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE INDEX idx_employee_job_effective ON TRN_EmployeeSkillGrade (employee_id, job_type_id, effective_date);
CREATE INDEX idx_employee_current ON TRN_EmployeeSkillGrade (employee_id, expiry_date);
CREATE INDEX idx_job_type_grade ON TRN_EmployeeSkillGrade (job_type_id, skill_grade);
CREATE INDEX idx_evaluation_date ON TRN_EmployeeSkillGrade (evaluation_date);
CREATE INDEX idx_next_evaluation ON TRN_EmployeeSkillGrade (next_evaluation_date);
CREATE INDEX idx_certification ON TRN_EmployeeSkillGrade (certification_flag);

-- 外部キー制約
ALTER TABLE TRN_EmployeeSkillGrade ADD CONSTRAINT fk_skill_grade_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE TRN_EmployeeSkillGrade ADD CONSTRAINT fk_skill_grade_job_type FOREIGN KEY (job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_EmployeeSkillGrade ADD CONSTRAINT fk_skill_grade_evaluator FOREIGN KEY (evaluator_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;


-- SYS_SkillIndex (スキル検索インデックス) DDL
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE SYS_SkillIndex (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- SYS_SkillMatrix (スキルマップ) DDL
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE SYS_SkillMatrix (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- SYS_BackupHistory (バックアップ履歴) DDL
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE SYS_BackupHistory (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- SYS_SystemLog (システムログ) DDL
-- 生成日時: 2025-06-01 16:12:38

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
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE SYS_TokenStore (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- SYS_MasterData (マスタデータ全般) DDL
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE SYS_MasterData (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- SYS_TenantUsage (テナント使用量) DDL
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE SYS_TenantUsage (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- SYS_IntegrationConfig (外部連携設定) DDL
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE SYS_IntegrationConfig (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- HIS_AuditLog (監査ログ) DDL
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE HIS_AuditLog (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- HIS_NotificationLog (通知送信履歴) DDL
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE HIS_NotificationLog (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- HIS_TenantBilling (テナント課金履歴) DDL
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE HIS_TenantBilling (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);



-- WRK_BatchJobLog (一括登録ジョブログ) DDL
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE WRK_BatchJobLog (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

