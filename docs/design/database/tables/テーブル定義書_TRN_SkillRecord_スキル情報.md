# テーブル定義書: TRN_SkillRecord

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | TRN_SkillRecord |
| 論理名 | スキル情報 |
| カテゴリ | トランザクション系 |
| 生成日時 | 2025-06-04 06:57:02 |

## 概要

TRN_SkillRecord（スキル情報）は、組織内の全社員が保有するスキル・技術・資格等の詳細情報を管理するトランザクションテーブルです。

主な目的：
- 社員個人のスキルポートフォリオ管理（技術スキル、ビジネススキル、資格等）
- スキルレベルの客観的評価・管理（5段階評価システム）
- 自己評価と上司評価による多面的スキル評価
- プロジェクトアサインメントのためのスキルマッチング
- 人材育成計画・キャリア開発支援
- 組織全体のスキル可視化・分析
- 資格取得状況・有効期限管理

このテーブルは、人材配置の最適化、教育研修計画の策定、組織のスキルギャップ分析など、
戦略的人材マネジメントの基盤となる重要なデータを提供します。



## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | スキルを保有する社員のID（MST_Employeeへの外部キー） |
| skill_item_id | スキル項目ID | VARCHAR | 50 | ○ |  | スキル項目のID（MST_SkillItemへの外部キー） |
| skill_level | スキルレベル | INT |  | ○ |  | スキルレベル（1:初級、2:中級、3:上級、4:エキスパート、5:マスター） |
| self_assessment | 自己評価 | INT |  | ○ |  | 自己評価（1-5段階） |
| manager_assessment | 上司評価 | INT |  | ○ |  | 上司による評価（1-5段階） |
| evidence_description | 証跡説明 | TEXT |  | ○ |  | スキル習得の証跡や根拠の説明 |
| acquisition_date | 習得日 | DATE |  | ○ |  | スキルを習得した日付 |
| last_used_date | 最終使用日 | DATE |  | ○ |  | スキルを最後に使用した日付 |
| expiry_date | 有効期限 | DATE |  | ○ |  | スキルの有効期限（資格等の場合） |
| certification_id | 関連資格ID | VARCHAR | 50 | ○ |  | 関連する資格のID（MST_Certificationへの外部キー） |
| skill_category_id | スキルカテゴリID | VARCHAR | 50 | ○ |  | スキルカテゴリのID（MST_SkillCategoryへの外部キー） |
| assessment_date | 評価日 | DATE |  | ○ |  | 最後に評価を行った日付 |
| assessor_id | 評価者ID | VARCHAR | 50 | ○ |  | 評価を行った人のID（MST_Employeeへの外部キー） |
| skill_status | スキル状況 | ENUM |  | ○ | ACTIVE | スキルの状況（ACTIVE:有効、EXPIRED:期限切れ、SUSPENDED:一時停止） |
| learning_hours | 学習時間 | INT |  | ○ |  | スキル習得にかけた学習時間（時間） |
| project_experience_count | プロジェクト経験回数 | INT |  | ○ |  | このスキルを使用したプロジェクトの回数 |
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
| idx_employee_skill | employee_id, skill_item_id | ○ | 社員・スキル項目の組み合わせ（一意） |
| idx_employee | employee_id | × | 社員別検索用 |
| idx_skill_item | skill_item_id | × | スキル項目別検索用 |
| idx_skill_level | skill_level | × | スキルレベル別検索用 |
| idx_skill_category | skill_category_id | × | スキルカテゴリ別検索用 |
| idx_certification | certification_id | × | 資格別検索用 |
| idx_status | skill_status | × | スキル状況別検索用 |
| idx_expiry_date | expiry_date | × | 有効期限検索用 |
| idx_assessment_date | assessment_date | × | 評価日検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_skill_employee | employee_id | MST_Employee | id | CASCADE | CASCADE | 社員への外部キー |
| fk_skill_item | skill_item_id | MST_SkillItem | id | CASCADE | CASCADE | スキル項目への外部キー |
| fk_skill_certification | certification_id | MST_Certification | id | CASCADE | SET NULL | 資格への外部キー |
| fk_skill_category | skill_category_id | MST_SkillCategory | id | CASCADE | SET NULL | スキルカテゴリへの外部キー |
| fk_skill_assessor | assessor_id | MST_Employee | id | CASCADE | SET NULL | 評価者への外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_employee_skill | UNIQUE |  | 社員・スキル項目の組み合わせ一意制約 |
| chk_skill_level | CHECK | skill_level BETWEEN 1 AND 5 | スキルレベル値チェック制約 |
| chk_self_assessment | CHECK | self_assessment IS NULL OR self_assessment BETWEEN 1 AND 5 | 自己評価値チェック制約 |
| chk_manager_assessment | CHECK | manager_assessment IS NULL OR manager_assessment BETWEEN 1 AND 5 | 上司評価値チェック制約 |
| chk_skill_status | CHECK | skill_status IN ('ACTIVE', 'EXPIRED', 'SUSPENDED') | スキル状況値チェック制約 |
| chk_learning_hours | CHECK | learning_hours IS NULL OR learning_hours >= 0 | 学習時間非負値チェック制約 |
| chk_project_count | CHECK | project_experience_count IS NULL OR project_experience_count >= 0 | プロジェクト経験回数非負値チェック制約 |

## サンプルデータ

| employee_id | skill_item_id | skill_level | self_assessment | manager_assessment | evidence_description | acquisition_date | last_used_date | expiry_date | certification_id | skill_category_id | assessment_date | assessor_id | skill_status | learning_hours | project_experience_count |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| EMP000001 | SKILL001 | 4 | 4 | 3 | Javaを使用したWebアプリケーション開発プロジェクトを3件担当 | 2020-06-01 | 2025-05-30 | None | CERT001 | CAT001 | 2025-04-01 | EMP000010 | ACTIVE | 120 | 3 |
| EMP000001 | SKILL002 | 3 | 3 | 3 | AWS環境でのインフラ構築・運用経験 | 2021-03-15 | 2025-05-25 | 2026-03-15 | CERT002 | CAT002 | 2025-04-01 | EMP000010 | ACTIVE | 80 | 2 |

## 特記事項

- 社員とスキル項目の組み合わせは一意（1人の社員が同じスキルを複数持つことはない）
- スキルレベルは1-5の5段階評価（1:初級、5:マスター）
- 自己評価と上司評価は任意項目（評価制度に応じて入力）
- 有効期限は資格系スキルの場合に設定
- 学習時間とプロジェクト経験回数は統計・分析用
- スキル状況により論理削除を実現

## 業務ルール

- スキルレベルは客観的な基準に基づいて設定
- 自己評価と上司評価の乖離が大きい場合は再評価を実施
- 有効期限が近づいた資格は自動的に通知
- 期限切れスキルは skill_status を EXPIRED に変更
- 評価は年1回以上実施することを推奨
- プロジェクト経験回数は実績管理システムと連携

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - スキル記録トランザクションテーブルの詳細定義 |
