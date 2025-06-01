-- MST_Certification (資格情報) DDL
-- 生成日時: 2025-06-01 16:12:38

CREATE TABLE MST_Certification (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    certification_code VARCHAR(50),
    certification_name VARCHAR(200),
    certification_name_en VARCHAR(200),
    issuer VARCHAR(100),
    issuer_country VARCHAR(10),
    certification_category ENUM,
    certification_level ENUM,
    validity_period_months INTEGER,
    renewal_required BOOLEAN DEFAULT False,
    renewal_requirements TEXT,
    exam_fee DECIMAL(10,2),
    exam_language VARCHAR(50),
    exam_format ENUM,
    official_url VARCHAR(500),
    description TEXT,
    skill_category_id VARCHAR(50),
    is_recommended BOOLEAN DEFAULT False,
    is_active BOOLEAN DEFAULT True,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_certification_code ON MST_Certification (certification_code);
CREATE INDEX idx_certification_name ON MST_Certification (certification_name);
CREATE INDEX idx_issuer ON MST_Certification (issuer);
CREATE INDEX idx_category_level ON MST_Certification (certification_category, certification_level);
CREATE INDEX idx_recommended ON MST_Certification (is_recommended, is_active);
CREATE INDEX idx_skill_category ON MST_Certification (skill_category_id);

-- 外部キー制約
ALTER TABLE MST_Certification ADD CONSTRAINT fk_certification_skill_category FOREIGN KEY (skill_category_id) REFERENCES MST_SkillCategory(id) ON UPDATE CASCADE ON DELETE SET NULL;
