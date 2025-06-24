-- ============================================
-- テーブル: MST_SkillCategory
-- 論理名: スキルカテゴリマスタ
-- 説明: MST_SkillCategory（スキルカテゴリマスタ）は、スキルの分類・カテゴリを管理するマスタテーブルです。

主な目的：
- スキルの体系的分類・階層管理
- スキル検索・絞り込みの基盤
- スキルマップ・スキル評価の構造化
- 業界標準・企業独自のスキル分類対応
- スキル統計・分析の軸設定
- キャリアパス・研修計画の基盤
- スキル可視化・レポート生成の支援

このテーブルは、スキル管理システムの基盤となり、
効率的なスキル管理と戦略的人材育成を支援します。

-- 作成日: 2025-06-24 22:56:16
-- ============================================

DROP TABLE IF EXISTS MST_SkillCategory;

CREATE TABLE MST_SkillCategory (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    category_code VARCHAR(20) COMMENT 'カテゴリコード',
    category_name VARCHAR(100) COMMENT 'カテゴリ名',
    category_level INT DEFAULT 1 COMMENT 'カテゴリレベル',
    category_name_en VARCHAR(100) COMMENT 'カテゴリ名英語',
    category_name_short VARCHAR(50) COMMENT 'カテゴリ名略称',
    category_path VARCHAR(500) COMMENT 'カテゴリパス',
    category_status ENUM('ACTIVE', 'INACTIVE', 'DEPRECATED') DEFAULT 'ACTIVE' COMMENT 'カテゴリ状態',
    category_type ENUM('TECHNICAL', 'BUSINESS', 'SOFT', 'CERTIFICATION', 'LANGUAGE') COMMENT 'カテゴリ種別',
    color_code VARCHAR(7) COMMENT 'カラーコード',
    description TEXT COMMENT 'カテゴリ説明',
    display_order INT DEFAULT 999 COMMENT '表示順序',
    effective_from DATE COMMENT '有効開始日',
    effective_to DATE COMMENT '有効終了日',
    evaluation_method ENUM('LEVEL', 'SCORE', 'BINARY', 'CERTIFICATION') COMMENT '評価方法',
    icon_url VARCHAR(255) COMMENT 'アイコンURL',
    is_leaf_category BOOLEAN DEFAULT True COMMENT '末端カテゴリフラグ',
    is_popular BOOLEAN DEFAULT False COMMENT '人気カテゴリフラグ',
    is_system_category BOOLEAN DEFAULT False COMMENT 'システムカテゴリフラグ',
    max_level INT COMMENT '最大レベル',
    parent_category_id VARCHAR(50) COMMENT '親カテゴリID',
    skill_count INT DEFAULT 0 COMMENT 'スキル数',
    skillcategory_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_SkillCategoryの主キー',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
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
CREATE INDEX idx_mst_skillcategory_tenant_id ON MST_SkillCategory (tenant_id);

-- 外部キー制約
ALTER TABLE MST_SkillCategory ADD CONSTRAINT fk_skillcategory_parent FOREIGN KEY (parent_category_id) REFERENCES MST_SkillCategory(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
-- 制約DDL生成エラー: uk_category_code
ALTER TABLE MST_SkillCategory ADD CONSTRAINT chk_category_type CHECK (category_type IN ('TECHNICAL', 'BUSINESS', 'SOFT', 'CERTIFICATION', 'LANGUAGE'));
ALTER TABLE MST_SkillCategory ADD CONSTRAINT chk_category_status CHECK (category_status IN ('ACTIVE', 'INACTIVE', 'DEPRECATED'));
ALTER TABLE MST_SkillCategory ADD CONSTRAINT chk_evaluation_method CHECK (evaluation_method IS NULL OR evaluation_method IN ('LEVEL', 'SCORE', 'BINARY', 'CERTIFICATION'));
ALTER TABLE MST_SkillCategory ADD CONSTRAINT chk_category_level CHECK (category_level > 0);
ALTER TABLE MST_SkillCategory ADD CONSTRAINT chk_max_level CHECK (max_level IS NULL OR max_level > 0);
ALTER TABLE MST_SkillCategory ADD CONSTRAINT chk_skill_count CHECK (skill_count >= 0);
ALTER TABLE MST_SkillCategory ADD CONSTRAINT chk_display_order CHECK (display_order >= 0);
ALTER TABLE MST_SkillCategory ADD CONSTRAINT chk_effective_period CHECK (effective_to IS NULL OR effective_from IS NULL OR effective_from <= effective_to);
