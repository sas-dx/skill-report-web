# テーブル定義書: MST_EmployeeDepartment

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_EmployeeDepartment |
| 論理名 | 社員部署関連 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 17:20:34 |

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
| employee_id |  | VARCHAR |  | ○ |  |  |
| department_id |  | VARCHAR |  | ○ |  |  |
| assignment_type |  | ENUM |  | ○ | PRIMARY |  |
| start_date |  | DATE |  | ○ |  |  |
| end_date |  | DATE |  | ○ |  |  |
| assignment_ratio |  | DECIMAL |  | ○ |  |  |
| role_in_department |  | VARCHAR |  | ○ |  |  |
| reporting_manager_id |  | VARCHAR |  | ○ |  |  |
| assignment_reason |  | VARCHAR |  | ○ |  |  |
| assignment_status |  | ENUM |  | ○ | ACTIVE |  |
| approval_status |  | ENUM |  | ○ | PENDING |  |
| approved_by |  | VARCHAR |  | ○ |  |  |
| approved_at |  | TIMESTAMP |  | ○ |  |  |
| created_at | レコード作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | レコード更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_MST_EmployeeDepartment_employee_id | employee_id | × |  |
| idx_MST_EmployeeDepartment_department_id | department_id | × |  |
| idx_MST_EmployeeDepartment_employee_department | employee_id, department_id | × |  |
| idx_MST_EmployeeDepartment_assignment_type | assignment_type | × |  |
| idx_MST_EmployeeDepartment_start_date | start_date | × |  |
| idx_MST_EmployeeDepartment_end_date | end_date | × |  |
| idx_MST_EmployeeDepartment_status | assignment_status | × |  |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| chk_assignment_type | CHECK | assignment_type IN (...) | assignment_type値チェック制約 |
| chk_assignment_status | CHECK | assignment_status IN (...) | assignment_status値チェック制約 |
| chk_approval_status | CHECK | approval_status IN (...) | approval_status値チェック制約 |

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