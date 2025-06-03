-- ============================================
-- テーブル: MST_SkillGradeRequirement
-- 論理名: スキルグレード要件
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_SkillGradeRequirement;

CREATE TABLE MST_SkillGradeRequirement (
    skill_grade_id VARCHAR(50) COMMENT 'スキルグレードのID（MST_SkillGradeへの外部キー）',
    requirement_category ENUM COMMENT '要件カテゴリ（TECHNICAL:技術、BUSINESS:業務、LEADERSHIP:リーダーシップ、COMMUNICATION:コミュニケーション）',
    requirement_name VARCHAR(200) COMMENT '要件の名称',
    requirement_description TEXT COMMENT '要件の詳細説明',
    evaluation_criteria TEXT COMMENT '具体的な評価基準・判定方法',
    proficiency_level INTEGER COMMENT '要求される習熟度レベル（1-5、5が最高）',
    weight_percentage DECIMAL(5,2) COMMENT 'グレード内での重み比率（%）',
    minimum_score DECIMAL(5,2) COMMENT '合格に必要な最低スコア',
    evidence_requirements TEXT COMMENT '評価に必要なエビデンス・証拠',
    learning_resources TEXT COMMENT '推奨学習リソース・教材（JSON形式）',
    prerequisite_requirements TEXT COMMENT '前提となる要件のリスト（JSON形式）',
    assessment_method ENUM COMMENT '評価方法（EXAM:試験、PORTFOLIO:ポートフォリオ、INTERVIEW:面接、PROJECT:プロジェクト、PEER_REVIEW:同僚評価）',
    assessment_frequency ENUM DEFAULT 'ANNUAL' COMMENT '評価頻度（ANNUAL:年次、SEMI_ANNUAL:半年、QUARTERLY:四半期、ON_DEMAND:随時）',
    validity_period INTEGER COMMENT '評価結果の有効期間（月数）',
    certification_mapping TEXT COMMENT '関連する外部資格・認定のマッピング（JSON形式）',
    requirement_status ENUM DEFAULT 'ACTIVE' COMMENT '要件状況（ACTIVE:有効、DEPRECATED:非推奨、OBSOLETE:廃止）',
    effective_date DATE COMMENT '要件の有効開始日',
    expiry_date DATE COMMENT '要件の有効終了日（NULL:無期限）',
    revision_notes TEXT COMMENT '要件変更時の備考・理由',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称',
    description TEXT COMMENT 'マスタ説明'
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

-- 外部キー制約
ALTER TABLE MST_SkillGradeRequirement ADD CONSTRAINT fk_MST_SkillGradeRequirement_skill_grade FOREIGN KEY (skill_grade_id) REFERENCES MST_SkillGrade(id) ON UPDATE CASCADE ON DELETE CASCADE;

-- その他の制約
ALTER TABLE MST_SkillGradeRequirement ADD CONSTRAINT uk_MST_SkillGradeRequirement_grade_name UNIQUE ();
ALTER TABLE MST_SkillGradeRequirement ADD CONSTRAINT chk_MST_SkillGradeRequirement_category CHECK (requirement_category IN ('TECHNICAL', 'BUSINESS', 'LEADERSHIP', 'COMMUNICATION'));
ALTER TABLE MST_SkillGradeRequirement ADD CONSTRAINT chk_MST_SkillGradeRequirement_proficiency_level CHECK (proficiency_level >= 1 AND proficiency_level <= 5);
ALTER TABLE MST_SkillGradeRequirement ADD CONSTRAINT chk_MST_SkillGradeRequirement_weight_percentage CHECK (weight_percentage >= 0 AND weight_percentage <= 100);
ALTER TABLE MST_SkillGradeRequirement ADD CONSTRAINT chk_MST_SkillGradeRequirement_minimum_score CHECK (minimum_score IS NULL OR (minimum_score >= 0 AND minimum_score <= 100));
ALTER TABLE MST_SkillGradeRequirement ADD CONSTRAINT chk_MST_SkillGradeRequirement_assessment_method CHECK (assessment_method IN ('EXAM', 'PORTFOLIO', 'INTERVIEW', 'PROJECT', 'PEER_REVIEW'));
ALTER TABLE MST_SkillGradeRequirement ADD CONSTRAINT chk_MST_SkillGradeRequirement_assessment_frequency CHECK (assessment_frequency IN ('ANNUAL', 'SEMI_ANNUAL', 'QUARTERLY', 'ON_DEMAND'));
ALTER TABLE MST_SkillGradeRequirement ADD CONSTRAINT chk_MST_SkillGradeRequirement_status CHECK (requirement_status IN ('ACTIVE', 'DEPRECATED', 'OBSOLETE'));
ALTER TABLE MST_SkillGradeRequirement ADD CONSTRAINT chk_MST_SkillGradeRequirement_validity_period CHECK (validity_period IS NULL OR validity_period > 0);
ALTER TABLE MST_SkillGradeRequirement ADD CONSTRAINT chk_MST_SkillGradeRequirement_date_range CHECK (expiry_date IS NULL OR effective_date <= expiry_date);
