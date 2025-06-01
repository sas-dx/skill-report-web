# テーブル定義書_MST_TrainingProgram_研修プログラム

## 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_TrainingProgram |
| 論理名 | 研修プログラム |
| カテゴリ | マスタ系 |
| 作成日 | 2025-06-01 |
| 作成者 | 開発チーム |
| バージョン | 1.0.0 |

## テーブル概要

MST_TrainingProgram（研修プログラム）は、組織で提供される研修・教育プログラムの詳細情報を管理するマスタテーブルです。

### 主な目的
- 研修プログラムの体系的管理
- 研修内容・カリキュラムの標準化
- スキル開発との連携
- 研修効果の測定・評価
- 人材育成計画の支援

このテーブルにより、効果的な研修体系を構築し、組織全体のスキル向上と人材育成を促進できます。

## カラム定義

| # | カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|---|----------|--------|----------|------|------|------------|------|
| 1 | id | ID | VARCHAR | 50 | NOT NULL | | 共通ID（主キー） |
| 2 | training_program_id | 研修プログラムID | VARCHAR | 50 | NOT NULL | | 研修プログラムを一意に識別するID |
| 3 | program_code | プログラムコード | VARCHAR | 20 | NOT NULL | | 研修プログラムの識別コード |
| 4 | program_name | プログラム名 | VARCHAR | 200 | NOT NULL | | 研修プログラムの名称 |
| 5 | program_name_en | プログラム名（英語） | VARCHAR | 200 | NULL | | 研修プログラムの英語名称 |
| 6 | program_description | プログラム説明 | TEXT | | NULL | | 研修プログラムの詳細説明 |
| 7 | program_category | プログラムカテゴリ | ENUM | | NOT NULL | | 研修の分類（TECHNICAL:技術、BUSINESS:ビジネス、MANAGEMENT:管理、COMPLIANCE:コンプライアンス、SOFT_SKILL:ソフトスキル、CERTIFICATION:資格、ORIENTATION:新人研修） |
| 8 | program_type | プログラム種別 | ENUM | | NOT NULL | | 研修の実施形態（CLASSROOM:集合研修、ONLINE:オンライン、BLENDED:ブレンド、OJT:OJT、SELF_STUDY:自習、EXTERNAL:外部研修） |
| 9 | target_audience | 対象者 | ENUM | | NOT NULL | | 研修の対象者（ALL:全社員、NEW_HIRE:新入社員、JUNIOR:若手、MIDDLE:中堅、SENIOR:シニア、MANAGER:管理職、EXECUTIVE:役員、SPECIALIST:専門職） |
| 10 | difficulty_level | 難易度 | ENUM | | NOT NULL | | 研修の難易度（BEGINNER:初級、INTERMEDIATE:中級、ADVANCED:上級、EXPERT:エキスパート） |
| 11 | duration_hours | 研修時間 | DECIMAL | 5,2 | NOT NULL | | 研修の総時間数 |
| 12 | duration_days | 研修日数 | INTEGER | | NOT NULL | | 研修の実施日数 |
| 13 | max_participants | 最大参加者数 | INTEGER | | NULL | | 1回の研修での最大参加者数 |
| 14 | min_participants | 最小参加者数 | INTEGER | | NULL | | 開催に必要な最小参加者数 |
| 15 | prerequisites | 前提条件 | TEXT | | NULL | | 受講に必要な前提知識・条件 |
| 16 | learning_objectives | 学習目標 | TEXT | | NOT NULL | | 研修の学習目標・到達目標 |
| 17 | curriculum_outline | カリキュラム概要 | TEXT | | NULL | | 研修のカリキュラム・内容概要 |
| 18 | curriculum_details | カリキュラム詳細 | TEXT | | NULL | | 詳細なカリキュラム内容（JSON形式） |
| 19 | materials_required | 必要教材 | TEXT | | NULL | | 研修に必要な教材・資料（JSON形式） |
| 20 | equipment_required | 必要機材 | TEXT | | NULL | | 研修に必要な機材・設備（JSON形式） |
| 21 | instructor_requirements | 講師要件 | TEXT | | NULL | | 講師に求められる要件・資格 |
| 22 | assessment_method | 評価方法 | ENUM | | NOT NULL | | 研修の評価方法（NONE:なし、TEST:テスト、ASSIGNMENT:課題、PRESENTATION:発表、PRACTICAL:実技、COMPREHENSIVE:総合評価） |
| 23 | passing_score | 合格点 | DECIMAL | 5,2 | NULL | | 研修合格に必要な点数 |
| 24 | certification_provided | 認定証発行 | BOOLEAN | | NOT NULL | FALSE | 修了時に認定証を発行するかどうか |
| 25 | pdu_credits | PDUクレジット | DECIMAL | 5,2 | NULL | | 取得可能なPDUクレジット数 |
| 26 | related_skills | 関連スキル | TEXT | | NULL | | 研修で習得・向上するスキル（JSON形式） |
| 27 | related_certifications | 関連資格 | TEXT | | NULL | | 研修に関連する資格（JSON形式） |
| 28 | cost_per_participant | 参加者単価 | DECIMAL | 10,2 | NULL | | 参加者1人あたりの研修費用 |
| 29 | external_provider | 外部提供者 | VARCHAR | 200 | NULL | | 外部研修の場合の提供会社・機関名 |
| 30 | external_url | 外部URL | VARCHAR | 500 | NULL | | 外部研修の詳細情報URL |
| 31 | venue_type | 会場種別 | ENUM | | NOT NULL | | 研修会場の種別（INTERNAL:社内、EXTERNAL:社外、ONLINE:オンライン、HYBRID:ハイブリッド） |
| 32 | venue_requirements | 会場要件 | TEXT | | NULL | | 研修会場に必要な設備・条件 |
| 33 | language | 実施言語 | ENUM | | NOT NULL | JA | 研修の実施言語（JA:日本語、EN:英語、BILINGUAL:バイリンガル） |
| 34 | repeat_interval | 再受講間隔 | INTEGER | | NULL | | 再受講可能な間隔（月数） |
| 35 | mandatory_flag | 必須研修フラグ | BOOLEAN | | NOT NULL | FALSE | 必須研修かどうか |
| 36 | active_flag | 有効フラグ | BOOLEAN | | NOT NULL | TRUE | 現在提供中の研修かどうか |
| 37 | effective_start_date | 有効開始日 | DATE | | NOT NULL | | 研修プログラムの提供開始日 |
| 38 | effective_end_date | 有効終了日 | DATE | | NULL | | 研修プログラムの提供終了日 |
| 39 | created_by | 作成者 | VARCHAR | 50 | NOT NULL | | プログラムを作成した担当者ID |
| 40 | approved_by | 承認者 | VARCHAR | 50 | NULL | | プログラムを承認した責任者ID |
| 41 | approval_date | 承認日 | DATE | | NULL | | プログラムが承認された日付 |
| 42 | version_number | バージョン番号 | VARCHAR | 10 | NOT NULL | 1.0 | プログラムのバージョン番号 |
| 43 | revision_notes | 改訂メモ | TEXT | | NULL | | バージョン改訂時のメモ・変更内容 |
| 44 | tags | タグ | TEXT | | NULL | | 検索・分類用のタグ（JSON形式） |
| 45 | created_at | 作成日時 | TIMESTAMP | | NOT NULL | CURRENT_TIMESTAMP | レコード作成日時 |
| 46 | updated_at | 更新日時 | TIMESTAMP | | NOT NULL | CURRENT_TIMESTAMP | レコード更新日時 |
| 47 | updated_by | 更新者 | VARCHAR | 50 | NOT NULL | | レコード更新者 |
| 48 | version | バージョン | INTEGER | | NOT NULL | 1 | 楽観的排他制御用 |
| 49 | deleted_flag | 削除フラグ | BOOLEAN | | NOT NULL | FALSE | 論理削除フラグ |

## インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|---------------|------|--------|------|
| pk_mst_training_program | PRIMARY KEY | id | 主キー |
| uk_training_program_id | UNIQUE | training_program_id | 研修プログラムID一意制約 |
| uk_program_code | UNIQUE | program_code | プログラムコード一意制約 |
| idx_program_category | INDEX | program_category | プログラムカテゴリ検索用 |
| idx_program_type | INDEX | program_type | プログラム種別検索用 |
| idx_target_audience | INDEX | target_audience | 対象者検索用 |
| idx_difficulty_level | INDEX | difficulty_level | 難易度検索用 |
| idx_active_flag | INDEX | active_flag | 有効フラグ検索用 |
| idx_mandatory_flag | INDEX | mandatory_flag | 必須研修フラグ検索用 |
| idx_effective_period | INDEX | effective_start_date, effective_end_date | 有効期間検索用 |
| idx_external_provider | INDEX | external_provider | 外部提供者検索用 |
| idx_language | INDEX | language | 実施言語検索用 |

## 制約定義

| 制約名 | 種別 | 内容 | 説明 |
|--------|------|------|------|
| pk_mst_training_program | PRIMARY KEY | id | 主キー制約 |
| uk_training_program_id | UNIQUE | training_program_id | 研修プログラムID一意制約 |
| uk_program_code | UNIQUE | program_code | プログラムコード一意制約 |
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

## 外部キー定義

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|------------|--------|--------------|------------|--------|--------|------|
| fk_training_program_created_by | created_by | MST_Employee | id | CASCADE | RESTRICT | 作成者への外部キー |
| fk_training_program_approved_by | approved_by | MST_Employee | id | CASCADE | SET NULL | 承認者への外部キー |

## サンプルデータ

| training_program_id | program_code | program_name | program_category | program_type | target_audience | difficulty_level |
|-------------------|--------------|--------------|------------------|--------------|-----------------|------------------|
| TRN_PROG_001 | PM-BASIC-001 | プロジェクトマネジメント基礎研修 | MANAGEMENT | CLASSROOM | MIDDLE | INTERMEDIATE |
| TRN_PROG_002 | AWS-ARCH-001 | AWS認定ソリューションアーキテクト対策研修 | TECHNICAL | BLENDED | SENIOR | ADVANCED |

## 業務ルール

1. 研修プログラムIDとプログラムコードは一意である必要がある
2. 研修時間と日数は正数である必要がある
3. 最小参加者数は最大参加者数以下である必要がある
4. 有効開始日は有効終了日以前である必要がある
5. 合格点は0-100の範囲で設定
6. 必須研修は有効期間内である必要がある
7. 外部研修の場合は提供者情報が必要
8. 承認済みプログラムのみ実施可能

## 特記事項

- カリキュラム詳細はJSON形式で柔軟に管理
- 外部研修との連携により多様な学習機会を提供
- PDUクレジットにより継続教育を支援
- バージョン管理により研修内容の改善を追跡
- タグ機能により柔軟な検索・分類が可能
- 多言語対応によりグローバル展開に対応

## 改版履歴

| バージョン | 日付 | 作成者 | 変更内容 |
|------------|------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 研修プログラムマスタの詳細定義 |
