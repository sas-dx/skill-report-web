# テーブル定義書: TRN_SkillRecord

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | TRN_SkillRecord |
| 論理名 | スキル情報 |
| カテゴリ | トランザクション系 |
| 生成日時 | 2025-06-24 23:02:18 |

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
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| acquisition_date | 習得日 | DATE |  | ○ |  | 習得日 |
| assessment_date | 評価日 | DATE |  | ○ |  | 評価日 |
| assessor_id | 評価者ID | VARCHAR | 50 | ○ |  | 評価者ID |
| certification_id | 関連資格ID | VARCHAR | 50 | ○ |  | 関連資格ID |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | 社員ID |
| evidence_description | 証跡説明 | TEXT |  | ○ |  | 証跡説明 |
| expiry_date | 有効期限 | DATE |  | ○ |  | 有効期限 |
| last_used_date | 最終使用日 | DATE |  | ○ |  | 最終使用日 |
| learning_hours | 学習時間 | INT |  | ○ |  | 学習時間 |
| manager_assessment | 上司評価 | INT |  | ○ |  | 上司評価 |
| project_experience_count | プロジェクト経験回数 | INT |  | ○ |  | プロジェクト経験回数 |
| self_assessment | 自己評価 | INT |  | ○ |  | 自己評価 |
| skill_category_id | スキルカテゴリID | VARCHAR | 50 | ○ |  | スキルカテゴリID |
| skill_item_id | スキル項目ID | VARCHAR | 50 | ○ |  | スキル項目ID |
| skill_level | スキルレベル | INT |  | ○ |  | スキルレベル |
| skill_status | スキル状況 | ENUM |  | ○ | ACTIVE | スキル状況 |
| skillrecord_id | TRN_SkillRecordの主キー | SERIAL |  | × |  | TRN_SkillRecordの主キー |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| created_by | 作成者ID | VARCHAR | 50 | ○ |  | 作成者ID |
| updated_by | 更新者ID | VARCHAR | 50 | ○ |  | 更新者ID |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_employee_skill | employee_id, skill_item_id | ○ |  |
| idx_employee | employee_id | × |  |
| idx_skill_item | skill_item_id | × |  |
| idx_skill_level | skill_level | × |  |
| idx_skill_category | skill_category_id | × |  |
| idx_certification | certification_id | × |  |
| idx_status | skill_status | × |  |
| idx_expiry_date | expiry_date | × |  |
| idx_assessment_date | assessment_date | × |  |
| idx_trn_skillrecord_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_skill_employee | employee_id | MST_Employee | id | CASCADE | CASCADE | 外部キー制約 |
| fk_skill_item | skill_item_id | MST_SkillItem | id | CASCADE | CASCADE | 外部キー制約 |
| fk_skill_certification | certification_id | MST_Certification | id | CASCADE | SET NULL | 外部キー制約 |
| fk_skill_category | skill_category_id | MST_SkillCategory | id | CASCADE | SET NULL | 外部キー制約 |
| fk_skill_assessor | assessor_id | MST_Employee | id | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| chk_skill_level | CHECK | skill_level > 0 | skill_level正値チェック制約 |
| chk_skill_status | CHECK | skill_status IN (...) | skill_status値チェック制約 |

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
- スキルレベルは客観的な基準に基づいて設定
- 自己評価と上司評価の乖離が大きい場合は再評価を実施
- 有効期限が近づいた資格は自動的に通知
- 期限切れスキルは skill_status を EXPIRED に変更
- 評価は年1回以上実施することを推奨
- プロジェクト経験回数は実績管理システムと連携

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - スキル記録トランザクションテーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214007 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214908 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215001 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215054 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222632 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223433 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |