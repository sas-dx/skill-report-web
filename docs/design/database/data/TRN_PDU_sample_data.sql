-- TRN_PDU (継続教育ポイント) サンプルデータ
-- 生成日時: 2025-06-04 06:57:02

INSERT INTO TRN_PDU (
    pdu_id, employee_id, certification_id, activity_type,
    activity_name, activity_description, provider_name, activity_date,
    start_time, end_time, duration_hours, pdu_points,
    pdu_category, pdu_subcategory, location, cost,
    cost_covered_by, evidence_type, evidence_file_path, certificate_number,
    instructor_name, learning_objectives, learning_outcomes, skills_developed,
    approval_status, approved_by, approval_date, approval_comment,
    expiry_date, is_recurring, recurrence_pattern, related_training_id,
    related_project_id, id, is_deleted, tenant_id,
    created_at, updated_at, created_by, updated_by
) VALUES
    ('PDU_001', 'EMP000001', 'CERT_PMP_001', 'TRAINING',
     'アジャイル開発手法研修', 'スクラム・カンバンを中心としたアジャイル開発手法の実践研修', 'アジャイル協会', '2024-03-15',
     '09:00:00', '17:00:00', 8.0, 8.0,
     'TECHNICAL', 'Development Methods', '東京研修センター', 50000,
     'COMPANY', 'CERTIFICATE', '/evidence/pdu/PDU_001_certificate.pdf', 'AGILE-2024-001',
     '山田講師', 'アジャイル開発手法の理解と実践スキル習得', 'スクラム・カンバンの基礎理解、実際のプロジェクトへの適用方法を習得', '["アジャイル開発", "スクラム", "カンバン", "チーム運営"]',
     'APPROVED', 'EMP000020', '2024-03-20', 'PMP資格維持に適切なPDU活動として承認',
     '2027-03-15', FALSE, NULL, 'TRN_HIS_003',
     NULL, NULL, NULL, NULL,
     NULL, NULL, NULL, NULL),
    ('PDU_002', 'EMP000002', 'CERT_AWS_001', 'CONFERENCE',
     'AWS re:Invent 2024', 'AWSの最新技術動向とベストプラクティスに関するカンファレンス', 'Amazon Web Services', '2024-11-28',
     NULL, NULL, 32.0, 32.0,
     'TECHNICAL', 'Cloud Technologies', 'ラスベガス（オンライン参加）', 200000,
     'COMPANY', 'ATTENDANCE', '/evidence/pdu/PDU_002_attendance.pdf', NULL,
     NULL, 'AWS最新技術の習得とクラウドアーキテクチャスキル向上', '最新のAWSサービス理解、セキュリティベストプラクティス習得', '["AWS最新技術", "クラウドセキュリティ", "サーバーレス", "機械学習"]',
     'APPROVED', 'EMP000020', '2024-12-05', 'AWS認定維持に有効なPDU活動として承認',
     '2027-11-28', FALSE, NULL, NULL,
     'PRJ_REC_002', NULL, NULL, NULL,
     NULL, NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM TRN_PDU ORDER BY created_at DESC;
