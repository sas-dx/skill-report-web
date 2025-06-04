# テーブル定義書: MST_TrainingProgram

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_TrainingProgram |
| 論理名 | 研修プログラム |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-04 06:57:02 |

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
| training_program_id | 研修プログラムID | VARCHAR | 50 | ○ |  | 研修プログラムを一意に識別するID |
| program_code | プログラムコード | VARCHAR | 20 | ○ |  | 研修プログラムの識別コード |
| program_name | プログラム名 | VARCHAR | 200 | ○ |  | 研修プログラムの名称 |
| program_name_en | プログラム名（英語） | VARCHAR | 200 | ○ |  | 研修プログラムの英語名称 |
| program_description | プログラム説明 | TEXT |  | ○ |  | 研修プログラムの詳細説明 |
| program_category | プログラムカテゴリ | ENUM |  | ○ |  | 研修の分類（TECHNICAL:技術、BUSINESS:ビジネス、MANAGEMENT:管理、COMPLIANCE:コンプライアンス、SOFT_SKILL:ソフトスキル、CERTIFICATION:資格、ORIENTATION:新人研修） |
| program_type | プログラム種別 | ENUM |  | ○ |  | 研修の実施形態（CLASSROOM:集合研修、ONLINE:オンライン、BLENDED:ブレンド、OJT:OJT、SELF_STUDY:自習、EXTERNAL:外部研修） |
| target_audience | 対象者 | ENUM |  | ○ |  | 研修の対象者（ALL:全社員、NEW_HIRE:新入社員、JUNIOR:若手、MIDDLE:中堅、SENIOR:シニア、MANAGER:管理職、EXECUTIVE:役員、SPECIALIST:専門職） |
| difficulty_level | 難易度 | ENUM |  | ○ |  | 研修の難易度（BEGINNER:初級、INTERMEDIATE:中級、ADVANCED:上級、EXPERT:エキスパート） |
| duration_hours | 研修時間 | DECIMAL | 5,2 | ○ |  | 研修の総時間数 |
| duration_days | 研修日数 | INTEGER |  | ○ |  | 研修の実施日数 |
| max_participants | 最大参加者数 | INTEGER |  | ○ |  | 1回の研修での最大参加者数 |
| min_participants | 最小参加者数 | INTEGER |  | ○ |  | 開催に必要な最小参加者数 |
| prerequisites | 前提条件 | TEXT |  | ○ |  | 受講に必要な前提知識・条件 |
| learning_objectives | 学習目標 | TEXT |  | ○ |  | 研修の学習目標・到達目標 |
| curriculum_outline | カリキュラム概要 | TEXT |  | ○ |  | 研修のカリキュラム・内容概要 |
| curriculum_details | カリキュラム詳細 | TEXT |  | ○ |  | 詳細なカリキュラム内容（JSON形式） |
| materials_required | 必要教材 | TEXT |  | ○ |  | 研修に必要な教材・資料（JSON形式） |
| equipment_required | 必要機材 | TEXT |  | ○ |  | 研修に必要な機材・設備（JSON形式） |
| instructor_requirements | 講師要件 | TEXT |  | ○ |  | 講師に求められる要件・資格 |
| assessment_method | 評価方法 | ENUM |  | ○ |  | 研修の評価方法（NONE:なし、TEST:テスト、ASSIGNMENT:課題、PRESENTATION:発表、PRACTICAL:実技、COMPREHENSIVE:総合評価） |
| passing_score | 合格点 | DECIMAL | 5,2 | ○ |  | 研修合格に必要な点数 |
| certification_provided | 認定証発行 | BOOLEAN |  | ○ | False | 修了時に認定証を発行するかどうか |
| pdu_credits | PDUクレジット | DECIMAL | 5,2 | ○ |  | 取得可能なPDUクレジット数 |
| related_skills | 関連スキル | TEXT |  | ○ |  | 研修で習得・向上するスキル（JSON形式） |
| related_certifications | 関連資格 | TEXT |  | ○ |  | 研修に関連する資格（JSON形式） |
| cost_per_participant | 参加者単価 | DECIMAL | 10,2 | ○ |  | 参加者1人あたりの研修費用 |
| external_provider | 外部提供者 | VARCHAR | 200 | ○ |  | 外部研修の場合の提供会社・機関名 |
| external_url | 外部URL | VARCHAR | 500 | ○ |  | 外部研修の詳細情報URL |
| venue_type | 会場種別 | ENUM |  | ○ |  | 研修会場の種別（INTERNAL:社内、EXTERNAL:社外、ONLINE:オンライン、HYBRID:ハイブリッド） |
| venue_requirements | 会場要件 | TEXT |  | ○ |  | 研修会場に必要な設備・条件 |
| language | 実施言語 | ENUM |  | ○ | JA | 研修の実施言語（JA:日本語、EN:英語、BILINGUAL:バイリンガル） |
| repeat_interval | 再受講間隔 | INTEGER |  | ○ |  | 再受講可能な間隔（月数） |
| mandatory_flag | 必須研修フラグ | BOOLEAN |  | ○ | False | 必須研修かどうか |
| active_flag | 有効フラグ | BOOLEAN |  | ○ | True | 現在提供中の研修かどうか |
| effective_start_date | 有効開始日 | DATE |  | ○ |  | 研修プログラムの提供開始日 |
| effective_end_date | 有効終了日 | DATE |  | ○ |  | 研修プログラムの提供終了日 |
| created_by | 作成者 | VARCHAR | 50 | ○ |  | プログラムを作成した担当者ID |
| approved_by | 承認者 | VARCHAR | 50 | ○ |  | プログラムを承認した責任者ID |
| approval_date | 承認日 | DATE |  | ○ |  | プログラムが承認された日付 |
| version_number | バージョン番号 | VARCHAR | 10 | ○ | 1.0 | プログラムのバージョン番号 |
| revision_notes | 改訂メモ | TEXT |  | ○ |  | バージョン改訂時のメモ・変更内容 |
| tags | タグ | TEXT |  | ○ |  | 検索・分類用のタグ（JSON形式） |
| code | コード | VARCHAR | 20 | × |  | マスタコード |
| name | 名称 | VARCHAR | 100 | × |  | マスタ名称 |
| description | 説明 | TEXT |  | ○ |  | マスタ説明 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_training_program_id | training_program_id | ○ | 研修プログラムID検索用（一意） |
| idx_program_code | program_code | ○ | プログラムコード検索用（一意） |
| idx_program_category | program_category | × | プログラムカテゴリ検索用 |
| idx_program_type | program_type | × | プログラム種別検索用 |
| idx_target_audience | target_audience | × | 対象者検索用 |
| idx_difficulty_level | difficulty_level | × | 難易度検索用 |
| idx_active_flag | active_flag | × | 有効フラグ検索用 |
| idx_mandatory_flag | mandatory_flag | × | 必須研修フラグ検索用 |
| idx_effective_period | effective_start_date, effective_end_date | × | 有効期間検索用 |
| idx_external_provider | external_provider | × | 外部提供者検索用 |
| idx_language | language | × | 実施言語検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_training_program_created_by | created_by | MST_Employee | id | CASCADE | RESTRICT | 作成者への外部キー |
| fk_training_program_approved_by | approved_by | MST_Employee | id | CASCADE | SET NULL | 承認者への外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_training_program_id | UNIQUE |  | 研修プログラムID一意制約 |
| uk_program_code | UNIQUE |  | プログラムコード一意制約 |
| chk_program_category | CHECK | program_category IN ('TECHNICAL', 'BUSINESS', 'MANAGEMENT', 'COMPLIANCE', 'SOFT_SKILL', 'CERTIFICATION', 'ORIENTATION') | プログラムカテゴリ値チェック制約 |
| chk_program_type | CHECK | program_type IN ('CLASSROOM', 'ONLINE', 'BLENDED', 'OJT', 'SELF_STUDY', 'EXTERNAL') | プログラム種別値チェック制約 |
| chk_target_audience | CHECK | target_audience IN ('ALL', 'NEW_HIRE', 'JUNIOR', 'MIDDLE', 'SENIOR', 'MANAGER', 'EXECUTIVE', 'SPECIALIST') | 対象者値チェック制約 |
| chk_difficulty_level | CHECK | difficulty_level IN ('BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT') | 難易度値チェック制約 |
| chk_assessment_method | CHECK | assessment_method IN ('NONE', 'TEST', 'ASSIGNMENT', 'PRESENTATION', 'PRACTICAL', 'COMPREHENSIVE') | 評価方法値チェック制約 |
| chk_venue_type | CHECK | venue_type IN ('INTERNAL', 'EXTERNAL', 'ONLINE', 'HYBRID') | 会場種別値チェック制約 |
| chk_language | CHECK | language IN ('JA', 'EN', 'BILINGUAL') | 実施言語値チェック制約 |
| chk_duration_positive | CHECK | duration_hours > 0 AND duration_days > 0 | 研修時間・日数正数チェック制約 |
| chk_participants_range | CHECK | min_participants IS NULL OR max_participants IS NULL OR min_participants <= max_participants | 参加者数範囲チェック制約 |
| chk_effective_period | CHECK | effective_end_date IS NULL OR effective_start_date <= effective_end_date | 有効期間整合性チェック制約 |
| chk_passing_score_range | CHECK | passing_score IS NULL OR (passing_score >= 0 AND passing_score <= 100) | 合格点範囲チェック制約 |

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

## 業務ルール

- 研修プログラムIDとプログラムコードは一意である必要がある
- 研修時間と日数は正数である必要がある
- 最小参加者数は最大参加者数以下である必要がある
- 有効開始日は有効終了日以前である必要がある
- 合格点は0-100の範囲で設定
- 必須研修は有効期間内である必要がある
- 外部研修の場合は提供者情報が必要
- 承認済みプログラムのみ実施可能

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 研修プログラムマスタの詳細定義 |
