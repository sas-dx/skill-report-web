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

-- 作成日: 2025-06-24 22:56:15
-- ============================================

DROP TABLE IF EXISTS MST_CertificationRequirement;

CREATE TABLE MST_CertificationRequirement (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    active_flag BOOLEAN DEFAULT True COMMENT '有効フラグ',
    alternative_certifications TEXT COMMENT '代替資格',
    approval_date DATE COMMENT '承認日',
    approved_by VARCHAR(50) COMMENT '承認者',
    assessment_criteria TEXT COMMENT '評価基準',
    average_study_hours DECIMAL(6,2) COMMENT '平均学習時間',
    business_justification TEXT COMMENT '業務上の根拠',
    certification_id VARCHAR(50) COMMENT '資格ID',
    certificationrequirement_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_CertificationRequirementの主キー',
    client_requirement BOOLEAN DEFAULT False COMMENT '顧客要件',
    compliance_requirement BOOLEAN DEFAULT False COMMENT 'コンプライアンス要件',
    cost_support_amount DECIMAL(10,2) COMMENT '支援金額',
    cost_support_available BOOLEAN DEFAULT False COMMENT '費用支援有無',
    cost_support_conditions TEXT COMMENT '支援条件',
    created_by VARCHAR(50) COMMENT '作成者',
    difficulty_rating ENUM('EASY', 'MEDIUM', 'HARD', 'VERY_HARD') COMMENT '難易度評価',
    effective_end_date DATE COMMENT '有効終了日',
    effective_start_date DATE COMMENT '有効開始日',
    escalation_timing INTEGER COMMENT 'エスカレーション期限',
    exemption_conditions TEXT COMMENT '免除条件',
    grace_period_months INTEGER COMMENT '猶予期間',
    internal_policy BOOLEAN DEFAULT False COMMENT '社内方針',
    minimum_experience_years INTEGER COMMENT '最低経験年数',
    minimum_skill_level ENUM('BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT') COMMENT '最低スキルレベル',
    notes TEXT COMMENT '備考',
    notification_timing INTEGER COMMENT '通知タイミング',
    priority_order INTEGER DEFAULT 1 COMMENT '優先順位',
    recommended_training_programs TEXT COMMENT '推奨研修プログラム',
    renewal_interval_months INTEGER COMMENT '更新間隔',
    renewal_required BOOLEAN DEFAULT False COMMENT '更新必要フラグ',
    requirement_description TEXT COMMENT '要件説明',
    requirement_id VARCHAR(50) COMMENT '要件ID',
    requirement_level ENUM('MANDATORY', 'PREFERRED', 'OPTIONAL', 'DISQUALIFYING') COMMENT '要件レベル',
    requirement_name VARCHAR(200) COMMENT '要件名',
    requirement_type ENUM('JOB_TYPE', 'POSITION', 'SKILL_GRADE', 'PROJECT', 'PROMOTION') COMMENT '要件種別',
    review_date DATE COMMENT '見直し日',
    study_time_allocation DECIMAL(5,2) COMMENT '学習時間配分',
    success_rate DECIMAL(5,2) COMMENT '合格率',
    target_department_id VARCHAR(50) COMMENT '対象部署ID',
    target_job_type_id VARCHAR(50) COMMENT '対象職種ID',
    target_position_id VARCHAR(50) COMMENT '対象役職ID',
    target_skill_grade_id VARCHAR(50) COMMENT '対象スキルグレードID',
    training_support_available BOOLEAN DEFAULT False COMMENT '研修支援有無',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
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
CREATE INDEX idx_mst_certificationrequirement_tenant_id ON MST_CertificationRequirement (tenant_id);

-- 外部キー制約
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_job_type FOREIGN KEY (target_job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_position FOREIGN KEY (target_position_id) REFERENCES MST_Position(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_skill_grade FOREIGN KEY (target_skill_grade_id) REFERENCES MST_SkillGrade(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_department FOREIGN KEY (target_department_id) REFERENCES MST_Department(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_certification FOREIGN KEY (certification_id) REFERENCES MST_Certification(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_created_by FOREIGN KEY (created_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_approved_by FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
-- 制約DDL生成エラー: uk_requirement_id
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT chk_requirement_type CHECK (requirement_type IN ('JOB_TYPE', 'POSITION', 'SKILL_GRADE', 'PROJECT', 'PROMOTION'));
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT chk_requirement_level CHECK (requirement_level IN ('MANDATORY', 'PREFERRED', 'OPTIONAL', 'DISQUALIFYING'));
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT chk_minimum_skill_level CHECK (minimum_skill_level IN ('BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT'));
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT chk_difficulty_rating CHECK (difficulty_rating IN ('EASY', 'MEDIUM', 'HARD', 'VERY_HARD'));
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT chk_priority_order_positive CHECK (priority_order > 0);
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT chk_experience_years_positive CHECK (minimum_experience_years IS NULL OR minimum_experience_years >= 0);
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT chk_grace_period_positive CHECK (grace_period_months IS NULL OR grace_period_months > 0);
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT chk_renewal_interval_positive CHECK (renewal_interval_months IS NULL OR renewal_interval_months > 0);
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT chk_effective_period CHECK (effective_end_date IS NULL OR effective_start_date <= effective_end_date);
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT chk_success_rate_range CHECK (success_rate IS NULL OR (success_rate >= 0 AND success_rate <= 100));
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT chk_cost_support_amount_positive CHECK (cost_support_amount IS NULL OR cost_support_amount >= 0);
