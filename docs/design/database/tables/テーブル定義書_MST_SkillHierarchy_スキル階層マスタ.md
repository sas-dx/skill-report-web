# テーブル定義書: MST_SkillHierarchy

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_SkillHierarchy |
| 論理名 | スキル階層マスタ |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-01 20:40:25 |

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
| id | ID | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  | マルチテナント識別子 |
| skill_id | スキルID | VARCHAR | 50 | ○ |  | スキル項目のID（MST_SkillItemへの外部キー） |
| parent_skill_id | 親スキルID | VARCHAR | 50 | ○ |  | 親スキルのID（MST_SkillHierarchyへの自己参照外部キー、NULLの場合はルートスキル） |
| hierarchy_level | 階層レベル | INTEGER |  | ○ |  | 階層の深さ（1:大分類、2:中分類、3:小分類、最大5階層まで） |
| skill_path | スキルパス | VARCHAR | 500 | ○ |  | ルートからのスキルパス（例：/技術スキル/プログラミング/Java） |
| sort_order | 表示順序 | INTEGER |  | ○ | 0 | 同一階層内での表示順序 |
| is_leaf | 末端フラグ | BOOLEAN |  | ○ | True | 末端ノード（子を持たない）かどうか |
| skill_category | スキルカテゴリ | ENUM |  | ○ |  | スキルの大分類（TECHNICAL:技術、BUSINESS:ビジネス、CERTIFICATION:資格、SOFT:ソフトスキル） |
| description | 説明 | TEXT |  | ○ |  | スキル階層の詳細説明 |
| is_active | 有効フラグ | BOOLEAN |  | ○ | True | 階層が有効かどうか |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  | レコード更新者のユーザーID |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_skill_id | skill_id | × | スキルID検索用 |
| idx_parent_skill | parent_skill_id | × | 親スキル検索用 |
| idx_hierarchy_level | hierarchy_level | × | 階層レベル検索用 |
| idx_skill_path | skill_path | × | スキルパス検索用 |
| idx_category_level | skill_category, hierarchy_level | × | カテゴリ別階層検索用 |
| idx_parent_sort | parent_skill_id, sort_order | × | 親スキル内での順序検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_hierarchy_skill | skill_id | MST_SkillItem | id | CASCADE | CASCADE | スキル項目への外部キー |
| fk_hierarchy_parent | parent_skill_id | MST_SkillHierarchy | skill_id | CASCADE | CASCADE | 親スキルへの自己参照外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_skill_hierarchy | UNIQUE |  | スキルと親スキルの組み合わせ一意制約 |
| chk_hierarchy_level | CHECK | hierarchy_level >= 1 AND hierarchy_level <= 5 | 階層レベル範囲チェック制約 |
| chk_skill_category | CHECK | skill_category IN ('TECHNICAL', 'BUSINESS', 'CERTIFICATION', 'SOFT') | スキルカテゴリ値チェック制約 |
| chk_no_self_reference | CHECK | skill_id != parent_skill_id | 自己参照防止制約 |

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
