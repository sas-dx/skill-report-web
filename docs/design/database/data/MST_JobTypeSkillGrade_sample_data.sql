-- MST_JobTypeSkillGrade (職種スキルグレード関連) サンプルデータ
-- 生成日時: 2025-06-24 23:05:57

INSERT INTO MST_JobTypeSkillGrade (
    id, tenant_id, business_impact, certification_requirements,
    effective_date, evaluation_frequency, expiry_date, grade_requirement_type,
    grade_status, job_type_id, jobtypeskillgrade_id, leadership_requirements,
    next_grade_path, performance_expectations, promotion_criteria, required_experience_years,
    salary_range_max, salary_range_min, skill_grade_id, team_size_expectation,
    technical_depth, is_deleted, created_at, updated_at
) VALUES
    (NULL, NULL, 2, '["基本情報技術者試験"]',
     '2025-01-01', 'SEMI_ANNUAL', NULL, 'MINIMUM',
     'ACTIVE', 'JOB001', NULL, 'チームワーク、積極的な学習姿勢',
     '["GRADE002"]', '指導の下での基本業務遂行、学習意欲の継続', '基礎研修修了、OJT完了、基本業務遂行能力', 0.0,
     4000000, 3000000, 'GRADE001', 0,
     2, NULL, NULL, NULL),
    (NULL, NULL, 4, '["応用情報技術者試験", "専門資格1つ以上"]',
     '2025-01-01', 'ANNUAL', NULL, 'STANDARD',
     'ACTIVE', 'JOB001', NULL, '後輩指導、技術的リーダーシップ',
     '["GRADE003"]', '独立した業務遂行、品質向上への貢献、後輩指導', '独立した業務遂行、技術スキル向上、プロジェクト貢献', 2.0,
     5500000, 4000000, 'GRADE002', 2,
     4, NULL, NULL, NULL),
    (NULL, NULL, 7, '["高度情報技術者試験", "マネジメント資格", "専門資格2つ以上"]',
     '2025-01-01', 'ANNUAL', NULL, 'ADVANCED',
     'ACTIVE', 'JOB002', NULL, 'チームマネジメント、技術戦略、人材育成',
     '["GRADE004", "GRADE005"]', 'チーム運営、技術戦略立案、事業成果創出', 'チーム運営実績、技術的専門性、事業貢献度', 5.0,
     8000000, 6000000, 'GRADE003', 5,
     7, NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_JobTypeSkillGrade ORDER BY created_at DESC;
