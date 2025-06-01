-- MST_UserRole (ユーザーロール紐付け) DDL
-- 生成日時: 2025-06-01 20:40:25

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
