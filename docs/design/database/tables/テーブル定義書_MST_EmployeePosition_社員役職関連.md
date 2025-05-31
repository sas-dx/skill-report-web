# テーブル定義書：社員役職関連 (MST_EmployeePosition)

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-018 |
| **テーブル名** | MST_EmployeePosition |
| **論理名** | 社員役職関連 |
| **カテゴリ** | マスタ系 |
| **優先度** | 最高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-05-31 |
| **最終更新日** | 2025-05-31 |

## 2. テーブル概要

### 2.1 概要・目的
社員役職関連テーブル（MST_EmployeePosition）は、社員の役職任命情報を管理し、部署別の役職設定や主務・兼務の概念を実現します。複数役職の保持、任命期間の履歴管理、部署別役職の管理により、複雑な組織構造に対応した柔軟な役職管理を提供します。

### 2.2 関連API
- [API-005](../api/specs/API仕様書_API-005.md) - 社員情報管理API
- [API-006](../api/specs/API仕様書_API-006.md) - 組織情報管理API
- [API-021](../api/specs/API仕様書_API-021.md) - 役職任命管理API（新規）

### 2.3 関連バッチ
- [BATCH-004](../batch/specs/バッチ定義書_BATCH-004.md) - 社員情報同期バッチ
- [BATCH-015](../batch/specs/バッチ定義書_BATCH-015.md) - マスタデータ同期バッチ
- [BATCH-026](../batch/specs/バッチ定義書_BATCH-026.md) - 役職整合性チェックバッチ（新規）

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | appointment_id | 任命ID | VARCHAR | 20 | × | ○ | - | - | 役職任命を一意に識別するID |
| 2 | employee_id | 社員ID | VARCHAR | 20 | × | - | ○ | - | 任命対象の社員ID |
| 3 | position_id | 役職ID | VARCHAR | 20 | × | - | ○ | - | 任命する役職ID |
| 4 | department_id | 対象部署ID | VARCHAR | 20 | × | - | ○ | - | 役職を担当する部署ID |
| 5 | appointment_type | 任命種別 | VARCHAR | 20 | × | - | - | 'PRIMARY' | 任命の種別（主務/兼務等） |
| 6 | responsibility_scope | 責任範囲 | VARCHAR | 100 | ○ | - | - | NULL | 役職の責任範囲・担当領域 |
| 7 | start_date | 任命開始日 | DATE | - | × | - | - | - | 役職任命開始年月日 |
| 8 | end_date | 任命終了日 | DATE | - | ○ | - | - | NULL | 役職任命終了年月日 |
| 9 | appointment_reason | 任命理由 | VARCHAR | 100 | ○ | - | - | NULL | 任命の理由・目的 |
| 10 | delegation_authority | 委任権限 | TEXT | - | ○ | - | - | NULL | 委任された権限の詳細 |
| 11 | approval_limit | 承認限度額 | DECIMAL | 15,2 | ○ | - | - | NULL | 当該役職での承認可能金額 |
| 12 | is_acting | 代理フラグ | BOOLEAN | - | × | - | - | FALSE | 代理役職かどうか |
| 13 | acting_for_employee_id | 代理対象社員ID | VARCHAR | 20 | ○ | - | ○ | NULL | 代理する対象の社員ID |
| 14 | approval_status | 承認状況 | VARCHAR | 20 | × | - | - | 'PENDING' | 任命の承認状況 |
| 15 | approved_by | 承認者ID | VARCHAR | 50 | ○ | - | ○ | NULL | 任命を承認したユーザーID |
| 16 | approved_at | 承認日時 | TIMESTAMP | - | ○ | - | - | NULL | 承認された日時 |
| 17 | remarks | 備考 | TEXT | - | ○ | - | - | NULL | 任命に関する備考・特記事項 |
| 18 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | 所属テナントのID |
| 19 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | 任命が有効かどうか |
| 20 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 21 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 22 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 23 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | appointment_id | 主キー |
| idx_employee_pos_dept | UNIQUE | employee_id, position_id, department_id, start_date | 同一社員・役職・部署・開始日の重複防止 |
| idx_employee | INDEX | employee_id | 社員検索用 |
| idx_position | INDEX | position_id | 役職検索用 |
| idx_department | INDEX | department_id | 部署検索用 |
| idx_appointment_type | INDEX | appointment_type | 任命種別検索用 |
| idx_period | INDEX | start_date, end_date | 期間検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_acting | INDEX | is_acting | 代理フラグ検索用 |
| idx_acting_for | INDEX | acting_for_employee_id | 代理対象検索用 |
| idx_approval | INDEX | approval_status | 承認状況検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_appointment | PRIMARY KEY | appointment_id | 主キー制約 |
| uq_emp_pos_dept_date | UNIQUE | employee_id, position_id, department_id, start_date | 同一社員・役職・部署・開始日の重複防止 |
| fk_employee | FOREIGN KEY | employee_id | MST_Employee.employee_id |
| fk_position | FOREIGN KEY | position_id | MST_Position.position_id |
| fk_department | FOREIGN KEY | department_id | MST_Department.department_id |
| fk_acting_for | FOREIGN KEY | acting_for_employee_id | MST_Employee.employee_id |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_approved_by | FOREIGN KEY | approved_by | MST_UserAuth.user_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_appointment_type | CHECK | appointment_type | appointment_type IN ('PRIMARY', 'CONCURRENT', 'TEMPORARY', 'ACTING') |
| chk_approval_limit | CHECK | approval_limit | approval_limit IS NULL OR approval_limit >= 0 |
| chk_end_date | CHECK | end_date | end_date IS NULL OR end_date >= start_date |
| chk_approval_status | CHECK | approval_status | approval_status IN ('PENDING', 'APPROVED', 'REJECTED', 'CANCELLED') |
| chk_acting_consistency | CHECK | acting_for_employee_id | (is_acting = FALSE AND acting_for_employee_id IS NULL) OR (is_acting = TRUE AND acting_for_employee_id IS NOT NULL) |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Employee | employee_id | 1:N | 任命対象社員 |
| MST_Position | position_id | 1:N | 任命役職 |
| MST_Department | department_id | 1:N | 対象部署 |
| MST_Employee | acting_for_employee_id | 1:N | 代理対象社員 |
| MST_Tenant | tenant_id | 1:N | テナント情報 |
| MST_UserAuth | approved_by, created_by, updated_by | 1:N | 承認者・作成者・更新者 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| TRN_ApprovalHistory | appointment_id | 1:N | 承認履歴 |
| TRN_AuthorityLog | appointment_id | 1:N | 権限行使ログ |

## 5. データ仕様

### 5.1 任命種別定義
| 任命種別 | 説明 | 用途 |
|----------|------|------|
| PRIMARY | 主務役職 | メインの役職 |
| CONCURRENT | 兼務役職 | サブの役職 |
| TEMPORARY | 一時役職 | 期間限定の役職 |
| ACTING | 代理役職 | 他者の代理としての役職 |

### 5.2 承認状況定義
| 承認状況 | 説明 | 次の状態 |
|----------|------|----------|
| PENDING | 承認待ち | APPROVED, REJECTED |
| APPROVED | 承認済み | CANCELLED |
| REJECTED | 却下 | PENDING（再申請） |
| CANCELLED | 取消 | - |

### 5.3 データ例
```sql
-- 主務役職任命
INSERT INTO MST_EmployeePosition (
    appointment_id, employee_id, position_id, department_id,
    appointment_type, responsibility_scope, start_date,
    approval_limit, approval_status, approved_by,
    tenant_id, created_by, updated_by
) VALUES (
    'APPOINT_001',
    'EMP_001',
    'POS_001',
    'DEPT_001',
    'PRIMARY',
    'システム開発部全体の管理・運営',
    '2023-04-01',
    5000000.00,
    'APPROVED',
    'USER_001',
    'TENANT_001',
    'system',
    'system'
);

-- 兼務役職任命
INSERT INTO MST_EmployeePosition (
    appointment_id, employee_id, position_id, department_id,
    appointment_type, responsibility_scope, start_date,
    approval_limit, approval_status, approved_by,
    tenant_id, created_by, updated_by
) VALUES (
    'APPOINT_002',
    'EMP_001',
    'POS_002',
    'DEPT_002',
    'CONCURRENT',
    'プロジェクト管理業務',
    '2023-06-01',
    1000000.00,
    'APPROVED',
    'USER_001',
    'TENANT_001',
    'system',
    'system'
);

-- 代理役職任命
INSERT INTO MST_EmployeePosition (
    appointment_id, employee_id, position_id, department_id,
    appointment_type, responsibility_scope, start_date, end_date,
    is_acting, acting_for_employee_id, approval_status,
    approved_by, tenant_id, created_by, updated_by
) VALUES (
    'APPOINT_003',
    'EMP_003',
    'POS_001',
    'DEPT_001',
    'ACTING',
    '部長代理業務',
    '2023-08-01',
    '2023-08-31',
    TRUE,
    'EMP_001',
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
| 初期データ件数 | 1,200件 | 既存社員の主務役職 |
| 年間増加件数 | 400件 | 兼務・昇進・新規任命 |
| 5年後想定件数 | 3,200件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：RANGE
- パーティション条件：start_date（年単位）

### 6.3 アーカイブ
- アーカイブ条件：任命終了から3年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | employee_id, is_active | 社員の有効役職一覧 |
| SELECT | 高 | department_id, is_active | 部署の役職者一覧 |
| SELECT | 中 | position_id | 役職別任命者一覧 |
| SELECT | 中 | appointment_type | 任命種別検索 |
| SELECT | 中 | start_date, end_date | 期間指定検索 |
| INSERT | 中 | - | 新規役職任命 |
| UPDATE | 中 | appointment_id | 任命情報更新 |

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
| exec_admin | ○ | ○ | ○ | × | 役員管理者 |
| dept_manager | ○ | × | × | × | 部署管理者（自部署のみ） |
| manager | ○ | × | × | × | 管理職 |
| employee | ○ | × | × | × | 一般社員（自分のみ） |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含む（役職情報）
- 機密情報：含む（組織情報、権限情報）
- 暗号化：必要（委任権限、任命理由、備考）

## 9. 移行仕様

### 9.1 データ移行
- 移行元：MST_Employee（既存の主務役職情報）
- 移行方法：SQLスクリプト実行
- 移行タイミング：システム移行時

### 9.2 移行スクリプト例
```sql
-- 既存の主務役職データを移行
INSERT INTO MST_EmployeePosition (
    appointment_id, employee_id, position_id, department_id,
    appointment_type, start_date, approval_status,
    tenant_id, created_by, updated_by
)
SELECT 
    CONCAT('APPOINT_', LPAD(ROW_NUMBER() OVER (ORDER BY employee_id), 6, '0')),
    employee_id,
    position_id,
    department_id,
    'PRIMARY',
    hire_date,
    'APPROVED',
    tenant_id,
    'migration',
    'migration'
FROM MST_Employee
WHERE is_active = TRUE;
```

### 9.3 DDL
```sql
CREATE TABLE MST_EmployeePosition (
    appointment_id VARCHAR(20) NOT NULL,
    employee_id VARCHAR(20) NOT NULL,
    position_id VARCHAR(20) NOT NULL,
    department_id VARCHAR(20) NOT NULL,
    appointment_type VARCHAR(20) NOT NULL DEFAULT 'PRIMARY',
    responsibility_scope VARCHAR(100) NULL,
    start_date DATE NOT NULL,
    end_date DATE NULL,
    appointment_reason VARCHAR(100) NULL,
    delegation_authority TEXT NULL,
    approval_limit DECIMAL(15,2) NULL,
    is_acting BOOLEAN NOT NULL DEFAULT FALSE,
    acting_for_employee_id VARCHAR(20) NULL,
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
    PRIMARY KEY (appointment_id),
    UNIQUE KEY idx_emp_pos_dept_date (employee_id, position_id, department_id, start_date),
    INDEX idx_employee (employee_id),
    INDEX idx_position (position_id),
    INDEX idx_department (department_id),
    INDEX idx_appointment_type (appointment_type),
    INDEX idx_period (start_date, end_date),
    INDEX idx_active (is_active),
    INDEX idx_tenant (tenant_id),
    INDEX idx_acting (is_acting),
    INDEX idx_acting_for (acting_for_employee_id),
    INDEX idx_approval (approval_status),
    CONSTRAINT fk_emp_pos_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(employee_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_emp_pos_position FOREIGN KEY (position_id) REFERENCES MST_Position(position_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_emp_pos_department FOREIGN KEY (department_id) REFERENCES MST_Department(department_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_emp_pos_acting_for FOREIGN KEY (acting_for_employee_id) REFERENCES MST_Employee(employee_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_emp_pos_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_emp_pos_approved_by FOREIGN KEY (approved_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_emp_pos_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_emp_pos_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_emp_pos_appointment_type CHECK (appointment_type IN ('PRIMARY', 'CONCURRENT', 'TEMPORARY', 'ACTING')),
    CONSTRAINT chk_emp_pos_approval_limit CHECK (approval_limit IS NULL OR approval_limit >= 0),
    CONSTRAINT chk_emp_pos_end_date CHECK (end_date IS NULL OR end_date >= start_date),
    CONSTRAINT chk_emp_pos_approval_status CHECK (approval_status IN ('PENDING', 'APPROVED', 'REJECTED', 'CANCELLED')),
    CONSTRAINT chk_emp_pos_acting_consistency CHECK ((is_acting = FALSE AND acting_for_employee_id IS NULL) OR (is_acting = TRUE AND acting_for_employee_id IS NOT NULL))
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

1. **主務・兼務の管理**: appointment_typeにより主務（PRIMARY）と兼務（CONCURRENT）を区別
2. **部署別役職**: department_idにより同一役職でも部署別に管理
3. **責任範囲管理**: responsibility_scopeにより役職の担当領域を明確化
4. **委任権限**: delegation_authorityにより具体的な権限内容を記録
5. **承認限度額**: approval_limitにより役職別の承認権限を設定
6. **代理機能**: is_acting、acting_for_employee_idにより代理役職を管理
7. **承認ワークフロー**: approval_statusにより任命の承認プロセスを管理
8. **履歴管理**: 任命期間（start_date, end_date）により履歴を管理
9. **パーティション設計**: 年単位でのパーティションにより大量データに対応
10. **既存システム連携**: MST_Employeeの主務役職情報との整合性を保持
11. **一時任命対応**: TEMPORARY、ACTINGにより特殊な任命パターンに対応
12. **監査対応**: 作成者・更新者・承認者の記録により監査要件に対応

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-31 | システムアーキテクト | 初版作成（主務・兼務機能対応） |
