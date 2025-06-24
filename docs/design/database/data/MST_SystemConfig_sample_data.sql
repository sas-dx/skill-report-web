-- MST_SystemConfig (システム設定) サンプルデータ
-- 生成日時: 2025-06-24 22:56:15

INSERT INTO MST_SystemConfig (
    id, tenant_id, config_key, config_category,
    config_name, config_type, config_value, default_value,
    description, environment, is_active, is_encrypted,
    is_system_only, is_user_configurable, last_modified_by, last_modified_reason,
    requires_restart, sort_order, systemconfig_id, tenant_specific,
    validation_rule, is_deleted, created_at, updated_at
) VALUES
    (NULL, NULL, 'MAX_LOGIN_ATTEMPTS', 'SECURITY',
     '最大ログイン試行回数', 'INTEGER', '5', '3',
     'アカウントロックまでの最大ログイン失敗回数', 'ALL', TRUE, FALSE,
     FALSE, TRUE, 'admin', 'セキュリティ強化のため',
     FALSE, 1, NULL, TRUE,
     '^[1-9][0-9]*$', NULL, NULL, NULL),
    (NULL, NULL, 'SESSION_TIMEOUT_MINUTES', 'SECURITY',
     'セッションタイムアウト時間（分）', 'INTEGER', '30', '60',
     'ユーザーセッションの自動タイムアウト時間', 'ALL', TRUE, FALSE,
     FALSE, TRUE, 'admin', 'セキュリティポリシー変更',
     FALSE, 2, NULL, TRUE,
     '^[1-9][0-9]*$', NULL, NULL, NULL),
    (NULL, NULL, 'SKILL_EVALUATION_PERIOD_MONTHS', 'BUSINESS',
     'スキル評価期間（月）', 'INTEGER', '6', '12',
     'スキル評価の実施間隔', 'ALL', TRUE, FALSE,
     FALSE, TRUE, 'hr_admin', '評価頻度の見直し',
     FALSE, 10, NULL, TRUE,
     '^[1-9][0-9]*$', NULL, NULL, NULL),
    (NULL, NULL, 'EMAIL_SMTP_PASSWORD', 'INTEGRATION',
     'SMTP認証パスワード', 'ENCRYPTED', 'encrypted_password_value', NULL,
     'メール送信用SMTP認証パスワード', 'PROD', TRUE, TRUE,
     TRUE, FALSE, 'system', '初期設定',
     TRUE, 100, NULL, FALSE,
     NULL, NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_SystemConfig ORDER BY created_at DESC;
