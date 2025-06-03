-- ============================================
-- テーブル: MST_EmployeeJobType
-- 論理名: 社員職種関連
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_EmployeeJobType;

CREATE TABLE MST_EmployeeJobType (
    employee_job_type_id VARCHAR(50) COMMENT '社員職種関連を一意に識別するID',
    employee_id VARCHAR(50) COMMENT '対象社員のID（MST_Employeeへの外部キー）',
    job_type_id VARCHAR(50) COMMENT '職種のID（MST_JobTypeへの外部キー）',
    assignment_type ENUM COMMENT '職種への配属種別（PRIMARY:主職種、SECONDARY:副職種、TEMPORARY:一時的、TRAINING:研修中、CANDIDATE:候補）',
    assignment_ratio DECIMAL(5,2) DEFAULT 100.0 COMMENT '職種への配属比率（%）',
    effective_start_date DATE COMMENT '職種配属の開始日',
    effective_end_date DATE COMMENT '職種配属の終了日',
    assignment_reason ENUM COMMENT '職種配属の理由（NEW_HIRE:新規採用、PROMOTION:昇進、TRANSFER:異動、SKILL_DEVELOPMENT:スキル開発、PROJECT_NEED:プロジェクト要請、REORGANIZATION:組織再編）',
    assignment_status ENUM DEFAULT 'ACTIVE' COMMENT '現在の配属状況（ACTIVE:有効、INACTIVE:無効、PENDING:保留中、SUSPENDED:一時停止）',
    proficiency_level ENUM DEFAULT 'NOVICE' COMMENT '職種における習熟度（NOVICE:初心者、BEGINNER:初級、INTERMEDIATE:中級、ADVANCED:上級、EXPERT:エキスパート）',
    target_proficiency_level ENUM COMMENT '目標とする習熟度（NOVICE:初心者、BEGINNER:初級、INTERMEDIATE:中級、ADVANCED:上級、EXPERT:エキスパート）',
    target_achievement_date DATE COMMENT '目標習熟度の達成予定日',
    certification_requirements TEXT COMMENT '職種に必要な資格一覧（JSON形式）',
    skill_requirements TEXT COMMENT '職種に必要なスキル一覧（JSON形式）',
    experience_requirements TEXT COMMENT '職種に必要な経験・実績（JSON形式）',
    development_plan TEXT COMMENT '職種における育成計画（JSON形式）',
    training_plan TEXT COMMENT '推奨研修プログラム（JSON形式）',
    mentor_id VARCHAR(50) COMMENT '職種指導担当者のID（MST_Employeeへの外部キー）',
    supervisor_id VARCHAR(50) COMMENT '職種における直属上司のID（MST_Employeeへの外部キー）',
    performance_rating ENUM COMMENT '職種でのパフォーマンス評価（EXCELLENT:優秀、GOOD:良好、SATISFACTORY:普通、NEEDS_IMPROVEMENT:要改善、UNSATISFACTORY:不満足）',
    last_evaluation_date DATE COMMENT '最後に評価を実施した日付',
    next_evaluation_date DATE COMMENT '次回評価予定日',
    evaluation_frequency ENUM DEFAULT 'QUARTERLY' COMMENT '評価の実施頻度（MONTHLY:月次、QUARTERLY:四半期、SEMI_ANNUAL:半年、ANNUAL:年次）',
    career_path TEXT COMMENT '職種でのキャリアパス・将来展望',
    strengths TEXT COMMENT '職種における強み・得意分野',
    improvement_areas TEXT COMMENT '改善が必要な領域・課題',
    achievements TEXT COMMENT '職種での主要な実績・成果',
    goals TEXT COMMENT '職種での短期・中期目標',
    workload_percentage DECIMAL(5,2) DEFAULT 100.0 COMMENT '全業務に占める職種業務の割合（%）',
    billable_flag BOOLEAN DEFAULT True COMMENT '顧客請求対象の職種かどうか',
    cost_center VARCHAR(20) COMMENT '職種に関連するコストセンター',
    budget_allocation DECIMAL(10,2) COMMENT '職種に配分された予算',
    hourly_rate DECIMAL(8,2) COMMENT '職種での時間単価',
    overtime_eligible BOOLEAN DEFAULT True COMMENT '残業代支給対象かどうか',
    remote_work_eligible BOOLEAN DEFAULT False COMMENT 'リモートワーク可能な職種かどうか',
    travel_required BOOLEAN DEFAULT False COMMENT '出張が必要な職種かどうか',
    security_clearance_required BOOLEAN DEFAULT False COMMENT 'セキュリティクリアランスが必要かどうか',
    created_by VARCHAR(50) COMMENT '関連付けを作成した担当者ID',
    approved_by VARCHAR(50) COMMENT '関連付けを承認した責任者ID',
    approval_date DATE COMMENT '関連付けが承認された日付',
    notes TEXT COMMENT 'その他の備考・特記事項',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称',
    description TEXT COMMENT 'マスタ説明'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_employee_job_type_id ON MST_EmployeeJobType (employee_job_type_id);
CREATE INDEX idx_employee_id ON MST_EmployeeJobType (employee_id);
CREATE INDEX idx_job_type_id ON MST_EmployeeJobType (job_type_id);
CREATE INDEX idx_employee_job_type ON MST_EmployeeJobType (employee_id, job_type_id);
CREATE INDEX idx_assignment_type ON MST_EmployeeJobType (assignment_type);
CREATE INDEX idx_assignment_status ON MST_EmployeeJobType (assignment_status);
CREATE INDEX idx_proficiency_level ON MST_EmployeeJobType (proficiency_level);
CREATE INDEX idx_effective_period ON MST_EmployeeJobType (effective_start_date, effective_end_date);
CREATE INDEX idx_mentor_id ON MST_EmployeeJobType (mentor_id);
CREATE INDEX idx_supervisor_id ON MST_EmployeeJobType (supervisor_id);
CREATE INDEX idx_performance_rating ON MST_EmployeeJobType (performance_rating);

-- 外部キー制約
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_job_type FOREIGN KEY (job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_mentor FOREIGN KEY (mentor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_supervisor FOREIGN KEY (supervisor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_created_by FOREIGN KEY (created_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_approved_by FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT uk_employee_job_type_id UNIQUE ();
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_assignment_type CHECK (assignment_type IN ('PRIMARY', 'SECONDARY', 'TEMPORARY', 'TRAINING', 'CANDIDATE'));
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_assignment_status CHECK (assignment_status IN ('ACTIVE', 'INACTIVE', 'PENDING', 'SUSPENDED'));
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_proficiency_level CHECK (proficiency_level IN ('NOVICE', 'BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT'));
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_target_proficiency_level CHECK (target_proficiency_level IN ('NOVICE', 'BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT'));
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_assignment_reason CHECK (assignment_reason IN ('NEW_HIRE', 'PROMOTION', 'TRANSFER', 'SKILL_DEVELOPMENT', 'PROJECT_NEED', 'REORGANIZATION'));
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_performance_rating CHECK (performance_rating IN ('EXCELLENT', 'GOOD', 'SATISFACTORY', 'NEEDS_IMPROVEMENT', 'UNSATISFACTORY'));
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_evaluation_frequency CHECK (evaluation_frequency IN ('MONTHLY', 'QUARTERLY', 'SEMI_ANNUAL', 'ANNUAL'));
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_assignment_ratio_range CHECK (assignment_ratio >= 0 AND assignment_ratio <= 100);
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_workload_percentage_range CHECK (workload_percentage >= 0 AND workload_percentage <= 100);
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_effective_period CHECK (effective_end_date IS NULL OR effective_start_date <= effective_end_date);
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_budget_allocation_positive CHECK (budget_allocation IS NULL OR budget_allocation >= 0);
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT chk_hourly_rate_positive CHECK (hourly_rate IS NULL OR hourly_rate >= 0);
