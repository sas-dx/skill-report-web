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

-- 作成日: 2025-06-24 22:56:15
-- ============================================

DROP TABLE IF EXISTS HIS_ReportGeneration;

CREATE TABLE HIS_ReportGeneration (
    id VARCHAR(50) COMMENT 'ID',
    tenant_id VARCHAR(50) COMMENT 'テナントID',
    completed_at TIMESTAMP COMMENT '完了日時',
    download_count INTEGER DEFAULT 0 COMMENT 'ダウンロード回数',
    error_details TEXT COMMENT 'エラー詳細',
    error_message TEXT COMMENT 'エラーメッセージ',
    expires_at TIMESTAMP COMMENT '有効期限',
    file_path VARCHAR(500) COMMENT 'ファイルパス',
    file_size BIGINT COMMENT 'ファイルサイズ',
    generation_status ENUM('PENDING', 'PROCESSING', 'SUCCESS', 'FAILED', 'CANCELLED') COMMENT '生成状態',
    last_downloaded_at TIMESTAMP COMMENT '最終ダウンロード日時',
    output_format ENUM('PDF', 'EXCEL', 'CSV', 'HTML') COMMENT '出力形式',
    parameters TEXT COMMENT 'パラメータ',
    processing_time_ms INTEGER COMMENT '処理時間',
    report_category ENUM('SKILL', 'GOAL', 'EVALUATION', 'SUMMARY', 'ANALYTICS') COMMENT '帳票カテゴリ',
    report_title VARCHAR(200) COMMENT '帳票タイトル',
    reportgeneration_id INT AUTO_INCREMENT NOT NULL COMMENT 'HIS_ReportGenerationの主キー',
    requested_at TIMESTAMP COMMENT '要求日時',
    requested_by VARCHAR(50) COMMENT '要求者',
    started_at TIMESTAMP COMMENT '開始日時',
    template_id VARCHAR(50) COMMENT 'テンプレートID',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
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
CREATE INDEX idx_his_reportgeneration_tenant_id ON HIS_ReportGeneration (tenant_id);

-- 外部キー制約
ALTER TABLE HIS_ReportGeneration ADD CONSTRAINT fk_report_generation_template FOREIGN KEY (template_id) REFERENCES MST_ReportTemplate(id) ON UPDATE CASCADE ON DELETE RESTRICT;

-- その他の制約
ALTER TABLE HIS_ReportGeneration ADD CONSTRAINT chk_report_generation_category CHECK (report_category IN ('SKILL', 'GOAL', 'EVALUATION', 'SUMMARY', 'ANALYTICS'));
ALTER TABLE HIS_ReportGeneration ADD CONSTRAINT chk_report_generation_format CHECK (output_format IN ('PDF', 'EXCEL', 'CSV', 'HTML'));
ALTER TABLE HIS_ReportGeneration ADD CONSTRAINT chk_report_generation_status CHECK (generation_status IN ('PENDING', 'PROCESSING', 'SUCCESS', 'FAILED', 'CANCELLED'));
ALTER TABLE HIS_ReportGeneration ADD CONSTRAINT chk_report_generation_file_size_positive CHECK (file_size IS NULL OR file_size >= 0);
ALTER TABLE HIS_ReportGeneration ADD CONSTRAINT chk_report_generation_download_count_positive CHECK (download_count >= 0);
ALTER TABLE HIS_ReportGeneration ADD CONSTRAINT chk_report_generation_processing_time_positive CHECK (processing_time_ms IS NULL OR processing_time_ms >= 0);
