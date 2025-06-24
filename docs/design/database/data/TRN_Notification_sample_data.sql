-- TRN_Notification (通知履歴) サンプルデータ
-- 生成日時: 2025-06-24 23:02:17

INSERT INTO TRN_Notification (
    id, tenant_id, batch_id, notification_id,
    title, message, action_label, action_url,
    archived_at, delivered_at, delivery_method, delivery_status,
    device_type, error_message, expiry_date, external_message_id,
    ip_address, is_bulk_notification, last_retry_at, max_retry_count,
    message_format, notification_category, notification_type, personalization_data,
    priority_level, read_at, read_status, recipient_id,
    related_entity_id, related_entity_type, retry_count, sender_id,
    sent_at, template_id, template_variables, user_agent,
    is_deleted, created_at, created_by, updated_by,
    updated_at
) VALUES
    (NULL, NULL, NULL, 'NOTIF_001',
     'AWS認定資格の更新期限が近づいています', 'お持ちのAWS認定ソリューションアーキテクト資格の有効期限が30日後に迫っています。更新手続きをお忘れなく。', '更新手続きへ', '/certifications/renewal/CERT_AWS_001',
     NULL, '2024-05-01 09:01:23', 'EMAIL', 'DELIVERED',
     'PC', NULL, '2024-06-01', 'email_12345',
     '192.168.1.100', FALSE, NULL, 3,
     'PLAIN', 'CERTIFICATION', 'REMINDER', '{"preferred_language": "ja", "timezone": "Asia/Tokyo"}',
     'HIGH', '2024-05-01 10:30:45', 'READ', 'EMP000001',
     'CERT_AWS_001', 'CERTIFICATION', 0, NULL,
     '2024-05-01 09:00:00', 'TMPL_CERT_RENEWAL', '{"certification_name": "AWS認定ソリューションアーキテクト", "days_until_expiry": 30}', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
     NULL, NULL, NULL, NULL,
     NULL),
    (NULL, NULL, NULL, 'NOTIF_002',
     '研修参加申請が承認されました', '申請いただいた「プロジェクトマネジメント基礎研修」への参加が承認されました。研修日程をご確認ください。', '研修詳細を確認', '/training/details/TRN_PROG_001',
     '2024-04-20 10:00:00', '2024-04-15 14:30:01', 'IN_APP', 'DELIVERED',
     'MOBILE', NULL, NULL, NULL,
     '192.168.1.101', FALSE, NULL, 3,
     'HTML', 'TRAINING', 'APPROVAL', '{"preferred_language": "ja", "notification_sound": true}',
     'NORMAL', '2024-04-15 15:45:20', 'READ', 'EMP000002',
     'TRN_PROG_001', 'TRAINING', 0, 'EMP000010',
     '2024-04-15 14:30:00', 'TMPL_TRAINING_APPROVAL', '{"training_name": "プロジェクトマネジメント基礎研修", "approver_name": "田中部長"}', 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',
     NULL, NULL, NULL, NULL,
     NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM TRN_Notification ORDER BY created_at DESC;
