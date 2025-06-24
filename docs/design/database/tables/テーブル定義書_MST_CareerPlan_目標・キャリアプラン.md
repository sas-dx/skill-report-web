# テーブル定義書: MST_CareerPlan

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_CareerPlan |
| 論理名 | 目標・キャリアプラン |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-24 23:05:56 |

## 概要

MST_CareerPlan（目標・キャリアプラン）は、社員の中長期的なキャリア目標と成長計画を管理するマスタテーブルです。
主な目的：
- キャリア目標の設定・管理
- 成長計画の策定支援
- スキル開発ロードマップの提供
- 人事評価・昇進判定の基準設定
- 人材育成計画の立案支援
このテーブルにより、個人の成長と組織の人材戦略を連携させ、
効果的なキャリア開発と人材育成を実現できます。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| plan_name | プラン名 | VARCHAR | 200 | ○ |  | プラン名 |
| budget_allocated | 割当予算 | DECIMAL | 10,2 | ○ |  | 割当予算 |
| budget_used | 使用予算 | DECIMAL | 10,2 | ○ | 0.0 | 使用予算 |
| career_plan_id | キャリアプランID | VARCHAR | 50 | ○ |  | キャリアプランID |
| careerplan_id | MST_CareerPlanの主キー | SERIAL |  | × |  | MST_CareerPlanの主キー |
| current_level | 現在レベル | ENUM |  | ○ |  | 現在レベル |
| custom_fields | カスタムフィールド | TEXT |  | ○ |  | カスタムフィールド |
| development_actions | 育成アクション | TEXT |  | ○ |  | 育成アクション |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | 社員ID |
| last_review_date | 最終レビュー日 | DATE |  | ○ |  | 最終レビュー日 |
| mentor_id | メンターID | VARCHAR | 50 | ○ |  | メンターID |
| milestone_1_date | マイルストーン1日付 | DATE |  | ○ |  | マイルストーン1日付 |
| milestone_1_description | マイルストーン1説明 | VARCHAR | 500 | ○ |  | マイルストーン1説明 |
| milestone_2_date | マイルストーン2日付 | DATE |  | ○ |  | マイルストーン2日付 |
| milestone_2_description | マイルストーン2説明 | VARCHAR | 500 | ○ |  | マイルストーン2説明 |
| milestone_3_date | マイルストーン3日付 | DATE |  | ○ |  | マイルストーン3日付 |
| milestone_3_description | マイルストーン3説明 | VARCHAR | 500 | ○ |  | マイルストーン3説明 |
| next_review_date | 次回レビュー日 | DATE |  | ○ |  | 次回レビュー日 |
| notes | 備考 | TEXT |  | ○ |  | 備考 |
| plan_description | プラン説明 | TEXT |  | ○ |  | プラン説明 |
| plan_end_date | プラン終了日 | DATE |  | ○ |  | プラン終了日 |
| plan_start_date | プラン開始日 | DATE |  | ○ |  | プラン開始日 |
| plan_status | プラン状況 | ENUM |  | ○ | DRAFT | プラン状況 |
| plan_type | プラン種別 | ENUM |  | ○ |  | プラン種別 |
| priority_level | 優先度 | ENUM |  | ○ | NORMAL | 優先度 |
| progress_percentage | 進捗率 | DECIMAL | 5,2 | ○ | 0.0 | 進捗率 |
| required_certifications | 必要資格 | TEXT |  | ○ |  | 必要資格 |
| required_experiences | 必要経験 | TEXT |  | ○ |  | 必要経験 |
| required_skills | 必要スキル | TEXT |  | ○ |  | 必要スキル |
| review_frequency | レビュー頻度 | ENUM |  | ○ | QUARTERLY | レビュー頻度 |
| risk_factors | リスク要因 | TEXT |  | ○ |  | リスク要因 |
| success_criteria | 成功基準 | TEXT |  | ○ |  | 成功基準 |
| supervisor_id | 上司ID | VARCHAR | 50 | ○ |  | 上司ID |
| support_resources | 支援リソース | TEXT |  | ○ |  | 支援リソース |
| target_department_id | 目標部署ID | VARCHAR | 50 | ○ |  | 目標部署ID |
| target_job_type_id | 目標職種ID | VARCHAR | 50 | ○ |  | 目標職種ID |
| target_level | 目標レベル | ENUM |  | ○ |  | 目標レベル |
| target_position_id | 目標役職ID | VARCHAR | 50 | ○ |  | 目標役職ID |
| template_id | テンプレートID | VARCHAR | 50 | ○ |  | テンプレートID |
| training_plan | 研修計画 | TEXT |  | ○ |  | 研修計画 |
| visibility_level | 公開レベル | ENUM |  | ○ | MANAGER | 公開レベル |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_career_plan_id | career_plan_id | ○ |  |
| idx_employee_id | employee_id | × |  |
| idx_plan_type | plan_type | × |  |
| idx_target_position | target_position_id | × |  |
| idx_target_job_type | target_job_type_id | × |  |
| idx_plan_status | plan_status | × |  |
| idx_plan_period | plan_start_date, plan_end_date | × |  |
| idx_review_date | next_review_date | × |  |
| idx_mentor_id | mentor_id | × |  |
| idx_supervisor_id | supervisor_id | × |  |
| idx_priority_level | priority_level | × |  |
| idx_mst_careerplan_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_career_plan_employee | employee_id | MST_Employee | id | CASCADE | RESTRICT | 外部キー制約 |
| fk_career_plan_target_position | target_position_id | MST_Position | id | CASCADE | SET NULL | 外部キー制約 |
| fk_career_plan_target_job_type | target_job_type_id | MST_JobType | id | CASCADE | SET NULL | 外部キー制約 |
| fk_career_plan_target_department | target_department_id | MST_Department | id | CASCADE | SET NULL | 外部キー制約 |
| fk_career_plan_mentor | mentor_id | MST_Employee | id | CASCADE | SET NULL | 外部キー制約 |
| fk_career_plan_supervisor | supervisor_id | MST_Employee | id | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| uk_career_plan_id | UNIQUE |  | career_plan_id一意制約 |
| chk_plan_status | CHECK | plan_status IN (...) | plan_status値チェック制約 |
| chk_plan_type | CHECK | plan_type IN (...) | plan_type値チェック制約 |
| chk_target_job_type_id | CHECK | target_job_type_id IN (...) | target_job_type_id値チェック制約 |

## サンプルデータ

| career_plan_id | employee_id | plan_name | plan_description | plan_type | target_position_id | target_job_type_id | target_department_id | current_level | target_level | plan_start_date | plan_end_date | milestone_1_date | milestone_1_description | milestone_2_date | milestone_2_description | milestone_3_date | milestone_3_description | required_skills | required_certifications | required_experiences | development_actions | training_plan | mentor_id | supervisor_id | plan_status | progress_percentage | last_review_date | next_review_date | review_frequency | success_criteria | risk_factors | support_resources | budget_allocated | budget_used | priority_level | visibility_level | template_id | custom_fields | notes |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| CP_001 | EMP000001 | シニアエンジニアへの成長プラン | 3年以内にシニアエンジニアとして技術リーダーシップを発揮できる人材になる | MEDIUM_TERM | POS_003 | JOB_001 | None | INTERMEDIATE | SENIOR | 2024-04-01 | 2027-03-31 | 2024-12-31 | AWS認定資格取得、チームリーダー経験 | 2025-12-31 | 大規模プロジェクトのテックリード担当 | 2026-12-31 | 後輩指導、技術選定の主導 | ["Java", "Spring Boot", "AWS", "Docker", "Kubernetes", "チームマネジメント"] | ["AWS認定ソリューションアーキテクト", "PMP"] | ["チームリーダー経験", "大規模システム設計", "後輩指導"] | ["技術研修受講", "社外勉強会参加", "OSS貢献", "技術ブログ執筆"] | ["AWS研修", "リーダーシップ研修", "アーキテクチャ設計研修"] | EMP000010 | EMP000005 | ACTIVE | 25.5 | 2024-03-31 | 2024-06-30 | QUARTERLY | 技術力向上、チーム貢献、後輩育成実績 | 業務多忙による学習時間確保困難、技術変化への対応 | 社内研修制度、書籍購入支援、外部セミナー参加費補助 | 300000.0 | 75000.0 | HIGH | MANAGER | TMPL_ENG_001 | {"specialization": "バックエンド", "preferred_domain": "金融系"} | 本人の強い意欲と上司の全面的なサポートにより順調に進行中 |
| CP_002 | EMP000002 | プロジェクトマネージャーへの転身プラン | 技術者からプロジェクトマネージャーへのキャリアチェンジ | MANAGEMENT | POS_004 | JOB_002 | None | SENIOR | MANAGER | 2024-01-01 | 2025-12-31 | 2024-06-30 | PMP資格取得、小規模プロジェクト管理経験 | 2024-12-31 | 中規模プロジェクトのサブPM担当 | None | None | ["プロジェクト管理", "リーダーシップ", "コミュニケーション", "リスク管理"] | ["PMP", "ITストラテジスト"] | ["プロジェクト管理", "チームマネジメント", "ステークホルダー調整"] | ["PM研修受講", "PMI勉強会参加", "管理業務OJT"] | ["プロジェクトマネジメント基礎", "リーダーシップ研修", "交渉術研修"] | EMP000015 | EMP000008 | ACTIVE | 60.0 | 2024-04-30 | 2024-07-31 | QUARTERLY | PMP取得、プロジェクト成功実績、チーム満足度向上 | 技術からマネジメントへの意識転換、人間関係構築 | PM研修制度、資格取得支援、メンター制度 | 200000.0 | 120000.0 | HIGH | DEPARTMENT | TMPL_MGR_001 | {"management_style": "コーチング重視", "team_size_target": "10-15名"} | 技術的バックグラウンドを活かしたPMとして期待 |

## 特記事項

- マイルストーンは最大3つまで設定可能
- JSON形式のフィールドは柔軟な拡張に対応
- 予算管理により投資対効果を測定
- メンター制度との連携で効果的な指導を実現
- レビュー頻度により継続的な改善を促進
- 公開レベルによりプライバシーと透明性を両立
- キャリアプランIDは一意である必要がある
- プラン開始日は終了日以前である必要がある
- 進捗率は0-100%の範囲で設定
- 使用予算は割当予算以下である必要がある
- 目標レベルは現在レベル以上である必要がある
- レビュー日は定期的に更新される必要がある
- 完了したプランは変更不可
- メンターと上司は異なる人物である必要がある

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 目標・キャリアプランマスタの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214905 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_214959 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215052 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222630 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223431 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |