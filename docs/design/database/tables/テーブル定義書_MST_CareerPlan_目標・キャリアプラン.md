# テーブル定義書_MST_CareerPlan_目標・キャリアプラン

## 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_CareerPlan |
| 論理名 | 目標・キャリアプラン |
| カテゴリ | マスタ系 |
| 作成日 | 2025-06-01 |
| 作成者 | 開発チーム |
| バージョン | 1.0.0 |

## テーブル概要

MST_CareerPlan（目標・キャリアプラン）は、社員の中長期的なキャリア目標と成長計画を管理するマスタテーブルです。

### 主な目的
- キャリア目標の設定・管理
- 成長計画の策定支援
- スキル開発ロードマップの提供
- 人事評価・昇進判定の基準設定
- 人材育成計画の立案支援

このテーブルにより、個人の成長と組織の人材戦略を連携させ、効果的なキャリア開発と人材育成を実現できます。

## カラム定義

| # | カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|---|----------|--------|----------|------|------|------------|------|
| 1 | id | ID | VARCHAR | 50 | NOT NULL | | 共通ID（主キー） |
| 2 | career_plan_id | キャリアプランID | VARCHAR | 50 | NOT NULL | | キャリアプランを一意に識別するID |
| 3 | employee_id | 社員ID | VARCHAR | 50 | NOT NULL | | 対象社員のID（MST_Employeeへの外部キー） |
| 4 | plan_name | プラン名 | VARCHAR | 200 | NOT NULL | | キャリアプランの名称 |
| 5 | plan_description | プラン説明 | TEXT | | NULL | | キャリアプランの詳細説明 |
| 6 | plan_type | プラン種別 | ENUM | | NOT NULL | | プランの種別（SHORT_TERM:短期、MEDIUM_TERM:中期、LONG_TERM:長期、SPECIALIZED:専門特化、MANAGEMENT:管理職、TECHNICAL:技術職） |
| 7 | target_position_id | 目標役職ID | VARCHAR | 50 | NULL | | 目標とする役職のID（MST_Positionへの外部キー） |
| 8 | target_job_type_id | 目標職種ID | VARCHAR | 50 | NULL | | 目標とする職種のID（MST_JobTypeへの外部キー） |
| 9 | target_department_id | 目標部署ID | VARCHAR | 50 | NULL | | 目標とする部署のID（MST_Departmentへの外部キー） |
| 10 | current_level | 現在レベル | ENUM | | NOT NULL | | 現在のキャリアレベル（ENTRY:新人、JUNIOR:初級、INTERMEDIATE:中級、SENIOR:上級、EXPERT:エキスパート、MANAGER:管理職、EXECUTIVE:役員） |
| 11 | target_level | 目標レベル | ENUM | | NOT NULL | | 目標とするキャリアレベル（ENTRY:新人、JUNIOR:初級、INTERMEDIATE:中級、SENIOR:上級、EXPERT:エキスパート、MANAGER:管理職、EXECUTIVE:役員） |
| 12 | plan_start_date | プラン開始日 | DATE | | NOT NULL | | キャリアプランの開始日 |
| 13 | plan_end_date | プラン終了日 | DATE | | NOT NULL | | キャリアプランの目標達成予定日 |
| 14 | milestone_1_date | マイルストーン1日付 | DATE | | NULL | | 第1マイルストーンの目標日 |
| 15 | milestone_1_description | マイルストーン1説明 | VARCHAR | 500 | NULL | | 第1マイルストーンの内容説明 |
| 16 | milestone_2_date | マイルストーン2日付 | DATE | | NULL | | 第2マイルストーンの目標日 |
| 17 | milestone_2_description | マイルストーン2説明 | VARCHAR | 500 | NULL | | 第2マイルストーンの内容説明 |
| 18 | milestone_3_date | マイルストーン3日付 | DATE | | NULL | | 第3マイルストーンの目標日 |
| 19 | milestone_3_description | マイルストーン3説明 | VARCHAR | 500 | NULL | | 第3マイルストーンの内容説明 |
| 20 | required_skills | 必要スキル | TEXT | | NULL | | 目標達成に必要なスキル一覧（JSON形式） |
| 21 | required_certifications | 必要資格 | TEXT | | NULL | | 目標達成に必要な資格一覧（JSON形式） |
| 22 | required_experiences | 必要経験 | TEXT | | NULL | | 目標達成に必要な経験・実績（JSON形式） |
| 23 | development_actions | 育成アクション | TEXT | | NULL | | 具体的な育成・開発アクション（JSON形式） |
| 24 | training_plan | 研修計画 | TEXT | | NULL | | 推奨研修・教育プログラム（JSON形式） |
| 25 | mentor_id | メンターID | VARCHAR | 50 | NULL | | 指導担当者のID（MST_Employeeへの外部キー） |
| 26 | supervisor_id | 上司ID | VARCHAR | 50 | NULL | | 直属上司のID（MST_Employeeへの外部キー） |
| 27 | plan_status | プラン状況 | ENUM | | NOT NULL | DRAFT | プランの進捗状況（DRAFT:下書き、ACTIVE:実行中、ON_HOLD:保留、COMPLETED:完了、CANCELLED:中止、REVISED:改訂） |
| 28 | progress_percentage | 進捗率 | DECIMAL | 5,2 | NOT NULL | 0.00 | プランの進捗率（0.00-100.00） |
| 29 | last_review_date | 最終レビュー日 | DATE | | NULL | | 最後にレビューを実施した日付 |
| 30 | next_review_date | 次回レビュー日 | DATE | | NULL | | 次回レビュー予定日 |
| 31 | review_frequency | レビュー頻度 | ENUM | | NOT NULL | QUARTERLY | レビューの実施頻度（MONTHLY:月次、QUARTERLY:四半期、SEMI_ANNUAL:半年、ANNUAL:年次） |
| 32 | success_criteria | 成功基準 | TEXT | | NULL | | プラン成功の判定基準 |
| 33 | risk_factors | リスク要因 | TEXT | | NULL | | 目標達成のリスク要因・課題 |
| 34 | support_resources | 支援リソース | TEXT | | NULL | | 利用可能な支援・リソース情報 |
| 35 | budget_allocated | 割当予算 | DECIMAL | 10,2 | NULL | | プラン実行のための割当予算 |
| 36 | budget_used | 使用予算 | DECIMAL | 10,2 | NOT NULL | 0.00 | 実際に使用した予算 |
| 37 | priority_level | 優先度 | ENUM | | NOT NULL | NORMAL | プランの優先度（LOW:低、NORMAL:通常、HIGH:高、CRITICAL:最重要） |
| 38 | visibility_level | 公開レベル | ENUM | | NOT NULL | MANAGER | プランの公開範囲（PRIVATE:本人のみ、MANAGER:上司まで、DEPARTMENT:部署内、COMPANY:全社） |
| 39 | template_id | テンプレートID | VARCHAR | 50 | NULL | | 使用したプランテンプレートのID |
| 40 | custom_fields | カスタムフィールド | TEXT | | NULL | | 組織固有の追加項目（JSON形式） |
| 41 | notes | 備考 | TEXT | | NULL | | その他の備考・メモ |
| 42 | created_at | 作成日時 | TIMESTAMP | | NOT NULL | CURRENT_TIMESTAMP | レコード作成日時 |
| 43 | updated_at | 更新日時 | TIMESTAMP | | NOT NULL | CURRENT_TIMESTAMP | レコード更新日時 |
| 44 | created_by | 作成者 | VARCHAR | 50 | NOT NULL | | レコード作成者 |
| 45 | updated_by | 更新者 | VARCHAR | 50 | NOT NULL | | レコード更新者 |
| 46 | version | バージョン | INTEGER | | NOT NULL | 1 | 楽観的排他制御用 |
| 47 | deleted_flag | 削除フラグ | BOOLEAN | | NOT NULL | FALSE | 論理削除フラグ |

## インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|---------------|------|--------|------|
| pk_mst_career_plan | PRIMARY KEY | id | 主キー |
| uk_career_plan_id | UNIQUE | career_plan_id | キャリアプランID一意制約 |
| idx_employee_id | INDEX | employee_id | 社員ID検索用 |
| idx_plan_type | INDEX | plan_type | プラン種別検索用 |
| idx_target_position | INDEX | target_position_id | 目標役職検索用 |
| idx_target_job_type | INDEX | target_job_type_id | 目標職種検索用 |
| idx_plan_status | INDEX | plan_status | プラン状況検索用 |
| idx_plan_period | INDEX | plan_start_date, plan_end_date | プラン期間検索用 |
| idx_review_date | INDEX | next_review_date | レビュー日検索用 |
| idx_mentor_id | INDEX | mentor_id | メンター検索用 |
| idx_supervisor_id | INDEX | supervisor_id | 上司検索用 |
| idx_priority_level | INDEX | priority_level | 優先度検索用 |

## 制約定義

| 制約名 | 種別 | 内容 | 説明 |
|--------|------|------|------|
| pk_mst_career_plan | PRIMARY KEY | id | 主キー制約 |
| uk_career_plan_id | UNIQUE | career_plan_id | キャリアプランID一意制約 |
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

## 外部キー定義

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|------------|--------|--------------|------------|--------|--------|------|
| fk_career_plan_employee | employee_id | MST_Employee | id | CASCADE | RESTRICT | 社員への外部キー |
| fk_career_plan_target_position | target_position_id | MST_Position | id | CASCADE | SET NULL | 目標役職への外部キー |
| fk_career_plan_target_job_type | target_job_type_id | MST_JobType | id | CASCADE | SET NULL | 目標職種への外部キー |
| fk_career_plan_target_department | target_department_id | MST_Department | id | CASCADE | SET NULL | 目標部署への外部キー |
| fk_career_plan_mentor | mentor_id | MST_Employee | id | CASCADE | SET NULL | メンターへの外部キー |
| fk_career_plan_supervisor | supervisor_id | MST_Employee | id | CASCADE | SET NULL | 上司への外部キー |

## サンプルデータ

| career_plan_id | employee_id | plan_name | plan_type | current_level | target_level | plan_status | progress_percentage |
|----------------|-------------|-----------|-----------|---------------|--------------|-------------|-------------------|
| CP_001 | EMP000001 | シニアエンジニアへの成長プラン | MEDIUM_TERM | INTERMEDIATE | SENIOR | ACTIVE | 25.50 |
| CP_002 | EMP000002 | プロジェクトマネージャーへの転身プラン | MANAGEMENT | SENIOR | MANAGER | ACTIVE | 60.00 |

## 業務ルール

1. キャリアプランIDは一意である必要がある
2. プラン開始日は終了日以前である必要がある
3. 進捗率は0-100%の範囲で設定
4. 使用予算は割当予算以下である必要がある
5. 目標レベルは現在レベル以上である必要がある
6. レビュー日は定期的に更新される必要がある
7. 完了したプランは変更不可
8. メンターと上司は異なる人物である必要がある

## 特記事項

- マイルストーンは最大3つまで設定可能
- JSON形式のフィールドは柔軟な拡張に対応
- 予算管理により投資対効果を測定
- メンター制度との連携で効果的な指導を実現
- レビュー頻度により継続的な改善を促進
- 公開レベルによりプライバシーと透明性を両立

## 改版履歴

| バージョン | 日付 | 作成者 | 変更内容 |
|------------|------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 目標・キャリアプランマスタの詳細定義 |
