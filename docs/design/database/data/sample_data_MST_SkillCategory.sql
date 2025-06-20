-- サンプルデータ INSERT文: MST_SkillCategory
-- 生成日時: 2025-06-21 07:31:30
-- レコード数: 3

BEGIN;

INSERT INTO MST_SkillCategory (category_code, category_name, category_name_short, category_name_en, category_type, parent_category_id, category_level, category_path, is_system_category, is_leaf_category, skill_count, evaluation_method, max_level, icon_url, color_code, display_order, is_popular, category_status, effective_from, effective_to, description, id, created_at, updated_at, is_deleted) VALUES ('CAT001', 'プログラミング言語', 'プログラミング', 'Programming Languages', 'TECHNICAL', NULL, 1, '/プログラミング言語', TRUE, FALSE, 25, 'LEVEL', 5, '/icons/programming.svg', '#007ACC', 1, TRUE, 'ACTIVE', '2025-01-01', NULL, '各種プログラミング言語のスキル', 'mst_d8124366', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO MST_SkillCategory (category_code, category_name, category_name_short, category_name_en, category_type, parent_category_id, category_level, category_path, is_system_category, is_leaf_category, skill_count, evaluation_method, max_level, icon_url, color_code, display_order, is_popular, category_status, effective_from, effective_to, description, id, created_at, updated_at, is_deleted) VALUES ('CAT002', 'Java', 'Java', 'Java', 'TECHNICAL', 'CAT001', 2, '/プログラミング言語/Java', TRUE, TRUE, 8, 'LEVEL', 5, '/icons/java.svg', '#ED8B00', 1, TRUE, 'ACTIVE', '2025-01-01', NULL, 'Java言語に関するスキル', 'mst_4d3c5a89', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO MST_SkillCategory (category_code, category_name, category_name_short, category_name_en, category_type, parent_category_id, category_level, category_path, is_system_category, is_leaf_category, skill_count, evaluation_method, max_level, icon_url, color_code, display_order, is_popular, category_status, effective_from, effective_to, description, id, created_at, updated_at, is_deleted) VALUES ('CAT003', 'コミュニケーション', 'コミュニケーション', 'Communication', 'SOFT', NULL, 1, '/コミュニケーション', TRUE, TRUE, 12, 'LEVEL', 4, '/icons/communication.svg', '#28A745', 10, TRUE, 'ACTIVE', '2025-01-01', NULL, 'コミュニケーション能力に関するスキル', 'mst_37025fcd', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);

COMMIT;

-- MST_SkillCategory サンプルデータ終了
