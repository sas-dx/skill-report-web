-- サンプルデータ INSERT文: MST_SystemConfig
-- 生成日時: 2025-06-21 07:31:30
-- レコード数: 4

BEGIN;

INSERT INTO MST_SystemConfig (config_key, config_name, config_value, config_type, config_category, default_value, validation_rule, description, is_encrypted, is_system_only, is_user_configurable, requires_restart, environment, tenant_specific, last_modified_by, last_modified_reason, sort_order, is_active, id, created_at, updated_at, is_deleted) VALUES ('MAX_LOGIN_ATTEMPTS', '最大ログイン試行回数', '5', 'INTEGER', 'SECURITY', '3', '^[1-9][0-9]*$', 'アカウントロックまでの最大ログイン失敗回数', FALSE, FALSE, TRUE, FALSE, 'ALL', TRUE, 'admin', 'セキュリティ強化のため', 1, TRUE, 'mst_8947efb7', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO MST_SystemConfig (config_key, config_name, config_value, config_type, config_category, default_value, validation_rule, description, is_encrypted, is_system_only, is_user_configurable, requires_restart, environment, tenant_specific, last_modified_by, last_modified_reason, sort_order, is_active, id, created_at, updated_at, is_deleted) VALUES ('SESSION_TIMEOUT_MINUTES', 'セッションタイムアウト時間（分）', '30', 'INTEGER', 'SECURITY', '60', '^[1-9][0-9]*$', 'ユーザーセッションの自動タイムアウト時間', FALSE, FALSE, TRUE, FALSE, 'ALL', TRUE, 'admin', 'セキュリティポリシー変更', 2, TRUE, 'mst_21d51cab', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO MST_SystemConfig (config_key, config_name, config_value, config_type, config_category, default_value, validation_rule, description, is_encrypted, is_system_only, is_user_configurable, requires_restart, environment, tenant_specific, last_modified_by, last_modified_reason, sort_order, is_active, id, created_at, updated_at, is_deleted) VALUES ('SKILL_EVALUATION_PERIOD_MONTHS', 'スキル評価期間（月）', '6', 'INTEGER', 'BUSINESS', '12', '^[1-9][0-9]*$', 'スキル評価の実施間隔', FALSE, FALSE, TRUE, FALSE, 'ALL', TRUE, 'hr_admin', '評価頻度の見直し', 10, TRUE, 'mst_c66e15a6', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO MST_SystemConfig (config_key, config_name, config_value, config_type, config_category, default_value, validation_rule, description, is_encrypted, is_system_only, is_user_configurable, requires_restart, environment, tenant_specific, last_modified_by, last_modified_reason, sort_order, is_active, id, created_at, updated_at, is_deleted) VALUES ('EMAIL_SMTP_PASSWORD', 'SMTP認証パスワード', 'encrypted_password_value', 'ENCRYPTED', 'INTEGRATION', NULL, NULL, 'メール送信用SMTP認証パスワード', TRUE, TRUE, FALSE, TRUE, 'PROD', FALSE, 'system', '初期設定', 100, TRUE, 'mst_10e12c0a', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);

COMMIT;

-- MST_SystemConfig サンプルデータ終了
