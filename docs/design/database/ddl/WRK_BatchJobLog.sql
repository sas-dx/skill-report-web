-- ============================================
-- テーブル: WRK_BatchJobLog
-- 論理名: 一括登録ジョブログ
-- 説明: 一括登録・更新処理のジョブ実行ログを管理するワーク系テーブル。

主な目的：
- バッチ処理の実行状況監視
- エラー発生時の原因調査・トラブルシューティング
- 処理結果の統計情報管理
- 一括処理の進捗追跡

このテーブルは一時的なワークテーブルとして機能し、
処理完了後は定期的にアーカイブ・削除される。
主に管理者画面での監視とAPI経由での状況確認に使用される。

-- 作成日: 2025-06-21 22:02:17
-- ============================================

DROP TABLE IF EXISTS WRK_BatchJobLog;

CREATE TABLE WRK_BatchJobLog (
    batchjoblog_id SERIAL NOT NULL COMMENT 'WRK_BatchJobLogの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    PRIMARY KEY (batchjoblog_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_wrk_batchjoblog_tenant_id ON WRK_BatchJobLog (tenant_id);

-- 外部キー制約
ALTER TABLE WRK_BatchJobLog ADD CONSTRAINT fk_WRK_BatchJobLog_executed_by FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE RESTRICT;
