# テーブル定義書：社員基本情報 (MST_Employee)

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-006 |
| **テーブル名** | MST_Employee |
| **論理名** | 社員基本情報 |
| **カテゴリ** | マスタ系 |
| **優先度** | 最高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-05-29 |
| **最終更新日** | 2025-05-31 |

## 2. テーブル概要

### 2.1 概要・目的
社員基本情報テーブル（MST_Employee）は、システムを利用する社員の基本的な個人情報を管理します。人事システムとの連携により、組織情報、役職情報、入退社情報などを一元管理し、スキル管理システムの基盤となります。

### 2.2 関連API
- [API-005](../api/specs/API仕様書_API-005.md) - 社員情報管理API
- [API-006](../api/specs/API仕様書_API-006.md) - 組織情報管理API

### 2.3 関連バッチ
- [BATCH-004](../batch/specs/バッチ定義書_BATCH-004.md) - 社員情報同期バッチ
- [BATCH-015](../batch/specs/バッチ定義書_BATCH-015.md) - マスタデータ同期バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | employee_id | 社員ID | VARCHAR | 20 | × | ○ | - | - | 社員を一意に識別するID |
| 2 | employee_number | 社員番号 | VARCHAR | 10 | × | - | - | - | 人事システムの社員番号 |
| 3 | last_name | 姓 | VARCHAR | 50 | × | - | - | - | 社員の姓 |
| 4 | first_name | 名 | VARCHAR | 50 | × | - | - | - | 社員の名 |
| 5 | last_name_kana | 姓（カナ） | VARCHAR | 50 | ○ | - | - | NULL | 社員の姓（カタカナ） |
| 6 | first_name_kana | 名（カナ） | VARCHAR | 50 | ○ | - | - | NULL | 社員の名（カタカナ） |
| 7 | email | メールアドレス | VARCHAR | 255 | × | - | - | - | 社員のメールアドレス |
| 8 | phone_number | 電話番号 | VARCHAR | 20 | ○ | - | - | NULL | 社員の電話番号 |
| 9 | department_id | 部署ID | VARCHAR | 20 | × | - | ○ | - | 所属部署のID |
| 10 | position_id | 役職ID | VARCHAR | 20 | × | - | ○ | - | 役職のID |
| 11 | manager_id | 上司ID | VARCHAR | 20 | ○ | - | ○ | NULL | 直属の上司の社員ID |
| 12 | hire_date | 入社日 | DATE | - | × | - | - | - | 入社年月日 |
| 13 | resignation_date | 退職日 | DATE | - | ○ | - | - | NULL | 退職年月日 |
| 14 | employment_status | 雇用形態 | VARCHAR | 20 | × | - | - | 'REGULAR' | 雇用形態（正社員/契約社員等） |
| 15 | work_location | 勤務地 | VARCHAR | 100 | ○ | - | - | NULL | 主な勤務地 |
| 16 | profile_image_url | プロフィール画像URL | VARCHAR | 500 | ○ | - | - | NULL | プロフィール画像のURL |
| 17 | self_introduction | 自己紹介 | TEXT | - | ○ | - | - | NULL | 自己紹介文 |
| 18 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | 所属テナントのID |
| 19 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | 社員が有効かどうか |
| 20 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 21 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 22 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 23 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | employee_id | 主キー |
| idx_employee_number | UNIQUE | employee_number, tenant_id | 社員番号の一意性を保証（テナント内） |
| idx_email | UNIQUE | email | メールアドレスの一意性を保証 |
| idx_department | INDEX | department_id | 部署検索用 |
| idx_position | INDEX | position_id | 役職検索用 |
| idx_manager | INDEX | manager_id | 上司検索用 |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_name | INDEX | last_name, first_name | 氏名検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |
| idx_hire_date | INDEX | hire_date | 入社日検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_employee | PRIMARY KEY | employee_id | 主キー制約 |
| uq_employee_number | UNIQUE | employee_number, tenant_id | 社員番号の一意性を保証（テナント内） |
| uq_email | UNIQUE | email | メールアドレスの一意性を保証 |
| fk_department | FOREIGN KEY | department_id | MST_Department.department_id |
| fk_position | FOREIGN KEY | position_id | MST_Position.position_id |
| fk_manager | FOREIGN KEY | manager_id | MST_Employee.employee_id |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_employment_status | CHECK | employment_status | employment_status IN ('REGULAR', 'CONTRACT', 'PART_TIME', 'TEMPORARY', 'INTERN') |
| chk_resignation_date | CHECK | resignation_date | resignation_date IS NULL OR resignation_date >= hire_date |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Department | department_id | 1:N | 部署情報 |
| MST_Position | position_id | 1:N | 役職情報 |
| MST_Employee | manager_id | 1:N | 上司（自己参照） |
| MST_Tenant | tenant_id | 1:N | テナント情報 |
| MST_UserAuth | created_by, updated_by | 1:N | 作成者・更新者 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_UserAuth | employee_id | 1:1 | ユーザー認証情報 |
| TRN_SkillRecord | employee_id | 1:N | スキル情報 |
| TRN_GoalProgress | employee_id | 1:N | 目標進捗 |
| TRN_ProjectRecord | employee_id | 1:N | 案件実績 |
| TRN_TrainingHistory | employee_id | 1:N | 研修参加履歴 |
| MST_Employee | manager_id | 1:N | 部下（自己参照） |

## 5. データ仕様

### 5.1 データ例
```sql
INSERT INTO MST_Employee (
    employee_id, employee_number, last_name, first_name,
    last_name_kana, first_name_kana, email, phone_number,
    department_id, position_id, manager_id, hire_date,
    employment_status, work_location, tenant_id,
    created_by, updated_by
) VALUES (
    'EMP_001',
    '12345',
    '田中',
    '太郎',
    'タナカ',
    'タロウ',
    'tanaka.taro@company.com',
    '090-1234-5678',
    'DEPT_001',
    'POS_001',
    'EMP_002',
    '2023-04-01',
    'REGULAR',
    '東京本社',
    'TENANT_001',
    'system',
    'system'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 1,000件 | 既存社員データ |
| 年間増加件数 | 200件 | 新入社員・中途採用 |
| 5年後想定件数 | 2,000件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：なし
- パーティション条件：-

### 6.3 アーカイブ
- アーカイブ条件：退職から3年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | employee_id | 社員情報取得 |
| SELECT | 高 | department_id | 部署別社員一覧 |
| SELECT | 中 | last_name, first_name | 氏名検索 |
| SELECT | 中 | manager_id | 部下一覧取得 |
| UPDATE | 中 | employee_id | 社員情報更新 |
| INSERT | 低 | - | 新規社員登録 |

### 7.2 パフォーマンス要件
- SELECT：10ms以内
- INSERT：50ms以内
- UPDATE：50ms以内
- DELETE：50ms以内

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| hr_admin | ○ | ○ | ○ | × | 人事管理者 |
| manager | ○ | × | ○ | × | 管理職（部下のみ） |
| employee | ○ | × | ○ | × | 一般社員（自分のみ） |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含む（氏名、メールアドレス、電話番号）
- 機密情報：含む（組織情報、雇用情報）
- 暗号化：必要（個人情報項目）

## 9. 移行仕様

### 9.1 データ移行
- 移行元：人事システム
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
CREATE TABLE MST_Employee (
    employee_id VARCHAR(20) NOT NULL,
    employee_number VARCHAR(10) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name_kana VARCHAR(50) NULL,
    first_name_kana VARCHAR(50) NULL,
    email VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NULL,
    department_id VARCHAR(20) NOT NULL,
    position_id VARCHAR(20) NOT NULL,
    manager_id VARCHAR(20) NULL,
    hire_date DATE NOT NULL,
    resignation_date DATE NULL,
    employment_status VARCHAR(20) NOT NULL DEFAULT 'REGULAR',
    work_location VARCHAR(100) NULL,
    profile_image_url VARCHAR(500) NULL,
    self_introduction TEXT NULL,
    tenant_id VARCHAR(50) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL,
    PRIMARY KEY (employee_id),
    UNIQUE KEY idx_employee_number (employee_number, tenant_id),
    UNIQUE KEY idx_email (email),
    INDEX idx_department (department_id),
    INDEX idx_position (position_id),
    INDEX idx_manager (manager_id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_name (last_name, first_name),
    INDEX idx_active (is_active),
    INDEX idx_hire_date (hire_date),
    CONSTRAINT fk_employee_department FOREIGN KEY (department_id) REFERENCES MST_Department(department_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_employee_position FOREIGN KEY (position_id) REFERENCES MST_Position(position_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_employee_manager FOREIGN KEY (manager_id) REFERENCES MST_Employee(employee_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_employee_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_employee_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_employee_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_employee_employment_status CHECK (employment_status IN ('REGULAR', 'CONTRACT', 'PART_TIME', 'TEMPORARY', 'INTERN')),
    CONSTRAINT chk_employee_resignation_date CHECK (resignation_date IS NULL OR resignation_date >= hire_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 10. 特記事項

1. 個人情報保護法に基づく適切な管理が必要
2. 人事システムとの定期同期により最新情報を維持
3. 退職者情報は論理削除（is_active=FALSE）で管理
4. 上司部下関係は自己参照により表現
5. メールアドレスは全システム内で一意
6. プロフィール画像は外部ストレージに保存し、URLのみ管理
7. 雇用形態により利用可能機能を制限する場合がある

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-29 | システムアーキテクト | 初版作成 |
| 1.1 | 2025-05-31 | システムアーキテクト | 新フォーマットに変更、詳細情報追加 |
