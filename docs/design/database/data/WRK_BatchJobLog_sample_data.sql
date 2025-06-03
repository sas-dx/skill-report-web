-- WRK_BatchJobLog (一括登録ジョブログ) サンプルデータ
-- 生成日時: 2025-06-04 06:57:02

INSERT INTO WRK_BatchJobLog (
    job_id, job_name, job_type, status,
    start_time, end_time, total_records, processed_records,
    success_records, error_records, error_details, input_file_path,
    output_file_path, executed_by, progress_percentage, execution_environment,
    job_parameters, id, is_deleted
) VALUES
    ('JOB-001-20250601-001', 'スキル情報一括登録（2025年6月分）', 'SKILL_IMPORT', 'COMPLETED',
     '2025-06-01 09:00:00', '2025-06-01 09:15:30', 500, 500,
     485, 15, '{"errors": [{"row": 23, "column": "skill_level", "message": "無効なスキルレベル値"}, {"row": 45, "column": "employee_id", "message": "存在しない社員ID"}]}', '/uploads/skill_import_20250601.csv',
     '/reports/skill_import_error_20250601.csv', 'admin001', 100.0, 'batch-server-01:12345',
     '{"delimiter": ",", "encoding": "UTF-8", "skip_header": true}', NULL, NULL),
    ('JOB-002-20250601-002', '社員部署情報一括更新', 'BULK_UPDATE', 'RUNNING',
     '2025-06-01 14:30:00', NULL, 1000, 650,
     640, 10, '{"errors": [{"row": 15, "column": "department_id", "message": "存在しない部署ID"}]}', '/uploads/employee_update_20250601.csv',
     NULL, 'hr_manager001', 65.0, 'batch-server-02:23456',
     '{"update_mode": "partial", "validate_only": false}', NULL, NULL),
    ('JOB-003-20250601-003', '全社員スキルデータエクスポート', 'DATA_EXPORT', 'FAILED',
     '2025-06-01 16:00:00', '2025-06-01 16:05:15', 0, 0,
     0, 0, '{"system_error": "データベース接続エラー", "error_code": "DB_CONNECTION_TIMEOUT"}', NULL,
     '/exports/skill_data_20250601.csv', 'system_admin001', 0.0, 'batch-server-01:34567',
     '{"format": "CSV", "include_deleted": false}', NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM WRK_BatchJobLog ORDER BY created_at DESC;
