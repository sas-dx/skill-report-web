-- ============================================
-- テーブル: MST_JobType
-- 論理名: 職種マスタ
-- 説明: MST_JobType（職種マスタ）は、組織内の職種分類と各職種の基本情報を管理するマスタテーブルです。

主な目的：
- 職種の体系的な分類・管理
- 職種別スキル要件の定義基盤
- 人材配置・採用計画の基準
- キャリアパス・昇進要件の管理
- 職種別評価基準の設定

このテーブルにより、社員のキャリア開発や適材適所の人材配置、
職種別スキル要件の管理を効率的に行うことができます。

-- 作成日: 2025-06-21 22:02:18
-- ============================================

DROP TABLE IF EXISTS MST_JobType;

CREATE TABLE MST_JobType (
    jobtype_id SERIAL NOT NULL COMMENT 'MST_JobTypeの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (jobtype_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_jobtype_tenant_id ON MST_JobType (tenant_id);
