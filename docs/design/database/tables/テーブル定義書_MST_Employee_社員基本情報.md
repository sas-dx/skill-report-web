# テーブル定義書: MST_Employee

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_Employee |
| 論理名 | 社員基本情報 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 17:21:48 |

## 概要

組織に所属する全社員の基本的な個人情報と組織情報を一元管理するマスタテーブル。
主な目的：
- 社員の基本情報（氏名、連絡先、入社日等）の管理
- 組織構造（部署、役職、上司関係）の管理
- 認証・権限管理のためのユーザー情報提供
- 人事システムとの連携データ基盤
このテーブルは年間スキル報告書システムの中核となるマスタデータであり、
スキル管理、目標管理、作業実績管理の全ての機能で参照される。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| employee_code | 社員番号 | VARCHAR | 30 | × |  | 社員番号（例：EMP000001） |
| full_name | 氏名 | VARCHAR | 100 | × |  | 氏名（暗号化対象） |
| full_name_kana | 氏名カナ | VARCHAR | 100 | × |  | 氏名カナ（暗号化対象） |
| email | メールアドレス | VARCHAR | 255 | × |  | メールアドレス（ログイン認証用） |
| phone | 電話番号 | VARCHAR | 20 | ○ |  | 電話番号（暗号化対象） |
| hire_date | 入社日 | DATE |  | × |  | 入社日 |
| birth_date | 生年月日 | DATE |  | ○ |  | 生年月日（暗号化対象） |
| gender | 性別 | VARCHAR | 1 | ○ |  | 性別（M:男性、F:女性、O:その他） |
| department_id | 所属部署ID | VARCHAR | 50 | × |  | 所属部署ID |
| position_id | 役職ID | VARCHAR | 50 | ○ |  | 役職ID |
| job_type_id | 職種ID | VARCHAR | 50 | ○ |  | 職種ID |
| employment_status | 雇用形態 | VARCHAR | 20 | × | FULL_TIME | 雇用形態（FULL_TIME:正社員、PART_TIME:パート、CONTRACT:契約社員） |
| manager_id | 直属の上司ID | VARCHAR | 50 | ○ |  | 直属の上司ID（自己参照） |
| employee_status | 在籍状況 | VARCHAR | 20 | × | ACTIVE | 在籍状況（ACTIVE:在籍、RETIRED:退職、SUSPENDED:休職） |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |

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
| fk_employee_department | None | None | None | CASCADE | RESTRICT |  |
| fk_employee_position | None | None | None | CASCADE | SET NULL |  |
| fk_employee_job_type | None | None | None | CASCADE | SET NULL |  |
| fk_employee_manager | None | None | None | CASCADE | SET NULL |  |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_mst_employee | PRIMARY KEY | id | 主キー制約 |
| uk_employee_code | UNIQUE |  | employee_code一意制約 |
| uk_email | UNIQUE |  | email一意制約 |
| chk_job_type_id | CHECK | job_type_id IN (...) | job_type_id値チェック制約 |
| chk_employment_status | CHECK | employment_status IN (...) | employment_status値チェック制約 |
| chk_employee_status | CHECK | employee_status IN (...) | employee_status値チェック制約 |

## サンプルデータ

| id | employee_code | full_name | full_name_kana | email | phone | hire_date | birth_date | gender | department_id | position_id | job_type_id | employment_status | manager_id | employee_status | is_deleted |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| emp_001 | EMP000001 | 山田太郎 | ヤマダタロウ | yamada.taro@example.com | 090-1234-5678 | 2020-04-01 | 1990-01-15 | M | dept_001 | pos_003 | job_001 | FULL_TIME | emp_002 | ACTIVE | False |
| emp_002 | EMP000002 | 佐藤花子 | サトウハナコ | sato.hanako@example.com | 090-2345-6789 | 2018-04-01 | 1985-03-20 | F | dept_001 | pos_002 | job_001 | FULL_TIME | None | ACTIVE | False |

## 特記事項

- 個人情報（氏名、氏名カナ、電話番号、生年月日）は暗号化対象
- 論理削除は is_deleted フラグで管理
- manager_idによる自己参照で組織階層を表現
- 人事システムとの連携でマスタデータを同期
- 認証・権限管理システムの基盤テーブル
- スキル管理・目標管理・作業実績管理の全機能で参照される

## 業務ルール

- 社員番号（employee_code）は一意で変更不可
- メールアドレス（email）は認証用のため一意制約必須
- 在籍状況（employee_status）がRETIREDの場合、論理削除フラグをtrueに設定
- 直属の上司（manager_id）は同一部署内の上位役職者のみ設定可能
- 雇用形態（employment_status）に応じた権限・機能制限を適用
- 個人情報の暗号化は法的要件に基づく必須対応
- 監査証跡として作成日時・更新日時は自動設定

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - MST_Employeeテーブルの詳細定義 |
| 1.1.0 | 2025-06-12 | 開発チーム | カラム追加 - manager_id, job_type_idを追加 |