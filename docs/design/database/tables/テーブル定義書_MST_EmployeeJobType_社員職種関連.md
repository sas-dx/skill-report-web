# テーブル定義書: MST_EmployeeJobType (社員職種関連)

## 📋 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_EmployeeJobType |
| 論理名 | 社員職種関連 |
| カテゴリ | マスタ系 |
| 作成日 | 2025-06-01 |

> **注意**: 本テーブル定義書は自動生成されます。手動編集は行わないでください。
> 詳細定義の変更は `table-details/MST_EmployeeJobType_details.yaml` で行ってください。


## 📝 改版履歴

> **注意**: 改版履歴の詳細は以下のYAMLファイルで管理されています：
> `table-details/TABLE_NAME_details.yaml`

| バージョン | 更新日 | 更新者 | 主な変更内容 |
|------------|--------|--------|-------------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 社員職種関連マスタの詳細定義 |


## 📝 テーブル概要

MST_EmployeeJobType（社員職種関連）は、社員と職種の関連付けを管理するマスタテーブルです。

主な目的：
- 社員の職種履歴管理
- 複数職種対応（兼任・転職）
- 職種変更の追跡
- 人材配置の最適化
- スキル要件との連携

このテーブルにより、社員の職種変遷を正確に管理し、
適切な人材配置とキャリア開発を支援できます。


## 🗂️ カラム定義

| カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト | 説明 |
|----------|--------|----------|------|------|----|----|------------|------|
| id | ID | VARCHAR | 50 | × | ● |  |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × |  |  |  | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  |  |  | マルチテナント識別子 |
| employee_job_type_id | 社員職種関連ID | VARCHAR | 50 | ○ |  |  |  | 社員職種関連を一意に識別するID |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | ● |  | 対象社員のID（MST_Employeeへの外部キー） |
| job_type_id | 職種ID | VARCHAR | 50 | ○ |  | ● |  | 職種のID（MST_JobTypeへの外部キー） |
| assignment_type | 配属種別 | ENUM |  | ○ |  |  |  | 職種への配属種別（PRIMARY:主職種、SECONDARY:副職種、TEMPORARY:一時的、TRAINING:研修中、CANDIDATE:候補） |
| assignment_ratio | 配属比率 | DECIMAL | 5,2 | ○ |  |  | 100.0 | 職種への配属比率（%） |
| effective_start_date | 有効開始日 | DATE |  | ○ |  |  |  | 職種配属の開始日 |
| effective_end_date | 有効終了日 | DATE |  | ○ |  |  |  | 職種配属の終了日 |
| assignment_reason | 配属理由 | ENUM |  | ○ |  |  |  | 職種配属の理由（NEW_HIRE:新規採用、PROMOTION:昇進、TRANSFER:異動、SKILL_DEVELOPMENT:スキル開発、PROJECT_NEED:プロジェクト要請、REORGANIZATION:組織再編） |
| assignment_status | 配属状況 | ENUM |  | ○ |  |  | ACTIVE | 現在の配属状況（ACTIVE:有効、INACTIVE:無効、PENDING:保留中、SUSPENDED:一時停止） |
| proficiency_level | 習熟度 | ENUM |  | ○ |  |  | NOVICE | 職種における習熟度（NOVICE:初心者、BEGINNER:初級、INTERMEDIATE:中級、ADVANCED:上級、EXPERT:エキスパート） |
| target_proficiency_level | 目標習熟度 | ENUM |  | ○ |  |  |  | 目標とする習熟度（NOVICE:初心者、BEGINNER:初級、INTERMEDIATE:中級、ADVANCED:上級、EXPERT:エキスパート） |
| target_achievement_date | 目標達成日 | DATE |  | ○ |  |  |  | 目標習熟度の達成予定日 |
| certification_requirements | 必要資格 | TEXT |  | ○ |  |  |  | 職種に必要な資格一覧（JSON形式） |
| skill_requirements | 必要スキル | TEXT |  | ○ |  |  |  | 職種に必要なスキル一覧（JSON形式） |
| experience_requirements | 必要経験 | TEXT |  | ○ |  |  |  | 職種に必要な経験・実績（JSON形式） |
| development_plan | 育成計画 | TEXT |  | ○ |  |  |  | 職種における育成計画（JSON形式） |
| training_plan | 研修計画 | TEXT |  | ○ |  |  |  | 推奨研修プログラム（JSON形式） |
| mentor_id | メンターID | VARCHAR | 50 | ○ |  | ● |  | 職種指導担当者のID（MST_Employeeへの外部キー） |
| supervisor_id | 上司ID | VARCHAR | 50 | ○ |  | ● |  | 職種における直属上司のID（MST_Employeeへの外部キー） |
| performance_rating | パフォーマンス評価 | ENUM |  | ○ |  |  |  | 職種でのパフォーマンス評価（EXCELLENT:優秀、GOOD:良好、SATISFACTORY:普通、NEEDS_IMPROVEMENT:要改善、UNSATISFACTORY:不満足） |
| last_evaluation_date | 最終評価日 | DATE |  | ○ |  |  |  | 最後に評価を実施した日付 |
| next_evaluation_date | 次回評価日 | DATE |  | ○ |  |  |  | 次回評価予定日 |
| evaluation_frequency | 評価頻度 | ENUM |  | ○ |  |  | QUARTERLY | 評価の実施頻度（MONTHLY:月次、QUARTERLY:四半期、SEMI_ANNUAL:半年、ANNUAL:年次） |
| career_path | キャリアパス | TEXT |  | ○ |  |  |  | 職種でのキャリアパス・将来展望 |
| strengths | 強み | TEXT |  | ○ |  |  |  | 職種における強み・得意分野 |
| improvement_areas | 改善領域 | TEXT |  | ○ |  |  |  | 改善が必要な領域・課題 |
| achievements | 実績 | TEXT |  | ○ |  |  |  | 職種での主要な実績・成果 |
| goals | 目標 | TEXT |  | ○ |  |  |  | 職種での短期・中期目標 |
| workload_percentage | 業務負荷率 | DECIMAL | 5,2 | ○ |  |  | 100.0 | 全業務に占める職種業務の割合（%） |
| billable_flag | 請求対象フラグ | BOOLEAN |  | ○ |  |  | True | 顧客請求対象の職種かどうか |
| cost_center | コストセンター | VARCHAR | 20 | ○ |  |  |  | 職種に関連するコストセンター |
| budget_allocation | 予算配分 | DECIMAL | 10,2 | ○ |  |  |  | 職種に配分された予算 |
| hourly_rate | 時間単価 | DECIMAL | 8,2 | ○ |  |  |  | 職種での時間単価 |
| overtime_eligible | 残業対象フラグ | BOOLEAN |  | ○ |  |  | True | 残業代支給対象かどうか |
| remote_work_eligible | リモートワーク可否 | BOOLEAN |  | ○ |  |  |  | リモートワーク可能な職種かどうか |
| travel_required | 出張要否 | BOOLEAN |  | ○ |  |  |  | 出張が必要な職種かどうか |
| security_clearance_required | セキュリティクリアランス要否 | BOOLEAN |  | ○ |  |  |  | セキュリティクリアランスが必要かどうか |
| created_by | 作成者 | VARCHAR | 50 | ○ |  | ● |  | 関連付けを作成した担当者ID |
| approved_by | 承認者 | VARCHAR | 50 | ○ |  | ● |  | 関連付けを承認した責任者ID |
| approval_date | 承認日 | DATE |  | ○ |  |  |  | 関連付けが承認された日付 |
| notes | 備考 | TEXT |  | ○ |  |  |  | その他の備考・特記事項 |
| created_at | 作成日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  | ● |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  |  |  | レコード更新者のユーザーID |

## 🔍 インデックス定義

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

## 🔒 制約定義

| 制約名 | 制約タイプ | 対象カラム | 条件 | 説明 |
|--------|------------|------------|------|------|
| uk_employee_job_type_id | UNIQUE | employee_job_type_id |  | 社員職種関連ID一意制約 |
| chk_assignment_type | CHECK |  | assignment_type IN ('PRIMARY', 'SECONDARY', 'TEMPORARY', 'TRAINING', 'CANDIDATE') | 配属種別値チェック制約 |
| chk_assignment_status | CHECK |  | assignment_status IN ('ACTIVE', 'INACTIVE', 'PENDING', 'SUSPENDED') | 配属状況値チェック制約 |
| chk_proficiency_level | CHECK |  | proficiency_level IN ('NOVICE', 'BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT') | 習熟度値チェック制約 |
| chk_target_proficiency_level | CHECK |  | target_proficiency_level IN ('NOVICE', 'BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT') | 目標習熟度値チェック制約 |
| chk_assignment_reason | CHECK |  | assignment_reason IN ('NEW_HIRE', 'PROMOTION', 'TRANSFER', 'SKILL_DEVELOPMENT', 'PROJECT_NEED', 'REORGANIZATION') | 配属理由値チェック制約 |
| chk_performance_rating | CHECK |  | performance_rating IN ('EXCELLENT', 'GOOD', 'SATISFACTORY', 'NEEDS_IMPROVEMENT', 'UNSATISFACTORY') | パフォーマンス評価値チェック制約 |
| chk_evaluation_frequency | CHECK |  | evaluation_frequency IN ('MONTHLY', 'QUARTERLY', 'SEMI_ANNUAL', 'ANNUAL') | 評価頻度値チェック制約 |
| chk_assignment_ratio_range | CHECK |  | assignment_ratio >= 0 AND assignment_ratio <= 100 | 配属比率範囲チェック制約 |
| chk_workload_percentage_range | CHECK |  | workload_percentage >= 0 AND workload_percentage <= 100 | 業務負荷率範囲チェック制約 |
| chk_effective_period | CHECK |  | effective_end_date IS NULL OR effective_start_date <= effective_end_date | 有効期間整合性チェック制約 |
| chk_budget_allocation_positive | CHECK |  | budget_allocation IS NULL OR budget_allocation >= 0 | 予算配分非負数チェック制約 |
| chk_hourly_rate_positive | CHECK |  | hourly_rate IS NULL OR hourly_rate >= 0 | 時間単価非負数チェック制約 |

## 🔗 外部キー関係

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|------------|--------|--------------|------------|--------|--------|------|
| fk_emp_job_type_employee | employee_id | MST_Employee | id | CASCADE | CASCADE | 社員への外部キー |
| fk_emp_job_type_job_type | job_type_id | MST_JobType | id | CASCADE | RESTRICT | 職種への外部キー |
| fk_emp_job_type_mentor | mentor_id | MST_Employee | id | CASCADE | SET NULL | メンターへの外部キー |
| fk_emp_job_type_supervisor | supervisor_id | MST_Employee | id | CASCADE | SET NULL | 上司への外部キー |
| fk_emp_job_type_created_by | created_by | MST_Employee | id | CASCADE | RESTRICT | 作成者への外部キー |
| fk_emp_job_type_approved_by | approved_by | MST_Employee | id | CASCADE | SET NULL | 承認者への外部キー |

## 📊 サンプルデータ

```json
[
  {
    "employee_job_type_id": "EJT_001",
    "employee_id": "EMP000001",
    "job_type_id": "JOB_001",
    "assignment_type": "PRIMARY",
    "assignment_ratio": 100.0,
    "effective_start_date": "2024-04-01",
    "effective_end_date": null,
    "assignment_reason": "NEW_HIRE",
    "assignment_status": "ACTIVE",
    "proficiency_level": "INTERMEDIATE",
    "target_proficiency_level": "ADVANCED",
    "target_achievement_date": "2025-03-31",
    "certification_requirements": "[\"基本情報技術者試験\", \"AWS認定\"]",
    "skill_requirements": "[\"Java\", \"Spring Boot\", \"AWS\", \"Docker\"]",
    "experience_requirements": "[\"Webアプリケーション開発\", \"チーム開発\"]",
    "development_plan": "{\"short_term\": \"AWS認定取得\", \"medium_term\": \"チームリーダー経験\", \"long_term\": \"アーキテクト昇格\"}",
    "training_plan": "[\"TRN_PROG_002\", \"TRN_PROG_006\"]",
    "mentor_id": "EMP000010",
    "supervisor_id": "EMP000005",
    "performance_rating": "GOOD",
    "last_evaluation_date": "2024-03-31",
    "next_evaluation_date": "2024-06-30",
    "evaluation_frequency": "QUARTERLY",
    "career_path": "シニアエンジニア → テックリード → アーキテクト",
    "strengths": "技術習得力、問題解決能力、チームワーク",
    "improvement_areas": "リーダーシップ、プレゼンテーション",
    "achievements": "新人研修システム開発、パフォーマンス改善20%達成",
    "goals": "AWS認定取得、チームリーダー経験積む",
    "workload_percentage": 100.0,
    "billable_flag": true,
    "cost_center": "DEV001",
    "budget_allocation": 5000000.0,
    "hourly_rate": 3500.0,
    "overtime_eligible": true,
    "remote_work_eligible": true,
    "travel_required": false,
    "security_clearance_required": false,
    "created_by": "EMP000005",
    "approved_by": "EMP000008",
    "approval_date": "2024-03-25",
    "notes": "新卒採用、高いポテンシャルを持つ"
  },
  {
    "employee_job_type_id": "EJT_002",
    "employee_id": "EMP000002",
    "job_type_id": "JOB_002",
    "assignment_type": "PRIMARY",
    "assignment_ratio": 80.0,
    "effective_start_date": "2024-01-01",
    "effective_end_date": null,
    "assignment_reason": "PROMOTION",
    "assignment_status": "ACTIVE",
    "proficiency_level": "ADVANCED",
    "target_proficiency_level": "EXPERT",
    "target_achievement_date": "2024-12-31",
    "certification_requirements": "[\"PMP\", \"ITストラテジスト\"]",
    "skill_requirements": "[\"プロジェクト管理\", \"リーダーシップ\", \"ステークホルダー管理\"]",
    "experience_requirements": "[\"大規模プロジェクト管理\", \"チームマネジメント\"]",
    "development_plan": "{\"short_term\": \"PMP取得\", \"medium_term\": \"大規模PM経験\", \"long_term\": \"PMO責任者\"}",
    "training_plan": "[\"TRN_PROG_001\", \"TRN_PROG_007\"]",
    "mentor_id": "EMP000015",
    "supervisor_id": "EMP000008",
    "performance_rating": "EXCELLENT",
    "last_evaluation_date": "2024-04-30",
    "next_evaluation_date": "2024-07-31",
    "evaluation_frequency": "QUARTERLY",
    "career_path": "プロジェクトマネージャー → シニアPM → PMO責任者",
    "strengths": "プロジェクト管理、コミュニケーション、問題解決",
    "improvement_areas": "戦略立案、予算管理",
    "achievements": "3つの大規模プロジェクト成功、チーム満足度向上",
    "goals": "PMP取得、PMO体制構築",
    "workload_percentage": 80.0,
    "billable_flag": true,
    "cost_center": "PMO001",
    "budget_allocation": 8000000.0,
    "hourly_rate": 5000.0,
    "overtime_eligible": false,
    "remote_work_eligible": true,
    "travel_required": true,
    "security_clearance_required": false,
    "created_by": "EMP000008",
    "approved_by": "EMP000001",
    "approval_date": "2023-12-15",
    "notes": "技術者からPMへの転身成功例"
  }
]
```

## 📌 特記事項

- 複数職種の兼任に対応（配属比率で管理）
- 職種変更履歴を時系列で追跡可能
- 習熟度と目標設定で成長を管理
- メンター制度との連携で効果的な指導
- パフォーマンス評価で適性を判定
- コスト管理・請求管理との連携

## 📋 業務ルール

- 社員職種関連IDは一意である必要がある
- 配属比率の合計は100%以下である必要がある
- 有効開始日は有効終了日以前である必要がある
- 主職種（PRIMARY）は1つのみ設定可能
- 目標習熟度は現在の習熟度以上である必要がある
- 評価日は定期的に更新される必要がある
- 承認済み関連付けのみ有効
- メンターと上司は異なる人物である必要がある
