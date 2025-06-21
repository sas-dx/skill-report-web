-- ============================================
-- テーブル: MST_RolePermission
-- 論理名: ロール権限紐付け
-- 説明: 
-- 作成日: 2025-06-21 17:20:35
-- ============================================

DROP TABLE IF EXISTS MST_RolePermission;

CREATE TABLE MST_RolePermission (
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_rolepermission_role_id ON MST_RolePermission (role_id);
CREATE INDEX idx_mst_rolepermission_permission_id ON MST_RolePermission (permission_id);
CREATE INDEX idx_mst_rolepermission_role_permission ON MST_RolePermission (role_id, permission_id);
CREATE INDEX idx_mst_rolepermission_active ON MST_RolePermission (is_active, role_id);
CREATE INDEX idx_mst_rolepermission_granted_at ON MST_RolePermission (granted_at);
