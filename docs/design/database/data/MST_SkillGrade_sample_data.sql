-- MST_SkillGrade (スキルグレードマスタ) サンプルデータ
-- 生成日時: 2025-06-24 23:02:18

INSERT INTO MST_SkillGrade (
    id, tenant_id, grade_code, grade_name,
    certification_requirements, color_code, competency_requirements, description,
    evaluation_criteria, grade_level, grade_name_short, is_active,
    leadership_level, mentoring_capability, project_complexity, promotion_eligibility,
    required_experience_months, salary_impact_factor, skill_indicators, skillgrade_id,
    sort_order, is_deleted, created_at, updated_at
) VALUES
    (NULL, NULL, 'BEGINNER', '初級',
     '[]', '#90EE90', '["基礎理論の理解", "基本操作の習得"]', '基本的な知識を持ち、指導の下で業務を遂行できるレベル',
     '基本概念の理解、簡単なタスクの実行、指導者のサポートが必要', 1, '初級', TRUE,
     'NONE', FALSE, 'SIMPLE', FALSE,
     6, 1.0, '["基本知識", "指導下での作業", "学習意欲"]', NULL,
     1, NULL, NULL, NULL),
    (NULL, NULL, 'INTERMEDIATE', '中級',
     '["基本情報技術者"]', '#FFD700', '["実践的スキル", "問題分析能力", "コミュニケーション能力"]', '一般的な業務を独立して遂行でき、部分的に他者を指導できるレベル',
     '独立した作業遂行、問題解決能力、基本的な指導スキル', 2, '中級', TRUE,
     'TEAM', TRUE, 'MODERATE', TRUE,
     18, 1.2, '["独立作業", "問題解決", "基本指導"]', NULL,
     2, NULL, NULL, NULL),
    (NULL, NULL, 'ADVANCED', '上級',
     '["応用情報技術者", "専門資格"]', '#FF8C00', '["専門技術", "チーム管理", "技術戦略立案"]', '複雑な業務をリードし、チーム全体の技術指導ができるレベル',
     '高度な技術力、リーダーシップ、戦略的思考', 3, '上級', TRUE,
     'PROJECT', TRUE, 'COMPLEX', TRUE,
     36, 1.5, '["高度技術", "リーダーシップ", "戦略思考"]', NULL,
     3, NULL, NULL, NULL),
    (NULL, NULL, 'EXPERT', '専門家',
     '["高度情報技術者", "業界認定資格"]', '#DC143C', '["業界知識", "組織運営", "技術革新"]', '組織全体の技術方針に影響を与え、業界レベルでの専門性を持つレベル',
     '業界専門性、組織への影響力、イノベーション創出', 4, '専門', TRUE,
     'ORGANIZATION', TRUE, 'CRITICAL', TRUE,
     60, 2.0, '["業界専門性", "組織影響力", "イノベーション"]', NULL,
     4, NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_SkillGrade ORDER BY created_at DESC;
