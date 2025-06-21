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

-- 作成日: 2025-06-21 17:20:35
-- ============================================

DROP TABLE IF EXISTS SYS_SkillIndex;

CREATE TABLE SYS_SkillIndex (
    id VARCHAR,
    tenant_id VARCHAR,
    skill_id VARCHAR,
    index_type ENUM,
    search_term VARCHAR,
    normalized_term VARCHAR,
    relevance_score DECIMAL DEFAULT 1.0,
    frequency_weight DECIMAL DEFAULT 1.0,
    position_weight DECIMAL DEFAULT 1.0,
    language_code VARCHAR DEFAULT 'ja',
    source_field ENUM,
    is_active BOOLEAN DEFAULT True,
    search_count INTEGER DEFAULT 0,
    last_searched_at TIMESTAMP,
    index_updated_at TIMESTAMP,
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
