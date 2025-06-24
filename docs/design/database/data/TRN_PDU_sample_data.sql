-- TRN_PDU (継続教育ポイント) サンプルデータ
-- 生成日時: 2025-06-24 23:05:57

INSERT INTO TRN_PDU (
    id, tenant_id, activity_date, activity_description,
    activity_name, activity_type, approval_comment, approval_date,
    approval_status, approved_by, certificate_number, certification_id,
    cost, cost_covered_by, duration_hours, employee_id,
    end_time, evidence_file_path, evidence_type, expiry_date,
    instructor_name, is_recurring, learning_objectives, learning_outcomes,
    location, pdu_category, pdu_id, pdu_points,
    pdu_subcategory, provider_name, recurrence_pattern, related_project_id,
    related_training_id, skills_developed, start_time, is_deleted,
    created_at, created_by, updated_by, updated_at
) VALUES
    (NULL, NULL, '2024-03-15', 'スクラム・カンバンを中心としたアジャイル開発手法の実践研修',
     'アジャイル開発手法研修', 'TRAINING', 'PMP資格維持に適切なPDU活動として承認', '2024-03-20',
     'APPROVED', 'EMP000020', 'AGILE-2024-001', 'CERT_PMP_001',
     50000, 'COMPANY', 8.0, 'EMP000001',
     '17:00:00', '/evidence/pdu/PDU_001_certificate.pdf', 'CERTIFICATE', '2027-03-15',
     '山田講師', FALSE, 'アジャイル開発手法の理解と実践スキル習得', 'スクラム・カンバンの基礎理解、実際のプロジェクトへの適用方法を習得',
     '東京研修センター', 'TECHNICAL', 'PDU_001', 8.0,
     'Development Methods', 'アジャイル協会', NULL, NULL,
     'TRN_HIS_003', '["アジャイル開発", "スクラム", "カンバン", "チーム運営"]', '09:00:00', NULL,
     NULL, NULL, NULL, NULL),
    (NULL, NULL, '2024-11-28', 'AWSの最新技術動向とベストプラクティスに関するカンファレンス',
     'AWS re:Invent 2024', 'CONFERENCE', 'AWS認定維持に有効なPDU活動として承認', '2024-12-05',
     'APPROVED', 'EMP000020', NULL, 'CERT_AWS_001',
     200000, 'COMPANY', 32.0, 'EMP000002',
     NULL, '/evidence/pdu/PDU_002_attendance.pdf', 'ATTENDANCE', '2027-11-28',
     NULL, FALSE, 'AWS最新技術の習得とクラウドアーキテクチャスキル向上', '最新のAWSサービス理解、セキュリティベストプラクティス習得',
     'ラスベガス（オンライン参加）', 'TECHNICAL', 'PDU_002', 32.0,
     'Cloud Technologies', 'Amazon Web Services', NULL, 'PRJ_REC_002',
     NULL, '["AWS最新技術", "クラウドセキュリティ", "サーバーレス", "機械学習"]', NULL, NULL,
     NULL, NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM TRN_PDU ORDER BY created_at DESC;
