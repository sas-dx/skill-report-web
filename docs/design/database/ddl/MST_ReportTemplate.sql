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

-- 作成日: 2025-06-21 22:02:17
-- ============================================

DROP TABLE IF EXISTS MST_ReportTemplate;

CREATE TABLE MST_ReportTemplate (
    reporttemplate_id SERIAL NOT NULL COMMENT 'MST_ReportTemplateの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (reporttemplate_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_reporttemplate_tenant_id ON MST_ReportTemplate (tenant_id);
