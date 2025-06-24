-- HIS_NotificationLog (通知送信履歴) サンプルデータ
-- 生成日時: 2025-06-24 23:05:57

INSERT INTO HIS_NotificationLog (
    id, tenant_id, notification_id, subject,
    delivered_at, error_details, integration_config_id, max_retry_count,
    message_body, message_format, notification_type, notificationlog_id,
    opened_at, priority_level, recipient_address, recipient_type,
    response_code, response_message, scheduled_at, send_attempts,
    send_status, sent_at, setting_id, template_id,
    is_deleted, created_at, updated_at
) VALUES
    ('NL001', 'TENANT001', 'NOTIF001', '【スキル更新】山田太郎さんのスキル情報が更新されました',
     '2025-06-01 10:30:45', NULL, 'IC003', 3,
     '山田太郎さん

以下のスキル情報が更新されました。

スキル名: Java
更新日時: 2025-06-01 10:30:00
更新者: 佐藤花子

詳細は以下のリンクからご確認ください。
https://system.company.com/skills/123

※このメールは自動送信されています。', 'PLAIN', 'EMAIL', NULL,
     '2025-06-01 11:15:30', 'MEDIUM', 'yamada.taro@company.com', 'USER',
     '250', 'Message accepted for delivery', '2025-06-01 10:30:00', 1,
     'SUCCESS', '2025-06-01 10:30:15', 'NS001', 'NT001',
     NULL, NULL, NULL),
    ('NL002', 'TENANT001', 'NOTIF002', NULL,
     NULL, '{"error": "channel_not_found", "details": "The specified channel does not exist or the bot is not a member"}', 'IC001', 3,
     ':warning: *目標期限のお知らせ* :warning:

山田太郎さんの目標「Java認定資格取得」の期限が近づいています。

• 期限: 2025-06-30
• 残り日数: 29日
• 進捗率: 75%

<https://system.company.com/goals/456|詳細を確認する>', 'MARKDOWN', 'SLACK', NULL,
     NULL, 'HIGH', '#notifications', 'CHANNEL',
     '404', 'channel_not_found', '2025-06-01 09:00:00', 3,
     'FAILED', NULL, 'NS002', 'NT002',
     NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM HIS_NotificationLog ORDER BY created_at DESC;
