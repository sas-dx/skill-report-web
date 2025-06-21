# テーブル定義書_MST_Employee_社員基本情報

## テーブル情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_Employee |
| 論理名 | 社員基本情報 |
| カテゴリ | マスタ系 |
| 優先度 | 最高 |
| 要求仕様ID | PRO.1-BASE.1 |

## カラム定義

| カラム名 | データ型 | NULL許可 | 主キー | デフォルト値 | 説明 | 要求仕様ID |
|----------|----------|----------|--------|--------------|------|-------------|
| id | VARCHAR(50) | NO | YES | - | プライマリキー（UUID） | PLT.1-WEB.1 |
| employee_code | VARCHAR(30) | NO | NO | - | 社員番号（例：EMP000001） | PRO.1-BASE.1 |
| full_name | VARCHAR(100) | NO | NO | - | 氏名（暗号化対象） | PRO.1-BASE.1 |
| full_name_kana | VARCHAR(100) | NO | NO | - | 氏名カナ（暗号化対象） | PRO.1-BASE.1 |
| email | VARCHAR(255) | NO | NO | - | メールアドレス（ログイン認証用） | ACC.1-AUTH.1 |
| phone | VARCHAR(20) | YES | NO | - | 電話番号（暗号化対象） | PRO.1-BASE.1 |
| hire_date | DATE | NO | NO | - | 入社日 | PRO.1-BASE.1 |
| birth_date | DATE | YES | NO | - | 生年月日（暗号化対象） | PRO.1-BASE.1 |
| gender | VARCHAR(1) | YES | NO | - | 性別（M:男性、F:女性、O:その他） | PRO.1-BASE.1 |
| department_id | VARCHAR(50) | NO | NO | - | 所属部署ID | PRO.1-BASE.1 |
| position_id | VARCHAR(50) | YES | NO | - | 役職ID | PRO.1-BASE.1 |
| job_type_id | VARCHAR(50) | YES | NO | - | 職種ID | PRO.1-BASE.1 |
| employment_status | VARCHAR(20) | NO | NO | FULL_TIME | 雇用形態（FULL_TIME:正社員、PART_TIME:パート、CONTRACT:契約社員） | PRO.1-BASE.1 |
| manager_id | VARCHAR(50) | YES | NO | - | 直属の上司ID（自己参照） | PRO.1-BASE.1 |
| employee_status | VARCHAR(20) | NO | NO | ACTIVE | 在籍状況（ACTIVE:在籍、RETIRED:退職、SUSPENDED:休職） | PRO.1-BASE.1 |
| created_at | TIMESTAMP | NO | NO | CURRENT_TIMESTAMP | 作成日時 | PLT.1-WEB.1 |
| updated_at | TIMESTAMP | NO | NO | CURRENT_TIMESTAMP | 更新日時 | PLT.1-WEB.1 |
| is_deleted | BOOLEAN | NO | NO | - | 論理削除フラグ | PLT.1-WEB.1 |

## インデックス定義

| インデックス名 | 対象カラム | ユニーク | 説明 |
|----------------|------------|----------|------|
| idx_employee_code | employee_code | YES | 社員番号検索用（一意） |
| idx_email | email | YES | メールアドレス検索用（一意） |
| idx_department | department_id | NO | 部署別検索用 |
| idx_manager | manager_id | NO | 上司別検索用 |
| idx_status | employee_status | NO | 在籍状況別検索用 |
| idx_hire_date | hire_date | NO | 入社日検索用 |

## 外部キー定義

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 |
|------------|--------|--------------|------------|--------|--------|
| fk_employee_department | department_id | MST_Department | id | CASCADE | RESTRICT |
| fk_employee_position | position_id | MST_Position | id | CASCADE | SET NULL |
| fk_employee_job_type | job_type_id | MST_JobType | id | CASCADE | SET NULL |
| fk_employee_manager | manager_id | MST_Employee | id | CASCADE | SET NULL |

---
生成日時: 2025-06-21 13:04:10
