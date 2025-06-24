-- ============================================
-- テーブル: MST_Skill
-- 論理名: スキルマスタ
-- 説明: スキルマスタテーブルは、システムで管理するスキル項目の基本情報を管理するマスタテーブルです。

主な目的：
- スキル項目の一元管理
- スキルカテゴリとレベル定義の管理
- スキル評価基準の標準化
- スキル検索とフィルタリングの支援

このテーブルは、スキル管理システムの基盤となるマスタテーブルで、
統一されたスキル評価基準と効率的なスキル管理を実現します。

-- 作成日: 2025-06-24 23:02:18
-- ============================================

DROP TABLE IF EXISTS MST_Skill;

CREATE TABLE MST_Skill (
    id VARCHAR(50) COMMENT 'スキルID',
    tenant_id VARCHAR(50) COMMENT 'テナントID',
    skill_name VARCHAR(200) COMMENT 'スキル名',
    category_id VARCHAR(50) COMMENT 'カテゴリID',
    certification_info TEXT COMMENT '資格情報',
    description TEXT COMMENT '説明',
    difficulty_level INTEGER DEFAULT 3 COMMENT '難易度レベル',
    display_order INTEGER DEFAULT 0 COMMENT '表示順序',
    effective_from DATE COMMENT '有効開始日',
    effective_to DATE COMMENT '有効終了日',
    evaluation_criteria TEXT COMMENT '評価基準',
    is_active BOOLEAN DEFAULT True COMMENT '有効フラグ',
    is_core_skill BOOLEAN DEFAULT False COMMENT 'コアスキルフラグ',
    learning_resources TEXT COMMENT '学習リソース',
    market_demand ENUM('LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH') DEFAULT 'MEDIUM' COMMENT '市場需要',
    prerequisite_skills TEXT COMMENT '前提スキル',
    related_skills TEXT COMMENT '関連スキル',
    required_experience_months INTEGER COMMENT '必要経験月数',
    skill_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_Skillの主キー',
    skill_name_en VARCHAR(200) COMMENT 'スキル名英語',
    skill_type ENUM('TECHNICAL', 'BUSINESS', 'SOFT', 'LANGUAGE') DEFAULT 'TECHNICAL' COMMENT 'スキル種別',
    technology_trend ENUM('EMERGING', 'GROWING', 'STABLE', 'DECLINING') DEFAULT 'STABLE' COMMENT '技術トレンド',
    is_deleted BOOLEAN DEFAULT False COMMENT '削除フラグ',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_MST_Skill_id ON MST_Skill (id);
CREATE INDEX idx_MST_Skill_skill_name ON MST_Skill (skill_name);
CREATE INDEX idx_MST_Skill_category_id ON MST_Skill (category_id);
CREATE INDEX idx_MST_Skill_skill_type ON MST_Skill (skill_type);
CREATE INDEX idx_MST_Skill_category_order ON MST_Skill (category_id, display_order);
CREATE INDEX idx_MST_Skill_market_demand ON MST_Skill (market_demand);
CREATE INDEX idx_MST_Skill_is_active ON MST_Skill (is_active);
CREATE INDEX idx_mst_skill_tenant_id ON MST_Skill (tenant_id);

-- 外部キー制約
ALTER TABLE MST_Skill ADD CONSTRAINT fk_MST_Skill_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_Skill ADD CONSTRAINT fk_MST_Skill_category FOREIGN KEY (category_id) REFERENCES MST_SkillCategory(id) ON UPDATE CASCADE ON DELETE RESTRICT;

-- その他の制約
-- 制約DDL生成エラー: uk_MST_Skill_id
ALTER TABLE MST_Skill ADD CONSTRAINT chk_MST_Skill_skill_type CHECK (skill_type IN ('TECHNICAL', 'BUSINESS', 'SOFT', 'LANGUAGE'));
ALTER TABLE MST_Skill ADD CONSTRAINT chk_MST_Skill_difficulty_level CHECK (difficulty_level BETWEEN 1 AND 5);
ALTER TABLE MST_Skill ADD CONSTRAINT chk_MST_Skill_required_experience CHECK (required_experience_months IS NULL OR required_experience_months >= 0);
ALTER TABLE MST_Skill ADD CONSTRAINT chk_MST_Skill_market_demand CHECK (market_demand IN ('LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH'));
ALTER TABLE MST_Skill ADD CONSTRAINT chk_MST_Skill_technology_trend CHECK (technology_trend IN ('EMERGING', 'GROWING', 'STABLE', 'DECLINING'));
ALTER TABLE MST_Skill ADD CONSTRAINT chk_MST_Skill_display_order CHECK (display_order >= 0);
ALTER TABLE MST_Skill ADD CONSTRAINT chk_MST_Skill_effective_period CHECK (effective_to IS NULL OR effective_from IS NULL OR effective_to >= effective_from);
