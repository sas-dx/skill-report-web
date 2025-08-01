-- テーブル: HIS_AuditLog
-- 説明: 
-- 生成日時: 2025-06-26 14:21:17

CREATE TABLE HIS_AuditLog (
    id VARCHAR,
    tenant_id VARCHAR,
    action_type ENUM,
    auditlog_id SERIAL,
    created_by VARCHAR,
    error_message TEXT,
    execution_time_ms INTEGER,
    ip_address VARCHAR,
    new_values TEXT,
    old_values TEXT,
    result_status ENUM DEFAULT SUCCESS,
    session_id VARCHAR,
    target_id VARCHAR,
    target_table VARCHAR,
    updated_by VARCHAR,
    user_agent VARCHAR,
    user_id VARCHAR,
    is_deleted BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- インデックス
CREATE UNIQUE INDEX idx_his_auditlog_id ON HIS_AuditLog (id);
CREATE INDEX idx_his_auditlog_user_id ON HIS_AuditLog (user_id);
CREATE INDEX idx_his_auditlog_tenant_id ON HIS_AuditLog (tenant_id);
CREATE INDEX idx_his_auditlog_action_type ON HIS_AuditLog (action_type);
CREATE INDEX idx_his_auditlog_target_table ON HIS_AuditLog (target_table);
CREATE INDEX idx_his_auditlog_created_at ON HIS_AuditLog (created_at);
CREATE INDEX idx_his_auditlog_user_created ON HIS_AuditLog (user_id, created_at);
CREATE INDEX idx_his_auditlog_tenant_created ON HIS_AuditLog (tenant_id, created_at);

-- 外部キー制約
ALTER TABLE HIS_AuditLog ADD CONSTRAINT fk_his_auditlog_tenant
    FOREIGN KEY (tenant_id) REFERENCES MST_Tenant (id);
ALTER TABLE HIS_AuditLog ADD CONSTRAINT fk_his_auditlog_user
    FOREIGN KEY (user_id) REFERENCES MST_Employee (id);