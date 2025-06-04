-- ============================================
-- テーブル: MST_CertificationRequirement
-- 論理名: 資格要件マスタ
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_CertificationRequirement;

CREATE TABLE MST_CertificationRequirement (
    requirement_id VARCHAR(50) COMMENT '資格要件を一意に識別するID',
    requirement_name VARCHAR(200) COMMENT '資格要件の名称',
    requirement_description TEXT COMMENT '資格要件の詳細説明',
    requirement_type ENUM COMMENT '要件の種別（JOB_TYPE:職種要件、POSITION:役職要件、SKILL_GRADE:スキルグレード要件、PROJECT:プロジェクト要件、PROMOTION:昇進要件）',
    target_job_type_id VARCHAR(50) COMMENT '要件が適用される職種のID（MST_JobTypeへの外部キー）',
    target_position_id VARCHAR(50) COMMENT '要件が適用される役職のID（MST_Positionへの外部キー）',
    target_skill_grade_id VARCHAR(50) COMMENT '要件が適用されるスキルグレードのID（MST_SkillGradeへの外部キー）',
    target_department_id VARCHAR(50) COMMENT '要件が適用される部署のID（MST_Departmentへの外部キー）',
    certification_id VARCHAR(50) COMMENT '必要な資格のID（MST_Certificationへの外部キー）',
    requirement_level ENUM COMMENT '要件の必要度（MANDATORY:必須、PREFERRED:推奨、OPTIONAL:任意、DISQUALIFYING:除外条件）',
    priority_order INTEGER DEFAULT 1 COMMENT '複数資格がある場合の優先順位（1が最高）',
    alternative_certifications TEXT COMMENT '代替可能な資格のリスト（JSON形式）',
    minimum_experience_years INTEGER COMMENT '資格取得に加えて必要な実務経験年数',
    minimum_skill_level ENUM COMMENT '併せて必要な最低スキルレベル（BEGINNER:初級、INTERMEDIATE:中級、ADVANCED:上級、EXPERT:エキスパート）',
    grace_period_months INTEGER COMMENT '資格取得までの猶予期間（月数）',
    renewal_required BOOLEAN DEFAULT False COMMENT '資格の定期更新が必要かどうか',
    renewal_interval_months INTEGER COMMENT '資格更新の間隔（月数）',
    exemption_conditions TEXT COMMENT '資格要件の免除条件',
    assessment_criteria TEXT COMMENT '要件充足の評価基準・判定方法',
    business_justification TEXT COMMENT '資格要件設定の業務上の根拠・理由',
    compliance_requirement BOOLEAN DEFAULT False COMMENT '法的・規制上の要件かどうか',
    client_requirement BOOLEAN DEFAULT False COMMENT '顧客要求による要件かどうか',
    internal_policy BOOLEAN DEFAULT False COMMENT '社内方針による要件かどうか',
    effective_start_date DATE COMMENT '要件の適用開始日',
    effective_end_date DATE COMMENT '要件の適用終了日',
    notification_timing INTEGER COMMENT '要件充足期限前の通知タイミング（日数）',
    escalation_timing INTEGER COMMENT '未充足時のエスカレーション期限（日数）',
    cost_support_available BOOLEAN DEFAULT False COMMENT '資格取得費用の支援があるかどうか',
    cost_support_amount DECIMAL(10,2) COMMENT '資格取得費用の支援金額',
    cost_support_conditions TEXT COMMENT '費用支援の条件・制約',
    training_support_available BOOLEAN DEFAULT False COMMENT '資格取得のための研修支援があるかどうか',
    recommended_training_programs TEXT COMMENT '資格取得に推奨される研修プログラム（JSON形式）',
    study_time_allocation DECIMAL(5,2) COMMENT '業務時間内での学習時間配分（時間/週）',
    success_rate DECIMAL(5,2) COMMENT '社内での資格取得成功率（%）',
    average_study_hours DECIMAL(6,2) COMMENT '資格取得に必要な平均学習時間',
    difficulty_rating ENUM COMMENT '社内での難易度評価（EASY:易、MEDIUM:中、HARD:難、VERY_HARD:非常に難）',
    active_flag BOOLEAN DEFAULT True COMMENT '現在有効な要件かどうか',
    created_by VARCHAR(50) COMMENT '要件を作成した担当者ID',
    approved_by VARCHAR(50) COMMENT '要件を承認した責任者ID',
    approval_date DATE COMMENT '要件が承認された日付',
    review_date DATE COMMENT '次回要件見直し予定日',
    notes TEXT COMMENT 'その他の備考・補足情報',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称',
    description TEXT COMMENT 'マスタ説明'
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

-- 外部キー制約
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_job_type FOREIGN KEY (target_job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_position FOREIGN KEY (target_position_id) REFERENCES MST_Position(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_skill_grade FOREIGN KEY (target_skill_grade_id) REFERENCES MST_SkillGrade(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_department FOREIGN KEY (target_department_id) REFERENCES MST_Department(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_certification FOREIGN KEY (certification_id) REFERENCES MST_Certification(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_created_by FOREIGN KEY (created_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_approved_by FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT uk_requirement_id UNIQUE ();
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
