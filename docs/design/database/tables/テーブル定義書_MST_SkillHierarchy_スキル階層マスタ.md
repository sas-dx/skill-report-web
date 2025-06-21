# テーブル定義書: MST_SkillHierarchy

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_SkillHierarchy |
| 論理名 | スキル階層マスタ |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 17:20:34 |

## 概要

MST_SkillHierarchy（スキル階層マスタ）は、スキル項目間の階層関係を管理するマスタテーブルです。
主な目的：
- スキルの親子関係・階層構造の管理
- スキル分類の体系化（大分類→中分類→小分類）
- スキル検索・フィルタリングの基盤提供
- スキルマップ・スキルツリーの表示支援
- 関連スキルの推薦機能の基盤
このテーブルにより、技術スキル、ビジネススキル、資格等を体系的に分類し、
社員のスキル管理を効率的に行うことができます。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| skill_id |  | VARCHAR |  | ○ |  |  |
| parent_skill_id |  | VARCHAR |  | ○ |  |  |
| hierarchy_level |  | INTEGER |  | ○ |  |  |
| skill_path |  | VARCHAR |  | ○ |  |  |
| sort_order |  | INTEGER |  | ○ | 0 |  |
| is_leaf |  | BOOLEAN |  | ○ | True |  |
| skill_category |  | ENUM |  | ○ |  |  |
| description |  | TEXT |  | ○ |  |  |
| is_active |  | BOOLEAN |  | ○ | True |  |
| created_at | レコード作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | レコード更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_skill_id | skill_id | × |  |
| idx_parent_skill | parent_skill_id | × |  |
| idx_hierarchy_level | hierarchy_level | × |  |
| idx_skill_path | skill_path | × |  |
| idx_category_level | skill_category, hierarchy_level | × |  |
| idx_parent_sort | parent_skill_id, sort_order | × |  |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| chk_hierarchy_level | CHECK | hierarchy_level > 0 | hierarchy_level正値チェック制約 |

## サンプルデータ

| skill_id | parent_skill_id | hierarchy_level | skill_path | sort_order | is_leaf | skill_category | description | is_active |
|------|------|------|------|------|------|------|------|------|
| SKILL_TECH_001 | None | 1 | /技術スキル | 1 | False | TECHNICAL | 技術系スキルの大分類 | True |
| SKILL_PROG_001 | SKILL_TECH_001 | 2 | /技術スキル/プログラミング | 1 | False | TECHNICAL | プログラミング言語・技術 | True |
| SKILL_JAVA_001 | SKILL_PROG_001 | 3 | /技術スキル/プログラミング/Java | 1 | True | TECHNICAL | Java言語でのプログラミングスキル | True |

## 特記事項

- 階層の最大深度は5階層まで制限
- 循環参照を防ぐため、自己参照チェック制約を設定
- スキルパスは検索・表示用に事前計算して格納
- is_leafフラグは子ノード追加時に自動更新
- 論理削除は is_active フラグで管理
- 階層変更時は関連する子ノードのパス更新が必要

## 業務ルール

- ルートスキル（parent_skill_id = NULL）は各カテゴリに1つまで
- 階層レベルは親の階層レベル + 1 である必要がある
- スキルパスは親のパス + '/' + 自スキル名で構成
- 子ノードが存在する場合、is_leaf = false に自動更新
- 階層削除時は子ノードも含めて論理削除
- 同一親内での表示順序は重複可能だが、連番推奨
- スキルカテゴリは階層全体で統一する必要がある

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - スキル階層マスタテーブルの詳細定義 |