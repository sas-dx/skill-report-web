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

-- 作成日: 2025-06-24 22:56:15
-- ============================================

DROP TABLE IF EXISTS MST_SkillGradeRequirement;

CREATE TABLE MST_SkillGradeRequirement (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    assessment_frequency ENUM('ANNUAL', 'SEMI_ANNUAL', 'QUARTERLY', 'ON_DEMAND') DEFAULT 'ANNUAL' COMMENT '評価頻度',
    assessment_method ENUM('EXAM', 'PORTFOLIO', 'INTERVIEW', 'PROJECT', 'PEER_REVIEW') COMMENT '評価方法',
    certification_mapping TEXT COMMENT '資格マッピング',
    effective_date DATE COMMENT '有効開始日',
    evaluation_criteria TEXT COMMENT '評価基準',
    evidence_requirements TEXT COMMENT 'エビデンス要件',
    expiry_date DATE COMMENT '有効終了日',
    learning_resources TEXT COMMENT '学習リソース',
    minimum_score DECIMAL(5,2) COMMENT '最低スコア',
    prerequisite_requirements TEXT COMMENT '前提要件',
    proficiency_level INTEGER COMMENT '習熟度レベル',
    requirement_category ENUM('TECHNICAL', 'BUSINESS', 'LEADERSHIP', 'COMMUNICATION') COMMENT '要件カテゴリ',
    requirement_description TEXT COMMENT '要件説明',
    requirement_name VARCHAR(200) COMMENT '要件名',
    requirement_status ENUM('ACTIVE', 'DEPRECATED', 'OBSOLETE') DEFAULT 'ACTIVE' COMMENT '要件状況',
    revision_notes TEXT COMMENT '改版備考',
    skill_grade_id VARCHAR(50) COMMENT 'スキルグレードID',
    skillgraderequirement_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_SkillGradeRequirementの主キー',
    validity_period INTEGER COMMENT '有効期間',
    weight_percentage DECIMAL(5,2) COMMENT '重み比率',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
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
CREATE INDEX idx_mst_skillgraderequirement_tenant_id ON MST_SkillGradeRequirement (tenant_id);

-- 外部キー制約
ALTER TABLE MST_SkillGradeRequirement ADD CONSTRAINT fk_MST_SkillGradeRequirement_skill_grade FOREIGN KEY (skill_grade_id) REFERENCES MST_SkillGrade(id) ON UPDATE CASCADE ON DELETE CASCADE;

-- その他の制約
-- 制約DDL生成エラー: uk_MST_SkillGradeRequirement_grade_name
ALTER TABLE MST_SkillGradeRequirement ADD CONSTRAINT chk_MST_SkillGradeRequirement_category CHECK (requirement_category IN ('TECHNICAL', 'BUSINESS', 'LEADERSHIP', 'COMMUNICATION'));
ALTER TABLE MST_SkillGradeRequirement ADD CONSTRAINT chk_MST_SkillGradeRequirement_proficiency_level CHECK (proficiency_level >= 1 AND proficiency_level <= 5);
ALTER TABLE MST_SkillGradeRequirement ADD CONSTRAINT chk_MST_SkillGradeRequirement_weight_percentage CHECK (weight_percentage >= 0 AND weight_percentage <= 100);
ALTER TABLE MST_SkillGradeRequirement ADD CONSTRAINT chk_MST_SkillGradeRequirement_minimum_score CHECK (minimum_score IS NULL OR (minimum_score >= 0 AND minimum_score <= 100));
ALTER TABLE MST_SkillGradeRequirement ADD CONSTRAINT chk_MST_SkillGradeRequirement_assessment_method CHECK (assessment_method IN ('EXAM', 'PORTFOLIO', 'INTERVIEW', 'PROJECT', 'PEER_REVIEW'));
ALTER TABLE MST_SkillGradeRequirement ADD CONSTRAINT chk_MST_SkillGradeRequirement_assessment_frequency CHECK (assessment_frequency IN ('ANNUAL', 'SEMI_ANNUAL', 'QUARTERLY', 'ON_DEMAND'));
ALTER TABLE MST_SkillGradeRequirement ADD CONSTRAINT chk_MST_SkillGradeRequirement_status CHECK (requirement_status IN ('ACTIVE', 'DEPRECATED', 'OBSOLETE'));
ALTER TABLE MST_SkillGradeRequirement ADD CONSTRAINT chk_MST_SkillGradeRequirement_validity_period CHECK (validity_period IS NULL OR validity_period > 0);
ALTER TABLE MST_SkillGradeRequirement ADD CONSTRAINT chk_MST_SkillGradeRequirement_date_range CHECK (expiry_date IS NULL OR effective_date <= expiry_date);
