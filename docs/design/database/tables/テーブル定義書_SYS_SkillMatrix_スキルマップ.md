# テーブル定義書: SYS_SkillMatrix

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | SYS_SkillMatrix |
| 論理名 | スキルマップ |
| カテゴリ | システム系 |
| 生成日時 | 2025-06-24 23:02:19 |

## 概要

スキルマップテーブルは、社員のスキル評価とスキル項目の関連を管理するシステムテーブルです。
主な目的：
- 社員とスキル項目の多対多関係を管理
- スキル評価レベルの記録
- スキル評価履歴の管理
このテーブルは、スキル管理システムの中核となるテーブルで、
社員のスキル可視化やスキル分析の基盤データを提供します。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| assessment_date | 評価日 | DATE |  | ○ |  | 評価日 |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | 社員ID |
| evidence_url | 根拠URL | VARCHAR | 500 | ○ |  | 根拠URL |
| manager_assessment | 上司評価 | INTEGER |  | ○ |  | 上司評価 |
| next_target_level | 次回目標レベル | INTEGER |  | ○ |  | 次回目標レベル |
| notes | 備考 | TEXT |  | ○ |  | 備考 |
| peer_assessment | 同僚評価 | INTEGER |  | ○ |  | 同僚評価 |
| self_assessment | 自己評価 | INTEGER |  | ○ |  | 自己評価 |
| skill_id | スキルID | VARCHAR | 50 | ○ |  | スキルID |
| skill_level | スキルレベル | INTEGER |  | ○ | 1 | スキルレベル |
| skillmatrix_id | SYS_SkillMatrixの主キー | SERIAL |  | × |  | SYS_SkillMatrixの主キー |
| target_date | 目標達成日 | DATE |  | ○ |  | 目標達成日 |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_SYS_SkillMatrix_employee_skill | employee_id, skill_id | ○ |  |
| idx_SYS_SkillMatrix_employee_id | employee_id | × |  |
| idx_SYS_SkillMatrix_skill_id | skill_id | × |  |
| idx_SYS_SkillMatrix_assessment_date | assessment_date | × |  |
| idx_SYS_SkillMatrix_skill_level | skill_level | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_SYS_SkillMatrix_employee | employee_id | MST_Employee | id | CASCADE | CASCADE | 外部キー制約 |
| fk_SYS_SkillMatrix_skill | skill_id | MST_Skill | id | CASCADE | CASCADE | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| chk_next_target_level | CHECK | next_target_level > 0 | next_target_level正値チェック制約 |
| chk_skill_level | CHECK | skill_level > 0 | skill_level正値チェック制約 |

## サンプルデータ

| employee_id | skill_id | skill_level | self_assessment | manager_assessment | peer_assessment | assessment_date | evidence_url | notes | next_target_level | target_date |
|------|------|------|------|------|------|------|------|------|------|------|
| EMP001 | SKILL001 | 3 | 3 | 3 | 2 | 2024-01-15 | https://example.com/project/web-app | Webアプリケーション開発プロジェクトでReactを使用 | 4 | 2024-06-30 |
| EMP001 | SKILL002 | 2 | 2 | 2 | 3 | 2024-01-15 | None | 基本的なPython開発は可能、フレームワーク経験が少ない | 3 | 2024-09-30 |

## 特記事項

- 社員とスキルの組み合わせは一意である必要がある
- スキルレベルは1-5の範囲で管理（1:初級、2:中級、3:上級、4:エキスパート、5:マスター）
- 自己評価、上司評価、同僚評価は任意項目
- 評価の根拠となる資料やプロジェクトのURLを記録可能
- 次回の目標レベルと達成予定日を設定可能
- 論理削除は is_deleted フラグで管理
- 同一社員・同一スキルの組み合わせは1レコードのみ
- スキルレベルは必須、その他の評価は任意
- 評価日は必須項目
- 目標達成日は評価日以降の日付のみ設定可能
- スキル評価の更新時は履歴として別テーブルに保存
- 削除時は論理削除を使用し、物理削除は行わない

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | システム | 初版作成 - SYS_SkillMatrixの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214007 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214907 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215000 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215054 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223433 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |