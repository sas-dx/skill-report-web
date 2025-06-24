-- SYS_BackupHistory (バックアップ履歴) サンプルデータ
-- 生成日時: 2025-06-24 23:02:18

INSERT INTO SYS_BackupHistory (
    id, backup_end_time, backup_file_path, backup_file_size,
    backup_id, backup_scope, backup_start_time, backup_status,
    backup_trigger, backup_type, backuphistory_id, checksum,
    compression_type, encryption_enabled, error_message, executed_by,
    expiry_date, recovery_test_date, recovery_tested, retention_period_days,
    target_objects, is_deleted, created_at, updated_at
) VALUES
    (NULL, '2024-01-01 02:45:00', '/backup/full/skill_report_20240101_020000.sql.gz', 1073741824,
     'BKP_20240101_001', 'DATABASE', '2024-01-01 02:00:00', 'SUCCESS',
     'SCHEDULED', 'FULL', NULL, 'a1b2c3d4e5f6789012345678901234567890abcd',
     'GZIP', TRUE, NULL, 'system_backup_job',
     '2024-04-01', '2024-01-15', TRUE, 90,
     NULL, NULL, NULL, NULL),
    (NULL, '2024-01-01 14:05:00', '/backup/incremental/skill_report_20240101_140000.sql.gz', 52428800,
     'BKP_20240101_002', 'DATABASE', '2024-01-01 14:00:00', 'SUCCESS',
     'SCHEDULED', 'INCREMENTAL', NULL, 'b2c3d4e5f6789012345678901234567890abcde1',
     'GZIP', TRUE, NULL, 'system_backup_job',
     '2024-01-31', NULL, FALSE, 30,
     NULL, NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM SYS_BackupHistory ORDER BY created_at DESC;
