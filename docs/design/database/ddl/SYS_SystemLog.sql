-- ============================================
-- テーブル: SYS_SystemLog
-- 論理名: システムログ
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS SYS_SystemLog;

CREATE TABLE SYS_SystemLog (
    log_level ENUM COMMENT 'ログレベル（ERROR:エラー、WARN:警告、INFO:情報、DEBUG:デバッグ）',
    log_category VARCHAR(50) COMMENT 'ログのカテゴリ（AUTH:認証、API:API、BATCH:バッチ、SYSTEM:システム）',
    message TEXT COMMENT 'ログメッセージの内容',
    user_id VARCHAR(50) COMMENT 'ログを発生させたユーザーのID（MST_UserAuthへの外部キー）',
    session_id VARCHAR(100) COMMENT 'セッションID（ユーザーセッションの識別）',
    ip_address VARCHAR(45) COMMENT 'クライアントのIPアドレス（IPv4/IPv6対応）',
    user_agent TEXT COMMENT 'クライアントのユーザーエージェント情報',
    request_url TEXT COMMENT 'リクエストされたURL',
    request_method VARCHAR(10) COMMENT 'HTTPメソッド（GET、POST、PUT、DELETE等）',
    response_status INT COMMENT 'HTTPレスポンスステータスコード',
    response_time INT COMMENT 'レスポンス時間（ミリ秒）',
    error_code VARCHAR(20) COMMENT 'アプリケーション固有のエラーコード',
    stack_trace TEXT COMMENT 'エラー発生時のスタックトレース',
    request_body TEXT COMMENT 'リクエストボディ（個人情報含む可能性があるため暗号化）',
    response_body TEXT COMMENT 'レスポンスボディ（個人情報含む可能性があるため暗号化）',
    correlation_id VARCHAR(100) COMMENT '分散システムでのトレーシング用相関ID',
    component_name VARCHAR(100) COMMENT 'ログを出力したコンポーネント名',
    thread_name VARCHAR(100) COMMENT 'ログを出力したスレッド名',
    server_name VARCHAR(100) COMMENT 'ログを出力したサーバー名',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    PRIMARY KEY (id)
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
ALTER TABLE SYS_SystemLog ADD CONSTRAINT fk_log_user FOREIGN KEY (user_id) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
ALTER TABLE SYS_SystemLog ADD CONSTRAINT chk_log_level CHECK (log_level IN ('ERROR', 'WARN', 'INFO', 'DEBUG'));
ALTER TABLE SYS_SystemLog ADD CONSTRAINT chk_response_status CHECK (response_status IS NULL OR (response_status >= 100 AND response_status <= 599));
ALTER TABLE SYS_SystemLog ADD CONSTRAINT chk_response_time CHECK (response_time IS NULL OR response_time >= 0);
