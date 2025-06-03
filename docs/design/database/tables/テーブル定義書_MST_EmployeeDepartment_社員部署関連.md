# テーブル定義書: MST_EmployeeDepartment

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_EmployeeDepartment |
| 論理名 | 社員部署関連 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-04 06:57:02 |

## 概要

MST_EmployeeDepartment（社員部署関連）は、社員と部署の関連付けを管理するマスタテーブルです。

主な目的：
- 社員の部署所属履歴の管理
- 複数部署兼務の管理
- 部署異動履歴の追跡
- 組織変更時の影響範囲把握
- 部署別人員配置の管理
- 権限管理における部署ベースアクセス制御

このテーブルにより、社員の組織所属状況を詳細に管理し、
人事異動や組織変更の履歴を正確に追跡できます。



## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | 社員のID（MST_Employeeへの外部キー） |
| department_id | 部署ID | VARCHAR | 50 | ○ |  | 部署のID（MST_Departmentへの外部キー） |
| assignment_type | 配属区分 | ENUM |  | ○ | PRIMARY | 配属区分（PRIMARY:主配属、SECONDARY:兼務、TEMPORARY:一時配属） |
| start_date | 配属開始日 | DATE |  | ○ |  | 部署への配属開始日 |
| end_date | 配属終了日 | DATE |  | ○ |  | 部署からの配属終了日（NULL:現在も配属中） |
| assignment_ratio | 配属比率 | DECIMAL | 5,2 | ○ |  | 配属比率（%）兼務時の工数配分用 |
| role_in_department | 部署内役割 | VARCHAR | 100 | ○ |  | 部署内での役割・職責 |
| reporting_manager_id | 報告先上司ID | VARCHAR | 50 | ○ |  | 当該部署での報告先上司ID（MST_Employeeへの外部キー） |
| assignment_reason | 配属理由 | VARCHAR | 500 | ○ |  | 配属・異動の理由 |
| assignment_status | 配属状況 | ENUM |  | ○ | ACTIVE | 配属状況（ACTIVE:有効、INACTIVE:無効、PENDING:保留） |
| approval_status | 承認状況 | ENUM |  | ○ | PENDING | 承認状況（APPROVED:承認済、PENDING:承認待ち、REJECTED:却下） |
| approved_by | 承認者ID | VARCHAR | 50 | ○ |  | 配属を承認した管理者のID |
| approved_at | 承認日時 | TIMESTAMP |  | ○ |  | 配属が承認された日時 |
| code | コード | VARCHAR | 20 | × |  | マスタコード |
| name | 名称 | VARCHAR | 100 | × |  | マスタ名称 |
| description | 説明 | TEXT |  | ○ |  | マスタ説明 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_MST_EmployeeDepartment_employee_id | employee_id | × | 社員ID検索用 |
| idx_MST_EmployeeDepartment_department_id | department_id | × | 部署ID検索用 |
| idx_MST_EmployeeDepartment_employee_department | employee_id, department_id | × | 社員・部署複合検索用 |
| idx_MST_EmployeeDepartment_assignment_type | assignment_type | × | 配属区分別検索用 |
| idx_MST_EmployeeDepartment_start_date | start_date | × | 配属開始日検索用 |
| idx_MST_EmployeeDepartment_end_date | end_date | × | 配属終了日検索用 |
| idx_MST_EmployeeDepartment_status | assignment_status | × | 配属状況別検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_MST_EmployeeDepartment_employee | employee_id | MST_Employee | id | CASCADE | CASCADE | 社員への外部キー |
| fk_MST_EmployeeDepartment_department | department_id | MST_Department | id | CASCADE | CASCADE | 部署への外部キー |
| fk_MST_EmployeeDepartment_reporting_manager | reporting_manager_id | MST_Employee | id | CASCADE | SET NULL | 報告先上司への外部キー |
| fk_MST_EmployeeDepartment_approved_by | approved_by | MST_Employee | id | CASCADE | SET NULL | 承認者への外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_MST_EmployeeDepartment_employee_dept_primary | UNIQUE |  | 社員・部署・配属区分・開始日一意制約 |
| chk_MST_EmployeeDepartment_assignment_type | CHECK | assignment_type IN ('PRIMARY', 'SECONDARY', 'TEMPORARY') | 配属区分値チェック制約 |
| chk_MST_EmployeeDepartment_assignment_status | CHECK | assignment_status IN ('ACTIVE', 'INACTIVE', 'PENDING') | 配属状況値チェック制約 |
| chk_MST_EmployeeDepartment_approval_status | CHECK | approval_status IN ('APPROVED', 'PENDING', 'REJECTED') | 承認状況値チェック制約 |
| chk_MST_EmployeeDepartment_date_range | CHECK | end_date IS NULL OR start_date <= end_date | 日付範囲整合性チェック制約 |
| chk_MST_EmployeeDepartment_assignment_ratio | CHECK | assignment_ratio IS NULL OR (assignment_ratio >= 0 AND assignment_ratio <= 100) | 配属比率範囲チェック制約 |

## サンプルデータ

| employee_id | department_id | assignment_type | start_date | end_date | assignment_ratio | role_in_department | reporting_manager_id | assignment_reason | assignment_status | approval_status | approved_by | approved_at |
|------|------|------|------|------|------|------|------|------|------|------|------|------|
| EMP000001 | DEPT001 | PRIMARY | 2020-04-01 | None | 100.0 | チームリーダー | EMP000010 | 新卒入社時配属 | ACTIVE | APPROVED | EMP000010 | 2020-03-25 10:00:00 |
| EMP000002 | DEPT002 | PRIMARY | 2021-04-01 | None | 80.0 | 開発担当 | EMP000011 | 新卒入社時配属 | ACTIVE | APPROVED | EMP000011 | 2021-03-25 10:00:00 |
| EMP000002 | DEPT003 | SECONDARY | 2023-01-01 | None | 20.0 | プロジェクト支援 | EMP000012 | プロジェクト支援のため兼務 | ACTIVE | APPROVED | EMP000012 | 2022-12-20 14:00:00 |

## 特記事項

- 社員は複数部署に同時所属可能（兼務対応）
- PRIMARY配属は社員につき1つのみ
- 配属比率の合計は100%を超えないよう運用で管理
- 部署異動時は前の配属のend_dateを設定し、新しい配属レコードを作成
- 承認フローにより配属変更を管理
- 論理削除は is_deleted フラグで管理
- 履歴管理により組織変更の追跡が可能

## 業務ルール

- 社員は必ず1つのPRIMARY配属を持つ必要がある
- SECONDARY配属（兼務）は複数設定可能
- TEMPORARY配属は期間限定の一時配属
- 配属変更は承認者の承認が必要
- 配属比率の合計は100%以下とする
- 部署異動時は履歴として前の配属を残す
- 報告先上司は配属先部署の社員である必要がある
- 配属終了日は配属開始日以降である必要がある

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 社員部署関連テーブルの詳細定義 |
