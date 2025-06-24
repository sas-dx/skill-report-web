# テーブル定義書: MST_EmployeeJobType

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_EmployeeJobType |
| 論理名 | 社員職種関連 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-24 23:02:18 |

## 概要

MST_EmployeeJobType（社員職種関連）は、社員と職種の関連付けを管理するマスタテーブルです。
主な目的：
- 社員の職種履歴管理
- 複数職種対応（兼任・転職）
- 職種変更の追跡
- 人材配置の最適化
- スキル要件との連携
このテーブルにより、社員の職種変遷を正確に管理し、
適切な人材配置とキャリア開発を支援できます。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| achievements | 実績 | TEXT |  | ○ |  | 実績 |
| approval_date | 承認日 | DATE |  | ○ |  | 承認日 |
| approved_by | 承認者 | VARCHAR | 50 | ○ |  | 承認者 |
| assignment_ratio | 配属比率 | DECIMAL | 5,2 | ○ | 100.0 | 配属比率 |
| assignment_reason | 配属理由 | ENUM |  | ○ |  | 配属理由 |
| assignment_status | 配属状況 | ENUM |  | ○ | ACTIVE | 配属状況 |
| assignment_type | 配属種別 | ENUM |  | ○ |  | 配属種別 |
| billable_flag | 請求対象フラグ | BOOLEAN |  | ○ | True | 請求対象フラグ |
| budget_allocation | 予算配分 | DECIMAL | 10,2 | ○ |  | 予算配分 |
| career_path | キャリアパス | TEXT |  | ○ |  | キャリアパス |
| certification_requirements | 必要資格 | TEXT |  | ○ |  | 必要資格 |
| cost_center | コストセンター | VARCHAR | 20 | ○ |  | コストセンター |
| created_by | 作成者 | VARCHAR | 50 | ○ |  | 作成者 |
| development_plan | 育成計画 | TEXT |  | ○ |  | 育成計画 |
| effective_end_date | 有効終了日 | DATE |  | ○ |  | 有効終了日 |
| effective_start_date | 有効開始日 | DATE |  | ○ |  | 有効開始日 |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | 社員ID |
| employee_job_type_id | 社員職種関連ID | VARCHAR | 50 | ○ |  | 社員職種関連ID |
| employeejobtype_id | MST_EmployeeJobTypeの主キー | SERIAL |  | × |  | MST_EmployeeJobTypeの主キー |
| evaluation_frequency | 評価頻度 | ENUM |  | ○ | QUARTERLY | 評価頻度 |
| experience_requirements | 必要経験 | TEXT |  | ○ |  | 必要経験 |
| goals | 目標 | TEXT |  | ○ |  | 目標 |
| hourly_rate | 時間単価 | DECIMAL | 8,2 | ○ |  | 時間単価 |
| improvement_areas | 改善領域 | TEXT |  | ○ |  | 改善領域 |
| job_type_id | 職種ID | VARCHAR | 50 | ○ |  | 職種ID |
| last_evaluation_date | 最終評価日 | DATE |  | ○ |  | 最終評価日 |
| mentor_id | メンターID | VARCHAR | 50 | ○ |  | メンターID |
| next_evaluation_date | 次回評価日 | DATE |  | ○ |  | 次回評価日 |
| notes | 備考 | TEXT |  | ○ |  | 備考 |
| overtime_eligible | 残業対象フラグ | BOOLEAN |  | ○ | True | 残業対象フラグ |
| performance_rating | パフォーマンス評価 | ENUM |  | ○ |  | パフォーマンス評価 |
| proficiency_level | 習熟度 | ENUM |  | ○ | NOVICE | 習熟度 |
| remote_work_eligible | リモートワーク可否 | BOOLEAN |  | ○ | False | リモートワーク可否 |
| security_clearance_required | セキュリティクリアランス要否 | BOOLEAN |  | ○ | False | セキュリティクリアランス要否 |
| skill_requirements | 必要スキル | TEXT |  | ○ |  | 必要スキル |
| strengths | 強み | TEXT |  | ○ |  | 強み |
| supervisor_id | 上司ID | VARCHAR | 50 | ○ |  | 上司ID |
| target_achievement_date | 目標達成日 | DATE |  | ○ |  | 目標達成日 |
| target_proficiency_level | 目標習熟度 | ENUM |  | ○ |  | 目標習熟度 |
| training_plan | 研修計画 | TEXT |  | ○ |  | 研修計画 |
| travel_required | 出張要否 | BOOLEAN |  | ○ | False | 出張要否 |
| workload_percentage | 業務負荷率 | DECIMAL | 5,2 | ○ | 100.0 | 業務負荷率 |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_employee_job_type_id | employee_job_type_id | ○ |  |
| idx_employee_id | employee_id | × |  |
| idx_job_type_id | job_type_id | × |  |
| idx_employee_job_type | employee_id, job_type_id | × |  |
| idx_assignment_type | assignment_type | × |  |
| idx_assignment_status | assignment_status | × |  |
| idx_proficiency_level | proficiency_level | × |  |
| idx_effective_period | effective_start_date, effective_end_date | × |  |
| idx_mentor_id | mentor_id | × |  |
| idx_supervisor_id | supervisor_id | × |  |
| idx_performance_rating | performance_rating | × |  |
| idx_mst_employeejobtype_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_emp_job_type_employee | employee_id | MST_Employee | id | CASCADE | CASCADE | 外部キー制約 |
| fk_emp_job_type_job_type | job_type_id | MST_JobType | id | CASCADE | RESTRICT | 外部キー制約 |
| fk_emp_job_type_mentor | mentor_id | MST_Employee | id | CASCADE | SET NULL | 外部キー制約 |
| fk_emp_job_type_supervisor | supervisor_id | MST_Employee | id | CASCADE | SET NULL | 外部キー制約 |
| fk_emp_job_type_created_by | created_by | MST_Employee | id | CASCADE | RESTRICT | 外部キー制約 |
| fk_emp_job_type_approved_by | approved_by | MST_Employee | id | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| uk_employee_job_type_id | UNIQUE |  | employee_job_type_id一意制約 |
| chk_assignment_status | CHECK | assignment_status IN (...) | assignment_status値チェック制約 |
| chk_assignment_type | CHECK | assignment_type IN (...) | assignment_type値チェック制約 |
| chk_employee_job_type_id | CHECK | employee_job_type_id IN (...) | employee_job_type_id値チェック制約 |
| chk_employeejobtype_id | CHECK | employeejobtype_id IN (...) | employeejobtype_id値チェック制約 |
| chk_job_type_id | CHECK | job_type_id IN (...) | job_type_id値チェック制約 |

## サンプルデータ

| employee_job_type_id | employee_id | job_type_id | assignment_type | assignment_ratio | effective_start_date | effective_end_date | assignment_reason | assignment_status | proficiency_level | target_proficiency_level | target_achievement_date | certification_requirements | skill_requirements | experience_requirements | development_plan | training_plan | mentor_id | supervisor_id | performance_rating | last_evaluation_date | next_evaluation_date | evaluation_frequency | career_path | strengths | improvement_areas | achievements | goals | workload_percentage | billable_flag | cost_center | budget_allocation | hourly_rate | overtime_eligible | remote_work_eligible | travel_required | security_clearance_required | created_by | approved_by | approval_date | notes |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| EJT_001 | EMP000001 | JOB_001 | PRIMARY | 100.0 | 2024-04-01 | None | NEW_HIRE | ACTIVE | INTERMEDIATE | ADVANCED | 2025-03-31 | ["基本情報技術者試験", "AWS認定"] | ["Java", "Spring Boot", "AWS", "Docker"] | ["Webアプリケーション開発", "チーム開発"] | {"short_term": "AWS認定取得", "medium_term": "チームリーダー経験", "long_term": "アーキテクト昇格"} | ["TRN_PROG_002", "TRN_PROG_006"] | EMP000010 | EMP000005 | GOOD | 2024-03-31 | 2024-06-30 | QUARTERLY | シニアエンジニア → テックリード → アーキテクト | 技術習得力、問題解決能力、チームワーク | リーダーシップ、プレゼンテーション | 新人研修システム開発、パフォーマンス改善20%達成 | AWS認定取得、チームリーダー経験積む | 100.0 | True | DEV001 | 5000000.0 | 3500.0 | True | True | False | False | EMP000005 | EMP000008 | 2024-03-25 | 新卒採用、高いポテンシャルを持つ |
| EJT_002 | EMP000002 | JOB_002 | PRIMARY | 80.0 | 2024-01-01 | None | PROMOTION | ACTIVE | ADVANCED | EXPERT | 2024-12-31 | ["PMP", "ITストラテジスト"] | ["プロジェクト管理", "リーダーシップ", "ステークホルダー管理"] | ["大規模プロジェクト管理", "チームマネジメント"] | {"short_term": "PMP取得", "medium_term": "大規模PM経験", "long_term": "PMO責任者"} | ["TRN_PROG_001", "TRN_PROG_007"] | EMP000015 | EMP000008 | EXCELLENT | 2024-04-30 | 2024-07-31 | QUARTERLY | プロジェクトマネージャー → シニアPM → PMO責任者 | プロジェクト管理、コミュニケーション、問題解決 | 戦略立案、予算管理 | 3つの大規模プロジェクト成功、チーム満足度向上 | PMP取得、PMO体制構築 | 80.0 | True | PMO001 | 8000000.0 | 5000.0 | False | True | True | False | EMP000008 | EMP000001 | 2023-12-15 | 技術者からPMへの転身成功例 |

## 特記事項

- 複数職種の兼任に対応（配属比率で管理）
- 職種変更履歴を時系列で追跡可能
- 習熟度と目標設定で成長を管理
- メンター制度との連携で効果的な指導
- パフォーマンス評価で適性を判定
- コスト管理・請求管理との連携
- 社員職種関連IDは一意である必要がある
- 配属比率の合計は100%以下である必要がある
- 有効開始日は有効終了日以前である必要がある
- 主職種（PRIMARY）は1つのみ設定可能
- 目標習熟度は現在の習熟度以上である必要がある
- 評価日は定期的に更新される必要がある
- 承認済み関連付けのみ有効
- メンターと上司は異なる人物である必要がある

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 社員職種関連マスタの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214906 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_214959 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215053 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223432 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |