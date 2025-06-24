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

-- 作成日: 2025-06-24 23:02:18
-- ============================================

DROP TABLE IF EXISTS HIS_AuditLog;

CREATE TABLE HIS_AuditLog (
    id VARCHAR(50) COMMENT 'ID',
    tenant_id VARCHAR(50) COMMENT 'テナントID',
    action_type ENUM('CREATE', 'READ', 'UPDATE', 'DELETE', 'LOGIN', 'LOGOUT') COMMENT 'アクション種別',
    auditlog_id INT AUTO_INCREMENT NOT NULL COMMENT 'HIS_AuditLogの主キー',
    created_by VARCHAR(50) COMMENT '作成者',
    error_message TEXT COMMENT 'エラーメッセージ',
    execution_time_ms INTEGER COMMENT '実行時間',
    ip_address VARCHAR(45) COMMENT 'IPアドレス',
    new_values TEXT COMMENT '変更後値',
    old_values TEXT COMMENT '変更前値',
    result_status ENUM('SUCCESS', 'FAILURE', 'ERROR') DEFAULT 'SUCCESS' COMMENT '実行結果',
    session_id VARCHAR(100) COMMENT 'セッションID',
    target_id VARCHAR(50) COMMENT '対象レコードID',
    target_table VARCHAR(100) COMMENT '対象テーブル',
    updated_by VARCHAR(50) COMMENT '更新者',
    user_agent VARCHAR(500) COMMENT 'ユーザーエージェント',
    user_id VARCHAR(50) COMMENT 'ユーザーID',
    is_deleted BOOLEAN DEFAULT False COMMENT '削除フラグ',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
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

-- 外部キー制約
ALTER TABLE HIS_AuditLog ADD CONSTRAINT fk_his_auditlog_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE HIS_AuditLog ADD CONSTRAINT fk_his_auditlog_user FOREIGN KEY (user_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;

-- その他の制約
ALTER TABLE HIS_AuditLog ADD CONSTRAINT chk_his_auditlog_action_type CHECK (action_type IN ('CREATE', 'READ', 'UPDATE', 'DELETE', 'LOGIN', 'LOGOUT'));
ALTER TABLE HIS_AuditLog ADD CONSTRAINT chk_his_auditlog_result_status CHECK (result_status IN ('SUCCESS', 'FAILURE', 'ERROR'));
ALTER TABLE HIS_AuditLog ADD CONSTRAINT chk_his_auditlog_execution_time_positive CHECK (execution_time_ms IS NULL OR execution_time_ms >= 0);
