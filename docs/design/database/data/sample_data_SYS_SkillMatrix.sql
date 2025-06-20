-- サンプルデータ INSERT文: SYS_SkillMatrix
-- 生成日時: 2025-06-21 07:31:30
-- レコード数: 2

BEGIN;

INSERT INTO SYS_SkillMatrix (employee_id, skill_id, skill_level, self_assessment, manager_assessment, peer_assessment, assessment_date, evidence_url, notes, next_target_level, target_date, id, created_at, updated_at, is_deleted) VALUES ('EMP001', 'SKILL001', 3, 3, 3, 2, '2024-01-15', 'https://example.com/project/web-app', 'Webアプリケーション開発プロジェクトでReactを使用', 4, '2024-06-30', 'sys_df80cf6c', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO SYS_SkillMatrix (employee_id, skill_id, skill_level, self_assessment, manager_assessment, peer_assessment, assessment_date, evidence_url, notes, next_target_level, target_date, id, created_at, updated_at, is_deleted) VALUES ('EMP001', 'SKILL002', 2, 2, 2, 3, '2024-01-15', NULL, '基本的なPython開発は可能、フレームワーク経験が少ない', 3, '2024-09-30', 'sys_8e4c8ae9', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);

COMMIT;

-- SYS_SkillMatrix サンプルデータ終了
