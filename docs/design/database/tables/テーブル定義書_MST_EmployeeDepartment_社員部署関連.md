# テーブル定義書: MST_EmployeeDepartment

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_EmployeeDepartment |
| 論理名 | 社員部署関連 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-24 22:56:16 |

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
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| approval_status | 承認状況 | ENUM |  | ○ | PENDING | 承認状況 |
| approved_at | 承認日時 | TIMESTAMP |  | ○ |  | 承認日時 |
| approved_by | 承認者ID | VARCHAR | 50 | ○ |  | 承認者ID |
| assignment_ratio | 配属比率 | DECIMAL | 5,2 | ○ |  | 配属比率 |
| assignment_reason | 配属理由 | VARCHAR | 500 | ○ |  | 配属理由 |
| assignment_status | 配属状況 | ENUM |  | ○ | ACTIVE | 配属状況 |
| assignment_type | 配属区分 | ENUM |  | ○ | PRIMARY | 配属区分 |
| department_id | 部署ID | VARCHAR | 50 | ○ |  | 部署ID |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | 社員ID |
| employeedepartment_id | MST_EmployeeDepartmentの主キー | SERIAL |  | × |  | MST_EmployeeDepartmentの主キー |
| end_date | 配属終了日 | DATE |  | ○ |  | 配属終了日 |
| reporting_manager_id | 報告先上司ID | VARCHAR | 50 | ○ |  | 報告先上司ID |
| role_in_department | 部署内役割 | VARCHAR | 100 | ○ |  | 部署内役割 |
| start_date | 配属開始日 | DATE |  | ○ |  | 配属開始日 |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

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
| idx_mst_employeedepartment_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_MST_EmployeeDepartment_employee | employee_id | MST_Employee | id | CASCADE | CASCADE | 外部キー制約 |
| fk_MST_EmployeeDepartment_department | department_id | MST_Department | id | CASCADE | CASCADE | 外部キー制約 |
| fk_MST_EmployeeDepartment_reporting_manager | reporting_manager_id | MST_Employee | id | CASCADE | SET NULL | 外部キー制約 |
| fk_MST_EmployeeDepartment_approved_by | approved_by | MST_Employee | id | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| chk_approval_status | CHECK | approval_status IN (...) | approval_status値チェック制約 |
| chk_assignment_status | CHECK | assignment_status IN (...) | assignment_status値チェック制約 |
| chk_assignment_type | CHECK | assignment_type IN (...) | assignment_type値チェック制約 |

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
- 社員は必ず1つのPRIMARY配属を持つ必要がある
- SECONDARY配属（兼務）は複数設定可能
- TEMPORARY配属は期間限定の一時配属
- 配属変更は承認者の承認が必要
- 配属比率の合計は100%以下とする
- 部署異動時は履歴として前の配属を残す
- 報告先上司は配属先部署の社員である必要がある
- 配属終了日は配属開始日以降である必要がある

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 社員部署関連テーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214906 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_214959 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215052 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223432 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |