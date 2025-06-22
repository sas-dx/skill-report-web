-- ============================================
-- テーブル: MST_NotificationSettings
-- 論理名: 通知設定
-- 説明: MST_NotificationSettings（通知設定）は、システム全体の通知機能に関する設定情報を管理するマスタテーブルです。

主な目的：
- 通知チャネル（メール、Slack、Teams等）の設定管理
- 通知タイミング・頻度の制御設定
- 通知対象者・グループの設定管理
- 通知テンプレートとの紐付け設定
- テナント別通知設定の管理

このテーブルは、通知・連携管理機能の基盤となる重要なマスタデータです。

-- 作成日: 2025-06-21 22:02:17
-- ============================================

DROP TABLE IF EXISTS MST_NotificationSettings;

CREATE TABLE MST_NotificationSettings (
    notificationsettings_id SERIAL NOT NULL COMMENT 'MST_NotificationSettingsの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (notificationsettings_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_notificationsettings_tenant_id ON MST_NotificationSettings (tenant_id);

-- 外部キー制約
ALTER TABLE MST_NotificationSettings ADD CONSTRAINT fk_notification_settings_template FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
