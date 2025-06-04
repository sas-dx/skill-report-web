# テーブル定義書: TRN_EmployeeSkillGrade

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | TRN_EmployeeSkillGrade |
| 論理名 | 社員スキルグレード |
| カテゴリ | トランザクション系 |
| 生成日時 | 2025-06-04 06:57:02 |

## 概要

TRN_EmployeeSkillGrade（社員スキルグレード）は、社員が職種ごとに持つスキルグレード情報を管理するトランザクションテーブルです。

主な目的：
- 社員の職種別スキルグレードの管理
- スキルグレードの履歴管理（昇格・降格の記録）
- 有効期間による時系列管理
- 人事評価・昇進判定の基礎データ提供
- スキル分析・レポート作成の基盤
- 組織のスキル可視化・最適化支援

このテーブルは、人事評価、キャリア開発、組織分析など、スキル管理の中核となる重要なデータです。



## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | 対象社員のID（MST_Employeeへの外部キー） |
| job_type_id | 職種ID | VARCHAR | 50 | ○ |  | 対象職種のID（MST_JobTypeへの外部キー） |
| skill_grade | スキルグレード | VARCHAR | 10 | ○ |  | スキルグレード値（例：S, A, B, C, D または 1, 2, 3, 4, 5） |
| skill_level | スキルレベル | INT |  | ○ |  | スキルレベル（数値表現、1-5の範囲） |
| effective_date | 有効開始日 | DATE |  | ○ |  | スキルグレードの有効開始日 |
| expiry_date | 有効終了日 | DATE |  | ○ |  | スキルグレードの有効終了日（NULL=現在有効） |
| evaluation_date | 評価日 | DATE |  | ○ |  | スキルグレードが評価・決定された日 |
| evaluator_id | 評価者ID | VARCHAR | 50 | ○ |  | 評価を行った社員のID（MST_Employeeへの外部キー） |
| evaluation_comment | 評価コメント | TEXT |  | ○ |  | 評価に関するコメント・備考 |
| certification_flag | 認定フラグ | BOOLEAN |  | ○ | False | 公式認定されたスキルグレードかどうか |
| next_evaluation_date | 次回評価予定日 | DATE |  | ○ |  | 次回スキル評価の予定日 |
| id | ID | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  | マルチテナント識別子 |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  | レコード更新者のユーザーID |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_employee_job_effective | employee_id, job_type_id, effective_date | × | 社員・職種・有効日検索用 |
| idx_employee_current | employee_id, expiry_date | × | 社員の現在有効なスキルグレード検索用 |
| idx_job_type_grade | job_type_id, skill_grade | × | 職種別スキルグレード検索用 |
| idx_evaluation_date | evaluation_date | × | 評価日検索用 |
| idx_next_evaluation | next_evaluation_date | × | 次回評価予定日検索用 |
| idx_certification | certification_flag | × | 認定フラグ検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_skill_grade_employee | employee_id | MST_Employee | id | CASCADE | CASCADE | 社員への外部キー |
| fk_skill_grade_job_type | job_type_id | MST_JobType | id | CASCADE | RESTRICT | 職種への外部キー |
| fk_skill_grade_evaluator | evaluator_id | MST_Employee | id | CASCADE | SET NULL | 評価者への外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_employee_job_effective | UNIQUE |  | 社員・職種・有効開始日の組み合わせ一意制約 |
| chk_skill_grade | CHECK | skill_grade IN ('S', 'A', 'B', 'C', 'D') OR skill_grade IN ('1', '2', '3', '4', '5') | スキルグレード値チェック制約 |
| chk_skill_level | CHECK | skill_level IS NULL OR (skill_level >= 1 AND skill_level <= 5) | スキルレベル範囲チェック制約 |
| chk_date_range | CHECK | expiry_date IS NULL OR effective_date <= expiry_date | 有効期間の整合性チェック制約 |
| chk_evaluation_date | CHECK | evaluation_date IS NULL OR evaluation_date <= effective_date | 評価日と有効開始日の整合性チェック制約 |

## サンプルデータ

| employee_id | job_type_id | skill_grade | skill_level | effective_date | expiry_date | evaluation_date | evaluator_id | evaluation_comment | certification_flag | next_evaluation_date |
|------|------|------|------|------|------|------|------|------|------|------|
| EMP000001 | JOB001 | A | 4 | 2024-04-01 | None | 2024-03-15 | EMP000010 | 優秀な技術力と指導力を発揮している | True | 2025-04-01 |
| EMP000002 | JOB002 | B | 3 | 2024-04-01 | None | 2024-03-20 | EMP000001 | 着実にスキルアップしており、次のレベルが期待される | True | 2025-04-01 |
| EMP000001 | JOB001 | B | 3 | 2023-04-01 | 2024-03-31 | 2023-03-15 | EMP000010 | 前年度からの成長が顕著 | True | 2024-04-01 |

## 特記事項

- 同一社員・同一職種で有効期間が重複しないよう制御
- 現在有効なスキルグレードは expiry_date が NULL
- スキルグレードの履歴は物理削除せず保持
- 評価者は上司または人事担当者のみ設定可能
- 認定フラグは公式評価による正式なグレードを示す
- 次回評価予定日は自動リマインダー機能で使用

## 業務ルール

- 同一社員・同一職種で有効期間の重複は禁止
- 新しいスキルグレード設定時は前のレコードの expiry_date を自動更新
- スキルグレード変更は評価者の承認が必要
- 認定フラグが true のレコードのみ公式スキルグレードとして扱う
- 評価日は有効開始日以前である必要がある
- 次回評価予定日は通常1年後に設定
- スキルグレード S > A > B > C > D の順で上位
- スキルレベル 5 > 4 > 3 > 2 > 1 の順で上位

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 社員スキルグレードテーブルの詳細定義 |
