-- SYS_SkillMatrix (スキルマップ) サンプルデータ
-- 生成日時: 2025-06-24 22:56:16

INSERT INTO SYS_SkillMatrix (
    id, assessment_date, employee_id, evidence_url,
    manager_assessment, next_target_level, notes, peer_assessment,
    self_assessment, skill_id, skill_level, skillmatrix_id,
    target_date, is_deleted, created_at, updated_at
) VALUES
    (NULL, '2024-01-15', 'EMP001', 'https://example.com/project/web-app',
     3, 4, 'Webアプリケーション開発プロジェクトでReactを使用', 2,
     3, 'SKILL001', 3, NULL,
     '2024-06-30', NULL, NULL, NULL),
    (NULL, '2024-01-15', 'EMP001', NULL,
     2, 3, '基本的なPython開発は可能、フレームワーク経験が少ない', 3,
     2, 'SKILL002', 2, NULL,
     '2024-09-30', NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM SYS_SkillMatrix ORDER BY created_at DESC;
