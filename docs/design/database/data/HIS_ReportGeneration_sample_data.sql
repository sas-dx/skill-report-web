-- HIS_ReportGeneration (帳票生成履歴) サンプルデータ
-- 生成日時: 2025-06-21 22:02:17

INSERT INTO HIS_ReportGeneration (
    reportgeneration_id, tenant_id, created_at, updated_at,
    id, is_deleted
) VALUES
    (NULL, 'TENANT001', NULL, NULL,
     'RG001', NULL),
    (NULL, 'TENANT001', NULL, NULL,
     'RG002', NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM HIS_ReportGeneration ORDER BY created_at DESC;
