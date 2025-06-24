-- SYS_MasterData (マスターデータ管理) サンプルデータ
-- 生成日時: 2025-06-24 22:56:15

INSERT INTO SYS_MasterData (
    id, data_type, default_value, description,
    display_order, effective_from, effective_to, is_editable,
    is_system_managed, last_modified_at, last_modified_by, master_category,
    master_key, master_name, master_value, masterdata_id,
    validation_rule, version, is_deleted, created_at,
    updated_at
) VALUES
    (NULL, 'INTEGER', '3', 'ログイン失敗時の最大試行回数。この回数を超えるとアカウントがロックされます。',
     1, '2024-01-01', NULL, TRUE,
     TRUE, '2024-01-01 10:00:00', 'system_admin', 'SYSTEM',
     'SYSTEM.MAX_LOGIN_ATTEMPTS', '最大ログイン試行回数', '5', NULL,
     '^[1-9][0-9]*$', 1, NULL, NULL,
     NULL),
    (NULL, 'INTEGER', '30', 'ユーザーセッションの有効時間（分）。この時間を過ぎると自動的にログアウトされます。',
     2, '2024-01-01', NULL, TRUE,
     TRUE, '2024-01-01 10:00:00', 'system_admin', 'SYSTEM',
     'SYSTEM.SESSION_TIMEOUT_MINUTES', 'セッションタイムアウト時間', '30', NULL,
     '^[1-9][0-9]*$', 1, NULL, NULL,
     NULL),
    (NULL, 'JSON', '{"1":"初級","2":"中級","3":"上級","4":"エキスパート","5":"マスター"}', 'スキル評価で使用するレベル定義。1-5の数値とその意味を定義します。',
     1, '2024-01-01', NULL, TRUE,
     FALSE, '2024-01-01 10:00:00', 'admin_user', 'CODE',
     'CODE.SKILL_LEVELS', 'スキルレベル定義', '{"1":"初級","2":"中級","3":"上級","4":"エキスパート","5":"マスター"}', NULL,
     NULL, 1, NULL, NULL,
     NULL),
    (NULL, 'INTEGER', '30', 'フルバックアップファイルの保持期間（日数）。この期間を過ぎたバックアップは自動削除されます。',
     1, '2024-01-01', NULL, TRUE,
     TRUE, '2024-01-01 10:00:00', 'system_admin', 'CONFIG',
     'CONFIG.BACKUP_RETENTION_DAYS', 'バックアップ保持日数', '90', NULL,
     '^[1-9][0-9]*$', 1, NULL, NULL,
     NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM SYS_MasterData ORDER BY created_at DESC;
