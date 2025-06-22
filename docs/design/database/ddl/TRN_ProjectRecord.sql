-- ============================================
-- テーブル: TRN_ProjectRecord
-- 論理名: 案件実績
-- 説明: TRN_ProjectRecord（案件実績）は、社員が参加したプロジェクト・案件の実績情報を管理するトランザクションテーブルです。

主な目的：
- プロジェクト参加履歴の記録・管理
- 担当役割・責任範囲の記録
- 使用技術・スキルの実績記録
- 成果・評価の記録
- キャリア形成・スキル証明の基盤

このテーブルにより、社員の実務経験を体系的に記録し、
スキル評価やキャリア開発の判断材料として活用できます。

-- 作成日: 2025-06-21 22:02:17
-- ============================================

DROP TABLE IF EXISTS TRN_ProjectRecord;

CREATE TABLE TRN_ProjectRecord (
    projectrecord_id SERIAL NOT NULL COMMENT 'TRN_ProjectRecordの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    created_by VARCHAR(50) NOT NULL COMMENT 'レコード作成者のユーザーID',
    updated_by VARCHAR(50) NOT NULL COMMENT 'レコード更新者のユーザーID',
    PRIMARY KEY (projectrecord_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_trn_projectrecord_tenant_id ON TRN_ProjectRecord (tenant_id);

-- 外部キー制約
ALTER TABLE TRN_ProjectRecord ADD CONSTRAINT fk_project_record_employee FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE RESTRICT;
