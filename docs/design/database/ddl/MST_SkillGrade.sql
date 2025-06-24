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

-- 作成日: 2025-06-24 23:02:18
-- ============================================

DROP TABLE IF EXISTS MST_SkillGrade;

CREATE TABLE MST_SkillGrade (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    grade_code VARCHAR(20) COMMENT 'グレードコード',
    grade_name VARCHAR(50) COMMENT 'グレード名',
    certification_requirements TEXT COMMENT '資格要件',
    color_code VARCHAR(7) COMMENT '表示色コード',
    competency_requirements TEXT COMMENT '能力要件',
    description TEXT COMMENT 'グレード説明',
    evaluation_criteria TEXT COMMENT '評価基準',
    grade_level INTEGER COMMENT 'グレードレベル',
    grade_name_short VARCHAR(10) COMMENT 'グレード名（短縮）',
    is_active BOOLEAN DEFAULT True COMMENT '有効フラグ',
    leadership_level ENUM('NONE', 'TEAM', 'PROJECT', 'ORGANIZATION') COMMENT 'リーダーシップレベル',
    mentoring_capability BOOLEAN DEFAULT False COMMENT '指導能力',
    project_complexity ENUM('SIMPLE', 'MODERATE', 'COMPLEX', 'CRITICAL') COMMENT 'プロジェクト複雑度',
    promotion_eligibility BOOLEAN DEFAULT False COMMENT '昇進資格',
    required_experience_months INTEGER COMMENT '必要経験期間（月）',
    salary_impact_factor DECIMAL(3,2) COMMENT '給与影響係数',
    skill_indicators TEXT COMMENT 'スキル指標',
    skillgrade_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_SkillGradeの主キー',
    sort_order INTEGER DEFAULT 0 COMMENT '表示順序',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_grade_code ON MST_SkillGrade (grade_code);
CREATE UNIQUE INDEX idx_grade_level ON MST_SkillGrade (grade_level);
CREATE INDEX idx_grade_name ON MST_SkillGrade (grade_name);
CREATE INDEX idx_mentoring ON MST_SkillGrade (mentoring_capability, is_active);
CREATE INDEX idx_promotion ON MST_SkillGrade (promotion_eligibility, is_active);
CREATE INDEX idx_sort_order ON MST_SkillGrade (sort_order);
CREATE INDEX idx_mst_skillgrade_tenant_id ON MST_SkillGrade (tenant_id);

-- その他の制約
-- 制約DDL生成エラー: uk_grade_code
-- 制約DDL生成エラー: uk_grade_level
ALTER TABLE MST_SkillGrade ADD CONSTRAINT chk_grade_level CHECK (grade_level >= 1 AND grade_level <= 5);
ALTER TABLE MST_SkillGrade ADD CONSTRAINT chk_project_complexity CHECK (project_complexity IN ('SIMPLE', 'MODERATE', 'COMPLEX', 'CRITICAL'));
ALTER TABLE MST_SkillGrade ADD CONSTRAINT chk_leadership_level CHECK (leadership_level IN ('NONE', 'TEAM', 'PROJECT', 'ORGANIZATION'));
ALTER TABLE MST_SkillGrade ADD CONSTRAINT chk_experience_months CHECK (required_experience_months IS NULL OR required_experience_months >= 0);
ALTER TABLE MST_SkillGrade ADD CONSTRAINT chk_salary_factor CHECK (salary_impact_factor IS NULL OR salary_impact_factor > 0);
