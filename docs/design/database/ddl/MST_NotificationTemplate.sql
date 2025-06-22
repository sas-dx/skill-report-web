-- ============================================
-- テーブル: MST_NotificationTemplate
-- 論理名: 通知テンプレート
-- 説明: MST_NotificationTemplate（通知テンプレート）は、システムで使用する通知メッセージのテンプレートを管理するマスタテーブルです。

主な目的：
- 通知メッセージの定型文管理
- 多言語対応の通知テンプレート管理
- 通知チャネル別のテンプレート管理
- 動的パラメータを含むテンプレート管理
- テナント別カスタマイズ対応

このテーブルは、通知・連携管理機能において一貫性のあるメッセージ配信を実現する重要なマスタデータです。

-- 作成日: 2025-06-21 22:02:17
-- ============================================

DROP TABLE IF EXISTS MST_NotificationTemplate;

CREATE TABLE MST_NotificationTemplate (
    notificationtemplate_id SERIAL NOT NULL COMMENT 'MST_NotificationTemplateの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (notificationtemplate_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_notificationtemplate_tenant_id ON MST_NotificationTemplate (tenant_id);
