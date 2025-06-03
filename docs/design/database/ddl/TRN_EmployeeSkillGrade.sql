-- ============================================
-- テーブル: TRN_EmployeeSkillGrade
-- 論理名: 社員スキルグレード
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS TRN_EmployeeSkillGrade;

CREATE TABLE TRN_EmployeeSkillGrade (
    employee_id VARCHAR(50) COMMENT '対象社員のID（MST_Employeeへの外部キー）',
    job_type_id VARCHAR(50) COMMENT '対象職種のID（MST_JobTypeへの外部キー）',
    skill_grade VARCHAR(10) COMMENT 'スキルグレード値（例：S, A, B, C, D または 1, 2, 3, 4, 5）',
    skill_level INT COMMENT 'スキルレベル（数値表現、1-5の範囲）',
    effective_date DATE COMMENT 'スキルグレードの有効開始日',
    expiry_date DATE COMMENT 'スキルグレードの有効終了日（NULL=現在有効）',
    evaluation_date DATE COMMENT 'スキルグレードが評価・決定された日',
    evaluator_id VARCHAR(50) COMMENT '評価を行った社員のID（MST_Employeeへの外部キー）',
    evaluation_comment TEXT COMMENT '評価に関するコメント・備考',
    certification_flag BOOLEAN DEFAULT False COMMENT '公式認定されたスキルグレードかどうか',
    next_evaluation_date DATE COMMENT '次回スキル評価の予定日',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'マルチテナント識別子',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT 'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP' COMMENT 'レコード更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT 'レコード作成者のユーザーID',
    updated_by VARCHAR(50) NOT NULL COMMENT 'レコード更新者のユーザーID',
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_employee_job_effective ON TRN_EmployeeSkillGrade (employee_id, job_type_id, effective_date);
CREATE INDEX idx_employee_current ON TRN_EmployeeSkillGrade (employee_id, expiry_date);
CREATE INDEX idx_job_type_grade ON TRN_EmployeeSkillGrade (job_type_id, skill_grade);
CREATE INDEX idx_evaluation_date ON TRN_EmployeeSkillGrade (evaluation_date);
CREATE INDEX idx_next_evaluation ON TRN_EmployeeSkillGrade (next_evaluation_date);
CREATE INDEX idx_certification ON TRN_EmployeeSkillGrade (certification_flag);

-- 外部キー制約
ALTER TABLE TRN_EmployeeSkillGrade ADD CONSTRAINT fk_skill_grade_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE TRN_EmployeeSkillGrade ADD CONSTRAINT fk_skill_grade_job_type FOREIGN KEY (job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_EmployeeSkillGrade ADD CONSTRAINT fk_skill_grade_evaluator FOREIGN KEY (evaluator_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
ALTER TABLE TRN_EmployeeSkillGrade ADD CONSTRAINT uk_employee_job_effective UNIQUE ();
ALTER TABLE TRN_EmployeeSkillGrade ADD CONSTRAINT chk_skill_grade CHECK (skill_grade IN ('S', 'A', 'B', 'C', 'D') OR skill_grade IN ('1', '2', '3', '4', '5'));
ALTER TABLE TRN_EmployeeSkillGrade ADD CONSTRAINT chk_skill_level CHECK (skill_level IS NULL OR (skill_level >= 1 AND skill_level <= 5));
ALTER TABLE TRN_EmployeeSkillGrade ADD CONSTRAINT chk_date_range CHECK (expiry_date IS NULL OR effective_date <= expiry_date);
ALTER TABLE TRN_EmployeeSkillGrade ADD CONSTRAINT chk_evaluation_date CHECK (evaluation_date IS NULL OR evaluation_date <= effective_date);
