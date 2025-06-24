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

-- 作成日: 2025-06-24 23:02:18
-- ============================================

DROP TABLE IF EXISTS MST_Certification;

CREATE TABLE MST_Certification (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    certification_code VARCHAR(50) COMMENT '資格コード',
    certification_name VARCHAR(200) COMMENT '資格名',
    certification_category ENUM('IT', 'BUSINESS', 'NATIONAL', 'LANGUAGE', 'OTHER') COMMENT '資格カテゴリ',
    certification_id INTEGER NOT NULL AUTO_INCREMENT COMMENT '資格ID',
    certification_level ENUM('BASIC', 'INTERMEDIATE', 'ADVANCED', 'EXPERT') COMMENT '資格レベル',
    certification_name_en VARCHAR(200) COMMENT '資格名（英語）',
    description TEXT COMMENT '説明',
    exam_fee DECIMAL(10,2) COMMENT '受験料',
    exam_format ENUM('ONLINE', 'OFFLINE', 'BOTH') COMMENT '試験形式',
    exam_language VARCHAR(50) COMMENT '試験言語',
    is_active BOOLEAN DEFAULT True COMMENT '有効フラグ',
    is_recommended BOOLEAN DEFAULT False COMMENT '推奨資格フラグ',
    issuer VARCHAR(100) COMMENT '発行機関',
    issuer_country VARCHAR(10) COMMENT '発行国',
    official_url VARCHAR(500) COMMENT '公式URL',
    renewal_required BOOLEAN DEFAULT False COMMENT '更新要否',
    renewal_requirements TEXT COMMENT '更新要件',
    skill_category_id VARCHAR(50) COMMENT 'スキルカテゴリID',
    validity_period_months INTEGER COMMENT '有効期間（月）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
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

-- その他の制約
ALTER TABLE MST_Certification ADD CONSTRAINT uk_certification_code UNIQUE (certification_code);
ALTER TABLE MST_Certification ADD CONSTRAINT chk_certification_category CHECK (certification_category IN ('IT', 'BUSINESS', 'NATIONAL', 'LANGUAGE', 'OTHER'));
ALTER TABLE MST_Certification ADD CONSTRAINT chk_certification_level CHECK (certification_level IN ('BASIC', 'INTERMEDIATE', 'ADVANCED', 'EXPERT'));
ALTER TABLE MST_Certification ADD CONSTRAINT chk_exam_format CHECK (exam_format IN ('ONLINE', 'OFFLINE', 'BOTH'));
ALTER TABLE MST_Certification ADD CONSTRAINT chk_validity_period CHECK (validity_period_months IS NULL OR validity_period_months > 0);
ALTER TABLE MST_Certification ADD CONSTRAINT chk_exam_fee CHECK (exam_fee IS NULL OR exam_fee >= 0);
