-- SYS_SkillIndex (スキル検索インデックス) DDL
-- 生成日時: 2025-06-01 20:40:26

CREATE TABLE SYS_SkillIndex (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    id VARCHAR(50),
    tenant_id VARCHAR(50),
    skill_id VARCHAR(50),
    index_type ENUM,
    search_term VARCHAR(200),
    normalized_term VARCHAR(200),
    relevance_score DECIMAL(5,3) DEFAULT 1.0,
    frequency_weight DECIMAL(5,3) DEFAULT 1.0,
    position_weight DECIMAL(5,3) DEFAULT 1.0,
    language_code VARCHAR(10) DEFAULT 'ja',
    source_field ENUM,
    is_active BOOLEAN DEFAULT True,
    search_count INTEGER DEFAULT 0,
    last_searched_at TIMESTAMP,
    index_updated_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE INDEX idx_skill_index_skill ON SYS_SkillIndex (skill_id);
CREATE INDEX idx_skill_index_search_term ON SYS_SkillIndex (normalized_term, language_code);
CREATE INDEX idx_skill_index_type ON SYS_SkillIndex (index_type);
CREATE INDEX idx_skill_index_tenant_term ON SYS_SkillIndex (tenant_id, normalized_term);
CREATE INDEX idx_skill_index_relevance ON SYS_SkillIndex (relevance_score);
CREATE INDEX idx_skill_index_active ON SYS_SkillIndex (is_active);
CREATE INDEX idx_skill_index_search_stats ON SYS_SkillIndex (search_count, last_searched_at);

-- 外部キー制約
ALTER TABLE SYS_SkillIndex ADD CONSTRAINT fk_skill_index_skill FOREIGN KEY (skill_id) REFERENCES MST_Skill(id) ON UPDATE CASCADE ON DELETE CASCADE;
