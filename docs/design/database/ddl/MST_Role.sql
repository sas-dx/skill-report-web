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
