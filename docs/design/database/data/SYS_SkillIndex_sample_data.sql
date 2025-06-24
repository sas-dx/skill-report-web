-- SYS_SkillIndex (スキル検索インデックス) サンプルデータ
-- 生成日時: 2025-06-24 22:56:15

INSERT INTO SYS_SkillIndex (
    id, tenant_id, frequency_weight, index_type,
    index_updated_at, is_active, language_code, last_searched_at,
    normalized_term, position_weight, relevance_score, search_count,
    search_term, skill_id, skillindex_id, source_field,
    is_deleted, created_at, updated_at
) VALUES
    ('SI001', 'TENANT001', 1.0, 'FULLTEXT',
     '2025-06-01 10:00:00', TRUE, 'ja', '2025-06-01 18:30:00',
     'java', 1.0, 1.0, 150,
     'Java', 'SKILL001', NULL, 'NAME',
     NULL, NULL, NULL),
    ('SI002', 'TENANT001', 0.75, 'KEYWORD',
     '2025-06-01 10:00:00', TRUE, 'ja', '2025-06-01 17:45:00',
     'プログラミング', 0.9, 0.8, 85,
     'プログラミング', 'SKILL001', NULL, 'DESCRIPTION',
     NULL, NULL, NULL),
    ('SI003', 'TENANT001', 0.5, 'SYNONYM',
     '2025-06-01 10:00:00', TRUE, 'ja', '2025-06-01 16:20:00',
     'ジャバ', 1.0, 0.9, 25,
     'ジャバ', 'SKILL001', NULL, 'KEYWORD',
     NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM SYS_SkillIndex ORDER BY created_at DESC;
