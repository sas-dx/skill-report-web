# テーブル定義書: MST_Employee

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_Employee |
| 論理名 | 社員基本情報 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-04 06:53:39 |

## 概要

MST_Employee（社員基本情報）は、組織に所属する全社員の基本的な個人情報と組織情報を一元管理するマスタテーブルです。

主な目的：
- 社員の基本プロフィール情報（氏名、連絡先、入社日等）の管理
- 組織階層（部署、役職、上司関係）の管理
- 認証システムとの連携（メールアドレスによるログイン）
- 人事システムとの連携（社員番号による突合）
- 個人情報保護法に準拠したセキュアなデータ管理

このテーブルは、スキル管理、目標管理、評価管理など、システム全体の基盤となる重要なマスタデータです。



## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| employee_code | 社員番号 | VARCHAR | 30 | ○ |  | 社員を一意に識別する番号（例：EMP000001、現行システムからの移行番号も対応） |
| full_name | 氏名 | VARCHAR | 100 | ○ |  | 社員の氏名（個人情報のため暗号化対象） |
| full_name_kana | 氏名カナ | VARCHAR | 100 | ○ |  | 社員の氏名カナ（個人情報のため暗号化対象） |
| email | メールアドレス | VARCHAR | 255 | ○ |  | 社員のメールアドレス（ログイン認証に使用） |
| phone | 電話番号 | VARCHAR | 20 | ○ |  | 社員の電話番号（個人情報のため暗号化対象） |
| hire_date | 入社日 | DATE |  | ○ |  | 社員の入社日 |
| birth_date | 生年月日 | DATE |  | ○ |  | 社員の生年月日（個人情報のため暗号化対象） |
| gender | 性別 | ENUM |  | ○ |  | 性別（M:男性、F:女性、O:その他） |
| department_id | 部署ID | VARCHAR | 50 | ○ |  | 所属部署のID（MST_Departmentへの外部キー） |
| position_id | 役職ID | VARCHAR | 50 | ○ |  | 役職のID（MST_Positionへの外部キー） |
| job_type_id | 職種ID | VARCHAR | 50 | ○ |  | 職種のID（MST_JobTypeへの外部キー） |
| employment_status | 雇用形態 | ENUM |  | ○ | FULL_TIME | 雇用形態（FULL_TIME:正社員、PART_TIME:パート、CONTRACT:契約社員） |
| manager_id | 上司ID | VARCHAR | 50 | ○ |  | 直属の上司のID（MST_Employeeへの自己参照外部キー） |
| employee_status | 在籍状況 | ENUM |  | ○ | ACTIVE | 在籍状況（ACTIVE:在籍、RETIRED:退職、SUSPENDED:休職） |
| code | コード | VARCHAR | 20 | × |  | マスタコード |
| name | 名称 | VARCHAR | 100 | × |  | マスタ名称 |
| description | 説明 | TEXT |  | ○ |  | マスタ説明 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_employee_code | employee_code | ○ | 社員番号検索用（一意） |
| idx_email | email | ○ | メールアドレス検索用（一意） |
| idx_department | department_id | × | 部署別検索用 |
| idx_manager | manager_id | × | 上司別検索用 |
| idx_status | employee_status | × | 在籍状況別検索用 |
| idx_hire_date | hire_date | × | 入社日検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_employee_department | department_id | MST_Department | id | CASCADE | RESTRICT | 部署への外部キー |
| fk_employee_position | position_id | MST_Position | id | CASCADE | SET NULL | 役職への外部キー |
| fk_employee_job_type | job_type_id | MST_JobType | id | CASCADE | SET NULL | 職種への外部キー |
| fk_employee_manager | manager_id | MST_Employee | id | CASCADE | SET NULL | 上司への自己参照外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_employee_code | UNIQUE |  | 社員番号一意制約 |
| uk_email | UNIQUE |  | メールアドレス一意制約 |
| chk_gender | CHECK | gender IN ('M', 'F', 'O') | 性別値チェック制約 |
| chk_employment_status | CHECK | employment_status IN ('FULL_TIME', 'PART_TIME', 'CONTRACT') | 雇用形態値チェック制約 |
| chk_employee_status | CHECK | employee_status IN ('ACTIVE', 'RETIRED', 'SUSPENDED') | 在籍状況値チェック制約 |

## サンプルデータ

| employee_code | full_name | full_name_kana | email | phone | hire_date | birth_date | gender | department_id | position_id | job_type_id | employment_status | manager_id | employee_status |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| EMP000001 | 山田太郎 | ヤマダタロウ | yamada.taro@company.com | 090-1234-5678 | 2020-04-01 | 1990-01-15 | M | DEPT001 | POS001 | JOB001 | FULL_TIME | None | ACTIVE |
| EMP000002 | 佐藤花子 | サトウハナコ | sato.hanako@company.com | 090-2345-6789 | 2021-04-01 | 1992-03-20 | F | DEPT002 | POS002 | JOB002 | FULL_TIME | EMP000001 | ACTIVE |

## 特記事項

- 個人情報保護法に基づき氏名・氏名カナ・電話番号・生年月日は暗号化必須
- 社員番号は人事システムとの連携キーとして使用
- メールアドレスは認証システムのユーザーIDとして使用
- 上司IDは組織階層の管理に使用（自己参照）
- 在籍状況により論理削除を実現（物理削除は行わない）
- 部署・役職・職種の変更履歴は別途履歴テーブルで管理
- 社員番号は30桁まで対応、現行システムからの移行番号も格納可能
- スキルグレード情報は別テーブル（TRN_EmployeeSkillGrade）で管理

## 業務ルール

- 社員番号は入社時に自動採番（EMP + 6桁連番）または現行システムからの移行番号を使用
- 現行システム移行時は既存の社員番号体系をそのまま使用可能
- メールアドレスは会社ドメイン必須
- 退職時は employee_status を RETIRED に変更
- 休職時は employee_status を SUSPENDED に変更
- 上司は同一部署または上位部署の社員のみ設定可能
- スキルグレードは職種ごとに TRN_EmployeeSkillGrade テーブルで管理

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 社員基本情報テーブルの詳細定義 |
| 1.1.0 | 2025-06-01 | 開発チーム | 改版履歴管理機能追加、個人情報暗号化対応強化 |
| 1.2.0 | 2025-06-01 | 開発チーム | 社員番号桁数拡張（20→30桁）、現行システム移行対応、スキルグレード管理の別テーブル化対応 |
