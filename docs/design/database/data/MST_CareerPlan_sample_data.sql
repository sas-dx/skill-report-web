-- MST_CareerPlan (目標・キャリアプラン) サンプルデータ
-- 生成日時: 2025-06-04 06:57:02

INSERT INTO MST_CareerPlan (
    career_plan_id, employee_id, plan_name, plan_description,
    plan_type, target_position_id, target_job_type_id, target_department_id,
    current_level, target_level, plan_start_date, plan_end_date,
    milestone_1_date, milestone_1_description, milestone_2_date, milestone_2_description,
    milestone_3_date, milestone_3_description, required_skills, required_certifications,
    required_experiences, development_actions, training_plan, mentor_id,
    supervisor_id, plan_status, progress_percentage, last_review_date,
    next_review_date, review_frequency, success_criteria, risk_factors,
    support_resources, budget_allocated, budget_used, priority_level,
    visibility_level, template_id, custom_fields, notes,
    code, name, description
) VALUES
    ('CP_001', 'EMP000001', 'シニアエンジニアへの成長プラン', '3年以内にシニアエンジニアとして技術リーダーシップを発揮できる人材になる',
     'MEDIUM_TERM', 'POS_003', 'JOB_001', NULL,
     'INTERMEDIATE', 'SENIOR', '2024-04-01', '2027-03-31',
     '2024-12-31', 'AWS認定資格取得、チームリーダー経験', '2025-12-31', '大規模プロジェクトのテックリード担当',
     '2026-12-31', '後輩指導、技術選定の主導', '["Java", "Spring Boot", "AWS", "Docker", "Kubernetes", "チームマネジメント"]', '["AWS認定ソリューションアーキテクト", "PMP"]',
     '["チームリーダー経験", "大規模システム設計", "後輩指導"]', '["技術研修受講", "社外勉強会参加", "OSS貢献", "技術ブログ執筆"]', '["AWS研修", "リーダーシップ研修", "アーキテクチャ設計研修"]', 'EMP000010',
     'EMP000005', 'ACTIVE', 25.5, '2024-03-31',
     '2024-06-30', 'QUARTERLY', '技術力向上、チーム貢献、後輩育成実績', '業務多忙による学習時間確保困難、技術変化への対応',
     '社内研修制度、書籍購入支援、外部セミナー参加費補助', 300000.0, 75000.0, 'HIGH',
     'MANAGER', 'TMPL_ENG_001', '{"specialization": "バックエンド", "preferred_domain": "金融系"}', '本人の強い意欲と上司の全面的なサポートにより順調に進行中',
     NULL, NULL, NULL),
    ('CP_002', 'EMP000002', 'プロジェクトマネージャーへの転身プラン', '技術者からプロジェクトマネージャーへのキャリアチェンジ',
     'MANAGEMENT', 'POS_004', 'JOB_002', NULL,
     'SENIOR', 'MANAGER', '2024-01-01', '2025-12-31',
     '2024-06-30', 'PMP資格取得、小規模プロジェクト管理経験', '2024-12-31', '中規模プロジェクトのサブPM担当',
     NULL, NULL, '["プロジェクト管理", "リーダーシップ", "コミュニケーション", "リスク管理"]', '["PMP", "ITストラテジスト"]',
     '["プロジェクト管理", "チームマネジメント", "ステークホルダー調整"]', '["PM研修受講", "PMI勉強会参加", "管理業務OJT"]', '["プロジェクトマネジメント基礎", "リーダーシップ研修", "交渉術研修"]', 'EMP000015',
     'EMP000008', 'ACTIVE', 60.0, '2024-04-30',
     '2024-07-31', 'QUARTERLY', 'PMP取得、プロジェクト成功実績、チーム満足度向上', '技術からマネジメントへの意識転換、人間関係構築',
     'PM研修制度、資格取得支援、メンター制度', 200000.0, 120000.0, 'HIGH',
     'DEPARTMENT', 'TMPL_MGR_001', '{"management_style": "コーチング重視", "team_size_target": "10-15名"}', '技術的バックグラウンドを活かしたPMとして期待',
     NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_CareerPlan ORDER BY created_at DESC;
