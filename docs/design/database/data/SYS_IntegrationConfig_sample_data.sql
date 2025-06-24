-- SYS_IntegrationConfig (外部連携設定) サンプルデータ
-- 生成日時: 2025-06-24 22:56:15

INSERT INTO SYS_IntegrationConfig (
    id, tenant_id, auth_config, auth_type,
    connection_config, endpoint_url, health_check_url, health_status,
    integration_key, integration_name, integration_type, integrationconfig_id,
    is_enabled, last_health_check, rate_limit_per_minute, request_headers,
    retry_count, retry_interval, timeout_seconds, is_deleted,
    created_at, updated_at
) VALUES
    ('IC001', 'TENANT001', NULL, 'NONE',
     '{"channel": "#notifications", "username": "SkillBot", "icon_emoji": ":robot_face:"}', 'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX', NULL, 'UNKNOWN',
     'slack_webhook', 'Slack通知連携', 'WEBHOOK', NULL,
     TRUE, NULL, 60, '{"Content-Type": "application/json"}',
     3, 5, 30, NULL,
     NULL, NULL),
    ('IC002', 'TENANT001', NULL, 'NONE',
     '{"title": "スキル管理システム", "theme_color": "0078D4"}', 'https://outlook.office.com/webhook/xxx/IncomingWebhook/yyy/zzz', NULL, 'UNKNOWN',
     'teams_connector', 'Microsoft Teams連携', 'WEBHOOK', NULL,
     TRUE, NULL, 30, '{"Content-Type": "application/json"}',
     3, 5, 30, NULL,
     NULL, NULL),
    ('IC003', 'TENANT001', '{"username": "noreply@company.com", "password": "encrypted_password"}', 'BASIC',
     '{"use_tls": true, "use_ssl": false, "from_address": "noreply@company.com", "from_name": "スキル管理システム"}', 'smtp.company.com:587', NULL, 'HEALTHY',
     'smtp_server', 'メール送信サーバー', 'SMTP', NULL,
     TRUE, '2025-06-01 19:00:00', 100, NULL,
     2, 10, 60, NULL,
     NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM SYS_IntegrationConfig ORDER BY created_at DESC;
