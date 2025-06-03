-- ============================================
-- テーブル: HIS_AuditLog
-- 論理名: 監査ログ
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS HIS_AuditLog;

CREATE TABLE HIS_AuditLog (
    id VARCHAR(50) COMMENT 'プライマリキー（UUID）',
    user_id VARCHAR(50) COMMENT '操作を実行したユーザーのID',
    session_id VARCHAR(100) COMMENT '操作時のセッション識別子',
    action_type ENUM COMMENT '実行されたアクションの種別（CREATE:作成、READ:参照、UPDATE:更新、DELETE:削除、LOGIN:ログイン、LOGOUT:ログアウト）',
    target_table VARCHAR(100) COMMENT '操作対象のテーブル名',
    target_id VARCHAR(50) COMMENT '操作対象のレコードID',
    old_values TEXT COMMENT '更新・削除前のデータ（JSON形式）',
    new_values TEXT COMMENT '作成・更新後のデータ（JSON形式）',
    ip_address VARCHAR(45) COMMENT '操作元のIPアドレス（IPv6対応）',
    user_agent VARCHAR(500) COMMENT '操作時のブラウザ・アプリケーション情報',
    result_status ENUM DEFAULT 'SUCCESS' COMMENT '操作の実行結果（SUCCESS:成功、FAILURE:失敗、ERROR:エラー）',
    error_message TEXT COMMENT '操作失敗時のエラーメッセージ',
    execution_time_ms INTEGER COMMENT '操作の実行時間（ミリ秒）',
    is_deleted BOOLEAN DEFAULT False COMMENT '論理削除フラグ（監査ログは物理削除禁止）',
    tenant_id VARCHAR(50) COMMENT 'マルチテナント識別子',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時',
    created_by VARCHAR(50) COMMENT 'レコード作成者のユーザーID',
    updated_by VARCHAR(50) COMMENT 'レコード更新者のユーザーID'
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
