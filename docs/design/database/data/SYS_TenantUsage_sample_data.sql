-- SYS_TenantUsage (テナント利用状況) サンプルデータ
-- 生成日時: 2025-06-24 23:02:18

INSERT INTO SYS_TenantUsage (
    id, tenant_id, active_users, api_requests,
    backup_storage_mb, billing_amount, collection_timestamp, cpu_usage_minutes,
    data_storage_mb, error_count, file_storage_mb, memory_usage_mb_hours,
    network_transfer_mb, notification_sent, peak_concurrent_users, peak_time,
    report_generations, response_time_avg_ms, skill_assessments, tenantusage_id,
    total_logins, uptime_percentage, usage_date, is_deleted,
    created_at, updated_at
) VALUES
    (NULL, 'TENANT001', 25, 15420,
     256.75, 1250.0, '2024-01-16 02:00:00', 180.5,
     1024.5, 2, 512.25, 2048.0,
     128.3, 8, 18, '14:30:00',
     12, 245.5, 35, NULL,
     47, 99.95, '2024-01-15', NULL,
     NULL, NULL),
    (NULL, 'TENANT002', 8, 3240,
     64.25, 320.0, '2024-01-16 02:00:00', 45.25,
     256.25, 0, 128.5, 512.0,
     32.1, 2, 6, '10:15:00',
     3, 198.25, 8, NULL,
     12, 100.0, '2024-01-15', NULL,
     NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM SYS_TenantUsage ORDER BY created_at DESC;
