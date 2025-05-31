# テーブル定義書：スキル評価記録 (TRN_SkillRecord)

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-011 |
| **テーブル名** | TRN_SkillRecord |
| **論理名** | スキル評価記録 |
| **カテゴリ** | トランザクション系 |
| **優先度** | 最高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-05-29 |
| **最終更新日** | 2025-05-31 |

## 2. テーブル概要

### 2.1 概要・目的
スキル評価記録テーブル（TRN_SkillRecord）は、社員のスキル評価結果を記録します。自己評価・上司評価・第三者評価の3つの評価軸で4段階評価（×/△/○/◎）を管理し、評価履歴の追跡とスキル成長の可視化を支援します。

### 2.2 関連API
- [API-010](../api/specs/API仕様書_API-010.md) - スキル評価API
- [API-011](../api/specs/API仕様書_API-011.md) - スキル記録管理API

### 2.3 関連バッチ
- [BATCH-009](../batch/specs/バッチ定義書_BATCH-009.md) - スキル評価集計バッチ
- [BATCH-010](../batch/specs/バッチ定義書_BATCH-010.md) - スキル成長分析バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | record_id | 記録ID | VARCHAR | 20 | × | ○ | - | - | スキル評価記録を一意に識別するID |
| 2 | employee_id | 社員ID | VARCHAR | 20 | × | - | ○ | - | 評価対象の社員ID |
| 3 | skill_id | スキルID | VARCHAR | 20 | × | - | ○ | - | 評価対象のスキル項目ID |
| 4 | evaluation_period | 評価期間 | VARCHAR | 10 | × | - | - | - | 評価期間（YYYY-MM形式） |
| 5 | evaluation_date | 評価日 | DATE | - | × | - | - | - | 評価実施日 |
| 6 | self_evaluation | 自己評価 | INTEGER | - | ○ | - | - | NULL | 自己評価（1:×、2:△、3:○、4:◎） |
| 7 | supervisor_evaluation | 上司評価 | INTEGER | - | ○ | - | - | NULL | 上司評価（1:×、2:△、3:○、4:◎） |
| 8 | peer_evaluation | 第三者評価 | INTEGER | - | ○ | - | - | NULL | 第三者評価（1:×、2:△、3:○、4:◎） |
| 9 | final_evaluation | 最終評価 | INTEGER | - | ○ | - | - | NULL | 最終確定評価（1:×、2:△、3:○、4:◎） |
| 10 | self_comment | 自己評価コメント | TEXT | - | ○ | - | - | NULL | 自己評価の詳細コメント |
| 11 | supervisor_comment | 上司評価コメント | TEXT | - | ○ | - | - | NULL | 上司評価の詳細コメント |
| 12 | peer_comment | 第三者評価コメント | TEXT | - | ○ | - | - | NULL | 第三者評価の詳細コメント |
| 13 | improvement_plan | 改善計画 | TEXT | - | ○ | - | - | NULL | スキル向上のための改善計画 |
| 14 | learning_goal | 学習目標 | TEXT | - | ○ | - | - | NULL | 次期までの学習目標 |
| 15 | evidence_count | 証跡件数 | INTEGER | - | × | - | - | 0 | 提出された証跡の件数 |
| 16 | supervisor_id | 評価者ID | VARCHAR | 20 | ○ | - | ○ | NULL | 上司評価を行った社員ID |
| 17 | peer_evaluator_id | 第三者評価者ID | VARCHAR | 20 | ○ | - | ○ | NULL | 第三者評価を行った社員ID |
| 18 | evaluation_status | 評価ステータス | VARCHAR | 20 | × | - | - | 'DRAFT' | 評価の進行状況 |
| 19 | approval_date | 承認日 | DATE | - | ○ | - | - | NULL | 評価承認日 |
| 20 | approved_by | 承認者ID | VARCHAR | 20 | ○ | - | ○ | NULL | 評価承認者の社員ID |
| 21 | previous_evaluation | 前回評価 | INTEGER | - | ○ | - | - | NULL | 前回の最終評価 |
| 22 | growth_rate | 成長率 | DECIMAL | 5,2 | ○ | - | - | NULL | 前回からの成長率（%） |
| 23 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | 所属テナントのID |
| 24 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | 記録が有効かどうか |
| 25 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 26 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 27 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 28 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | record_id | 主キー |
| idx_employee_skill | UNIQUE | employee_id, skill_id, evaluation_period | 社員・スキル・期間の一意性を保証 |
| idx_employee | INDEX | employee_id | 社員検索用 |
| idx_skill | INDEX | skill_id | スキル検索用 |
| idx_period | INDEX | evaluation_period | 評価期間検索用 |
| idx_supervisor | INDEX | supervisor_id | 評価者検索用 |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_status | INDEX | evaluation_status | ステータス検索用 |
| idx_date | INDEX | evaluation_date | 評価日検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_skill_record | PRIMARY KEY | record_id | 主キー制約 |
| uq_employee_skill_period | UNIQUE | employee_id, skill_id, evaluation_period | 社員・スキル・期間の一意性を保証 |
| fk_employee | FOREIGN KEY | employee_id | MST_Employee.employee_id |
| fk_skill | FOREIGN KEY | skill_id | MST_SkillItem.skill_id |
| fk_supervisor | FOREIGN KEY | supervisor_id | MST_Employee.employee_id |
| fk_peer_evaluator | FOREIGN KEY | peer_evaluator_id | MST_Employee.employee_id |
| fk_approved_by | FOREIGN KEY | approved_by | MST_Employee.employee_id |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_self_evaluation | CHECK | self_evaluation | self_evaluation IS NULL OR (self_evaluation >= 1 AND self_evaluation <= 4) |
| chk_supervisor_evaluation | CHECK | supervisor_evaluation | supervisor_evaluation IS NULL OR (supervisor_evaluation >= 1 AND supervisor_evaluation <= 4) |
| chk_peer_evaluation | CHECK | peer_evaluation | peer_evaluation IS NULL OR (peer_evaluation >= 1 AND peer_evaluation <= 4) |
| chk_final_evaluation | CHECK | final_evaluation | final_evaluation IS NULL OR (final_evaluation >= 1 AND final_evaluation <= 4) |
| chk_previous_evaluation | CHECK | previous_evaluation | previous_evaluation IS NULL OR (previous_evaluation >= 1 AND previous_evaluation <= 4) |
| chk_evaluation_status | CHECK | evaluation_status | evaluation_status IN ('DRAFT', 'SELF_COMPLETED', 'SUPERVISOR_COMPLETED', 'PEER_COMPLETED', 'APPROVED', 'REJECTED') |
| chk_evidence_count | CHECK | evidence_count | evidence_count >= 0 |
| chk_growth_rate | CHECK | growth_rate | growth_rate IS NULL OR growth_rate >= -100.00 |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Employee | employee_id | 1:N | 評価対象社員 |
| MST_SkillItem | skill_id | 1:N | 評価対象スキル |
| MST_Employee | supervisor_id | 1:N | 評価者（上司） |
| MST_Employee | peer_evaluator_id | 1:N | 第三者評価者 |
| MST_Employee | approved_by | 1:N | 承認者 |
| MST_Tenant | tenant_id | 1:N | テナント情報 |
| MST_UserAuth | created_by, updated_by | 1:N | 作成者・更新者 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| TRN_SkillEvidence | record_id | 1:N | スキル証跡 |

## 5. データ仕様

### 5.1 データ例
```sql
INSERT INTO TRN_SkillRecord (
    record_id, employee_id, skill_id, evaluation_period,
    evaluation_date, self_evaluation, supervisor_evaluation,
    final_evaluation, self_comment, supervisor_comment,
    supervisor_id, evaluation_status, tenant_id,
    created_by, updated_by
) VALUES (
    'REC_001',
    'EMP_001',
    'SKILL_001',
    '2024-03',
    '2024-03-31',
    3,
    3,
    3,
    'Javaの基本的な文法を理解し、簡単なWebアプリケーションを開発できるようになりました。',
    '基礎的なスキルは身についている。今後はフレームワークの習得を期待する。',
    'EMP_002',
    'APPROVED',
    'TENANT_001',
    'system',
    'system'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 0件 | 新規システム |
| 月間増加件数 | 50,000件 | 社員数×スキル数×評価頻度 |
| 年間増加件数 | 600,000件 | 想定値 |
| 5年後想定件数 | 3,000,000件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：RANGE
- パーティション条件：evaluation_period（月単位）

### 6.3 アーカイブ
- アーカイブ条件：評価期間から3年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | employee_id, evaluation_period | 社員別期間別評価取得 |
| SELECT | 高 | skill_id, evaluation_period | スキル別期間別評価取得 |
| SELECT | 中 | tenant_id, evaluation_period | テナント別期間別評価取得 |
| SELECT | 中 | evaluation_status | ステータス別評価取得 |
| UPDATE | 中 | record_id | 評価更新 |
| INSERT | 中 | - | 新規評価記録作成 |

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
| manager | ○ | ○ | ○ | × | 管理職（部下のみ） |
| employee | ○ | ○ | ○ | × | 一般社員（自分のみ） |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含む（評価情報）
- 機密情報：含む（人事評価）
- 暗号化：必要（評価コメント）

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存人事評価システム
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
CREATE TABLE TRN_SkillRecord (
    record_id VARCHAR(20) NOT NULL,
    employee_id VARCHAR(20) NOT NULL,
    skill_id VARCHAR(20) NOT NULL,
    evaluation_period VARCHAR(10) NOT NULL,
    evaluation_date DATE NOT NULL,
    self_evaluation INTEGER NULL,
    supervisor_evaluation INTEGER NULL,
    peer_evaluation INTEGER NULL,
    final_evaluation INTEGER NULL,
    self_comment TEXT NULL,
    supervisor_comment TEXT NULL,
    peer_comment TEXT NULL,
    improvement_plan TEXT NULL,
    learning_goal TEXT NULL,
    evidence_count INTEGER NOT NULL DEFAULT 0,
    supervisor_id VARCHAR(20) NULL,
    peer_evaluator_id VARCHAR(20) NULL,
    evaluation_status VARCHAR(20) NOT NULL DEFAULT 'DRAFT',
    approval_date DATE NULL,
    approved_by VARCHAR(20) NULL,
    previous_evaluation INTEGER NULL,
    growth_rate DECIMAL(5,2) NULL,
    tenant_id VARCHAR(50) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL,
    PRIMARY KEY (record_id),
    UNIQUE KEY idx_employee_skill_period (employee_id, skill_id, evaluation_period),
    INDEX idx_employee (employee_id),
    INDEX idx_skill (skill_id),
    INDEX idx_period (evaluation_period),
    INDEX idx_supervisor (supervisor_id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_status (evaluation_status),
    INDEX idx_date (evaluation_date),
    INDEX idx_active (is_active),
    CONSTRAINT fk_skill_record_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(employee_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_skill_record_skill FOREIGN KEY (skill_id) REFERENCES MST_SkillItem(skill_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_skill_record_supervisor FOREIGN KEY (supervisor_id) REFERENCES MST_Employee(employee_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_skill_record_peer_evaluator FOREIGN KEY (peer_evaluator_id) REFERENCES MST_Employee(employee_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_skill_record_approved_by FOREIGN KEY (approved_by) REFERENCES MST_Employee(employee_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_skill_record_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_skill_record_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_skill_record_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_skill_record_self_evaluation CHECK (self_evaluation IS NULL OR (self_evaluation >= 1 AND self_evaluation <= 4)),
    CONSTRAINT chk_skill_record_supervisor_evaluation CHECK (supervisor_evaluation IS NULL OR (supervisor_evaluation >= 1 AND supervisor_evaluation <= 4)),
    CONSTRAINT chk_skill_record_peer_evaluation CHECK (peer_evaluation IS NULL OR (peer_evaluation >= 1 AND peer_evaluation <= 4)),
    CONSTRAINT chk_skill_record_final_evaluation CHECK (final_evaluation IS NULL OR (final_evaluation >= 1 AND final_evaluation <= 4)),
    CONSTRAINT chk_skill_record_previous_evaluation CHECK (previous_evaluation IS NULL OR (previous_evaluation >= 1 AND previous_evaluation <= 4)),
    CONSTRAINT chk_skill_record_evaluation_status CHECK (evaluation_status IN ('DRAFT', 'SELF_COMPLETED', 'SUPERVISOR_COMPLETED', 'PEER_COMPLETED', 'APPROVED', 'REJECTED')),
    CONSTRAINT chk_skill_record_evidence_count CHECK (evidence_count >= 0),
    CONSTRAINT chk_skill_record_growth_rate CHECK (growth_rate IS NULL OR growth_rate >= -100.00)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
PARTITION BY RANGE (YEAR(STR_TO_DATE(CONCAT(evaluation_period, '-01'), '%Y-%m-%d'))) (
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p2026 VALUES LESS THAN (2027),
    PARTITION p2027 VALUES LESS THAN (2028),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

## 10. 特記事項

1. 3つの評価軸（自己・上司・第三者）による多面的評価
2. 4段階評価（×/△/○/◎）による統一的な評価基準
3. 評価ワークフローによる段階的な評価プロセス
4. 前回評価との比較による成長率の自動計算
5. 証跡件数による評価の客観性担保
6. 評価期間による履歴管理とトレンド分析
7. パーティション設計による大量データの効率的管理
8. 評価コメントの暗号化による機密性保護
9. 承認フローによる評価品質の確保
10. テナント分離による多組織対応

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-29 | システムアーキテクト | 初版作成 |
| 1.1 | 2025-05-31 | システムアーキテクト | 新フォーマットに変更、詳細情報追加 |
