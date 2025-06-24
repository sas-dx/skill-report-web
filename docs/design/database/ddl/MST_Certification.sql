-- ============================================
-- テーブル: MST_Certification
-- 論理名: 資格情報
-- 説明: MST_Certification（資格情報）は、各種資格・認定・免許の基本情報を管理するマスタテーブルです。

主な目的：
- IT資格、業務資格、国家資格等の統一管理
- 資格の有効期限・更新要件の管理
- 資格とスキルの関連付け
- 資格取得推奨・必須要件の管理
- 資格取得状況の追跡・分析基盤

このテーブルにより、社員の資格取得状況を体系的に管理し、
キャリア開発や人材配置の判断材料として活用できます。

-- 作成日: 2025-06-24 20:30:44
-- ============================================

DROP TABLE IF EXISTS MST_Certification;

CREATE TABLE MST_Certification (
    certification_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_Certificationの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    certification_code VARCHAR(50) COMMENT '資格コード',
    certification_name VARCHAR(200) COMMENT '資格名',
    certification_name_en VARCHAR(200) COMMENT '資格名（英語）',
    issuer VARCHAR(100) COMMENT '発行機関',
    issuer_country VARCHAR(10) COMMENT '発行国',
    certification_category ENUM('IT', 'BUSINESS', 'NATIONAL', 'LANGUAGE', 'OTHER') COMMENT '資格カテゴリ',
    certification_level ENUM('BASIC', 'INTERMEDIATE', 'ADVANCED', 'EXPERT') COMMENT '資格レベル',
    validity_period_months INTEGER COMMENT '有効期間（月）',
    renewal_required BOOLEAN DEFAULT False COMMENT '更新要否',
    renewal_requirements TEXT COMMENT '更新要件',
    exam_fee DECIMAL(10,2) COMMENT '受験料',
    exam_language VARCHAR(50) COMMENT '試験言語',
    exam_format ENUM('ONLINE', 'OFFLINE', 'BOTH') COMMENT '試験形式',
    official_url VARCHAR(500) COMMENT '公式URL',
    description TEXT COMMENT '説明',
    skill_category_id VARCHAR(50) COMMENT 'スキルカテゴリID',
    is_recommended BOOLEAN DEFAULT False COMMENT '推奨資格フラグ',
    is_active BOOLEAN DEFAULT True COMMENT '有効フラグ',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (certification_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_certification_code ON MST_Certification (certification_code);
CREATE INDEX idx_certification_name ON MST_Certification (certification_name);
CREATE INDEX idx_issuer ON MST_Certification (issuer);
CREATE INDEX idx_category_level ON MST_Certification (certification_category, certification_level);
CREATE INDEX idx_recommended ON MST_Certification (is_recommended, is_active);
CREATE INDEX idx_skill_category ON MST_Certification (skill_category_id);
CREATE INDEX idx_mst_certification_tenant_id ON MST_Certification (tenant_id);

-- 外部キー制約
ALTER TABLE MST_Certification ADD CONSTRAINT fk_certification_skill_category FOREIGN KEY (skill_category_id) REFERENCES MST_SkillCategory(id) ON UPDATE CASCADE ON DELETE SET NULL;
