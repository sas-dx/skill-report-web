-- MST_SkillHierarchy (スキル階層マスタ) DDL
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE MST_SkillHierarchy (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    skill_id VARCHAR(50),
    parent_skill_id VARCHAR(50),
    hierarchy_level INTEGER,
    skill_path VARCHAR(500),
    sort_order INTEGER DEFAULT 0,
    is_leaf BOOLEAN DEFAULT True,
    skill_category ENUM,
    description TEXT,
    is_active BOOLEAN DEFAULT True,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE INDEX idx_skill_id ON MST_SkillHierarchy (skill_id);
CREATE INDEX idx_parent_skill ON MST_SkillHierarchy (parent_skill_id);
CREATE INDEX idx_hierarchy_level ON MST_SkillHierarchy (hierarchy_level);
CREATE INDEX idx_skill_path ON MST_SkillHierarchy (skill_path);
CREATE INDEX idx_category_level ON MST_SkillHierarchy (skill_category, hierarchy_level);
CREATE INDEX idx_parent_sort ON MST_SkillHierarchy (parent_skill_id, sort_order);

-- 外部キー制約
ALTER TABLE MST_SkillHierarchy ADD CONSTRAINT fk_hierarchy_skill FOREIGN KEY (skill_id) REFERENCES MST_SkillItem(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_SkillHierarchy ADD CONSTRAINT fk_hierarchy_parent FOREIGN KEY (parent_skill_id) REFERENCES MST_SkillHierarchy(skill_id) ON UPDATE CASCADE ON DELETE CASCADE;
