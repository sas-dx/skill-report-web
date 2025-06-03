-- MST_JobTypeSkill (職種スキル関連) サンプルデータ
-- 生成日時: 2025-06-04 06:57:02

INSERT INTO MST_JobTypeSkill (
    job_type_id, skill_item_id, required_level, skill_priority,
    skill_category, experience_years, certification_required, skill_weight,
    evaluation_criteria, learning_path, skill_status, effective_date,
    expiry_date, alternative_skills, prerequisite_skills, code,
    name, description
) VALUES
    ('JOB001', 'SKILL001', 4, 'CRITICAL',
     'TECHNICAL', 3.0, TRUE, 25.0,
     '実務プロジェクトでの設計・実装経験、コードレビュー能力', '基礎研修→実践プロジェクト→上級研修→資格取得', 'ACTIVE', '2025-01-01',
     NULL, '["SKILL002", "SKILL003"]', '["SKILL010", "SKILL011"]', NULL,
     NULL, NULL),
    ('JOB001', 'SKILL002', 3, 'HIGH',
     'BUSINESS', 2.0, FALSE, 20.0,
     '業務要件の理解度、顧客とのコミュニケーション能力', '業務知識研修→OJT→実践経験', 'ACTIVE', '2025-01-01',
     NULL, '["SKILL004"]', '["SKILL012"]', NULL,
     NULL, NULL),
    ('JOB002', 'SKILL003', 5, 'CRITICAL',
     'MANAGEMENT', 5.0, TRUE, 30.0,
     'チーム運営実績、プロジェクト成功率、メンバー育成実績', 'リーダーシップ研修→実践経験→管理職研修→資格取得', 'ACTIVE', '2025-01-01',
     NULL, NULL, '["SKILL001", "SKILL002"]', NULL,
     NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_JobTypeSkill ORDER BY created_at DESC;
