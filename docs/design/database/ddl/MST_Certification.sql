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

-- 作成日: 2025-06-21 22:02:17
-- ============================================

DROP TABLE IF EXISTS MST_Certification;

CREATE TABLE MST_Certification (
    certification_id SERIAL NOT NULL COMMENT 'MST_Certificationの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (certification_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_certification_tenant_id ON MST_Certification (tenant_id);

-- 外部キー制約
ALTER TABLE MST_Certification ADD CONSTRAINT fk_certification_skill_category FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
