# テーブル定義書: SYS_SkillMatrix

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | SYS_SkillMatrix |
| 論理名 | スキルマップ |
| カテゴリ | システム系 |
| 生成日時 | 2025-06-01 20:40:26 |

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
| id | ID | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | 評価対象の社員ID（MST_Employeeへの外部キー） |
| skill_id | スキルID | VARCHAR | 50 | ○ |  | スキル項目ID（MST_Skillへの外部キー） |
| skill_level | スキルレベル | INTEGER |  | ○ | 1 | スキル評価レベル（1:初級、2:中級、3:上級、4:エキスパート、5:マスター） |
| self_assessment | 自己評価 | INTEGER |  | ○ |  | 本人による自己評価レベル（1-5） |
| manager_assessment | 上司評価 | INTEGER |  | ○ |  | 上司による評価レベル（1-5） |
| peer_assessment | 同僚評価 | INTEGER |  | ○ |  | 同僚による評価レベル（1-5） |
| assessment_date | 評価日 | DATE |  | ○ |  | スキル評価を実施した日付 |
| evidence_url | 根拠URL | VARCHAR | 500 | ○ |  | スキル評価の根拠となる資料やプロジェクトのURL |
| notes | 備考 | TEXT |  | ○ |  | スキル評価に関する詳細な備考やコメント |
| next_target_level | 次回目標レベル | INTEGER |  | ○ |  | 次回評価での目標レベル（1-5） |
| target_date | 目標達成日 | DATE |  | ○ |  | 目標レベル達成予定日 |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  | レコード更新者のユーザーID |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_SYS_SkillMatrix_employee_skill | employee_id, skill_id | ○ | 社員とスキルの組み合わせ検索用（一意） |
| idx_SYS_SkillMatrix_employee_id | employee_id | × | 社員ID検索用 |
| idx_SYS_SkillMatrix_skill_id | skill_id | × | スキルID検索用 |
| idx_SYS_SkillMatrix_assessment_date | assessment_date | × | 評価日検索用 |
| idx_SYS_SkillMatrix_skill_level | skill_level | × | スキルレベル検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_SYS_SkillMatrix_employee | employee_id | MST_Employee | id | CASCADE | CASCADE | MST_Employeeへの外部キー |
| fk_SYS_SkillMatrix_skill | skill_id | MST_Skill | id | CASCADE | CASCADE | MST_Skillへの外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_SYS_SkillMatrix_employee_skill | UNIQUE |  | 社員とスキルの組み合わせ一意制約 |
| chk_SYS_SkillMatrix_skill_level | CHECK | skill_level BETWEEN 1 AND 5 | スキルレベル値チェック制約（1-5） |
| chk_SYS_SkillMatrix_self_assessment | CHECK | self_assessment IS NULL OR self_assessment BETWEEN 1 AND 5 | 自己評価値チェック制約（1-5またはNULL） |
| chk_SYS_SkillMatrix_manager_assessment | CHECK | manager_assessment IS NULL OR manager_assessment BETWEEN 1 AND 5 | 上司評価値チェック制約（1-5またはNULL） |
| chk_SYS_SkillMatrix_peer_assessment | CHECK | peer_assessment IS NULL OR peer_assessment BETWEEN 1 AND 5 | 同僚評価値チェック制約（1-5またはNULL） |
| chk_SYS_SkillMatrix_next_target_level | CHECK | next_target_level IS NULL OR next_target_level BETWEEN 1 AND 5 | 次回目標レベル値チェック制約（1-5またはNULL） |
| chk_SYS_SkillMatrix_target_date | CHECK | target_date IS NULL OR target_date >= assessment_date | 目標達成日は評価日以降チェック制約 |

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

## 業務ルール

- 同一社員・同一スキルの組み合わせは1レコードのみ
- スキルレベルは必須、その他の評価は任意
- 評価日は必須項目
- 目標達成日は評価日以降の日付のみ設定可能
- スキル評価の更新時は履歴として別テーブルに保存
- 削除時は論理削除を使用し、物理削除は行わない

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | システム | 初版作成 - SYS_SkillMatrixの詳細定義 |
