-- ============================================
-- テーブル: MST_TEMPLATE
-- 論理名: テンプレートテーブル
-- 説明: [テーブルの概要説明]

主な目的：
- [目的1]
- [目的2]
- [目的3]

[このテーブルの役割や重要性について説明]

-- 作成日: 2025-06-21 22:02:18
-- ============================================

DROP TABLE IF EXISTS MST_TEMPLATE;

CREATE TABLE MST_TEMPLATE (
    [主キーカラム名] VARCHAR,
    [カラム名] VARCHAR,
    [ステータスカラム名] ENUM DEFAULT '値1',
    [数値カラム名] INTEGER DEFAULT 0,
    [日付カラム名] DATE,
    [テキストカラム名] TEXT,
    is_active BOOLEAN DEFAULT True,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 外部キー制約
ALTER TABLE MST_TEMPLATE ADD CONSTRAINT fk_[テーブル名]_[参照テーブル名] FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE RESTRICT;
