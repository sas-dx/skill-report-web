-- ============================================
-- テーブル: MST_Certification
-- 論理名: 資格情報
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_Certification;

CREATE TABLE MST_Certification (
    certification_code VARCHAR(50) COMMENT '資格を一意に識別するコード（例：CERT_AWS_SAA、CERT_PMP）',
    certification_name VARCHAR(200) COMMENT '正式な資格名称',
    certification_name_en VARCHAR(200) COMMENT '英語での資格名称',
    issuer VARCHAR(100) COMMENT '資格を発行する機関・団体名',
    issuer_country VARCHAR(10) COMMENT '資格発行国（ISO 3166-1 alpha-2コード）',
    certification_category ENUM COMMENT '資格の分類（IT:IT関連、BUSINESS:ビジネス、NATIONAL:国家資格、LANGUAGE:語学、OTHER:その他）',
    certification_level ENUM COMMENT '資格の難易度レベル（BASIC:基礎、INTERMEDIATE:中級、ADVANCED:上級、EXPERT:エキスパート）',
    validity_period_months INTEGER COMMENT '資格の有効期間（月数、NULLの場合は無期限）',
    renewal_required BOOLEAN DEFAULT False COMMENT '定期的な更新が必要かどうか',
    renewal_requirements TEXT COMMENT '資格更新に必要な要件・条件',
    exam_fee DECIMAL(10,2) COMMENT '受験料（円）',
    exam_language VARCHAR(50) COMMENT '試験で使用される言語',
    exam_format ENUM COMMENT '試験の実施形式（ONLINE:オンライン、OFFLINE:会場、BOTH:両方）',
    official_url VARCHAR(500) COMMENT '資格の公式サイトURL',
    description TEXT COMMENT '資格の詳細説明・概要',
    skill_category_id VARCHAR(50) COMMENT '関連するスキルカテゴリのID',
    is_recommended BOOLEAN DEFAULT False COMMENT '会社として取得を推奨する資格かどうか',
    is_active BOOLEAN DEFAULT True COMMENT '資格が有効かどうか',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_certification_code ON MST_Certification (certification_code);
CREATE INDEX idx_certification_name ON MST_Certification (certification_name);
CREATE INDEX idx_issuer ON MST_Certification (issuer);
CREATE INDEX idx_category_level ON MST_Certification (certification_category, certification_level);
CREATE INDEX idx_recommended ON MST_Certification (is_recommended, is_active);
CREATE INDEX idx_skill_category ON MST_Certification (skill_category_id);

-- 外部キー制約
ALTER TABLE MST_Certification ADD CONSTRAINT fk_certification_skill_category FOREIGN KEY (skill_category_id) REFERENCES MST_SkillCategory(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
ALTER TABLE MST_Certification ADD CONSTRAINT uk_certification_code UNIQUE ();
ALTER TABLE MST_Certification ADD CONSTRAINT chk_certification_category CHECK (certification_category IN ('IT', 'BUSINESS', 'NATIONAL', 'LANGUAGE', 'OTHER'));
ALTER TABLE MST_Certification ADD CONSTRAINT chk_certification_level CHECK (certification_level IN ('BASIC', 'INTERMEDIATE', 'ADVANCED', 'EXPERT'));
ALTER TABLE MST_Certification ADD CONSTRAINT chk_exam_format CHECK (exam_format IN ('ONLINE', 'OFFLINE', 'BOTH'));
ALTER TABLE MST_Certification ADD CONSTRAINT chk_validity_period CHECK (validity_period_months IS NULL OR validity_period_months > 0);
ALTER TABLE MST_Certification ADD CONSTRAINT chk_exam_fee CHECK (exam_fee IS NULL OR exam_fee >= 0);
