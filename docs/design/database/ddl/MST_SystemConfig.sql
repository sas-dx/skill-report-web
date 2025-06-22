-- ============================================
-- テーブル: MST_SystemConfig
-- 論理名: システム設定
-- 説明: MST_SystemConfig（システム設定）は、システム全体の設定値・パラメータを管理するマスタテーブルです。

主な目的：
- システム運用パラメータの一元管理
- 機能ON/OFF設定の管理
- 業務ルール・閾値の設定管理
- 外部連携設定の管理
- セキュリティ設定の管理

このテーブルにより、システムの動作を柔軟に制御し、
運用環境に応じた設定変更を効率的に行うことができます。

-- 作成日: 2025-06-21 22:02:18
-- ============================================

DROP TABLE IF EXISTS MST_SystemConfig;

CREATE TABLE MST_SystemConfig (
    systemconfig_id SERIAL NOT NULL COMMENT 'MST_SystemConfigの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (systemconfig_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_systemconfig_tenant_id ON MST_SystemConfig (tenant_id);
