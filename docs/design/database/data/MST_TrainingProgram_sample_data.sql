-- MST_TrainingProgram (研修プログラム) サンプルデータ
-- 生成日時: 2025-06-24 23:05:57

INSERT INTO MST_TrainingProgram (
    id, tenant_id, active_flag, approval_date,
    approved_by, assessment_method, certification_provided, cost_per_participant,
    created_by, curriculum_details, curriculum_outline, difficulty_level,
    duration_days, duration_hours, effective_end_date, effective_start_date,
    equipment_required, external_provider, external_url, instructor_requirements,
    language, learning_objectives, mandatory_flag, materials_required,
    max_participants, min_participants, passing_score, pdu_credits,
    prerequisites, program_category, program_code, program_description,
    program_name, program_name_en, program_type, related_certifications,
    related_skills, repeat_interval, revision_notes, tags,
    target_audience, training_program_id, trainingprogram_id, venue_requirements,
    venue_type, version_number, is_deleted, created_at,
    updated_at
) VALUES
    (NULL, NULL, TRUE, '2023-12-15',
     'EMP000005', 'COMPREHENSIVE', TRUE, 50000.0,
     'EMP000010', '{"day1": ["PM概論", "プロジェクト憲章", "WBS作成"], "day2": ["進捗管理", "リスク分析", "ケーススタディ"]}', '1日目：PM概論、計画立案　2日目：実行・監視、リスク管理', 'INTERMEDIATE',
     2, 16.0, NULL, '2024-01-01',
     '["プロジェクター", "ホワイトボード", "PC環境"]', NULL, NULL, 'PMP資格保有、実務経験5年以上',
     'JA', 'PMBOKの基本概念理解、プロジェクト計画立案、リスク管理手法の習得', FALSE, '["テキスト", "演習用PC", "プロジェクト計画テンプレート"]',
     20, 8, 70.0, 16.0,
     '実務経験2年以上、基本的なビジネススキル', 'MANAGEMENT', 'PM-BASIC-001', 'プロジェクトマネジメントの基本概念と手法を学ぶ研修',
     'プロジェクトマネジメント基礎研修', 'Project Management Fundamentals', 'CLASSROOM', '["PMP", "プロジェクトマネージャ試験"]',
     '["プロジェクト管理", "リーダーシップ", "コミュニケーション"]', 24, '初版作成', '["プロジェクト管理", "PMBOK", "リーダーシップ", "中級"]',
     'MIDDLE', 'TRN_PROG_001', NULL, '20名収容可能な研修室、プロジェクター設備',
     'INTERNAL', '1.0', NULL, NULL,
     NULL),
    (NULL, NULL, TRUE, '2024-01-20',
     'EMP000008', 'TEST', TRUE, 80000.0,
     'EMP000015', '{"day1": ["EC2", "S3", "VPC"], "day2": ["高可用性設計", "セキュリティ", "コスト最適化"], "day3": ["模擬試験", "解説", "試験対策"]}', '1日目：AWS基礎　2日目：アーキテクチャ設計　3日目：模擬試験・解説', 'ADVANCED',
     3, 24.0, NULL, '2024-02-01',
     '["AWS環境", "PC", "インターネット接続"]', 'AWSトレーニングパートナー', 'https://aws.amazon.com/training/', 'AWS認定資格保有、実務経験3年以上',
     'JA', 'AWSサービス理解、アーキテクチャ設計、試験合格', FALSE, '["AWS公式テキスト", "模擬試験問題集", "ハンズオン環境"]',
     15, 5, 80.0, 24.0,
     'AWS基礎知識、クラウド実務経験1年以上', 'TECHNICAL', 'AWS-ARCH-001', 'AWS認定ソリューションアーキテクト資格取得のための対策研修',
     'AWS認定ソリューションアーキテクト対策研修', 'AWS Certified Solutions Architect Preparation', 'BLENDED', '["AWS認定ソリューションアーキテクト"]',
     '["AWS", "クラウドアーキテクチャ", "インフラ設計"]', 12, 'ハンズオン内容を強化', '["AWS", "クラウド", "認定資格", "アーキテクチャ", "上級"]',
     'SENIOR', 'TRN_PROG_002', NULL, 'PC環境、AWS環境アクセス可能',
     'HYBRID', '1.1', NULL, NULL,
     NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_TrainingProgram ORDER BY created_at DESC;
