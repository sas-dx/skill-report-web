-- ============================================
-- テーブル: MST_CertificationRequirement
-- 論理名: 資格要件マスタ
-- 説明: MST_CertificationRequirement（資格要件マスタ）は、職種・役職・スキルレベルに応じた資格要件を管理するマスタテーブルです。

主な目的：
- 職種別必要資格の定義
- 昇進・昇格要件の管理
- スキルレベル認定基準の設定
- 人材配置判定の支援
- キャリア開発ガイドラインの提供

このテーブルにより、組織の人材要件を明確化し、
適切な人材配置と計画的な人材育成を実現できます。

-- 作成日: 2025-06-21 17:20:34
-- ============================================

DROP TABLE IF EXISTS MST_CertificationRequirement;

CREATE TABLE MST_CertificationRequirement (
    requirement_id VARCHAR,
    requirement_name VARCHAR,
    requirement_description TEXT,
    requirement_type ENUM,
    target_job_type_id VARCHAR,
    target_position_id VARCHAR,
    target_skill_grade_id VARCHAR,
    target_department_id VARCHAR,
    certification_id VARCHAR,
    requirement_level ENUM,
    priority_order INTEGER DEFAULT 1,
    alternative_certifications TEXT,
    minimum_experience_years INTEGER,
    minimum_skill_level ENUM,
    grace_period_months INTEGER,
    renewal_required BOOLEAN DEFAULT False,
    renewal_interval_months INTEGER,
    exemption_conditions TEXT,
    assessment_criteria TEXT,
    business_justification TEXT,
    compliance_requirement BOOLEAN DEFAULT False,
    client_requirement BOOLEAN DEFAULT False,
    internal_policy BOOLEAN DEFAULT False,
    effective_start_date DATE,
    effective_end_date DATE,
    notification_timing INTEGER,
    escalation_timing INTEGER,
    cost_support_available BOOLEAN DEFAULT False,
    cost_support_amount DECIMAL,
    cost_support_conditions TEXT,
    training_support_available BOOLEAN DEFAULT False,
    recommended_training_programs TEXT,
    study_time_allocation DECIMAL,
    success_rate DECIMAL,
    average_study_hours DECIMAL,
    difficulty_rating ENUM,
    active_flag BOOLEAN DEFAULT True,
    created_by VARCHAR,
    approved_by VARCHAR,
    approval_date DATE,
    review_date DATE,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_requirement_id ON MST_CertificationRequirement (requirement_id);
CREATE INDEX idx_requirement_type ON MST_CertificationRequirement (requirement_type);
CREATE INDEX idx_target_job_type ON MST_CertificationRequirement (target_job_type_id);
CREATE INDEX idx_target_position ON MST_CertificationRequirement (target_position_id);
CREATE INDEX idx_target_skill_grade ON MST_CertificationRequirement (target_skill_grade_id);
CREATE INDEX idx_certification_id ON MST_CertificationRequirement (certification_id);
CREATE INDEX idx_requirement_level ON MST_CertificationRequirement (requirement_level);
CREATE INDEX idx_active_flag ON MST_CertificationRequirement (active_flag);
CREATE INDEX idx_effective_period ON MST_CertificationRequirement (effective_start_date, effective_end_date);
CREATE INDEX idx_compliance_requirement ON MST_CertificationRequirement (compliance_requirement);
CREATE INDEX idx_priority_order ON MST_CertificationRequirement (priority_order);
