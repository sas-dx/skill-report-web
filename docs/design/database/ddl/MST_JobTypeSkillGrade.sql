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

-- 作成日: 2025-06-24 23:02:18
-- ============================================

DROP TABLE IF EXISTS MST_JobTypeSkillGrade;

CREATE TABLE MST_JobTypeSkillGrade (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    business_impact INTEGER COMMENT '事業影響度',
    certification_requirements TEXT COMMENT '資格要件',
    effective_date DATE COMMENT '有効開始日',
    evaluation_frequency ENUM('ANNUAL', 'SEMI_ANNUAL', 'QUARTERLY') DEFAULT 'ANNUAL' COMMENT '評価頻度',
    expiry_date DATE COMMENT '有効終了日',
    grade_requirement_type ENUM('MINIMUM', 'STANDARD', 'ADVANCED') DEFAULT 'STANDARD' COMMENT 'グレード要件区分',
    grade_status ENUM('ACTIVE', 'DEPRECATED', 'OBSOLETE') DEFAULT 'ACTIVE' COMMENT 'グレード状況',
    job_type_id VARCHAR(50) COMMENT '職種ID',
    jobtypeskillgrade_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_JobTypeSkillGradeの主キー',
    leadership_requirements TEXT COMMENT 'リーダーシップ要件',
    next_grade_path TEXT COMMENT '次グレードパス',
    performance_expectations TEXT COMMENT '成果期待値',
    promotion_criteria TEXT COMMENT '昇進基準',
    required_experience_years DECIMAL(4,1) COMMENT '必要経験年数',
    salary_range_max DECIMAL(10,0) COMMENT '給与範囲上限',
    salary_range_min DECIMAL(10,0) COMMENT '給与範囲下限',
    skill_grade_id VARCHAR(50) COMMENT 'スキルグレードID',
    team_size_expectation INTEGER COMMENT '期待チームサイズ',
    technical_depth INTEGER COMMENT '技術深度',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
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
CREATE INDEX idx_mst_jobtypeskillgrade_tenant_id ON MST_JobTypeSkillGrade (tenant_id);

-- 外部キー制約
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT fk_MST_JobTypeSkillGrade_job_type FOREIGN KEY (job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT fk_MST_JobTypeSkillGrade_skill_grade FOREIGN KEY (skill_grade_id) REFERENCES MST_SkillGrade(id) ON UPDATE CASCADE ON DELETE CASCADE;

-- その他の制約
-- 制約DDL生成エラー: uk_MST_JobTypeSkillGrade_job_grade
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT chk_MST_JobTypeSkillGrade_requirement_type CHECK (grade_requirement_type IN ('MINIMUM', 'STANDARD', 'ADVANCED'));
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT chk_MST_JobTypeSkillGrade_status CHECK (grade_status IN ('ACTIVE', 'DEPRECATED', 'OBSOLETE'));
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT chk_MST_JobTypeSkillGrade_evaluation_frequency CHECK (evaluation_frequency IN ('ANNUAL', 'SEMI_ANNUAL', 'QUARTERLY'));
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT chk_MST_JobTypeSkillGrade_experience_years CHECK (required_experience_years IS NULL OR required_experience_years >= 0);
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT chk_MST_JobTypeSkillGrade_technical_depth CHECK (technical_depth IS NULL OR (technical_depth >= 1 AND technical_depth <= 10));
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT chk_MST_JobTypeSkillGrade_business_impact CHECK (business_impact IS NULL OR (business_impact >= 1 AND business_impact <= 10));
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT chk_MST_JobTypeSkillGrade_team_size CHECK (team_size_expectation IS NULL OR team_size_expectation >= 0);
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT chk_MST_JobTypeSkillGrade_salary_range CHECK (salary_range_min IS NULL OR salary_range_max IS NULL OR salary_range_min <= salary_range_max);
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT chk_MST_JobTypeSkillGrade_date_range CHECK (expiry_date IS NULL OR effective_date <= expiry_date);
