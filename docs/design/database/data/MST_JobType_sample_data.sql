-- MST_JobType (職種マスタ) サンプルデータ
-- 生成日時: 2025-06-24 23:02:19

INSERT INTO MST_JobType (
    id, tenant_id, career_path, department_affinity,
    description, is_active, job_category, job_level,
    job_type_code, job_type_name, job_type_name_en, jobtype_id,
    remote_work_eligible, required_certifications, required_experience_years, required_skills,
    salary_grade_max, salary_grade_min, sort_order, travel_frequency,
    is_deleted, created_at, updated_at
) VALUES
    (NULL, NULL, 'SE → シニアSE → テックリード → エンジニアリングマネージャー', '["開発部", "システム部"]',
     'システムの設計・開発・テストを担当するエンジニア', TRUE, 'ENGINEERING', 'SENIOR',
     'SE', 'システムエンジニア', 'Systems Engineer', NULL,
     TRUE, '["基本情報技術者", "応用情報技術者"]', 3, '["Java", "SQL", "システム設計", "要件定義"]',
     6, 3, 1, 'LOW',
     NULL, NULL, NULL),
    (NULL, NULL, 'SE → リーダー → PM → 部門マネージャー', '["開発部", "PMO"]',
     'プロジェクトの計画・実行・管理を統括する責任者', TRUE, 'MANAGEMENT', 'MANAGER',
     'PM', 'プロジェクトマネージャー', 'Project Manager', NULL,
     TRUE, '["PMP", "プロジェクトマネージャ試験"]', 5, '["プロジェクト管理", "リーダーシップ", "コミュニケーション", "リスク管理"]',
     8, 5, 2, 'MEDIUM',
     NULL, NULL, NULL),
    (NULL, NULL, 'QA → シニアQA → QAリード → QAマネージャー', '["品質保証部", "開発部"]',
     'ソフトウェアの品質保証・テスト設計・実行を担当', TRUE, 'ENGINEERING', 'SENIOR',
     'QA', '品質保証エンジニア', 'Quality Assurance Engineer', NULL,
     TRUE, '["JSTQB", "ソフトウェア品質技術者資格"]', 2, '["テスト設計", "自動化テスト", "品質管理", "バグ分析"]',
     6, 3, 3, 'NONE',
     NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_JobType ORDER BY created_at DESC;
