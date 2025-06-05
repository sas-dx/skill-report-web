-- ============================================
-- テーブル: HIS_ReportGeneration
-- 論理名: 帳票生成履歴
-- 説明: 
-- 作成日: 2025-06-05 23:01:00
-- ============================================

DROP TABLE IF EXISTS HIS_ReportGeneration;

CREATE TABLE HIS_ReportGeneration (
    id VARCHAR(50) NOT NULL PRIMARY KEY COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'マルチテナント識別子',
    template_id VARCHAR(50) NOT NULL COMMENT '使用された帳票テンプレートのID（MST_ReportTemplateへの参照）',
    requested_by VARCHAR(50) NOT NULL COMMENT '帳票生成を要求したユーザーID',
    report_title VARCHAR(200) NOT NULL COMMENT '生成された帳票のタイトル',
    report_category ENUM('SKILL', 'GOAL', 'EVALUATION', 'SUMMARY', 'ANALYTICS') NOT NULL COMMENT '帳票の分類（SKILL:スキル関連、GOAL:目標関連、EVALUATION:評価関連、SUMMARY:サマリー、ANALYTICS:分析）',
    output_format ENUM('PDF', 'EXCEL', 'CSV', 'HTML') NOT NULL COMMENT '帳票の出力形式（PDF:PDF、EXCEL:Excel、CSV:CSV、HTML:HTML）',
    generation_status ENUM('PENDING', 'PROCESSING', 'SUCCESS', 'FAILED', 'CANCELLED') NOT NULL COMMENT '生成の状態（PENDING:待機中、PROCESSING:処理中、SUCCESS:成功、FAILED:失敗、CANCELLED:キャンセル）',
    parameters TEXT COMMENT '帳票生成時のパラメータ（JSON形式）',
    file_path VARCHAR(500) COMMENT '生成された帳票ファイルのパス',
    file_size BIGINT COMMENT '生成された帳票ファイルのサイズ（バイト）',
    download_count INTEGER NOT NULL DEFAULT 0 COMMENT '帳票がダウンロードされた回数',
    last_downloaded_at TIMESTAMP COMMENT '帳票が最後にダウンロードされた日時',
    requested_at TIMESTAMP NOT NULL COMMENT '帳票生成が要求された日時',
    started_at TIMESTAMP COMMENT '帳票生成処理が開始された日時',
    completed_at TIMESTAMP COMMENT '帳票生成処理が完了した日時',
    processing_time_ms INTEGER COMMENT '帳票生成にかかった時間（ミリ秒）',
    error_message TEXT COMMENT '生成失敗時のエラーメッセージ',
    error_details TEXT COMMENT '生成失敗時のエラー詳細情報（JSON形式）',
    expires_at TIMESTAMP COMMENT '生成された帳票ファイルの有効期限',
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

-- 外部キー制約
ALTER TABLE HIS_ReportGeneration ADD CONSTRAINT fk_report_generation_template FOREIGN KEY (template_id) REFERENCES MST_ReportTemplate(id) ON UPDATE CASCADE ON DELETE RESTRICT;

-- その他の制約
ALTER TABLE HIS_ReportGeneration ADD CONSTRAINT chk_report_generation_category CHECK (report_category IN ('SKILL', 'GOAL', 'EVALUATION', 'SUMMARY', 'ANALYTICS'));
ALTER TABLE HIS_ReportGeneration ADD CONSTRAINT chk_report_generation_format CHECK (output_format IN ('PDF', 'EXCEL', 'CSV', 'HTML'));
ALTER TABLE HIS_ReportGeneration ADD CONSTRAINT chk_report_generation_status CHECK (generation_status IN ('PENDING', 'PROCESSING', 'SUCCESS', 'FAILED', 'CANCELLED'));
ALTER TABLE HIS_ReportGeneration ADD CONSTRAINT chk_report_generation_file_size_positive CHECK (file_size IS NULL OR file_size >= 0);
ALTER TABLE HIS_ReportGeneration ADD CONSTRAINT chk_report_generation_download_count_positive CHECK (download_count >= 0);
ALTER TABLE HIS_ReportGeneration ADD CONSTRAINT chk_report_generation_processing_time_positive CHECK (processing_time_ms IS NULL OR processing_time_ms >= 0);
