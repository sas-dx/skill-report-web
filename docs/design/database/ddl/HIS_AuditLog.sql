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
