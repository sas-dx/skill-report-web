# テーブル定義書：社員部署関連 (MST_EmployeeDepartment)

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-017 |
| **テーブル名** | MST_EmployeeDepartment |
| **論理名** | 社員部署関連 |
| **カテゴリ** | マスタ系 |
| **優先度** | 最高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-05-31 |
| **最終更新日** | 2025-05-31 |

## 2. テーブル概要

### 2.1 概要・目的
社員部署関連テーブル（MST_EmployeeDepartment）は、社員の部署配属情報を管理し、主務・兼務の概念を実現します。複数部署への配属、配属期間の履歴管理、配属種別の管理により、複雑な組織構造に対応した柔軟な人事管理を提供します。

### 2.2 関連API
- [API-005](../api/specs/API仕様書_API-005.md) - 社員情報管理API
- [API-006](../api/specs/API仕様書_API-006.md) - 組織情報管理API
- [API-020](../api/specs/API仕様書_API-020.md) - 配属管理API（新規）

### 2.3 関連バッチ
- [BATCH-004](../batch/specs/バッチ定義書_BATCH-004.md) - 社員情報同期バッチ
- [BATCH-015](../batch/specs/バッチ定義書_BATCH-015.md) - マスタデータ同期バッチ
- [BATCH-025](../batch/specs/バッチ定義書_BATCH-025.md) - 配属整合性チェックバッチ（新規）

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | assignment_id | 配属ID | VARCHAR | 20 | × | ○ | - | - | 配属を一意に識別するID |
| 2 | employee_id | 社員ID | VARCHAR | 20 | × | - | ○ | - | 配属対象の社員ID |
| 3 | department_id | 部署ID | VARCHAR | 20 | × | - | ○ | - | 配属先の部署ID |
| 4 | assignment_type | 配属種別 | VARCHAR | 20 | × | - | - | 'PRIMARY' | 配属の種別（主務/兼務等） |
| 5 | assignment_ratio | 配属比率 | DECIMAL | 5,2 | ○ | - | - | NULL | 配属比率（%）兼務時の工数配分 |
| 6 | start_date | 配属開始日 | DATE | - | × | - | - | - | 配属開始年月日 |
| 7 | end_date | 配属終了日 | DATE | - | ○ | - | - | NULL | 配属終了年月日 |
| 8 | assignment_reason | 配属理由 | VARCHAR | 100 | ○ | - | - | NULL | 配属の理由・目的 |
| 9 | reporting_manager_id | 報告先上司ID | VARCHAR | 20 | ○ | - | ○ | NULL | 当該部署での報告先上司 |
| 10 | cost_allocation | コスト配分 | DECIMAL | 5,2 | ○ | - | - | NULL | コスト配分比率（%） |
| 11 | approval_status | 承認状況 | VARCHAR | 20 | × | - | - | 'PENDING' | 配属の承認状況 |
| 12 | approved_by | 承認者ID | VARCHAR | 50 | ○ | - | ○ | NULL | 配属を承認したユーザーID |
| 13 | approved_at | 承認日時 | TIMESTAMP | - | ○ | - | - | NULL | 承認された日時 |
| 14 | remarks | 備考 | TEXT | - | ○ | - | - | NULL | 配属に関する備考・特記事項 |
| 15 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | 所属テナントのID |
| 16 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | 配属が有効かどうか |
| 17 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 18 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 19 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 20 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | assignment_id | 主キー |
| idx_employee_dept | UNIQUE | employee_id, department_id, start_date | 同一社員・部署・開始日の重複防止 |
| idx_employee | INDEX | employee_id | 社員検索用 |
| idx_department | INDEX | department_id | 部署検索用 |
| idx_assignment_type | INDEX | assignment_type | 配属種別検索用 |
| idx_period | INDEX | start_date, end_date | 期間検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_manager | INDEX | reporting_manager_id | 報告先上司検索用 |
| idx_approval | INDEX | approval_status | 承認状況検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_assignment | PRIMARY KEY | assignment_id | 主キー制約 |
| uq_employee_dept_date | UNIQUE | employee_id, department_id, start_date | 同一社員・部署・開始日の重複防止 |
| fk_employee | FOREIGN KEY | employee_id | MST_Employee.employee_id |
| fk_department | FOREIGN KEY | department_id | MST_Department.department_id |
| fk_reporting_manager | FOREIGN KEY | reporting_manager_id | MST_Employee.employee_id |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_approved_by | FOREIGN KEY | approved_by | MST_UserAuth.user_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_assignment_type | CHECK | assignment_type | assignment_type IN ('PRIMARY', 'CONCURRENT', 'TEMPORARY', 'ACTING') |
| chk_assignment_ratio | CHECK | assignment_ratio | assignment_ratio IS NULL OR (assignment_ratio >= 0 AND assignment_ratio <= 100) |
| chk_cost_allocation | CHECK | cost_allocation | cost_allocation IS NULL OR (cost_allocation >= 0 AND cost_allocation <= 100) |
| chk_end_date | CHECK | end_date | end_date IS NULL OR end_date >= start_date |
| chk_approval_status | CHECK | approval_status | approval_status IN ('PENDING', 'APPROVED', 'REJECTED', 'CANCELLED') |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Employee | employee_id | 1:N | 配属対象社員 |
| MST_Department | department_id | 1:N | 配属先部署 |
| MST_Employee | reporting_manager_id | 1:N | 報告先上司 |
| MST_Tenant | tenant_id | 1:N | テナント情報 |
| MST_UserAuth | approved_by, created_by, updated_by | 1:N | 承認者・作成者・更新者 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| TRN_SkillRecord | assignment_id | 1:N | 配属別スキル記録 |
| TRN_WorkLog | assignment_id | 1:N | 配属別作業ログ |

## 5. データ仕様

### 5.1 配属種別定義
| 配属種別 | 説明 | 用途 |
|----------|------|------|
| PRIMARY | 主務 | メインの所属部署 |
| CONCURRENT | 兼務 | サブの所属部署 |
| TEMPORARY | 一時配属 | 期間限定の配属 |
| ACTING | 代理・代行 | 他者の代理としての配属 |

### 5.2 承認状況定義
| 承認状況 | 説明 | 次の状態 |
|----------|------|----------|
| PENDING | 承認待ち | APPROVED, REJECTED |
| APPROVED | 承認済み | CANCELLED |
| REJECTED | 却下 | PENDING（再申請） |
| CANCELLED | 取消 | - |

### 5.3 データ例
```sql
-- 主務配属
INSERT INTO MST_EmployeeDepartment (
    assignment_id, employee_id, department_id, assignment_type,
    assignment_ratio, start_date, reporting_manager_id,
    cost_allocation, approval_status, approved_by,
    tenant_id, created_by, updated_by
) VALUES (
    'ASSIGN_001',
    'EMP_001',
    'DEPT_001',
    'PRIMARY',
    100.00,
    '2023-04-01',
    'EMP_002',
    100.00,
    'APPROVED',
    'USER_001',
    'TENANT_001',
    'system',
    'system'
);

-- 兼務配属
INSERT INTO MST_EmployeeDepartment (
    assignment_id, employee_id, department_id, assignment_type,
    assignment_ratio, start_date, reporting_manager_id,
    cost_allocation, approval_status, approved_by,
    tenant_id, created_by, updated_by
) VALUES (
    'ASSIGN_002',
    'EMP_001',
    'DEPT_002',
    'CONCURRENT',
    30.00,
    '2023-06-01',
    'EMP_003',
    30.00,
    'APPROVED',
    'USER_001',
    'TENANT_001',
    'system',
    'system'
);
```

### 5.4 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 1,200件 | 既存社員の主務配属 |
| 年間増加件数 | 500件 | 兼務・異動・新規配属 |
| 5年後想定件数 | 3,700件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：RANGE
- パーティション条件：start_date（年単位）

### 6.3 アーカイブ
- アーカイブ条件：配属終了から3年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | employee_id, is_active | 社員の有効配属一覧 |
| SELECT | 高 | department_id, is_active | 部署の配属社員一覧 |
| SELECT | 中 | assignment_type | 配属種別検索 |
| SELECT | 中 | start_date, end_date | 期間指定検索 |
| INSERT | 中 | - | 新規配属登録 |
| UPDATE | 中 | assignment_id | 配属情報更新 |

### 7.2 パフォーマンス要件
- SELECT：15ms以内
- INSERT：100ms以内
- UPDATE：100ms以内
- DELETE：100ms以内

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| hr_admin | ○ | ○ | ○ | × | 人事管理者 |
| dept_manager | ○ | ○ | ○ | × | 部署管理者（自部署のみ） |
| manager | ○ | × | × | × | 管理職 |
| employee | ○ | × | × | × | 一般社員（自分のみ） |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含む（配属情報）
- 機密情報：含む（組織情報、人事情報）
- 暗号化：必要（配属理由、備考）

## 9. 移行仕様

### 9.1 データ移行
- 移行元：MST_Employee（既存の主務情報）
- 移行方法：SQLスクリプト実行
- 移行タイミング：システム移行時

### 9.2 移行スクリプト例
```sql
-- 既存の主務配属データを移行
INSERT INTO MST_EmployeeDepartment (
    assignment_id, employee_id, department_id, assignment_type,
    assignment_ratio, start_date, reporting_manager_id,
    cost_allocation, approval_status, tenant_id,
    created_by, updated_by
)
SELECT 
    CONCAT('ASSIGN_', LPAD(ROW_NUMBER() OVER (ORDER BY employee_id), 6, '0')),
    employee_id,
    department_id,
    'PRIMARY',
    100.00,
    hire_date,
    manager_id,
    100.00,
    'APPROVED',
    tenant_id,
    'migration',
    'migration'
FROM MST_Employee
WHERE is_active = TRUE;
```

### 9.3 DDL
```sql
CREATE TABLE MST_EmployeeDepartment (
    assignment_id VARCHAR(20) NOT NULL,
    employee_id VARCHAR(20) NOT NULL,
    department_id VARCHAR(20) NOT NULL,
    assignment_type VARCHAR(20) NOT NULL DEFAULT 'PRIMARY',
    assignment_ratio DECIMAL(5,2) NULL,
    start_date DATE NOT NULL,
    end_date DATE NULL,
    assignment_reason VARCHAR(100) NULL,
    reporting_manager_id VARCHAR(20) NULL,
    cost_allocation DECIMAL(5,2) NULL,
    approval_status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    approved_by VARCHAR(50) NULL,
    approved_at TIMESTAMP NULL,
    remarks TEXT NULL,
    tenant_id VARCHAR(50) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL,
    PRIMARY KEY (assignment_id),
    UNIQUE KEY idx_employee_dept_date (employee_id, department_id, start_date),
    INDEX idx_employee (employee_id),
    INDEX idx_department (department_id),
    INDEX idx_assignment_type (assignment_type),
    INDEX idx_period (start_date, end_date),
    INDEX idx_active (is_active),
    INDEX idx_tenant (tenant_id),
    INDEX idx_manager (reporting_manager_id),
    INDEX idx_approval (approval_status),
    CONSTRAINT fk_emp_dept_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(employee_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_emp_dept_department FOREIGN KEY (department_id) REFERENCES MST_Department(department_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_emp_dept_manager FOREIGN KEY (reporting_manager_id) REFERENCES MST_Employee(employee_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_emp_dept_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_emp_dept_approved_by FOREIGN KEY (approved_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_emp_dept_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_emp_dept_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_emp_dept_assignment_type CHECK (assignment_type IN ('PRIMARY', 'CONCURRENT', 'TEMPORARY', 'ACTING')),
    CONSTRAINT chk_emp_dept_assignment_ratio CHECK (assignment_ratio IS NULL OR (assignment_ratio >= 0 AND assignment_ratio <= 100)),
    CONSTRAINT chk_emp_dept_cost_allocation CHECK (cost_allocation IS NULL OR (cost_allocation >= 0 AND cost_allocation <= 100)),
    CONSTRAINT chk_emp_dept_end_date CHECK (end_date IS NULL OR end_date >= start_date),
    CONSTRAINT chk_emp_dept_approval_status CHECK (approval_status IN ('PENDING', 'APPROVED', 'REJECTED', 'CANCELLED'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
PARTITION BY RANGE (YEAR(start_date)) (
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p2026 VALUES LESS THAN (2027),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

## 10. 特記事項

1. **主務・兼務の管理**: assignment_typeにより主務（PRIMARY）と兼務（CONCURRENT）を区別
2. **配属比率管理**: assignment_ratioにより工数配分を管理（兼務時の業務比率）
3. **コスト配分**: cost_allocationによりコスト配分比率を管理
4. **承認ワークフロー**: approval_statusにより配属の承認プロセスを管理
5. **履歴管理**: 配属期間（start_date, end_date）により履歴を管理
6. **報告先管理**: reporting_manager_idにより部署別の報告先上司を設定
7. **パーティション設計**: 年単位でのパーティションにより大量データに対応
8. **既存システム連携**: MST_Employeeの主務情報との整合性を保持
9. **一時配属対応**: TEMPORARY、ACTINGにより特殊な配属パターンに対応
10. **監査対応**: 作成者・更新者・承認者の記録により監査要件に対応

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-31 | システムアーキテクト | 初版作成（主務・兼務機能対応） |
