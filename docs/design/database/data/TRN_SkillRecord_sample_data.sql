-- TRN_SkillRecord (スキル情報) サンプルデータ
-- 生成日時: 2025-06-24 23:05:57

INSERT INTO TRN_SkillRecord (
    id, tenant_id, acquisition_date, assessment_date,
    assessor_id, certification_id, employee_id, evidence_description,
    expiry_date, last_used_date, learning_hours, manager_assessment,
    project_experience_count, self_assessment, skill_category_id, skill_item_id,
    skill_level, skill_status, skillrecord_id, is_deleted,
    created_at, created_by, updated_by, updated_at
) VALUES
    (NULL, NULL, '2020-06-01', '2025-04-01',
     'EMP000010', 'CERT001', 'EMP000001', 'Javaを使用したWebアプリケーション開発プロジェクトを3件担当',
     NULL, '2025-05-30', 120, 3,
     3, 4, 'CAT001', 'SKILL001',
     4, 'ACTIVE', NULL, NULL,
     NULL, NULL, NULL, NULL),
    (NULL, NULL, '2021-03-15', '2025-04-01',
     'EMP000010', 'CERT002', 'EMP000001', 'AWS環境でのインフラ構築・運用経験',
     '2026-03-15', '2025-05-25', 80, 3,
     2, 3, 'CAT002', 'SKILL002',
     3, 'ACTIVE', NULL, NULL,
     NULL, NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM TRN_SkillRecord ORDER BY created_at DESC;
