-- ============================================
-- テーブル: MST_TenantSettings
-- 論理名: テナント設定
-- 説明: MST_TenantSettings（テナント設定）は、マルチテナントシステムにおける各テナント固有の設定情報を管理するマスタテーブルです。

主な目的：
- テナント別システム設定の管理
- 機能有効/無効の制御設定
- UI・表示設定のカスタマイズ
- 業務ルール・制限値の設定
- 外部連携設定の管理

このテーブルは、マルチテナント管理機能において各テナントの個別要件に対応する重要なマスタデータです。

-- 作成日: 2025-06-21 22:02:17
-- ============================================

DROP TABLE IF EXISTS MST_TenantSettings;

CREATE TABLE MST_TenantSettings (
    tenantsettings_id SERIAL NOT NULL COMMENT 'MST_TenantSettingsの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (tenantsettings_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_tenantsettings_tenant_id ON MST_TenantSettings (tenant_id);

-- 外部キー制約
ALTER TABLE MST_TenantSettings ADD CONSTRAINT fk_tenant_settings_tenant FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
