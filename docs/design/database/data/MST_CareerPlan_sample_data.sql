-- MST_CareerPlan (目標・キャリアプラン) サンプルデータ
-- 生成日時: 2025-06-24 23:02:18

INSERT INTO MST_CareerPlan (
    id, tenant_id, plan_name, budget_allocated,
    budget_used, career_plan_id, careerplan_id, current_level,
    custom_fields, development_actions, employee_id, last_review_date,
    mentor_id, milestone_1_date, milestone_1_description, milestone_2_date,
    milestone_2_description, milestone_3_date, milestone_3_description, next_review_date,
    notes, plan_description, plan_end_date, plan_start_date,
    plan_status, plan_type, priority_level, progress_percentage,
    required_certifications, required_experiences, required_skills, review_frequency,
    risk_factors, success_criteria, supervisor_id, support_resources,
    target_department_id, target_job_type_id, target_level, target_position_id,
    template_id, training_plan, visibility_level, is_deleted,
    created_at, updated_at
) VALUES
    (NULL, NULL, 'シニアエンジニアへの成長プラン', 300000.0,
     75000.0, 'CP_001', NULL, 'INTERMEDIATE',
     '{"specialization": "バックエンド", "preferred_domain": "金融系"}', '["技術研修受講", "社外勉強会参加", "OSS貢献", "技術ブログ執筆"]', 'EMP000001', '2024-03-31',
     'EMP000010', '2024-12-31', 'AWS認定資格取得、チームリーダー経験', '2025-12-31',
     '大規模プロジェクトのテックリード担当', '2026-12-31', '後輩指導、技術選定の主導', '2024-06-30',
     '本人の強い意欲と上司の全面的なサポートにより順調に進行中', '3年以内にシニアエンジニアとして技術リーダーシップを発揮できる人材になる', '2027-03-31', '2024-04-01',
     'ACTIVE', 'MEDIUM_TERM', 'HIGH', 25.5,
     '["AWS認定ソリューションアーキテクト", "PMP"]', '["チームリーダー経験", "大規模システム設計", "後輩指導"]', '["Java", "Spring Boot", "AWS", "Docker", "Kubernetes", "チームマネジメント"]', 'QUARTERLY',
     '業務多忙による学習時間確保困難、技術変化への対応', '技術力向上、チーム貢献、後輩育成実績', 'EMP000005', '社内研修制度、書籍購入支援、外部セミナー参加費補助',
     NULL, 'JOB_001', 'SENIOR', 'POS_003',
     'TMPL_ENG_001', '["AWS研修", "リーダーシップ研修", "アーキテクチャ設計研修"]', 'MANAGER', NULL,
     NULL, NULL),
    (NULL, NULL, 'プロジェクトマネージャーへの転身プラン', 200000.0,
     120000.0, 'CP_002', NULL, 'SENIOR',
     '{"management_style": "コーチング重視", "team_size_target": "10-15名"}', '["PM研修受講", "PMI勉強会参加", "管理業務OJT"]', 'EMP000002', '2024-04-30',
     'EMP000015', '2024-06-30', 'PMP資格取得、小規模プロジェクト管理経験', '2024-12-31',
     '中規模プロジェクトのサブPM担当', NULL, NULL, '2024-07-31',
     '技術的バックグラウンドを活かしたPMとして期待', '技術者からプロジェクトマネージャーへのキャリアチェンジ', '2025-12-31', '2024-01-01',
     'ACTIVE', 'MANAGEMENT', 'HIGH', 60.0,
     '["PMP", "ITストラテジスト"]', '["プロジェクト管理", "チームマネジメント", "ステークホルダー調整"]', '["プロジェクト管理", "リーダーシップ", "コミュニケーション", "リスク管理"]', 'QUARTERLY',
     '技術からマネジメントへの意識転換、人間関係構築', 'PMP取得、プロジェクト成功実績、チーム満足度向上', 'EMP000008', 'PM研修制度、資格取得支援、メンター制度',
     NULL, 'JOB_002', 'MANAGER', 'POS_004',
     'TMPL_MGR_001', '["プロジェクトマネジメント基礎", "リーダーシップ研修", "交渉術研修"]', 'DEPARTMENT', NULL,
     NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_CareerPlan ORDER BY created_at DESC;
