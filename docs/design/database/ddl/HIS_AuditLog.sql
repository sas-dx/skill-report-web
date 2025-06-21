-- ============================================
-- テーブル: HIS_AuditLog
-- 論理名: 監査ログ
-- 説明: システム内で発生する全ての重要な操作を記録する監査ログテーブルです。

主な目的：
- セキュリティ監査のための操作履歴記録
- システム不正利用の検知・追跡
- コンプライアンス要件への対応
- トラブルシューティング時の操作履歴確認

このテーブルは法的要件やセキュリティポリシーに基づき、
90日間のログ保持期間を設けています。

-- 作成日: 2025-06-21 17:20:34
-- ============================================

DROP TABLE IF EXISTS HIS_AuditLog;

CREATE TABLE HIS_AuditLog (
    id VARCHAR,
    user_id VARCHAR,
    session_id VARCHAR,
    action_type ENUM,
    target_table VARCHAR,
    target_id VARCHAR,
    old_values TEXT,
    new_values TEXT,
    ip_address VARCHAR,
    user_agent VARCHAR,
    result_status ENUM DEFAULT 'SUCCESS',
    error_message TEXT,
    execution_time_ms INTEGER,
    is_deleted BOOLEAN DEFAULT False,
    tenant_id VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR,
    updated_by VARCHAR
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_his_auditlog_id ON HIS_AuditLog (id);
CREATE INDEX idx_his_auditlog_user_id ON HIS_AuditLog (user_id);
CREATE INDEX idx_his_auditlog_tenant_id ON HIS_AuditLog (tenant_id);
CREATE INDEX idx_his_auditlog_action_type ON HIS_AuditLog (action_type);
CREATE INDEX idx_his_auditlog_target_table ON HIS_AuditLog (target_table);
CREATE INDEX idx_his_auditlog_created_at ON HIS_AuditLog (created_at);
CREATE INDEX idx_his_auditlog_user_created ON HIS_AuditLog (user_id, created_at);
CREATE INDEX idx_his_auditlog_tenant_created ON HIS_AuditLog (tenant_id, created_at);
