-- ============================================
-- テーブル: MST_JobTypeSkillGrade
-- 論理名: 職種スキルグレード関連
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_JobTypeSkillGrade;

CREATE TABLE MST_JobTypeSkillGrade (
    job_type_id VARCHAR(50) COMMENT '職種のID（MST_JobTypeへの外部キー）',
    skill_grade_id VARCHAR(50) COMMENT 'スキルグレードのID（MST_SkillGradeへの外部キー）',
    grade_requirement_type ENUM DEFAULT 'STANDARD' COMMENT 'グレード要件区分（MINIMUM:最低要件、STANDARD:標準要件、ADVANCED:上級要件）',
    required_experience_years DECIMAL(4,1) COMMENT '当該グレード到達に必要な経験年数',
    promotion_criteria TEXT COMMENT '当該グレードへの昇進基準・評価項目',
    salary_range_min DECIMAL(10,0) COMMENT '当該グレードの給与範囲下限',
    salary_range_max DECIMAL(10,0) COMMENT '当該グレードの給与範囲上限',
    performance_expectations TEXT COMMENT '当該グレードでの期待される成果・パフォーマンス',
    leadership_requirements TEXT COMMENT '当該グレードで求められるリーダーシップ能力',
    technical_depth INTEGER COMMENT '技術的深度レベル（1-10、10が最高）',
    business_impact INTEGER COMMENT '事業への影響度レベル（1-10、10が最高）',
    team_size_expectation INTEGER COMMENT '管理が期待されるチームサイズ',
    certification_requirements TEXT COMMENT '必要な資格・認定のリスト（JSON形式）',
    grade_status ENUM DEFAULT 'ACTIVE' COMMENT 'グレード状況（ACTIVE:有効、DEPRECATED:非推奨、OBSOLETE:廃止）',
    effective_date DATE COMMENT 'グレード要件の有効開始日',
    expiry_date DATE COMMENT 'グレード要件の有効終了日（NULL:無期限）',
    next_grade_path TEXT COMMENT '次のグレードへの昇進パス（JSON形式）',
    evaluation_frequency ENUM DEFAULT 'ANNUAL' COMMENT '評価頻度（ANNUAL:年次、SEMI_ANNUAL:半年、QUARTERLY:四半期）',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称',
    description TEXT COMMENT 'マスタ説明'
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

-- 外部キー制約
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT fk_MST_JobTypeSkillGrade_job_type FOREIGN KEY (job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT fk_MST_JobTypeSkillGrade_skill_grade FOREIGN KEY (skill_grade_id) REFERENCES MST_SkillGrade(id) ON UPDATE CASCADE ON DELETE CASCADE;

-- その他の制約
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT uk_MST_JobTypeSkillGrade_job_grade UNIQUE ();
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT chk_MST_JobTypeSkillGrade_requirement_type CHECK (grade_requirement_type IN ('MINIMUM', 'STANDARD', 'ADVANCED'));
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT chk_MST_JobTypeSkillGrade_status CHECK (grade_status IN ('ACTIVE', 'DEPRECATED', 'OBSOLETE'));
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT chk_MST_JobTypeSkillGrade_evaluation_frequency CHECK (evaluation_frequency IN ('ANNUAL', 'SEMI_ANNUAL', 'QUARTERLY'));
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT chk_MST_JobTypeSkillGrade_experience_years CHECK (required_experience_years IS NULL OR required_experience_years >= 0);
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT chk_MST_JobTypeSkillGrade_technical_depth CHECK (technical_depth IS NULL OR (technical_depth >= 1 AND technical_depth <= 10));
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT chk_MST_JobTypeSkillGrade_business_impact CHECK (business_impact IS NULL OR (business_impact >= 1 AND business_impact <= 10));
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT chk_MST_JobTypeSkillGrade_team_size CHECK (team_size_expectation IS NULL OR team_size_expectation >= 0);
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT chk_MST_JobTypeSkillGrade_salary_range CHECK (salary_range_min IS NULL OR salary_range_max IS NULL OR salary_range_min <= salary_range_max);
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT chk_MST_JobTypeSkillGrade_date_range CHECK (expiry_date IS NULL OR effective_date <= expiry_date);
