-- ============================================
-- テーブル: MST_SkillGrade
-- 論理名: スキルグレードマスタ
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_SkillGrade;

CREATE TABLE MST_SkillGrade (
    grade_code VARCHAR(20) COMMENT 'スキルグレードを一意に識別するコード（例：BEGINNER、INTERMEDIATE、ADVANCED、EXPERT）',
    grade_name VARCHAR(50) COMMENT 'スキルグレードの名称',
    grade_name_short VARCHAR(10) COMMENT '表示用の短縮名称（例：初級、中級、上級、専門）',
    grade_level INTEGER COMMENT 'グレードの数値レベル（1:初級、2:中級、3:上級、4:専門、5:エキスパート）',
    description TEXT COMMENT 'スキルグレードの詳細説明・到達基準',
    evaluation_criteria TEXT COMMENT 'グレード判定のための具体的な評価基準',
    required_experience_months INTEGER COMMENT 'グレード到達に必要な経験期間の目安（月数）',
    skill_indicators TEXT COMMENT 'グレード判定のためのスキル指標（JSON形式）',
    competency_requirements TEXT COMMENT 'グレードに求められる能力・知識要件（JSON形式）',
    certification_requirements TEXT COMMENT 'グレード認定に必要な資格（JSON形式）',
    project_complexity ENUM COMMENT '担当可能なプロジェクトの複雑度（SIMPLE:単純、MODERATE:中程度、COMPLEX:複雑、CRITICAL:重要）',
    mentoring_capability BOOLEAN DEFAULT False COMMENT '他者への指導・メンタリング能力があるか',
    leadership_level ENUM COMMENT '発揮できるリーダーシップレベル（NONE:なし、TEAM:チーム、PROJECT:プロジェクト、ORGANIZATION:組織）',
    salary_impact_factor DECIMAL(3,2) COMMENT '給与計算への影響係数（1.0を基準とした倍率）',
    promotion_eligibility BOOLEAN DEFAULT False COMMENT '昇進要件として考慮されるグレードか',
    color_code VARCHAR(7) COMMENT 'UI表示用の色コード（例：#FF0000）',
    sort_order INTEGER DEFAULT 0 COMMENT 'グレード一覧での表示順序',
    is_active BOOLEAN DEFAULT True COMMENT 'グレードが有効かどうか',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_grade_code ON MST_SkillGrade (grade_code);
CREATE UNIQUE INDEX idx_grade_level ON MST_SkillGrade (grade_level);
CREATE INDEX idx_grade_name ON MST_SkillGrade (grade_name);
CREATE INDEX idx_mentoring ON MST_SkillGrade (mentoring_capability, is_active);
CREATE INDEX idx_promotion ON MST_SkillGrade (promotion_eligibility, is_active);
CREATE INDEX idx_sort_order ON MST_SkillGrade (sort_order);

-- その他の制約
ALTER TABLE MST_SkillGrade ADD CONSTRAINT uk_grade_code UNIQUE ();
ALTER TABLE MST_SkillGrade ADD CONSTRAINT uk_grade_level UNIQUE ();
ALTER TABLE MST_SkillGrade ADD CONSTRAINT chk_grade_level CHECK (grade_level >= 1 AND grade_level <= 5);
ALTER TABLE MST_SkillGrade ADD CONSTRAINT chk_project_complexity CHECK (project_complexity IN ('SIMPLE', 'MODERATE', 'COMPLEX', 'CRITICAL'));
ALTER TABLE MST_SkillGrade ADD CONSTRAINT chk_leadership_level CHECK (leadership_level IN ('NONE', 'TEAM', 'PROJECT', 'ORGANIZATION'));
ALTER TABLE MST_SkillGrade ADD CONSTRAINT chk_experience_months CHECK (required_experience_months IS NULL OR required_experience_months >= 0);
ALTER TABLE MST_SkillGrade ADD CONSTRAINT chk_salary_factor CHECK (salary_impact_factor IS NULL OR salary_impact_factor > 0);
