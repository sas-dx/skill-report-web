-- TRN_SkillRecord (スキル情報) サンプルデータ
-- 生成日時: 2025-06-21 17:20:34

INSERT INTO TRN_SkillRecord (
    employee_id, skill_item_id, skill_level, self_assessment,
    manager_assessment, evidence_description, acquisition_date, last_used_date,
    expiry_date, certification_id, skill_category_id, assessment_date,
    assessor_id, skill_status, learning_hours, project_experience_count,
    id, is_deleted, created_by, updated_by,
    created_at, updated_at
) VALUES
    ('EMP000001', 'SKILL001', 4, 4,
     3, 'Javaを使用したWebアプリケーション開発プロジェクトを3件担当', '2020-06-01', '2025-05-30',
     NULL, 'CERT001', 'CAT001', '2025-04-01',
     'EMP000010', 'ACTIVE', 120, 3,
     NULL, NULL, NULL, NULL,
     NULL, NULL),
    ('EMP000001', 'SKILL002', 3, 3,
     3, 'AWS環境でのインフラ構築・運用経験', '2021-03-15', '2025-05-25',
     '2026-03-15', 'CERT002', 'CAT002', '2025-04-01',
     'EMP000010', 'ACTIVE', 80, 2,
     NULL, NULL, NULL, NULL,
     NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM TRN_SkillRecord ORDER BY created_at DESC;
