# テーブル定義書: TRN_EmployeeSkillGrade

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | TRN_EmployeeSkillGrade |
| 論理名 | 社員スキルグレード |
| カテゴリ | トランザクション系 |
| 生成日時 | 2025-06-24 23:05:57 |

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
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| certification_flag | 認定フラグ | BOOLEAN |  | ○ | False | 認定フラグ |
| effective_date | 有効開始日 | DATE |  | ○ |  | 有効開始日 |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | 社員ID |
| employeeskillgrade_id | TRN_EmployeeSkillGradeの主キー | SERIAL |  | × |  | TRN_EmployeeSkillGradeの主キー |
| evaluation_comment | 評価コメント | TEXT |  | ○ |  | 評価コメント |
| evaluation_date | 評価日 | DATE |  | ○ |  | 評価日 |
| evaluator_id | 評価者ID | VARCHAR | 50 | ○ |  | 評価者ID |
| expiry_date | 有効終了日 | DATE |  | ○ |  | 有効終了日 |
| job_type_id | 職種ID | VARCHAR | 50 | ○ |  | 職種ID |
| next_evaluation_date | 次回評価予定日 | DATE |  | ○ |  | 次回評価予定日 |
| skill_grade | スキルグレード | VARCHAR | 10 | ○ |  | スキルグレード |
| skill_level | スキルレベル | INT |  | ○ |  | スキルレベル |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| created_by | 作成者ID | VARCHAR | 50 | ○ |  | 作成者ID |
| updated_by | 更新者ID | VARCHAR | 50 | ○ |  | 更新者ID |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_employee_job_effective | employee_id, job_type_id, effective_date | × |  |
| idx_employee_current | employee_id, expiry_date | × |  |
| idx_job_type_grade | job_type_id, skill_grade | × |  |
| idx_evaluation_date | evaluation_date | × |  |
| idx_next_evaluation | next_evaluation_date | × |  |
| idx_certification | certification_flag | × |  |
| idx_trn_employeeskillgrade_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_skill_grade_employee | employee_id | MST_Employee | id | CASCADE | CASCADE | 外部キー制約 |
| fk_skill_grade_job_type | job_type_id | MST_JobType | id | CASCADE | RESTRICT | 外部キー制約 |
| fk_skill_grade_evaluator | evaluator_id | MST_Employee | id | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| chk_job_type_id | CHECK | job_type_id IN (...) | job_type_id値チェック制約 |
| chk_skill_level | CHECK | skill_level > 0 | skill_level正値チェック制約 |

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
- 同一社員・同一職種で有効期間の重複は禁止
- 新しいスキルグレード設定時は前のレコードの expiry_date を自動更新
- スキルグレード変更は評価者の承認が必要
- 認定フラグが true のレコードのみ公式スキルグレードとして扱う
- 評価日は有効開始日以前である必要がある
- 次回評価予定日は通常1年後に設定
- スキルグレード S > A > B > C > D の順で上位
- スキルレベル 5 > 4 > 3 > 2 > 1 の順で上位

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 社員スキルグレードテーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214007 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214908 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215001 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215054 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223433 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |