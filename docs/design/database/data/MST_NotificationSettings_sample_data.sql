-- MST_NotificationSettings (通知設定) サンプルデータ
-- 生成日時: 2025-06-24 23:02:17

INSERT INTO MST_NotificationSettings (
    id, tenant_id, channel_config, frequency_type,
    frequency_value, is_enabled, notification_type, notificationsettings_id,
    priority_level, setting_key, setting_name, target_audience,
    template_id, trigger_event, is_deleted, created_at,
    updated_at
) VALUES
    ('NS001', 'TENANT001', '{"smtp_server": "smtp.company.com", "from_address": "noreply@company.com"}', 'IMMEDIATE',
     NULL, TRUE, 'EMAIL', NULL,
     'MEDIUM', 'skill_update_notification', 'スキル更新通知', 'MANAGER',
     'NT001', 'skill_registered', NULL, NULL,
     NULL),
    ('NS002', 'TENANT001', '{"webhook_url": "https://hooks.slack.com/services/xxx", "channel": "#notifications"}', 'DAILY',
     9, TRUE, 'SLACK', NULL,
     'HIGH', 'goal_deadline_reminder', '目標期限リマインダー', 'EMPLOYEE',
     'NT002', 'goal_deadline_approaching', NULL, NULL,
     NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_NotificationSettings ORDER BY created_at DESC;
