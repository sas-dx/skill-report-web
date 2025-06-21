-- サンプルデータ INSERT文: MST_SkillHierarchy
-- 生成日時: 2025-06-21 17:21:42
-- レコード数: 3

INSERT INTO MST_SkillHierarchy (skill_id, parent_skill_id, hierarchy_level, skill_path, sort_order, is_leaf, skill_category, description, is_active, id, created_at, updated_at, is_deleted) VALUES ('SKILL_TECH_001', NULL, 1, '/技術スキル', 1, FALSE, 'TECHNICAL', '技術系スキルの大分類', TRUE, 'mst_21fb6479', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO MST_SkillHierarchy (skill_id, parent_skill_id, hierarchy_level, skill_path, sort_order, is_leaf, skill_category, description, is_active, id, created_at, updated_at, is_deleted) VALUES ('SKILL_PROG_001', 'SKILL_TECH_001', 2, '/技術スキル/プログラミング', 1, FALSE, 'TECHNICAL', 'プログラミング言語・技術', TRUE, 'mst_9635113c', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO MST_SkillHierarchy (skill_id, parent_skill_id, hierarchy_level, skill_path, sort_order, is_leaf, skill_category, description, is_active, id, created_at, updated_at, is_deleted) VALUES ('SKILL_JAVA_001', 'SKILL_PROG_001', 3, '/技術スキル/プログラミング/Java', 1, TRUE, 'TECHNICAL', 'Java言語でのプログラミングスキル', TRUE, 'mst_fb0f7456', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);

-- MST_SkillHierarchy サンプルデータ終了
