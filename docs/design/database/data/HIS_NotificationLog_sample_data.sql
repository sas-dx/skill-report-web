-- HIS_NotificationLog (通知送信履歴) サンプルデータ
-- 生成日時: 2025-06-21 22:02:18

INSERT INTO HIS_NotificationLog (
    notificationlog_id, tenant_id, created_at, updated_at,
    id, is_deleted
) VALUES
    (NULL, 'TENANT001', NULL, NULL,
     'NL001', NULL),
    (NULL, 'TENANT001', NULL, NULL,
     'NL002', NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM HIS_NotificationLog ORDER BY created_at DESC;
