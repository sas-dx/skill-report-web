-- サンプルデータ INSERT文: SYS_SystemLog
-- 生成日時: 2025-06-21 22:54:40
-- レコード数: 2

INSERT INTO SYS_SystemLog (log_level, log_category, message, user_id, session_id, ip_address, user_agent, request_url, request_method, response_status, response_time, error_code, stack_trace, correlation_id, component_name, thread_name, server_name, id, created_at, updated_at, is_deleted) VALUES ('INFO', 'AUTH', 'ユーザーログイン成功', 'user001', 'sess_abc123', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '/api/auth/login', 'POST', 200, 150, NULL, NULL, 'corr_xyz789', 'AuthService', 'http-nio-8080-exec-1', 'app-server-01', 'sys_223569b1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO SYS_SystemLog (log_level, log_category, message, user_id, session_id, ip_address, user_agent, request_url, request_method, response_status, response_time, error_code, stack_trace, correlation_id, component_name, thread_name, server_name, id, created_at, updated_at, is_deleted) VALUES ('ERROR', 'API', 'データベース接続エラー', 'user002', 'sess_def456', '192.168.1.101', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '/api/employees', 'GET', 500, 5000, 'DB_CONNECTION_ERROR', 'java.sql.SQLException: Connection timeout...', 'corr_abc456', 'EmployeeService', 'http-nio-8080-exec-2', 'app-server-02', 'sys_86bdd2ab', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);

-- SYS_SystemLog サンプルデータ終了
