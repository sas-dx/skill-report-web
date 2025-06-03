-- SYS_SystemLog (システムログ) サンプルデータ
-- 生成日時: 2025-06-04 06:57:02

INSERT INTO SYS_SystemLog (
    log_level, log_category, message, user_id,
    session_id, ip_address, user_agent, request_url,
    request_method, response_status, response_time, error_code,
    stack_trace, request_body, response_body, correlation_id,
    component_name, thread_name, server_name, id,
    is_deleted
) VALUES
    ('INFO', 'AUTH', 'ユーザーログイン成功', 'user001',
     'sess_abc123', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '/api/auth/login',
     'POST', 200, 150, NULL,
     NULL, NULL, NULL, 'corr_xyz789',
     'AuthService', 'http-nio-8080-exec-1', 'app-server-01', NULL,
     NULL),
    ('ERROR', 'API', 'データベース接続エラー', 'user002',
     'sess_def456', '192.168.1.101', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '/api/employees',
     'GET', 500, 5000, 'DB_CONNECTION_ERROR',
     'java.sql.SQLException: Connection timeout...', NULL, NULL, 'corr_abc456',
     'EmployeeService', 'http-nio-8080-exec-2', 'app-server-02', NULL,
     NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM SYS_SystemLog ORDER BY created_at DESC;
