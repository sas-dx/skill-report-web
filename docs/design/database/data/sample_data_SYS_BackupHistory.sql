-- サンプルデータ INSERT文: SYS_BackupHistory
-- 生成日時: 2025-06-21 07:31:30
-- レコード数: 2

BEGIN;

INSERT INTO SYS_BackupHistory (backup_id, backup_type, backup_scope, target_objects, backup_start_time, backup_end_time, backup_status, backup_file_path, backup_file_size, compression_type, encryption_enabled, checksum, retention_period_days, expiry_date, backup_trigger, executed_by, error_message, recovery_tested, recovery_test_date, id, created_at, updated_at, is_deleted) VALUES ('BKP_20240101_001', 'FULL', 'DATABASE', NULL, '2024-01-01 02:00:00', '2024-01-01 02:45:00', 'SUCCESS', '/backup/full/skill_report_20240101_020000.sql.gz', 1073741824, 'GZIP', TRUE, 'a1b2c3d4e5f6789012345678901234567890abcd', 90, '2024-04-01', 'SCHEDULED', 'system_backup_job', NULL, TRUE, '2024-01-15', 'sys_43bd4d99', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO SYS_BackupHistory (backup_id, backup_type, backup_scope, target_objects, backup_start_time, backup_end_time, backup_status, backup_file_path, backup_file_size, compression_type, encryption_enabled, checksum, retention_period_days, expiry_date, backup_trigger, executed_by, error_message, recovery_tested, recovery_test_date, id, created_at, updated_at, is_deleted) VALUES ('BKP_20240101_002', 'INCREMENTAL', 'DATABASE', NULL, '2024-01-01 14:00:00', '2024-01-01 14:05:00', 'SUCCESS', '/backup/incremental/skill_report_20240101_140000.sql.gz', 52428800, 'GZIP', TRUE, 'b2c3d4e5f6789012345678901234567890abcde1', 30, '2024-01-31', 'SCHEDULED', 'system_backup_job', NULL, FALSE, NULL, 'sys_00b368e0', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);

COMMIT;

-- SYS_BackupHistory サンプルデータ終了
