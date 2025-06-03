# テーブル定義書: MST_CareerPlan

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_CareerPlan |
| 論理名 | 目標・キャリアプラン |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-04 06:57:02 |

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
| career_plan_id | キャリアプランID | VARCHAR | 50 | ○ |  | キャリアプランを一意に識別するID |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | 対象社員のID（MST_Employeeへの外部キー） |
| plan_name | プラン名 | VARCHAR | 200 | ○ |  | キャリアプランの名称 |
| plan_description | プラン説明 | TEXT |  | ○ |  | キャリアプランの詳細説明 |
| plan_type | プラン種別 | ENUM |  | ○ |  | プランの種別（SHORT_TERM:短期、MEDIUM_TERM:中期、LONG_TERM:長期、SPECIALIZED:専門特化、MANAGEMENT:管理職、TECHNICAL:技術職） |
| target_position_id | 目標役職ID | VARCHAR | 50 | ○ |  | 目標とする役職のID（MST_Positionへの外部キー） |
| target_job_type_id | 目標職種ID | VARCHAR | 50 | ○ |  | 目標とする職種のID（MST_JobTypeへの外部キー） |
| target_department_id | 目標部署ID | VARCHAR | 50 | ○ |  | 目標とする部署のID（MST_Departmentへの外部キー） |
| current_level | 現在レベル | ENUM |  | ○ |  | 現在のキャリアレベル（ENTRY:新人、JUNIOR:初級、INTERMEDIATE:中級、SENIOR:上級、EXPERT:エキスパート、MANAGER:管理職、EXECUTIVE:役員） |
| target_level | 目標レベル | ENUM |  | ○ |  | 目標とするキャリアレベル（ENTRY:新人、JUNIOR:初級、INTERMEDIATE:中級、SENIOR:上級、EXPERT:エキスパート、MANAGER:管理職、EXECUTIVE:役員） |
| plan_start_date | プラン開始日 | DATE |  | ○ |  | キャリアプランの開始日 |
| plan_end_date | プラン終了日 | DATE |  | ○ |  | キャリアプランの目標達成予定日 |
| milestone_1_date | マイルストーン1日付 | DATE |  | ○ |  | 第1マイルストーンの目標日 |
| milestone_1_description | マイルストーン1説明 | VARCHAR | 500 | ○ |  | 第1マイルストーンの内容説明 |
| milestone_2_date | マイルストーン2日付 | DATE |  | ○ |  | 第2マイルストーンの目標日 |
| milestone_2_description | マイルストーン2説明 | VARCHAR | 500 | ○ |  | 第2マイルストーンの内容説明 |
| milestone_3_date | マイルストーン3日付 | DATE |  | ○ |  | 第3マイルストーンの目標日 |
| milestone_3_description | マイルストーン3説明 | VARCHAR | 500 | ○ |  | 第3マイルストーンの内容説明 |
| required_skills | 必要スキル | TEXT |  | ○ |  | 目標達成に必要なスキル一覧（JSON形式） |
| required_certifications | 必要資格 | TEXT |  | ○ |  | 目標達成に必要な資格一覧（JSON形式） |
| required_experiences | 必要経験 | TEXT |  | ○ |  | 目標達成に必要な経験・実績（JSON形式） |
| development_actions | 育成アクション | TEXT |  | ○ |  | 具体的な育成・開発アクション（JSON形式） |
| training_plan | 研修計画 | TEXT |  | ○ |  | 推奨研修・教育プログラム（JSON形式） |
| mentor_id | メンターID | VARCHAR | 50 | ○ |  | 指導担当者のID（MST_Employeeへの外部キー） |
| supervisor_id | 上司ID | VARCHAR | 50 | ○ |  | 直属上司のID（MST_Employeeへの外部キー） |
| plan_status | プラン状況 | ENUM |  | ○ | DRAFT | プランの進捗状況（DRAFT:下書き、ACTIVE:実行中、ON_HOLD:保留、COMPLETED:完了、CANCELLED:中止、REVISED:改訂） |
| progress_percentage | 進捗率 | DECIMAL | 5,2 | ○ | 0.0 | プランの進捗率（0.00-100.00） |
| last_review_date | 最終レビュー日 | DATE |  | ○ |  | 最後にレビューを実施した日付 |
| next_review_date | 次回レビュー日 | DATE |  | ○ |  | 次回レビュー予定日 |
| review_frequency | レビュー頻度 | ENUM |  | ○ | QUARTERLY | レビューの実施頻度（MONTHLY:月次、QUARTERLY:四半期、SEMI_ANNUAL:半年、ANNUAL:年次） |
| success_criteria | 成功基準 | TEXT |  | ○ |  | プラン成功の判定基準 |
| risk_factors | リスク要因 | TEXT |  | ○ |  | 目標達成のリスク要因・課題 |
| support_resources | 支援リソース | TEXT |  | ○ |  | 利用可能な支援・リソース情報 |
| budget_allocated | 割当予算 | DECIMAL | 10,2 | ○ |  | プラン実行のための割当予算 |
| budget_used | 使用予算 | DECIMAL | 10,2 | ○ | 0.0 | 実際に使用した予算 |
| priority_level | 優先度 | ENUM |  | ○ | NORMAL | プランの優先度（LOW:低、NORMAL:通常、HIGH:高、CRITICAL:最重要） |
| visibility_level | 公開レベル | ENUM |  | ○ | MANAGER | プランの公開範囲（PRIVATE:本人のみ、MANAGER:上司まで、DEPARTMENT:部署内、COMPANY:全社） |
| template_id | テンプレートID | VARCHAR | 50 | ○ |  | 使用したプランテンプレートのID |
| custom_fields | カスタムフィールド | TEXT |  | ○ |  | 組織固有の追加項目（JSON形式） |
| notes | 備考 | TEXT |  | ○ |  | その他の備考・メモ |
| code | コード | VARCHAR | 20 | × |  | マスタコード |
| name | 名称 | VARCHAR | 100 | × |  | マスタ名称 |
| description | 説明 | TEXT |  | ○ |  | マスタ説明 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_career_plan_id | career_plan_id | ○ | キャリアプランID検索用（一意） |
| idx_employee_id | employee_id | × | 社員ID検索用 |
| idx_plan_type | plan_type | × | プラン種別検索用 |
| idx_target_position | target_position_id | × | 目標役職検索用 |
| idx_target_job_type | target_job_type_id | × | 目標職種検索用 |
| idx_plan_status | plan_status | × | プラン状況検索用 |
| idx_plan_period | plan_start_date, plan_end_date | × | プラン期間検索用 |
| idx_review_date | next_review_date | × | レビュー日検索用 |
| idx_mentor_id | mentor_id | × | メンター検索用 |
| idx_supervisor_id | supervisor_id | × | 上司検索用 |
| idx_priority_level | priority_level | × | 優先度検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_career_plan_employee | employee_id | MST_Employee | id | CASCADE | RESTRICT | 社員への外部キー |
| fk_career_plan_target_position | target_position_id | MST_Position | id | CASCADE | SET NULL | 目標役職への外部キー |
| fk_career_plan_target_job_type | target_job_type_id | MST_JobType | id | CASCADE | SET NULL | 目標職種への外部キー |
| fk_career_plan_target_department | target_department_id | MST_Department | id | CASCADE | SET NULL | 目標部署への外部キー |
| fk_career_plan_mentor | mentor_id | MST_Employee | id | CASCADE | SET NULL | メンターへの外部キー |
| fk_career_plan_supervisor | supervisor_id | MST_Employee | id | CASCADE | SET NULL | 上司への外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_career_plan_id | UNIQUE |  | キャリアプランID一意制約 |
| chk_plan_type | CHECK | plan_type IN ('SHORT_TERM', 'MEDIUM_TERM', 'LONG_TERM', 'SPECIALIZED', 'MANAGEMENT', 'TECHNICAL') | プラン種別値チェック制約 |
| chk_current_level | CHECK | current_level IN ('ENTRY', 'JUNIOR', 'INTERMEDIATE', 'SENIOR', 'EXPERT', 'MANAGER', 'EXECUTIVE') | 現在レベル値チェック制約 |
| chk_target_level | CHECK | target_level IN ('ENTRY', 'JUNIOR', 'INTERMEDIATE', 'SENIOR', 'EXPERT', 'MANAGER', 'EXECUTIVE') | 目標レベル値チェック制約 |
| chk_plan_status | CHECK | plan_status IN ('DRAFT', 'ACTIVE', 'ON_HOLD', 'COMPLETED', 'CANCELLED', 'REVISED') | プラン状況値チェック制約 |
| chk_review_frequency | CHECK | review_frequency IN ('MONTHLY', 'QUARTERLY', 'SEMI_ANNUAL', 'ANNUAL') | レビュー頻度値チェック制約 |
| chk_priority_level | CHECK | priority_level IN ('LOW', 'NORMAL', 'HIGH', 'CRITICAL') | 優先度値チェック制約 |
| chk_visibility_level | CHECK | visibility_level IN ('PRIVATE', 'MANAGER', 'DEPARTMENT', 'COMPANY') | 公開レベル値チェック制約 |
| chk_plan_period | CHECK | plan_start_date <= plan_end_date | プラン期間整合性チェック制約 |
| chk_progress_percentage | CHECK | progress_percentage >= 0.00 AND progress_percentage <= 100.00 | 進捗率範囲チェック制約 |
| chk_budget_positive | CHECK | budget_allocated IS NULL OR budget_allocated >= 0 | 割当予算非負数チェック制約 |
| chk_budget_used_positive | CHECK | budget_used >= 0 | 使用予算非負数チェック制約 |

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

## 業務ルール

- キャリアプランIDは一意である必要がある
- プラン開始日は終了日以前である必要がある
- 進捗率は0-100%の範囲で設定
- 使用予算は割当予算以下である必要がある
- 目標レベルは現在レベル以上である必要がある
- レビュー日は定期的に更新される必要がある
- 完了したプランは変更不可
- メンターと上司は異なる人物である必要がある

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 目標・キャリアプランマスタの詳細定義 |
