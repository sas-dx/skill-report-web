-- HIS_NotificationLog (通知送信履歴) サンプルデータ
-- 生成日時: 2025-06-04 06:57:02

INSERT INTO HIS_NotificationLog (
    id, tenant_id, notification_id, setting_id,
    template_id, notification_type, recipient_type, recipient_address,
    subject, message_body, message_format, send_status,
    send_attempts, max_retry_count, scheduled_at, sent_at,
    delivered_at, opened_at, response_code, response_message,
    error_details, integration_config_id, priority_level, is_deleted
) VALUES
    ('NL001', 'TENANT001', 'NOTIF001', 'NS001',
     'NT001', 'EMAIL', 'USER', 'yamada.taro@company.com',
     '【スキル更新】山田太郎さんのスキル情報が更新されました', '山田太郎さん

以下のスキル情報が更新されました。

スキル名: Java
更新日時: 2025-06-01 10:30:00
更新者: 佐藤花子

詳細は以下のリンクからご確認ください。
https://system.company.com/skills/123

※このメールは自動送信されています。', 'PLAIN', 'SUCCESS',
     1, 3, '2025-06-01 10:30:00', '2025-06-01 10:30:15',
     '2025-06-01 10:30:45', '2025-06-01 11:15:30', '250', 'Message accepted for delivery',
     NULL, 'IC003', 'MEDIUM', NULL),
    ('NL002', 'TENANT001', 'NOTIF002', 'NS002',
     'NT002', 'SLACK', 'CHANNEL', '#notifications',
     NULL, ':warning: *目標期限のお知らせ* :warning:

山田太郎さんの目標「Java認定資格取得」の期限が近づいています。

• 期限: 2025-06-30
• 残り日数: 29日
• 進捗率: 75%

<https://system.company.com/goals/456|詳細を確認する>', 'MARKDOWN', 'FAILED',
     3, 3, '2025-06-01 09:00:00', NULL,
     NULL, NULL, '404', 'channel_not_found',
     '{"error": "channel_not_found", "details": "The specified channel does not exist or the bot is not a member"}', 'IC001', 'HIGH', NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM HIS_NotificationLog ORDER BY created_at DESC;
