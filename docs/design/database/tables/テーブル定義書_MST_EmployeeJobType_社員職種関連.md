# テーブル定義書_MST_EmployeeJobType_社員職種関連

## 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_EmployeeJobType |
| 論理名 | 社員職種関連 |
| カテゴリ | マスタ系 |
| 作成日 | 2025-06-01 |
| 作成者 | 開発チーム |
| バージョン | 1.0.0 |

## テーブル概要

MST_EmployeeJobType（社員職種関連）は、社員と職種の関連付けを管理するマスタテーブルです。

### 主な目的
- 社員の職種履歴管理
- 複数職種対応（兼任・転職）
- 職種変更の追跡
- 人材配置の最適化
- スキル要件との連携

このテーブルにより、社員の職種変遷を正確に管理し、適切な人材配置とキャリア開発を支援できます。

## カラム定義

| # | カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|---|----------|--------|----------|------|------|------------|------|
| 1 | id | ID | VARCHAR | 50 | NOT NULL | | 共通ID（主キー） |
| 2 | employee_job_type_id | 社員職種関連ID | VARCHAR | 50 | NOT NULL | | 社員職種関連を一意に識別するID |
| 3 | employee_id | 社員ID | VARCHAR | 50 | NOT NULL | | 対象社員のID（MST_Employeeへの外部キー） |
| 4 | job_type_id | 職種ID | VARCHAR | 50 | NOT NULL | | 職種のID（MST_JobTypeへの外部キー） |
| 5 | assignment_type | 配属種別 | ENUM | | NOT NULL | | 職種への配属種別（PRIMARY:主職種、SECONDARY:副職種、TEMPORARY:一時的、TRAINING:研修中、CANDIDATE:候補） |
| 6 | assignment_ratio | 配属比率 | DECIMAL | 5,2 | NOT NULL | 100.00 | 職種への配属比率（%） |
| 7 | effective_start_date | 有効開始日 | DATE | | NOT NULL | | 職種配属の開始日 |
| 8 | effective_end_date | 有効終了日 | DATE | | NULL | | 職種配属の終了日 |
| 9 | assignment_reason | 配属理由 | ENUM | | NOT NULL | | 職種配属の理由（NEW_HIRE:新規採用、PROMOTION:昇進、TRANSFER:異動、SKILL_DEVELOPMENT:スキル開発、PROJECT_NEED:プロジェクト要請、REORGANIZATION:組織再編） |
| 10 | assignment_status | 配属状況 | ENUM | | NOT NULL | ACTIVE | 現在の配属状況（ACTIVE:有効、INACTIVE:無効、PENDING:保留中、SUSPENDED:一時停止） |
| 11 | proficiency_level | 習熟度 | ENUM | | NOT NULL | NOVICE | 職種における習熟度（NOVICE:初心者、BEGINNER:初級、INTERMEDIATE:中級、ADVANCED:上級、EXPERT:エキスパート） |
| 12 | target_proficiency_level | 目標習熟度 | ENUM | | NULL | | 目標とする習熟度（NOVICE:初心者、BEGINNER:初級、INTERMEDIATE:中級、ADVANCED:上級、EXPERT:エキスパート） |
| 13 | target_achievement_date | 目標達成日 | DATE | | NULL | | 目標習熟度の達成予定日 |
| 14 | certification_requirements | 必要資格 | TEXT | | NULL | | 職種に必要な資格一覧（JSON形式） |
| 15 | skill_requirements | 必要スキル | TEXT | | NULL | | 職種に必要なスキル一覧（JSON形式） |
| 16 | experience_requirements | 必要経験 | TEXT | | NULL | | 職種に必要な経験・実績（JSON形式） |
| 17 | development_plan | 育成計画 | TEXT | | NULL | | 職種における育成計画（JSON形式） |
| 18 | training_plan | 研修計画 | TEXT | | NULL | | 推奨研修プログラム（JSON形式） |
| 19 | mentor_id | メンターID | VARCHAR | 50 | NULL | | 職種指導担当者のID（MST_Employeeへの外部キー） |
| 20 | supervisor_id | 上司ID | VARCHAR | 50 | NULL | | 職種における直属上司のID（MST_Employeeへの外部キー） |
| 21 | performance_rating | パフォーマンス評価 | ENUM | | NULL | | 職種でのパフォーマンス評価（EXCELLENT:優秀、GOOD:良好、SATISFACTORY:普通、NEEDS_IMPROVEMENT:要改善、UNSATISFACTORY:不満足） |
| 22 | last_evaluation_date | 最終評価日 | DATE | | NULL | | 最後に評価を実施した日付 |
| 23 | next_evaluation_date | 次回評価日 | DATE | | NULL | | 次回評価予定日 |
| 24 | evaluation_frequency | 評価頻度 | ENUM | | NOT NULL | QUARTERLY | 評価の実施頻度（MONTHLY:月次、QUARTERLY:四半期、SEMI_ANNUAL:半年、ANNUAL:年次） |
| 25 | career_path | キャリアパス | TEXT | | NULL | | 職種でのキャリアパス・将来展望 |
| 26 | strengths | 強み | TEXT | | NULL | | 職種における強み・得意分野 |
| 27 | improvement_areas | 改善領域 | TEXT | | NULL | | 改善が必要な領域・課題 |
| 28 | achievements | 実績 | TEXT | | NULL | | 職種での主要な実績・成果 |
| 29 | goals | 目標 | TEXT | | NULL | | 職種での短期・中期目標 |
| 30 | workload_percentage | 業務負荷率 | DECIMAL | 5,2 | NOT NULL | 100.00 | 全業務に占める職種業務の割合（%） |
| 31 | billable_flag | 請求対象フラグ | BOOLEAN | | NOT NULL | TRUE | 顧客請求対象の職種かどうか |
| 32 | cost_center | コストセンター | VARCHAR | 20 | NULL | | 職種に関連するコストセンター |
| 33 | budget_allocation | 予算配分 | DECIMAL | 10,2 | NULL | | 職種に配分された予算 |
| 34 | hourly_rate | 時間単価 | DECIMAL | 8,2 | NULL | | 職種での時間単価 |
| 35 | overtime_eligible | 残業対象フラグ | BOOLEAN | | NOT NULL | TRUE | 残業代支給対象かどうか |
| 36 | remote_work_eligible | リモートワーク可否 | BOOLEAN | | NOT NULL | FALSE | リモートワーク可能な職種かどうか |
| 37 | travel_required | 出張要否 | BOOLEAN | | NOT NULL | FALSE | 出張が必要な職種かどうか |
| 38 | security_clearance_required | セキュリティクリアランス要否 | BOOLEAN | | NOT NULL | FALSE | セキュリティクリアランスが必要かどうか |
| 39 | created_by | 作成者 | VARCHAR | 50 | NOT NULL | | 関連付けを作成した担当者ID |
| 40 | approved_by | 承認者 | VARCHAR | 50 | NULL | | 関連付けを承認した責任者ID |
| 41 | approval_date | 承認日 | DATE | | NULL | | 関連付けが承認された日付 |
| 42 | notes | 備考 | TEXT | | NULL | | その他の備考・特記事項 |
| 43 | created_at | 作成日時 | TIMESTAMP | | NOT NULL | CURRENT_TIMESTAMP | レコード作成日時 |
| 44 | updated_at | 更新日時 | TIMESTAMP | | NOT NULL | CURRENT_TIMESTAMP | レコード更新日時 |
| 45 | updated_by | 更新者 | VARCHAR | 50 | NOT NULL | | レコード更新者 |
| 46 | version | バージョン | INTEGER | | NOT NULL | 1 | 楽観的排他制御用 |
| 47 | deleted_flag | 削除フラグ | BOOLEAN | | NOT NULL | FALSE | 論理削除フラグ |

## インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|---------------|------|--------|------|
| pk_mst_employee_job_type | PRIMARY KEY | id | 主キー |
| uk_employee_job_type_id | UNIQUE | employee_job_type_id | 社員職種関連ID一意制約 |
| idx_employee_id | INDEX | employee_id | 社員ID検索用 |
| idx_job_type_id | INDEX | job_type_id | 職種ID検索用 |
| idx_employee_job_type | INDEX | employee_id, job_type_id | 社員・職種組み合わせ検索用 |
| idx_assignment_type | INDEX | assignment_type | 配属種別検索用 |
| idx_assignment_status | INDEX | assignment_status | 配属状況検索用 |
| idx_proficiency_level | INDEX | proficiency_level | 習熟度検索用 |
| idx_effective_period | INDEX | effective_start_date, effective_end_date | 有効期間検索用 |
| idx_mentor_id | INDEX | mentor_id | メンター検索用 |
| idx_supervisor_id | INDEX | supervisor_id | 上司検索用 |
| idx_performance_rating | INDEX | performance_rating | パフォーマンス評価検索用 |

## 制約定義

| 制約名 | 種別 | 内容 | 説明 |
|--------|------|------|------|
| pk_mst_employee_job_type | PRIMARY KEY | id | 主キー制約 |
| uk_employee_job_type_id | UNIQUE | employee_job_type_id | 社員職種関連ID一意制約 |
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

## 外部キー定義

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|------------|--------|--------------|------------|--------|--------|------|
| fk_emp_job_type_employee | employee_id | MST_Employee | id | CASCADE | CASCADE | 社員への外部キー |
| fk_emp_job_type_job_type | job_type_id | MST_JobType | id | CASCADE | RESTRICT | 職種への外部キー |
| fk_emp_job_type_mentor | mentor_id | MST_Employee | id | CASCADE | SET NULL | メンターへの外部キー |
| fk_emp_job_type_supervisor | supervisor_id | MST_Employee | id | CASCADE | SET NULL | 上司への外部キー |
| fk_emp_job_type_created_by | created_by | MST_Employee | id | CASCADE | RESTRICT | 作成者への外部キー |
| fk_emp_job_type_approved_by | approved_by | MST_Employee | id | CASCADE | SET NULL | 承認者への外部キー |

## サンプルデータ

| employee_job_type_id | employee_id | job_type_id | assignment_type | assignment_ratio | proficiency_level | assignment_status |
|---------------------|-------------|-------------|-----------------|------------------|-------------------|-------------------|
| EJT_001 | EMP000001 | JOB_001 | PRIMARY | 100.00 | INTERMEDIATE | ACTIVE |
| EJT_002 | EMP000002 | JOB_002 | PRIMARY | 80.00 | ADVANCED | ACTIVE |

## 業務ルール

1. 社員職種関連IDは一意である必要がある
2. 配属比率の合計は100%以下である必要がある
3. 有効開始日は有効終了日以前である必要がある
4. 主職種（PRIMARY）は1つのみ設定可能
5. 目標習熟度は現在の習熟度以上である必要がある
6. 評価日は定期的に更新される必要がある
7. 承認済み関連付けのみ有効
8. メンターと上司は異なる人物である必要がある

## 特記事項

- 複数職種の兼任に対応（配属比率で管理）
- 職種変更履歴を時系列で追跡可能
- 習熟度と目標設定で成長を管理
- メンター制度との連携で効果的な指導
- パフォーマンス評価で適性を判定
- コスト管理・請求管理との連携

## 改版履歴

| バージョン | 日付 | 作成者 | 変更内容 |
|------------|------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 社員職種関連マスタの詳細定義 |
