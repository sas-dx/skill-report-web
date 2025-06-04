-- TRN_Notification (通知履歴) サンプルデータ
-- 生成日時: 2025-06-04 06:57:02

INSERT INTO TRN_Notification (
    notification_id, recipient_id, sender_id, notification_type,
    notification_category, priority_level, title, message,
    message_format, action_url, action_label, delivery_method,
    delivery_status, sent_at, delivered_at, read_status,
    read_at, archived_at, expiry_date, retry_count,
    max_retry_count, last_retry_at, error_message, external_message_id,
    template_id, template_variables, related_entity_type, related_entity_id,
    batch_id, user_agent, ip_address, device_type,
    is_bulk_notification, personalization_data, id, is_deleted,
    tenant_id, created_at, updated_at, created_by,
    updated_by
) VALUES
    ('NOTIF_001', 'EMP000001', NULL, 'REMINDER',
     'CERTIFICATION', 'HIGH', 'AWS認定資格の更新期限が近づいています', 'お持ちのAWS認定ソリューションアーキテクト資格の有効期限が30日後に迫っています。更新手続きをお忘れなく。',
     'PLAIN', '/certifications/renewal/CERT_AWS_001', '更新手続きへ', 'EMAIL',
     'DELIVERED', '2024-05-01 09:00:00', '2024-05-01 09:01:23', 'READ',
     '2024-05-01 10:30:45', NULL, '2024-06-01', 0,
     3, NULL, NULL, 'email_12345',
     'TMPL_CERT_RENEWAL', '{"certification_name": "AWS認定ソリューションアーキテクト", "days_until_expiry": 30}', 'CERTIFICATION', 'CERT_AWS_001',
     NULL, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.100', 'PC',
     FALSE, '{"preferred_language": "ja", "timezone": "Asia/Tokyo"}', NULL, NULL,
     NULL, NULL, NULL, NULL,
     NULL),
    ('NOTIF_002', 'EMP000002', 'EMP000010', 'APPROVAL',
     'TRAINING', 'NORMAL', '研修参加申請が承認されました', '申請いただいた「プロジェクトマネジメント基礎研修」への参加が承認されました。研修日程をご確認ください。',
     'HTML', '/training/details/TRN_PROG_001', '研修詳細を確認', 'IN_APP',
     'DELIVERED', '2024-04-15 14:30:00', '2024-04-15 14:30:01', 'READ',
     '2024-04-15 15:45:20', '2024-04-20 10:00:00', NULL, 0,
     3, NULL, NULL, NULL,
     'TMPL_TRAINING_APPROVAL', '{"training_name": "プロジェクトマネジメント基礎研修", "approver_name": "田中部長"}', 'TRAINING', 'TRN_PROG_001',
     NULL, 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)', '192.168.1.101', 'MOBILE',
     FALSE, '{"preferred_language": "ja", "notification_sound": true}', NULL, NULL,
     NULL, NULL, NULL, NULL,
     NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM TRN_Notification ORDER BY created_at DESC;
