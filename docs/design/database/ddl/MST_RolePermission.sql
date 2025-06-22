-- ============================================
-- テーブル: MST_RolePermission
-- 論理名: ロール権限紐付け
-- 説明: MST_RolePermission（ロール権限紐付け）は、ロールと権限の多対多関係を管理するマスタテーブルです。

主な目的：
- ロールベースアクセス制御（RBAC）の実現
- 権限付与・取消の履歴管理と監査証跡の保持
- 細粒度な権限制御による情報セキュリティの確保
- 権限変更の追跡可能性とコンプライアンス対応
- システム機能へのアクセス制御の柔軟な管理

このテーブルは、システムのセキュリティ基盤として重要な役割を果たし、
適切な権限管理により情報漏洩や不正アクセスを防止します。

-- 作成日: 2025-06-21 22:37:20
-- ============================================

DROP TABLE IF EXISTS MST_RolePermission;

CREATE TABLE MST_RolePermission (
    role_permission_id BIGINT NOT NULL AUTO_INCREMENT COMMENT 'ロール権限紐付けの一意識別子',
    role_id BIGINT NOT NULL COMMENT '権限を付与するロールのID',
    permission_id BIGINT NOT NULL COMMENT 'ロールに付与する権限のID',
    is_active BOOLEAN NOT NULL DEFAULT True COMMENT 'この権限付与が有効かどうか',
    granted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'この権限がロールに付与された日時',
    granted_by BIGINT NOT NULL COMMENT 'この権限を付与したユーザーのID',
    revoked_at TIMESTAMP COMMENT 'この権限が取り消された日時（NULL=未取消）',
    revoked_by BIGINT COMMENT 'この権限を取り消したユーザーのID',
    notes TEXT COMMENT '権限付与・取消に関する備考',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT 'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP' COMMENT 'レコード最終更新日時',
    PRIMARY KEY (role_permission_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_rolepermission_role_id ON MST_RolePermission (role_id);
CREATE INDEX idx_mst_rolepermission_permission_id ON MST_RolePermission (permission_id);
CREATE INDEX idx_mst_rolepermission_role_permission ON MST_RolePermission (role_id, permission_id);
CREATE INDEX idx_mst_rolepermission_active ON MST_RolePermission (is_active, role_id);
CREATE INDEX idx_mst_rolepermission_granted_at ON MST_RolePermission (granted_at);

-- 外部キー制約
ALTER TABLE MST_RolePermission ADD CONSTRAINT fk_mst_rolepermission_role_id FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_RolePermission ADD CONSTRAINT fk_mst_rolepermission_permission_id FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_RolePermission ADD CONSTRAINT fk_mst_rolepermission_granted_by FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_RolePermission ADD CONSTRAINT fk_mst_rolepermission_revoked_by FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE RESTRICT;
