-- SYS_SystemLog (システムログ) DDL
-- 生成日時: 2025-06-01 13:28:12

CREATE TABLE SYS_SystemLog (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    is_deleted BOOLEAN NOT NULL DEFAULT False,
    log_level ENUM,
    log_category VARCHAR(50),
    message TEXT,
    user_id VARCHAR(50),
    session_id VARCHAR(100),
    ip_address VARCHAR(45),
    user_agent TEXT,
    request_url TEXT,
    request_method VARCHAR(10),
    response_status INT,
    response_time INT,
    error_code VARCHAR(20),
    stack_trace TEXT,
    request_body TEXT,
    response_body TEXT,
    correlation_id VARCHAR(100),
    component_name VARCHAR(100),
    thread_name VARCHAR(100),
    server_name VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

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
