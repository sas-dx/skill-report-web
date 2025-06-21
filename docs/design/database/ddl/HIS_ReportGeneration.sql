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

-- 作成日: 2025-06-21 17:20:34
-- ============================================

DROP TABLE IF EXISTS HIS_ReportGeneration;

CREATE TABLE HIS_ReportGeneration (
    id VARCHAR,
    tenant_id VARCHAR,
    template_id VARCHAR,
    requested_by VARCHAR,
    report_title VARCHAR,
    report_category ENUM,
    output_format ENUM,
    generation_status ENUM,
    parameters TEXT,
    file_path VARCHAR,
    file_size BIGINT,
    download_count INTEGER DEFAULT 0,
    last_downloaded_at TIMESTAMP,
    requested_at TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    processing_time_ms INTEGER,
    error_message TEXT,
    error_details TEXT,
    expires_at TIMESTAMP,
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_report_generation_template ON HIS_ReportGeneration (template_id);
CREATE INDEX idx_report_generation_requester ON HIS_ReportGeneration (requested_by);
CREATE INDEX idx_report_generation_tenant_status ON HIS_ReportGeneration (tenant_id, generation_status);
CREATE INDEX idx_report_generation_category ON HIS_ReportGeneration (report_category);
CREATE INDEX idx_report_generation_format ON HIS_ReportGeneration (output_format);
CREATE INDEX idx_report_generation_requested ON HIS_ReportGeneration (requested_at);
CREATE INDEX idx_report_generation_completed ON HIS_ReportGeneration (completed_at);
CREATE INDEX idx_report_generation_expires ON HIS_ReportGeneration (expires_at);
