# テーブル定義書: MST_EmployeeDepartment (社員部署関連)

## 📋 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_EmployeeDepartment |
| 論理名 | 社員部署関連 |
| カテゴリ | マスタ系 |
| 作成日 | 2025-06-01 |

> **注意**: 本テーブル定義書は自動生成されます。手動編集は行わないでください。
> 詳細定義の変更は `table-details/MST_EmployeeDepartment_details.yaml` で行ってください。


## 📝 改版履歴

> **注意**: 改版履歴の詳細は以下のYAMLファイルで管理されています：
> `table-details/TABLE_NAME_details.yaml`

| バージョン | 更新日 | 更新者 | 主な変更内容 |
|------------|--------|--------|-------------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 社員部署関連テーブルの詳細定義 |


## 📝 テーブル概要

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


## 🗂️ カラム定義

| カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト | 説明 |
|----------|--------|----------|------|------|----|----|------------|------|
| id | ID | VARCHAR | 50 | × | ● |  |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × |  |  |  | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  |  |  | マルチテナント識別子 |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | ● |  | 社員のID（MST_Employeeへの外部キー） |
| department_id | 部署ID | VARCHAR | 50 | ○ |  | ● |  | 部署のID（MST_Departmentへの外部キー） |
| assignment_type | 配属区分 | ENUM |  | ○ |  |  | PRIMARY | 配属区分（PRIMARY:主配属、SECONDARY:兼務、TEMPORARY:一時配属） |
| start_date | 配属開始日 | DATE |  | ○ |  |  |  | 部署への配属開始日 |
| end_date | 配属終了日 | DATE |  | ○ |  |  |  | 部署からの配属終了日（NULL:現在も配属中） |
| assignment_ratio | 配属比率 | DECIMAL | 5,2 | ○ |  |  |  | 配属比率（%）兼務時の工数配分用 |
| role_in_department | 部署内役割 | VARCHAR | 100 | ○ |  |  |  | 部署内での役割・職責 |
| reporting_manager_id | 報告先上司ID | VARCHAR | 50 | ○ |  | ● |  | 当該部署での報告先上司ID（MST_Employeeへの外部キー） |
| assignment_reason | 配属理由 | VARCHAR | 500 | ○ |  |  |  | 配属・異動の理由 |
| assignment_status | 配属状況 | ENUM |  | ○ |  |  | ACTIVE | 配属状況（ACTIVE:有効、INACTIVE:無効、PENDING:保留） |
| approval_status | 承認状況 | ENUM |  | ○ |  |  | PENDING | 承認状況（APPROVED:承認済、PENDING:承認待ち、REJECTED:却下） |
| approved_by | 承認者ID | VARCHAR | 50 | ○ |  | ● |  | 配属を承認した管理者のID |
| approved_at | 承認日時 | TIMESTAMP |  | ○ |  |  |  | 配属が承認された日時 |
| created_at | 作成日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  |  |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  |  |  | レコード更新者のユーザーID |

## 🔍 インデックス定義

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_MST_EmployeeDepartment_employee_id | employee_id | × | 社員ID検索用 |
| idx_MST_EmployeeDepartment_department_id | department_id | × | 部署ID検索用 |
| idx_MST_EmployeeDepartment_employee_department | employee_id, department_id | × | 社員・部署複合検索用 |
| idx_MST_EmployeeDepartment_assignment_type | assignment_type | × | 配属区分別検索用 |
| idx_MST_EmployeeDepartment_start_date | start_date | × | 配属開始日検索用 |
| idx_MST_EmployeeDepartment_end_date | end_date | × | 配属終了日検索用 |
| idx_MST_EmployeeDepartment_status | assignment_status | × | 配属状況別検索用 |

## 🔒 制約定義

| 制約名 | 制約タイプ | 対象カラム | 条件 | 説明 |
|--------|------------|------------|------|------|
| uk_MST_EmployeeDepartment_employee_dept_primary | UNIQUE | employee_id, department_id, assignment_type, start_date |  | 社員・部署・配属区分・開始日一意制約 |
| chk_MST_EmployeeDepartment_assignment_type | CHECK |  | assignment_type IN ('PRIMARY', 'SECONDARY', 'TEMPORARY') | 配属区分値チェック制約 |
| chk_MST_EmployeeDepartment_assignment_status | CHECK |  | assignment_status IN ('ACTIVE', 'INACTIVE', 'PENDING') | 配属状況値チェック制約 |
| chk_MST_EmployeeDepartment_approval_status | CHECK |  | approval_status IN ('APPROVED', 'PENDING', 'REJECTED') | 承認状況値チェック制約 |
| chk_MST_EmployeeDepartment_date_range | CHECK |  | end_date IS NULL OR start_date <= end_date | 日付範囲整合性チェック制約 |
| chk_MST_EmployeeDepartment_assignment_ratio | CHECK |  | assignment_ratio IS NULL OR (assignment_ratio >= 0 AND assignment_ratio <= 100) | 配属比率範囲チェック制約 |

## 🔗 外部キー関係

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|------------|--------|--------------|------------|--------|--------|------|
| fk_MST_EmployeeDepartment_employee | employee_id | MST_Employee | id | CASCADE | CASCADE | 社員への外部キー |
| fk_MST_EmployeeDepartment_department | department_id | MST_Department | id | CASCADE | CASCADE | 部署への外部キー |
| fk_MST_EmployeeDepartment_reporting_manager | reporting_manager_id | MST_Employee | id | CASCADE | SET NULL | 報告先上司への外部キー |
| fk_MST_EmployeeDepartment_approved_by | approved_by | MST_Employee | id | CASCADE | SET NULL | 承認者への外部キー |

## 📊 サンプルデータ

```json
[
  {
    "employee_id": "EMP000001",
    "department_id": "DEPT001",
    "assignment_type": "PRIMARY",
    "start_date": "2020-04-01",
    "end_date": null,
    "assignment_ratio": 100.0,
    "role_in_department": "チームリーダー",
    "reporting_manager_id": "EMP000010",
    "assignment_reason": "新卒入社時配属",
    "assignment_status": "ACTIVE",
    "approval_status": "APPROVED",
    "approved_by": "EMP000010",
    "approved_at": "2020-03-25 10:00:00"
  },
  {
    "employee_id": "EMP000002",
    "department_id": "DEPT002",
    "assignment_type": "PRIMARY",
    "start_date": "2021-04-01",
    "end_date": null,
    "assignment_ratio": 80.0,
    "role_in_department": "開発担当",
    "reporting_manager_id": "EMP000011",
    "assignment_reason": "新卒入社時配属",
    "assignment_status": "ACTIVE",
    "approval_status": "APPROVED",
    "approved_by": "EMP000011",
    "approved_at": "2021-03-25 10:00:00"
  },
  {
    "employee_id": "EMP000002",
    "department_id": "DEPT003",
    "assignment_type": "SECONDARY",
    "start_date": "2023-01-01",
    "end_date": null,
    "assignment_ratio": 20.0,
    "role_in_department": "プロジェクト支援",
    "reporting_manager_id": "EMP000012",
    "assignment_reason": "プロジェクト支援のため兼務",
    "assignment_status": "ACTIVE",
    "approval_status": "APPROVED",
    "approved_by": "EMP000012",
    "approved_at": "2022-12-20 14:00:00"
  }
]
```

## 📌 特記事項

- 社員は複数部署に同時所属可能（兼務対応）
- PRIMARY配属は社員につき1つのみ
- 配属比率の合計は100%を超えないよう運用で管理
- 部署異動時は前の配属のend_dateを設定し、新しい配属レコードを作成
- 承認フローにより配属変更を管理
- 論理削除は is_deleted フラグで管理
- 履歴管理により組織変更の追跡が可能

## 📋 業務ルール

- 社員は必ず1つのPRIMARY配属を持つ必要がある
- SECONDARY配属（兼務）は複数設定可能
- TEMPORARY配属は期間限定の一時配属
- 配属変更は承認者の承認が必要
- 配属比率の合計は100%以下とする
- 部署異動時は履歴として前の配属を残す
- 報告先上司は配属先部署の社員である必要がある
- 配属終了日は配属開始日以降である必要がある
