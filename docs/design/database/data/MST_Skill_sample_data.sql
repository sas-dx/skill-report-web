-- MST_Skill (スキルマスタ) サンプルデータ
-- 生成日時: 2025-06-24 23:05:57

INSERT INTO MST_Skill (
    id, tenant_id, skill_name, category_id,
    certification_info, description, difficulty_level, display_order,
    effective_from, effective_to, evaluation_criteria, is_active,
    is_core_skill, learning_resources, market_demand, prerequisite_skills,
    related_skills, required_experience_months, skill_id, skill_name_en,
    skill_type, technology_trend, is_deleted, created_at,
    updated_at
) VALUES
    ('SKILL001', NULL, 'React', 'CAT_FRONTEND',
     '{"name":"React Developer Certification","provider":"Meta","url":"https://developers.facebook.com/certification/"}', 'Reactライブラリを使用したフロントエンド開発スキル。コンポーネント設計、状態管理、Hooksの理解が含まれます。', 3, 1,
     '2024-01-01', NULL, '{"level1":"基本的なコンポーネント作成","level2":"状態管理とイベント処理","level3":"Hooks活用とパフォーマンス最適化","level4":"複雑なアプリケーション設計","level5":"ライブラリ開発とベストプラクティス"}', TRUE,
     TRUE, '["https://reactjs.org/docs/","https://react.dev/learn","https://egghead.io/courses/react"]', 'HIGH', '["SKILL_JS001", "SKILL_HTML001"]',
     '["SKILL002", "SKILL003", "SKILL004"]', 6, NULL, 'React',
     'TECHNICAL', 'GROWING', NULL, NULL,
     NULL),
    ('SKILL002', NULL, 'TypeScript', 'CAT_FRONTEND',
     NULL, 'TypeScriptを使用した型安全なJavaScript開発スキル。型定義、ジェネリクス、高度な型操作が含まれます。', 3, 2,
     '2024-01-01', NULL, '{"level1":"基本的な型定義","level2":"インターフェースとクラス","level3":"ジェネリクスと高度な型","level4":"型レベルプログラミング","level5":"ライブラリ型定義作成"}', TRUE,
     TRUE, '["https://www.typescriptlang.org/docs/","https://typescript-jp.gitbook.io/deep-dive/"]', 'VERY_HIGH', '["SKILL_JS001"]',
     '["SKILL001", "SKILL003"]', 4, NULL, 'TypeScript',
     'TECHNICAL', 'GROWING', NULL, NULL,
     NULL),
    ('SKILL003', NULL, 'Node.js', 'CAT_BACKEND',
     NULL, 'Node.jsを使用したサーバーサイド開発スキル。非同期処理、API開発、パフォーマンス最適化が含まれます。', 3, 1,
     '2024-01-01', NULL, '{"level1":"基本的なサーバー構築","level2":"Express.jsでのAPI開発","level3":"非同期処理とストリーム","level4":"パフォーマンス最適化","level5":"スケーラブルアーキテクチャ設計"}', TRUE,
     TRUE, '["https://nodejs.org/en/docs/","https://expressjs.com/","https://nodeschool.io/"]', 'HIGH', '["SKILL_JS001"]',
     '["SKILL001", "SKILL002", "SKILL004"]', 8, NULL, 'Node.js',
     'TECHNICAL', 'STABLE', NULL, NULL,
     NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_Skill ORDER BY created_at DESC;
