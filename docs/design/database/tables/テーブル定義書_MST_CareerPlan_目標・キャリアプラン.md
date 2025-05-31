# テーブル定義書：目標・キャリアプラン (MST_CareerPlan)

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-013 |
| **テーブル名** | MST_CareerPlan |
| **論理名** | 目標・キャリアプラン |
| **カテゴリ** | マスタ系 |
| **優先度** | 中 |
| **ステータス** | 運用中 |
| **作成日** | 2025-05-31 |
| **最終更新日** | 2025-05-31 |

## 2. テーブル概要

### 2.1 概要・目的
目標・キャリアプランテーブル（MST_CareerPlan）は、社員のキャリア目標と成長計画を管理するマスタテーブルです。短期・中期・長期の目標設定、目標達成に必要なスキル、目標とする役職・ポジション、メンター情報などを記録します。このテーブルは社員のキャリア開発と人材育成の基盤となり、定期的な目標設定と評価のサイクルをサポートします。

### 2.2 関連API
- [API-012](../api/specs/API仕様書_API-012.md) - キャリアプラン管理API

### 2.3 関連バッチ
- [BATCH-008](../batch/specs/バッチ定義書_BATCH-008.md) - 目標進捗更新バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | career_plan_id | キャリアプランID | VARCHAR | 50 | × | ○ | - | - | キャリアプランを一意に識別するID |
| 2 | employee_id | 社員ID | VARCHAR | 20 | × | - | ○ | - | 社員を一意に識別するID |
| 3 | plan_year | 計画年度 | INTEGER | 4 | × | - | - | - | キャリアプランの年度 |
| 4 | short_term_goal | 短期目標 | TEXT | - | × | - | - | - | 1年以内の短期目標 |
| 5 | mid_term_goal | 中期目標 | TEXT | - | × | - | - | - | 1〜3年の中期目標 |
| 6 | long_term_goal | 長期目標 | TEXT | - | ○ | - | - | NULL | 3〜5年の長期目標 |
| 7 | target_position_id | 目標役職ID | VARCHAR | 20 | ○ | - | ○ | NULL | 目標とする役職ID |
| 8 | target_dept_id | 目標部署ID | VARCHAR | 20 | ○ | - | ○ | NULL | 目標とする部署ID |
| 9 | required_skill_id1 | 必要スキルID1 | VARCHAR | 50 | ○ | - | ○ | NULL | 目標達成に必要なスキル1 |
| 10 | required_skill_id2 | 必要スキルID2 | VARCHAR | 50 | ○ | - | ○ | NULL | 目標達成に必要なスキル2 |
| 11 | required_skill_id3 | 必要スキルID3 | VARCHAR | 50 | ○ | - | ○ | NULL | 目標達成に必要なスキル3 |
| 12 | required_cert_id | 必要資格ID | VARCHAR | 50 | ○ | - | ○ | NULL | 目標達成に必要な資格ID |
| 13 | required_training_id | 必要研修ID | VARCHAR | 50 | ○ | - | ○ | NULL | 目標達成に必要な研修ID |
| 14 | mentor_id | メンターID | VARCHAR | 20 | ○ | - | ○ | NULL | メンター社員のID |
| 15 | self_assessment | 自己評価 | TEXT | - | ○ | - | - | NULL | 目標に対する自己評価 |
| 16 | manager_assessment | 上長評価 | TEXT | - | ○ | - | - | NULL | 目標に対する上長評価 |
| 17 | manager_confirmed | 上長確認フラグ | BOOLEAN | - | × | - | - | FALSE | 上長による確認が完了したかどうか |
| 18 | manager_confirmed_at | 上長確認日時 | TIMESTAMP | - | ○ | - | - | NULL | 上長による確認日時 |
| 19 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | 所属テナントのID |
| 20 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | キャリアプランが有効かどうか |
| 21 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 22 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 23 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 24 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | career_plan_id | 主キー |
| idx_employee | INDEX | employee_id | 社員による検索用 |
| idx_plan_year | INDEX | plan_year | 年度による検索用 |
| idx_target_position | INDEX | target_position_id | 目標役職による検索用 |
| idx_target_dept | INDEX | target_dept_id | 目標部署による検索用 |
| idx_mentor | INDEX | mentor_id | メンターによる検索用 |
| idx_confirmed | INDEX | manager_confirmed | 上長確認状況による検索用 |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_active | INDEX | is_active | 有効フラグによる検索用 |
| uk_employee_year | UNIQUE | employee_id, plan_year | 社員・年度の組み合わせの一意性 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_career_plan | PRIMARY KEY | career_plan_id | 主キー制約 |
| uk_employee_year | UNIQUE | employee_id, plan_year | 社員・年度の組み合わせの一意性制約 |
| fk_employee | FOREIGN KEY | employee_id | MST_Employee.employee_id |
| fk_target_position | FOREIGN KEY | target_position_id | MST_Position.position_id |
| fk_target_dept | FOREIGN KEY | target_dept_id | MST_Department.department_id |
| fk_required_skill1 | FOREIGN KEY | required_skill_id1 | MST_SkillHierarchy.skill_id |
| fk_required_skill2 | FOREIGN KEY | required_skill_id2 | MST_SkillHierarchy.skill_id |
| fk_required_skill3 | FOREIGN KEY | required_skill_id3 | MST_SkillHierarchy.skill_id |
| fk_required_cert | FOREIGN KEY | required_cert_id | MST_Certification.cert_id |
| fk_mentor | FOREIGN KEY | mentor_id | MST_Employee.employee_id |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_plan_year | CHECK | plan_year | plan_year >= 2020 AND plan_year <= 2050 |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Employee | employee_id | 1:N | キャリアプランの対象社員 |
| MST_Position | target_position_id | 1:N | 目標とする役職 |
| MST_Department | target_dept_id | 1:N | 目標とする部署 |
| MST_SkillHierarchy | required_skill_id1-3 | 1:N | 目標達成に必要なスキル |
| MST_Certification | required_cert_id | 1:N | 目標達成に必要な資格 |
| MST_Employee | mentor_id | 1:N | メンター社員 |
| MST_Tenant | tenant_id | 1:N | テナント情報 |
| MST_UserAuth | created_by, updated_by | 1:N | 作成者・更新者 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| TRN_GoalProgress | career_plan_id | 1:N | 目標の進捗状況 |

## 5. データ仕様

### 5.1 目標期間定義
| 期間 | 説明 | 期間 |
|------|------|------|
| 短期目標 | 1年以内の目標 | 〜1年 |
| 中期目標 | 1〜3年の目標 | 1〜3年 |
| 長期目標 | 3〜5年の目標 | 3〜5年 |

### 5.2 確認プロセス
| ステップ | 説明 | フラグ |
|----------|------|-------|
| 作成 | 社員がキャリアプランを作成 | manager_confirmed=FALSE |
| 確認 | 上長が内容を確認・承認 | manager_confirmed=TRUE |

### 5.3 データ例
```sql
-- キャリアプランの例
INSERT INTO MST_CareerPlan (
    career_plan_id, employee_id, plan_year,
    short_term_goal, mid_term_goal, long_term_goal,
    target_position_id, target_dept_id,
    required_skill_id1, required_skill_id2, required_skill_id3,
    required_cert_id, mentor_id,
    tenant_id, created_by, updated_by
) VALUES (
    'CP_2024_001',
    'EMP_001',
    2024,
    'Javaフレームワークの習得とプロジェクトリーダー経験を積む',
    'システムアーキテクトとしてのスキルを身につけ、大規模プロジェクトの設計を担当する',
    '技術部門のマネージャーとして組織運営に携わる',
    'POS_003',
    'DEPT_002',
    'SKILL_JAVA_001',
    'SKILL_ARCH_001',
    'SKILL_MGMT_001',
    'CERT_PMP_001',
    'EMP_100',
    'TENANT_001',
    'EMP_001',
    'EMP_001'
);

-- 新入社員のキャリアプラン例
INSERT INTO MST_CareerPlan (
    career_plan_id, employee_id, plan_year,
    short_term_goal, mid_term_goal, long_term_goal,
    required_skill_id1, required_skill_id2,
    mentor_id, tenant_id, created_by, updated_by
) VALUES (
    'CP_2024_002',
    'EMP_002',
    2024,
    'プログラミング基礎を習得し、小規模な開発タスクを独力で完了できるようになる',
    'チームの一員として中規模プロジェクトに参画し、設計・開発・テストの全工程を経験する',
    'プロジェクトリーダーとして小規模チームをまとめ、後輩の指導も行う',
    'SKILL_PROG_001',
    'SKILL_DB_001',
    'EMP_101',
    'TENANT_001',
    'EMP_002',
    'EMP_002'
);
```

### 5.4 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 1,000件 | 全社員の当年度プラン |
| 年間増加件数 | 1,000件 | 年度更新 |
| 5年後想定件数 | 6,000件 | 履歴保持 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：RANGE
- パーティション条件：plan_year（年度単位）

### 6.3 アーカイブ
- アーカイブ条件：5年経過したプラン
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | employee_id, plan_year | 社員の年度別プラン |
| SELECT | 高 | manager_confirmed=FALSE | 未確認プラン一覧 |
| SELECT | 中 | target_position_id | 目標役職別集計 |
| SELECT | 中 | mentor_id | メンター別担当者 |
| SELECT | 中 | tenant_id | テナント別プラン |
| INSERT | 中 | - | 新規プラン作成 |
| UPDATE | 中 | career_plan_id | プラン更新 |

### 7.2 パフォーマンス要件
- SELECT：20ms以内
- INSERT：100ms以内
- UPDATE：100ms以内
- DELETE：100ms以内

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| hr_admin | ○ | ○ | ○ | × | 人事管理者 |
| manager | ○ | × | ○ | × | 管理職（部下のみ） |
| employee | ○ | ○ | ○ | × | 一般社員（自分のみ） |
| mentor | ○ | × | × | × | メンター（担当者のみ） |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含む（キャリア目標情報）
- 機密情報：含む（評価情報）
- 暗号化：必要（評価コメント）

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存人事システム
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 移行スクリプト例
```sql
-- 既存データの移行
INSERT INTO MST_CareerPlan (
    career_plan_id, employee_id, plan_year,
    short_term_goal, mid_term_goal, long_term_goal,
    tenant_id, created_by, updated_by
)
SELECT 
    CONCAT('CP_', plan_year, '_', LPAD(ROW_NUMBER() OVER (ORDER BY emp_no), 6, '0')),
    emp_no,
    plan_year,
    short_goal,
    mid_goal,
    long_goal,
    'TENANT_001',
    'migration',
    'migration'
FROM old_career_plan
WHERE is_valid = 1;
```

### 9.3 DDL
```sql
CREATE TABLE MST_CareerPlan (
    career_plan_id VARCHAR(50) NOT NULL,
    employee_id VARCHAR(20) NOT NULL,
    plan_year INTEGER NOT NULL,
    short_term_goal TEXT NOT NULL,
    mid_term_goal TEXT NOT NULL,
    long_term_goal TEXT NULL,
    target_position_id VARCHAR(20) NULL,
    target_dept_id VARCHAR(20) NULL,
    required_skill_id1 VARCHAR(50) NULL,
    required_skill_id2 VARCHAR(50) NULL,
    required_skill_id3 VARCHAR(50) NULL,
    required_cert_id VARCHAR(50) NULL,
    required_training_id VARCHAR(50) NULL,
    mentor_id VARCHAR(20) NULL,
    self_assessment TEXT NULL,
    manager_assessment TEXT NULL,
    manager_confirmed BOOLEAN NOT NULL DEFAULT FALSE,
    manager_confirmed_at TIMESTAMP NULL,
    tenant_id VARCHAR(50) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL,
    PRIMARY KEY (career_plan_id),
    UNIQUE KEY uk_employee_year (employee_id, plan_year),
    INDEX idx_employee (employee_id),
    INDEX idx_plan_year (plan_year),
    INDEX idx_target_position (target_position_id),
    INDEX idx_target_dept (target_dept_id),
    INDEX idx_mentor (mentor_id),
    INDEX idx_confirmed (manager_confirmed),
    INDEX idx_tenant (tenant_id),
    INDEX idx_active (is_active),
    CONSTRAINT fk_career_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(employee_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_career_target_position FOREIGN KEY (target_position_id) REFERENCES MST_Position(position_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_career_target_dept FOREIGN KEY (target_dept_id) REFERENCES MST_Department(department_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_career_skill1 FOREIGN KEY (required_skill_id1) REFERENCES MST_SkillHierarchy(skill_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_career_skill2 FOREIGN KEY (required_skill_id2) REFERENCES MST_SkillHierarchy(skill_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_career_skill3 FOREIGN KEY (required_skill_id3) REFERENCES MST_SkillHierarchy(skill_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_career_cert FOREIGN KEY (required_cert_id) REFERENCES MST_Certification(cert_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_career_mentor FOREIGN KEY (mentor_id) REFERENCES MST_Employee(employee_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_career_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_career_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_career_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_career_plan_year CHECK (plan_year >= 2020 AND plan_year <= 2050)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
PARTITION BY RANGE (plan_year) (
    PARTITION p2020 VALUES LESS THAN (2021),
    PARTITION p2021 VALUES LESS THAN (2022),
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

## 10. 特記事項

1. **年度管理**: 社員ごとに年度単位でキャリアプランを管理
2. **3段階目標**: 短期・中期・長期の段階的な目標設定
3. **スキル連携**: 必要スキルとの紐付けで具体的な成長計画
4. **メンター制度**: メンター社員との連携でキャリア支援
5. **承認プロセス**: 上長による確認・承認機能
6. **進捗管理**: TRN_GoalProgressとの連携で進捗追跡
7. **履歴保持**: 過去のキャリアプランを履歴として保持
8. **テナント分離**: マルチテナント対応
9. **評価連携**: 自己評価・上長評価の記録
10. **目標設定支援**: 役職・部署・スキル・資格との連携で具体的な目標設定
11. **定期見直し**: 年度ごとの見直しと継続的な改善
12. **人材育成**: 組織全体の人材育成計画との連携

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-31 | システムアーキテクト | 初版作成（キャリア開発管理対応） |
