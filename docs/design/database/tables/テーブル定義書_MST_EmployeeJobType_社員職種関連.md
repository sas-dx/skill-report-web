# テーブル定義書: MST_EmployeeJobType

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_EmployeeJobType |
| 論理名 | 社員職種関連 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 17:20:35 |

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
| employee_job_type_id |  | VARCHAR |  | ○ |  |  |
| employee_id |  | VARCHAR |  | ○ |  |  |
| job_type_id |  | VARCHAR |  | ○ |  |  |
| assignment_type |  | ENUM |  | ○ |  |  |
| assignment_ratio |  | DECIMAL |  | ○ | 100.0 |  |
| effective_start_date |  | DATE |  | ○ |  |  |
| effective_end_date |  | DATE |  | ○ |  |  |
| assignment_reason |  | ENUM |  | ○ |  |  |
| assignment_status |  | ENUM |  | ○ | ACTIVE |  |
| proficiency_level |  | ENUM |  | ○ | NOVICE |  |
| target_proficiency_level |  | ENUM |  | ○ |  |  |
| target_achievement_date |  | DATE |  | ○ |  |  |
| certification_requirements |  | TEXT |  | ○ |  |  |
| skill_requirements |  | TEXT |  | ○ |  |  |
| experience_requirements |  | TEXT |  | ○ |  |  |
| development_plan |  | TEXT |  | ○ |  |  |
| training_plan |  | TEXT |  | ○ |  |  |
| mentor_id |  | VARCHAR |  | ○ |  |  |
| supervisor_id |  | VARCHAR |  | ○ |  |  |
| performance_rating |  | ENUM |  | ○ |  |  |
| last_evaluation_date |  | DATE |  | ○ |  |  |
| next_evaluation_date |  | DATE |  | ○ |  |  |
| evaluation_frequency |  | ENUM |  | ○ | QUARTERLY |  |
| career_path |  | TEXT |  | ○ |  |  |
| strengths |  | TEXT |  | ○ |  |  |
| improvement_areas |  | TEXT |  | ○ |  |  |
| achievements |  | TEXT |  | ○ |  |  |
| goals |  | TEXT |  | ○ |  |  |
| workload_percentage |  | DECIMAL |  | ○ | 100.0 |  |
| billable_flag |  | BOOLEAN |  | ○ | True |  |
| cost_center |  | VARCHAR |  | ○ |  |  |
| budget_allocation |  | DECIMAL |  | ○ |  |  |
| hourly_rate |  | DECIMAL |  | ○ |  |  |
| overtime_eligible |  | BOOLEAN |  | ○ | True |  |
| remote_work_eligible |  | BOOLEAN |  | ○ | False |  |
| travel_required |  | BOOLEAN |  | ○ | False |  |
| security_clearance_required |  | BOOLEAN |  | ○ | False |  |
| created_by |  | VARCHAR |  | ○ |  |  |
| approved_by |  | VARCHAR |  | ○ |  |  |
| approval_date |  | DATE |  | ○ |  |  |
| notes |  | TEXT |  | ○ |  |  |
| created_at | レコード作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | レコード更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード更新日時 |

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

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_employee_job_type_id | UNIQUE |  | employee_job_type_id一意制約 |
| chk_employee_job_type_id | CHECK | employee_job_type_id IN (...) | employee_job_type_id値チェック制約 |
| chk_job_type_id | CHECK | job_type_id IN (...) | job_type_id値チェック制約 |
| chk_assignment_type | CHECK | assignment_type IN (...) | assignment_type値チェック制約 |
| chk_assignment_status | CHECK | assignment_status IN (...) | assignment_status値チェック制約 |

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

## 業務ルール

- 社員職種関連IDは一意である必要がある
- 配属比率の合計は100%以下である必要がある
- 有効開始日は有効終了日以前である必要がある
- 主職種（PRIMARY）は1つのみ設定可能
- 目標習熟度は現在の習熟度以上である必要がある
- 評価日は定期的に更新される必要がある
- 承認済み関連付けのみ有効
- メンターと上司は異なる人物である必要がある

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 社員職種関連マスタの詳細定義 |