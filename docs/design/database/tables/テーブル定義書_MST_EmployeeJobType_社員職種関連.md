# テーブル定義書: MST_EmployeeJobType

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_EmployeeJobType |
| 論理名 | 社員職種関連 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-04 06:57:02 |

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
| employee_job_type_id | 社員職種関連ID | VARCHAR | 50 | ○ |  | 社員職種関連を一意に識別するID |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | 対象社員のID（MST_Employeeへの外部キー） |
| job_type_id | 職種ID | VARCHAR | 50 | ○ |  | 職種のID（MST_JobTypeへの外部キー） |
| assignment_type | 配属種別 | ENUM |  | ○ |  | 職種への配属種別（PRIMARY:主職種、SECONDARY:副職種、TEMPORARY:一時的、TRAINING:研修中、CANDIDATE:候補） |
| assignment_ratio | 配属比率 | DECIMAL | 5,2 | ○ | 100.0 | 職種への配属比率（%） |
| effective_start_date | 有効開始日 | DATE |  | ○ |  | 職種配属の開始日 |
| effective_end_date | 有効終了日 | DATE |  | ○ |  | 職種配属の終了日 |
| assignment_reason | 配属理由 | ENUM |  | ○ |  | 職種配属の理由（NEW_HIRE:新規採用、PROMOTION:昇進、TRANSFER:異動、SKILL_DEVELOPMENT:スキル開発、PROJECT_NEED:プロジェクト要請、REORGANIZATION:組織再編） |
| assignment_status | 配属状況 | ENUM |  | ○ | ACTIVE | 現在の配属状況（ACTIVE:有効、INACTIVE:無効、PENDING:保留中、SUSPENDED:一時停止） |
| proficiency_level | 習熟度 | ENUM |  | ○ | NOVICE | 職種における習熟度（NOVICE:初心者、BEGINNER:初級、INTERMEDIATE:中級、ADVANCED:上級、EXPERT:エキスパート） |
| target_proficiency_level | 目標習熟度 | ENUM |  | ○ |  | 目標とする習熟度（NOVICE:初心者、BEGINNER:初級、INTERMEDIATE:中級、ADVANCED:上級、EXPERT:エキスパート） |
| target_achievement_date | 目標達成日 | DATE |  | ○ |  | 目標習熟度の達成予定日 |
| certification_requirements | 必要資格 | TEXT |  | ○ |  | 職種に必要な資格一覧（JSON形式） |
| skill_requirements | 必要スキル | TEXT |  | ○ |  | 職種に必要なスキル一覧（JSON形式） |
| experience_requirements | 必要経験 | TEXT |  | ○ |  | 職種に必要な経験・実績（JSON形式） |
| development_plan | 育成計画 | TEXT |  | ○ |  | 職種における育成計画（JSON形式） |
| training_plan | 研修計画 | TEXT |  | ○ |  | 推奨研修プログラム（JSON形式） |
| mentor_id | メンターID | VARCHAR | 50 | ○ |  | 職種指導担当者のID（MST_Employeeへの外部キー） |
| supervisor_id | 上司ID | VARCHAR | 50 | ○ |  | 職種における直属上司のID（MST_Employeeへの外部キー） |
| performance_rating | パフォーマンス評価 | ENUM |  | ○ |  | 職種でのパフォーマンス評価（EXCELLENT:優秀、GOOD:良好、SATISFACTORY:普通、NEEDS_IMPROVEMENT:要改善、UNSATISFACTORY:不満足） |
| last_evaluation_date | 最終評価日 | DATE |  | ○ |  | 最後に評価を実施した日付 |
| next_evaluation_date | 次回評価日 | DATE |  | ○ |  | 次回評価予定日 |
| evaluation_frequency | 評価頻度 | ENUM |  | ○ | QUARTERLY | 評価の実施頻度（MONTHLY:月次、QUARTERLY:四半期、SEMI_ANNUAL:半年、ANNUAL:年次） |
| career_path | キャリアパス | TEXT |  | ○ |  | 職種でのキャリアパス・将来展望 |
| strengths | 強み | TEXT |  | ○ |  | 職種における強み・得意分野 |
| improvement_areas | 改善領域 | TEXT |  | ○ |  | 改善が必要な領域・課題 |
| achievements | 実績 | TEXT |  | ○ |  | 職種での主要な実績・成果 |
| goals | 目標 | TEXT |  | ○ |  | 職種での短期・中期目標 |
| workload_percentage | 業務負荷率 | DECIMAL | 5,2 | ○ | 100.0 | 全業務に占める職種業務の割合（%） |
| billable_flag | 請求対象フラグ | BOOLEAN |  | ○ | True | 顧客請求対象の職種かどうか |
| cost_center | コストセンター | VARCHAR | 20 | ○ |  | 職種に関連するコストセンター |
| budget_allocation | 予算配分 | DECIMAL | 10,2 | ○ |  | 職種に配分された予算 |
| hourly_rate | 時間単価 | DECIMAL | 8,2 | ○ |  | 職種での時間単価 |
| overtime_eligible | 残業対象フラグ | BOOLEAN |  | ○ | True | 残業代支給対象かどうか |
| remote_work_eligible | リモートワーク可否 | BOOLEAN |  | ○ | False | リモートワーク可能な職種かどうか |
| travel_required | 出張要否 | BOOLEAN |  | ○ | False | 出張が必要な職種かどうか |
| security_clearance_required | セキュリティクリアランス要否 | BOOLEAN |  | ○ | False | セキュリティクリアランスが必要かどうか |
| created_by | 作成者 | VARCHAR | 50 | ○ |  | 関連付けを作成した担当者ID |
| approved_by | 承認者 | VARCHAR | 50 | ○ |  | 関連付けを承認した責任者ID |
| approval_date | 承認日 | DATE |  | ○ |  | 関連付けが承認された日付 |
| notes | 備考 | TEXT |  | ○ |  | その他の備考・特記事項 |
| code | コード | VARCHAR | 20 | × |  | マスタコード |
| name | 名称 | VARCHAR | 100 | × |  | マスタ名称 |
| description | 説明 | TEXT |  | ○ |  | マスタ説明 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_employee_job_type_id | employee_job_type_id | ○ | 社員職種関連ID検索用（一意） |
| idx_employee_id | employee_id | × | 社員ID検索用 |
| idx_job_type_id | job_type_id | × | 職種ID検索用 |
| idx_employee_job_type | employee_id, job_type_id | × | 社員・職種組み合わせ検索用 |
| idx_assignment_type | assignment_type | × | 配属種別検索用 |
| idx_assignment_status | assignment_status | × | 配属状況検索用 |
| idx_proficiency_level | proficiency_level | × | 習熟度検索用 |
| idx_effective_period | effective_start_date, effective_end_date | × | 有効期間検索用 |
| idx_mentor_id | mentor_id | × | メンター検索用 |
| idx_supervisor_id | supervisor_id | × | 上司検索用 |
| idx_performance_rating | performance_rating | × | パフォーマンス評価検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_emp_job_type_employee | employee_id | MST_Employee | id | CASCADE | CASCADE | 社員への外部キー |
| fk_emp_job_type_job_type | job_type_id | MST_JobType | id | CASCADE | RESTRICT | 職種への外部キー |
| fk_emp_job_type_mentor | mentor_id | MST_Employee | id | CASCADE | SET NULL | メンターへの外部キー |
| fk_emp_job_type_supervisor | supervisor_id | MST_Employee | id | CASCADE | SET NULL | 上司への外部キー |
| fk_emp_job_type_created_by | created_by | MST_Employee | id | CASCADE | RESTRICT | 作成者への外部キー |
| fk_emp_job_type_approved_by | approved_by | MST_Employee | id | CASCADE | SET NULL | 承認者への外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_employee_job_type_id | UNIQUE |  | 社員職種関連ID一意制約 |
| chk_assignment_type | CHECK | assignment_type IN ('PRIMARY', 'SECONDARY', 'TEMPORARY', 'TRAINING', 'CANDIDATE') | 配属種別値チェック制約 |
| chk_assignment_status | CHECK | assignment_status IN ('ACTIVE', 'INACTIVE', 'PENDING', 'SUSPENDED') | 配属状況値チェック制約 |
| chk_proficiency_level | CHECK | proficiency_level IN ('NOVICE', 'BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT') | 習熟度値チェック制約 |
| chk_target_proficiency_level | CHECK | target_proficiency_level IN ('NOVICE', 'BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT') | 目標習熟度値チェック制約 |
| chk_assignment_reason | CHECK | assignment_reason IN ('NEW_HIRE', 'PROMOTION', 'TRANSFER', 'SKILL_DEVELOPMENT', 'PROJECT_NEED', 'REORGANIZATION') | 配属理由値チェック制約 |
| chk_performance_rating | CHECK | performance_rating IN ('EXCELLENT', 'GOOD', 'SATISFACTORY', 'NEEDS_IMPROVEMENT', 'UNSATISFACTORY') | パフォーマンス評価値チェック制約 |
| chk_evaluation_frequency | CHECK | evaluation_frequency IN ('MONTHLY', 'QUARTERLY', 'SEMI_ANNUAL', 'ANNUAL') | 評価頻度値チェック制約 |
| chk_assignment_ratio_range | CHECK | assignment_ratio >= 0 AND assignment_ratio <= 100 | 配属比率範囲チェック制約 |
| chk_workload_percentage_range | CHECK | workload_percentage >= 0 AND workload_percentage <= 100 | 業務負荷率範囲チェック制約 |
| chk_effective_period | CHECK | effective_end_date IS NULL OR effective_start_date <= effective_end_date | 有効期間整合性チェック制約 |
| chk_budget_allocation_positive | CHECK | budget_allocation IS NULL OR budget_allocation >= 0 | 予算配分非負数チェック制約 |
| chk_hourly_rate_positive | CHECK | hourly_rate IS NULL OR hourly_rate >= 0 | 時間単価非負数チェック制約 |

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
