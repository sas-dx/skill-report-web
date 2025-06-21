# テーブル定義書: SYS_SkillMatrix

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | SYS_SkillMatrix |
| 論理名 | スキルマップ |
| カテゴリ | システム系 |
| 生成日時 | 2025-06-21 17:20:35 |

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
| employee_id |  | VARCHAR |  | ○ |  |  |
| skill_id |  | VARCHAR |  | ○ |  |  |
| skill_level |  | INTEGER |  | ○ | 1 |  |
| self_assessment |  | INTEGER |  | ○ |  |  |
| manager_assessment |  | INTEGER |  | ○ |  |  |
| peer_assessment |  | INTEGER |  | ○ |  |  |
| assessment_date |  | DATE |  | ○ |  |  |
| evidence_url |  | VARCHAR |  | ○ |  |  |
| notes |  | TEXT |  | ○ |  |  |
| next_target_level |  | INTEGER |  | ○ |  |  |
| target_date |  | DATE |  | ○ |  |  |
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_SYS_SkillMatrix_employee_skill | employee_id, skill_id | ○ |  |
| idx_SYS_SkillMatrix_employee_id | employee_id | × |  |
| idx_SYS_SkillMatrix_skill_id | skill_id | × |  |
| idx_SYS_SkillMatrix_assessment_date | assessment_date | × |  |
| idx_SYS_SkillMatrix_skill_level | skill_level | × |  |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_sys_skillmatrix | PRIMARY KEY | id | 主キー制約 |
| chk_skill_level | CHECK | skill_level > 0 | skill_level正値チェック制約 |
| chk_next_target_level | CHECK | next_target_level > 0 | next_target_level正値チェック制約 |

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