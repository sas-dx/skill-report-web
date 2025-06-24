-- WRK_BatchJobLog (一括登録ジョブログ) サンプルデータ
-- 生成日時: 2025-06-24 22:56:14

INSERT INTO WRK_BatchJobLog (
    id, tenant_id, job_id, batchjoblog_id,
    end_time, error_details, error_records, executed_by,
    execution_environment, input_file_path, job_name, job_parameters,
    job_type, output_file_path, processed_records, progress_percentage,
    start_time, status, success_records, total_records,
    is_deleted, created_at, updated_at
) VALUES
    (NULL, NULL, 'JOB-001-20250601-001', NULL,
     '2025-06-01 09:15:30', '{"errors": [{"row": 23, "column": "skill_level", "message": "無効なスキルレベル値"}, {"row": 45, "column": "employee_id", "message": "存在しない社員ID"}]}', 15, 'admin001',
     'batch-server-01:12345', '/uploads/skill_import_20250601.csv', 'スキル情報一括登録（2025年6月分）', '{"delimiter": ",", "encoding": "UTF-8", "skip_header": true}',
     'SKILL_IMPORT', '/reports/skill_import_error_20250601.csv', 500, 100.0,
     '2025-06-01 09:00:00', 'COMPLETED', 485, 500,
     NULL, NULL, NULL),
    (NULL, NULL, 'JOB-002-20250601-002', NULL,
     NULL, '{"errors": [{"row": 15, "column": "department_id", "message": "存在しない部署ID"}]}', 10, 'hr_manager001',
     'batch-server-02:23456', '/uploads/employee_update_20250601.csv', '社員部署情報一括更新', '{"update_mode": "partial", "validate_only": false}',
     'BULK_UPDATE', NULL, 650, 65.0,
     '2025-06-01 14:30:00', 'RUNNING', 640, 1000,
     NULL, NULL, NULL),
    (NULL, NULL, 'JOB-003-20250601-003', NULL,
     '2025-06-01 16:05:15', '{"system_error": "データベース接続エラー", "error_code": "DB_CONNECTION_TIMEOUT"}', 0, 'system_admin001',
     'batch-server-01:34567', NULL, '全社員スキルデータエクスポート', '{"format": "CSV", "include_deleted": false}',
     'DATA_EXPORT', '/exports/skill_data_20250601.csv', 0, 0.0,
     '2025-06-01 16:00:00', 'FAILED', 0, 0,
     NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM WRK_BatchJobLog ORDER BY created_at DESC;
