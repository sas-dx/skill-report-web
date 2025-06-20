-- サンプルデータ INSERT文: SYS_TenantUsage
-- 生成日時: 2025-06-21 07:31:30
-- レコード数: 2

BEGIN;

INSERT INTO SYS_TenantUsage (usage_date, tenant_id, active_users, total_logins, api_requests, data_storage_mb, file_storage_mb, backup_storage_mb, cpu_usage_minutes, memory_usage_mb_hours, network_transfer_mb, report_generations, skill_assessments, notification_sent, peak_concurrent_users, peak_time, error_count, response_time_avg_ms, uptime_percentage, billing_amount, collection_timestamp, id, created_at, updated_at, is_deleted) VALUES ('2024-01-15', 'TENANT001', 25, 47, 15420, 1024.5, 512.25, 256.75, 180.5, 2048.0, 128.3, 12, 35, 8, 18, '14:30:00', 2, 245.5, 99.95, 1250.0, '2024-01-16 02:00:00', 'sys_c86ec25d', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO SYS_TenantUsage (usage_date, tenant_id, active_users, total_logins, api_requests, data_storage_mb, file_storage_mb, backup_storage_mb, cpu_usage_minutes, memory_usage_mb_hours, network_transfer_mb, report_generations, skill_assessments, notification_sent, peak_concurrent_users, peak_time, error_count, response_time_avg_ms, uptime_percentage, billing_amount, collection_timestamp, id, created_at, updated_at, is_deleted) VALUES ('2024-01-15', 'TENANT002', 8, 12, 3240, 256.25, 128.5, 64.25, 45.25, 512.0, 32.1, 3, 8, 2, 6, '10:15:00', 0, 198.25, 100.0, 320.0, '2024-01-16 02:00:00', 'sys_a25bc1bf', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);

COMMIT;

-- SYS_TenantUsage サンプルデータ終了
