-- MST_SkillItem (スキル項目マスタ) サンプルデータ
-- 生成日時: 2025-06-24 23:02:18

INSERT INTO MST_SkillItem (
    id, tenant_id, skill_code, skill_name,
    difficulty_level, importance_level, skill_category_id, skill_type,
    skillitem_id, is_deleted, created_at, updated_at
) VALUES
    (NULL, NULL, 'SKILL001', 'Java',
     3, 4, 'CAT001', 'TECHNICAL',
     NULL, NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_SkillItem ORDER BY created_at DESC;
