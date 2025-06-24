-- TRN_ProjectRecord (案件実績) サンプルデータ
-- 生成日時: 2025-06-24 23:05:57

INSERT INTO TRN_ProjectRecord (
    id, tenant_id, project_code, project_name,
    achievements, budget_range, challenges_faced, client_name,
    employee_id, end_date, evaluation_comment, evaluation_score,
    is_confidential, is_public_reference, lessons_learned, participation_rate,
    project_record_id, project_scale, project_status, project_type,
    projectrecord_id, responsibilities, role_title, skills_applied,
    start_date, team_size, technologies_used, is_deleted,
    created_at, created_by, updated_by, updated_at
) VALUES
    (NULL, NULL, 'CRM2024_001', '顧客管理システム刷新プロジェクト',
     '予定より2週間早期リリース、性能要件120%達成', 'UNDER_100M', 'レガシーシステムとの連携、短納期対応', '株式会社サンプル',
     'EMP000001', '2024-12-31', '技術リーダーシップを発揮し、プロジェクトを成功に導いた', 4.5,
     FALSE, TRUE, 'マイクロサービス設計の重要性、チーム間コミュニケーション', 80.0,
     'PRJ_REC_001', 'LARGE', 'COMPLETED', 'DEVELOPMENT',
     NULL, 'システム設計、開発チームリード、技術選定', 'テックリード', '["システム設計", "チームマネジメント", "技術選定"]',
     '2024-01-15', 8, '["Java", "Spring Boot", "PostgreSQL", "React", "Docker"]', NULL,
     NULL, NULL, NULL, NULL),
    (NULL, NULL, 'AI2024_002', 'AI画像解析システム開発',
     '認識精度95%達成、処理速度30%向上', 'UNDER_10M', '学習データ不足、モデル精度向上', '機密プロジェクト',
     'EMP000002', NULL, NULL, NULL,
     TRUE, FALSE, 'データ品質の重要性、MLOpsの必要性', 100.0,
     'PRJ_REC_002', 'MEDIUM', 'ONGOING', 'RESEARCH',
     NULL, '機械学習モデル開発、データ前処理、精度改善', 'AIエンジニア', '["機械学習", "画像処理", "データ分析"]',
     '2024-03-01', 4, '["Python", "TensorFlow", "OpenCV", "AWS SageMaker"]', NULL,
     NULL, NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM TRN_ProjectRecord ORDER BY created_at DESC;
