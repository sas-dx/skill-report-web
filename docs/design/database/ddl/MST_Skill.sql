-- ============================================
-- テーブル: MST_Skill
-- 論理名: スキルマスタ
-- 説明: 
-- 作成日: 2025-06-06 19:50:10
-- ============================================

DROP TABLE IF EXISTS MST_Skill;

CREATE TABLE MST_Skill (
    id VARCHAR(50) NOT NULL COMMENT 'スキルの一意識別子',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    skill_name VARCHAR(200) NOT NULL COMMENT 'スキルの名称',
    skill_name_en VARCHAR(200) COMMENT 'スキルの英語名称',
    category_id VARCHAR(50) NOT NULL COMMENT 'スキルカテゴリのID（MST_SkillCategoryへの外部キー）',
    skill_type ENUM('TECHNICAL', 'BUSINESS', 'SOFT', 'LANGUAGE') NOT NULL DEFAULT 'TECHNICAL' COMMENT 'スキルの種別（TECHNICAL:技術スキル、BUSINESS:ビジネススキル、SOFT:ソフトスキル、LANGUAGE:言語スキル）',
    difficulty_level INTEGER NOT NULL DEFAULT 3 COMMENT 'スキルの習得難易度（1:易、2:普通、3:難、4:非常に難、5:最高難度）',
    description TEXT COMMENT 'スキルの詳細説明',
    evaluation_criteria TEXT COMMENT 'スキル評価の基準や指標（JSON形式）',
    required_experience_months INTEGER COMMENT 'スキル習得に必要な経験期間（月数）',
    related_skills TEXT COMMENT '関連するスキルのID一覧（JSON配列形式）',
    prerequisite_skills TEXT COMMENT '習得前提となるスキルのID一覧（JSON配列形式）',
    certification_info TEXT COMMENT '関連する資格や認定情報（JSON形式）',
    learning_resources TEXT COMMENT '学習に役立つリソースのURL一覧（JSON配列形式）',
    market_demand ENUM('LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH') NOT NULL DEFAULT 'MEDIUM' COMMENT '市場での需要レベル（LOW:低、MEDIUM:中、HIGH:高、VERY_HIGH:非常に高）',
    technology_trend ENUM('EMERGING', 'GROWING', 'STABLE', 'DECLINING') NOT NULL DEFAULT 'STABLE' COMMENT '技術トレンド（EMERGING:新興、GROWING:成長中、STABLE:安定、DECLINING:衰退）',
    is_core_skill BOOLEAN NOT NULL DEFAULT FALSE COMMENT '組織のコアスキルかどうか',
    display_order INTEGER NOT NULL DEFAULT 0 COMMENT '同一カテゴリ内での表示順序',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT 'スキルが有効かどうか',
    effective_from DATE COMMENT 'スキルの有効開始日',
    effective_to DATE COMMENT 'スキルの有効終了日',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_MST_Skill_id ON MST_Skill (id);
CREATE INDEX idx_MST_Skill_skill_name ON MST_Skill (skill_name);
CREATE INDEX idx_MST_Skill_category_id ON MST_Skill (category_id);
CREATE INDEX idx_MST_Skill_tenant_id ON MST_Skill (tenant_id);
CREATE INDEX idx_MST_Skill_tenant_skill_name ON MST_Skill (tenant_id, skill_name);
CREATE INDEX idx_MST_Skill_tenant_category ON MST_Skill (tenant_id, category_id);
CREATE INDEX idx_MST_Skill_skill_type ON MST_Skill (skill_type);
CREATE INDEX idx_MST_Skill_category_order ON MST_Skill (category_id, display_order);
CREATE INDEX idx_MST_Skill_market_demand ON MST_Skill (market_demand);
CREATE INDEX idx_MST_Skill_is_active ON MST_Skill (is_active);
CREATE INDEX idx_MST_Skill_tenant_active ON MST_Skill (tenant_id, is_active);

-- 外部キー制約
ALTER TABLE MST_Skill ADD CONSTRAINT fk_MST_Skill_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_Skill ADD CONSTRAINT fk_MST_Skill_category FOREIGN KEY (category_id) REFERENCES MST_SkillCategory(id) ON UPDATE CASCADE ON DELETE RESTRICT;

-- その他の制約
ALTER TABLE MST_Skill ADD CONSTRAINT chk_MST_Skill_skill_type CHECK (skill_type IN ('TECHNICAL', 'BUSINESS', 'SOFT', 'LANGUAGE'));
ALTER TABLE MST_Skill ADD CONSTRAINT chk_MST_Skill_difficulty_level CHECK (difficulty_level BETWEEN 1 AND 5);
ALTER TABLE MST_Skill ADD CONSTRAINT chk_MST_Skill_required_experience CHECK (required_experience_months IS NULL OR required_experience_months >= 0);
ALTER TABLE MST_Skill ADD CONSTRAINT chk_MST_Skill_market_demand CHECK (market_demand IN ('LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH'));
ALTER TABLE MST_Skill ADD CONSTRAINT chk_MST_Skill_technology_trend CHECK (technology_trend IN ('EMERGING', 'GROWING', 'STABLE', 'DECLINING'));
ALTER TABLE MST_Skill ADD CONSTRAINT chk_MST_Skill_display_order CHECK (display_order >= 0);
ALTER TABLE MST_Skill ADD CONSTRAINT chk_MST_Skill_effective_period CHECK (effective_to IS NULL OR effective_from IS NULL OR effective_to >= effective_from);
