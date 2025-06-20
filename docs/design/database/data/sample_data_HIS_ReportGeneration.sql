-- サンプルデータ INSERT文: HIS_ReportGeneration
-- 生成日時: 2025-06-21 07:31:30
-- レコード数: 2

BEGIN;

INSERT INTO HIS_ReportGeneration (id, tenant_id, template_id, requested_by, report_title, report_category, output_format, generation_status, parameters, file_path, file_size, download_count, last_downloaded_at, requested_at, started_at, completed_at, processing_time_ms, error_message, error_details, expires_at, created_at, updated_at, is_deleted) VALUES ('RG001', 'TENANT001', 'RT001', 'USER001', '山田太郎さんのスキルサマリーレポート', 'SKILL', 'PDF', 'SUCCESS', '{"employee_id": "EMP001", "report_date": "2025-06-01"}', '/reports/2025/06/01/skill_summary_EMP001_20250601.pdf', 1048576, 3, '2025-06-01 18:45:00', '2025-06-01 15:30:00', '2025-06-01 15:30:05', '2025-06-01 15:30:25', 20000, NULL, NULL, '2025-06-08 15:30:00', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO HIS_ReportGeneration (id, tenant_id, template_id, requested_by, report_title, report_category, output_format, generation_status, parameters, file_path, file_size, download_count, last_downloaded_at, requested_at, started_at, completed_at, processing_time_ms, error_message, error_details, expires_at, created_at, updated_at, is_deleted) VALUES ('RG002', 'TENANT001', 'RT002', 'USER002', '開発部目標進捗レポート', 'GOAL', 'EXCEL', 'FAILED', '{"department_id": "DEPT001", "period_start": "2025-05-01", "period_end": "2025-05-31"}', NULL, NULL, 0, NULL, '2025-06-01 16:00:00', '2025-06-01 16:00:10', '2025-06-01 16:00:15', 5000, 'データ取得エラー: 指定された期間のデータが見つかりません', '{"error_code": "DATA_NOT_FOUND", "sql_error": "No rows found for the specified period"}', NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);

COMMIT;

-- HIS_ReportGeneration サンプルデータ終了
