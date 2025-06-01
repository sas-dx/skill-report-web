-- SYS_SkillMatrix (スキルマップ) DDL
-- 生成日時: 2025-06-01 20:40:26

CREATE TABLE SYS_SkillMatrix (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    employee_id VARCHAR(50),
    skill_id VARCHAR(50),
    skill_level INTEGER DEFAULT 1,
    self_assessment INTEGER,
    manager_assessment INTEGER,
    peer_assessment INTEGER,
    assessment_date DATE,
    evidence_url VARCHAR(500),
    notes TEXT,
    next_target_level INTEGER,
    target_date DATE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_SYS_SkillMatrix_employee_skill ON SYS_SkillMatrix (employee_id, skill_id);
CREATE INDEX idx_SYS_SkillMatrix_employee_id ON SYS_SkillMatrix (employee_id);
CREATE INDEX idx_SYS_SkillMatrix_skill_id ON SYS_SkillMatrix (skill_id);
CREATE INDEX idx_SYS_SkillMatrix_assessment_date ON SYS_SkillMatrix (assessment_date);
CREATE INDEX idx_SYS_SkillMatrix_skill_level ON SYS_SkillMatrix (skill_level);

-- 外部キー制約
ALTER TABLE SYS_SkillMatrix ADD CONSTRAINT fk_SYS_SkillMatrix_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE SYS_SkillMatrix ADD CONSTRAINT fk_SYS_SkillMatrix_skill FOREIGN KEY (skill_id) REFERENCES MST_Skill(id) ON UPDATE CASCADE ON DELETE CASCADE;
