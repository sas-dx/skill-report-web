-- SYS_SystemLog (システムログ) サンプルデータ
-- 生成日時: 2025-06-24 23:02:19

INSERT INTO SYS_SystemLog (
    id, tenant_id, log_level, message,
    component_name, user_id, session_id, correlation_id,
    error_code, stack_trace, request_url, request_method,
    request_body, response_status, response_body, user_agent,
    ip_address, log_category, response_time, server_name,
    thread_name, is_deleted, created_at, updated_at
) VALUES
    (NULL, NULL, 'INFO', 'ユーザーログイン成功',
     'AuthService', 'user001', 'sess_abc123', 'corr_xyz789',
     NULL, NULL, '/api/auth/login', 'POST',
     NULL, 200, NULL, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
     '192.168.1.100', 'AUTH', 150, 'app-server-01',
     'http-nio-8080-exec-1', NULL, NULL, NULL),
    (NULL, NULL, 'ERROR', 'データベース接続エラー',
     'EmployeeService', 'user002', 'sess_def456', 'corr_abc456',
     'DB_CONNECTION_ERROR', 'java.sql.SQLException: Connection timeout...', '/api/employees', 'GET',
     NULL, 500, NULL, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
     '192.168.1.101', 'API', 5000, 'app-server-02',
     'http-nio-8080-exec-2', NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM SYS_SystemLog ORDER BY created_at DESC;
