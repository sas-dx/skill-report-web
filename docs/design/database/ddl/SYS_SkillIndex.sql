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

-- 作成日: 2025-06-21 22:02:18
-- ============================================

DROP TABLE IF EXISTS SYS_SkillIndex;

CREATE TABLE SYS_SkillIndex (
    skillindex_id SERIAL NOT NULL COMMENT 'SYS_SkillIndexの主キー',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    PRIMARY KEY (skillindex_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 外部キー制約
ALTER TABLE SYS_SkillIndex ADD CONSTRAINT fk_skill_index_skill FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
