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

-- 作成日: 2025-06-24 22:56:15
-- ============================================

DROP TABLE IF EXISTS MST_ReportTemplate;

CREATE TABLE MST_ReportTemplate (
    id VARCHAR(50) COMMENT 'ID',
    tenant_id VARCHAR(50) COMMENT 'テナントID',
    data_source_config TEXT COMMENT 'データソース設定',
    footer_template TEXT COMMENT 'フッターテンプレート',
    header_template TEXT COMMENT 'ヘッダーテンプレート',
    is_active BOOLEAN DEFAULT True COMMENT '有効フラグ',
    is_default BOOLEAN DEFAULT False COMMENT 'デフォルトフラグ',
    language_code VARCHAR(10) DEFAULT 'ja' COMMENT '言語コード',
    output_format ENUM('PDF', 'EXCEL', 'CSV', 'HTML') COMMENT '出力形式',
    page_settings TEXT COMMENT 'ページ設定',
    parameters_schema TEXT COMMENT 'パラメータスキーマ',
    preview_image_url VARCHAR(500) COMMENT 'プレビュー画像URL',
    report_category ENUM('SKILL', 'GOAL', 'EVALUATION', 'SUMMARY', 'ANALYTICS') COMMENT '帳票カテゴリ',
    reporttemplate_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_ReportTemplateの主キー',
    style_sheet TEXT COMMENT 'スタイルシート',
    template_content TEXT COMMENT 'テンプレート内容',
    template_key VARCHAR(100) COMMENT 'テンプレートキー',
    template_name VARCHAR(200) COMMENT 'テンプレート名',
    version VARCHAR(20) DEFAULT '1.0.0' COMMENT 'バージョン',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_report_template_tenant_key ON MST_ReportTemplate (tenant_id, template_key, language_code);
CREATE INDEX idx_report_template_category ON MST_ReportTemplate (report_category);
CREATE INDEX idx_report_template_format ON MST_ReportTemplate (output_format);
CREATE INDEX idx_report_template_language ON MST_ReportTemplate (language_code);
CREATE INDEX idx_report_template_default ON MST_ReportTemplate (is_default, is_active);
CREATE INDEX idx_mst_reporttemplate_tenant_id ON MST_ReportTemplate (tenant_id);

-- その他の制約
-- 制約DDL生成エラー: uk_report_template_tenant_key_lang
ALTER TABLE MST_ReportTemplate ADD CONSTRAINT chk_report_template_category CHECK (report_category IN ('SKILL', 'GOAL', 'EVALUATION', 'SUMMARY', 'ANALYTICS'));
ALTER TABLE MST_ReportTemplate ADD CONSTRAINT chk_report_template_format CHECK (output_format IN ('PDF', 'EXCEL', 'CSV', 'HTML'));
ALTER TABLE MST_ReportTemplate ADD CONSTRAINT chk_report_template_language CHECK (language_code IN ('ja', 'en'));
