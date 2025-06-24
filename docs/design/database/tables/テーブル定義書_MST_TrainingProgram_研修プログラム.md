# テーブル定義書: MST_TrainingProgram

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_TrainingProgram |
| 論理名 | 研修プログラム |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-24 23:02:18 |

## 概要

MST_TrainingProgram（研修プログラム）は、組織で提供される研修・教育プログラムの詳細情報を管理するマスタテーブルです。
主な目的：
- 研修プログラムの体系的管理
- 研修内容・カリキュラムの標準化
- スキル開発との連携
- 研修効果の測定・評価
- 人材育成計画の支援
このテーブルにより、効果的な研修体系を構築し、
組織全体のスキル向上と人材育成を促進できます。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| active_flag | 有効フラグ | BOOLEAN |  | ○ | True | 有効フラグ |
| approval_date | 承認日 | DATE |  | ○ |  | 承認日 |
| approved_by | 承認者 | VARCHAR | 50 | ○ |  | 承認者 |
| assessment_method | 評価方法 | ENUM |  | ○ |  | 評価方法 |
| certification_provided | 認定証発行 | BOOLEAN |  | ○ | False | 認定証発行 |
| cost_per_participant | 参加者単価 | DECIMAL | 10,2 | ○ |  | 参加者単価 |
| created_by | 作成者 | VARCHAR | 50 | ○ |  | 作成者 |
| curriculum_details | カリキュラム詳細 | TEXT |  | ○ |  | カリキュラム詳細 |
| curriculum_outline | カリキュラム概要 | TEXT |  | ○ |  | カリキュラム概要 |
| difficulty_level | 難易度 | ENUM |  | ○ |  | 難易度 |
| duration_days | 研修日数 | INTEGER |  | ○ |  | 研修日数 |
| duration_hours | 研修時間 | DECIMAL | 5,2 | ○ |  | 研修時間 |
| effective_end_date | 有効終了日 | DATE |  | ○ |  | 有効終了日 |
| effective_start_date | 有効開始日 | DATE |  | ○ |  | 有効開始日 |
| equipment_required | 必要機材 | TEXT |  | ○ |  | 必要機材 |
| external_provider | 外部提供者 | VARCHAR | 200 | ○ |  | 外部提供者 |
| external_url | 外部URL | VARCHAR | 500 | ○ |  | 外部URL |
| instructor_requirements | 講師要件 | TEXT |  | ○ |  | 講師要件 |
| language | 実施言語 | ENUM |  | ○ | JA | 実施言語 |
| learning_objectives | 学習目標 | TEXT |  | ○ |  | 学習目標 |
| mandatory_flag | 必須研修フラグ | BOOLEAN |  | ○ | False | 必須研修フラグ |
| materials_required | 必要教材 | TEXT |  | ○ |  | 必要教材 |
| max_participants | 最大参加者数 | INTEGER |  | ○ |  | 最大参加者数 |
| min_participants | 最小参加者数 | INTEGER |  | ○ |  | 最小参加者数 |
| passing_score | 合格点 | DECIMAL | 5,2 | ○ |  | 合格点 |
| pdu_credits | PDUクレジット | DECIMAL | 5,2 | ○ |  | PDUクレジット |
| prerequisites | 前提条件 | TEXT |  | ○ |  | 前提条件 |
| program_category | プログラムカテゴリ | ENUM |  | ○ |  | プログラムカテゴリ |
| program_code | プログラムコード | VARCHAR | 20 | ○ |  | プログラムコード |
| program_description | プログラム説明 | TEXT |  | ○ |  | プログラム説明 |
| program_name | プログラム名 | VARCHAR | 200 | ○ |  | プログラム名 |
| program_name_en | プログラム名 | VARCHAR | 200 | ○ |  | プログラム名（英語） |
| program_type | プログラム種別 | ENUM |  | ○ |  | プログラム種別 |
| related_certifications | 関連資格 | TEXT |  | ○ |  | 関連資格 |
| related_skills | 関連スキル | TEXT |  | ○ |  | 関連スキル |
| repeat_interval | 再受講間隔 | INTEGER |  | ○ |  | 再受講間隔 |
| revision_notes | 改訂メモ | TEXT |  | ○ |  | 改訂メモ |
| tags | タグ | TEXT |  | ○ |  | タグ |
| target_audience | 対象者 | ENUM |  | ○ |  | 対象者 |
| training_program_id | 研修プログラムID | VARCHAR | 50 | ○ |  | 研修プログラムID |
| trainingprogram_id | MST_TrainingProgramの主キー | SERIAL |  | × |  | MST_TrainingProgramの主キー |
| venue_requirements | 会場要件 | TEXT |  | ○ |  | 会場要件 |
| venue_type | 会場種別 | ENUM |  | ○ |  | 会場種別 |
| version_number | バージョン番号 | VARCHAR | 10 | ○ | 1.0 | バージョン番号 |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_training_program_id | training_program_id | ○ |  |
| idx_program_code | program_code | ○ |  |
| idx_program_category | program_category | × |  |
| idx_program_type | program_type | × |  |
| idx_target_audience | target_audience | × |  |
| idx_difficulty_level | difficulty_level | × |  |
| idx_active_flag | active_flag | × |  |
| idx_mandatory_flag | mandatory_flag | × |  |
| idx_effective_period | effective_start_date, effective_end_date | × |  |
| idx_external_provider | external_provider | × |  |
| idx_language | language | × |  |
| idx_mst_trainingprogram_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_training_program_created_by | created_by | MST_Employee | id | CASCADE | RESTRICT | 外部キー制約 |
| fk_training_program_approved_by | approved_by | MST_Employee | id | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| uk_program_code | UNIQUE |  | program_code一意制約 |
| uk_training_program_id | UNIQUE |  | training_program_id一意制約 |
| chk_program_type | CHECK | program_type IN (...) | program_type値チェック制約 |
| chk_venue_type | CHECK | venue_type IN (...) | venue_type値チェック制約 |

## サンプルデータ

| training_program_id | program_code | program_name | program_name_en | program_description | program_category | program_type | target_audience | difficulty_level | duration_hours | duration_days | max_participants | min_participants | prerequisites | learning_objectives | curriculum_outline | curriculum_details | materials_required | equipment_required | instructor_requirements | assessment_method | passing_score | certification_provided | pdu_credits | related_skills | related_certifications | cost_per_participant | external_provider | external_url | venue_type | venue_requirements | language | repeat_interval | mandatory_flag | active_flag | effective_start_date | effective_end_date | created_by | approved_by | approval_date | version_number | revision_notes | tags |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| TRN_PROG_001 | PM-BASIC-001 | プロジェクトマネジメント基礎研修 | Project Management Fundamentals | プロジェクトマネジメントの基本概念と手法を学ぶ研修 | MANAGEMENT | CLASSROOM | MIDDLE | INTERMEDIATE | 16.0 | 2 | 20 | 8 | 実務経験2年以上、基本的なビジネススキル | PMBOKの基本概念理解、プロジェクト計画立案、リスク管理手法の習得 | 1日目：PM概論、計画立案　2日目：実行・監視、リスク管理 | {"day1": ["PM概論", "プロジェクト憲章", "WBS作成"], "day2": ["進捗管理", "リスク分析", "ケーススタディ"]} | ["テキスト", "演習用PC", "プロジェクト計画テンプレート"] | ["プロジェクター", "ホワイトボード", "PC環境"] | PMP資格保有、実務経験5年以上 | COMPREHENSIVE | 70.0 | True | 16.0 | ["プロジェクト管理", "リーダーシップ", "コミュニケーション"] | ["PMP", "プロジェクトマネージャ試験"] | 50000.0 | None | None | INTERNAL | 20名収容可能な研修室、プロジェクター設備 | JA | 24 | False | True | 2024-01-01 | None | EMP000010 | EMP000005 | 2023-12-15 | 1.0 | 初版作成 | ["プロジェクト管理", "PMBOK", "リーダーシップ", "中級"] |
| TRN_PROG_002 | AWS-ARCH-001 | AWS認定ソリューションアーキテクト対策研修 | AWS Certified Solutions Architect Preparation | AWS認定ソリューションアーキテクト資格取得のための対策研修 | TECHNICAL | BLENDED | SENIOR | ADVANCED | 24.0 | 3 | 15 | 5 | AWS基礎知識、クラウド実務経験1年以上 | AWSサービス理解、アーキテクチャ設計、試験合格 | 1日目：AWS基礎　2日目：アーキテクチャ設計　3日目：模擬試験・解説 | {"day1": ["EC2", "S3", "VPC"], "day2": ["高可用性設計", "セキュリティ", "コスト最適化"], "day3": ["模擬試験", "解説", "試験対策"]} | ["AWS公式テキスト", "模擬試験問題集", "ハンズオン環境"] | ["AWS環境", "PC", "インターネット接続"] | AWS認定資格保有、実務経験3年以上 | TEST | 80.0 | True | 24.0 | ["AWS", "クラウドアーキテクチャ", "インフラ設計"] | ["AWS認定ソリューションアーキテクト"] | 80000.0 | AWSトレーニングパートナー | https://aws.amazon.com/training/ | HYBRID | PC環境、AWS環境アクセス可能 | JA | 12 | False | True | 2024-02-01 | None | EMP000015 | EMP000008 | 2024-01-20 | 1.1 | ハンズオン内容を強化 | ["AWS", "クラウド", "認定資格", "アーキテクチャ", "上級"] |

## 特記事項

- カリキュラム詳細はJSON形式で柔軟に管理
- 外部研修との連携により多様な学習機会を提供
- PDUクレジットにより継続教育を支援
- バージョン管理により研修内容の改善を追跡
- タグ機能により柔軟な検索・分類が可能
- 多言語対応によりグローバル展開に対応
- 研修プログラムIDとプログラムコードは一意である必要がある
- 研修時間と日数は正数である必要がある
- 最小参加者数は最大参加者数以下である必要がある
- 有効開始日は有効終了日以前である必要がある
- 合格点は0-100の範囲で設定
- 必須研修は有効期間内である必要がある
- 外部研修の場合は提供者情報が必要
- 承認済みプログラムのみ実施可能

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 研修プログラムマスタの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214907 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215000 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215053 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223432 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |