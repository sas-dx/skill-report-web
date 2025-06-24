-- MST_JobTypeSkill (職種スキル関連) サンプルデータ
-- 生成日時: 2025-06-24 23:02:18

INSERT INTO MST_JobTypeSkill (
    id, tenant_id, alternative_skills, certification_required,
    effective_date, evaluation_criteria, experience_years, expiry_date,
    job_type_id, jobtypeskill_id, learning_path, prerequisite_skills,
    required_level, skill_category, skill_item_id, skill_priority,
    skill_status, skill_weight, is_deleted, created_at,
    updated_at
) VALUES
    (NULL, NULL, '["SKILL002", "SKILL003"]', TRUE,
     '2025-01-01', '実務プロジェクトでの設計・実装経験、コードレビュー能力', 3.0, NULL,
     'JOB001', NULL, '基礎研修→実践プロジェクト→上級研修→資格取得', '["SKILL010", "SKILL011"]',
     4, 'TECHNICAL', 'SKILL001', 'CRITICAL',
     'ACTIVE', 25.0, NULL, NULL,
     NULL),
    (NULL, NULL, '["SKILL004"]', FALSE,
     '2025-01-01', '業務要件の理解度、顧客とのコミュニケーション能力', 2.0, NULL,
     'JOB001', NULL, '業務知識研修→OJT→実践経験', '["SKILL012"]',
     3, 'BUSINESS', 'SKILL002', 'HIGH',
     'ACTIVE', 20.0, NULL, NULL,
     NULL),
    (NULL, NULL, NULL, TRUE,
     '2025-01-01', 'チーム運営実績、プロジェクト成功率、メンバー育成実績', 5.0, NULL,
     'JOB002', NULL, 'リーダーシップ研修→実践経験→管理職研修→資格取得', '["SKILL001", "SKILL002"]',
     5, 'MANAGEMENT', 'SKILL003', 'CRITICAL',
     'ACTIVE', 30.0, NULL, NULL,
     NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_JobTypeSkill ORDER BY created_at DESC;
