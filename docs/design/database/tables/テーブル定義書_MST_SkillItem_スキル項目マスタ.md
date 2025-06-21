# テーブル定義書: MST_SkillItem

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_SkillItem |
| 論理名 | スキル項目マスタ |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 17:20:34 |

## 概要

MST_SkillItem（スキル項目マスタ）は、組織で管理・評価対象となるスキル項目の詳細情報を管理するマスタテーブルです。
主な目的：
- スキル項目の体系的管理（技術スキル、ビジネススキル、資格等）
- スキル評価基準の標準化（レベル定義、評価指標等）
- スキルカテゴリ・分類の階層管理
- 人材育成計画・研修プログラムの基盤
- プロジェクトアサインメント・スキルマッチングの基礎
- 組織スキル分析・可視化の基盤
- 外部資格・認定との連携管理
このテーブルは、人材のスキル管理、キャリア開発、組織能力分析など、
戦略的人材マネジメントの基盤となる重要なマスタデータです。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| skill_code |  | VARCHAR |  | ○ |  |  |
| skill_name |  | VARCHAR |  | ○ |  |  |
| skill_category_id |  | VARCHAR |  | ○ |  |  |
| skill_type |  | ENUM |  | ○ |  |  |
| difficulty_level |  | INT |  | ○ |  |  |
| importance_level |  | INT |  | ○ |  |  |
| created_at | レコード作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | レコード更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_skill_code | skill_code | ○ |  |
| idx_skill_category | skill_category_id | × |  |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_skill_code | UNIQUE |  | skill_code一意制約 |
| chk_skill_type | CHECK | skill_type IN (...) | skill_type値チェック制約 |
| chk_difficulty_level | CHECK | difficulty_level > 0 | difficulty_level正値チェック制約 |
| chk_importance_level | CHECK | importance_level > 0 | importance_level正値チェック制約 |

## サンプルデータ

| skill_code | skill_name | skill_category_id | skill_type | difficulty_level | importance_level |
|------|------|------|------|------|------|
| SKILL001 | Java | CAT001 | TECHNICAL | 3 | 4 |

## 特記事項

- スキル項目は階層構造で管理
- 評価基準は標準化されたレベル定義を使用

## 業務ルール

- スキルコードは自動採番（SKILL + 3桁連番）
- 重要度・難易度は1-5の5段階評価

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - スキル項目マスタテーブルの詳細定義 |