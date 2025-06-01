-- MST_Permission (権限情報) DDL
-- 生成日時: 2025-06-01 13:28:12

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
