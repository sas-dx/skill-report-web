# テーブル定義書: MST_SkillHierarchy

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_SkillHierarchy |
| 論理名 | スキル階層マスタ |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-24 23:05:56 |

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
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| description | 説明 | TEXT |  | ○ |  | 説明 |
| hierarchy_level | 階層レベル | INTEGER |  | ○ |  | 階層レベル |
| is_active | 有効フラグ | BOOLEAN |  | ○ | True | 有効フラグ |
| is_leaf | 末端フラグ | BOOLEAN |  | ○ | True | 末端フラグ |
| parent_skill_id | 親スキルID | VARCHAR | 50 | ○ |  | 親スキルID |
| skill_category | スキルカテゴリ | ENUM |  | ○ |  | スキルカテゴリ |
| skill_id | スキルID | VARCHAR | 50 | ○ |  | スキルID |
| skill_path | スキルパス | VARCHAR | 500 | ○ |  | スキルパス |
| skillhierarchy_id | MST_SkillHierarchyの主キー | SERIAL |  | × |  | MST_SkillHierarchyの主キー |
| sort_order | 表示順序 | INTEGER |  | ○ | 0 | 表示順序 |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_skill_id | skill_id | × |  |
| idx_parent_skill | parent_skill_id | × |  |
| idx_hierarchy_level | hierarchy_level | × |  |
| idx_skill_path | skill_path | × |  |
| idx_category_level | skill_category, hierarchy_level | × |  |
| idx_parent_sort | parent_skill_id, sort_order | × |  |
| idx_mst_skillhierarchy_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_hierarchy_skill | skill_id | MST_SkillItem | id | CASCADE | CASCADE | 外部キー制約 |
| fk_hierarchy_parent | parent_skill_id | MST_SkillHierarchy | id | CASCADE | CASCADE | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
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
- ルートスキル（parent_skill_id = NULL）は各カテゴリに1つまで
- 階層レベルは親の階層レベル + 1 である必要がある
- スキルパスは親のパス + '/' + 自スキル名で構成
- 子ノードが存在する場合、is_leaf = false に自動更新
- 階層削除時は子ノードも含めて論理削除
- 同一親内での表示順序は重複可能だが、連番推奨
- スキルカテゴリは階層全体で統一する必要がある

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - スキル階層マスタテーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214907 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215000 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215053 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223432 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |