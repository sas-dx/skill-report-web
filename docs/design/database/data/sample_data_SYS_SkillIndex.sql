-- サンプルデータ INSERT文: SYS_SkillIndex
-- 生成日時: 2025-06-21 07:31:30
-- レコード数: 3

BEGIN;

INSERT INTO SYS_SkillIndex (id, tenant_id, skill_id, index_type, search_term, normalized_term, relevance_score, frequency_weight, position_weight, language_code, source_field, is_active, search_count, last_searched_at, index_updated_at, created_at, updated_at, is_deleted) VALUES ('SI001', 'TENANT001', 'SKILL001', 'FULLTEXT', 'Java', 'java', 1.0, 1.0, 1.0, 'ja', 'NAME', TRUE, 150, '2025-06-01 18:30:00', '2025-06-01 10:00:00', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO SYS_SkillIndex (id, tenant_id, skill_id, index_type, search_term, normalized_term, relevance_score, frequency_weight, position_weight, language_code, source_field, is_active, search_count, last_searched_at, index_updated_at, created_at, updated_at, is_deleted) VALUES ('SI002', 'TENANT001', 'SKILL001', 'KEYWORD', 'プログラミング', 'プログラミング', 0.8, 0.75, 0.9, 'ja', 'DESCRIPTION', TRUE, 85, '2025-06-01 17:45:00', '2025-06-01 10:00:00', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO SYS_SkillIndex (id, tenant_id, skill_id, index_type, search_term, normalized_term, relevance_score, frequency_weight, position_weight, language_code, source_field, is_active, search_count, last_searched_at, index_updated_at, created_at, updated_at, is_deleted) VALUES ('SI003', 'TENANT001', 'SKILL001', 'SYNONYM', 'ジャバ', 'ジャバ', 0.9, 0.5, 1.0, 'ja', 'KEYWORD', TRUE, 25, '2025-06-01 16:20:00', '2025-06-01 10:00:00', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);

COMMIT;

-- SYS_SkillIndex サンプルデータ終了
