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

-- 作成日: 2025-06-21 22:02:17
-- ============================================

DROP TABLE IF EXISTS HIS_AuditLog;

CREATE TABLE HIS_AuditLog (
    auditlog_id SERIAL NOT NULL COMMENT 'HIS_AuditLogの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    PRIMARY KEY (auditlog_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_his_auditlog_tenant_id ON HIS_AuditLog (tenant_id);

-- 外部キー制約
ALTER TABLE HIS_AuditLog ADD CONSTRAINT fk_his_auditlog_tenant FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE HIS_AuditLog ADD CONSTRAINT fk_his_auditlog_user FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE RESTRICT;
