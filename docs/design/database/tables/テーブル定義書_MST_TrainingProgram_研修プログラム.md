# テーブル定義書：MST_TrainingProgram（研修プログラム）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-040 |
| **テーブル名** | MST_TrainingProgram |
| **論理名** | 研修プログラム |
| **カテゴリ** | マスタ系 |
| **優先度** | 中 |
| **ステータス** | 運用中 |
| **作成日** | 2025-06-01 |
| **最終更新日** | 2025-06-01 |

## 2. テーブル概要

### 2.1 概要・目的
研修プログラムマスタテーブル（MST_TrainingProgram）は、社内外で実施される研修プログラムの情報を管理します。技術研修、ビジネススキル研修、資格取得支援研修など、様々な研修プログラムを体系的に管理し、社員のスキル向上とキャリア開発を支援します。

### 2.2 関連API
- [API-040](../../api/specs/API仕様書_API-040_研修プログラム管理API.md) - 研修プログラム管理API

### 2.3 関連バッチ
- [BATCH-036](../../batch/specs/バッチ定義書_BATCH-036_研修プログラム同期バッチ.md) - 研修プログラム同期バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | training_program_id | 研修プログラムID | VARCHAR | 20 | × | ○ | - | - | 研修プログラムを一意に識別するID |
| 2 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | テナントID |
| 3 | program_code | プログラムコード | VARCHAR | 50 | × | - | - | - | 研修プログラムの一意コード |
| 4 | program_name | プログラム名 | VARCHAR | 200 | × | - | - | - | 研修プログラムの名称 |
| 5 | program_name_en | プログラム名（英語） | VARCHAR | 200 | ○ | - | - | NULL | 研修プログラムの英語名称 |
| 6 | program_description | プログラム説明 | TEXT | - | ○ | - | - | NULL | 研修プログラムの詳細説明 |
| 7 | program_category | プログラムカテゴリ | VARCHAR | 50 | × | - | - | 'TECHNICAL' | 研修の分類（TECHNICAL/BUSINESS/SOFT/CERTIFICATION/COMPLIANCE等） |
| 8 | program_type | プログラム種別 | VARCHAR | 30 | × | - | - | 'INTERNAL' | 研修の種別（INTERNAL/EXTERNAL/ONLINE/BLENDED） |
| 9 | skill_category_id | スキルカテゴリID | VARCHAR | 20 | ○ | - | ○ | NULL | 関連するスキルカテゴリID |
| 10 | target_skill_items | 対象スキル項目 | TEXT | - | ○ | - | - | NULL | 習得対象スキル項目（JSON形式） |
| 11 | prerequisite_skills | 前提スキル | TEXT | - | ○ | - | - | NULL | 受講に必要な前提スキル（JSON形式） |
| 12 | target_audience | 対象者 | VARCHAR | 100 | ○ | - | - | NULL | 研修対象者（新入社員、中堅社員、管理職等） |
| 13 | target_job_types | 対象職種 | TEXT | - | ○ | - | - | NULL | 対象職種（JSON形式） |
| 14 | target_skill_levels | 対象スキルレベル | TEXT | - | ○ | - | - | NULL | 対象スキルレベル（JSON形式） |
| 15 | difficulty_level | 難易度レベル | INTEGER | - | ○ | - | - | 3 | 研修の難易度（1:易、5:難） |
| 16 | duration_hours | 研修時間 | INTEGER | - | ○ | - | - | NULL | 研修の総時間数 |
| 17 | duration_days | 研修日数 | INTEGER | - | ○ | - | - | NULL | 研修の総日数 |
| 18 | max_participants | 最大参加者数 | INTEGER | - | ○ | - | - | NULL | 1回あたりの最大参加者数 |
| 19 | min_participants | 最小参加者数 | INTEGER | - | ○ | - | - | NULL | 開催に必要な最小参加者数 |
| 20 | instructor_type | 講師種別 | VARCHAR | 30 | ○ | - | - | 'INTERNAL' | 講師の種別（INTERNAL/EXTERNAL/VENDOR） |
| 21 | instructor_info | 講師情報 | TEXT | - | ○ | - | - | NULL | 講師の詳細情報（JSON形式） |
| 22 | training_provider | 研修提供者 | VARCHAR | 200 | ○ | - | - | NULL | 研修提供機関・会社 |
| 23 | training_location | 研修場所 | VARCHAR | 200 | ○ | - | - | NULL | 研修実施場所 |
| 24 | online_platform | オンラインプラットフォーム | VARCHAR | 100 | ○ | - | - | NULL | オンライン研修のプラットフォーム |
| 25 | materials_required | 必要教材 | TEXT | - | ○ | - | - | NULL | 必要な教材・資料（JSON形式） |
| 26 | equipment_required | 必要機材 | TEXT | - | ○ | - | - | NULL | 必要な機材・設備（JSON形式） |
| 27 | cost_per_person | 1人あたり費用 | DECIMAL | 10,2 | ○ | - | - | NULL | 1人あたりの研修費用 |
| 28 | total_budget | 総予算 | DECIMAL | 12,2 | ○ | - | - | NULL | 研修の総予算 |
| 29 | currency | 通貨 | VARCHAR | 3 | ○ | - | - | 'JPY' | 費用の通貨単位 |
| 30 | certification_available | 認定証発行 | BOOLEAN | - | × | - | - | FALSE | 修了認定証の発行有無 |
| 31 | certification_criteria | 認定基準 | TEXT | - | ○ | - | - | NULL | 認定証発行の基準（JSON形式） |
| 32 | pdu_points | PDUポイント | INTEGER | - | ○ | - | - | NULL | 取得可能なPDUポイント |
| 33 | external_certification | 外部資格連携 | VARCHAR | 200 | ○ | - | - | NULL | 連携する外部資格名 |
| 34 | evaluation_method | 評価方法 | TEXT | - | ○ | - | - | NULL | 研修効果の評価方法（JSON形式） |
| 35 | feedback_required | フィードバック必須 | BOOLEAN | - | × | - | - | TRUE | 受講後フィードバックの必須性 |
| 36 | recurring_schedule | 定期開催スケジュール | TEXT | - | ○ | - | - | NULL | 定期開催のスケジュール（JSON形式） |
| 37 | enrollment_start_date | 申込開始日 | DATE | - | ○ | - | - | NULL | 申込受付開始日 |
| 38 | enrollment_end_date | 申込終了日 | DATE | - | ○ | - | - | NULL | 申込受付終了日 |
| 39 | program_start_date | プログラム開始日 | DATE | - | ○ | - | - | NULL | 研修プログラム開始日 |
| 40 | program_end_date | プログラム終了日 | DATE | - | ○ | - | - | NULL | 研修プログラム終了日 |
| 41 | registration_url | 申込URL | VARCHAR | 500 | ○ | - | - | NULL | 外部申込サイトのURL |
| 42 | program_url | プログラムURL | VARCHAR | 500 | ○ | - | - | NULL | 研修プログラムの詳細URL |
| 43 | syllabus_url | シラバスURL | VARCHAR | 500 | ○ | - | - | NULL | シラバス・カリキュラムのURL |
| 44 | tags | タグ | TEXT | - | ○ | - | - | NULL | 検索・分類用タグ（JSON形式） |
| 45 | popularity_score | 人気度スコア | INTEGER | - | ○ | - | - | 0 | 研修の人気度スコア |
| 46 | effectiveness_score | 効果度スコア | DECIMAL | 3,2 | ○ | - | - | NULL | 研修効果の評価スコア |
| 47 | approval_required | 承認必須 | BOOLEAN | - | × | - | - | FALSE | 受講に上司承認が必要かどうか |
| 48 | approval_workflow | 承認ワークフロー | TEXT | - | ○ | - | - | NULL | 承認ワークフローの定義（JSON形式） |
| 49 | is_mandatory | 必須研修フラグ | BOOLEAN | - | × | - | - | FALSE | 必須研修かどうか |
| 50 | mandatory_for | 必須対象者 | TEXT | - | ○ | - | - | NULL | 必須研修の対象者（JSON形式） |
| 51 | display_order | 表示順序 | INTEGER | - | × | - | - | 0 | 研修一覧での表示順序 |
| 52 | is_featured | 注目研修フラグ | BOOLEAN | - | × | - | - | FALSE | 注目すべき研修かどうか |
| 53 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | 研修プログラムが有効かどうか |
| 54 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 55 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 56 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 57 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | training_program_id | 主キー |
| uq_program_code | UNIQUE | tenant_id, program_code | テナント内でのプログラムコード一意性 |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_program_category | INDEX | program_category | プログラムカテゴリ検索用 |
| idx_program_type | INDEX | program_type | プログラム種別検索用 |
| idx_skill_category | INDEX | skill_category_id | スキルカテゴリ検索用 |
| idx_target_audience | INDEX | target_audience | 対象者検索用 |
| idx_difficulty | INDEX | difficulty_level | 難易度検索用 |
| idx_instructor_type | INDEX | instructor_type | 講師種別検索用 |
| idx_training_provider | INDEX | training_provider | 研修提供者検索用 |
| idx_certification | INDEX | certification_available | 認定証発行検索用 |
| idx_enrollment_dates | INDEX | enrollment_start_date, enrollment_end_date | 申込期間検索用 |
| idx_program_dates | INDEX | program_start_date, program_end_date | 研修期間検索用 |
| idx_mandatory | INDEX | is_mandatory | 必須研修検索用 |
| idx_featured | INDEX | is_featured | 注目研修検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |
| idx_display_order | INDEX | program_category, display_order | 表示順序検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_training_program | PRIMARY KEY | training_program_id | 主キー制約 |
| uq_program_code | UNIQUE | tenant_id, program_code | テナント内でのプログラムコード一意性 |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_skill_category | FOREIGN KEY | skill_category_id | MST_SkillCategory.skill_category_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_program_category | CHECK | program_category | program_category IN ('TECHNICAL', 'BUSINESS', 'SOFT', 'CERTIFICATION', 'COMPLIANCE', 'LEADERSHIP', 'SAFETY') |
| chk_program_type | CHECK | program_type | program_type IN ('INTERNAL', 'EXTERNAL', 'ONLINE', 'BLENDED', 'SELF_PACED', 'WORKSHOP') |
| chk_difficulty_level | CHECK | difficulty_level | difficulty_level IS NULL OR (difficulty_level >= 1 AND difficulty_level <= 5) |
| chk_duration_hours | CHECK | duration_hours | duration_hours IS NULL OR duration_hours > 0 |
| chk_duration_days | CHECK | duration_days | duration_days IS NULL OR duration_days > 0 |
| chk_max_participants | CHECK | max_participants | max_participants IS NULL OR max_participants > 0 |
| chk_min_participants | CHECK | min_participants | min_participants IS NULL OR min_participants > 0 |
| chk_participant_logic | CHECK | max_participants, min_participants | (max_participants IS NULL OR min_participants IS NULL) OR (max_participants >= min_participants) |
| chk_instructor_type | CHECK | instructor_type | instructor_type IS NULL OR instructor_type IN ('INTERNAL', 'EXTERNAL', 'VENDOR', 'FREELANCE') |
| chk_cost_per_person | CHECK | cost_per_person | cost_per_person IS NULL OR cost_per_person >= 0 |
| chk_total_budget | CHECK | total_budget | total_budget IS NULL OR total_budget >= 0 |
| chk_currency | CHECK | currency | currency IS NULL OR currency IN ('JPY', 'USD', 'EUR', 'GBP', 'CNY') |
| chk_pdu_points | CHECK | pdu_points | pdu_points IS NULL OR pdu_points >= 0 |
| chk_popularity_score | CHECK | popularity_score | popularity_score >= 0 |
| chk_effectiveness_score | CHECK | effectiveness_score | effectiveness_score IS NULL OR (effectiveness_score >= 0 AND effectiveness_score <= 5) |
| chk_display_order | CHECK | display_order | display_order >= 0 |
| chk_enrollment_dates | CHECK | enrollment_start_date, enrollment_end_date | (enrollment_start_date IS NULL OR enrollment_end_date IS NULL) OR (enrollment_start_date <= enrollment_end_date) |
| chk_program_dates | CHECK | program_start_date, program_end_date | (program_start_date IS NULL OR program_end_date IS NULL) OR (program_start_date <= program_end_date) |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Tenant | tenant_id | 1:N | テナント情報 |
| MST_SkillCategory | skill_category_id | 1:N | スキルカテゴリ |
| MST_UserAuth | created_by, updated_by | 1:N | 作成者・更新者 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| TRN_TrainingHistory | training_program_id | 1:N | 研修参加履歴 |

## 5. データ仕様

### 5.1 データ例
```sql
-- 技術研修プログラム
INSERT INTO MST_TrainingProgram (
    training_program_id, tenant_id, program_code, program_name, program_name_en,
    program_description, program_category, program_type, skill_category_id,
    target_skill_items, target_audience, difficulty_level, duration_hours, duration_days,
    max_participants, min_participants, instructor_type, training_provider,
    cost_per_person, certification_available, pdu_points, is_featured,
    created_by, updated_by
) VALUES (
    'TRAIN_PROG_001', 'TENANT_001', 'JAVA_BASIC', 'Java基礎研修', 'Java Basic Training',
    'Javaプログラミングの基礎から実践まで学ぶ研修プログラム。オブジェクト指向プログラミングの概念を習得。',
    'TECHNICAL', 'INTERNAL', 'CAT_PROGRAMMING',
    '["SKILL_JAVA", "SKILL_OOP", "SKILL_ECLIPSE"]', '新入社員', 2, 40, 5,
    20, 5, 'INTERNAL', '株式会社テックアカデミー',
    150000.00, TRUE, 40, TRUE,
    'user_admin', 'user_admin'
);

-- ビジネススキル研修
INSERT INTO MST_TrainingProgram (
    training_program_id, tenant_id, program_code, program_name, program_name_en,
    program_description, program_category, program_type, target_audience,
    difficulty_level, duration_hours, duration_days, max_participants, min_participants,
    instructor_type, training_location, cost_per_person, certification_available,
    approval_required, is_mandatory, mandatory_for, created_by, updated_by
) VALUES (
    'TRAIN_PROG_002', 'TENANT_001', 'PROJECT_MGMT', 'プロジェクト管理研修', 'Project Management Training',
    'プロジェクト管理の基礎知識とPMBOKに基づく実践的なスキルを習得する研修。',
    'BUSINESS', 'EXTERNAL', '中堅社員', 3, 24, 3,
    15, 8, 'EXTERNAL', '東京研修センター',
    200000.00, TRUE, TRUE, FALSE, NULL,
    'user_admin', 'user_admin'
);

-- オンライン研修
INSERT INTO MST_TrainingProgram (
    training_program_id, tenant_id, program_code, program_name, program_name_en,
    program_description, program_category, program_type, target_audience,
    difficulty_level, duration_hours, max_participants, instructor_type,
    online_platform, program_url, cost_per_person, certification_available,
    pdu_points, recurring_schedule, created_by, updated_by
) VALUES (
    'TRAIN_PROG_003', 'TENANT_001', 'AWS_CLOUD', 'AWS クラウド基礎', 'AWS Cloud Fundamentals',
    'Amazon Web Servicesの基礎知識とクラウドアーキテクチャを学ぶオンライン研修。',
    'TECHNICAL', 'ONLINE', '全社員', 2, 16,
    100, 'EXTERNAL', 'AWS Training Portal',
    'https://aws.amazon.com/training/', 80000.00, TRUE,
    16, '{"frequency": "monthly", "day_of_month": 15}',
    'user_admin', 'user_admin'
);

-- 必須コンプライアンス研修
INSERT INTO MST_TrainingProgram (
    training_program_id, tenant_id, program_code, program_name, program_name_en,
    program_description, program_category, program_type, target_audience,
    difficulty_level, duration_hours, instructor_type, training_location,
    cost_per_person, certification_available, is_mandatory, mandatory_for,
    approval_required, feedback_required, created_by, updated_by
) VALUES (
    'TRAIN_PROG_004', 'TENANT_001', 'COMPLIANCE_2025', '2025年度コンプライアンス研修', '2025 Compliance Training',
    '法令遵守、情報セキュリティ、ハラスメント防止に関する必須研修。',
    'COMPLIANCE', 'INTERNAL', '全社員', 1, 4,
    'INTERNAL', '本社会議室', 0.00, TRUE,
    TRUE, '["全社員"]', FALSE, TRUE,
    'user_admin', 'user_admin'
);

-- 資格取得支援研修
INSERT INTO MST_TrainingProgram (
    training_program_id, tenant_id, program_code, program_name, program_name_en,
    program_description, program_category, program_type, skill_category_id,
    target_skill_items, target_audience, difficulty_level, duration_hours, duration_days,
    max_participants, instructor_type, training_provider, cost_per_person,
    certification_available, external_certification, pdu_points,
    approval_required, created_by, updated_by
) VALUES (
    'TRAIN_PROG_005', 'TENANT_001', 'PMP_PREP', 'PMP試験対策講座', 'PMP Exam Preparation',
    'Project Management Professional (PMP)資格取得のための試験対策講座。',
    'CERTIFICATION', 'EXTERNAL', 'CAT_PROJECT_MGMT',
    '["SKILL_PROJECT_MGMT", "SKILL_PMBOK"]', '管理職', 4, 35, 7,
    12, 'EXTERNAL', 'PMI認定教育機関', 300000.00,
    FALSE, 'PMP', 35, TRUE,
    'user_admin', 'user_admin'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 50件 | 基本的な研修プログラム |
| 月間増加件数 | 5件 | 新規研修プログラムの追加 |
| 年間増加件数 | 60件 | 想定値 |
| 5年後想定件数 | 350件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：なし
- パーティション条件：-

### 6.3 アーカイブ
- アーカイブ条件：終了から3年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | program_category, is_active | カテゴリ別研修一覧取得 |
| SELECT | 高 | target_audience, is_active | 対象者別研修検索 |
| SELECT | 中 | enrollment_start_date, enrollment_end_date | 申込期間検索 |
| SELECT | 中 | is_mandatory | 必須研修取得 |
| SELECT | 中 | is_featured | 注目研修取得 |
| INSERT | 低 | - | 新規研修プログラム登録 |
| UPDATE | 低 | training_program_id | 研修プログラム情報更新 |

### 7.2 パフォーマンス要件
- SELECT：30ms以内
- INSERT：100ms以内
- UPDATE：100ms以内
- DELETE：100ms以内

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| tenant_admin | ○ | ○ | ○ | × | テナント管理者（自テナントのみ） |
| training_admin | ○ | ○ | ○ | × | 研修管理者 |
| hr_admin | ○ | ○ | ○ | × | 人事管理者 |
| manager | ○ | × | × | × | 管理職（参照のみ） |
| employee | ○ | × | × | × | 一般社員（参照のみ） |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含まない
- 機密情報：含む（費用情報）
- 暗号化：費用関連情報

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存研修管理システム
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
CREATE TABLE MST_TrainingProgram (
    training_program_id VARCHAR(20) NOT NULL COMMENT '研修プログラムID',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    program_code VARCHAR(50) NOT NULL COMMENT 'プログラムコード',
    program_name VARCHAR(200) NOT NULL COMMENT 'プログラム名',
    program_name_en VARCHAR(200) NULL COMMENT 'プログラム名（英語）',
    program_description TEXT NULL COMMENT 'プログラム説明',
    program_category VARCHAR(50) NOT NULL DEFAULT 'TECHNICAL' COMMENT 'プログラムカテゴリ',
    program_type VARCHAR(30) NOT NULL DEFAULT 'INTERNAL' COMMENT 'プログラム種別',
    skill_category_id VARCHAR(20) NULL COMMENT 'スキルカテゴリID',
    target_skill_items TEXT NULL COMMENT '対象スキル項目',
    prerequisite_skills TEXT NULL COMMENT '前提スキル',
    target_audience VARCHAR(100) NULL COMMENT '対象者',
    target_job_types TEXT NULL COMMENT '対象職種',
    target_skill_levels TEXT NULL COMMENT '対象スキルレベル',
    difficulty_level INTEGER NULL DEFAULT 3 COMMENT '難易度レベル',
    duration_hours INTEGER NULL COMMENT '研修時間',
    duration_days INTEGER NULL COMMENT '研修日数',
    max_participants INTEGER NULL COMMENT '最大参加者数',
    min_participants INTEGER NULL COMMENT '最小参加者数',
    instructor_type VARCHAR(30) NULL DEFAULT 'INTERNAL' COMMENT '講師種別',
    instructor_info TEXT NULL COMMENT '講師情報',
    training_provider VARCHAR(200) NULL COMMENT '研修提供者',
    training_location VARCHAR(200) NULL COMMENT '研修場所',
    online_platform VARCHAR(100) NULL COMMENT 'オンラインプラットフォーム',
    materials_required TEXT NULL COMMENT '必要教材',
    equipment_required TEXT NULL COMMENT '必要機材',
    cost_per_person DECIMAL(10,2) NULL COMMENT '1人あたり費用',
    total_budget DECIMAL(12,2) NULL COMMENT '総予算',
    currency VARCHAR(3) NULL DEFAULT 'JPY' COMMENT '通貨',
    certification_available BOOLEAN NOT NULL DEFAULT FALSE COMMENT '認定証発行',
    certification_criteria TEXT NULL COMMENT '認定基準',
    pdu_points INTEGER NULL COMMENT 'PDUポイント',
    external_certification VARCHAR(200) NULL COMMENT '外部資格連携',
    evaluation_method TEXT NULL COMMENT '評価方法',
    feedback_required BOOLEAN NOT NULL DEFAULT TRUE COMMENT 'フィードバック必須',
    recurring_schedule TEXT NULL COMMENT '定期開催スケジュール',
    enrollment_start_date DATE NULL COMMENT '申込開始日',
    enrollment_end_date DATE NULL COMMENT '申込終了日',
    program_start_date DATE NULL COMMENT 'プログラム開始日',
    program_end_date DATE NULL COMMENT 'プログラム終了日',
    registration_url VARCHAR(500) NULL COMMENT '申込URL',
    program_url VARCHAR(500) NULL COMMENT 'プログラムURL',
    syllabus_url VARCHAR(500) NULL COMMENT 'シラバスURL',
    tags TEXT NULL COMMENT 'タグ',
    popularity_score INTEGER NULL DEFAULT 0 COMMENT '人気度スコア',
    effectiveness_score DECIMAL(3,2) NULL COMMENT '効果度スコア',
    approval_required BOOLEAN NOT NULL DEFAULT FALSE COMMENT '承認必須',
    approval_workflow TEXT NULL COMMENT '承認ワークフロー',
    is_mandatory BOOLEAN NOT NULL DEFAULT FALSE COMMENT '必須研修フラグ',
    mandatory_for TEXT NULL COMMENT '必須対象者',
    display_order INTEGER NOT NULL DEFAULT 0 COMMENT '表示順序',
    is_featured BOOLEAN NOT NULL DEFAULT FALSE COMMENT '注目研修フラグ',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '有効フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT '作成者ID',
    updated_by VARCHAR(50) NOT NULL COMMENT '更新者ID',
    PRIMARY KEY (training_program_id),
    UNIQUE KEY uq_program_code (tenant_id, program_code),
    INDEX idx_tenant (tenant_id),
    INDEX idx_program_category (program_category),
    INDEX idx_program_type (program_type),
    INDEX idx_skill_category (skill_category_id),
    INDEX idx_target_audience (target_audience),
    INDEX idx_difficulty (difficulty_level),
    INDEX idx_instructor_type (instructor_type),
    INDEX idx_training_provider (training_provider),
    INDEX idx_certification (certification_available),
    INDEX idx_enrollment_dates (enrollment_start_date, enrollment_end_date),
    INDEX idx_program_dates (program_start_date, program_end_date),
    INDEX idx_mandatory (is_mandatory),
    INDEX idx_featured (is_featured),
    INDEX idx_active (is_active),
    INDEX idx_display_order (program_category, display_order),
    CONSTRAINT fk_training_program_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_training_program_skill_category FOREIGN KEY (skill_category_id) REFERENCES MST_SkillCategory(skill_category_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_training_program_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_training_program_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_training_program_category CHECK (program_category IN ('TECHNICAL', 'BUSINESS', 'SOFT', 'CERTIFICATION', 'COMPLIANCE', 'LEADERSHIP', 'SAFETY')),
    CONSTRAINT chk_training_program_type CHECK (program_type IN ('INTERNAL', 'EXTERNAL', 'ONLINE', 'BLENDED', 'SELF_PACED', 'WORKSHOP')),
    CONSTRAINT chk_training_program_difficulty CHECK (difficulty_level IS NULL OR (difficulty_level >= 1 AND difficulty_level <= 5)),
    CONSTRAINT chk_training_program_duration_hours CHECK (duration_hours IS NULL OR duration_hours > 0),
    CONSTRAINT chk_training_program_duration_days CHECK (duration_days IS NULL OR duration_days > 0),
    CONSTRAINT chk_training_program_max_participants CHECK (max_participants IS NULL OR max_participants > 0),
    CONSTRAINT chk_training_program_min_participants CHECK (min_participants IS NULL OR min_participants > 0),
    CONSTRAINT chk_training_program_participant_logic CHECK ((max_participants IS NULL OR min_participants IS NULL) OR (max_participants >= min_participants)),
    CONSTRAINT chk_training_program_instructor_type CHECK (instructor_type IS NULL OR instructor_type IN ('INTERNAL', 'EXTERNAL', 'VENDOR', 'FREELANCE')),
    CONSTRAINT chk_training_program_cost_per_person CHECK (cost_per_person IS NULL OR cost_per_person >= 0),
    CONSTRAINT chk_training_program_total_budget CHECK (total_budget IS NULL OR total_budget >= 0),
    CONSTRAINT chk_training_program_currency CHECK (currency IS NULL OR currency IN ('JPY', 'USD', 'EUR', 'GBP', 'CNY')),
    CONSTRAINT chk_training_program_pdu_points CHECK (pdu_points IS NULL OR pdu_points >= 0),
    CONSTRAINT chk_training_program_popularity_score CHECK (popularity_score >= 0),
    CONSTRAINT chk_training_program_effectiveness_score CHECK (effectiveness_score IS NULL OR (effectiveness_score >= 0 AND effectiveness_score <= 5)),
    CONSTRAINT chk_training_program_display_order CHECK (display_order >= 0),
    CONSTRAINT chk_training_program_enrollment_dates CHECK ((enrollment_start_date IS NULL OR enrollment_end_date IS NULL) OR (enrollment_start_date <= enrollment_end_date)),
    CONSTRAINT chk_training_program_program_dates CHECK ((program_start_date IS NULL OR program_end_date IS NULL) OR (program_start_date <= program_end_date))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='研修プログラム';
```

## 10. 特記事項

1. **多様な研修形態対応**
   - 社内研修、外部研修、オンライン研修、ブレンド型研修
   - 自己学習型、ワークショップ型など多様な形態をサポート

2. **スキル連携機能**
   - スキルカテゴリとの連携による体系的な研修管理
   - 対象スキル項目、前提スキルの明確化

3. **承認ワークフロー**
   - 研修受講の承認プロセス管理
   - 上司承認、予算承認などの柔軟なワークフロー

4. **費用管理機能**
   - 1人あたり費用、総予算の管理
   - 多通貨対応による国際的な研修管理

5. **効果測定機能**
   - 研修効果の評価方法定義
   - 人気度スコア、効果度スコアによる研修品質管理

6. **定期開催対応**
   - 定期開催スケジュールの管理
   - 継続的な研修プログラムの効率的な運用
