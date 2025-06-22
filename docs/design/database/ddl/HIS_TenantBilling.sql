-- ============================================
-- テーブル: HIS_TenantBilling
-- 論理名: テナント課金履歴
-- 説明: HIS_TenantBilling（テナント課金履歴）は、マルチテナントシステムにおける各テナントの課金情報を履歴として管理するテーブルです。

主な目的：
- テナント別課金履歴の管理
- 使用量ベース課金の計算履歴
- 請求書発行のための基礎データ管理
- 課金監査のための証跡管理
- 収益分析のためのデータ蓄積

このテーブルは、マルチテナント管理機能において課金・請求業務を支える重要な履歴データです。

-- 作成日: 2025-06-21 22:02:17
-- ============================================

DROP TABLE IF EXISTS HIS_TenantBilling;

CREATE TABLE HIS_TenantBilling (
    tenantbilling_id SERIAL NOT NULL COMMENT 'HIS_TenantBillingの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    PRIMARY KEY (tenantbilling_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_his_tenantbilling_tenant_id ON HIS_TenantBilling (tenant_id);

-- 外部キー制約
ALTER TABLE HIS_TenantBilling ADD CONSTRAINT fk_tenant_billing_tenant FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE RESTRICT;
