-- ============================================
-- テーブル: TRN_Notification
-- 論理名: 通知履歴
-- 説明: TRN_Notification（通知履歴）は、システムから送信された各種通知の履歴を管理するトランザクションテーブルです。

主な目的：
- 通知送信履歴の記録・管理
- 通知配信状況の追跡
- 通知効果の分析
- 未読通知の管理
- 通知設定の最適化支援

このテーブルにより、効果的な情報伝達を実現し、
重要な情報の確実な配信と適切なコミュニケーションを支援できます。

-- 作成日: 2025-06-21 22:02:17
-- ============================================

DROP TABLE IF EXISTS TRN_Notification;

CREATE TABLE TRN_Notification (
    notification_id SERIAL NOT NULL COMMENT 'TRN_Notificationの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    created_by VARCHAR(50) NOT NULL COMMENT 'レコード作成者のユーザーID',
    updated_by VARCHAR(50) NOT NULL COMMENT 'レコード更新者のユーザーID',
    PRIMARY KEY (notification_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_trn_notification_tenant_id ON TRN_Notification (tenant_id);

-- 外部キー制約
ALTER TABLE TRN_Notification ADD CONSTRAINT fk_notification_recipient FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_Notification ADD CONSTRAINT fk_notification_sender FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
