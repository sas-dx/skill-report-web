-- ============================================
-- テーブル: SYS_SystemLog
-- 論理名: システムログ
-- 説明: SYS_SystemLog（システムログ）は、アプリケーション全体で発生するあらゆるシステムイベントを記録・管理するログテーブルです。

主な目的：
- システム運用監視（エラー、警告、情報ログの記録）
- セキュリティ監査（認証、アクセス、操作履歴の追跡）
- パフォーマンス分析（レスポンス時間、処理時間の測定）
- 障害調査・デバッグ（詳細なエラー情報、スタックトレースの保存）
- 分散システムトレーシング（相関IDによるリクエスト追跡）
- コンプライアンス対応（法的要件に基づくログ保持）

このテーブルは、システムの安定運用、セキュリティ確保、問題解決の基盤となる重要なログ管理システムです。
大量データの効率的な管理のため、月次パーティション分割と自動アーカイブ機能を実装しています。

-- 作成日: 2025-06-21 22:02:17
-- ============================================

DROP TABLE IF EXISTS SYS_SystemLog;

CREATE TABLE SYS_SystemLog (
    systemlog_id SERIAL NOT NULL COMMENT 'SYS_SystemLogの主キー',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    PRIMARY KEY (systemlog_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 外部キー制約
ALTER TABLE SYS_SystemLog ADD CONSTRAINT fk_log_user FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
