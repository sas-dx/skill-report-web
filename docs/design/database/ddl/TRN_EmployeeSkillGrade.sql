-- TRN_EmployeeSkillGrade (社員スキルグレード) DDL
-- 生成日時: 2025-06-01 20:54:47

CREATE TABLE TRN_EmployeeSkillGrade (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    employee_id VARCHAR(50),
    job_type_id VARCHAR(50),
    skill_grade VARCHAR(10),
    skill_level INT,
    effective_date DATE,
    expiry_date DATE,
    evaluation_date DATE,
    evaluator_id VARCHAR(50),
    evaluation_comment TEXT,
    certification_flag BOOLEAN DEFAULT False,
    next_evaluation_date DATE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

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
