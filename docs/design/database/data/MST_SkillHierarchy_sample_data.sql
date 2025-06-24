-- MST_SkillHierarchy (スキル階層マスタ) サンプルデータ
-- 生成日時: 2025-06-24 23:05:56

INSERT INTO MST_SkillHierarchy (
    id, tenant_id, description, hierarchy_level,
    is_active, is_leaf, parent_skill_id, skill_category,
    skill_id, skill_path, skillhierarchy_id, sort_order,
    is_deleted, created_at, updated_at
) VALUES
    (NULL, NULL, '技術系スキルの大分類', 1,
     TRUE, FALSE, NULL, 'TECHNICAL',
     'SKILL_TECH_001', '/技術スキル', NULL, 1,
     NULL, NULL, NULL),
    (NULL, NULL, 'プログラミング言語・技術', 2,
     TRUE, FALSE, 'SKILL_TECH_001', 'TECHNICAL',
     'SKILL_PROG_001', '/技術スキル/プログラミング', NULL, 1,
     NULL, NULL, NULL),
    (NULL, NULL, 'Java言語でのプログラミングスキル', 3,
     TRUE, TRUE, 'SKILL_PROG_001', 'TECHNICAL',
     'SKILL_JAVA_001', '/技術スキル/プログラミング/Java', NULL, 1,
     NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_SkillHierarchy ORDER BY created_at DESC;
