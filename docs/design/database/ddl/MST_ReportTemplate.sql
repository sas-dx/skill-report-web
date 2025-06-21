-- ============================================
-- テーブル: MST_ReportTemplate
-- 論理名: 帳票テンプレート
-- 説明: MST_ReportTemplate（帳票テンプレート）は、システムで生成する各種帳票のテンプレート情報を管理するマスタテーブルです。

主な目的：
- 帳票レイアウト・フォーマットの管理
- 帳票生成パラメータの管理
- 多言語対応の帳票テンプレート管理
- テナント別カスタマイズ対応
- 帳票出力形式の管理

このテーブルは、帳票・レポート機能において一貫性のある帳票出力を実現する重要なマスタデータです。

-- 作成日: 2025-06-21 17:20:34
-- ============================================

DROP TABLE IF EXISTS MST_ReportTemplate;

CREATE TABLE MST_ReportTemplate (
    id VARCHAR,
    tenant_id VARCHAR,
    template_key VARCHAR,
    template_name VARCHAR,
    report_category ENUM,
    output_format ENUM,
    language_code VARCHAR DEFAULT 'ja',
    template_content TEXT,
    style_sheet TEXT,
    parameters_schema TEXT,
    data_source_config TEXT,
    page_settings TEXT,
    header_template TEXT,
    footer_template TEXT,
    is_default BOOLEAN DEFAULT False,
    is_active BOOLEAN DEFAULT True,
    version VARCHAR DEFAULT '1.0.0',
    preview_image_url VARCHAR,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_report_template_tenant_key ON MST_ReportTemplate (tenant_id, template_key, language_code);
CREATE INDEX idx_report_template_category ON MST_ReportTemplate (report_category);
CREATE INDEX idx_report_template_format ON MST_ReportTemplate (output_format);
CREATE INDEX idx_report_template_language ON MST_ReportTemplate (language_code);
CREATE INDEX idx_report_template_default ON MST_ReportTemplate (is_default, is_active);
