-- TRN_GoalProgress (目標進捗) サンプルデータ
-- 生成日時: 2025-06-24 23:02:19

INSERT INTO TRN_GoalProgress (
    id, tenant_id, achievement_rate, achievement_status,
    approval_status, approved_at, approved_by, completion_date,
    current_value, employee_id, evaluation_comments, goal_category,
    goal_description, goal_id, goal_title, goal_type,
    goalprogress_id, last_updated_at, milestones, next_review_date,
    obstacles, priority_level, progress_rate, related_career_plan_id,
    related_skill_items, self_evaluation, start_date, supervisor_evaluation,
    supervisor_id, support_needed, target_date, target_value,
    unit, is_deleted, created_at, created_by,
    updated_by, updated_at
) VALUES
    (NULL, NULL, NULL, 'IN_PROGRESS',
     'APPROVED', '2025-01-05 10:00:00', 'EMP000010', NULL,
     NULL, 'EMP000001', NULL, 'SKILL',
     'Spring Frameworkを使用したWebアプリケーション開発技術の習得', 'GOAL000001', 'Java技術習得', 'QUALITATIVE',
     NULL, '2025-06-01 09:00:00', '["基礎学習完了", "実践プロジェクト参加", "技術認定取得"]', '2025-07-01',
     NULL, 'HIGH', 50.0, 'CP000001',
     '["JAVA", "SPRING", "WEB_DEVELOPMENT"]', NULL, '2025-01-01', NULL,
     'EMP000010', '外部研修参加、メンター指導', '2025-12-31', NULL,
     NULL, NULL, NULL, NULL,
     NULL, NULL),
    (NULL, NULL, NULL, 'IN_PROGRESS',
     'APPROVED', '2025-03-25 14:00:00', 'EMP000011', NULL,
     6500000.0, 'EMP000002', NULL, 'BUSINESS',
     '第2四半期の個人売上目標1000万円の達成', 'GOAL000002', '売上目標達成', 'QUANTITATIVE',
     NULL, '2025-06-01 17:00:00', '["4月目標達成", "5月目標達成", "6月目標達成"]', '2025-06-15',
     '["競合他社の価格競争", "新規顧客開拓の困難"]', 'HIGH', 65.0, NULL,
     '["SALES", "NEGOTIATION", "CUSTOMER_MANAGEMENT"]', NULL, '2025-04-01', NULL,
     'EMP000011', 'マーケティング支援、価格戦略見直し', '2025-06-30', 10000000.0,
     '円', NULL, NULL, NULL,
     NULL, NULL),
    (NULL, NULL, NULL, 'IN_PROGRESS',
     'APPROVED', '2025-01-10 11:00:00', 'EMP000012', NULL,
     NULL, 'EMP000003', NULL, 'CAREER',
     'リーダーシップスキル向上とチーム管理経験の積み重ね', 'GOAL000003', 'チームリーダー昇進', 'MILESTONE',
     NULL, '2025-06-01 12:00:00', '["リーダーシップ研修受講", "プロジェクトリーダー経験", "昇進面談"]', '2025-08-01',
     NULL, 'MEDIUM', 30.0, 'CP000002',
     '["LEADERSHIP", "TEAM_MANAGEMENT", "COMMUNICATION"]', NULL, '2025-01-01', NULL,
     'EMP000012', 'リーダーシップ研修、メンタリング', '2025-12-31', NULL,
     NULL, NULL, NULL, NULL,
     NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM TRN_GoalProgress ORDER BY created_at DESC;
