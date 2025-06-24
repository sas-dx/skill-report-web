-- MST_SkillCategory (スキルカテゴリマスタ) サンプルデータ
-- 生成日時: 2025-06-24 22:56:16

INSERT INTO MST_SkillCategory (
    id, tenant_id, category_code, category_name,
    category_level, category_name_en, category_name_short, category_path,
    category_status, category_type, color_code, description,
    display_order, effective_from, effective_to, evaluation_method,
    icon_url, is_leaf_category, is_popular, is_system_category,
    max_level, parent_category_id, skill_count, skillcategory_id,
    is_deleted, created_at, updated_at
) VALUES
    (NULL, NULL, 'CAT001', 'プログラミング言語',
     1, 'Programming Languages', 'プログラミング', '/プログラミング言語',
     'ACTIVE', 'TECHNICAL', '#007ACC', '各種プログラミング言語のスキル',
     1, '2025-01-01', NULL, 'LEVEL',
     '/icons/programming.svg', FALSE, TRUE, TRUE,
     5, NULL, 25, NULL,
     NULL, NULL, NULL),
    (NULL, NULL, 'CAT002', 'Java',
     2, 'Java', 'Java', '/プログラミング言語/Java',
     'ACTIVE', 'TECHNICAL', '#ED8B00', 'Java言語に関するスキル',
     1, '2025-01-01', NULL, 'LEVEL',
     '/icons/java.svg', TRUE, TRUE, TRUE,
     5, 'CAT001', 8, NULL,
     NULL, NULL, NULL),
    (NULL, NULL, 'CAT003', 'コミュニケーション',
     1, 'Communication', 'コミュニケーション', '/コミュニケーション',
     'ACTIVE', 'SOFT', '#28A745', 'コミュニケーション能力に関するスキル',
     10, '2025-01-01', NULL, 'LEVEL',
     '/icons/communication.svg', TRUE, TRUE, TRUE,
     4, NULL, 12, NULL,
     NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_SkillCategory ORDER BY created_at DESC;
