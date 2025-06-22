# テーブル定義書: MST_SkillHierarchy

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_SkillHierarchy |
| 論理名 | スキル階層マスタ |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 22:02:18 |

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
| skillhierarchy_id | MST_SkillHierarchyの主キー | SERIAL |  | × |  | MST_SkillHierarchyの主キー |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_mst_skillhierarchy_tenant_id | tenant_id | × | テナントID検索用インデックス |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_hierarchy_skill | None | None | None | CASCADE | CASCADE | 外部キー制約 |
| fk_hierarchy_parent | None | None | None | CASCADE | CASCADE | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_mst_skillhierarchy | PRIMARY KEY | skillhierarchy_id | 主キー制約 |

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