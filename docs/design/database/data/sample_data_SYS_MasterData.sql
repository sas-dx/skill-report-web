-- サンプルデータ INSERT文: SYS_MasterData
-- 生成日時: 2025-06-21 07:31:30
-- レコード数: 4

BEGIN;

INSERT INTO SYS_MasterData (master_key, master_category, master_name, master_value, data_type, default_value, validation_rule, is_system_managed, is_editable, display_order, description, effective_from, effective_to, last_modified_by, last_modified_at, version, id, created_at, updated_at, is_deleted) VALUES ('SYSTEM.MAX_LOGIN_ATTEMPTS', 'SYSTEM', '最大ログイン試行回数', '5', 'INTEGER', '3', '^[1-9][0-9]*$', TRUE, TRUE, 1, 'ログイン失敗時の最大試行回数。この回数を超えるとアカウントがロックされます。', '2024-01-01', NULL, 'system_admin', '2024-01-01 10:00:00', 1, 'sys_35296e7b', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO SYS_MasterData (master_key, master_category, master_name, master_value, data_type, default_value, validation_rule, is_system_managed, is_editable, display_order, description, effective_from, effective_to, last_modified_by, last_modified_at, version, id, created_at, updated_at, is_deleted) VALUES ('SYSTEM.SESSION_TIMEOUT_MINUTES', 'SYSTEM', 'セッションタイムアウト時間', '30', 'INTEGER', '30', '^[1-9][0-9]*$', TRUE, TRUE, 2, 'ユーザーセッションの有効時間（分）。この時間を過ぎると自動的にログアウトされます。', '2024-01-01', NULL, 'system_admin', '2024-01-01 10:00:00', 1, 'sys_e1e3dbe8', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO SYS_MasterData (master_key, master_category, master_name, master_value, data_type, default_value, validation_rule, is_system_managed, is_editable, display_order, description, effective_from, effective_to, last_modified_by, last_modified_at, version, id, created_at, updated_at, is_deleted) VALUES ('CODE.SKILL_LEVELS', 'CODE', 'スキルレベル定義', '{"1":"初級","2":"中級","3":"上級","4":"エキスパート","5":"マスター"}', 'JSON', '{"1":"初級","2":"中級","3":"上級","4":"エキスパート","5":"マスター"}', NULL, FALSE, TRUE, 1, 'スキル評価で使用するレベル定義。1-5の数値とその意味を定義します。', '2024-01-01', NULL, 'admin_user', '2024-01-01 10:00:00', 1, 'sys_f4d9cf0b', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO SYS_MasterData (master_key, master_category, master_name, master_value, data_type, default_value, validation_rule, is_system_managed, is_editable, display_order, description, effective_from, effective_to, last_modified_by, last_modified_at, version, id, created_at, updated_at, is_deleted) VALUES ('CONFIG.BACKUP_RETENTION_DAYS', 'CONFIG', 'バックアップ保持日数', '90', 'INTEGER', '30', '^[1-9][0-9]*$', TRUE, TRUE, 1, 'フルバックアップファイルの保持期間（日数）。この期間を過ぎたバックアップは自動削除されます。', '2024-01-01', NULL, 'system_admin', '2024-01-01 10:00:00', 1, 'sys_e3793c64', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);

COMMIT;

-- SYS_MasterData サンプルデータ終了
