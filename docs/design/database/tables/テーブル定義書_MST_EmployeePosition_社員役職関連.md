# テーブル定義書: MST_EmployeePosition

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_EmployeePosition |
| 論理名 | 社員役職関連 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-01 20:40:25 |

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
| id | ID | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  | マルチテナント識別子 |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | 社員のID（MST_Employeeへの外部キー） |
| position_id | 役職ID | VARCHAR | 50 | ○ |  | 役職のID（MST_Positionへの外部キー） |
| appointment_type | 任命区分 | ENUM |  | ○ | PRIMARY | 任命区分（PRIMARY:主役職、ACTING:代理、CONCURRENT:兼任） |
| start_date | 任命開始日 | DATE |  | ○ |  | 役職への任命開始日 |
| end_date | 任命終了日 | DATE |  | ○ |  | 役職からの任命終了日（NULL:現在も任命中） |
| appointment_reason | 任命理由 | VARCHAR | 500 | ○ |  | 任命・昇進・降格の理由 |
| responsibility_scope | 責任範囲 | VARCHAR | 500 | ○ |  | 当該役職での責任範囲・職務内容 |
| authority_level | 権限レベル | INTEGER |  | ○ |  | 権限レベル（1-10、数値が大きいほど高権限） |
| salary_grade | 給与等級 | VARCHAR | 20 | ○ |  | 役職に対応する給与等級 |
| appointment_status | 任命状況 | ENUM |  | ○ | ACTIVE | 任命状況（ACTIVE:有効、INACTIVE:無効、SUSPENDED:停止） |
| approval_status | 承認状況 | ENUM |  | ○ | PENDING | 承認状況（APPROVED:承認済、PENDING:承認待ち、REJECTED:却下） |
| approved_by | 承認者ID | VARCHAR | 50 | ○ |  | 任命を承認した管理者のID |
| approved_at | 承認日時 | TIMESTAMP |  | ○ |  | 任命が承認された日時 |
| performance_target | 成果目標 | TEXT |  | ○ |  | 当該役職での成果目標・KPI |
| delegation_authority | 委譲権限 | TEXT |  | ○ |  | 委譲された権限の詳細（JSON形式） |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  | レコード更新者のユーザーID |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_MST_EmployeePosition_employee_id | employee_id | × | 社員ID検索用 |
| idx_MST_EmployeePosition_position_id | position_id | × | 役職ID検索用 |
| idx_MST_EmployeePosition_employee_position | employee_id, position_id | × | 社員・役職複合検索用 |
| idx_MST_EmployeePosition_appointment_type | appointment_type | × | 任命区分別検索用 |
| idx_MST_EmployeePosition_start_date | start_date | × | 任命開始日検索用 |
| idx_MST_EmployeePosition_end_date | end_date | × | 任命終了日検索用 |
| idx_MST_EmployeePosition_status | appointment_status | × | 任命状況別検索用 |
| idx_MST_EmployeePosition_authority_level | authority_level | × | 権限レベル別検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_MST_EmployeePosition_employee | employee_id | MST_Employee | id | CASCADE | CASCADE | 社員への外部キー |
| fk_MST_EmployeePosition_position | position_id | MST_Position | id | CASCADE | CASCADE | 役職への外部キー |
| fk_MST_EmployeePosition_approved_by | approved_by | MST_Employee | id | CASCADE | SET NULL | 承認者への外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_MST_EmployeePosition_employee_pos_primary | UNIQUE |  | 社員・役職・任命区分・開始日一意制約 |
| chk_MST_EmployeePosition_appointment_type | CHECK | appointment_type IN ('PRIMARY', 'ACTING', 'CONCURRENT') | 任命区分値チェック制約 |
| chk_MST_EmployeePosition_appointment_status | CHECK | appointment_status IN ('ACTIVE', 'INACTIVE', 'SUSPENDED') | 任命状況値チェック制約 |
| chk_MST_EmployeePosition_approval_status | CHECK | approval_status IN ('APPROVED', 'PENDING', 'REJECTED') | 承認状況値チェック制約 |
| chk_MST_EmployeePosition_date_range | CHECK | end_date IS NULL OR start_date <= end_date | 日付範囲整合性チェック制約 |
| chk_MST_EmployeePosition_authority_level | CHECK | authority_level IS NULL OR (authority_level >= 1 AND authority_level <= 10) | 権限レベル範囲チェック制約 |

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

## 業務ルール

- 社員は必ず1つのPRIMARY役職を持つ必要がある
- ACTING任命は期間限定の代理職務
- CONCURRENT任命は複数役職の兼任
- 役職変更は承認者の承認が必要
- 権限レベルは役職に応じて適切に設定
- 昇進時は履歴として前の任命を残す
- 給与等級は役職と連動して管理
- 任命終了日は任命開始日以降である必要がある
- 委譲権限はJSON形式で詳細な権限設定を管理

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 社員役職関連テーブルの詳細定義 |
