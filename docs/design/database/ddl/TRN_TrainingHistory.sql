-- ============================================
-- テーブル: TRN_TrainingHistory
-- 論理名: 研修参加履歴
-- 説明: TRN_TrainingHistory（研修参加履歴）は、社員が参加した研修・教育プログラムの履歴を管理するトランザクションテーブルです。

主な目的：
- 研修参加履歴の記録・管理
- 学習成果・評価の記録
- スキル向上の追跡
- 継続教育ポイント（PDU）の管理
- 人材育成計画の進捗管理

このテーブルにより、社員の学習履歴を体系的に記録し、
スキル開発やキャリア形成の支援を効率的に行うことができます。

-- 作成日: 2025-06-21 22:02:17
-- ============================================

DROP TABLE IF EXISTS TRN_TrainingHistory;

CREATE TABLE TRN_TrainingHistory (
    traininghistory_id SERIAL NOT NULL COMMENT 'TRN_TrainingHistoryの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    created_by VARCHAR(50) NOT NULL COMMENT 'レコード作成者のユーザーID',
    updated_by VARCHAR(50) NOT NULL COMMENT 'レコード更新者のユーザーID',
    PRIMARY KEY (traininghistory_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_trn_traininghistory_tenant_id ON TRN_TrainingHistory (tenant_id);

-- 外部キー制約
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT fk_training_history_employee FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT fk_training_history_program FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT fk_training_history_approver FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
