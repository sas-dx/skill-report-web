# テーブル定義書：TRN_SkillRecord（スキル評価記録）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-010 |
| **テーブル名** | TRN_SkillRecord |
| **論理名** | スキル評価記録 |
| **カテゴリ** | トランザクション系 |
| **優先度** | 最高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-06-01 |
| **最終更新日** | 2025-06-01 |

## 2. テーブル概要

### 2.1 概要・目的
スキル評価記録テーブル（TRN_SkillRecord）は、社員のスキル評価情報を管理します。自己評価、上司評価、ピア評価など多様な評価方法に対応し、時系列でのスキル成長を追跡できます。評価根拠や証跡情報も保持し、客観的なスキル管理を実現します。

### 2.2 関連API
- [API-008](../../api/specs/API仕様書_API-008_スキル評価API.md) - スキル評価API

### 2.3 関連バッチ
- [BATCH-006](../../batch/specs/バッチ定義書_BATCH-006_スキル評価集計バッチ.md) - スキル評価集計バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | skill_record_id | スキル記録ID | VARCHAR | 20 | × | ○ | - | - | スキル評価記録を一意に識別するID |
| 2 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | テナントID |
| 3 | employee_id | 社員ID | VARCHAR | 20 | × | - | ○ | - | 評価対象の社員ID |
| 4 | skill_item_id | スキル項目ID | VARCHAR | 20 | × | - | ○ | - | 評価対象のスキル項目ID |
| 5 | skill_category_id | スキルカテゴリID | VARCHAR | 20 | × | - | ○ | - | スキルカテゴリID |
| 6 | evaluation_date | 評価日 | DATE | - | × | - | - | - | スキル評価を実施した日 |
| 7 | evaluation_period | 評価期間 | VARCHAR | 20 | × | - | - | - | 評価期間（YYYY-MM形式） |
| 8 | evaluation_type | 評価種別 | VARCHAR | 20 | × | - | - | 'SELF' | 評価の種別（SELF/MANAGER/PEER/EXPERT/CUSTOMER） |
| 9 | evaluator_id | 評価者ID | VARCHAR | 20 | × | - | ○ | - | 評価を実施した人のID |
| 10 | skill_level | スキルレベル | INTEGER | - | × | - | - | 1 | スキルレベル（1-5段階） |
| 11 | skill_grade_id | スキルグレードID | VARCHAR | 20 | ○ | - | ○ | NULL | 対応するスキルグレードID |
| 12 | proficiency_score | 習熟度スコア | DECIMAL | 5,2 | ○ | - | - | NULL | 習熟度スコア（0.00-100.00） |
| 13 | experience_years | 経験年数 | DECIMAL | 4,1 | ○ | - | - | NULL | 該当スキルの経験年数 |
| 14 | project_count | プロジェクト数 | INTEGER | - | ○ | - | - | NULL | 該当スキルを使用したプロジェクト数 |
| 15 | certification_count | 関連資格数 | INTEGER | - | ○ | - | - | 0 | 関連する取得資格数 |
| 16 | training_hours | 研修時間 | INTEGER | - | ○ | - | - | 0 | 関連する研修受講時間 |
| 17 | self_assessment | 自己評価 | INTEGER | - | ○ | - | - | NULL | 自己評価（1-5段階） |
| 18 | manager_assessment | 上司評価 | INTEGER | - | ○ | - | - | NULL | 上司評価（1-5段階） |
| 19 | peer_assessment | ピア評価 | INTEGER | - | ○ | - | - | NULL | 同僚評価（1-5段階） |
| 20 | customer_feedback | 顧客評価 | INTEGER | - | ○ | - | - | NULL | 顧客評価（1-5段階） |
| 21 | evaluation_comment | 評価コメント | TEXT | - | ○ | - | - | NULL | 評価に関するコメント |
| 22 | improvement_plan | 改善計画 | TEXT | - | ○ | - | - | NULL | スキル向上のための改善計画 |
| 23 | evidence_description | 証跡説明 | TEXT | - | ○ | - | - | NULL | 評価根拠となる証跡の説明 |
| 24 | evidence_files | 証跡ファイル | TEXT | - | ○ | - | - | NULL | 証跡ファイルのパス（JSON形式） |
| 25 | next_evaluation_date | 次回評価予定日 | DATE | - | ○ | - | - | NULL | 次回評価の予定日 |
| 26 | is_target_skill | 目標スキルフラグ | BOOLEAN | - | × | - | - | FALSE | 目標設定されたスキルかどうか |
| 27 | target_level | 目標レベル | INTEGER | - | ○ | - | - | NULL | 目標とするスキルレベル |
| 28 | target_date | 目標達成日 | DATE | - | ○ | - | - | NULL | 目標達成予定日 |
| 29 | achievement_date | 達成日 | DATE | - | ○ | - | - | NULL | 目標達成日 |
| 30 | status | ステータス | VARCHAR | 20 | × | - | - | 'ACTIVE' | 記録のステータス（ACTIVE/ARCHIVED/DELETED） |
| 31 | version | バージョン | INTEGER | - | × | - | - | 1 | 評価記録のバージョン |
| 32 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 33 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 34 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 35 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | skill_record_id | 主キー |
| idx_employee_skill | UNIQUE | employee_id, skill_item_id, evaluation_date, evaluation_type | 社員・スキル・評価日・評価種別の組み合わせ |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_employee | INDEX | employee_id | 社員検索用 |
| idx_skill_item | INDEX | skill_item_id | スキル項目検索用 |
| idx_skill_category | INDEX | skill_category_id | スキルカテゴリ検索用 |
| idx_evaluation_date | INDEX | evaluation_date | 評価日検索用 |
| idx_evaluation_period | INDEX | evaluation_period | 評価期間検索用 |
| idx_evaluation_type | INDEX | evaluation_type | 評価種別検索用 |
| idx_evaluator | INDEX | evaluator_id | 評価者検索用 |
| idx_skill_level | INDEX | skill_level | スキルレベル検索用 |
| idx_target_skill | INDEX | is_target_skill | 目標スキル検索用 |
| idx_status | INDEX | status | ステータス検索用 |
| idx_next_evaluation | INDEX | next_evaluation_date | 次回評価日検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_skill_record | PRIMARY KEY | skill_record_id | 主キー制約 |
| uq_employee_skill_eval | UNIQUE | employee_id, skill_item_id, evaluation_date, evaluation_type | 社員・スキル・評価日・評価種別の一意性 |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_employee | FOREIGN KEY | employee_id | MST_Employee.employee_id |
| fk_skill_item | FOREIGN KEY | skill_item_id | MST_SkillItem.skill_item_id |
| fk_skill_category | FOREIGN KEY | skill_category_id | MST_SkillCategory.skill_category_id |
| fk_skill_grade | FOREIGN KEY | skill_grade_id | MST_SkillGrade.grade_id |
| fk_evaluator | FOREIGN KEY | evaluator_id | MST_Employee.employee_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_evaluation_type | CHECK | evaluation_type | evaluation_type IN ('SELF', 'MANAGER', 'PEER', 'EXPERT', 'CUSTOMER') |
| chk_skill_level | CHECK | skill_level | skill_level >= 1 AND skill_level <= 5 |
| chk_proficiency_score | CHECK | proficiency_score | proficiency_score IS NULL OR (proficiency_score >= 0.00 AND proficiency_score <= 100.00) |
| chk_experience_years | CHECK | experience_years | experience_years IS NULL OR experience_years >= 0 |
| chk_project_count | CHECK | project_count | project_count IS NULL OR project_count >= 0 |
| chk_certification_count | CHECK | certification_count | certification_count >= 0 |
| chk_training_hours | CHECK | training_hours | training_hours >= 0 |
| chk_self_assessment | CHECK | self_assessment | self_assessment IS NULL OR (self_assessment >= 1 AND self_assessment <= 5) |
| chk_manager_assessment | CHECK | manager_assessment | manager_assessment IS NULL OR (manager_assessment >= 1 AND manager_assessment <= 5) |
| chk_peer_assessment | CHECK | peer_assessment | peer_assessment IS NULL OR (peer_assessment >= 1 AND peer_assessment <= 5) |
| chk_customer_feedback | CHECK | customer_feedback | customer_feedback IS NULL OR (customer_feedback >= 1 AND customer_feedback <= 5) |
| chk_target_level | CHECK | target_level | target_level IS NULL OR (target_level >= 1 AND target_level <= 5) |
| chk_status | CHECK | status | status IN ('ACTIVE', 'ARCHIVED', 'DELETED') |
| chk_version | CHECK | version | version >= 1 |
| chk_target_date | CHECK | target_date | target_date IS NULL OR target_date >= evaluation_date |
| chk_achievement_date | CHECK | achievement_date | achievement_date IS NULL OR achievement_date >= evaluation_date |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Tenant | tenant_id | 1:N | テナント情報 |
| MST_Employee | employee_id | 1:N | 評価対象社員 |
| MST_Employee | evaluator_id | 1:N | 評価者 |
| MST_SkillItem | skill_item_id | 1:N | スキル項目 |
| MST_SkillCategory | skill_category_id | 1:N | スキルカテゴリ |
| MST_SkillGrade | skill_grade_id | 1:N | スキルグレード |
| MST_UserAuth | created_by, updated_by | 1:N | 作成者・更新者 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| TRN_SkillEvidence | skill_record_id | 1:N | スキル証跡 |
| TRN_GoalProgress | skill_record_id | 1:N | 目標進捗 |

## 5. データ仕様

### 5.1 データ例
```sql
-- 自己評価記録
INSERT INTO TRN_SkillRecord (
    skill_record_id, tenant_id, employee_id, skill_item_id, skill_category_id,
    evaluation_date, evaluation_period, evaluation_type, evaluator_id,
    skill_level, proficiency_score, experience_years, project_count,
    self_assessment, evaluation_comment, is_target_skill, target_level, target_date,
    created_by, updated_by
) VALUES (
    'SKILL_REC_001', 'TENANT_001', 'EMP_001', 'SKILL_001', 'CAT_001',
    '2025-06-01', '2025-06', 'SELF', 'EMP_001',
    3, 75.50, 2.5, 5,
    3, 'Javaでの開発経験は2年半。基本的な機能実装は問題なくできるが、パフォーマンスチューニングなどの高度な技術はまだ学習中。',
    TRUE, 4, '2025-12-31',
    'user_001', 'user_001'
);

-- 上司評価記録
INSERT INTO TRN_SkillRecord (
    skill_record_id, tenant_id, employee_id, skill_item_id, skill_category_id,
    evaluation_date, evaluation_period, evaluation_type, evaluator_id,
    skill_level, manager_assessment, evaluation_comment, improvement_plan,
    next_evaluation_date, created_by, updated_by
) VALUES (
    'SKILL_REC_002', 'TENANT_001', 'EMP_001', 'SKILL_001', 'CAT_001',
    '2025-06-01', '2025-06', 'MANAGER', 'EMP_MGR_001',
    3, 3, 'コーディング品質は良好。設計力の向上が必要。',
    '設計パターンの学習とコードレビューへの積極的な参加を推奨。',
    '2025-09-01', 'user_mgr_001', 'user_mgr_001'
);

-- ピア評価記録
INSERT INTO TRN_SkillRecord (
    skill_record_id, tenant_id, employee_id, skill_item_id, skill_category_id,
    evaluation_date, evaluation_period, evaluation_type, evaluator_id,
    skill_level, peer_assessment, evaluation_comment,
    created_by, updated_by
) VALUES (
    'SKILL_REC_003', 'TENANT_001', 'EMP_001', 'SKILL_002', 'CAT_002',
    '2025-06-01', '2025-06', 'PEER', 'EMP_002',
    4, 4, 'チームワークが良く、技術的な相談にも親身に対応してくれる。',
    'user_002', 'user_002'
);

-- 目標達成記録
INSERT INTO TRN_SkillRecord (
    skill_record_id, tenant_id, employee_id, skill_item_id, skill_category_id,
    evaluation_date, evaluation_period, evaluation_type, evaluator_id,
    skill_level, self_assessment, is_target_skill, target_level, target_date, achievement_date,
    evaluation_comment, created_by, updated_by
) VALUES (
    'SKILL_REC_004', 'TENANT_001', 'EMP_003', 'SKILL_003', 'CAT_001',
    '2025-06-01', '2025-06', 'SELF', 'EMP_003',
    4, 4, TRUE, 4, '2025-06-30', '2025-06-01',
    'AWS認定資格を取得し、クラウドアーキテクチャの設計ができるようになった。',
    'user_003', 'user_003'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 0件 | 運用開始時 |
| 月間増加件数 | 5,000件 | 社員500名×スキル10項目×月1回評価 |
| 年間増加件数 | 60,000件 | 想定値 |
| 5年後想定件数 | 300,000件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：RANGE（evaluation_date）
- パーティション条件：月単位でパーティション分割

### 6.3 アーカイブ
- アーカイブ条件：評価日から3年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 最高 | employee_id, evaluation_period | 個人スキル評価取得 |
| SELECT | 高 | skill_item_id, evaluation_period | スキル別評価取得 |
| SELECT | 高 | tenant_id, evaluation_period | テナント内評価取得 |
| SELECT | 中 | evaluation_type, evaluation_date | 評価種別・期間検索 |
| INSERT | 高 | - | 新規評価記録登録 |
| UPDATE | 中 | skill_record_id | 評価記録更新 |

### 7.2 パフォーマンス要件
- SELECT：50ms以内
- INSERT：100ms以内
- UPDATE：100ms以内
- DELETE：100ms以内

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| tenant_admin | ○ | ○ | ○ | × | テナント管理者（自テナントのみ） |
| skill_admin | ○ | ○ | ○ | × | スキル管理者 |
| manager | ○ | ○ | ○ | × | 管理職（部下のみ） |
| employee | ○ | ○ | ○ | × | 一般社員（自分のみ） |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含む（評価情報）
- 機密情報：含む（人事評価）
- 暗号化：評価コメント、改善計画

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存スキル管理システム
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
CREATE TABLE TRN_SkillRecord (
    skill_record_id VARCHAR(20) NOT NULL COMMENT 'スキル記録ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    employee_id VARCHAR(20) NOT NULL COMMENT '社員ID',
    skill_item_id VARCHAR(20) NOT NULL COMMENT 'スキル項目ID',
    skill_category_id VARCHAR(20) NOT NULL COMMENT 'スキルカテゴリID',
    evaluation_date DATE NOT NULL COMMENT '評価日',
    evaluation_period VARCHAR(20) NOT NULL COMMENT '評価期間',
    evaluation_type VARCHAR(20) NOT NULL DEFAULT 'SELF' COMMENT '評価種別',
    evaluator_id VARCHAR(20) NOT NULL COMMENT '評価者ID',
    skill_level INTEGER NOT NULL DEFAULT 1 COMMENT 'スキルレベル',
    skill_grade_id VARCHAR(20) NULL COMMENT 'スキルグレードID',
    proficiency_score DECIMAL(5,2) NULL COMMENT '習熟度スコア',
    experience_years DECIMAL(4,1) NULL COMMENT '経験年数',
    project_count INTEGER NULL COMMENT 'プロジェクト数',
    certification_count INTEGER NOT NULL DEFAULT 0 COMMENT '関連資格数',
    training_hours INTEGER NOT NULL DEFAULT 0 COMMENT '研修時間',
    self_assessment INTEGER NULL COMMENT '自己評価',
    manager_assessment INTEGER NULL COMMENT '上司評価',
    peer_assessment INTEGER NULL COMMENT 'ピア評価',
    customer_feedback INTEGER NULL COMMENT '顧客評価',
    evaluation_comment TEXT NULL COMMENT '評価コメント',
    improvement_plan TEXT NULL COMMENT '改善計画',
    evidence_description TEXT NULL COMMENT '証跡説明',
    evidence_files TEXT NULL COMMENT '証跡ファイル',
    next_evaluation_date DATE NULL COMMENT '次回評価予定日',
    is_target_skill BOOLEAN NOT NULL DEFAULT FALSE COMMENT '目標スキルフラグ',
    target_level INTEGER NULL COMMENT '目標レベル',
    target_date DATE NULL COMMENT '目標達成日',
    achievement_date DATE NULL COMMENT '達成日',
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' COMMENT 'ステータス',
    version INTEGER NOT NULL DEFAULT 1 COMMENT 'バージョン',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT '作成者ID',
    updated_by VARCHAR(50) NOT NULL COMMENT '更新者ID',
    PRIMARY KEY (skill_record_id),
    UNIQUE KEY idx_employee_skill_eval (employee_id, skill_item_id, evaluation_date, evaluation_type),
    INDEX idx_tenant (tenant_id),
    INDEX idx_employee (employee_id),
    INDEX idx_skill_item (skill_item_id),
    INDEX idx_skill_category (skill_category_id),
    INDEX idx_evaluation_date (evaluation_date),
    INDEX idx_evaluation_period (evaluation_period),
    INDEX idx_evaluation_type (evaluation_type),
    INDEX idx_evaluator (evaluator_id),
    INDEX idx_skill_level (skill_level),
    INDEX idx_target_skill (is_target_skill),
    INDEX idx_status (status),
    INDEX idx_next_evaluation (next_evaluation_date),
    CONSTRAINT fk_skill_record_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_skill_record_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(employee_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_skill_record_skill_item FOREIGN KEY (skill_item_id) REFERENCES MST_SkillItem(skill_item_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_skill_record_skill_category FOREIGN KEY (skill_category_id) REFERENCES MST_SkillCategory(skill_category_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_skill_record_skill_grade FOREIGN KEY (skill_grade_id) REFERENCES MST_SkillGrade(grade_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_skill_record_evaluator FOREIGN KEY (evaluator_id) REFERENCES MST_Employee(employee_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_skill_record_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_skill_record_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_skill_record_evaluation_type CHECK (evaluation_type IN ('SELF', 'MANAGER', 'PEER', 'EXPERT', 'CUSTOMER')),
    CONSTRAINT chk_skill_record_skill_level CHECK (skill_level >= 1 AND skill_level <= 5),
    CONSTRAINT chk_skill_record_proficiency_score CHECK (proficiency_score IS NULL OR (proficiency_score >= 0.00 AND proficiency_score <= 100.00)),
    CONSTRAINT chk_skill_record_experience_years CHECK (experience_years IS NULL OR experience_years >= 0),
    CONSTRAINT chk_skill_record_project_count CHECK (project_count IS NULL OR project_count >= 0),
    CONSTRAINT chk_skill_record_certification_count CHECK (certification_count >= 0),
    CONSTRAINT chk_skill_record_training_hours CHECK (training_hours >= 0),
    CONSTRAINT chk_skill_record_self_assessment CHECK (self_assessment IS NULL OR (self_assessment >= 1 AND self_assessment <= 5)),
    CONSTRAINT chk_skill_record_manager_assessment CHECK (manager_assessment IS NULL OR (manager_assessment >= 1 AND manager_assessment <= 5)),
    CONSTRAINT chk_skill_record_peer_assessment CHECK (peer_assessment IS NULL OR (peer_assessment >= 1 AND peer_assessment <= 5)),
    CONSTRAINT chk_skill_record_customer_feedback CHECK (customer_feedback IS NULL OR (customer_feedback >= 1 AND customer_feedback <= 5)),
    CONSTRAINT chk_skill_record_target_level CHECK (target_level IS NULL OR (target_level >= 1 AND target_level <= 5)),
    CONSTRAINT chk_skill_record_status CHECK (status IN ('ACTIVE', 'ARCHIVED', 'DELETED')),
    CONSTRAINT chk_skill_record_version CHECK (version >= 1),
    CONSTRAINT chk_skill_record_target_date CHECK (target_date IS NULL OR target_date >= evaluation_date),
    CONSTRAINT chk_skill_record_achievement_date CHECK (achievement_date IS NULL OR achievement_date >= evaluation_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='スキル評価記録'
PARTITION BY RANGE (YEAR(evaluation_date) * 100 + MONTH(evaluation_date)) (
    PARTITION p202501 VALUES LESS THAN (202502),
    PARTITION p202502 VALUES LESS THAN (202503),
    PARTITION p202503 VALUES LESS THAN (202504),
    PARTITION p202504 VALUES LESS THAN (202505),
    PARTITION p202505 VALUES LESS THAN (202506),
    PARTITION p202506 VALUES LESS THAN (202507),
    PARTITION p202507 VALUES LESS THAN (202508),
    PARTITION p202508 VALUES LESS THAN (202509),
    PARTITION p202509 VALUES LESS THAN (202510),
    PARTITION p202510 VALUES LESS THAN (202511),
    PARTITION p202511 VALUES LESS THAN (202512),
    PARTITION p202512 VALUES LESS THAN (202601),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

## 10. 特記事項

1. **多面的評価システム**
   - 自己評価、上司評価、ピア評価、専門家評価、顧客評価に対応
   - 360度評価による客観的なスキル評価を実現

2. **時系列スキル管理**
   - 評価期間による時系列でのスキル成長追跡
   - バージョン管理による評価履歴の保持

3. **目標管理連携**
   - 目標スキル設定と達成状況の管理
   - 目標レベルと達成日の追跡

4. **証跡管理**
   - 評価根拠となる証跡の説明と添付ファイル管理
   - 客観的な
