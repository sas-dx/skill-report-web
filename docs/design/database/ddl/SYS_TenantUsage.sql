-- ============================================
-- テーブル: SYS_TenantUsage
-- 論理名: テナント利用状況
-- 説明: テナント利用状況テーブルは、マルチテナント環境における各テナントのシステム利用状況を管理するシステムテーブルです。

主な目的：
- テナント別のリソース使用量監視
- 課金情報の基礎データ収集
- システム負荷分析とキャパシティプランニング
- SLA監視とパフォーマンス分析

このテーブルは、マルチテナントシステムの運用管理と課金処理を支える重要なテーブルで、
テナント毎の公平なリソース配分と適切な課金を実現します。

-- 作成日: 2025-06-21 22:02:17
-- ============================================

DROP TABLE IF EXISTS SYS_TenantUsage;

CREATE TABLE SYS_TenantUsage (
    tenantusage_id SERIAL NOT NULL COMMENT 'SYS_TenantUsageの主キー',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    PRIMARY KEY (tenantusage_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 外部キー制約
ALTER TABLE SYS_TenantUsage ADD CONSTRAINT fk_SYS_TenantUsage_tenant FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
