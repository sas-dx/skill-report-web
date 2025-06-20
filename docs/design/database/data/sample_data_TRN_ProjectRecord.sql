-- サンプルデータ INSERT文: TRN_ProjectRecord
-- 生成日時: 2025-06-21 07:31:30
-- レコード数: 2

BEGIN;

INSERT INTO TRN_ProjectRecord (project_record_id, employee_id, project_name, project_code, client_name, project_type, project_scale, start_date, end_date, participation_rate, role_title, responsibilities, technologies_used, skills_applied, achievements, challenges_faced, lessons_learned, team_size, budget_range, project_status, evaluation_score, evaluation_comment, is_confidential, is_public_reference, id, created_at, updated_at, is_deleted) VALUES ('PRJ_REC_001', 'EMP000001', '顧客管理システム刷新プロジェクト', 'CRM2024_001', '株式会社サンプル', 'DEVELOPMENT', 'LARGE', '2024-01-15', '2024-12-31', 80.0, 'テックリード', 'システム設計、開発チームリード、技術選定', '["Java", "Spring Boot", "PostgreSQL", "React", "Docker"]', '["システム設計", "チームマネジメント", "技術選定"]', '予定より2週間早期リリース、性能要件120%達成', 'レガシーシステムとの連携、短納期対応', 'マイクロサービス設計の重要性、チーム間コミュニケーション', 8, 'UNDER_100M', 'COMPLETED', 4.5, '技術リーダーシップを発揮し、プロジェクトを成功に導いた', FALSE, TRUE, 'trn_dccfbbfd', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO TRN_ProjectRecord (project_record_id, employee_id, project_name, project_code, client_name, project_type, project_scale, start_date, end_date, participation_rate, role_title, responsibilities, technologies_used, skills_applied, achievements, challenges_faced, lessons_learned, team_size, budget_range, project_status, evaluation_score, evaluation_comment, is_confidential, is_public_reference, id, created_at, updated_at, is_deleted) VALUES ('PRJ_REC_002', 'EMP000002', 'AI画像解析システム開発', 'AI2024_002', '機密プロジェクト', 'RESEARCH', 'MEDIUM', '2024-03-01', NULL, 100.0, 'AIエンジニア', '機械学習モデル開発、データ前処理、精度改善', '["Python", "TensorFlow", "OpenCV", "AWS SageMaker"]', '["機械学習", "画像処理", "データ分析"]', '認識精度95%達成、処理速度30%向上', '学習データ不足、モデル精度向上', 'データ品質の重要性、MLOpsの必要性', 4, 'UNDER_10M', 'ONGOING', NULL, NULL, TRUE, FALSE, 'trn_51ac334a', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);

COMMIT;

-- TRN_ProjectRecord サンプルデータ終了
