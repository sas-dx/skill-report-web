-- サンプルデータ INSERT文: TRN_TrainingHistory
-- 生成日時: 2025-06-21 07:31:30
-- レコード数: 2

BEGIN;

INSERT INTO TRN_TrainingHistory (training_history_id, employee_id, training_program_id, training_name, training_type, training_category, provider_name, instructor_name, start_date, end_date, duration_hours, location, cost, cost_covered_by, attendance_status, completion_rate, test_score, grade, certificate_obtained, certificate_number, pdu_earned, skills_acquired, learning_objectives, learning_outcomes, feedback, satisfaction_score, recommendation_score, follow_up_required, follow_up_date, manager_approval, approved_by, id, created_at, updated_at, is_deleted) VALUES ('TRN_HIS_001', 'EMP000001', 'TRN_PROG_001', 'AWS認定ソリューションアーキテクト研修', 'EXTERNAL', 'TECHNICAL', 'AWS Training', '田中講師', '2024-03-01', '2024-03-03', 24.0, '東京研修センター', 150000.0, 'COMPANY', 'COMPLETED', 100.0, 85.0, '合格', TRUE, 'AWS-SAA-2024-001', 24.0, '["AWS設計", "クラウドアーキテクチャ", "セキュリティ設計"]', 'AWSでのソリューション設計スキル習得', 'クラウドアーキテクチャ設計の基礎を習得、実践的な設計手法を学習', '実践的な内容で非常に有用だった。講師の説明も分かりやすい。', 4.5, 5.0, TRUE, '2024-06-01', TRUE, 'EMP000010', 'trn_9ddd0500', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO TRN_TrainingHistory (training_history_id, employee_id, training_program_id, training_name, training_type, training_category, provider_name, instructor_name, start_date, end_date, duration_hours, location, cost, cost_covered_by, attendance_status, completion_rate, test_score, grade, certificate_obtained, certificate_number, pdu_earned, skills_acquired, learning_objectives, learning_outcomes, feedback, satisfaction_score, recommendation_score, follow_up_required, follow_up_date, manager_approval, approved_by, id, created_at, updated_at, is_deleted) VALUES ('TRN_HIS_002', 'EMP000002', NULL, 'プロジェクトマネジメント基礎', 'ONLINE', 'MANAGEMENT', '社内研修センター', '佐藤部長', '2024-02-15', '2024-02-15', 8.0, 'オンライン', 0.0, 'COMPANY', 'COMPLETED', 100.0, 92.0, 'A', TRUE, 'PM-BASIC-2024-002', 8.0, '["プロジェクト計画", "リスク管理", "チームマネジメント"]', 'プロジェクトマネジメントの基礎知識習得', 'PMBOKの基礎理解、実際のプロジェクト運営に活用可能な知識を習得', '基礎から体系的に学べて良かった。実例が豊富で理解しやすい。', 4.0, 4.0, FALSE, NULL, TRUE, 'EMP000010', 'trn_afe9c7ff', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);

COMMIT;

-- TRN_TrainingHistory サンプルデータ終了
