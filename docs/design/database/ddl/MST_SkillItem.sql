-- MST_SkillItem (スキル項目マスタ) DDL
-- 生成日時: 2025-06-01 20:40:25

CREATE TABLE MST_SkillItem (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    skill_code VARCHAR(20),
    skill_name VARCHAR(100),
    skill_category_id VARCHAR(50),
    skill_type ENUM,
    difficulty_level INT,
    importance_level INT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_skill_code ON MST_SkillItem (skill_code);
CREATE INDEX idx_skill_category ON MST_SkillItem (skill_category_id);
