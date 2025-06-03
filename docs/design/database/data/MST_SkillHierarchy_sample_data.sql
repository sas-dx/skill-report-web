-- MST_SkillHierarchy (スキル階層マスタ) サンプルデータ
-- 生成日時: 2025-06-04 06:57:02

INSERT INTO MST_SkillHierarchy (
    skill_id, parent_skill_id, hierarchy_level, skill_path,
    sort_order, is_leaf, skill_category, description,
    is_active, code, name
) VALUES
    ('SKILL_TECH_001', NULL, 1, '/技術スキル',
     1, FALSE, 'TECHNICAL', '技術系スキルの大分類',
     TRUE, NULL, NULL),
    ('SKILL_PROG_001', 'SKILL_TECH_001', 2, '/技術スキル/プログラミング',
     1, FALSE, 'TECHNICAL', 'プログラミング言語・技術',
     TRUE, NULL, NULL),
    ('SKILL_JAVA_001', 'SKILL_PROG_001', 3, '/技術スキル/プログラミング/Java',
     1, TRUE, 'TECHNICAL', 'Java言語でのプログラミングスキル',
     TRUE, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_SkillHierarchy ORDER BY created_at DESC;
