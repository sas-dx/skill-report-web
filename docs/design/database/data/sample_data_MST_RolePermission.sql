-- サンプルデータ INSERT文: MST_RolePermission
-- 生成日時: 2025-06-21 07:31:30
-- レコード数: 13

BEGIN;

INSERT INTO MST_RolePermission (role_permission_id, role_id, permission_id, is_active, granted_at, granted_by, revoked_at, revoked_by, notes, created_at, updated_at, id, is_deleted) VALUES ('1', '1', '1', 'True', '2024-01-01 00:00:00', '1', NULL, NULL, 'システム管理者の基本権限', '2024-01-01 00:00:00', '2024-01-01 00:00:00', 'mst_84869f97', FALSE);
INSERT INTO MST_RolePermission (role_permission_id, role_id, permission_id, is_active, granted_at, granted_by, revoked_at, revoked_by, notes, created_at, updated_at, id, is_deleted) VALUES ('2', '1', '2', 'True', '2024-01-01 00:00:00', '1', NULL, NULL, 'システム管理者の基本権限', '2024-01-01 00:00:00', '2024-01-01 00:00:00', 'mst_4e934173', FALSE);
INSERT INTO MST_RolePermission (role_permission_id, role_id, permission_id, is_active, granted_at, granted_by, revoked_at, revoked_by, notes, created_at, updated_at, id, is_deleted) VALUES ('3', '1', '3', 'True', '2024-01-01 00:00:00', '1', NULL, NULL, 'システム管理者の基本権限', '2024-01-01 00:00:00', '2024-01-01 00:00:00', 'mst_03c26acc', FALSE);
INSERT INTO MST_RolePermission (role_permission_id, role_id, permission_id, is_active, granted_at, granted_by, revoked_at, revoked_by, notes, created_at, updated_at, id, is_deleted) VALUES ('4', '2', '4', 'True', '2024-01-01 00:00:00', '1', NULL, NULL, '人事管理者の基本権限', '2024-01-01 00:00:00', '2024-01-01 00:00:00', 'mst_73b2677f', FALSE);
INSERT INTO MST_RolePermission (role_permission_id, role_id, permission_id, is_active, granted_at, granted_by, revoked_at, revoked_by, notes, created_at, updated_at, id, is_deleted) VALUES ('5', '2', '5', 'True', '2024-01-01 00:00:00', '1', NULL, NULL, '人事管理者の基本権限', '2024-01-01 00:00:00', '2024-01-01 00:00:00', 'mst_c2b80586', FALSE);
INSERT INTO MST_RolePermission (role_permission_id, role_id, permission_id, is_active, granted_at, granted_by, revoked_at, revoked_by, notes, created_at, updated_at, id, is_deleted) VALUES ('6', '3', '6', 'True', '2024-01-01 00:00:00', '1', NULL, NULL, 'スキル管理者の基本権限', '2024-01-01 00:00:00', '2024-01-01 00:00:00', 'mst_ad25b69f', FALSE);
INSERT INTO MST_RolePermission (role_permission_id, role_id, permission_id, is_active, granted_at, granted_by, revoked_at, revoked_by, notes, created_at, updated_at, id, is_deleted) VALUES ('7', '3', '7', 'True', '2024-01-01 00:00:00', '1', NULL, NULL, 'スキル管理者の基本権限', '2024-01-01 00:00:00', '2024-01-01 00:00:00', 'mst_4a43c332', FALSE);
INSERT INTO MST_RolePermission (role_permission_id, role_id, permission_id, is_active, granted_at, granted_by, revoked_at, revoked_by, notes, created_at, updated_at, id, is_deleted) VALUES ('8', '4', '8', 'True', '2024-01-01 00:00:00', '1', NULL, NULL, '一般ユーザーの基本権限', '2024-01-01 00:00:00', '2024-01-01 00:00:00', 'mst_22381d66', FALSE);
INSERT INTO MST_RolePermission (role_permission_id, role_id, permission_id, is_active, granted_at, granted_by, revoked_at, revoked_by, notes, created_at, updated_at, id, is_deleted) VALUES ('9', '4', '9', 'True', '2024-01-01 00:00:00', '1', NULL, NULL, '一般ユーザーの基本権限', '2024-01-01 00:00:00', '2024-01-01 00:00:00', 'mst_8076c352', FALSE);
INSERT INTO MST_RolePermission (role_permission_id, role_id, permission_id, is_active, granted_at, granted_by, revoked_at, revoked_by, notes, created_at, updated_at, id, is_deleted) VALUES ('10', '5', '8', 'True', '2024-01-01 00:00:00', '1', NULL, NULL, '閲覧専用ユーザーの基本権限', '2024-01-01 00:00:00', '2024-01-01 00:00:00', 'mst_becfa12e', FALSE);
INSERT INTO MST_RolePermission (role_permission_id, role_id, permission_id, is_active, granted_at, granted_by, revoked_at, revoked_by, notes, created_at, updated_at, id, is_deleted) VALUES ('11', '5', '10', 'True', '2024-01-01 00:00:00', '1', NULL, NULL, '閲覧専用ユーザーの基本権限', '2024-01-01 00:00:00', '2024-01-01 00:00:00', 'mst_edf332af', FALSE);
INSERT INTO MST_RolePermission (role_permission_id, role_id, permission_id, is_active, granted_at, granted_by, revoked_at, revoked_by, notes, created_at, updated_at, id, is_deleted) VALUES ('12', '2', '11', 'True', '2024-02-01 00:00:00', '1', NULL, NULL, '研修管理権限の追加付与', '2024-02-01 00:00:00', '2024-02-01 00:00:00', 'mst_7e683828', FALSE);
INSERT INTO MST_RolePermission (role_permission_id, role_id, permission_id, is_active, granted_at, granted_by, revoked_at, revoked_by, notes, created_at, updated_at, id, is_deleted) VALUES ('13', '3', '12', 'False', '2024-01-01 00:00:00', '1', '2024-03-01 00:00:00', '1', '権限範囲の見直しにより取消', '2024-01-01 00:00:00', '2024-03-01 00:00:00', 'mst_1afdd269', FALSE);

COMMIT;

-- MST_RolePermission サンプルデータ終了
