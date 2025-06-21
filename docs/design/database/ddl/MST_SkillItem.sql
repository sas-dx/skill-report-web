-- ============================================
-- テーブル: MST_SkillItem
-- 論理名: スキル項目マスタ
-- 説明: MST_SkillItem（スキル項目マスタ）は、組織で管理・評価対象となるスキル項目の詳細情報を管理するマスタテーブルです。

主な目的：
- スキル項目の体系的管理（技術スキル、ビジネススキル、資格等）
- スキル評価基準の標準化（レベル定義、評価指標等）
- スキルカテゴリ・分類の階層管理
- 人材育成計画・研修プログラムの基盤
- プロジェクトアサインメント・スキルマッチングの基礎
- 組織スキル分析・可視化の基盤
- 外部資格・認定との連携管理

このテーブルは、人材のスキル管理、キャリア開発、組織能力分析など、
戦略的人材マネジメントの基盤となる重要なマスタデータです。

-- 作成日: 2025-06-21 17:20:34
-- ============================================

DROP TABLE IF EXISTS MST_SkillItem;

CREATE TABLE MST_SkillItem (
    skill_code VARCHAR,
    skill_name VARCHAR,
    skill_category_id VARCHAR,
    skill_type ENUM,
    difficulty_level INT,
    importance_level INT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_skill_code ON MST_SkillItem (skill_code);
CREATE INDEX idx_skill_category ON MST_SkillItem (skill_category_id);
