-- ============================================
-- テーブル: MST_SkillGrade
-- 論理名: スキルグレードマスタ
-- 説明: MST_SkillGrade（スキルグレードマスタ）は、スキルの習熟度レベルを定義・管理するマスタテーブルです。

主な目的：
- スキル習熟度の標準化・統一
- スキル評価基準の明確化
- 職種別スキル要件の定義基盤
- スキル成長パスの可視化
- 人材育成計画の策定支援

このテーブルにより、組織全体で統一されたスキル評価基準を確立し、
社員のスキル開発と適切な人材配置を効率的に行うことができます。

-- 作成日: 2025-06-21 17:20:34
-- ============================================

DROP TABLE IF EXISTS MST_SkillGrade;

CREATE TABLE MST_SkillGrade (
    grade_code VARCHAR,
    grade_name VARCHAR,
    grade_name_short VARCHAR,
    grade_level INTEGER,
    description TEXT,
    evaluation_criteria TEXT,
    required_experience_months INTEGER,
    skill_indicators TEXT,
    competency_requirements TEXT,
    certification_requirements TEXT,
    project_complexity ENUM,
    mentoring_capability BOOLEAN DEFAULT False,
    leadership_level ENUM,
    salary_impact_factor DECIMAL,
    promotion_eligibility BOOLEAN DEFAULT False,
    color_code VARCHAR,
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT True,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_grade_code ON MST_SkillGrade (grade_code);
CREATE UNIQUE INDEX idx_grade_level ON MST_SkillGrade (grade_level);
CREATE INDEX idx_grade_name ON MST_SkillGrade (grade_name);
CREATE INDEX idx_mentoring ON MST_SkillGrade (mentoring_capability, is_active);
CREATE INDEX idx_promotion ON MST_SkillGrade (promotion_eligibility, is_active);
CREATE INDEX idx_sort_order ON MST_SkillGrade (sort_order);
