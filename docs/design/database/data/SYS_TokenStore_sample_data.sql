-- SYS_TokenStore (トークン管理) サンプルデータ
-- 生成日時: 2025-06-21 22:02:17

INSERT INTO SYS_TokenStore (
    tokenstore_id, created_at, updated_at, id,
    is_deleted
) VALUES
    (NULL, NULL, NULL, 'TS001',
     NULL),
    (NULL, NULL, NULL, 'TS002',
     NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM SYS_TokenStore ORDER BY created_at DESC;
