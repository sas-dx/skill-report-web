-- ============================================
-- テーブル: SYS_SkillIndex
-- 論理名: スキル検索インデックス
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS SYS_SkillIndex;

CREATE TABLE SYS_SkillIndex (
    id VARCHAR(50) COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) COMMENT 'マルチテナント識別子',
    skill_id VARCHAR(50) COMMENT 'インデックス対象のスキルID（MST_Skillへの参照）',
    index_type ENUM COMMENT 'インデックスの種類（FULLTEXT:全文検索、KEYWORD:キーワード、CATEGORY:カテゴリ、SYNONYM:同義語）',
    search_term VARCHAR(200) COMMENT '検索対象となる語句・キーワード',
    normalized_term VARCHAR(200) COMMENT '検索最適化のため正規化された語句',
    relevance_score DECIMAL(5,3) DEFAULT 1.0 COMMENT '検索結果の関連度スコア（0.000-1.000）',
    frequency_weight DECIMAL(5,3) DEFAULT 1.0 COMMENT '語句の出現頻度による重み（0.000-1.000）',
    position_weight DECIMAL(5,3) DEFAULT 1.0 COMMENT '語句の出現位置による重み（0.000-1.000）',
    language_code VARCHAR(10) DEFAULT 'ja' COMMENT '検索語の言語（ja:日本語、en:英語等）',
    source_field ENUM COMMENT 'インデックス元のフィールド（NAME:スキル名、DESCRIPTION:説明、KEYWORD:キーワード、CATEGORY:カテゴリ）',
    is_active BOOLEAN DEFAULT True COMMENT 'インデックスが有効かどうか',
    search_count INTEGER DEFAULT 0 COMMENT 'この語句での検索実行回数',
    last_searched_at TIMESTAMP COMMENT 'この語句で最後に検索された日時',
    index_updated_at TIMESTAMP COMMENT 'インデックスが最後に更新された日時',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_skill_index_skill ON SYS_SkillIndex (skill_id);
CREATE INDEX idx_skill_index_search_term ON SYS_SkillIndex (normalized_term, language_code);
CREATE INDEX idx_skill_index_type ON SYS_SkillIndex (index_type);
CREATE INDEX idx_skill_index_tenant_term ON SYS_SkillIndex (tenant_id, normalized_term);
CREATE INDEX idx_skill_index_relevance ON SYS_SkillIndex (relevance_score);
CREATE INDEX idx_skill_index_active ON SYS_SkillIndex (is_active);
CREATE INDEX idx_skill_index_search_stats ON SYS_SkillIndex (search_count, last_searched_at);

-- 外部キー制約
ALTER TABLE SYS_SkillIndex ADD CONSTRAINT fk_skill_index_skill FOREIGN KEY (skill_id) REFERENCES MST_Skill(id) ON UPDATE CASCADE ON DELETE CASCADE;

-- その他の制約
ALTER TABLE SYS_SkillIndex ADD CONSTRAINT chk_skill_index_type CHECK (index_type IN ('FULLTEXT', 'KEYWORD', 'CATEGORY', 'SYNONYM'));
ALTER TABLE SYS_SkillIndex ADD CONSTRAINT chk_skill_index_source_field CHECK (source_field IN ('NAME', 'DESCRIPTION', 'KEYWORD', 'CATEGORY'));
ALTER TABLE SYS_SkillIndex ADD CONSTRAINT chk_skill_index_relevance_range CHECK (relevance_score >= 0.000 AND relevance_score <= 1.000);
ALTER TABLE SYS_SkillIndex ADD CONSTRAINT chk_skill_index_frequency_range CHECK (frequency_weight >= 0.000 AND frequency_weight <= 1.000);
ALTER TABLE SYS_SkillIndex ADD CONSTRAINT chk_skill_index_position_range CHECK (position_weight >= 0.000 AND position_weight <= 1.000);
ALTER TABLE SYS_SkillIndex ADD CONSTRAINT chk_skill_index_search_count_positive CHECK (search_count >= 0);
