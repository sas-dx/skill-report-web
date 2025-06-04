# MST_Employee

**社員基本情報**

**概要**: 

## テーブル情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_Employee |
| 論理名 | 社員基本情報 |
| 説明 |  |
| 作成日 | 2025-06-04 |

## カラム定義

| No | カラム名 | データ型 | NULL | デフォルト | 説明 |
|----|----------|----------|------|------------|------|
| 1 | employee_code | VARCHAR | ○ |  | 社員を一意に識別する番号（例：EMP000001、現行システムからの移行番号も対応） |
| 2 | full_name | VARCHAR | ○ |  | 社員の氏名（個人情報のため暗号化対象） |
| 3 | full_name_kana | VARCHAR | ○ |  | 社員の氏名カナ（個人情報のため暗号化対象） |
| 4 | email | VARCHAR | ○ |  | 社員のメールアドレス（ログイン認証に使用） |
| 5 | phone | VARCHAR | ○ |  | 社員の電話番号（個人情報のため暗号化対象） |
| 6 | hire_date | DATE | ○ |  | 社員の入社日 |
| 7 | birth_date | DATE | ○ |  | 社員の生年月日（個人情報のため暗号化対象） |
| 8 | gender | ENUM | ○ |  | 性別（M:男性、F:女性、O:その他） |
| 9 | department_id | VARCHAR | ○ |  | 所属部署のID（MST_Departmentへの外部キー） |
| 10 | position_id | VARCHAR | ○ |  | 役職のID（MST_Positionへの外部キー） |
| 11 | job_type_id | VARCHAR | ○ |  | 職種のID（MST_JobTypeへの外部キー） |
| 12 | employment_status | ENUM | ○ | FULL_TIME | 雇用形態（FULL_TIME:正社員、PART_TIME:パート、CONTRACT:契約社員） |
| 13 | manager_id | VARCHAR | ○ |  | 直属の上司のID（MST_Employeeへの自己参照外部キー） |
| 14 | employee_status | ENUM | ○ | ACTIVE | 在籍状況（ACTIVE:在籍、RETIRED:退職、SUSPENDED:休職） |
| 15 | code | VARCHAR | × |  | マスタコード |
| 16 | name | VARCHAR | × |  | マスタ名称 |
| 17 | description | TEXT | ○ |  | マスタ説明 |

## インデックス定義

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_employee_code | employee_code | ○ | 社員番号検索用（一意） |
| idx_email | email | ○ | メールアドレス検索用（一意） |
| idx_department | department_id | × | 部署別検索用 |
| idx_manager | manager_id | × | 上司別検索用 |
| idx_status | employee_status | × | 在籍状況別検索用 |
| idx_hire_date | hire_date | × | 入社日検索用 |

## 外部キー定義

| 制約名 | カラム | 参照テーブル | 参照カラム | 説明 |
|--------|--------|--------------|------------|------|
| fk_employee_department | department_id | MST_Department | id | 部署への外部キー |
| fk_employee_position | position_id | MST_Position | id | 役職への外部キー |
| fk_employee_job_type | job_type_id | MST_JobType | id | 職種への外部キー |
| fk_employee_manager | manager_id | MST_Employee | id | 上司への自己参照外部キー |

## ビジネスルール

1. 社員番号は入社時に自動採番（EMP + 6桁連番）または現行システムからの移行番号を使用
2. 現行システム移行時は既存の社員番号体系をそのまま使用可能
3. メールアドレスは会社ドメイン必須
4. 退職時は employee_status を RETIRED に変更
5. 休職時は employee_status を SUSPENDED に変更
6. 上司は同一部署または上位部署の社員のみ設定可能
7. スキルグレードは職種ごとに TRN_EmployeeSkillGrade テーブルで管理

## 備考

- 個人情報保護法に基づき氏名・氏名カナ・電話番号・生年月日は暗号化必須
- 社員番号は人事システムとの連携キーとして使用
- メールアドレスは認証システムのユーザーIDとして使用
- 上司IDは組織階層の管理に使用（自己参照）
- 在籍状況により論理削除を実現（物理削除は行わない）
- 部署・役職・職種の変更履歴は別途履歴テーブルで管理
- 社員番号は30桁まで対応、現行システムからの移行番号も格納可能
- スキルグレード情報は別テーブル（TRN_EmployeeSkillGrade）で管理
