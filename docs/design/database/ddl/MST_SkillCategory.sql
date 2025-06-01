-- MST_SkillCategory (スキルカテゴリマスタ) DDL
-- 生成日時: 2025-06-01 20:40:25

CREATE TABLE MST_SkillCategory (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    category_code VARCHAR(20),
    category_name VARCHAR(100),
    category_name_short VARCHAR(50),
    category_name_en VARCHAR(100),
    category_type ENUM,
    parent_category_id VARCHAR(50),
    category_level INT DEFAULT 1,
    category_path VARCHAR(500),
    is_system_category BOOLEAN DEFAULT False,
    is_leaf_category BOOLEAN DEFAULT True,
    skill_count INT DEFAULT 0,
    evaluation_method ENUM,
    max_level INT,
    icon_url VARCHAR(255),
    color_code VARCHAR(7),
    display_order INT DEFAULT 999,
    is_popular BOOLEAN DEFAULT False,
    category_status ENUM DEFAULT 'ACTIVE',
    effective_from DATE,
    effective_to DATE,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_category_code ON MST_SkillCategory (category_code);
CREATE INDEX idx_category_type ON MST_SkillCategory (category_type);
CREATE INDEX idx_parent_category ON MST_SkillCategory (parent_category_id);
CREATE INDEX idx_category_level ON MST_SkillCategory (category_level);
CREATE INDEX idx_category_path ON MST_SkillCategory (category_path);
CREATE INDEX idx_system_category ON MST_SkillCategory (is_system_category);
CREATE INDEX idx_leaf_category ON MST_SkillCategory (is_leaf_category);
CREATE INDEX idx_category_status ON MST_SkillCategory (category_status);
CREATE INDEX idx_display_order ON MST_SkillCategory (parent_category_id, display_order);
CREATE INDEX idx_popular_category ON MST_SkillCategory (is_popular);

-- 外部キー制約
ALTER TABLE MST_SkillCategory ADD CONSTRAINT fk_skillcategory_parent FOREIGN KEY (parent_category_id) REFERENCES MST_SkillCategory(id) ON UPDATE CASCADE ON DELETE SET NULL;
