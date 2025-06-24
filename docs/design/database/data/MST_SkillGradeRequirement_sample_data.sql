-- MST_SkillGradeRequirement (スキルグレード要件) サンプルデータ
-- 生成日時: 2025-06-24 23:02:18

INSERT INTO MST_SkillGradeRequirement (
    id, tenant_id, assessment_frequency, assessment_method,
    certification_mapping, effective_date, evaluation_criteria, evidence_requirements,
    expiry_date, learning_resources, minimum_score, prerequisite_requirements,
    proficiency_level, requirement_category, requirement_description, requirement_name,
    requirement_status, revision_notes, skill_grade_id, skillgraderequirement_id,
    validity_period, weight_percentage, is_deleted, created_at,
    updated_at
) VALUES
    (NULL, NULL, 'SEMI_ANNUAL', 'PROJECT',
     '["基本情報技術者試験"]', '2025-01-01', '指定された仕様に基づく簡単なプログラムの作成、基本的なアルゴリズムの理解', '作成したプログラムのソースコード、動作確認結果',
     NULL, '["プログラミング入門書", "オンライン学習サイト", "基礎研修"]', 70.0, '["コンピュータ基礎知識"]',
     2, 'TECHNICAL', '基本的なプログラミング言語の理解と簡単なプログラムの作成能力', 'プログラミング基礎',
     'ACTIVE', '初版作成', 'GRADE001', NULL,
     24, 30.0, NULL, NULL,
     NULL),
    (NULL, NULL, 'ANNUAL', 'PORTFOLIO',
     NULL, '2025-01-01', '業務フローの説明、顧客要件の整理と文書化', '業務分析レポート、要件定義書',
     NULL, '["業務知識研修", "業界動向資料", "先輩社員からのOJT"]', 75.0, NULL,
     2, 'BUSINESS', '担当業務の基本的な理解と顧客要件の把握能力', '業務理解',
     'ACTIVE', '初版作成', 'GRADE001', NULL,
     12, 25.0, NULL, NULL,
     NULL),
    (NULL, NULL, 'ANNUAL', 'PEER_REVIEW',
     '["PMP", "プロジェクトマネージャ試験"]', '2025-01-01', 'チーム運営実績、メンバー育成成果、プロジェクト成功率', 'チーム運営レポート、メンバー評価、プロジェクト成果物',
     NULL, '["リーダーシップ研修", "マネジメント書籍", "外部セミナー"]', 80.0, '["チームリーダー経験", "プロジェクト管理経験"]',
     4, 'LEADERSHIP', 'チームの運営管理と成果創出のためのリーダーシップ能力', 'チームマネジメント',
     'ACTIVE', '初版作成', 'GRADE003', NULL,
     36, 35.0, NULL, NULL,
     NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_SkillGradeRequirement ORDER BY created_at DESC;
