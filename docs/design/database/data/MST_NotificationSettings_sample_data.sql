-- MST_NotificationSettings (通知設定) サンプルデータ
-- 生成日時: 2025-06-04 06:57:02

INSERT INTO MST_NotificationSettings (
    id, tenant_id, setting_key, setting_name,
    notification_type, target_audience, trigger_event, frequency_type,
    frequency_value, template_id, channel_config, is_enabled,
    priority_level, code, name, description
) VALUES
    ('NS001', 'TENANT001', 'skill_update_notification', 'スキル更新通知',
     'EMAIL', 'MANAGER', 'skill_registered', 'IMMEDIATE',
     NULL, 'NT001', '{"smtp_server": "smtp.company.com", "from_address": "noreply@company.com"}', TRUE,
     'MEDIUM', NULL, NULL, NULL),
    ('NS002', 'TENANT001', 'goal_deadline_reminder', '目標期限リマインダー',
     'SLACK', 'EMPLOYEE', 'goal_deadline_approaching', 'DAILY',
     9, 'NT002', '{"webhook_url": "https://hooks.slack.com/services/xxx", "channel": "#notifications"}', TRUE,
     'HIGH', NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_NotificationSettings ORDER BY created_at DESC;
