-- ============================================
-- テーブル: MST_JobTypeSkillGrade
-- 論理名: 職種スキルグレード関連
-- 説明: MST_JobTypeSkillGrade（職種スキルグレード関連）は、職種とスキルグレードの関連付けを管理するマスタテーブルです。

主な目的：
- 職種ごとの必要スキルグレードの定義
- 昇進・昇格要件の明確化
- キャリアパス設計の基礎データ
- 人材評価基準の標準化
- 給与体系との連動管理
- 教育計画の目標設定

このテーブルにより、各職種に求められるスキルグレードを明確に定義し、
人材育成や昇進管理の判断基準として活用できます。

-- 作成日: 2025-06-21 17:20:33
-- ============================================

DROP TABLE IF EXISTS MST_JobTypeSkillGrade;

CREATE TABLE MST_JobTypeSkillGrade (
    job_type_id VARCHAR,
    skill_grade_id VARCHAR,
    grade_requirement_type ENUM DEFAULT 'STANDARD',
    required_experience_years DECIMAL,
    promotion_criteria TEXT,
    salary_range_min DECIMAL,
    salary_range_max DECIMAL,
    performance_expectations TEXT,
    leadership_requirements TEXT,
    technical_depth INTEGER,
    business_impact INTEGER,
    team_size_expectation INTEGER,
    certification_requirements TEXT,
    grade_status ENUM DEFAULT 'ACTIVE',
    effective_date DATE,
    expiry_date DATE,
    next_grade_path TEXT,
    evaluation_frequency ENUM DEFAULT 'ANNUAL',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_MST_JobTypeSkillGrade_job_type_id ON MST_JobTypeSkillGrade (job_type_id);
CREATE INDEX idx_MST_JobTypeSkillGrade_skill_grade_id ON MST_JobTypeSkillGrade (skill_grade_id);
CREATE UNIQUE INDEX idx_MST_JobTypeSkillGrade_job_grade ON MST_JobTypeSkillGrade (job_type_id, skill_grade_id);
CREATE INDEX idx_MST_JobTypeSkillGrade_requirement_type ON MST_JobTypeSkillGrade (grade_requirement_type);
CREATE INDEX idx_MST_JobTypeSkillGrade_experience_years ON MST_JobTypeSkillGrade (required_experience_years);
CREATE INDEX idx_MST_JobTypeSkillGrade_status ON MST_JobTypeSkillGrade (grade_status);
CREATE INDEX idx_MST_JobTypeSkillGrade_effective_date ON MST_JobTypeSkillGrade (effective_date);
CREATE INDEX idx_MST_JobTypeSkillGrade_technical_depth ON MST_JobTypeSkillGrade (technical_depth);
