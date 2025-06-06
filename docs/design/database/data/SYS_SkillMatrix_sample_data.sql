-- SYS_SkillMatrix (スキルマップ) サンプルデータ
-- 生成日時: 2025-06-04 06:57:02

INSERT INTO SYS_SkillMatrix (
    employee_id, skill_id, skill_level, self_assessment,
    manager_assessment, peer_assessment, assessment_date, evidence_url,
    notes, next_target_level, target_date, id,
    is_deleted
) VALUES
    ('EMP001', 'SKILL001', 3, 3,
     3, 2, '2024-01-15', 'https://example.com/project/web-app',
     'Webアプリケーション開発プロジェクトでReactを使用', 4, '2024-06-30', NULL,
     NULL),
    ('EMP001', 'SKILL002', 2, 2,
     2, 3, '2024-01-15', NULL,
     '基本的なPython開発は可能、フレームワーク経験が少ない', 3, '2024-09-30', NULL,
     NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM SYS_SkillMatrix ORDER BY created_at DESC;
