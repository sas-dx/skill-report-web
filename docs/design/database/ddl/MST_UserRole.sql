-- ============================================
-- テーブル: MST_UserRole
-- 論理名: ユーザーロール紐付け
-- 説明: MST_UserRole（ユーザーロール紐付け）は、ユーザーとロールの関連付けを管理するマスタテーブルです。

主な目的：
- ユーザーとロールの多対多関係管理
- 動的なロール割り当て・解除
- 時限ロール・条件付きロール割り当て
- ロール継承・委譲の管理
- 権限昇格・降格の履歴管理
- 職務分離・最小権限の原則実装
- 監査・コンプライアンス対応

このテーブルは、ユーザーの実際の権限を決定する重要な関連テーブルであり、
システムセキュリティの実装において中核的な役割を果たします。

-- 作成日: 2025-06-21 22:02:18
-- ============================================

DROP TABLE IF EXISTS MST_UserRole;

CREATE TABLE MST_UserRole (
    userrole_id SERIAL NOT NULL COMMENT 'MST_UserRoleの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (userrole_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_userrole_tenant_id ON MST_UserRole (tenant_id);

-- 外部キー制約
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_user FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_role FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_assigned_by FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_delegation_source FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_approved_by FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
