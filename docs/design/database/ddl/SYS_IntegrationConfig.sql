-- ============================================
-- テーブル: SYS_IntegrationConfig
-- 論理名: 外部連携設定
-- 説明: SYS_IntegrationConfig（外部連携設定）は、外部システムとの連携に必要な設定情報を管理するシステムテーブルです。

主な目的：
- 外部API接続設定の管理
- 認証情報・エンドポイント情報の管理
- 連携パラメータ・設定値の管理
- 外部システム別設定の管理
- テナント別連携設定の管理

このテーブルは、通知・連携管理機能において外部システムとの安全で効率的な連携を実現する重要なシステムデータです。

-- 作成日: 2025-06-21 22:02:18
-- ============================================

DROP TABLE IF EXISTS SYS_IntegrationConfig;

CREATE TABLE SYS_IntegrationConfig (
    integrationconfig_id SERIAL NOT NULL COMMENT 'SYS_IntegrationConfigの主キー',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    PRIMARY KEY (integrationconfig_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
