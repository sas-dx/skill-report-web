-- ============================================
-- テーブル: MST_SkillCategory
-- 論理名: スキルカテゴリマスタ
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_SkillCategory;

CREATE TABLE MST_SkillCategory (
    category_code VARCHAR(20) COMMENT 'スキルカテゴリを一意に識別するコード（例：CAT001）',
    category_name VARCHAR(100) COMMENT 'スキルカテゴリの正式名称',
    category_name_short VARCHAR(50) COMMENT 'スキルカテゴリの略称・短縮名',
    category_name_en VARCHAR(100) COMMENT 'スキルカテゴリの英語名称',
    category_type ENUM COMMENT 'カテゴリの種別（TECHNICAL:技術、BUSINESS:ビジネス、SOFT:ソフト、CERTIFICATION:資格、LANGUAGE:言語）',
    parent_category_id VARCHAR(50) COMMENT '上位カテゴリのID（MST_SkillCategoryへの自己参照外部キー）',
    category_level INT DEFAULT 1 COMMENT 'カテゴリの階層レベル（1:最上位、数値が大きいほど下位）',
    category_path VARCHAR(500) COMMENT 'ルートからのカテゴリパス（例：/技術/プログラミング/Java）',
    is_system_category BOOLEAN DEFAULT False COMMENT 'システム標準カテゴリかどうか（削除・変更不可）',
    is_leaf_category BOOLEAN DEFAULT True COMMENT '末端カテゴリ（子カテゴリを持たない）かどうか',
    skill_count INT DEFAULT 0 COMMENT 'このカテゴリに属するスキル数',
    evaluation_method ENUM COMMENT 'このカテゴリのスキル評価方法（LEVEL:レベル、SCORE:スコア、BINARY:有無、CERTIFICATION:資格）',
    max_level INT COMMENT 'レベル評価時の最大レベル数',
    icon_url VARCHAR(255) COMMENT 'カテゴリ表示用アイコンのURL',
    color_code VARCHAR(7) COMMENT 'カテゴリ表示用カラーコード（#RRGGBB形式）',
    display_order INT DEFAULT 999 COMMENT '同階層内での表示順序',
    is_popular BOOLEAN DEFAULT False COMMENT '人気・注目カテゴリかどうか',
    category_status ENUM DEFAULT 'ACTIVE' COMMENT 'カテゴリの状態（ACTIVE:有効、INACTIVE:無効、DEPRECATED:非推奨）',
    effective_from DATE COMMENT 'カテゴリの有効開始日',
    effective_to DATE COMMENT 'カテゴリの有効終了日',
    description TEXT COMMENT 'カテゴリの詳細説明・用途',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称'
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

-- 外部キー制約
ALTER TABLE MST_SkillCategory ADD CONSTRAINT fk_skillcategory_parent FOREIGN KEY (parent_category_id) REFERENCES MST_SkillCategory(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
ALTER TABLE MST_SkillCategory ADD CONSTRAINT uk_category_code UNIQUE ();
ALTER TABLE MST_SkillCategory ADD CONSTRAINT chk_category_type CHECK (category_type IN ('TECHNICAL', 'BUSINESS', 'SOFT', 'CERTIFICATION', 'LANGUAGE'));
ALTER TABLE MST_SkillCategory ADD CONSTRAINT chk_category_status CHECK (category_status IN ('ACTIVE', 'INACTIVE', 'DEPRECATED'));
ALTER TABLE MST_SkillCategory ADD CONSTRAINT chk_evaluation_method CHECK (evaluation_method IS NULL OR evaluation_method IN ('LEVEL', 'SCORE', 'BINARY', 'CERTIFICATION'));
ALTER TABLE MST_SkillCategory ADD CONSTRAINT chk_category_level CHECK (category_level > 0);
ALTER TABLE MST_SkillCategory ADD CONSTRAINT chk_max_level CHECK (max_level IS NULL OR max_level > 0);
ALTER TABLE MST_SkillCategory ADD CONSTRAINT chk_skill_count CHECK (skill_count >= 0);
ALTER TABLE MST_SkillCategory ADD CONSTRAINT chk_display_order CHECK (display_order >= 0);
ALTER TABLE MST_SkillCategory ADD CONSTRAINT chk_effective_period CHECK (effective_to IS NULL OR effective_from IS NULL OR effective_from <= effective_to);
