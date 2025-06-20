-- サンプルデータ INSERT文: MST_SkillGradeRequirement
-- 生成日時: 2025-06-21 07:31:30
-- レコード数: 3

BEGIN;

INSERT INTO MST_SkillGradeRequirement (skill_grade_id, requirement_category, requirement_name, requirement_description, evaluation_criteria, proficiency_level, weight_percentage, minimum_score, evidence_requirements, learning_resources, prerequisite_requirements, assessment_method, assessment_frequency, validity_period, certification_mapping, requirement_status, effective_date, expiry_date, revision_notes, id, created_at, updated_at, is_deleted) VALUES ('GRADE001', 'TECHNICAL', 'プログラミング基礎', '基本的なプログラミング言語の理解と簡単なプログラムの作成能力', '指定された仕様に基づく簡単なプログラムの作成、基本的なアルゴリズムの理解', 2, 30.0, 70.0, '作成したプログラムのソースコード、動作確認結果', '["プログラミング入門書", "オンライン学習サイト", "基礎研修"]', '["コンピュータ基礎知識"]', 'PROJECT', 'SEMI_ANNUAL', 24, '["基本情報技術者試験"]', 'ACTIVE', '2025-01-01', NULL, '初版作成', 'mst_e6360cbd', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO MST_SkillGradeRequirement (skill_grade_id, requirement_category, requirement_name, requirement_description, evaluation_criteria, proficiency_level, weight_percentage, minimum_score, evidence_requirements, learning_resources, prerequisite_requirements, assessment_method, assessment_frequency, validity_period, certification_mapping, requirement_status, effective_date, expiry_date, revision_notes, id, created_at, updated_at, is_deleted) VALUES ('GRADE001', 'BUSINESS', '業務理解', '担当業務の基本的な理解と顧客要件の把握能力', '業務フローの説明、顧客要件の整理と文書化', 2, 25.0, 75.0, '業務分析レポート、要件定義書', '["業務知識研修", "業界動向資料", "先輩社員からのOJT"]', NULL, 'PORTFOLIO', 'ANNUAL', 12, NULL, 'ACTIVE', '2025-01-01', NULL, '初版作成', 'mst_334bc375', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO MST_SkillGradeRequirement (skill_grade_id, requirement_category, requirement_name, requirement_description, evaluation_criteria, proficiency_level, weight_percentage, minimum_score, evidence_requirements, learning_resources, prerequisite_requirements, assessment_method, assessment_frequency, validity_period, certification_mapping, requirement_status, effective_date, expiry_date, revision_notes, id, created_at, updated_at, is_deleted) VALUES ('GRADE003', 'LEADERSHIP', 'チームマネジメント', 'チームの運営管理と成果創出のためのリーダーシップ能力', 'チーム運営実績、メンバー育成成果、プロジェクト成功率', 4, 35.0, 80.0, 'チーム運営レポート、メンバー評価、プロジェクト成果物', '["リーダーシップ研修", "マネジメント書籍", "外部セミナー"]', '["チームリーダー経験", "プロジェクト管理経験"]', 'PEER_REVIEW', 'ANNUAL', 36, '["PMP", "プロジェクトマネージャ試験"]', 'ACTIVE', '2025-01-01', NULL, '初版作成', 'mst_16809afd', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);

COMMIT;

-- MST_SkillGradeRequirement サンプルデータ終了
