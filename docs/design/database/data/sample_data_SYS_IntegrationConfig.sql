-- サンプルデータ INSERT文: SYS_IntegrationConfig
-- 生成日時: 2025-06-21 07:31:30
-- レコード数: 3

BEGIN;

INSERT INTO SYS_IntegrationConfig (id, tenant_id, integration_key, integration_name, integration_type, endpoint_url, auth_type, auth_config, connection_config, request_headers, timeout_seconds, retry_count, retry_interval, rate_limit_per_minute, is_enabled, health_check_url, last_health_check, health_status, created_at, updated_at, is_deleted) VALUES ('IC001', 'TENANT001', 'slack_webhook', 'Slack通知連携', 'WEBHOOK', 'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX', 'NONE', NULL, '{"channel": "#notifications", "username": "SkillBot", "icon_emoji": ":robot_face:"}', '{"Content-Type": "application/json"}', 30, 3, 5, 60, TRUE, NULL, NULL, 'UNKNOWN', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO SYS_IntegrationConfig (id, tenant_id, integration_key, integration_name, integration_type, endpoint_url, auth_type, auth_config, connection_config, request_headers, timeout_seconds, retry_count, retry_interval, rate_limit_per_minute, is_enabled, health_check_url, last_health_check, health_status, created_at, updated_at, is_deleted) VALUES ('IC002', 'TENANT001', 'teams_connector', 'Microsoft Teams連携', 'WEBHOOK', 'https://outlook.office.com/webhook/xxx/IncomingWebhook/yyy/zzz', 'NONE', NULL, '{"title": "スキル管理システム", "theme_color": "0078D4"}', '{"Content-Type": "application/json"}', 30, 3, 5, 30, TRUE, NULL, NULL, 'UNKNOWN', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO SYS_IntegrationConfig (id, tenant_id, integration_key, integration_name, integration_type, endpoint_url, auth_type, auth_config, connection_config, request_headers, timeout_seconds, retry_count, retry_interval, rate_limit_per_minute, is_enabled, health_check_url, last_health_check, health_status, created_at, updated_at, is_deleted) VALUES ('IC003', 'TENANT001', 'smtp_server', 'メール送信サーバー', 'SMTP', 'smtp.company.com:587', 'BASIC', '{"username": "noreply@company.com", "password": "encrypted_password"}', '{"use_tls": true, "use_ssl": false, "from_address": "noreply@company.com", "from_name": "スキル管理システム"}', NULL, 60, 2, 10, 100, TRUE, NULL, '2025-06-01 19:00:00', 'HEALTHY', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);

COMMIT;

-- SYS_IntegrationConfig サンプルデータ終了
