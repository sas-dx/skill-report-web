# テーブル定義書：MST_Employee（社員基本情報）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-006 |
| **テーブル名** | MST_Employee |
| **論理名** | 社員基本情報 |
| **カテゴリ** | マスタ系 |
| **機能カテゴリ** | プロフィール管理 |
| **優先度** | 最高 |
| **個人情報含有** | あり |
| **機密情報レベル** | 高 |
| **暗号化要否** | 要 |
| **ステータス** | 運用中 |
| **作成日** | 2025-06-01 |
| **最終更新日** | 2025-06-01 |

## 2. テーブル概要

### 2.1 概要・目的
SCR-PROFILE

### 2.2 特記事項
- 個人情報保護法に基づき氏名・氏名カナ・電話番号・生年月日は暗号化必須
- 社員番号は人事システムとの連携キーとして使用
- メールアドレスは認証システムのユーザーIDとして使用
- 上司IDは組織階層の管理に使用（自己参照）
- 在籍状況により論理削除を実現（物理削除は行わない）
- 部署・役職・職種の変更履歴は別途履歴テーブルで管理

### 2.3 関連API
API-005

### 2.4 関連バッチ
BATCH-004

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
| 8 | employee_code | 社員番号 | VARCHAR | 20 | ○ | - | - | - | 社員を一意に識別する番号（例：EMP000001） |
| 9 | full_name | 氏名 | VARCHAR | 100 | ○ | - | - | - | 社員の氏名（個人情報のため暗号化対象） |
| 10 | full_name_kana | 氏名カナ | VARCHAR | 100 | ○ | - | - | - | 社員の氏名カナ（個人情報のため暗号化対象） |
| 11 | email | メールアドレス | VARCHAR | 255 | ○ | - | - | - | 社員のメールアドレス（ログイン認証に使用） |
| 12 | phone | 電話番号 | VARCHAR | 20 | ○ | - | - | - | 社員の電話番号（個人情報のため暗号化対象） |
| 13 | hire_date | 入社日 | DATE | None | ○ | - | - | - | 社員の入社日 |
| 14 | birth_date | 生年月日 | DATE | None | ○ | - | - | - | 社員の生年月日（個人情報のため暗号化対象） |
| 15 | gender | 性別 | ENUM | None | ○ | - | - | - | 性別（M:男性、F:女性、O:その他） |
| 16 | department_id | 部署ID | VARCHAR | 50 | ○ | - | ○ | - | 所属部署のID（MST_Departmentへの外部キー） |
| 17 | position_id | 役職ID | VARCHAR | 50 | ○ | - | ○ | - | 役職のID（MST_Positionへの外部キー） |
| 18 | job_type_id | 職種ID | VARCHAR | 50 | ○ | - | ○ | - | 職種のID（MST_JobTypeへの外部キー） |
| 19 | employment_status | 雇用形態 | ENUM | None | ○ | - | - | FULL_TIME | 雇用形態（FULL_TIME:正社員、PART_TIME:パート、CONTRACT:契約社員） |
| 20 | manager_id | 上司ID | VARCHAR | 50 | ○ | - | ○ | - | 直属の上司のID（MST_Employeeへの自己参照外部キー） |
| 21 | employee_status | 在籍状況 | ENUM | None | ○ | - | - | ACTIVE | 在籍状況（ACTIVE:在籍、RETIRED:退職、SUSPENDED:休職） |


### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | id | 主キー |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |
| idx_created_at | INDEX | created_at | 作成日時検索用 |
| idx_employee_code | UNIQUE INDEX | employee_code | 社員番号検索用（一意） |
| idx_email | UNIQUE INDEX | email | メールアドレス検索用（一意） |
| idx_department | INDEX | department_id | 部署別検索用 |
| idx_manager | INDEX | manager_id | 上司別検索用 |
| idx_status | INDEX | employee_status | 在籍状況別検索用 |
| idx_hire_date | INDEX | hire_date | 入社日検索用 |


### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_mst_employee | PRIMARY KEY | id | 主キー制約 |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| uk_employee_code | UNIQUE | employee_code | ['employee_code'] |
| uk_email | UNIQUE | email | ['email'] |
| chk_gender | CHECK |  | gender IN ('M', 'F', 'O') |
| chk_employment_status | CHECK |  | employment_status IN ('FULL_TIME', 'PART_TIME', 'CONTRACT') |
| chk_employee_status | CHECK |  | employee_status IN ('ACTIVE', 'RETIRED', 'SUSPENDED') |


## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_UserAuth | created_by, updated_by | 1:N | ユーザー情報 |
| MST_Department | department_id | 1:N | 部署への外部キー |
| MST_Position | position_id | 1:N | 役職への外部キー |
| MST_JobType | job_type_id | 1:N | 職種への外部キー |
| MST_Employee | manager_id | 1:N | 上司への自己参照外部キー |


### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| - | - | - | 必要に応じて追加 |

## 5. データ仕様

### 5.1 データ例
```sql
-- サンプルデータ
INSERT INTO MST_Employee (
    id, tenant_id, employee_code, full_name, full_name_kana, email, phone, hire_date, birth_date, gender, department_id, position_id, job_type_id, employment_status, manager_id, employee_status, created_by, updated_by
) VALUES (
    'sample_001', 'tenant_001', 'EMP000001', '山田太郎', 'ヤマダタロウ', 'yamada.taro@company.com', '090-1234-5678', '2020-04-01', '1990-01-15', 'M', 'DEPT001', 'POS001', 'JOB001', 'FULL_TIME', NULL, 'ACTIVE', 'user_admin', 'user_admin'
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
- 個人情報：あり
- 機密情報：高レベル
- 暗号化：要

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存システム
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
-- 社員基本情報テーブル作成DDL
CREATE TABLE MST_Employee (
    id VARCHAR(50) NOT NULL COMMENT 'ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '有効フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT '作成者ID',
    updated_by VARCHAR(50) NOT NULL COMMENT '更新者ID',
    employee_code VARCHAR(20) COMMENT '社員番号',
    full_name VARCHAR(100) COMMENT '氏名',
    full_name_kana VARCHAR(100) COMMENT '氏名カナ',
    email VARCHAR(255) COMMENT 'メールアドレス',
    phone VARCHAR(20) COMMENT '電話番号',
    hire_date DATE COMMENT '入社日',
    birth_date DATE COMMENT '生年月日',
    gender ENUM COMMENT '性別',
    department_id VARCHAR(50) COMMENT '部署ID',
    position_id VARCHAR(50) COMMENT '役職ID',
    job_type_id VARCHAR(50) COMMENT '職種ID',
    employment_status ENUM DEFAULT FULL_TIME COMMENT '雇用形態',
    manager_id VARCHAR(50) COMMENT '上司ID',
    employee_status ENUM DEFAULT ACTIVE COMMENT '在籍状況',
    PRIMARY KEY (id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_active (is_active),
    INDEX idx_created_at (created_at),
    UNIQUE INDEX idx_employee_code (employee_code),
    UNIQUE INDEX idx_email (email),
    INDEX idx_department (department_id),
    INDEX idx_manager (manager_id),
    INDEX idx_status (employee_status),
    INDEX idx_hire_date (hire_date),
    CONSTRAINT fk_employee_department FOREIGN KEY (department_id) REFERENCES MST_Department(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_employee_position FOREIGN KEY (position_id) REFERENCES MST_Position(id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_employee_job_type FOREIGN KEY (job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_employee_manager FOREIGN KEY (manager_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='社員基本情報';

```

## 10. 特記事項

1. **設計方針**
   - マスタ系として設計
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

- 社員番号は入社時に自動採番（EMP + 6桁連番）
- メールアドレスは会社ドメイン必須
- 退職時は employee_status を RETIRED に変更
- 休職時は employee_status を SUSPENDED に変更
- 上司は同一部署または上位部署の社員のみ設定可能
