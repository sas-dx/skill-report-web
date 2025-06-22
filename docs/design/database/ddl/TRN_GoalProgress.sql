-- ============================================
-- テーブル: TRN_GoalProgress
-- 論理名: 目標進捗
-- 説明: TRN_GoalProgress（目標進捗）は、社員個人の目標設定と進捗状況を管理するトランザクションテーブルです。

主な目的：
- 個人目標の設定・管理（業務目標、スキル向上目標等）
- 目標達成度の定期的な進捗管理
- 上司・部下間での目標共有・フィードバック
- 人事評価・査定の基礎データ
- 組織目標と個人目標の連携管理
- 目標設定から達成までのプロセス管理
- 成果測定・KPI管理
- 人材育成計画の基礎データ

このテーブルは、人事評価制度、目標管理制度（MBO）、人材育成など、
組織の成果管理と人材開発の基盤となる重要なデータを提供します。

-- 作成日: 2025-06-21 22:02:18
-- ============================================

DROP TABLE IF EXISTS TRN_GoalProgress;

CREATE TABLE TRN_GoalProgress (
    goalprogress_id SERIAL NOT NULL COMMENT 'TRN_GoalProgressの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    created_by VARCHAR(50) NOT NULL COMMENT 'レコード作成者のユーザーID',
    updated_by VARCHAR(50) NOT NULL COMMENT 'レコード更新者のユーザーID',
    PRIMARY KEY (goalprogress_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_trn_goalprogress_tenant_id ON TRN_GoalProgress (tenant_id);

-- 外部キー制約
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_employee FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_supervisor FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_approved_by FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_career_plan FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
