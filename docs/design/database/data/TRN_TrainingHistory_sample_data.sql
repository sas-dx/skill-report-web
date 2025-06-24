-- TRN_TrainingHistory (研修参加履歴) サンプルデータ
-- 生成日時: 2025-06-24 23:02:18

INSERT INTO TRN_TrainingHistory (
    id, tenant_id, training_name, approved_by,
    attendance_status, certificate_number, certificate_obtained, completion_rate,
    cost, cost_covered_by, duration_hours, employee_id,
    end_date, feedback, follow_up_date, follow_up_required,
    grade, instructor_name, learning_objectives, learning_outcomes,
    location, manager_approval, pdu_earned, provider_name,
    recommendation_score, satisfaction_score, skills_acquired, start_date,
    test_score, training_category, training_history_id, training_program_id,
    training_type, traininghistory_id, is_deleted, created_at,
    created_by, updated_by, updated_at
) VALUES
    (NULL, NULL, 'AWS認定ソリューションアーキテクト研修', 'EMP000010',
     'COMPLETED', 'AWS-SAA-2024-001', TRUE, 100.0,
     150000, 'COMPANY', 24.0, 'EMP000001',
     '2024-03-03', '実践的な内容で非常に有用だった。講師の説明も分かりやすい。', '2024-06-01', TRUE,
     '合格', '田中講師', 'AWSでのソリューション設計スキル習得', 'クラウドアーキテクチャ設計の基礎を習得、実践的な設計手法を学習',
     '東京研修センター', TRUE, 24.0, 'AWS Training',
     5.0, 4.5, '["AWS設計", "クラウドアーキテクチャ", "セキュリティ設計"]', '2024-03-01',
     85.0, 'TECHNICAL', 'TRN_HIS_001', 'TRN_PROG_001',
     'EXTERNAL', NULL, NULL, NULL,
     NULL, NULL, NULL),
    (NULL, NULL, 'プロジェクトマネジメント基礎', 'EMP000010',
     'COMPLETED', 'PM-BASIC-2024-002', TRUE, 100.0,
     0, 'COMPANY', 8.0, 'EMP000002',
     '2024-02-15', '基礎から体系的に学べて良かった。実例が豊富で理解しやすい。', NULL, FALSE,
     'A', '佐藤部長', 'プロジェクトマネジメントの基礎知識習得', 'PMBOKの基礎理解、実際のプロジェクト運営に活用可能な知識を習得',
     'オンライン', TRUE, 8.0, '社内研修センター',
     4.0, 4.0, '["プロジェクト計画", "リスク管理", "チームマネジメント"]', '2024-02-15',
     92.0, 'MANAGEMENT', 'TRN_HIS_002', NULL,
     'ONLINE', NULL, NULL, NULL,
     NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM TRN_TrainingHistory ORDER BY created_at DESC;
