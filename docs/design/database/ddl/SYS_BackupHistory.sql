-- ============================================
-- テーブル: SYS_BackupHistory
-- 論理名: バックアップ履歴
-- 説明: バックアップ履歴テーブルは、システムのデータバックアップ実行履歴を管理するシステムテーブルです。

主な目的：
- データベースバックアップの実行履歴管理
- バックアップの成功・失敗状況の記録
- バックアップファイルの保存場所管理
- 復旧時のバックアップ選択支援

このテーブルは、システムの可用性とデータ保護を支える重要なテーブルで、
障害時の迅速な復旧とデータ整合性の確保に貢献します。

-- 作成日: 2025-06-21 22:02:18
-- ============================================

DROP TABLE IF EXISTS SYS_BackupHistory;

CREATE TABLE SYS_BackupHistory (
    backuphistory_id SERIAL NOT NULL COMMENT 'SYS_BackupHistoryの主キー',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    PRIMARY KEY (backuphistory_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
