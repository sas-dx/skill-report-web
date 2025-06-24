# テーブル定義書: MST_JobType

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_JobType |
| 論理名 | 職種マスタ |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-24 23:05:58 |

## 概要

MST_JobType（職種マスタ）は、組織内の職種分類と各職種の基本情報を管理するマスタテーブルです。
主な目的：
- 職種の体系的な分類・管理
- 職種別スキル要件の定義基盤
- 人材配置・採用計画の基準
- キャリアパス・昇進要件の管理
- 職種別評価基準の設定
このテーブルにより、社員のキャリア開発や適材適所の人材配置、
職種別スキル要件の管理を効率的に行うことができます。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| career_path | キャリアパス | TEXT |  | ○ |  | キャリアパス |
| department_affinity | 部署親和性 | TEXT |  | ○ |  | 部署親和性 |
| description | 職種説明 | TEXT |  | ○ |  | 職種説明 |
| is_active | 有効フラグ | BOOLEAN |  | ○ | True | 有効フラグ |
| job_category | 職種カテゴリ | ENUM |  | ○ |  | 職種カテゴリ |
| job_level | 職種レベル | ENUM |  | ○ |  | 職種レベル |
| job_type_code | 職種コード | VARCHAR | 20 | ○ |  | 職種コード |
| job_type_name | 職種名 | VARCHAR | 100 | ○ |  | 職種名 |
| job_type_name_en | 職種名 | VARCHAR | 100 | ○ |  | 職種名（英語） |
| jobtype_id | MST_JobTypeの主キー | SERIAL |  | × |  | MST_JobTypeの主キー |
| remote_work_eligible | リモートワーク可否 | BOOLEAN |  | ○ | False | リモートワーク可否 |
| required_certifications | 必要資格 | TEXT |  | ○ |  | 必要資格 |
| required_experience_years | 必要経験年数 | INTEGER |  | ○ |  | 必要経験年数 |
| required_skills | 必要スキル | TEXT |  | ○ |  | 必要スキル |
| salary_grade_max | 給与グレード上限 | INTEGER |  | ○ |  | 給与グレード上限 |
| salary_grade_min | 給与グレード下限 | INTEGER |  | ○ |  | 給与グレード下限 |
| sort_order | 表示順序 | INTEGER |  | ○ | 0 | 表示順序 |
| travel_frequency | 出張頻度 | ENUM |  | ○ |  | 出張頻度 |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_job_type_code | job_type_code | ○ |  |
| idx_job_type_name | job_type_name | × |  |
| idx_job_category | job_category | × |  |
| idx_job_level | job_level | × |  |
| idx_category_level | job_category, job_level | × |  |
| idx_remote_eligible | remote_work_eligible, is_active | × |  |
| idx_sort_order | sort_order | × |  |
| idx_mst_jobtype_tenant_id | tenant_id | × |  |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| uk_job_type_code | UNIQUE |  | job_type_code一意制約 |
| chk_job_type_code | CHECK | job_type_code IN (...) | job_type_code値チェック制約 |
| chk_job_type_name | CHECK | job_type_name IN (...) | job_type_name値チェック制約 |
| chk_job_type_name_en | CHECK | job_type_name_en IN (...) | job_type_name_en値チェック制約 |
| chk_jobtype_id | CHECK | jobtype_id IN (...) | jobtype_id値チェック制約 |

## サンプルデータ

| job_type_code | job_type_name | job_type_name_en | job_category | job_level | description | required_experience_years | salary_grade_min | salary_grade_max | career_path | required_certifications | required_skills | department_affinity | remote_work_eligible | travel_frequency | sort_order | is_active |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| SE | システムエンジニア | Systems Engineer | ENGINEERING | SENIOR | システムの設計・開発・テストを担当するエンジニア | 3 | 3 | 6 | SE → シニアSE → テックリード → エンジニアリングマネージャー | ["基本情報技術者", "応用情報技術者"] | ["Java", "SQL", "システム設計", "要件定義"] | ["開発部", "システム部"] | True | LOW | 1 | True |
| PM | プロジェクトマネージャー | Project Manager | MANAGEMENT | MANAGER | プロジェクトの計画・実行・管理を統括する責任者 | 5 | 5 | 8 | SE → リーダー → PM → 部門マネージャー | ["PMP", "プロジェクトマネージャ試験"] | ["プロジェクト管理", "リーダーシップ", "コミュニケーション", "リスク管理"] | ["開発部", "PMO"] | True | MEDIUM | 2 | True |
| QA | 品質保証エンジニア | Quality Assurance Engineer | ENGINEERING | SENIOR | ソフトウェアの品質保証・テスト設計・実行を担当 | 2 | 3 | 6 | QA → シニアQA → QAリード → QAマネージャー | ["JSTQB", "ソフトウェア品質技術者資格"] | ["テスト設計", "自動化テスト", "品質管理", "バグ分析"] | ["品質保証部", "開発部"] | True | NONE | 3 | True |

## 特記事項

- 職種コードは組織内で一意である必要がある
- 必要資格・スキル・部署親和性はJSON形式で柔軟に管理
- 給与グレードは人事制度との連携で使用
- キャリアパスは社員のキャリア開発指針として活用
- リモートワーク可否は働き方改革・採用要件で参照
- 論理削除は is_active フラグで管理
- 職種コードは英数字・アンダースコアのみ使用可能
- 職種レベルは組織の階層構造と整合性を保つ
- 給与グレードは下限 ≤ 上限の関係を維持
- 必要経験年数は職種レベルと整合性を保つ
- リモートワーク可否は業務特性を考慮して設定
- 出張頻度は職種の業務内容に応じて適切に設定
- 表示順序は職種の重要度・階層に応じて設定

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 職種マスタテーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214906 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_214959 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215053 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223432 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |