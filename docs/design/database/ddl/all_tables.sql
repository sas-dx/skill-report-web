-- 全テーブル統合DDL
-- 生成日時: 2025-06-01 12:50:47

-- MST_Role (ロール情報) DDL
-- 生成日時: 2025-06-01 12:50:47

CREATE TABLE MST_Role (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL,
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
-- 生成日時: 2025-06-01 12:50:47

CREATE TABLE MST_Permission (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL,
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
