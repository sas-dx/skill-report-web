-- MST_JobTypeSkillGrade (職種スキルグレード関連) サンプルデータ
-- 生成日時: 2025-06-04 06:57:02

INSERT INTO MST_JobTypeSkillGrade (
    job_type_id, skill_grade_id, grade_requirement_type, required_experience_years,
    promotion_criteria, salary_range_min, salary_range_max, performance_expectations,
    leadership_requirements, technical_depth, business_impact, team_size_expectation,
    certification_requirements, grade_status, effective_date, expiry_date,
    next_grade_path, evaluation_frequency, code, name,
    description
) VALUES
    ('JOB001', 'GRADE001', 'MINIMUM', 0.0,
     '基礎研修修了、OJT完了、基本業務遂行能力', 3000000, 4000000, '指導の下での基本業務遂行、学習意欲の継続',
     'チームワーク、積極的な学習姿勢', 2, 2, 0,
     '["基本情報技術者試験"]', 'ACTIVE', '2025-01-01', NULL,
     '["GRADE002"]', 'SEMI_ANNUAL', NULL, NULL,
     NULL),
    ('JOB001', 'GRADE002', 'STANDARD', 2.0,
     '独立した業務遂行、技術スキル向上、プロジェクト貢献', 4000000, 5500000, '独立した業務遂行、品質向上への貢献、後輩指導',
     '後輩指導、技術的リーダーシップ', 4, 4, 2,
     '["応用情報技術者試験", "専門資格1つ以上"]', 'ACTIVE', '2025-01-01', NULL,
     '["GRADE003"]', 'ANNUAL', NULL, NULL,
     NULL),
    ('JOB002', 'GRADE003', 'ADVANCED', 5.0,
     'チーム運営実績、技術的専門性、事業貢献度', 6000000, 8000000, 'チーム運営、技術戦略立案、事業成果創出',
     'チームマネジメント、技術戦略、人材育成', 7, 7, 5,
     '["高度情報技術者試験", "マネジメント資格", "専門資格2つ以上"]', 'ACTIVE', '2025-01-01', NULL,
     '["GRADE004", "GRADE005"]', 'ANNUAL', NULL, NULL,
     NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_JobTypeSkillGrade ORDER BY created_at DESC;
