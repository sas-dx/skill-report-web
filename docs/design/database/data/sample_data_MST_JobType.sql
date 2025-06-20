-- サンプルデータ INSERT文: MST_JobType
-- 生成日時: 2025-06-21 07:22:21
-- レコード数: 3

BEGIN;

INSERT INTO MST_JobType (job_type_code, job_type_name, job_type_name_en, job_category, job_level, description, required_experience_years, salary_grade_min, salary_grade_max, career_path, required_certifications, required_skills, department_affinity, remote_work_eligible, travel_frequency, sort_order, is_active, id, created_at, updated_at, is_deleted) VALUES ('SE', 'システムエンジニア', 'Systems Engineer', 'ENGINEERING', 'SENIOR', 'システムの設計・開発・テストを担当するエンジニア', 3, 3, 6, 'SE → シニアSE → テックリード → エンジニアリングマネージャー', '["基本情報技術者", "応用情報技術者"]', '["Java", "SQL", "システム設計", "要件定義"]', '["開発部", "システム部"]', TRUE, 'LOW', 1, TRUE, 'mst_2e01f23a', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO MST_JobType (job_type_code, job_type_name, job_type_name_en, job_category, job_level, description, required_experience_years, salary_grade_min, salary_grade_max, career_path, required_certifications, required_skills, department_affinity, remote_work_eligible, travel_frequency, sort_order, is_active, id, created_at, updated_at, is_deleted) VALUES ('PM', 'プロジェクトマネージャー', 'Project Manager', 'MANAGEMENT', 'MANAGER', 'プロジェクトの計画・実行・管理を統括する責任者', 5, 5, 8, 'SE → リーダー → PM → 部門マネージャー', '["PMP", "プロジェクトマネージャ試験"]', '["プロジェクト管理", "リーダーシップ", "コミュニケーション", "リスク管理"]', '["開発部", "PMO"]', TRUE, 'MEDIUM', 2, TRUE, 'mst_fb667b3e', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO MST_JobType (job_type_code, job_type_name, job_type_name_en, job_category, job_level, description, required_experience_years, salary_grade_min, salary_grade_max, career_path, required_certifications, required_skills, department_affinity, remote_work_eligible, travel_frequency, sort_order, is_active, id, created_at, updated_at, is_deleted) VALUES ('QA', '品質保証エンジニア', 'Quality Assurance Engineer', 'ENGINEERING', 'SENIOR', 'ソフトウェアの品質保証・テスト設計・実行を担当', 2, 3, 6, 'QA → シニアQA → QAリード → QAマネージャー', '["JSTQB", "ソフトウェア品質技術者資格"]', '["テスト設計", "自動化テスト", "品質管理", "バグ分析"]', '["品質保証部", "開発部"]', TRUE, 'NONE', 3, TRUE, 'mst_4e76ce00', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);

COMMIT;

-- MST_JobType サンプルデータ終了
