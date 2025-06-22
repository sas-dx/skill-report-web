-- HIS_TenantBilling (テナント課金履歴) サンプルデータ
-- 生成日時: 2025-06-21 22:02:17

INSERT INTO HIS_TenantBilling (
    tenantbilling_id, tenant_id, created_at, updated_at,
    id, is_deleted
) VALUES
    (NULL, 'TENANT001', NULL, NULL,
     'TB001', NULL),
    (NULL, 'TENANT002', NULL, NULL,
     'TB002', NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM HIS_TenantBilling ORDER BY created_at DESC;
