-- SYS_TenantUsage (テナント利用状況) サンプルデータ
-- 生成日時: 2025-06-21 17:20:34

INSERT INTO SYS_TenantUsage (
    usage_date, tenant_id, active_users, total_logins,
    api_requests, data_storage_mb, file_storage_mb, backup_storage_mb,
    cpu_usage_minutes, memory_usage_mb_hours, network_transfer_mb, report_generations,
    skill_assessments, notification_sent, peak_concurrent_users, peak_time,
    error_count, response_time_avg_ms, uptime_percentage, billing_amount,
    collection_timestamp, id, is_deleted
) VALUES
    ('2024-01-15', 'TENANT001', 25, 47,
     15420, 1024.5, 512.25, 256.75,
     180.5, 2048.0, 128.3, 12,
     35, 8, 18, '14:30:00',
     2, 245.5, 99.95, 1250.0,
     '2024-01-16 02:00:00', NULL, NULL),
    ('2024-01-15', 'TENANT002', 8, 12,
     3240, 256.25, 128.5, 64.25,
     45.25, 512.0, 32.1, 3,
     8, 2, 6, '10:15:00',
     0, 198.25, 100.0, 320.0,
     '2024-01-16 02:00:00', NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM SYS_TenantUsage ORDER BY created_at DESC;
