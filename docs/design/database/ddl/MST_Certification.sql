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

-- 作成日: 2025-06-21 17:20:34
-- ============================================

DROP TABLE IF EXISTS MST_Certification;

CREATE TABLE MST_Certification (
    certification_code VARCHAR,
    certification_name VARCHAR,
    certification_name_en VARCHAR,
    issuer VARCHAR,
    issuer_country VARCHAR,
    certification_category ENUM,
    certification_level ENUM,
    validity_period_months INTEGER,
    renewal_required BOOLEAN DEFAULT False,
    renewal_requirements TEXT,
    exam_fee DECIMAL,
    exam_language VARCHAR,
    exam_format ENUM,
    official_url VARCHAR,
    description TEXT,
    skill_category_id VARCHAR,
    is_recommended BOOLEAN DEFAULT False,
    is_active BOOLEAN DEFAULT True,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_certification_code ON MST_Certification (certification_code);
CREATE INDEX idx_certification_name ON MST_Certification (certification_name);
CREATE INDEX idx_issuer ON MST_Certification (issuer);
CREATE INDEX idx_category_level ON MST_Certification (certification_category, certification_level);
CREATE INDEX idx_recommended ON MST_Certification (is_recommended, is_active);
CREATE INDEX idx_skill_category ON MST_Certification (skill_category_id);
