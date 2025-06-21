-- MST_SkillGrade (スキルグレードマスタ) サンプルデータ
-- 生成日時: 2025-06-21 17:20:34

INSERT INTO MST_SkillGrade (
    grade_code, grade_name, grade_name_short, grade_level,
    description, evaluation_criteria, required_experience_months, skill_indicators,
    competency_requirements, certification_requirements, project_complexity, mentoring_capability,
    leadership_level, salary_impact_factor, promotion_eligibility, color_code,
    sort_order, is_active, created_at, updated_at
) VALUES
    ('BEGINNER', '初級', '初級', 1,
     '基本的な知識を持ち、指導の下で業務を遂行できるレベル', '基本概念の理解、簡単なタスクの実行、指導者のサポートが必要', 6, '["基本知識", "指導下での作業", "学習意欲"]',
     '["基礎理論の理解", "基本操作の習得"]', '[]', 'SIMPLE', FALSE,
     'NONE', 1.0, FALSE, '#90EE90',
     1, TRUE, NULL, NULL),
    ('INTERMEDIATE', '中級', '中級', 2,
     '一般的な業務を独立して遂行でき、部分的に他者を指導できるレベル', '独立した作業遂行、問題解決能力、基本的な指導スキル', 18, '["独立作業", "問題解決", "基本指導"]',
     '["実践的スキル", "問題分析能力", "コミュニケーション能力"]', '["基本情報技術者"]', 'MODERATE', TRUE,
     'TEAM', 1.2, TRUE, '#FFD700',
     2, TRUE, NULL, NULL),
    ('ADVANCED', '上級', '上級', 3,
     '複雑な業務をリードし、チーム全体の技術指導ができるレベル', '高度な技術力、リーダーシップ、戦略的思考', 36, '["高度技術", "リーダーシップ", "戦略思考"]',
     '["専門技術", "チーム管理", "技術戦略立案"]', '["応用情報技術者", "専門資格"]', 'COMPLEX', TRUE,
     'PROJECT', 1.5, TRUE, '#FF8C00',
     3, TRUE, NULL, NULL),
    ('EXPERT', '専門家', '専門', 4,
     '組織全体の技術方針に影響を与え、業界レベルでの専門性を持つレベル', '業界専門性、組織への影響力、イノベーション創出', 60, '["業界専門性", "組織影響力", "イノベーション"]',
     '["業界知識", "組織運営", "技術革新"]', '["高度情報技術者", "業界認定資格"]', 'CRITICAL', TRUE,
     'ORGANIZATION', 2.0, TRUE, '#DC143C',
     4, TRUE, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_SkillGrade ORDER BY created_at DESC;
