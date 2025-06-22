-- ============================================
-- テーブル: MST_TrainingProgram
-- 論理名: 研修プログラム
-- 説明: MST_TrainingProgram（研修プログラム）は、組織で提供される研修・教育プログラムの詳細情報を管理するマスタテーブルです。

主な目的：
- 研修プログラムの体系的管理
- 研修内容・カリキュラムの標準化
- スキル開発との連携
- 研修効果の測定・評価
- 人材育成計画の支援

このテーブルにより、効果的な研修体系を構築し、
組織全体のスキル向上と人材育成を促進できます。

-- 作成日: 2025-06-21 22:02:18
-- ============================================

DROP TABLE IF EXISTS MST_TrainingProgram;

CREATE TABLE MST_TrainingProgram (
    trainingprogram_id SERIAL NOT NULL COMMENT 'MST_TrainingProgramの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (trainingprogram_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_trainingprogram_tenant_id ON MST_TrainingProgram (tenant_id);

-- 外部キー制約
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT fk_training_program_created_by FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT fk_training_program_approved_by FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
