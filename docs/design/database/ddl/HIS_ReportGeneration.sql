-- ============================================
-- テーブル: HIS_ReportGeneration
-- 論理名: 帳票生成履歴
-- 説明: HIS_ReportGeneration（帳票生成履歴）は、システムで生成された帳票・レポートの履歴を管理するテーブルです。

主な目的：
- 帳票生成の履歴管理
- 生成成功・失敗の記録
- 帳票ファイルの管理
- 生成パフォーマンスの監視
- 帳票利用状況の分析

このテーブルは、帳票・レポート機能において生成状況の把握と品質向上を支える重要な履歴データです。

-- 作成日: 2025-06-21 22:02:17
-- ============================================

DROP TABLE IF EXISTS HIS_ReportGeneration;

CREATE TABLE HIS_ReportGeneration (
    reportgeneration_id SERIAL NOT NULL COMMENT 'HIS_ReportGenerationの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    PRIMARY KEY (reportgeneration_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_his_reportgeneration_tenant_id ON HIS_ReportGeneration (tenant_id);

-- 外部キー制約
ALTER TABLE HIS_ReportGeneration ADD CONSTRAINT fk_report_generation_template FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE RESTRICT;
