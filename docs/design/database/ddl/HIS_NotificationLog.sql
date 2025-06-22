-- ============================================
-- テーブル: HIS_NotificationLog
-- 論理名: 通知送信履歴
-- 説明: HIS_NotificationLog（通知送信履歴）は、システムから送信された全ての通知の履歴を管理するテーブルです。

主な目的：
- 通知送信の履歴管理
- 送信成功・失敗の記録
- 通知配信の監査証跡
- 通知システムの分析・改善データ
- 再送処理のための情報管理

このテーブルは、通知・連携管理機能において送信状況の把握と品質向上を支える重要な履歴データです。

-- 作成日: 2025-06-21 22:02:18
-- ============================================

DROP TABLE IF EXISTS HIS_NotificationLog;

CREATE TABLE HIS_NotificationLog (
    notificationlog_id SERIAL NOT NULL COMMENT 'HIS_NotificationLogの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    PRIMARY KEY (notificationlog_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_his_notificationlog_tenant_id ON HIS_NotificationLog (tenant_id);

-- 外部キー制約
ALTER TABLE HIS_NotificationLog ADD CONSTRAINT fk_notification_log_notification FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE HIS_NotificationLog ADD CONSTRAINT fk_notification_log_setting FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE HIS_NotificationLog ADD CONSTRAINT fk_notification_log_template FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE HIS_NotificationLog ADD CONSTRAINT fk_notification_log_integration FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
