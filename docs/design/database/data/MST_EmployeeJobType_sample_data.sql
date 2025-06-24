-- MST_EmployeeJobType (社員職種関連) サンプルデータ
-- 生成日時: 2025-06-24 22:56:14

INSERT INTO MST_EmployeeJobType (
    id, tenant_id, achievements, approval_date,
    approved_by, assignment_ratio, assignment_reason, assignment_status,
    assignment_type, billable_flag, budget_allocation, career_path,
    certification_requirements, cost_center, created_by, development_plan,
    effective_end_date, effective_start_date, employee_id, employee_job_type_id,
    employeejobtype_id, evaluation_frequency, experience_requirements, goals,
    hourly_rate, improvement_areas, job_type_id, last_evaluation_date,
    mentor_id, next_evaluation_date, notes, overtime_eligible,
    performance_rating, proficiency_level, remote_work_eligible, security_clearance_required,
    skill_requirements, strengths, supervisor_id, target_achievement_date,
    target_proficiency_level, training_plan, travel_required, workload_percentage,
    is_deleted, created_at, updated_at
) VALUES
    (NULL, NULL, '新人研修システム開発、パフォーマンス改善20%達成', '2024-03-25',
     'EMP000008', 100.0, 'NEW_HIRE', 'ACTIVE',
     'PRIMARY', TRUE, 5000000.0, 'シニアエンジニア → テックリード → アーキテクト',
     '["基本情報技術者試験", "AWS認定"]', 'DEV001', 'EMP000005', '{"short_term": "AWS認定取得", "medium_term": "チームリーダー経験", "long_term": "アーキテクト昇格"}',
     NULL, '2024-04-01', 'EMP000001', 'EJT_001',
     NULL, 'QUARTERLY', '["Webアプリケーション開発", "チーム開発"]', 'AWS認定取得、チームリーダー経験積む',
     3500.0, 'リーダーシップ、プレゼンテーション', 'JOB_001', '2024-03-31',
     'EMP000010', '2024-06-30', '新卒採用、高いポテンシャルを持つ', TRUE,
     'GOOD', 'INTERMEDIATE', TRUE, FALSE,
     '["Java", "Spring Boot", "AWS", "Docker"]', '技術習得力、問題解決能力、チームワーク', 'EMP000005', '2025-03-31',
     'ADVANCED', '["TRN_PROG_002", "TRN_PROG_006"]', FALSE, 100.0,
     NULL, NULL, NULL),
    (NULL, NULL, '3つの大規模プロジェクト成功、チーム満足度向上', '2023-12-15',
     'EMP000001', 80.0, 'PROMOTION', 'ACTIVE',
     'PRIMARY', TRUE, 8000000.0, 'プロジェクトマネージャー → シニアPM → PMO責任者',
     '["PMP", "ITストラテジスト"]', 'PMO001', 'EMP000008', '{"short_term": "PMP取得", "medium_term": "大規模PM経験", "long_term": "PMO責任者"}',
     NULL, '2024-01-01', 'EMP000002', 'EJT_002',
     NULL, 'QUARTERLY', '["大規模プロジェクト管理", "チームマネジメント"]', 'PMP取得、PMO体制構築',
     5000.0, '戦略立案、予算管理', 'JOB_002', '2024-04-30',
     'EMP000015', '2024-07-31', '技術者からPMへの転身成功例', FALSE,
     'EXCELLENT', 'ADVANCED', TRUE, FALSE,
     '["プロジェクト管理", "リーダーシップ", "ステークホルダー管理"]', 'プロジェクト管理、コミュニケーション、問題解決', 'EMP000008', '2024-12-31',
     'EXPERT', '["TRN_PROG_001", "TRN_PROG_007"]', TRUE, 80.0,
     NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_EmployeeJobType ORDER BY created_at DESC;
