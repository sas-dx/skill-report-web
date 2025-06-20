-- サンプルデータ INSERT文: MST_RolePermission
-- 生成日時: 2025-06-21 07:22:21
-- レコード数: 13

BEGIN;

INSERT INTO MST_RolePermission (role_permission_id, role_id, permission_id, is_active, granted_at, granted_by, revoked_at, revoked_by, notes, created_at, updated_at, id, is_deleted) VALUES ('1', '1', '1', 'True', '2024-01-01 00:00:00', '1', NULL, NULL, 'システム管理者の基本権限', '2024-01-01 00:00:00', '2024-01-01 00:00:00', 'mst_a8f18ca1', FALSE);
INSERT INTO MST_RolePermission (role_permission_id, role_id, permission_id, is_active, granted_at, granted_by, revoked_at, revoked_by, notes, created_at, updated_at, id, is_deleted) VALUES ('2', '1', '2', 'True', '2024-01-01 00:00:00', '1', NULL, NULL, 'システム管理者の基本権限', '2024-01-01 00:00:00', '2024-01-01 00:00:00', 'mst_5665f949', FALSE);
INSERT INTO MST_RolePermission (role_permission_id, role_id, permission_id, is_active, granted_at, granted_by, revoked_at, revoked_by, notes, created_at, updated_at, id, is_deleted) VALUES ('3', '1', '3', 'True', '2024-01-01 00:00:00', '1', NULL, NULL, 'システム管理者の基本権限', '2024-01-01 00:00:00', '2024-01-01 00:00:00', 'mst_52ef403b', FALSE);
INSERT INTO MST_RolePermission (role_permission_id, role_id, permission_id, is_active, granted_at, granted_by, revoked_at, revoked_by, notes, created_at, updated_at, id, is_deleted) VALUES ('4', '2', '4', 'True', '2024-01-01 00:00:00', '1', NULL, NULL, '人事管理者の基本権限', '2024-01-01 00:00:00', '2024-01-01 00:00:00', 'mst_aa541160', FALSE);
INSERT INTO MST_RolePermission (role_permission_id, role_id, permission_id, is_active, granted_at, granted_by, revoked_at, revoked_by, notes, created_at, updated_at, id, is_deleted) VALUES ('5', '2', '5', 'True', '2024-01-01 00:00:00', '1', NULL, NULL, '人事管理者の基本権限', '2024-01-01 00:00:00', '2024-01-01 00:00:00', 'mst_6ff1e763', FALSE);
INSERT INTO MST_RolePermission (role_permission_id, role_id, permission_id, is_active, granted_at, granted_by, revoked_at, revoked_by, notes, created_at, updated_at, id, is_deleted) VALUES ('6', '3', '6', 'True', '2024-01-01 00:00:00', '1', NULL, NULL, 'スキル管理者の基本権限', '2024-01-01 00:00:00', '2024-01-01 00:00:00', 'mst_56404dba', FALSE);
INSERT INTO MST_RolePermission (role_permission_id, role_id, permission_id, is_active, granted_at, granted_by, revoked_at, revoked_by, notes, created_at, updated_at, id, is_deleted) VALUES ('7', '3', '7', 'True', '2024-01-01 00:00:00', '1', NULL, NULL, 'スキル管理者の基本権限', '2024-01-01 00:00:00', '2024-01-01 00:00:00', 'mst_059eb4ec', FALSE);
INSERT INTO MST_RolePermission (role_permission_id, role_id, permission_id, is_active, granted_at, granted_by, revoked_at, revoked_by, notes, created_at, updated_at, id, is_deleted) VALUES ('8', '4', '8', 'True', '2024-01-01 00:00:00', '1', NULL, NULL, '一般ユーザーの基本権限', '2024-01-01 00:00:00', '2024-01-01 00:00:00', 'mst_e2f65c31', FALSE);
INSERT INTO MST_RolePermission (role_permission_id, role_id, permission_id, is_active, granted_at, granted_by, revoked_at, revoked_by, notes, created_at, updated_at, id, is_deleted) VALUES ('9', '4', '9', 'True', '2024-01-01 00:00:00', '1', NULL, NULL, '一般ユーザーの基本権限', '2024-01-01 00:00:00', '2024-01-01 00:00:00', 'mst_89506769', FALSE);
INSERT INTO MST_RolePermission (role_permission_id, role_id, permission_id, is_active, granted_at, granted_by, revoked_at, revoked_by, notes, created_at, updated_at, id, is_deleted) VALUES ('10', '5', '8', 'True', '2024-01-01 00:00:00', '1', NULL, NULL, '閲覧専用ユーザーの基本権限', '2024-01-01 00:00:00', '2024-01-01 00:00:00', 'mst_5a21a048', FALSE);
INSERT INTO MST_RolePermission (role_permission_id, role_id, permission_id, is_active, granted_at, granted_by, revoked_at, revoked_by, notes, created_at, updated_at, id, is_deleted) VALUES ('11', '5', '10', 'True', '2024-01-01 00:00:00', '1', NULL, NULL, '閲覧専用ユーザーの基本権限', '2024-01-01 00:00:00', '2024-01-01 00:00:00', 'mst_7366bd7a', FALSE);
INSERT INTO MST_RolePermission (role_permission_id, role_id, permission_id, is_active, granted_at, granted_by, revoked_at, revoked_by, notes, created_at, updated_at, id, is_deleted) VALUES ('12', '2', '11', 'True', '2024-02-01 00:00:00', '1', NULL, NULL, '研修管理権限の追加付与', '2024-02-01 00:00:00', '2024-02-01 00:00:00', 'mst_ee757d10', FALSE);
INSERT INTO MST_RolePermission (role_permission_id, role_id, permission_id, is_active, granted_at, granted_by, revoked_at, revoked_by, notes, created_at, updated_at, id, is_deleted) VALUES ('13', '3', '12', 'False', '2024-01-01 00:00:00', '1', '2024-03-01 00:00:00', '1', '権限範囲の見直しにより取消', '2024-01-01 00:00:00', '2024-03-01 00:00:00', 'mst_c9cd5749', FALSE);

COMMIT;

-- MST_RolePermission サンプルデータ終了
