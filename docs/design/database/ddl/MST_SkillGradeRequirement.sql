-- ============================================
-- テーブル: MST_SkillGradeRequirement
-- 論理名: スキルグレード要件
-- 説明: MST_SkillGradeRequirement（スキルグレード要件）は、スキルグレードごとの詳細要件を管理するマスタテーブルです。

主な目的：
- スキルグレード別の詳細要件定義
- 昇格基準の明確化
- 評価項目の標準化
- 学習目標の設定
- 能力開発計画の基礎データ
- 人材評価の客観化

このテーブルにより、各スキルグレードに求められる具体的な要件を明確に定義し、
公正で透明性の高い人材評価・育成システムを構築できます。

-- 作成日: 2025-06-21 17:20:34
-- ============================================

DROP TABLE IF EXISTS MST_SkillGradeRequirement;

CREATE TABLE MST_SkillGradeRequirement (
    skill_grade_id VARCHAR,
    requirement_category ENUM,
    requirement_name VARCHAR,
    requirement_description TEXT,
    evaluation_criteria TEXT,
    proficiency_level INTEGER,
    weight_percentage DECIMAL,
    minimum_score DECIMAL,
    evidence_requirements TEXT,
    learning_resources TEXT,
    prerequisite_requirements TEXT,
    assessment_method ENUM,
    assessment_frequency ENUM DEFAULT 'ANNUAL',
    validity_period INTEGER,
    certification_mapping TEXT,
    requirement_status ENUM DEFAULT 'ACTIVE',
    effective_date DATE,
    expiry_date DATE,
    revision_notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_MST_SkillGradeRequirement_skill_grade_id ON MST_SkillGradeRequirement (skill_grade_id);
CREATE INDEX idx_MST_SkillGradeRequirement_category ON MST_SkillGradeRequirement (requirement_category);
CREATE INDEX idx_MST_SkillGradeRequirement_grade_category ON MST_SkillGradeRequirement (skill_grade_id, requirement_category);
CREATE INDEX idx_MST_SkillGradeRequirement_proficiency_level ON MST_SkillGradeRequirement (proficiency_level);
CREATE INDEX idx_MST_SkillGradeRequirement_assessment_method ON MST_SkillGradeRequirement (assessment_method);
CREATE INDEX idx_MST_SkillGradeRequirement_status ON MST_SkillGradeRequirement (requirement_status);
CREATE INDEX idx_MST_SkillGradeRequirement_effective_date ON MST_SkillGradeRequirement (effective_date);
CREATE INDEX idx_MST_SkillGradeRequirement_weight ON MST_SkillGradeRequirement (weight_percentage);
