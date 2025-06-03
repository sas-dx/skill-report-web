-- ============================================
-- テーブル: MST_ReportTemplate
-- 論理名: 帳票テンプレート
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_ReportTemplate;

CREATE TABLE MST_ReportTemplate (
    id VARCHAR(50) COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) COMMENT 'マルチテナント識別子',
    template_key VARCHAR(100) COMMENT 'テンプレートの識別キー（例：skill_report、goal_summary等）',
    template_name VARCHAR(200) COMMENT 'テンプレートの表示名',
    report_category ENUM COMMENT '帳票の分類（SKILL:スキル関連、GOAL:目標関連、EVALUATION:評価関連、SUMMARY:サマリー、ANALYTICS:分析）',
    output_format ENUM COMMENT '帳票の出力形式（PDF:PDF、EXCEL:Excel、CSV:CSV、HTML:HTML）',
    language_code VARCHAR(10) DEFAULT 'ja' COMMENT 'テンプレートの言語（ja:日本語、en:英語等）',
    template_content TEXT COMMENT '帳票テンプレートの内容（HTML、XML等の形式）',
    style_sheet TEXT COMMENT '帳票のスタイル定義（CSS等）',
    parameters_schema TEXT COMMENT '帳票生成に必要なパラメータの定義（JSON Schema形式）',
    data_source_config TEXT COMMENT 'データ取得に関する設定（JSON形式）',
    page_settings TEXT COMMENT 'ページサイズ・余白等の設定（JSON形式）',
    header_template TEXT COMMENT '帳票ヘッダー部分のテンプレート',
    footer_template TEXT COMMENT '帳票フッター部分のテンプレート',
    is_default BOOLEAN DEFAULT False COMMENT '同一キー・カテゴリでのデフォルトテンプレートかどうか',
    is_active BOOLEAN DEFAULT True COMMENT 'テンプレートが有効かどうか',
    version VARCHAR(20) DEFAULT '1.0.0' COMMENT 'テンプレートのバージョン番号',
    preview_image_url VARCHAR(500) COMMENT 'テンプレートのプレビュー画像URL',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称',
    description TEXT COMMENT 'マスタ説明'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_report_template_tenant_key ON MST_ReportTemplate (tenant_id, template_key, language_code);
CREATE INDEX idx_report_template_category ON MST_ReportTemplate (report_category);
CREATE INDEX idx_report_template_format ON MST_ReportTemplate (output_format);
CREATE INDEX idx_report_template_language ON MST_ReportTemplate (language_code);
CREATE INDEX idx_report_template_default ON MST_ReportTemplate (is_default, is_active);

-- その他の制約
ALTER TABLE MST_ReportTemplate ADD CONSTRAINT uk_report_template_tenant_key_lang UNIQUE ();
ALTER TABLE MST_ReportTemplate ADD CONSTRAINT chk_report_template_category CHECK (report_category IN ('SKILL', 'GOAL', 'EVALUATION', 'SUMMARY', 'ANALYTICS'));
ALTER TABLE MST_ReportTemplate ADD CONSTRAINT chk_report_template_format CHECK (output_format IN ('PDF', 'EXCEL', 'CSV', 'HTML'));
ALTER TABLE MST_ReportTemplate ADD CONSTRAINT chk_report_template_language CHECK (language_code IN ('ja', 'en'));
