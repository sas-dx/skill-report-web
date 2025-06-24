-- ============================================
-- テーブル: TRN_EmployeeSkillGrade
-- 論理名: 社員スキルグレード
-- 説明: TRN_EmployeeSkillGrade（社員スキルグレード）は、社員が職種ごとに持つスキルグレード情報を管理するトランザクションテーブルです。

主な目的：
- 社員の職種別スキルグレードの管理
- スキルグレードの履歴管理（昇格・降格の記録）
- 有効期間による時系列管理
- 人事評価・昇進判定の基礎データ提供
- スキル分析・レポート作成の基盤
- 組織のスキル可視化・最適化支援

このテーブルは、人事評価、キャリア開発、組織分析など、スキル管理の中核となる重要なデータです。

-- 作成日: 2025-06-24 23:02:18
-- ============================================

DROP TABLE IF EXISTS TRN_EmployeeSkillGrade;

CREATE TABLE TRN_EmployeeSkillGrade (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    certification_flag BOOLEAN DEFAULT False COMMENT '認定フラグ',
    effective_date DATE COMMENT '有効開始日',
    employee_id VARCHAR(50) COMMENT '社員ID',
    employeeskillgrade_id INT AUTO_INCREMENT NOT NULL COMMENT 'TRN_EmployeeSkillGradeの主キー',
    evaluation_comment TEXT COMMENT '評価コメント',
    evaluation_date DATE COMMENT '評価日',
    evaluator_id VARCHAR(50) COMMENT '評価者ID',
    expiry_date DATE COMMENT '有効終了日',
    job_type_id VARCHAR(50) COMMENT '職種ID',
    next_evaluation_date DATE COMMENT '次回評価予定日',
    skill_grade VARCHAR(10) COMMENT 'スキルグレード',
    skill_level INT COMMENT 'スキルレベル',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    created_by VARCHAR(50) COMMENT '作成者ID',
    updated_by VARCHAR(50) COMMENT '更新者ID',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_employee_job_effective ON TRN_EmployeeSkillGrade (employee_id, job_type_id, effective_date);
CREATE INDEX idx_employee_current ON TRN_EmployeeSkillGrade (employee_id, expiry_date);
CREATE INDEX idx_job_type_grade ON TRN_EmployeeSkillGrade (job_type_id, skill_grade);
CREATE INDEX idx_evaluation_date ON TRN_EmployeeSkillGrade (evaluation_date);
CREATE INDEX idx_next_evaluation ON TRN_EmployeeSkillGrade (next_evaluation_date);
CREATE INDEX idx_certification ON TRN_EmployeeSkillGrade (certification_flag);
CREATE INDEX idx_trn_employeeskillgrade_tenant_id ON TRN_EmployeeSkillGrade (tenant_id);

-- 外部キー制約
ALTER TABLE TRN_EmployeeSkillGrade ADD CONSTRAINT fk_skill_grade_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE TRN_EmployeeSkillGrade ADD CONSTRAINT fk_skill_grade_job_type FOREIGN KEY (job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_EmployeeSkillGrade ADD CONSTRAINT fk_skill_grade_evaluator FOREIGN KEY (evaluator_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
-- 制約DDL生成エラー: uk_employee_job_effective
ALTER TABLE TRN_EmployeeSkillGrade ADD CONSTRAINT chk_skill_grade CHECK (skill_grade IN ('S', 'A', 'B', 'C', 'D') OR skill_grade IN ('1', '2', '3', '4', '5'));
ALTER TABLE TRN_EmployeeSkillGrade ADD CONSTRAINT chk_skill_level CHECK (skill_level IS NULL OR (skill_level >= 1 AND skill_level <= 5));
ALTER TABLE TRN_EmployeeSkillGrade ADD CONSTRAINT chk_date_range CHECK (expiry_date IS NULL OR effective_date <= expiry_date);
ALTER TABLE TRN_EmployeeSkillGrade ADD CONSTRAINT chk_evaluation_date CHECK (evaluation_date IS NULL OR evaluation_date <= effective_date);
