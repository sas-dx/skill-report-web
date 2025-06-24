# テーブル定義書: MST_EmployeePosition

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_EmployeePosition |
| 論理名 | 社員役職関連 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-24 23:02:18 |

## 概要

MST_EmployeePosition（社員役職関連）は、社員と役職の関連付けを管理するマスタテーブルです。
主な目的：
- 社員の役職任命履歴の管理
- 複数役職兼任の管理
- 昇進・降格履歴の追跡
- 役職変更時の影響範囲把握
- 役職別権限管理
- 組織階層における権限委譲の管理
このテーブルにより、社員の役職変遷を詳細に管理し、
人事評価や昇進管理の履歴を正確に追跡できます。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| appointment_reason | 任命理由 | VARCHAR | 500 | ○ |  | 任命理由 |
| appointment_status | 任命状況 | ENUM |  | ○ | ACTIVE | 任命状況 |
| appointment_type | 任命区分 | ENUM |  | ○ | PRIMARY | 任命区分 |
| approval_status | 承認状況 | ENUM |  | ○ | PENDING | 承認状況 |
| approved_at | 承認日時 | TIMESTAMP |  | ○ |  | 承認日時 |
| approved_by | 承認者ID | VARCHAR | 50 | ○ |  | 承認者ID |
| authority_level | 権限レベル | INTEGER |  | ○ |  | 権限レベル |
| delegation_authority | 委譲権限 | TEXT |  | ○ |  | 委譲権限 |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | 社員ID |
| employeeposition_id | MST_EmployeePositionの主キー | SERIAL |  | × |  | MST_EmployeePositionの主キー |
| end_date | 任命終了日 | DATE |  | ○ |  | 任命終了日 |
| performance_target | 成果目標 | TEXT |  | ○ |  | 成果目標 |
| position_id | 役職ID | VARCHAR | 50 | ○ |  | 役職ID |
| responsibility_scope | 責任範囲 | VARCHAR | 500 | ○ |  | 責任範囲 |
| salary_grade | 給与等級 | VARCHAR | 20 | ○ |  | 給与等級 |
| start_date | 任命開始日 | DATE |  | ○ |  | 任命開始日 |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_MST_EmployeePosition_employee_id | employee_id | × |  |
| idx_MST_EmployeePosition_position_id | position_id | × |  |
| idx_MST_EmployeePosition_employee_position | employee_id, position_id | × |  |
| idx_MST_EmployeePosition_appointment_type | appointment_type | × |  |
| idx_MST_EmployeePosition_start_date | start_date | × |  |
| idx_MST_EmployeePosition_end_date | end_date | × |  |
| idx_MST_EmployeePosition_status | appointment_status | × |  |
| idx_MST_EmployeePosition_authority_level | authority_level | × |  |
| idx_mst_employeeposition_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_MST_EmployeePosition_employee | employee_id | MST_Employee | id | CASCADE | CASCADE | 外部キー制約 |
| fk_MST_EmployeePosition_position | position_id | MST_Position | id | CASCADE | CASCADE | 外部キー制約 |
| fk_MST_EmployeePosition_approved_by | approved_by | MST_Employee | id | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| chk_appointment_status | CHECK | appointment_status IN (...) | appointment_status値チェック制約 |
| chk_appointment_type | CHECK | appointment_type IN (...) | appointment_type値チェック制約 |
| chk_approval_status | CHECK | approval_status IN (...) | approval_status値チェック制約 |
| chk_authority_level | CHECK | authority_level > 0 | authority_level正値チェック制約 |

## サンプルデータ

| employee_id | position_id | appointment_type | start_date | end_date | appointment_reason | responsibility_scope | authority_level | salary_grade | appointment_status | approval_status | approved_by | approved_at | performance_target | delegation_authority |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| EMP000001 | POS001 | PRIMARY | 2020-04-01 | None | 新卒入社時任命 | チーム運営、メンバー指導、プロジェクト管理 | 5 | G5 | ACTIVE | APPROVED | EMP000010 | 2020-03-25 10:00:00 | チーム生産性20%向上、メンバー育成2名 | {"budget_approval": 1000000, "hiring_authority": true, "performance_evaluation": true} |
| EMP000002 | POS002 | PRIMARY | 2021-04-01 | 2023-03-31 | 新卒入社時任命 | システム開発、技術調査 | 3 | G3 | INACTIVE | APPROVED | EMP000011 | 2021-03-25 10:00:00 | 開発効率向上、技術スキル習得 | {"code_review": true, "technical_decision": false} |
| EMP000002 | POS003 | PRIMARY | 2023-04-01 | None | 昇進による任命 | シニア開発者、技術指導、アーキテクチャ設計 | 4 | G4 | ACTIVE | APPROVED | EMP000011 | 2023-03-20 14:00:00 | 技術品質向上、後輩指導3名 | {"technical_decision": true, "architecture_review": true} |

## 特記事項

- 社員は複数役職を同時に持つことが可能（兼任対応）
- PRIMARY任命は社員につき1つのみ
- ACTING（代理）は一時的な役職代行
- CONCURRENT（兼任）は複数役職の同時保持
- 役職変更時は履歴として前の任命を残す
- 承認フローにより役職変更を管理
- 権限レベルにより システム内権限を制御
- 論理削除は is_deleted フラグで管理
- 社員は必ず1つのPRIMARY役職を持つ必要がある
- ACTING任命は期間限定の代理職務
- CONCURRENT任命は複数役職の兼任
- 役職変更は承認者の承認が必要
- 権限レベルは役職に応じて適切に設定
- 昇進時は履歴として前の任命を残す
- 給与等級は役職と連動して管理
- 任命終了日は任命開始日以降である必要がある
- 委譲権限はJSON形式で詳細な権限設定を管理

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 社員役職関連テーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214906 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_214959 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215053 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223432 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |