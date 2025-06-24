-- ============================================
-- テーブル: SYS_SkillIndex
-- 論理名: スキル検索インデックス
-- 説明: SYS_SkillIndex（スキル検索インデックス）は、スキル検索機能の高速化のための検索インデックス情報を管理するシステムテーブルです。

主な目的：
- 全文検索インデックスの管理
- スキル名・キーワードの検索最適化
- 検索パフォーマンスの向上
- 検索結果の関連度スコア管理
- 検索統計情報の蓄積

このテーブルは、スキル管理機能において高速で精度の高い検索を実現する重要なシステムデータです。

-- 作成日: 2025-06-24 23:05:57
-- ============================================

DROP TABLE IF EXISTS SYS_SkillIndex;

CREATE TABLE SYS_SkillIndex (
    id VARCHAR(50) COMMENT 'ID',
    tenant_id VARCHAR(50) COMMENT 'テナントID',
    frequency_weight DECIMAL(5,3) DEFAULT 1.0 COMMENT '頻度重み',
    index_type ENUM('FULLTEXT', 'KEYWORD', 'CATEGORY', 'SYNONYM') COMMENT 'インデックスタイプ',
    index_updated_at TIMESTAMP COMMENT 'インデックス更新日時',
    is_active BOOLEAN DEFAULT True COMMENT '有効フラグ',
    language_code VARCHAR(10) DEFAULT 'ja' COMMENT '言語コード',
    last_searched_at TIMESTAMP COMMENT '最終検索日時',
    normalized_term VARCHAR(200) COMMENT '正規化語',
    position_weight DECIMAL(5,3) DEFAULT 1.0 COMMENT '位置重み',
    relevance_score DECIMAL(5,3) DEFAULT 1.0 COMMENT '関連度スコア',
    search_count INTEGER DEFAULT 0 COMMENT '検索回数',
    search_term VARCHAR(200) COMMENT '検索語',
    skill_id VARCHAR(50) COMMENT 'スキルID',
    skillindex_id INT AUTO_INCREMENT NOT NULL COMMENT 'SYS_SkillIndexの主キー',
    source_field ENUM('NAME', 'DESCRIPTION', 'KEYWORD', 'CATEGORY') COMMENT 'ソースフィールド',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
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
