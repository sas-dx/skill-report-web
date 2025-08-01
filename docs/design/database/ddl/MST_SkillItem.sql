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

-- 作成日: 2025-06-24 23:05:56
-- ============================================

DROP TABLE IF EXISTS MST_SkillItem;

CREATE TABLE MST_SkillItem (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    skill_code VARCHAR(20) COMMENT 'スキルコード',
    skill_name VARCHAR(100) COMMENT 'スキル名',
    difficulty_level INT COMMENT '習得難易度',
    importance_level INT COMMENT '重要度',
    skill_category_id VARCHAR(50) COMMENT 'スキルカテゴリID',
    skill_type ENUM('TECHNICAL', 'BUSINESS', 'CERTIFICATION') COMMENT 'スキル種別',
    skillitem_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_SkillItemの主キー',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_skill_code ON MST_SkillItem (skill_code);
CREATE INDEX idx_skill_category ON MST_SkillItem (skill_category_id);
CREATE INDEX idx_mst_skillitem_tenant_id ON MST_SkillItem (tenant_id);

-- その他の制約
-- 制約DDL生成エラー: uk_skill_code
