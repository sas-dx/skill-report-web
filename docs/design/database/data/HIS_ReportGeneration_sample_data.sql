-- HIS_ReportGeneration (帳票生成履歴) サンプルデータ
-- 生成日時: 2025-06-24 23:02:18

INSERT INTO HIS_ReportGeneration (
    id, tenant_id, completed_at, download_count,
    error_details, error_message, expires_at, file_path,
    file_size, generation_status, last_downloaded_at, output_format,
    parameters, processing_time_ms, report_category, report_title,
    reportgeneration_id, requested_at, requested_by, started_at,
    template_id, is_deleted, created_at, updated_at
) VALUES
    ('RG001', 'TENANT001', '2025-06-01 15:30:25', 3,
     NULL, NULL, '2025-06-08 15:30:00', '/reports/2025/06/01/skill_summary_EMP001_20250601.pdf',
     1048576, 'SUCCESS', '2025-06-01 18:45:00', 'PDF',
     '{"employee_id": "EMP001", "report_date": "2025-06-01"}', 20000, 'SKILL', '山田太郎さんのスキルサマリーレポート',
     NULL, '2025-06-01 15:30:00', 'USER001', '2025-06-01 15:30:05',
     'RT001', NULL, NULL, NULL),
    ('RG002', 'TENANT001', '2025-06-01 16:00:15', 0,
     '{"error_code": "DATA_NOT_FOUND", "sql_error": "No rows found for the specified period"}', 'データ取得エラー: 指定された期間のデータが見つかりません', NULL, NULL,
     NULL, 'FAILED', NULL, 'EXCEL',
     '{"department_id": "DEPT001", "period_start": "2025-05-01", "period_end": "2025-05-31"}', 5000, 'GOAL', '開発部目標進捗レポート',
     NULL, '2025-06-01 16:00:00', 'USER002', '2025-06-01 16:00:10',
     'RT002', NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM HIS_ReportGeneration ORDER BY created_at DESC;
