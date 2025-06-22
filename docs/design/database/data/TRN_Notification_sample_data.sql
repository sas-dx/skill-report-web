-- TRN_Notification (通知履歴) サンプルデータ
-- 生成日時: 2025-06-21 22:02:17

INSERT INTO TRN_Notification (
    notification_id, tenant_id, created_at, updated_at,
    id, is_deleted, created_by, updated_by
) VALUES
    ('NOTIF_001', NULL, NULL, NULL,
     NULL, NULL, NULL, NULL),
    ('NOTIF_002', NULL, NULL, NULL,
     NULL, NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM TRN_Notification ORDER BY created_at DESC;
