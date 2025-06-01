# テーブル定義書：TRN_SkillRecord（スキル情報）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-010 |
| **テーブル名** | TRN_SkillRecord |
| **論理名** | スキル情報 |
| **カテゴリ** | トランザクション系 |
| **機能カテゴリ** | スキル管理 |
| **優先度** | 最高 |
| **個人情報含有** | なし |
| **機密情報レベル** | 中 |
| **暗号化要否** | 不要 |
| **ステータス** | 運用中 |
| **作成日** | 2025-06-01 |
| **最終更新日** | 2025-06-01 |

## 2. テーブル概要

### 2.1 概要・目的
TRN_SkillRecord（スキル情報）は、組織内の全社員が保有するスキル・技術・資格等の詳細情報を管理するトランザクションテーブルです。

主な目的：
- 社員個人のスキルポートフォリオ管理（技術スキル、ビジネススキル、資格等）
- スキルレベルの客観的評価・管理（5段階評価システム）
- 自己評価と上司評価による多面的スキル評価
- プロジェクトアサインメントのためのスキルマッチング
- 人材育成計画・キャリア開発支援
- 組織全体のスキル可視化・分析
- 資格取得状況・有効期限管理

このテーブルは、人材配置の最適化、教育研修計画の策定、組織のスキルギャップ分析など、
戦略的人材マネジメントの基盤となる重要なデータを提供します。


### 2.2 特記事項
- 社員とスキル項目の組み合わせは一意（1人の社員が同じスキルを複数持つことはない）
- スキルレベルは1-5の5段階評価（1:初級、5:マスター）
- 自己評価と上司評価は任意項目（評価制度に応じて入力）
- 有効期限は資格系スキルの場合に設定
- 学習時間とプロジェクト経験回数は統計・分析用
- スキル状況により論理削除を実現

### 2.3 関連API
API-008

### 2.4 関連バッチ
BATCH-006

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | id | ID | VARCHAR | 50 | × | ○ | - | - | 主キー |
| 2 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | テナントID |
| 3 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | レコードが有効かどうか |
| 4 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 5 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 6 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 7 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |
| 8 | employee_id | 社員ID | VARCHAR | 50 | ○ | - | ○ | - | スキルを保有する社員のID（MST_Employeeへの外部キー） |
| 9 | skill_item_id | スキル項目ID | VARCHAR | 50 | ○ | - | ○ | - | スキル項目のID（MST_SkillItemへの外部キー） |
| 10 | skill_level | スキルレベル | INT | None | ○ | - | - | - | スキルレベル（1:初級、2:中級、3:上級、4:エキスパート、5:マスター） |
| 11 | self_assessment | 自己評価 | INT | None | ○ | - | - | - | 自己評価（1-5段階） |
| 12 | manager_assessment | 上司評価 | INT | None | ○ | - | - | - | 上司による評価（1-5段階） |
| 13 | evidence_description | 証跡説明 | TEXT | None | ○ | - | - | - | スキル習得の証跡や根拠の説明 |
| 14 | acquisition_date | 習得日 | DATE | None | ○ | - | - | - | スキルを習得した日付 |
| 15 | last_used_date | 最終使用日 | DATE | None | ○ | - | - | - | スキルを最後に使用した日付 |
| 16 | expiry_date | 有効期限 | DATE | None | ○ | - | - | - | スキルの有効期限（資格等の場合） |
| 17 | certification_id | 関連資格ID | VARCHAR | 50 | ○ | - | ○ | - | 関連する資格のID（MST_Certificationへの外部キー） |
| 18 | skill_category_id | スキルカテゴリID | VARCHAR | 50 | ○ | - | ○ | - | スキルカテゴリのID（MST_SkillCategoryへの外部キー） |
| 19 | assessment_date | 評価日 | DATE | None | ○ | - | - | - | 最後に評価を行った日付 |
| 20 | assessor_id | 評価者ID | VARCHAR | 50 | ○ | - | ○ | - | 評価を行った人のID（MST_Employeeへの外部キー） |
| 21 | skill_status | スキル状況 | ENUM | None | ○ | - | - | ACTIVE | スキルの状況（ACTIVE:有効、EXPIRED:期限切れ、SUSPENDED:一時停止） |
| 22 | learning_hours | 学習時間 | INT | None | ○ | - | - | - | スキル習得にかけた学習時間（時間） |
| 23 | project_experience_count | プロジェクト経験回数 | INT | None | ○ | - | - | - | このスキルを使用したプロジェクトの回数 |


### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | id | 主キー |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |
| idx_created_at | INDEX | created_at | 作成日時検索用 |
| idx_employee_skill | UNIQUE INDEX | employee_id, skill_item_id | 社員・スキル項目の組み合わせ（一意） |
| idx_employee | INDEX | employee_id | 社員別検索用 |
| idx_skill_item | INDEX | skill_item_id | スキル項目別検索用 |
| idx_skill_level | INDEX | skill_level | スキルレベル別検索用 |
| idx_skill_category | INDEX | skill_category_id | スキルカテゴリ別検索用 |
| idx_certification | INDEX | certification_id | 資格別検索用 |
| idx_status | INDEX | skill_status | スキル状況別検索用 |
| idx_expiry_date | INDEX | expiry_date | 有効期限検索用 |
| idx_assessment_date | INDEX | assessment_date | 評価日検索用 |


### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_trn_skillrecord | PRIMARY KEY | id | 主キー制約 |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| uk_employee_skill | UNIQUE | employee_id, skill_item_id | ['employee_id', 'skill_item_id'] |
| chk_skill_level | CHECK |  | skill_level BETWEEN 1 AND 5 |
| chk_self_assessment | CHECK |  | self_assessment IS NULL OR self_assessment BETWEEN 1 AND 5 |
| chk_manager_assessment | CHECK |  | manager_assessment IS NULL OR manager_assessment BETWEEN 1 AND 5 |
| chk_skill_status | CHECK |  | skill_status IN ('ACTIVE', 'EXPIRED', 'SUSPENDED') |
| chk_learning_hours | CHECK |  | learning_hours IS NULL OR learning_hours >= 0 |
| chk_project_count | CHECK |  | project_experience_count IS NULL OR project_experience_count >= 0 |


## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_UserAuth | created_by, updated_by | 1:N | ユーザー情報 |
| MST_Employee | employee_id | 1:N | 社員への外部キー |
| MST_SkillItem | skill_item_id | 1:N | スキル項目への外部キー |
| MST_Certification | certification_id | 1:N | 資格への外部キー |
| MST_SkillCategory | skill_category_id | 1:N | スキルカテゴリへの外部キー |
| MST_Employee | assessor_id | 1:N | 評価者への外部キー |


### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| - | - | - | 必要に応じて追加 |

## 5. データ仕様

### 5.1 データ例
```sql
-- サンプルデータ
INSERT INTO TRN_SkillRecord (
    id, tenant_id, employee_id, skill_item_id, skill_level, self_assessment, manager_assessment, evidence_description, acquisition_date, last_used_date, expiry_date, certification_id, skill_category_id, assessment_date, assessor_id, skill_status, learning_hours, project_experience_count, created_by, updated_by
) VALUES (
    'sample_001', 'tenant_001', 'EMP000001', 'SKILL001', '4', '4', '3', 'Javaを使用したWebアプリケーション開発プロジェクトを3件担当', '2020-06-01', '2025-05-30', NULL, 'CERT001', 'CAT001', '2025-04-01', 'EMP000010', 'ACTIVE', '120', '3', 'user_admin', 'user_admin'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 500件 | 初期設定データ |
| 月間増加件数 | 100件 | 想定値 |
| 年間増加件数 | 1,200件 | 想定値 |
| 5年後想定件数 | 6,500件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：なし
- パーティション条件：-

### 6.3 アーカイブ
- アーカイブ条件：作成から3年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | id, tenant_id | 基本検索 |
| INSERT | 中 | - | 新規登録 |
| UPDATE | 中 | id | 更新処理 |
| DELETE | 低 | id | 削除処理 |

### 7.2 パフォーマンス要件
- SELECT：15ms以内
- INSERT：50ms以内
- UPDATE：50ms以内
- DELETE：100ms以内

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| tenant_admin | ○ | ○ | ○ | × | テナント管理者（自テナントのみ） |
| user | ○ | × | × | × | 一般ユーザー（参照のみ） |

### 8.2 データ保護
- 個人情報：なし
- 機密情報：中レベル
- 暗号化：不要

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存システム
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
-- スキル情報テーブル作成DDL
CREATE TABLE TRN_SkillRecord (
    id VARCHAR(50) NOT NULL COMMENT 'ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '有効フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT '作成者ID',
    updated_by VARCHAR(50) NOT NULL COMMENT '更新者ID',
    employee_id VARCHAR(50) COMMENT '社員ID',
    skill_item_id VARCHAR(50) COMMENT 'スキル項目ID',
    skill_level INT COMMENT 'スキルレベル',
    self_assessment INT COMMENT '自己評価',
    manager_assessment INT COMMENT '上司評価',
    evidence_description TEXT COMMENT '証跡説明',
    acquisition_date DATE COMMENT '習得日',
    last_used_date DATE COMMENT '最終使用日',
    expiry_date DATE COMMENT '有効期限',
    certification_id VARCHAR(50) COMMENT '関連資格ID',
    skill_category_id VARCHAR(50) COMMENT 'スキルカテゴリID',
    assessment_date DATE COMMENT '評価日',
    assessor_id VARCHAR(50) COMMENT '評価者ID',
    skill_status ENUM DEFAULT ACTIVE COMMENT 'スキル状況',
    learning_hours INT COMMENT '学習時間',
    project_experience_count INT COMMENT 'プロジェクト経験回数',
    PRIMARY KEY (id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_active (is_active),
    INDEX idx_created_at (created_at),
    UNIQUE INDEX idx_employee_skill (employee_id, skill_item_id),
    INDEX idx_employee (employee_id),
    INDEX idx_skill_item (skill_item_id),
    INDEX idx_skill_level (skill_level),
    INDEX idx_skill_category (skill_category_id),
    INDEX idx_certification (certification_id),
    INDEX idx_status (skill_status),
    INDEX idx_expiry_date (expiry_date),
    INDEX idx_assessment_date (assessment_date),
    CONSTRAINT fk_skill_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_skill_item FOREIGN KEY (skill_item_id) REFERENCES MST_SkillItem(id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_skill_certification FOREIGN KEY (certification_id) REFERENCES MST_Certification(id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_skill_category FOREIGN KEY (skill_category_id) REFERENCES MST_SkillCategory(id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_skill_assessor FOREIGN KEY (assessor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='スキル情報';

```

## 10. 特記事項

1. **設計方針**
   - トランザクション系として設計
   - マルチテナント対応
   - 監査証跡の保持

2. **運用上の注意点**
   - 定期的なデータクリーンアップが必要
   - パフォーマンス監視を実施
   - データ量見積もりの定期見直し

3. **今後の拡張予定**
   - 必要に応じて機能拡張を検討

4. **関連画面**
   - 関連画面情報

5. **データ量・パフォーマンス監視**
   - データ量が想定の150%を超えた場合はアラート
   - 応答時間が設定値の120%を超えた場合は調査


## 11. 業務ルール

- スキルレベルは客観的な基準に基づいて設定
- 自己評価と上司評価の乖離が大きい場合は再評価を実施
- 有効期限が近づいた資格は自動的に通知
- 期限切れスキルは skill_status を EXPIRED に変更
- 評価は年1回以上実施することを推奨
- プロジェクト経験回数は実績管理システムと連携
