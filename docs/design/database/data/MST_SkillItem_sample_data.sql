-- MST_SkillItem (スキル項目マスタ) サンプルデータ
-- 生成日時: 2025-06-21 17:20:34

INSERT INTO MST_SkillItem (
    skill_code, skill_name, skill_category_id, skill_type,
    difficulty_level, importance_level, created_at, updated_at
) VALUES
    ('SKILL001', 'Java', 'CAT001', 'TECHNICAL',
     3, 4, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_SkillItem ORDER BY created_at DESC;
