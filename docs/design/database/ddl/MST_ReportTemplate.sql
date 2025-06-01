-- MST_ReportTemplate (帳票テンプレート) DDL
-- 生成日時: 2025-06-01 20:40:25

CREATE TABLE MST_ReportTemplate (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    tenant_id VARCHAR(50) NOT NULL,
    id VARCHAR(50),
    tenant_id VARCHAR(50),
    template_key VARCHAR(100),
    template_name VARCHAR(200),
    report_category ENUM,
    output_format ENUM,
    language_code VARCHAR(10) DEFAULT 'ja',
    template_content TEXT,
    style_sheet TEXT,
    parameters_schema TEXT,
    data_source_config TEXT,
    page_settings TEXT,
    header_template TEXT,
    footer_template TEXT,
    is_default BOOLEAN DEFAULT False,
    is_active BOOLEAN DEFAULT True,
    version VARCHAR(20) DEFAULT '1.0.0',
    preview_image_url VARCHAR(500),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX idx_report_template_tenant_key ON MST_ReportTemplate (tenant_id, template_key, language_code);
CREATE INDEX idx_report_template_category ON MST_ReportTemplate (report_category);
CREATE INDEX idx_report_template_format ON MST_ReportTemplate (output_format);
CREATE INDEX idx_report_template_language ON MST_ReportTemplate (language_code);
CREATE INDEX idx_report_template_default ON MST_ReportTemplate (is_default, is_active);

-- 外部キー制約
