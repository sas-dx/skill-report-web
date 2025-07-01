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

-- 作成日: 2025-06-24 23:05:57
-- ============================================

DROP TABLE IF EXISTS SYS_SystemLog;

CREATE TABLE SYS_SystemLog (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) COMMENT 'テナントID',
    log_level ENUM('ERROR', 'WARN', 'INFO', 'DEBUG') COMMENT 'ログレベル',
    message TEXT COMMENT 'ログメッセージ',
    component_name VARCHAR(100) COMMENT 'コンポーネント名',
    user_id VARCHAR(50) COMMENT '実行ユーザーID',
    session_id VARCHAR(100) COMMENT 'セッションID',
    correlation_id VARCHAR(100) COMMENT '相関ID',
    error_code VARCHAR(20) COMMENT 'エラーコード',
    stack_trace TEXT COMMENT 'スタックトレース',
    request_url TEXT COMMENT 'リクエストURL',
    request_method VARCHAR(10) COMMENT 'HTTPメソッド',
    request_body TEXT COMMENT 'リクエストボディ',
    response_status INT COMMENT 'レスポンスステータス',
    response_body TEXT COMMENT 'レスポンスボディ',
    user_agent TEXT COMMENT 'ユーザーエージェント',
    ip_address VARCHAR(45) COMMENT 'IPアドレス',
    log_category VARCHAR(50) COMMENT 'ログカテゴリ',
    response_time INT COMMENT 'レスポンス時間',
    server_name VARCHAR(100) COMMENT 'サーバー名',
    thread_name VARCHAR(100) COMMENT 'スレッド名',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_log_level ON SYS_SystemLog (log_level);
CREATE INDEX idx_log_category ON SYS_SystemLog (log_category);
CREATE INDEX idx_user_id ON SYS_SystemLog (user_id);
CREATE INDEX idx_session_id ON SYS_SystemLog (session_id);
CREATE INDEX idx_ip_address ON SYS_SystemLog (ip_address);
CREATE INDEX idx_error_code ON SYS_SystemLog (error_code);
CREATE INDEX idx_correlation_id ON SYS_SystemLog (correlation_id);
CREATE INDEX idx_component ON SYS_SystemLog (component_name);
CREATE INDEX idx_server ON SYS_SystemLog (server_name);
CREATE INDEX idx_response_time ON SYS_SystemLog (response_time);
CREATE INDEX idx_created_at_level ON SYS_SystemLog (created_at, log_level);

-- 外部キー制約
ALTER TABLE SYS_SystemLog ADD CONSTRAINT fk_log_user FOREIGN KEY (user_id) REFERENCES MST_UserAuth(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
ALTER TABLE SYS_SystemLog ADD CONSTRAINT chk_log_level CHECK (log_level IN ('ERROR', 'WARN', 'INFO', 'DEBUG'));
ALTER TABLE SYS_SystemLog ADD CONSTRAINT chk_response_status CHECK (response_status IS NULL OR (response_status >= 100 AND response_status <= 599));
ALTER TABLE SYS_SystemLog ADD CONSTRAINT chk_response_time CHECK (response_time IS NULL OR response_time >= 0);
